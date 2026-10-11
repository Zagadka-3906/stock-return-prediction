"""Four full final fits and independent native controls on all future-X rows."""
from pathlib import Path
import gc
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
OUT = A / 'quantile_tree_future_qa_20261006'


def main():
    import numpy as np
    import polars as pl
    import lightgbm as lgb
    import train_quantile_tree_bank_20261006 as bank
    from locked_read_hash_cache_20261004 import LockedReadHashCache
    from linear_leaf_actual_resource_sampler_20261005 import ResourceSampler
    from verify_linear_leaf_bank_20261005 import manual_native_prediction
    audit = bank.OUT / 'oof_audit.json'
    execution = bank.OUT / 'training_execution_scope.json'
    assert bank.read(audit)['status'] == bank.read(execution)['status'] == 'passed'
    assert bank.read(audit)['actual_annual_fits'] == 20
    assert not OUT.exists()
    OUT.mkdir()
    sources = [Path(__file__), Path(bank.__file__), Path(bank.core.__file__),
        bank.STORAGE, bank.OUT / 'protocol.json', audit, execution,
        A / 'quantile_tree_preflight_20261006/verification.json',
        A / 'linear_leaf_actual_resource_sampler_20261005.py',
        A / 'verify_linear_leaf_bank_20261005.py',
        ROOT / 'deliveries/connected_topk0175_20261003/generation_inputs.parquet',
        ROOT / 'deliveries/connected_topk0175_20261003/train_test.json']
    sources += [Path(p) for p in bank.read(bank.OUT / 'protocol.json')['input_sha256']]
    sources += list(bank.OUT.glob('*/info_202[0-4].json')) + list(bank.OUT.glob('*/model_202[0-4].joblib'))
    # Final target-specific maturity references are frozen before the four final fits.
    sources += [A / f'linear_bank_20261003/{name}/info_2025.json'
                for name in ('rank_ridge_l01', 'return_ridge_l01')]
    bindings = {str(p.resolve()): bank.sha(p) for p in dict.fromkeys(sources)}
    bank.dump(OUT / 'protocol.json', {'status': 'frozen_before_four_actual_full_final_quantile_fits',
        'input_sha256': bindings, 'expected_final_fits': 4, 'iterations_each_full_fit': 300,
        'expected_future_rows': 1599600, 'expected_future_days': 344, 'expected_codes': 4650,
        'future_X_loaded_after_each_actual_fit': True, 'no_validation_early_stopping': True,
        'complete_scheme_official_quality_still_pending': True,
        'new_quality_scores': 0, 'test_labels_read': False}, immutable=True)
    recorder, checks, failure = ResourceSampler(OUT), [], None
    cache = LockedReadHashCache(bindings)
    old_engine_sha, old_bank_sha = bank.engine.sha, bank.sha
    try:
        with cache:
            bank.engine.sha = bank.sha = cache.sha
            bank.RESOURCE = recorder
            recorder.start()
            for name, cfg in bank.CONFIGS.items():
                info = bank.train_one(name, 2025)
                assert info['fulltraining_only_test_prediction_not_generated']
                features = bank.engine.feature_names()
                frame = (pl.scan_parquet(bank.engine.FEATURE_FILE).filter(~pl.col('is_train'))
                    .select(bank.engine.KEYS + features + ['price_valid']).sort('trade_date', 'ts_code').collect())
                expected = pl.read_parquet(ROOT / 'deliveries/connected_topk0175_20261003/generation_inputs.parquet',
                    columns=bank.engine.KEYS + ['price_valid'])
                assert frame.select(bank.engine.KEYS + ['price_valid']).equals(expected)
                assert (len(frame), frame['trade_date'].n_unique(), frame['ts_code'].n_unique()) == (1599600, 344, 4650)
                first = int(frame['trade_date'].min())
                meta = info['training_meta']
                assert meta['last'] < meta['cutoff_exclusive'] and meta['last_label_end'] <= meta['cutoff_exclusive'] <= first
                x = bank.engine.to_matrix(frame, features)
                cutoff = int(frame['trade_date'].unique().sort()[79])
                prefix_rows = int((frame['trade_date'] <= cutoff).sum())
                assert prefix_rows == 80 * 4650
                model = bank.OUT / name / 'model_2025.joblib'
                bank.dump(OUT / f'{name}_frozen_before_inference.json', {
                    'model_sha256': info['model_sha256'], 'configuration': cfg,
                    'training_info_sha256': bank.sha(bank.OUT / name / 'info_2025.json'),
                    'first_actual_future_date': first, 'new_quality_scores': 0,
                    'test_labels_read': False}, immutable=True)
                recorder.context = {'stage': 'all1599600_future_rows_native_reload_cold80_controls', 'model': name}
                bundle = bank.engine.load_bundle(model)
                pred = bank.predict_arrays(bundle, x)
                assert np.isfinite(pred).all()
                assert np.array_equal(pred, bank.predict_arrays(bank.engine.load_bundle(model), x))
                assert np.array_equal(pred[:prefix_rows], bank.predict_arrays(bank.engine.load_bundle(model), x[:prefix_rows]))
                z = bank.core.matched.standardize(x[:131], bundle['mean'], bundle['scale'], cfg)
                manual = manual_native_prediction(lgb.Booster(model_str=bundle['model_string']), z)
                error = float(np.max(np.abs(manual - pred[:131])))
                assert error < 1e-10
                pred[~frame['price_valid'].to_numpy()] = -1e6
                raw = OUT / f'{name}_raw.parquet'
                frame.select(bank.engine.KEYS).with_columns(pl.Series('pred_raw', pred)).write_parquet(raw)
                checks.append({'model': name, 'model_sha256': info['model_sha256'],
                    'raw_sha256': bank.sha(raw), 'actual_final_training_rows': meta['rows'],
                    'actual_native_boosting_iterations': 300, 'actual_full_future_rows': len(frame),
                    'actual344_days4650_codes': True, 'actual_full_reload_and_native_cold80_bit_identical': True,
                    'independent_native_dumped_leaf_sum_131_rows_max_abs_error': error,
                    'complete_original_final_matrix_target_keys_and_maturity_hashes_matched': True,
                    'new_quality_scores': 0, 'test_labels_read': False})
                del frame, expected, x, pred, bundle, z, manual
                gc.collect()
            cache.reverify()
    except BaseException as error:
        failure = f'{type(error).__name__}: {error}'
        raise
    finally:
        resources = recorder.finish()
        bank.dump(OUT / 'resource_summary.json', resources, immutable=True)
        bank.engine.sha, bank.sha, bank.RESOURCE = old_engine_sha, old_bank_sha, None
        bank.dump(OUT / 'execution_scope.json', {'status': 'passed' if failure is None else 'failed',
            'failure': failure, 'input_sha256': bindings, 'new_quality_scores': 0,
            'test_labels_read': False}, immutable=True)
    assert len(checks) == 4
    bank.dump(OUT / 'verification.json', {'status': 'passed', 'checks': checks,
        'actual_full_final_fits': 4, 'all_four_full1599600_row_native_reload_and_cold80_controls_passed': True,
        'complete_scheme_official_quality_and_causality_and_final_adoption_still_pending': True,
        'input_sha256': bindings, 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'new_quality_scores': 0, 'test_labels_read': False}, immutable=True)
