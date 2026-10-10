"""Actual mature-row streaming, native classifier and future-poison controls."""
from pathlib import Path
import hashlib
import json
import sys
import threading
import time

import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
import streaming_rank_classification_20261005 as method
OUT = A / 'streaming_rank_classification_preflight_20261005'


def head(iterator, count):
    import pyarrow as pa
    parts = []
    for batch in iterator:
        if len(batch):
            size = min(count, len(batch))
            parts.append(batch.slice(0, size))
            count -= size
        if not count:
            break
    return pa.Table.from_batches(parts)


def main():
    import numpy as np
    import pyarrow as pa
    import pyarrow.compute as pc
    import pyarrow.dataset as ds
    import pyarrow.parquet as pq
    from sklearn.linear_model import SGDClassifier
    assert not OUT.exists()
    OUT.mkdir()
    features = method.feature_names()
    columns = method.KEYS + ['y_rank', 'is_train', 'price_valid'] + features
    stop = method.cutoff(2020)
    past = head(method.scanner(columns, method.training_condition(stop)), 4096)
    future_condition = ((ds.field('is_train') == True) & (ds.field('trade_date') >= stop)
                        & ds.field('y_rank').is_valid() & (ds.field('y_rank') < float('inf'))
                        & (ds.field('y_rank') > float('-inf')) & (ds.field('price_valid') == True))
    future = head(method.scanner(columns, future_condition), 128)
    dummy = past.slice(0, 8).set_column(columns.index('is_train'), 'is_train', pa.array([False] * 8))
    combined = pa.concat_tables([past, future, dummy])
    source = OUT / 'actual_past_and_withheld_future_control.parquet'
    poisoned_source = OUT / 'future_label_and_feature_poison_control.parquet'
    pq.write_table(combined, source)
    mask = pc.or_(pc.greater_equal(combined['trade_date'], stop), pc.invert(combined['is_train']))
    changed = combined
    for name in ['y_rank', *features]:
        index = changed.schema.get_field_index(name)
        values = pc.if_else(mask, pa.scalar(12345., type=changed[name].type), changed[name])
        changed = changed.set_column(index, name, values)
    pq.write_table(changed, poisoned_source)
    baseline = A / 'linear_bank_20261003/rank_ridge_l01/info_2020.json'
    frozen = {str(path): method.sha(path) for path in (Path(__file__), Path(method.__file__),
               method.MANIFEST, method.FEATURE_FILE, source, poisoned_source, baseline, ROOT / '后续选模标准.md')}
    method.dump(OUT / 'frozen_before_actual_controls.json', {
        'status': 'frozen_before4_32epoch_streamed4096row_models_and_independent_refits',
        'input_sha256': frozen, 'configurations': method.CONFIGS,
        'actual_past_rows': len(past), 'withheld_future_training_rows': len(future),
        'synthetic_excluded_is_train_false_rows': len(dummy),
        'test_X_and_test_labels_read': False, 'new_quality_scores': 0}, immutable=True)
    resources, stopping = [], threading.Event()
    process = psutil.Process()
    def observe():
        while not stopping.wait(.25):
            resources.append({'at_seconds': time.monotonic(), 'rss': process.memory_info().rss,
                              'host_available': psutil.virtual_memory().available})
    thread = threading.Thread(target=observe, daemon=True)
    thread.start()
    controls = []
    try:
        raw = method.matrix(past, features)
        y = past['y_rank'].to_numpy().astype(np.float32)
        probe = np.asarray([0., .1, .5, .9, 1.], dtype=np.float32)
        assert np.array_equal(method.rank_classes(probe, {'rank_objective': 'decile'}), [0, 1, 5, 9, 9])
        assert np.array_equal(method.rank_classes(probe, {'rank_objective': 'top10'}), [0, 0, 0, 1, 1])
        synthetic = np.random.default_rng(20261005).normal(size=(317, 63))
        synthetic[:40, 1] = np.nan
        synthetic[::7, 2] = np.inf
        synthetic[:, 3] = np.nan
        synthetic[:, 4] = 2.
        stats = method.RunningStats()
        for offset in range(0, len(synthetic), 40):
            stats.partial_fit(synthetic[offset:offset + 40])
        for column in range(63):
            values = synthetic[:, column]
            values = values[np.isfinite(values)]
            expected_mean = values.mean() if len(values) else 0.
            expected_scale = values.std() if len(values) else 0.
            np.testing.assert_allclose(stats.mean_[column], expected_mean, rtol=1e-12, atol=1e-12)
            np.testing.assert_allclose(stats.scale_[column], expected_scale, rtol=1e-12, atol=1e-12)
        for name, cfg in method.CONFIGS.items():
            started = time.monotonic()
            streamed, metadata, epochs = method.fit_stream(2020, cfg, source=source, limit_rows=4096)
            array = method.fit_arrays(raw, y, cfg)
            poisoned, poisoned_meta, _ = method.fit_stream(2020, cfg, source=poisoned_source, limit_rows=4096)
            assert epochs == [4096] * 32 and streamed['actual_native_sample_counter'] == 131073
            for other in (array, poisoned):
                for key in ('mean', 'scale'):
                    assert np.array_equal(streamed[key], other[key])
                assert np.array_equal(streamed['classifier'].coef_, other['classifier'].coef_)
                assert np.array_equal(streamed['classifier'].intercept_, other['classifier'].intercept_)
            assert metadata == poisoned_meta
            # An independently configured native sklearn estimator receives the
            # same full small training rows and the explicit fixed label rules.
            native = SGDClassifier(loss='log_loss', penalty='l2', alpha=cfg['alpha'],
                fit_intercept=True, learning_rate='invscaling', eta0=.01, power_t=.25,
                average=True, shuffle=False, random_state=20261005, n_jobs=1,
                early_stopping=False, tol=None)
            values = method.transform(raw, streamed['mean'], streamed['scale'])
            labels = (y >= np.float32(.9)).astype(np.int64) if cfg['rank_objective'] == 'top10' else np.digitize(
                y, np.arange(1, 10, dtype=np.float32) / np.float32(10), right=False)
            all_classes = np.arange(2 if cfg['rank_objective'] == 'top10' else 10)
            for _ in range(32):
                native.partial_fit(values, labels, classes=all_classes)
            assert np.array_equal(streamed['classifier'].coef_, native.coef_)
            prediction = method.predict_arrays(streamed, raw)
            native_probability = native.predict_proba(values)
            reference = native_probability[:, 1] if cfg['rank_objective'] == 'top10' else (
                native_probability @ ((native.classes_.astype(np.float64) + .5) / 10))
            np.testing.assert_allclose(prediction, reference, rtol=2e-13, atol=2e-13)
            path = OUT / f'{name}_4096row32epoch.joblib'
            method.save_bundle(path, streamed)
            assert np.array_equal(prediction, method.predict_arrays(method.load_bundle(path), raw))
            for size in (1, 80, 131, 257):
                assert np.array_equal(prediction[:size], method.predict_arrays(method.load_bundle(path), raw[:size]))
            assert np.isfinite(prediction).all() and prediction.std() > 0
            controls.append({'model': name, 'actual_training_rows': 4096, 'actual_completed_epochs': 32,
                'actual_native_sample_counter': streamed['actual_native_sample_counter'],
                'stream_array_and_poisoned_future_model_state_bit_identical': True,
                'independent_native_sklearn_model_coefficients_bit_identical': True,
                'native_probability_max_absolute_difference': float(np.max(np.abs(prediction - reference))),
                'actual_reload_and1_80_131_257_row_prefix_bit_identical': True,
                'model_sha256': method.sha(path), 'elapsed_seconds': time.monotonic() - started})
    finally:
        stopping.set()
        thread.join()
    assert all(method.sha(path) == digest for path, digest in frozen.items())
    method.dump(OUT / 'resource_samples.json', resources, immutable=True)
    method.dump(OUT / 'verification.json', {
        'status': 'passed_actual_streamed_rank_classification_maturity_native_reload_and_prefix_controls',
        'controls': controls, 'actual_small32epoch_fits': 16, 'actual_full_annual_fits': 0,
        'finite_column_running_moments_match_independent_numpy_including_initial_and_entire_missing': True,
        'provided_float32_rank_class_boundaries_explicitly_checked': True,
        'peak_process_rss_bytes_sampled': max(row['rss'] for row in resources),
        'minimum_host_available_bytes_sampled': min(row['host_available'] for row in resources),
        'full_native20_annual4_final_complete_quality_not_substituted_by_small_controls': True,
        'input_sha256': frozen, 'new_quality_scores': 0, 'test_labels_read': False}, immutable=True)
    print(json.dumps({'status': 'passed', 'models': len(controls), 'small32epoch_fits': 16,
                      'peak_rss': max(row['rss'] for row in resources), 'actual_full_annual_fits': 0}), flush=True)


if __name__ == '__main__':
    main()
