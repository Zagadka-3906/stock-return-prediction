"""Train genuine flag-only return-rank specialists with mature annual cutoffs."""
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
OUT = A / 'conditional_flag_rank_bank_20261006'
CONFIGS = {
    'flag_rank_leaf7_e64': {'num_leaves': 7, 'max_depth': 3, 'min_data_in_leaf': 128, 'lambda_l2': 10.},
    'flag_rank_leaf15_e64': {'num_leaves': 15, 'max_depth': 4, 'min_data_in_leaf': 128, 'lambda_l2': 10.},
    'flag_rank_leaf31_e64': {'num_leaves': 31, 'max_depth': 5, 'min_data_in_leaf': 256, 'lambda_l2': 25.}}


def numeric_sha(values):
    import numpy as np
    return hashlib.sha256(memoryview(np.ascontiguousarray(values)).cast('B')).hexdigest()


def main():
    import psutil
    assert not OUT.exists()
    OUT.mkdir()
    original = read(A / 'optimization_20261003_r95/protocol.json')['input_sha256']
    paths = [ROOT / 'data/raw/训练集.csv', ROOT / 'data/features.parquet',
             ROOT / 'data/feature_manifest.json', ROOT / 'src/features.py', ROOT / 'run.py',
             A / 'connected_validation_20261002/combined_fold_frame.parquet',
             A / 'cohort_rank_calibration_full_controls_20261006/historical_label_percentile.npy',
             A / 'cohort_rank_calibration_full_controls_20261006/verification.json',
             A / 'conditional_flag_rank_codec_20261006.py', Path(__file__)]
    pins = {str(p): original[str(p)] if str(p) in original else sha(p) for p in paths}
    create(OUT / 'frozen_before_actual_training.json', {
        'input_sha256': pins, 'configurations': CONFIGS, 'annual_years': [2020, 2021, 2022, 2023, 2024],
        'prospective_final_training_year': 2025, 'expected_actual_native_fits': 18,
        'target': 'Official float64 historical daily finite-pool return rank divided by finite count plus one',
        'cohort': 'Training rows with supplied flag_limit_up == 1',
        'first2020_fit_includes_only_mature_pre2020_training_labels': True,
        'maximum_boosting_rounds': 64, 'no_validation_early_stopping_or_hyperparameter_selection': True,
        'selection_and_complete_official_scoring_still_required': True,
        'future_test_features_or_labels_not_used_by_this_bank': True, 'test_labels_read': False})
    while psutil.virtual_memory().available < 9 * 2**30:
        time.sleep(30)
    import numpy as np
    import polars as pl
    import lightgbm as lgb
    from run import fold_cutoff
    from conditional_flag_rank_codec_20261006 import clean_matrix, predict_dump
    from locked_read_hash_cache_20261004 import LockedReadHashCache
    features = read(ROOT / 'data/feature_manifest.json')['features']
    assert len(features) == 63 and not set(features) & {'y_ret_1d', 'y_rank', 'is_train', 'row_id', 'trade_date', 'ts_code'}
    with LockedReadHashCache(pins):
        # All finite-label stocks participate in the rank denominator before
        # restricting training to the supplied flag cohort.
        labels = pl.read_csv(ROOT / 'data/raw/训练集.csv',
            columns=['ts_code', 'trade_date', 'y_ret_1d', 'flag_limit_up'],
            schema_overrides={'trade_date': pl.Int32, 'y_ret_1d': pl.Float64})
        assert labels.select(pl.struct('ts_code', 'trade_date').n_unique()).item() == len(labels)
        train_days = np.sort(labels['trade_date'].unique().to_numpy())
        assert train_days.max() < 20250101 and not labels['y_ret_1d'].is_infinite().any()
        finite = labels.filter(pl.col('y_ret_1d').is_finite())
        ranked = finite.with_columns((pl.col('y_ret_1d').rank(method='average').over('trade_date') /
            (pl.len().over('trade_date') + 1.)).alias('target_rank'))
        targets = ranked.filter(pl.col('flag_limit_up') == 1).select('ts_code', 'trade_date', 'target_rank')
        del labels, ranked, finite
        gc.collect()
        matrix = pl.scan_parquet(ROOT / 'data/features.parquet').filter(
            pl.col('is_train') & (pl.col('flag_limit_up') == 1)).select(['ts_code', 'trade_date', *features]).collect()
        assert matrix['trade_date'].max() < 20250101
        assert matrix.select(pl.struct('ts_code', 'trade_date').n_unique()).item() == len(matrix)
        historical = matrix.join(targets, on=['ts_code', 'trade_date'], how='inner', validate='1:1').sort('trade_date', 'ts_code')
        assert historical['target_rank'].is_finite().all() and len(historical)
        frame = pl.read_parquet(A / 'connected_validation_20261002/combined_fold_frame.parquet',
            columns=['ts_code', 'trade_date', 'flag_limit_up'])
        assert len(frame) == 5635800 and frame['trade_date'].n_unique() == 1212 and frame['ts_code'].n_unique() == 4650
        flagged = frame.with_row_index('oof_position').filter(pl.col('flag_limit_up') == 1)
        keyed = flagged.join(matrix.drop('flag_limit_up'), on=['ts_code', 'trade_date'], how='left', validate='1:1').sort('oof_position')
        assert len(keyed) == len(flagged) and keyed['ts_code'].equals(flagged['ts_code'])
        check = flagged.join(targets, on=['ts_code', 'trade_date'], how='left', validate='1:1').sort('oof_position')
        reference = np.load(A / 'cohort_rank_calibration_full_controls_20261006/historical_label_percentile.npy', mmap_mode='r')
        actual_targets = check['target_rank'].to_numpy()
        expected_targets = reference[check['oof_position'].to_numpy()]
        assert np.array_equal(np.isnan(actual_targets), np.isnan(expected_targets))
        mask = np.isfinite(actual_targets)
        assert np.array_equal(actual_targets[mask].view(np.uint64), expected_targets[mask].view(np.uint64))
        historical.write_parquet(OUT / 'flagged_training_targets_and_features.parquet')
        keyed.write_parquet(OUT / 'flagged_validation_features.parquet')
        create(OUT / 'actual_target_and_feature_alignment.json', {
            'status': 'passed_original_float64_train_targets_exactly_match_all_official_OOF_flagged_targets',
            'historical_flagged_finite_rows': len(historical), 'validation_flagged_rows': len(flagged),
            'features': features, 'target_dtype': 'float64',
            'all_targets_use_whole_finite_label_pool_before_cohort_filter': True,
            'flagged_training_parquet_sha256': sha(OUT / 'flagged_training_targets_and_features.parquet'),
            'flagged_validation_parquet_sha256': sha(OUT / 'flagged_validation_features.parquet'),
            'test_labels_read': False})
        x = clean_matrix(historical.select(features).to_numpy())
        y = historical['target_rank'].to_numpy()
        dates = historical['trade_date'].to_numpy()
        validation_x = clean_matrix(keyed.select(features).to_numpy())
        validation_dates = keyed['trade_date'].to_numpy()
        positions = keyed['oof_position'].to_numpy()
        records = []
        for name, cfg in CONFIGS.items():
            folder = OUT / name
            folder.mkdir()
            oof = np.zeros(len(frame), dtype=np.float64)
            for year in (2020, 2021, 2022, 2023, 2024, 2025):
                cutoff = fold_cutoff(year)
                training = dates < cutoff
                assert training.sum() >= 300
                last = int(dates[training].max())
                label_end = int(train_days[np.searchsorted(train_days, last) + 1])
                assert last < cutoff and label_end <= cutoff
                params = {'objective': 'regression', 'metric': 'None', 'learning_rate': .05,
                    'deterministic': True, 'force_col_wise': True, 'num_threads': 2,
                    'seed': 20261006, 'verbosity': -1, 'max_bin': 127,
                    'feature_fraction': 1., 'bagging_fraction': 1., 'bagging_freq': 0,
                    'use_missing': True, 'zero_as_missing': False, **cfg}
                dataset = lgb.Dataset(x[training], label=y[training], feature_name=features, params=params)
                booster = lgb.train(params, dataset, num_boost_round=64)
                model_text = booster.model_to_string()
                model_dump = booster.dump_model()
                native_path = folder / f'model_{year}.txt'
                with native_path.open('x', encoding='utf-8') as stream:
                    stream.write(model_text)
                create(folder / f'model_dump_{year}.json', model_dump)
                actual_trees = booster.num_trees()
                assert 1 <= actual_trees <= 64
                selected = validation_dates // 10000 == year
                test = validation_x[selected] if year != 2025 else x[training][:min(1000, int(training.sum()))]
                primary = booster.predict(test, num_threads=2)
                reload = lgb.Booster(model_file=str(native_path)).predict(test, num_threads=2)
                independent = predict_dump(read(folder / f'model_dump_{year}.json'), test)
                assert np.array_equal(primary.view(np.uint64), reload.view(np.uint64))
                assert np.array_equal(primary.view(np.uint64), independent.view(np.uint64))
                # Prediction receives only features. Clearing or replacing labels
                # cannot affect these real saved-model and independent-tree decoders.
                if year != 2025:
                    oof[positions[selected]] = primary
                    for count in (80, 260, 975):
                        end_day = frame['trade_date'].unique().sort()[count - 1]
                        prefix = validation_dates[selected] <= end_day
                        cold = lgb.Booster(model_file=str(native_path)).predict(test[prefix], num_threads=2) if prefix.any() else np.empty(0)
                        assert np.array_equal(cold.view(np.uint64), primary[prefix].view(np.uint64))
                record = {'name': name, 'year': year, 'features': features,
                    'training_rows': int(training.sum()), 'last_training_label_date': last,
                    'last_training_label_end': label_end, 'exclusive_cutoff': cutoff,
                    'native_model_path': str(native_path), 'native_model_sha256': sha(native_path),
                    'independent_tree_dump_path': str(folder / f'model_dump_{year}.json'),
                    'independent_tree_dump_sha256': sha(folder / f'model_dump_{year}.json'),
                    'actual_tree_count': actual_trees, 'maximum_boosting_rounds': 64,
                    'actual_control_rows': len(test), 'original_native_saved_and_independent_decoders_full_bits_exact': True,
                    'actual_cold80_260_975_flagged_prefixes_exact': year != 2025,
                    'target': 'official finite-pool historical return rank', 'parameters': params,
                    'new_native_model_fits': 1, 'future_test_features_or_labels_used': False}
                create(folder / f'info_{year}.json', record)
                records.append(record)
                print(__import__('json').dumps({'model': name, 'year': year, 'mature_rows': int(training.sum()),
                    'actual_tree_count': actual_trees, 'full_independent_codec_bits_exact': True}), flush=True)
                del booster, dataset
                gc.collect()
            np.save(folder / 'flagged_oof_predictions.npy', oof)
            create(folder / 'oof_verification.json', {'status': 'passed', 'rows': len(oof),
                'flagged_rows': len(flagged), 'numeric_sha256': numeric_sha(oof),
                'all_nonflagged_outputs_zero_and_not_used_by_scheme': True,
                'prediction_array_sha256': sha(folder / 'flagged_oof_predictions.npy'),
                'official_complete_scheme_score_not_computed': True, 'test_labels_read': False})
        create(OUT / 'verification.json', {'status': 'passed_actual18_mature_flag_specialists_native_and_independent_codec_controls',
            'input_sha256': pins, 'configurations': CONFIGS, 'actual_native_fits': len(records),
            'actual_models': records, 'all_annual_native_reload_independent_codec_and_prefix_controls_passed': True,
            'pre2020_training_labels_used_only_for_valid_2020_first_year_model': True,
            'actual_whole_official_label_pool_targets_bit_exact': True,
            'official_complete_scheme_comparisons_and_frozen_candidate_qualification_pending': True,
            'new_quality_score_records': 0, 'test_labels_read': False})


if __name__ == '__main__':
    try:
        main()
    except BaseException as exc:
        if OUT.exists() and not (OUT / 'failure.json').exists():
            create(OUT / 'failure.json', {'status': 'failed_preserved_conditional_flag_native_training',
                'error': f'{type(exc).__name__}: {exc}', 'test_labels_read': False})
        raise
