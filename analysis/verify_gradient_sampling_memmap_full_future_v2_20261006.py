"""Recheck all1,599,600 future rows for six final models reused with full native provenance."""
from pathlib import Path
import gc
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
OUT = A / 'gradient_sampling_memmap_future_qa_v2_20261006'


def main():
    import numpy as np
    import polars as pl
    import train_gradient_sampling_memmap_bank_v2_20261006 as bank
    from locked_read_hash_cache_20261004 import LockedReadHashCache
    from linear_leaf_actual_resource_sampler_20261005 import ResourceSampler
    from handoff_distribution_views_progress_monitor_20261006 import read, sha, create
    audit = bank.OUT / 'oof_audit.json'
    execution = bank.OUT / 'training_execution_scope.json'
    assert read(audit)['status'] == read(execution)['status'] == 'passed'
    assert read(audit)['actual_annual_fits'] == 30
    assert not OUT.exists()
    sources = [Path(__file__), Path(bank.__file__), Path(bank.codec.__file__), audit, execution,
        bank.OUT / 'protocol.json', bank.CAPACITY / 'verification.json',
        A / 'linear_leaf_actual_resource_sampler_20261005.py', A / 'locked_read_hash_cache_20261004.py',
        ROOT / 'deliveries/connected_topk0175_20261003/generation_inputs.parquet',
        ROOT / 'deliveries/connected_topk0175_20261003/train_test.json']
    sources += [Path(p) for p in read(bank.OUT / 'protocol.json')['input_sha256']]
    sources += list(bank.OUT.glob('*/model_2025.joblib')) + list(bank.OUT.glob('*/info_2025.json'))
    bindings = {str(p.resolve()): sha(p) for p in dict.fromkeys(sources)}
    OUT.mkdir()
    create(OUT / 'protocol.json', {'status': 'frozen_before_full_future_verification_of_reused6_actual_final_fits',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': bindings,
        'expected_final_fits': 6, 'full_final_fits_reused_with_native_capacity_provenance': True,
        'new_native_fits_by_this_verifier': 0, 'expected_future_shape': [1599600, 344, 4650],
        'future_X_never_used_to_choose_configs_or_a_complete_scheme': True,
        'original124_plus138_quality_records_still_required': True,
        'new_quality_scores': 0, 'test_labels_read': False})
    resources, checks, failure = ResourceSampler(OUT), [], None
    resources.start()
    try:
        with LockedReadHashCache(bindings):
            for name, cfg in bank.CONFIGS.items():
                info = bank.verified_info(name, 2025)
                assert info['copied_file_is_not_an_additional_native_fit']
                assert info['test_data_read'] is False and info['fulltraining_only_test_prediction_not_generated']
                assert info['model_sha256'] == sha(bank.CAPACITY / name / 'model_2025.joblib')
                capacity_check = read(bank.CAPACITY / name / 'future_verification.json')
                assert capacity_check['status'] == 'passed'
                assert capacity_check['actual_full_training_rows'] == 6754006
                assert capacity_check['actual_native_iterations'] == 300
                features = bank.engine.feature_names()
                frame = pl.scan_parquet(bank.engine.FEATURE_FILE).filter(~pl.col('is_train')).select(
                    bank.engine.KEYS + features + ['price_valid']).sort('trade_date', 'ts_code').collect()
                expected = pl.read_parquet(ROOT / 'deliveries/connected_topk0175_20261003/generation_inputs.parquet',
                    columns=bank.engine.KEYS + ['price_valid'])
                assert frame.select(bank.engine.KEYS + ['price_valid']).equals(expected)
                assert (len(frame), frame['trade_date'].n_unique(), frame['ts_code'].n_unique()) == (1599600, 344, 4650)
                first = int(frame['trade_date'].min())
                meta = info['training_meta']
                assert meta['last'] < meta['cutoff_exclusive'] and meta['last_label_end'] <= meta['cutoff_exclusive'] <= first
                model = bank.OUT / name / 'model_2025.joblib'
                create(OUT / f'{name}_frozen_before_inference.json', {
                    'model_sha256': info['model_sha256'], 'configuration': cfg,
                    'training_info_sha256': sha(bank.OUT / name / 'info_2025.json'),
                    'actual_complete_native_fit_origin_info_sha256': info['actual_fit_origin_info_sha256'],
                    'first_actual_future_date': first, 'new_quality_scores': 0, 'test_labels_read': False})
                resources.context = {'stage': 'actual_complete_GOSS_future_reload_codec_and_cold80_controls', 'model': name}
                x = bank.engine.to_matrix(frame, features)
                pred = bank.core.predict_arrays(bank.engine.load_bundle(model), x)
                assert np.isfinite(pred).all()
                assert np.array_equal(pred, bank.core.predict_arrays(bank.engine.load_bundle(model), x))
                assert np.array_equal(pred, bank.codec.predict(bank.engine.load_bundle(model), x))
                assert np.array_equal(pred[:372000], bank.codec.predict(bank.engine.load_bundle(model), x[:372000]))
                assert np.array_equal(pred[:37 * 4650], bank.codec.predict(bank.engine.load_bundle(model), x[:37 * 4650]))
                assert bank.engine.array_hash(pred) == capacity_check['full_future_raw_array_sha256']
                pred[~frame['price_valid'].to_numpy()] = -1e6
                source = bank.CAPACITY / name / 'future_raw.parquet'
                assert sha(source) == capacity_check['future_parquet_sha256']
                previous = pl.read_parquet(source)
                assert frame.select(bank.engine.KEYS).equals(previous.select(bank.engine.KEYS))
                assert np.array_equal(pred, previous['pred_raw'].to_numpy())
                raw = OUT / f'{name}_raw.parquet'
                frame.select(bank.engine.KEYS).with_columns(pl.Series('pred_raw', pred)).write_parquet(raw)
                checks.append({'model': name, 'model_sha256': info['model_sha256'], 'raw_sha256': sha(raw),
                    'mature_training': meta, 'actual_full1599600_row_reload_bit_identical': True,
                    'actual_cold80_day_prefix_bit_identical': True, 'actual_independent_codec_whole_and37day_bit_identical': True,
                    'source_capacity_predictions_bit_identical_all1599600_rows': True,
                    'native131_row_prediction_bit_identical': True,
                    'native131_row_dumped_leaf_formula_previously_verified_at_capacity': capacity_check['independent_dumped_leaf_sum131_rows_max_abs_error'],
                    'new_quality_scores': 0, 'test_labels_read': False})
                del frame, expected, x, pred, previous
                gc.collect()
    except BaseException as error:
        failure = f'{type(error).__name__}: {error}'
        raise
    finally:
        create(OUT / 'resource_summary.json', {'status': 'passed' if failure is None else 'failed',
            'failure': failure, **resources.finish()})
        create(OUT / 'execution_scope.json', {'status': 'passed' if failure is None else 'failed',
            'failure': failure, 'input_sha256': bindings, 'new_native_fits': 0,
            'new_quality_scores': 0, 'test_labels_read': False})
    assert len(checks) == 6
    create(OUT / 'verification.json', {'status': 'passed', 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'checks': checks, 'actual_fulltraining_fits': 6, 'actual_full_final_fits': 6,
        'all6_models_fullfuture_reload_and_cold80_controls_passed': True,
        'actual_native_fits_reused_with_full_provenance': True, 'new_native_fits_by_this_verifier': 0,
        'input_sha256': bindings, 'resource_summary_sha256': sha(OUT / 'resource_summary.json'),
        'complete_output_official_quality_and_adoption_still_pending': True,
        'new_quality_scores': 0, 'test_labels_read': False})


if __name__ == '__main__':
    main()
