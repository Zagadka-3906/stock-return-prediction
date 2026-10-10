"""Fit20 CPU-only .25/.75 quantile histogram regressors using mature past flagged OOF residual labels."""
from pathlib import Path
import gc
import hashlib
import os
import sys
import time
import warnings

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'POLARS_MAX_THREADS'):
    os.environ[key] = '4'
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from atomic_optimization_observer_writes_20261005 import write

OUT = A / 'quantile_HGB_native_bank20_20261007'
PLAN = A / 'quantile_HGB_native_bank20_plan_20261007.json'


def numeric_sha(x):
    import numpy as np
    return hashlib.sha256(memoryview(np.ascontiguousarray(x)).cast('B')).hexdigest()


def main():
    import numpy as np
    import polars as pl
    import psutil
    import joblib
    import sklearn
    from sklearn.ensemble import HistGradientBoostingRegressor
    from sklearn.exceptions import ConvergenceWarning
    from threadpoolctl import threadpool_limits
    from run import fold_cutoff
    from direct_flag_centered_rank_CDF_transform_20261007 import prepare as prepare_cdf
    from cpu_conditional_residual_hgb_codec_20261007 import fit_preprocessing, prepare, export, predict_native, predict_decoded
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    assert not OUT.exists()
    OUT.mkdir()
    service = A / 'service_owned_workflows_20261006/direct_rank_micro74_round109_full_registration'
    while not (service / 'native_launch.json').exists() or owned(read(service / 'native_launch.json')):
        time.sleep(15)
    assert read(service / 'service_execution.json')['status'] == 'passed'
    assert read(A / 'github_validation_sync_main_20261005/round109_receipt.json')['actual_full_QA_version'] == 20
    while psutil.virtual_memory().available < 9 * 2**30:
        time.sleep(15)
    plan = read(PLAN)
    codec_proof = A / 'quantile_HGB_codec_preflight_20261007/verification.json'
    assert read(codec_proof)['status'] == 'passed_actual_four_historical_quantile_HGB_codec_controls'
    admitted=read(A/'quantile_HGB_native_bank20_admission_20261007.json')
    assert admitted['status']=='passed_actual4_quantile_codec_fits_and20_mature_window_plan_source_admission'
    for p,d in admitted['input_sha256'].items():assert sha(p)==d,p
    features = read(ROOT / 'data/feature_manifest.json')['features']
    assert len(features) == 63
    sources = [Path(__file__), PLAN, A / 'quantile_HGB_native_bank20_admission_20261007.json', codec_proof, A / 'verify_quantile_HGB_codec_preflight_20261007.py', A / 'cpu_conditional_residual_hgb_codec_20261007.py',
        A / 'direct_flag_centered_rank_CDF_transform_20261007.py', ROOT / 'run.py', ROOT / 'src/features.py',
        ROOT / '后续选模标准.md', ROOT / 'data/features.parquet', ROOT / 'data/feature_manifest.json',
        A / 'connected_validation_20261002/combined_fold_frame.parquet',
        A / 'conditional_flag_rank_bank_v2_20261006/flagged_validation_features.parquet',
        A / 'optimization_20261003_r106/selected_validation.npy', A / 'optimization_20261003_r106/selection.json',
        A / 'github_validation_sync_main_20261005/round106_receipt.json',
        A / 'github_validation_sync_main_20261005/round109_receipt.json']
    pins = {str(p): sha(p) for p in sources}
    create(OUT / 'frozen_before_actual_training.json', {'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'input_sha256': pins, 'configurations': plan['configurations'], 'actual_declared_native_fits': 20,
        'first2020_identity_no_mature_prior_OOF_training_available': True,
        'preprocessing_only_corresponding_mature_past_flagged_training_rows': True,
        'teacher_is_qualified106_expanding_OOF_current_forecast_percentile': True,
        'teacher_hyperparameters_selected_on_training_validation_multiple_selection_bias_uncorrected': True,
        'no_validation_early_stopping': True, 'no_new_official_scores_by_training': True,
        'CPU_only_no_torch_or_CUDA_used': True, 'test_labels_read': False})
    records = []
    started = time.perf_counter()
    with LockedReadHashCache(pins) as scope, threadpool_limits(limits=4):
        frame = pl.read_parquet(A / 'connected_validation_20261002/combined_fold_frame.parquet',
            columns=['ts_code', 'trade_date', 'flag_limit_up', 'price_valid'])
        assert (len(frame), frame['trade_date'].n_unique(), frame['ts_code'].n_unique()) == (5635800, 1212, 4650)
        keyed = pl.read_parquet(A / 'conditional_flag_rank_bank_v2_20261006/flagged_validation_features.parquet')
        flagged = frame.with_row_index('oof_position').filter(pl.col('flag_limit_up') == 1)
        assert keyed['oof_position'].equals(flagged['oof_position'])
        assert keyed.select('ts_code', 'trade_date').equals(flagged.select('ts_code', 'trade_date'))
        truth = pl.scan_parquet(ROOT / 'data/features.parquet').filter(pl.col('is_train') & (pl.col('flag_limit_up') == 1)).select('ts_code', 'trade_date', 'y_rank').collect()
        keyed = keyed.join(truth, on=['ts_code', 'trade_date'], how='left', validate='1:1', maintain_order='left')
        assert len(keyed) == 86968
        raw = np.load(A / 'optimization_20261003_r106/selected_validation.npy', mmap_mode='r')
        dates, flags, valid = (frame[k].to_numpy() for k in ('trade_date', 'flag_limit_up', 'price_valid'))
        parent_pct = np.zeros(len(frame), dtype=np.float64)
        for _, positions, percentile, _, _ in prepare_cdf(raw, dates, flags, valid, 'all_current_raw_forecasts'):
            parent_pct[positions] = percentile
        positions = keyed['oof_position'].to_numpy()
        kd = keyed['trade_date'].to_numpy()
        x = np.column_stack([keyed.select(features).to_numpy(), parent_pct[positions]]).astype(np.float64)
        y = keyed['y_rank'].to_numpy().astype(np.float64) + .5 - parent_pct[positions]
        available_label = np.isfinite(y) & valid[positions]
        feature_names = [*features, 'qualified106_current_forecast_average_rank_over_N']
        days = pl.scan_parquet(ROOT / 'data/features.parquet').filter(pl.col('is_train')).select('trade_date').unique().sort('trade_date').collect()['trade_date'].to_numpy()
        oof_days = frame['trade_date'].unique().sort().to_numpy()
        create(OUT / 'actual_target_and_key_alignment.json', {'status': 'passed_mature_training_only_flagged_OOF_residual_target',
            'flagged_rows': len(keyed), 'features': feature_names, 'residual_target_numeric_sha256': numeric_sha(y),
            'current_forecast_percentile_numeric_sha256': numeric_sha(parent_pct[positions]),
            'target': 'original supplied-return-derived cached y_rank_plus0.5 minus qualified106 same-day forecast average_rank/N',
            'every_window_mask_applied_before_preprocessing_or_fit': True, 'future_test_labels_read': False})
        outputs = {name: np.zeros(len(frame), dtype=np.float64) for name in plan['configurations']}
        for name in outputs:
            (OUT / name).mkdir()
        for year in range(2021, 2026):
            cutoff = fold_cutoff(year)
            train = (kd < cutoff) & available_label
            assert train.sum() >= 300
            last = int(kd[train].max())
            label_end = int(days[np.searchsorted(days, last)+1])
            assert last < cutoff and label_end <= cutoff
            preprocessing = fit_preprocessing(x[train])
            bx = prepare(x[train], preprocessing)
            selected = kd // 10000 == year
            test = x[selected] if year < 2025 else x[train][:1000]
            for name, configuration in plan['configurations'].items():
                write(OUT / 'actual_stage.json', {'status': 'actual_CPU_HGB_training',
                    'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'model': name, 'year': year,
                    'actual_completed_native_fits': len(records), 'expected_fits': 20,
                    'available_RAM_GiB': psutil.virtual_memory().available / 2**30})
                params = {**plan['fixed_parameters'], **configuration}
                model = HistGradientBoostingRegressor(**params)
                fit_start = time.perf_counter()
                with warnings.catch_warnings(record=True) as observed:
                    warnings.simplefilter('always', ConvergenceWarning)
                    model.fit(bx, y[train])
                assert model.n_iter_ == plan['fixed_parameters']['max_iter']
                fit_seconds = time.perf_counter()-fit_start
                native = OUT / name / f'model_{year}.joblib'
                assert not native.exists()
                bundle = {'model': model, 'preprocessing': preprocessing, 'features': feature_names}
                joblib.dump(bundle, native)
                decoded_path = OUT / name / f'independent_hist_tree_state_{year}.json'
                create(decoded_path, export(model, preprocessing, feature_names))
                saved = joblib.load(native)
                actual = predict_native(bundle, test)
                replay = predict_native(saved, test)
                independent = predict_decoded(read(decoded_path), test)
                assert np.array_equal(actual.view(np.uint64), replay.view(np.uint64))
                assert np.array_equal(actual.view(np.uint64), independent.view(np.uint64))
                controls = []
                if year < 2025:
                    outputs[name][positions[selected]] = actual
                    for count in (80, 260, 975):
                        mask = kd[selected] <= oof_days[count-1]
                        cold = predict_native(saved, test[mask])
                        cold_decoded = predict_decoded(read(decoded_path), test[mask])
                        assert np.array_equal(actual[mask].view(np.uint64), cold.view(np.uint64))
                        assert np.array_equal(cold.view(np.uint64), cold_decoded.view(np.uint64))
                        controls.append({'days': count, 'flagged_rows': int(mask.sum()), 'native_and_independent_bits_exact': True})
                item = {'name': name, 'year': year, 'parameters': params, 'features': feature_names,
                    'training_rows': int(train.sum()), 'last_training_label_date': last, 'last_training_label_end': label_end,
                    'exclusive_cutoff': cutoff, 'training_matrix_numeric_sha256': numeric_sha(bx),
                    'training_target_numeric_sha256': numeric_sha(y[train]), 'actual_iterations': model.n_iter_,
                    'training_score_curve_empty_without_early_stopping': list(map(float, model.train_score_)), 'fit_seconds': fit_seconds,
                    'native_model_path': str(native), 'native_model_sha256': sha(native),
                    'independent_hist_tree_state_path': str(decoded_path), 'independent_hist_tree_state_sha256': sha(decoded_path),
                    'native_reload_and_independent_numpy_codec_bits_exact': True, 'actual_control_rows': len(test),
                    'actual_cold_prefix_controls': controls, 'expected_max_iter_warnings': [str(w.message) for w in observed],
                    'sklearn_version': sklearn.__version__, 'CPU_threads': 4, 'new_native_fits': 1, 'test_labels_read': False}
                create(OUT / name / f'info_{year}.json', item)
                records.append(item)
                print({'model': name, 'year': year, 'fit_seconds': fit_seconds, 'native_fits': len(records)}, flush=True)
                del model, saved, bundle, actual, replay, independent
                gc.collect()
        for name, values in outputs.items():
            assert np.all(values[flags == 0] == 0) and np.all(values[dates // 10000 == 2020] == 0)
            np.save(OUT / name / 'flagged_oof_predictions.npy', values)
            create(OUT / name / 'oof_verification.json', {'status': 'passed',
                'prediction_array_sha256': sha(OUT / name / 'flagged_oof_predictions.npy'),
                'first2020_and_nonflag_identity_zero_residual': True, 'test_labels_read': False})
        assert len(records) == 20
        scope.reverify()
        create(OUT / 'verification.json', {'status': 'passed_actual20_CPU_quantile_HGB_native_independent_numpy_and_prefix_controls',
            'input_sha256': pins, 'configurations': plan['configurations'], 'actual_models': records,
            'actual_native_fits': 20, 'elapsed_seconds': time.perf_counter()-started,
            'actual_current_process_RSS_GiB_at_completion': psutil.Process().memory_info().rss / 2**30,
            'all_four_annual_mature_windows_and_one_final_window': True,
            'all20_native_reload_independent_numpy_codec_bit_controls': True,
            'new_official_quality_scores': 0, 'CPU_only_no_CUDA_or_torch_used': True,
            'full_official_comparisons_and_selected_future_inference_still_required': True, 'test_labels_read': False})


if __name__ == '__main__':
    main()
