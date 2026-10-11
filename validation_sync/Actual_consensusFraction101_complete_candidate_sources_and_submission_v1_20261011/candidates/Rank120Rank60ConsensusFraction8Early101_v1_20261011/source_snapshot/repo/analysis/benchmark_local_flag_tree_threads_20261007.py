"""Measure local CPU throughput; choose threads only when trained trees are identical."""
from pathlib import Path
import os
import sys
import time
import statistics

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'POLARS_MAX_THREADS'):
    os.environ[key] = '2'
from run_dependency_queue_v3_20261006 import read, create, sha

OUT = A / 'local_flag_tree_thread_benchmark_20261007'


def main():
    import lightgbm as lgb
    import polars as pl
    import numpy as np
    from run import fold_cutoff
    from conditional_flag_rank_codec_20261006 import clean_matrix
    from locked_read_hash_cache_20261004 import LockedReadHashCache
    assert not OUT.exists()
    OUT.mkdir()
    source = A / 'conditional_flag_rank_bank_v2_20261006/flagged_training_targets_and_features.parquet'
    paths = [Path(__file__), source, ROOT / 'data/feature_manifest.json', ROOT / 'run.py',
             A / 'conditional_flag_rank_codec_20261006.py']
    pins = {str(p): sha(p) for p in paths}
    create(OUT / 'frozen_benchmark.json', {'input_sha256': pins, 'threads': [2, 4, 8],
        'repeats': 2, 'boosting_rounds': 128, 'training_window': 'mature before2024',
        'quality_score_records': 0, 'hardware_selection_only': True,
        'must_match_all_native_tree_structures_and_prediction_bits': True})
    with LockedReadHashCache(pins):
        frame = pl.read_parquet(source).filter(pl.col('trade_date') < fold_cutoff(2024))
        features = read(ROOT / 'data/feature_manifest.json')['features']
        x = clean_matrix(frame.select(features).to_numpy())
        y = frame['target_rank'].to_numpy()
        records = []
        reference_trees = reference_prediction = None
        for repeat in range(2):
            for threads in (2, 4, 8):
                params = {'objective': 'regression_l2', 'metric': 'None', 'learning_rate': .05,
                    'deterministic': True, 'force_col_wise': True, 'num_threads': threads,
                    'seed': 20261006, 'verbosity': -1, 'max_bin': 127,
                    'feature_fraction': 1., 'bagging_fraction': 1., 'bagging_freq': 0,
                    'use_missing': True, 'zero_as_missing': False, 'num_leaves': 31,
                    'max_depth': 5, 'min_data_in_leaf': 128, 'lambda_l2': 10.}
                started = time.perf_counter()
                dataset = lgb.Dataset(x, label=y, feature_name=features, params=params)
                booster = lgb.train(params, dataset, num_boost_round=128)
                elapsed = time.perf_counter() - started
                trees = booster.dump_model()['tree_info']
                prediction = booster.predict(x[:10000], num_threads=threads)
                if reference_trees is None:
                    reference_trees, reference_prediction = trees, prediction
                exact = trees == reference_trees and np.array_equal(
                    prediction.view(np.uint64), reference_prediction.view(np.uint64))
                records.append({'repeat': repeat, 'threads': threads,
                    'elapsed_seconds_including_matrix_binning': elapsed,
                    'native_trees_and_prediction_bits_equal_2thread_reference': exact})
                create(OUT / f'actual_{repeat}_{threads}.json', records[-1])
                print(records[-1], flush=True)
                del booster, dataset
        timings = {str(t): statistics.median(r['elapsed_seconds_including_matrix_binning']
                    for r in records if r['threads'] == t) for t in (2, 4, 8)}
        eligible = [t for t in (2, 4, 8) if all(r['native_trees_and_prediction_bits_equal_2thread_reference']
                    for r in records if r['threads'] == t)]
        selected = min(eligible, key=lambda t: (timings[str(t)], t))
        create(OUT / 'verification.json', {'status': 'passed_actual_local_thread_throughput_and_exact_native_controls',
            'input_sha256': pins, 'training_rows': len(frame), 'records': records,
            'median_seconds': timings, 'selected_threads': selected,
            'measured_speedup_over_2_threads': timings['2'] / timings[str(selected)],
            'diagnostic_native_fits': 6, 'new_quality_score_records': 0,
            'benchmark_is_not_official_model_selection': True, 'test_labels_read': False})


if __name__ == '__main__':
    main()
