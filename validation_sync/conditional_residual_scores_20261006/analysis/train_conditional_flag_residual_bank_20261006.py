"""Fit conditional residuals using mature OOF ranks and supplied causal features."""
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
from run_dependency_queue_v3_20261006 import read, create, sha, owned
from atomic_optimization_observer_writes_20261005 import write

OUT = A / 'conditional_flag_residual_bank_20261006'
CONFIGS = {
    'flag_residual_rank_only_leaf7_e64': {'num_leaves': 7, 'max_depth': 3, 'min_data_in_leaf': 128, 'lambda_l2': 10., 'rank_only': True},
    'flag_residual_leaf7_e64': {'num_leaves': 7, 'max_depth': 3, 'min_data_in_leaf': 128, 'lambda_l2': 10., 'rank_only': False},
    'flag_residual_leaf15_e64': {'num_leaves': 15, 'max_depth': 4, 'min_data_in_leaf': 128, 'lambda_l2': 10., 'rank_only': False},
    'flag_residual_leaf31_e64': {'num_leaves': 31, 'max_depth': 5, 'min_data_in_leaf': 256, 'lambda_l2': 25., 'rank_only': False}}


def numeric_sha(values):
    import numpy as np
    return hashlib.sha256(memoryview(np.ascontiguousarray(values)).cast('B')).hexdigest()


def main():
    import psutil
    assert not OUT.exists()
    OUT.mkdir()
    paths = [Path(__file__), A / 'conditional_flag_rank_codec_20261006.py',
        A / 'cohort_rank_calibration_v2_20261006.py',
        A / 'conditional_flag_rank_bank_v2_20261006/flagged_validation_features.parquet',
        A / 'conditional_flag_rank_bank_v2_20261006/actual_target_and_feature_alignment.json',
        A / 'conditional_flag_rank_bank_v2_20261006/verification.json',
        A / 'extended_cohort_rank_calibration_full_controls_20261006/parent_percentile.npy',
        A / 'extended_cohort_rank_calibration_full_controls_20261006/historical_label_percentile.npy',
        A / 'extended_cohort_rank_calibration_full_controls_20261006/annual_models_b16_s0.json',
        A / 'extended_cohort_rank_calibration_full_controls_20261006/verification.json',
        A / 'connected_validation_20261002/combined_fold_frame.parquet',
        ROOT / 'data/raw/训练集.csv', ROOT / 'data/feature_manifest.json',
        ROOT / 'run.py', ROOT / 'src/features.py', ROOT / '后续选模标准.md',
        ROOT / 'candidates/extended_cohort_rank_calibration_20261006/cohort_curve.json',
        ROOT / 'candidates/extended_cohort_rank_calibration_20261006/selection.json',
        ROOT / 'candidates/extended_cohort_rank_calibration_20261006/verification.json',
        ROOT / 'candidates/extended_cohort_rank_calibration_20261006/manifest.json']
    pins = {str(p): sha(p) for p in paths}
    create(OUT / 'frozen_before_actual_training.json', {
        'input_sha256': pins, 'configurations': CONFIGS, 'explicit_parent_round': 100,
        'annual_years': [2021, 2022, 2023, 2024], 'final_training_year': 2025,
        'expected_actual_native_fits': 20, 'maximum_boosting_rounds': 64,
        'features': '63 supplied causal features plus parent95 daily OOF percentile; rank-only ablation uses one percentile feature',
        'target': 'Official historical finite-pool return rank minus the annual mature training flagged curve',
        'annual_residual_targets_use_only_own_training_window_labels': True,
        'first2020_residual_identity_no_available_prior_full_scheme_OOF': True,
        'parent100_actual_full_registration_and_main_required_before_training': True,
        'no_validation_early_stopping_or_model_selection': True,
        'all_saved_native_independent_codec_and_cold80_260_975_controls_required': True,
        'no_future_test_features_or_labels_used': True, 'test_labels_read': False})
    predecessor = A / 'service_owned_workflows_20261006/conditional_flag_rank_official_comparison_v2'
    predecessor_identity = read(predecessor / 'native_launch.json')
    receipt = A / 'github_validation_sync_main_20261005/round100_receipt.json'
    while True:
        qualified = receipt.exists() and read(receipt)['status'] == 'pushed_and_remote_head_verified'
        closed = not owned(predecessor_identity)
        available = psutil.virtual_memory().available / 2**30
        write(OUT / 'waiting_status.json', {
            'status': 'waiting_for_parent100_full_main_and_previous_comparison_and_memory',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'parent100_actual_full_main_receipt_present': qualified,
            'previous37_comparison_live': not closed, 'available_RAM_GiB': available})
        if qualified and closed and available >= 9:
            assert read(predecessor / 'service_execution.json')['status'] == 'passed'
            break
        time.sleep(30)
    pins[str(receipt)] = sha(receipt)
    create(OUT / 'actual_training_admission.json', {
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins,
        'available_RAM_GiB': available, 'parent_full_main_receipt': read(receipt),
        'scientific_processes_suspended_or_restarted': 0, 'test_labels_read': False})
    import numpy as np
    import polars as pl
    import lightgbm as lgb
    from run import fold_cutoff
    from conditional_flag_rank_codec_20261006 import clean_matrix, predict_dump
    from locked_read_hash_cache_20261004 import LockedReadHashCache
    import cohort_rank_calibration_v2_20261006 as curve
    records = []
    with LockedReadHashCache(pins):
        frame = pl.read_parquet(A / 'connected_validation_20261002/combined_fold_frame.parquet',
            columns=['ts_code', 'trade_date', 'flag_limit_up'])
        assert len(frame) == 5635800 and frame['trade_date'].n_unique() == 1212
        keyed = pl.read_parquet(A / 'conditional_flag_rank_bank_v2_20261006/flagged_validation_features.parquet')
        flagged = frame.with_row_index('oof_position').filter(pl.col('flag_limit_up') == 1)
        assert keyed['oof_position'].equals(flagged['oof_position'])
        assert keyed.select('ts_code', 'trade_date').equals(flagged.select('ts_code', 'trade_date'))
        positions = keyed['oof_position'].to_numpy()
        dates, flags = frame['trade_date'].to_numpy(), frame['flag_limit_up'].to_numpy()
        p = np.load(A / 'extended_cohort_rank_calibration_full_controls_20261006/parent_percentile.npy', mmap_mode='r')
        target = np.load(A / 'extended_cohort_rank_calibration_full_controls_20261006/historical_label_percentile.npy', mmap_mode='r')
        assert len(p) == len(target) == len(frame)
        assert np.isfinite(p).all() and np.all((p > 0) & (p <= 1))
        features = read(ROOT / 'data/feature_manifest.json')['features']
        assert len(features) == 63 and not set(features) & {'y_ret_1d', 'y_rank', 'is_train', 'row_id', 'trade_date', 'ts_code'}
        feature_names = [*features, 'parent95_oof_percentile']
        x = clean_matrix(np.column_stack([keyed.select(features).to_numpy(), p[positions]]))
        cohort_dates, cohort_target = dates[positions], target[positions]
        finite = np.isfinite(cohort_target)
        train_days = pl.scan_csv(ROOT / 'data/raw/训练集.csv').select('trade_date').unique().sort('trade_date').collect()['trade_date'].to_numpy()
        annual = read(A / 'extended_cohort_rank_calibration_full_controls_20261006/annual_models_b16_s0.json')['annual_models']
        final = read(ROOT / 'candidates/extended_cohort_rank_calibration_20261006/cohort_curve.json')['model']
        fitted = {}
        for year in (2021, 2022, 2023, 2024, 2025):
            cutoff = fold_cutoff(year)
            model = curve.fit(p, target, flags, dates, cutoff, 16, 0.)
            assert model == (annual[str(year)] if year != 2025 else final)
            if year != 2025:
                poisoned = np.asarray(target).copy()
                poisoned[dates >= year * 10000 + 101] = np.nan
                assert model == curve.fit(p, poisoned, flags, dates, cutoff, 16, 0.)
                del poisoned
            fitted[str(year)] = model
        create(OUT / 'actual_parent_curve_and_current_year_poison_controls.json', {
            'status': 'passed_all5_past_curve_fits_equal_original_parent100_saved_curves',
            'annual_models': fitted, 'diagnostic_parent_curve_pair_refits': 5,
            'every_current_validation_year_label_poison_leaves_own_training_curve_exact': True,
            'new_quality_scores': 0, 'test_labels_read': False})
        all_days = np.sort(frame['trade_date'].unique().to_numpy())
        for name, cfg in CONFIGS.items():
            folder = OUT / name
            folder.mkdir()
            model_x = x[:, -1:] if cfg['rank_only'] else x
            model_features = feature_names[-1:] if cfg['rank_only'] else feature_names
            oof = np.zeros(len(frame), dtype=np.float64)
            for year in (2021, 2022, 2023, 2024, 2025):
                cutoff = fold_cutoff(year)
                training = (cohort_dates < cutoff) & finite
                assert training.sum() >= 300
                last = int(cohort_dates[training].max())
                end = int(train_days[np.searchsorted(train_days, last) + 1])
                assert last < cutoff and end <= cutoff
                model = fitted[str(year)]
                common = np.interp(p[positions][training], model['centers'], model['flagged_curve'])
                residual = cohort_target[training] - common
                assert np.isfinite(residual).all()
                params = {'objective': 'regression', 'metric': 'None', 'learning_rate': .05,
                    'deterministic': True, 'force_col_wise': True, 'num_threads': 2,
                    'seed': 20261006, 'verbosity': -1, 'max_bin': 127,
                    'feature_fraction': 1., 'bagging_fraction': 1., 'bagging_freq': 0,
                    'use_missing': True, 'zero_as_missing': False,
                    **{k: v for k, v in cfg.items() if k != 'rank_only'}}
                dataset = lgb.Dataset(model_x[training], label=residual, feature_name=model_features, params=params)
                booster = lgb.train(params, dataset, num_boost_round=64)
                native_path = folder / f'model_{year}.txt'
                with native_path.open('x', encoding='utf-8') as stream:
                    stream.write(booster.model_to_string())
                dump_path = folder / f'model_dump_{year}.json'
                create(dump_path, booster.dump_model())
                selected = cohort_dates // 10000 == year
                test = model_x[selected] if year != 2025 else model_x[training][:1000]
                primary = booster.predict(test, num_threads=2)
                saved = lgb.Booster(model_str=native_path.read_text(encoding='utf-8'))
                replay = saved.predict(test, num_threads=2)
                independent = predict_dump(read(dump_path), test)
                assert np.array_equal(primary.view(np.uint64), replay.view(np.uint64))
                assert np.array_equal(primary.view(np.uint64), independent.view(np.uint64))
                if year != 2025:
                    oof[positions[selected]] = primary
                    for count in (80, 260, 975):
                        prefix = cohort_dates[selected] <= all_days[count - 1]
                        cold = saved.predict(test[prefix], num_threads=2) if prefix.any() else np.empty(0)
                        assert np.array_equal(cold.view(np.uint64), primary[prefix].view(np.uint64))
                item = {'name': name, 'year': year, 'features': model_features,
                    'training_rows': int(training.sum()), 'last_training_label_date': last,
                    'last_training_label_end': end, 'exclusive_cutoff': cutoff,
                    'actual_tree_count': booster.num_trees(), 'maximum_boosting_rounds': 64,
                    'native_model_path': str(native_path), 'native_model_sha256': sha(native_path),
                    'independent_tree_dump_path': str(dump_path), 'independent_tree_dump_sha256': sha(dump_path),
                    'training_residual_numeric_sha256': numeric_sha(residual),
                    'annual_training_curve_sha256': hashlib.sha256(__import__('json').dumps(model, sort_keys=True).encode()).hexdigest(),
                    'actual_control_rows': len(test), 'parameters': params,
                    'original_native_saved_and_independent_decoders_full_bits_exact': True,
                    'actual_cold80_260_975_flagged_prefixes_exact': year != 2025,
                    'future_test_features_or_labels_used': False}
                assert 1 <= item['actual_tree_count'] <= 64
                create(folder / f'info_{year}.json', item)
                records.append(item)
                print(__import__('json').dumps({'model': name, 'year': year,
                    'mature_rows': item['training_rows'], 'actual_tree_count': item['actual_tree_count'],
                    'native_saved_independent_full_bits_exact': True}), flush=True)
                del booster, dataset, saved
                gc.collect()
            assert np.all(oof[flags == 0] == 0) and np.all(oof[dates < 20210101] == 0)
            np.save(folder / 'flagged_oof_predictions.npy', oof)
            create(folder / 'oof_verification.json', {'status': 'passed', 'rows': len(oof),
                'numeric_sha256': numeric_sha(oof), 'prediction_array_sha256': sha(folder / 'flagged_oof_predictions.npy'),
                'first2020_and_all_nonflagged_predictions_zero_identity': True,
                'new_quality_scores': 0, 'test_labels_read': False})
        assert len(records) == 20
        create(OUT / 'verification.json', {
            'status': 'passed_actual20_past_OOF_conditional_residual_native_models_and_independent_codec',
            'input_sha256': pins, 'configurations': CONFIGS, 'actual_native_fits': 20,
            'actual_models': records, 'diagnostic_parent_curve_pair_refits': 5,
            'first2020_identity': True, 'all_annual_native_saved_independent_and_prefix_controls_passed': True,
            'official_full_scheme_comparison_and_candidate_and_board_still_required': True,
            'new_quality_score_records': 0, 'test_labels_read': False})


if __name__ == '__main__':
    try:
        main()
    except BaseException as error:
        if OUT.exists() and not (OUT / 'failure.json').exists():
            create(OUT / 'failure.json', {'status': 'failed_preserved_conditional_residual_bank',
                'error': f'{type(error).__name__}: {error}', 'test_labels_read': False})
        raise
