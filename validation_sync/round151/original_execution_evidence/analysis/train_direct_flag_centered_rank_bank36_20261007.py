"""Local-only direct rank specialists; reuse one mature-window binning for six models."""
from pathlib import Path
import gc
import hashlib
import os
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'POLARS_MAX_THREADS'):
    os.environ[key] = '2'
from run_dependency_queue_v3_20261006 import read, create, sha
from atomic_optimization_observer_writes_20261005 import write

OUT = A / 'direct_flag_centered_rank_bank36_20261007'
PLAN = A / 'single_host_direct_flag_rank_plan_20261007.json'
BENCHMARK = A / 'local_flag_tree_thread_benchmark_20261007/verification.json'


def numeric_sha(values):
    import numpy as np
    return hashlib.sha256(memoryview(np.ascontiguousarray(values)).cast('B')).hexdigest()


def main():
    import psutil
    import numpy as np
    import polars as pl
    import lightgbm as lgb
    from run import fold_cutoff
    from conditional_identity_regression_tree_codec_20261006 import clean_matrix, predict_dump
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    plan, benchmark = read(PLAN), read(BENCHMARK)
    assert benchmark['status'] == 'passed_actual_local_thread_throughput_and_exact_native_controls'
    threads = benchmark['selected_threads']
    assert threads in (2, 4, 8)
    configs = plan['configurations']
    assert len(configs) == 6 and sum(c['objective'] == 'huber' for c in configs.values()) == 3
    assert all(c.get('alpha') == .1 for c in configs.values() if c['objective'] == 'huber')
    assert not OUT.exists()
    OUT.mkdir()
    paths = [Path(__file__), PLAN, BENCHMARK,
        A / 'benchmark_local_flag_tree_threads_20261007.py',
        A / 'conditional_identity_regression_tree_codec_20261006.py',
        A / 'conditional_flag_rank_codec_20261006.py',
        A / 'win32_read_handle_hash_cache_with_filename_v2_20261006.py',
        A / 'win32_read_handle_hash_cache_20261006.py',
        ROOT / 'data/features.parquet', ROOT / 'data/feature_manifest.json',
        ROOT / 'src/features.py', ROOT / 'run.py', ROOT / '后续选模标准.md',
        A / 'connected_validation_20261002/combined_fold_frame.parquet',
        A / 'conditional_flag_rank_bank_v2_20261006/flagged_validation_features.parquet',
        A / 'conditional_flag_rank_bank_v2_20261006/actual_target_and_feature_alignment.json',
        A / 'github_validation_sync_main_20261005/round106_receipt.json']
    pins = {str(p): sha(p) for p in paths}
    create(OUT / 'frozen_before_actual_training.json', {'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'input_sha256': pins, 'configurations': configs, 'annual_years': list(range(2020, 2025)),
        'final_training_year': 2025, 'expected_actual_native_fits': 36,
        'target': 'Existing features.py y_rank: float32 historical daily rank/count minus0.5',
        'target_for_future_CDF': 'Saved direct forecast plus0.5; no newly supplied rank label is claimed',
        'training_only_finite_targets_and_current_price_valid_flagged_rows': True,
        'selected_threads_from_hardware_benchmark_only': threads,
        'one_training_only_Dataset_construction_per_year_reused_by_six_configurations': True,
        'no_validation_early_stopping_or_new_score_selection': True,
        'original_running_scientific_workers_untouched': True, 'test_labels_read': False})
    while psutil.virtual_memory().available < 9 * 2**30:
        write(OUT / 'waiting_status.json', {'status': 'waiting_for_local_available_RAM_9GiB',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'available_RAM_GiB': psutil.virtual_memory().available / 2**30})
        time.sleep(30)
    features = read(ROOT / 'data/feature_manifest.json')['features']
    assert len(features) == 63 and 'y_rank' not in features
    records = []
    started = time.perf_counter()
    with LockedReadHashCache(pins):
        lazy = pl.scan_parquet(ROOT / 'data/features.parquet')
        historical = lazy.filter(pl.col('is_train') & (pl.col('flag_limit_up') == 1)
            & pl.col('price_valid') & pl.col('y_rank').is_finite()).select(
                ['ts_code', 'trade_date', 'y_rank', *features]).collect().sort('trade_date', 'ts_code')
        assert historical['trade_date'].max() < 20250101
        assert historical.select(pl.struct('ts_code', 'trade_date').n_unique()).item() == len(historical)
        days = lazy.filter(pl.col('is_train')).select('trade_date').unique().sort('trade_date').collect()['trade_date'].to_numpy()
        assert days.max() < 20250101
        frame = pl.read_parquet(A / 'connected_validation_20261002/combined_fold_frame.parquet',
            columns=['ts_code', 'trade_date', 'flag_limit_up'])
        assert len(frame) == 5635800 and frame['trade_date'].n_unique() == 1212
        assert frame['ts_code'].n_unique() == 4650
        keyed = pl.read_parquet(A / 'conditional_flag_rank_bank_v2_20261006/flagged_validation_features.parquet')
        flagged = frame.with_row_index('oof_position').filter(pl.col('flag_limit_up') == 1)
        assert keyed['oof_position'].equals(flagged['oof_position'])
        assert keyed.select('ts_code', 'trade_date').equals(flagged.select('ts_code', 'trade_date'))
        x = clean_matrix(historical.select(features).to_numpy())
        y = historical['y_rank'].to_numpy().astype(np.float64)
        dates = historical['trade_date'].to_numpy()
        vx = clean_matrix(keyed.select(features).to_numpy())
        vd = keyed['trade_date'].to_numpy()
        positions = keyed['oof_position'].to_numpy()
        all_days = frame['trade_date'].unique().sort().to_numpy()
        assert np.isfinite(y).all() and y.min() >= -.5 and y.max() <= .5
        assert len(keyed) == 86968
        create(OUT / 'actual_training_target_and_validation_alignment.json', {
            'status': 'passed_existing_centered_rank_labels_and_original_flagged_feature_keys',
            'training_rows': len(historical), 'training_target_numeric_sha256': numeric_sha(y),
            'training_matrix_numeric_sha256': numeric_sha(x), 'validation_matrix_numeric_sha256': numeric_sha(vx),
            'label_source': 'data/features.parquet.y_rank, original features.py training return ranks',
            'training_label_dtype_in_feature_cache': str(historical['y_rank'].dtype),
            'validation_flagged_rows': len(keyed), 'validation_labels_not_used_for_fit': True,
            'features': features, 'test_labels_read': False})
        outputs = {}
        for name in configs:
            (OUT / name).mkdir()
            outputs[name] = np.zeros(len(frame), dtype=np.float64)
        common = {'metric': 'None', 'learning_rate': .05, 'deterministic': True,
            'force_col_wise': True, 'num_threads': threads, 'seed': 20261006,
            'verbosity': -1, 'max_bin': 127, 'feature_fraction': 1.,
            'bagging_fraction': 1., 'bagging_freq': 0, 'use_missing': True,
            'zero_as_missing': False, 'feature_pre_filter': False,
            'max_depth': 5, 'min_data_in_leaf': 128, 'lambda_l2': 10.}
        binning = []
        for year in range(2020, 2026):
            cutoff = fold_cutoff(year)
            mask = dates < cutoff
            assert mask.sum() >= 300
            last = int(dates[mask].max())
            end = int(days[np.searchsorted(days, last) + 1])
            assert last < cutoff and end <= cutoff
            bx, by = x[mask], y[mask]
            ds_started = time.perf_counter()
            dataset = lgb.Dataset(bx, label=by, feature_name=features,
                params=common, free_raw_data=False)
            dataset.construct()
            binning.append({'year': year, 'construction_seconds': time.perf_counter()-ds_started,
                'training_rows': int(mask.sum()), 'reused_by_actual_models': list(configs)})
            selected = vd // 10000 == year
            test = vx[selected] if year < 2025 else bx[:1000]
            for name, cfg in configs.items():
                write(OUT / 'actual_stage.json', {'status': 'actual_native_training',
                    'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'year': year,
                    'model': name, 'actual_complete_fits': len(records), 'expected_fits': 36,
                    'available_RAM_GiB': psutil.virtual_memory().available / 2**30,
                    'CPU_threads': threads, 'GPU_training_started_by_this_bank': False})
                params = {**common, **cfg}
                fit_started = time.perf_counter()
                booster = lgb.train(params, dataset, num_boost_round=256)
                fit_seconds = time.perf_counter()-fit_started
                native = OUT / name / f'model_{year}.txt'
                with native.open('x', encoding='utf-8') as stream:
                    stream.write(booster.model_to_string())
                dump = OUT / name / f'model_dump_{year}.json'
                create(dump, booster.dump_model())
                saved = lgb.Booster(model_str=native.read_text(encoding='utf-8'))
                actual = booster.predict(test, num_threads=threads)
                replay = saved.predict(test, num_threads=threads)
                independent = predict_dump(read(dump), test)
                assert np.array_equal(actual.view(np.uint64), replay.view(np.uint64))
                assert np.array_equal(actual.view(np.uint64), independent.view(np.uint64))
                controls = []
                if year < 2025:
                    outputs[name][positions[selected]] = actual
                    for count in (80, 260, 975):
                        prefix = vd[selected] <= all_days[count-1]
                        cold = saved.predict(test[prefix], num_threads=threads) if prefix.any() else np.empty(0)
                        assert np.array_equal(actual[prefix].view(np.uint64), cold.view(np.uint64))
                        controls.append({'days': count, 'actual_flagged_rows': int(prefix.sum()), 'bits_exact': True})
                item = {'name': name, 'year': year, 'features': features, 'parameters': params,
                    'training_rows': int(mask.sum()), 'training_target_numeric_sha256': numeric_sha(by),
                    'last_training_label_date': last, 'last_training_label_end': end,
                    'exclusive_cutoff': cutoff, 'actual_tree_count': booster.num_trees(),
                    'maximum_boosting_rounds': 256, 'fit_seconds': fit_seconds,
                    'native_model_path': str(native), 'native_model_sha256': sha(native),
                    'independent_tree_dump_path': str(dump), 'independent_tree_dump_sha256': sha(dump),
                    'actual_control_rows': len(test), 'native_saved_independent_bits_exact': True,
                    'actual_cold_prefix_controls': controls, 'new_native_model_fits': 1,
                    'future_test_features_or_labels_used': False}
                assert 1 <= item['actual_tree_count'] <= 256
                create(OUT / name / f'info_{year}.json', item)
                records.append(item)
                print({'model': name, 'year': year, 'fit_seconds': fit_seconds,
                    'actual_complete_fits': len(records), 'native_saved_independent_bits_exact': True}, flush=True)
                del booster, saved, actual, replay, independent
                gc.collect()
            del dataset, bx, by
            gc.collect()
        for name, values in outputs.items():
            assert np.all(values[frame['flag_limit_up'].to_numpy() == 0] == 0)
            np.save(OUT / name / 'flagged_oof_predictions.npy', values)
            create(OUT / name / 'oof_verification.json', {'status': 'passed', 'rows': len(values),
                'numeric_sha256': numeric_sha(values), 'prediction_array_sha256': sha(OUT / name / 'flagged_oof_predictions.npy'),
                'includes_actual2020_mature_direct_model': True, 'nonflagged_values_zero_unused': True,
                'output_is_centered_rank_add0.5_before_CDF': True, 'test_labels_read': False})
        assert len(records) == 36
        for path, digest in pins.items():
            assert sha(Path(path)) == digest, path
        create(OUT / 'verification.json', {'status': 'passed_actual36_direct_centered_rank_native_saved_independent_and_prefix_controls',
            'input_sha256': pins, 'configurations': configs, 'actual_native_fits': 36,
            'actual_models': records, 'actual_training_only_Dataset_constructions': binning,
            'six_dataset_constructions_instead_of36': True, 'CPU_threads': threads,
            'elapsed_seconds': time.perf_counter()-started, 'new_quality_score_records': 0,
            'complete_official92_comparisons_and_candidate_registration_pending': True,
            'test_labels_read': False})
        write(OUT / 'actual_stage.json', {'status': 'passed_actual36_native_fits_official_comparison_pending',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'actual_complete_fits': 36,
            'expected_fits': 36, 'CPU_threads': threads})


if __name__ == '__main__':
    try:
        main()
    except BaseException as error:
        if OUT.exists() and not (OUT / 'failure.json').exists():
            create(OUT / 'failure.json', {'status': 'failed_preserved_local_direct_rank_bank',
                'error': f'{type(error).__name__}: {error}', 'test_labels_read': False})
        raise
