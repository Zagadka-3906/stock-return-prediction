"""Mature raw63 SGD regression: matched squared and Huber losses, no label clipping."""
from pathlib import Path
import gc
import hashlib
import numpy as np
import streaming_rank_classification_v3_20261005 as shared

ROOT, FEATURE_FILE, MANIFEST = shared.ROOT, shared.FEATURE_FILE, shared.MANIFEST
OUT = ROOT / 'analysis/streaming_robust_regression_bank_20261005'
BASELINE = shared.BASELINE
YEARS, KEYS = shared.YEARS, shared.KEYS
read, dump, sha, log = shared.read, shared.dump, shared.sha, shared.log
feature_names, scanner, matrix = shared.feature_names, shared.scanner, shared.matrix
RunningStats, finite_values, transform = shared.RunningStats, shared.finite_values, shared.transform
save_bundle, load_bundle = shared.save_bundle, shared.load_bundle
CONFIGS = {f'{label}_sgd_{loss}_e32': {
    'kind': 'streaming_robust_regression', 'target': target, 'loss': loss,
    'alpha': .0001, 'epsilon': .1, 'epochs': 32, 'chunk_rows': 65536, 'clip_z': 8.,
    'learning_rate': 'invscaling', 'eta0': .01, 'power_t': .25,
    'average': True, 'shuffle': False, 'seed': 20261005,
    'target_scaling': 'mature_past_mean_std_inverse_output_no_target_clipping'}
    for label, target in (('rank', 'y_rank'), ('return', 'y_ret_1d'))
    for loss in ('squared_error', 'huber')}


def baseline_path(cfg, year):
    name = 'rank_ridge_l01' if cfg['target'] == 'y_rank' else 'return_ridge_l01'
    return ROOT / f'analysis/linear_bank_20261003/{name}/info_{year}.json'


def cutoff(year, cfg):
    return read(baseline_path(cfg, year))['training_meta']['cutoff_exclusive']


def training_condition(stop, cfg):
    import pyarrow.dataset as ds
    y = ds.field(cfg['target'])
    return ((ds.field('is_train') == True) & (ds.field('price_valid') == True)
            & (ds.field('trade_date') < stop) & y.is_valid()
            & (y < float('inf')) & (y > float('-inf')))


def parameters(stats):
    mean = np.where(np.isfinite(stats.mean_), stats.mean_, 0.)
    scale = np.where(np.isfinite(stats.scale_) & (stats.scale_ > 1e-5), stats.scale_, 1.)
    return mean, scale


def new_regressor(cfg):
    from sklearn.linear_model import SGDRegressor
    return SGDRegressor(loss=cfg['loss'], penalty='l2', alpha=cfg['alpha'], epsilon=cfg['epsilon'],
        fit_intercept=True, learning_rate=cfg['learning_rate'], eta0=cfg['eta0'],
        power_t=cfg['power_t'], average=cfg['average'], shuffle=cfg['shuffle'],
        random_state=cfg['seed'], early_stopping=False, tol=None)


def build_bundle(model, stats, target_stats, cfg, rows, steps):
    mean, scale = parameters(stats)
    center, target_scale = parameters(target_stats)
    assert np.isfinite(model.coef_).all() and np.isfinite(model.intercept_).all()
    assert model.t_ == 1 + rows * cfg['epochs']
    return {'kind': 'streaming_robust_regression', 'regressor': model,
        'mean': mean, 'scale': scale, 'target_center': float(center[0]),
        'target_scale': float(target_scale[0]), 'config': dict(cfg),
        'completed_epochs': cfg['epochs'], 'training_rows': rows,
        'actual_partial_fit_calls': steps, 'actual_native_sample_counter': float(model.t_),
        'target_units': cfg['target'], 'training_device': 'cpu',
        'training_row_order': 'frozen_Parquet_physical_order_after_past_mature_filter',
        'target_not_clipped': True, 'no_validation_early_stopping': True}


def fit_arrays(x, y, cfg):
    stats, target_stats = RunningStats(), RunningStats()
    y = np.asarray(y, dtype=np.float32)
    assert np.isfinite(y).all()
    chunk = cfg['chunk_rows']
    for offset in range(0, len(y), chunk):
        stats.partial_fit(finite_values(x[offset:offset+chunk]))
        target_stats.partial_fit(y[offset:offset+chunk, None])
    mean, scale = parameters(stats)
    center, target_scale = parameters(target_stats)
    model, steps = new_regressor(cfg), 0
    for _ in range(cfg['epochs']):
        for offset in range(0, len(y), chunk):
            values = transform(x[offset:offset+chunk], mean, scale, cfg['clip_z'])
            target = (y[offset:offset+chunk].astype(np.float64) - center[0]) / target_scale[0]
            model.partial_fit(values, target)
            steps += 1
    return build_bundle(model, stats, target_stats, cfg, len(y), steps)


def predict_arrays(bundle, x):
    assert bundle['kind'] == 'streaming_robust_regression'
    cfg, model = bundle['config'], bundle['regressor']
    result = []
    for offset in range(0, len(x), cfg['chunk_rows']):
        values = transform(x[offset:offset+cfg['chunk_rows']], bundle['mean'], bundle['scale'], cfg['clip_z'])
        standardized = np.einsum('ij,j->i', values, model.coef_, optimize=False) + model.intercept_[0]
        pred = standardized * bundle['target_scale'] + bundle['target_center']
        assert np.isfinite(pred).all()
        result.append(pred)
    return np.concatenate(result) if result else np.empty(0, dtype=np.float64)


def fit_stream(year, cfg, source=FEATURE_FILE, limit_rows=None):
    import polars as pl
    features, stop = feature_names(), cutoff(year, cfg)
    condition = training_condition(stop, cfg)
    columns = KEYS + [cfg['target']] + features
    stats, target_stats = RunningStats(), RunningStats()
    rows, dates, key_hashes = 0, set(), []
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
        y = batch.column(cfg['target']).to_numpy(zero_copy_only=False).astype(np.float32)
        assert np.isfinite(y).all()
        stats.partial_fit(finite_values(x))
        target_stats.partial_fit(y[:, None])
        rows += len(batch)
        dates.update(batch.column('trade_date').to_pylist())
        key_hashes.append(pl.from_arrow(batch.select(KEYS)).hash_rows(seed=2026).to_numpy())
        matrix_hash.update(memoryview(x).cast('B'))
        target_hash.update(memoryview(np.ascontiguousarray(y)).cast('B'))
    assert rows
    key_digest = shared.sorted_key_hash_digest(np.concatenate(key_hashes))
    del key_hashes, batch, x, y
    gc.collect()
    mean, scale = parameters(stats)
    center, target_scale = parameters(target_stats)
    model, steps, epoch_counts = new_regressor(cfg), 0, []
    for epoch in range(cfg['epochs']):
        seen = 0
        for batch in batches():
            x = matrix(batch, features)
            y = batch.column(cfg['target']).to_numpy(zero_copy_only=False).astype(np.float32)
            target = (y.astype(np.float64) - center[0]) / target_scale[0]
            model.partial_fit(transform(x, mean, scale, cfg['clip_z']), target)
            steps += 1
            seen += len(y)
        assert seen == rows
        epoch_counts.append(seen)
        if epoch == 0 or (epoch + 1) % 4 == 0:
            log(f"Streamed {cfg['target']} {cfg['loss']} fold{year} epoch{epoch+1}/{cfg['epochs']} actual{seen} mature rows")
    meta = {'rows': rows, 'days': len(dates), 'first': min(dates), 'last': max(dates),
        'cutoff_exclusive': stop, 'validation_year': year, 'features': features,
        'physical_training_matrix_sha256': matrix_hash.hexdigest(),
        'physical_training_target_sha256': target_hash.hexdigest(),
        'sorted_training_key_hash_multiset_sha256': key_digest,
        'training_row_order': 'frozen_Parquet_physical_order_after_past_mature_filter',
        'target': cfg['target'], 'target_not_clipped': True}
    if limit_rows is None:
        baseline = read(baseline_path(cfg, year))['training_meta']
        for key in ('rows', 'days', 'first', 'last', 'cutoff_exclusive', 'validation_year', 'features'):
            assert meta[key] == baseline[key], key
        expected = (pl.scan_parquet(source).filter(pl.col('is_train') & pl.col('price_valid')
            & (pl.col('trade_date') < stop) & pl.col(cfg['target']).is_finite())
            .select(KEYS).collect(engine='streaming').hash_rows(seed=2026).to_numpy())
        assert shared.sorted_key_hash_digest(expected) == key_digest
        meta['full_selected_row_keys_match_independent_original_filter'] = True
        meta['last_label_end'] = baseline['last_label_end']
        assert meta['last'] < stop and meta['last_label_end'] <= stop
    return build_bundle(model, stats, target_stats, cfg, rows, steps), meta, epoch_counts


engine = __import__('sys').modules[__name__]
