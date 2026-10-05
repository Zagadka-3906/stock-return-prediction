"""Past-only streamed logistic classification of supplied one-day rank labels."""
from pathlib import Path
import gc
import hashlib
import json
import os
import time

for variable in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'POLARS_MAX_THREADS'):
    os.environ[variable] = '2'

ROOT = Path(__file__).resolve().parents[1]
FEATURE_FILE = ROOT / 'data/features.parquet'
MANIFEST = ROOT / 'data/feature_manifest.json'
OUT = ROOT / 'analysis/streaming_rank_classification_bank_v2_20261005'
BASELINE = ROOT / 'analysis/linear_bank_20261003/rank_ridge_l01'
YEARS = (2020, 2021, 2022, 2023, 2024)
KEYS = ['ts_code', 'trade_date']
CONFIGS = {f'rank_{objective}_sgd_{suffix}_e32': {
    'kind': 'streaming_rank_classifier', 'target': 'y_rank', 'rank_objective': objective,
    'alpha': alpha, 'epochs': 32, 'chunk_rows': 65536, 'clip_z': 8.,
    'learning_rate': 'invscaling', 'eta0': .01, 'power_t': .25, 'average': True,
    'shuffle': False, 'seed': 20261005, 'n_jobs': 1}
    for objective in ('top10', 'decile') for suffix, alpha in (('l2e4', .0001), ('l2e3', .001))}


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def dump(path, payload, immutable=False):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x' if immutable else 'w', encoding='utf-8') as stream:
        json.dump(payload, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def log(message):
    print(f'[{time.strftime("%H:%M:%S")}] {message}', flush=True)


def feature_names():
    return read(MANIFEST)['features']


def cutoff(year):
    return read(BASELINE / f'info_{year}.json')['training_meta']['cutoff_exclusive']


def scanner(columns, condition, chunk_rows=65536, source=FEATURE_FILE):
    import pyarrow.dataset as ds
    options = ds.ParquetFragmentScanOptions(pre_buffer=False, use_buffered_stream=True, buffer_size=2**20)
    format = ds.ParquetFileFormat(default_fragment_scan_options=options)
    data = ds.dataset(source, format=format)
    return data.scanner(columns=columns, filter=condition, batch_size=chunk_rows,
                        batch_readahead=0, fragment_readahead=0, use_threads=False).to_batches()


def training_condition(cutoff_exclusive):
    import pyarrow.dataset as ds
    rank = ds.field('y_rank')
    return ((ds.field('is_train') == True) & (ds.field('price_valid') == True)
            & (ds.field('trade_date') < cutoff_exclusive) & rank.is_valid()
            & (rank < float('inf')) & (rank > float('-inf')))


def matrix(batch, features):
    import numpy as np
    return np.ascontiguousarray(np.column_stack([
        batch.column(name).to_numpy(zero_copy_only=False) for name in features]), dtype=np.float32)


def learned_rank_thresholds(y, cfg):
    import numpy as np
    y = np.asarray(y, dtype=np.float64)
    assert np.isfinite(y).all() and len(y)
    quantiles = [.9] if cfg['rank_objective'] == 'top10' else np.arange(1, 10) / 10
    return np.quantile(y, quantiles)


def rank_classes(y, cfg, thresholds):
    import numpy as np
    y = np.asarray(y, dtype=np.float64)
    assert np.isfinite(y).all()
    assert len(thresholds) == (1 if cfg['rank_objective'] == 'top10' else 9)
    return np.searchsorted(thresholds, y, side='right').astype(np.int64)


def classes(cfg):
    import numpy as np
    return np.arange(2 if cfg['rank_objective'] == 'top10' else 10, dtype=np.int64)


def new_classifier(cfg):
    from sklearn.linear_model import SGDClassifier
    return SGDClassifier(loss='log_loss', penalty='l2', alpha=cfg['alpha'],
        fit_intercept=True, learning_rate=cfg['learning_rate'], eta0=cfg['eta0'],
        power_t=cfg['power_t'], average=cfg['average'], shuffle=cfg['shuffle'],
        random_state=cfg['seed'], n_jobs=cfg['n_jobs'], early_stopping=False, tol=None)


def finite_values(x):
    import numpy as np
    values = np.asarray(x, dtype=np.float64)
    return np.where(np.isfinite(values), values, np.nan)


class RunningStats:
    """Finite per-column Chan moments, including initially all-missing columns."""
    def __init__(self):
        self.count = self.mean_ = self.m2 = None

    def partial_fit(self, x):
        import numpy as np
        values = np.asarray(x, dtype=np.float64)
        finite = np.isfinite(values)
        count = finite.sum(axis=0)
        total = np.where(finite, values, 0.).sum(axis=0)
        mean = np.divide(total, count, out=np.zeros(values.shape[1]), where=count > 0)
        centered = np.where(finite, values - mean, 0.)
        m2 = np.square(centered).sum(axis=0)
        if self.count is None:
            self.count, self.mean_, self.m2 = count.copy(), mean.copy(), m2.copy()
            return
        combined = self.count + count
        mask = count > 0
        delta = mean[mask] - self.mean_[mask]
        self.m2[mask] += m2[mask] + np.square(delta) * self.count[mask] * count[mask] / combined[mask]
        self.mean_[mask] += delta * count[mask] / combined[mask]
        self.count = combined

    @property
    def scale_(self):
        import numpy as np
        variance = np.divide(self.m2, self.count, out=np.zeros_like(self.m2), where=self.count > 0)
        return np.sqrt(np.maximum(variance, 0.))


def transform(x, mean, scale, clip=8.):
    import numpy as np
    values = np.asarray(x, dtype=np.float64)
    return np.ascontiguousarray(np.clip((np.where(np.isfinite(values), values, mean) - mean) / scale, -clip, clip))


def build_bundle(model, scaler, cfg, rows, steps, thresholds):
    import numpy as np
    mean = np.where(np.isfinite(scaler.mean_), scaler.mean_, 0.)
    scale = np.where(np.isfinite(scaler.scale_) & (scaler.scale_ > 1e-5), scaler.scale_, 1.)
    assert np.isfinite(model.coef_).all() and np.isfinite(model.intercept_).all()
    assert model.t_ == 1 + rows * cfg['epochs']
    return {'kind': 'streaming_rank_classifier', 'classifier': model, 'mean': mean, 'scale': scale,
            'config': dict(cfg), 'class_thresholds': thresholds, 'completed_epochs': cfg['epochs'], 'training_rows': rows,
            'actual_partial_fit_calls': steps, 'actual_native_sample_counter': float(model.t_),
            'class_count': len(model.classes_), 'target_units': 'classification_score_requires_past_return_mapping',
            'training_row_order': 'frozen_Parquet_physical_order_after_past_mature_filter',
            'no_validation_early_stopping': True, 'training_device': 'cpu'}


def fit_arrays(x, y, cfg):
    """Small-control path using precisely the same partial_fit and preprocessing."""
    scaler = RunningStats()
    thresholds = learned_rank_thresholds(y, cfg)
    chunk = cfg['chunk_rows']
    for offset in range(0, len(y), chunk):
        scaler.partial_fit(finite_values(x[offset:offset + chunk]))
    import numpy as np
    mean = np.where(np.isfinite(scaler.mean_), scaler.mean_, 0.)
    scale = np.where(np.isfinite(scaler.scale_) & (scaler.scale_ > 1e-5), scaler.scale_, 1.)
    model = new_classifier(cfg)
    steps = 0
    for _ in range(cfg['epochs']):
        for offset in range(0, len(y), chunk):
            block = x[offset:offset + chunk]
            model.partial_fit(transform(block, mean, scale, cfg['clip_z']), rank_classes(y[offset:offset + len(block)], cfg, thresholds),
                              classes=classes(cfg))
            steps += 1
    return build_bundle(model, scaler, cfg, len(y), steps, thresholds)


def predict_arrays(bundle, x):
    """Fixed per-row reductions reproduce native OvR logistic probabilities."""
    import numpy as np
    from scipy.special import expit
    assert bundle['kind'] == 'streaming_rank_classifier'
    classifier, cfg = bundle['classifier'], bundle['config']
    parts = []
    for offset in range(0, len(x), cfg['chunk_rows']):
        values = transform(x[offset:offset + cfg['chunk_rows']], bundle['mean'], bundle['scale'], cfg['clip_z'])
        decisions = np.einsum('ij,kj->ik', values, classifier.coef_, optimize=False) + classifier.intercept_
        probabilities = expit(decisions)
        if cfg['rank_objective'] == 'top10':
            score = probabilities[:, 0]
        else:
            denominator = probabilities.sum(axis=1, keepdims=True)
            assert np.all(denominator > 0)
            probabilities /= denominator
            centers = (classifier.classes_.astype(np.float64) + .5) / 10
            score = np.einsum('ij,j->i', probabilities, centers, optimize=False)
        assert np.isfinite(score).all()
        parts.append(score)
    return np.concatenate(parts) if parts else np.empty(0, dtype=np.float64)


def save_bundle(path, bundle):
    import joblib
    joblib.dump(bundle, path, compress=3)


def load_bundle(path):
    import joblib
    return joblib.load(path)


def fit_stream(year, cfg, source=FEATURE_FILE, limit_rows=None):
    import numpy as np
    import polars as pl
    features = feature_names()
    stop = cutoff(year)
    condition = training_condition(stop)
    columns = KEYS + ['y_rank'] + features
    scaler = RunningStats()
    rows, dates, key_hashes = 0, set(), []
    target_values = []
    matrix_hash, target_hash = hashlib.sha256(), hashlib.sha256()
    def batches():
        remaining = limit_rows
        for batch in scanner(columns, condition, cfg['chunk_rows'], source):
            if not len(batch):
                continue
            if remaining is not None:
                batch = batch.slice(0, min(len(batch), remaining))
                remaining -= len(batch)
            yield batch
            if remaining == 0:
                break
    for batch in batches():
        x = matrix(batch, features)
        y = batch.column('y_rank').to_numpy(zero_copy_only=False).astype(np.float32)
        assert np.isfinite(y).all()
        target_values.append(y.copy())
        scaler.partial_fit(finite_values(x))
        rows += len(batch)
        dates.update(batch.column('trade_date').to_pylist())
        keys = pl.from_arrow(batch.select(KEYS)).hash_rows(seed=2026).to_numpy()
        key_hashes.append(keys)
        matrix_hash.update(memoryview(x).cast('B'))
        target_hash.update(memoryview(np.ascontiguousarray(y)).cast('B'))
    assert rows
    thresholds = learned_rank_thresholds(np.concatenate(target_values), cfg)
    del target_values
    key_values = np.concatenate(key_hashes)
    key_values.sort()
    key_digest = hashlib.sha256(memoryview(key_values).cast('B')).hexdigest()
    del key_values, key_hashes, batch, x, y, keys
    gc.collect()
    mean = np.where(np.isfinite(scaler.mean_), scaler.mean_, 0.)
    scale = np.where(np.isfinite(scaler.scale_) & (scaler.scale_ > 1e-5), scaler.scale_, 1.)
    model = new_classifier(cfg)
    steps = 0
    epoch_counts = []
    for epoch in range(cfg['epochs']):
        seen = 0
        for batch in batches():
            x = matrix(batch, features)
            y = batch.column('y_rank').to_numpy(zero_copy_only=False).astype(np.float32)
            model.partial_fit(transform(x, mean, scale, cfg['clip_z']), rank_classes(y, cfg, thresholds), classes=classes(cfg))
            steps += 1
            seen += len(y)
        assert seen == rows
        epoch_counts.append(seen)
        if epoch == 0 or (epoch + 1) % 4 == 0:
            log(f"Streamed {cfg['rank_objective']} L2={cfg['alpha']} fold{year} epoch{epoch+1}/{cfg['epochs']} actual{seen} mature rows")
    meta = {'rows': rows, 'days': len(dates), 'first': min(dates), 'last': max(dates),
            'cutoff_exclusive': stop, 'validation_year': year, 'features': features,
            'physical_training_matrix_sha256': matrix_hash.hexdigest(),
            'physical_training_target_sha256': target_hash.hexdigest(),
            'sorted_training_key_hash_multiset_sha256': key_digest,
            'training_row_order': 'frozen_Parquet_physical_order_after_past_mature_filter',
            'training_matrix_hash_not_the_date_sorted_old_control_hash': True}
    baseline = read(BASELINE / f'info_{year}.json')['training_meta']
    if limit_rows is None:
        for key in ('rows', 'days', 'first', 'last', 'cutoff_exclusive', 'validation_year', 'features'):
            assert meta[key] == baseline[key], key
        expected = (pl.scan_parquet(source).filter(pl.col('is_train') & pl.col('price_valid')
            & (pl.col('trade_date') < stop) & pl.col('y_rank').is_finite()).select(KEYS)
            .collect(engine='streaming').hash_rows(seed=2026).to_numpy())
        expected.sort()
        assert hashlib.sha256(memoryview(expected).cast('B')).hexdigest() == key_digest
        meta['full_selected_row_keys_match_independent_original_filter'] = True
        meta['last_label_end'] = baseline['last_label_end']
        assert meta['last'] < stop and meta['last_label_end'] <= stop
        del expected
    return build_bundle(model, scaler, cfg, rows, steps, thresholds), meta, epoch_counts


engine = __import__('sys').modules[__name__]
