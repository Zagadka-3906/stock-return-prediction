"""Actual past-only regression, withheld-future poison, native and reload controls."""
from pathlib import Path
import sys
import time
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
import streaming_robust_regression_20261005 as method
from verify_streaming_rank_classification_v3_20261005 import head
from streaming_rank_classifier_actual_resource_recorder_20261005 import ActualCPUResourceRecorder
OUT = A / 'streaming_robust_regression_preflight_20261005'


def main():
    import polars as pl
    import pyarrow as pa
    import pyarrow.compute as pc
    import pyarrow.dataset as ds
    import pyarrow.parquet as pq
    from sklearn.linear_model import SGDRegressor
    assert not OUT.exists()
    OUT.mkdir()
    cfg = next(iter(method.CONFIGS.values()))
    features, stop = method.feature_names(), method.cutoff(2020, cfg)
    columns = method.KEYS + ['y_rank', 'y_ret_1d', 'is_train', 'price_valid'] + features
    past = head(method.scanner(columns, method.training_condition(stop, cfg)), 4096)
    future = head(method.scanner(columns, (ds.field('is_train') == True)
                  & (ds.field('trade_date') >= stop) & (ds.field('price_valid') == True)), 128)
    dummy = past.slice(0, 8).set_column(columns.index('is_train'), 'is_train', pa.array([False] * 8))
    combined = pa.concat_tables([past, future, dummy])
    source, poisoned_source = OUT / 'past_with_withheld_future.parquet', OUT / 'poisoned_withheld_future.parquet'
    pq.write_table(combined, source)
    mask = pc.or_(pc.greater_equal(combined['trade_date'], stop), pc.invert(combined['is_train']))
    changed = combined
    for name in ['y_rank', 'y_ret_1d', *features]:
        changed = changed.set_column(changed.schema.get_field_index(name), name,
            pc.if_else(mask, pa.scalar(12345., type=changed[name].type), changed[name]))
    pq.write_table(changed, poisoned_source)
    inputs = [Path(__file__), Path(method.__file__), Path(method.shared.__file__),
              method.MANIFEST, method.FEATURE_FILE, source, poisoned_source, ROOT / '后续选模标准.md']
    inputs += [method.baseline_path(c, 2020) for c in method.CONFIGS.values()]
    frozen = {str(path.resolve()): method.sha(path) for path in dict.fromkeys(inputs)}
    method.dump(OUT / 'frozen_before_controls.json', {
        'status': 'frozen_before16_actual4096row32pass_controls', 'input_sha256': frozen,
        'configurations': method.CONFIGS, 'actual_past_rows': 4096,
        'withheld_actual_future_training_rows': 128, 'excluded_is_train_false_rows': 8,
        'actual_full_native20_annual4_final_fits_and_quality_remain_required': True,
        'test_X_or_test_labels_read': False, 'new_quality_scores': 0}, immutable=True)
    recorder = ActualCPUResourceRecorder(OUT)
    recorder.start()
    controls, identities = [], []
    try:
        for target in ('y_rank', 'y_ret_1d'):
            full = (pl.scan_parquet(method.FEATURE_FILE).filter(pl.col('is_train') & pl.col('price_valid')
                & (pl.col('trade_date') < stop) & pl.col(target).is_finite()).select(method.KEYS)
                .collect(engine='streaming'))
            assert len(full) == 1694259
            digest = method.shared.sorted_key_hash_digest(full.hash_rows(seed=2026).to_numpy())
            identities.append({'target': target, 'actual_full2020_mature_keys': len(full), 'sorted_key_sha256': digest})
        assert identities[0]['sorted_key_sha256'] == identities[1]['sorted_key_sha256']
        raw = method.matrix(past, features)
        for name, cfg in method.CONFIGS.items():
            started = time.monotonic()
            y = past[cfg['target']].to_numpy().astype(np.float32)
            assert np.isfinite(y).all()
            streamed, metadata, epochs = method.fit_stream(2020, cfg, source=source, limit_rows=4096)
            array = method.fit_arrays(raw, y, cfg)
            poisoned, poison_meta, _ = method.fit_stream(2020, cfg, source=poisoned_source, limit_rows=4096)
            assert epochs == [4096] * 32 and streamed['actual_native_sample_counter'] == 131073
            assert metadata == poison_meta
            for other in (array, poisoned):
                for key in ('mean', 'scale'):
                    assert np.array_equal(streamed[key], other[key])
                for key in ('target_center', 'target_scale'):
                    assert streamed[key] == other[key]
                assert np.array_equal(streamed['regressor'].coef_, other['regressor'].coef_)
                assert np.array_equal(streamed['regressor'].intercept_, other['regressor'].intercept_)
            target = y.astype(np.float64)
            np.testing.assert_allclose(streamed['target_center'], target.mean(), atol=1e-14, rtol=1e-13)
            np.testing.assert_allclose(streamed['target_scale'], target.std(), atol=1e-14, rtol=1e-13)
            values = method.transform(raw, streamed['mean'], streamed['scale'])
            standardized = (target - streamed['target_center']) / streamed['target_scale']
            native = SGDRegressor(loss=cfg['loss'], penalty='l2', alpha=.0001, epsilon=.1,
                fit_intercept=True, learning_rate='invscaling', eta0=.01, power_t=.25,
                average=True, shuffle=False, random_state=20261005, early_stopping=False, tol=None)
            for _ in range(32):
                native.partial_fit(values, standardized)
            assert np.array_equal(streamed['regressor'].coef_, native.coef_)
            assert np.array_equal(streamed['regressor'].intercept_, native.intercept_)
            prediction = method.predict_arrays(streamed, raw)
            reference = native.predict(values) * streamed['target_scale'] + streamed['target_center']
            np.testing.assert_allclose(prediction, reference, atol=2e-12, rtol=2e-12)
            path = OUT / f'{name}_4096row32pass.joblib'
            method.save_bundle(path, streamed)
            assert np.array_equal(prediction, method.predict_arrays(method.load_bundle(path), raw))
            for size in (1, 80, 131, 257):
                assert np.array_equal(prediction[:size], method.predict_arrays(method.load_bundle(path), raw[:size]))
            assert np.isfinite(prediction).all() and prediction.std() > 0
            controls.append({'model': name, 'actual_rows': 4096, 'complete_passes': 32,
                'actual_native_sample_counter': native.t_, 'past_target_center': streamed['target_center'],
                'past_target_scale': streamed['target_scale'], 'target_not_clipped': True,
                'stream_array_future_poison_and_independent_native_coefficients_bit_identical': True,
                'native_prediction_max_absolute_difference': float(np.max(np.abs(prediction-reference))),
                'reload_and_prefixes_bit_identical': True, 'model_sha256': method.sha(path),
                'elapsed_seconds': time.monotonic()-started})
    finally:
        resources = recorder.finish()
    assert all(method.sha(path) == digest for path, digest in frozen.items())
    method.dump(OUT / 'verification.json', {
        'status': 'passed_actual_streamed_robust_regression_maturity_native_reload_and_prefix_controls',
        'controls': controls, 'actual_full2020_rank_return_eligibility_checks': identities,
        'actual_small32pass_fits': 16, 'actual_full_annual_fits': 0,
        'all20_full_annual4_final_and_complete_quality_not_replaced_by_controls': True,
        'actual_resources': resources, 'source_sha256': frozen,
        'target_scaling_fitted_only_mature_past_and_inverted_at_prediction': True,
        'new_quality_scores': 0, 'test_labels_read': False}, immutable=True)
    print(method.read(OUT / 'verification.json')['status'], flush=True)


if __name__ == '__main__':
    main()
