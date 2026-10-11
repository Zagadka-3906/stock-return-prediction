"""Official training-only mapped-output comparison; final release remains separate."""
from pathlib import Path
from types import SimpleNamespace
import gc
import hashlib
import json
import os
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A), str(A / 'connected_validation_20261002')]
for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'POLARS_MAX_THREADS'):
    os.environ[key] = '4'
from run_dependency_queue_v3_20261006 import read, sha, create
from atomic_optimization_observer_writes_20261005 import write

OUT = A / 'causal_entry_exit_buffer_official_pilot_20261006'


def main():
    import psutil
    assert not OUT.exists()
    available = psutil.virtual_memory().available
    assert available >= 8 * 2**30, 'An 8GiB host reserve is required for this compact CPU-only pilot'
    assert psutil.disk_usage('D:/').free >= 3 * 2**30
    OUT.mkdir()
    scratch = ROOT / 'tmp/causal_entry_exit_buffer_official_pilot_20261006'
    scratch.mkdir(exist_ok=True)
    for key in ('TMP', 'TEMP', 'TMPDIR'): os.environ[key] = str(scratch)
    import tempfile
    tempfile.tempdir = str(scratch)
    import numpy as np
    import polars as pl
    from causal_entry_exit_buffer_v2_20261006 import transform
    from locked_read_hash_cache_20261004 import LockedReadHashCache
    from score_calibrated_candidates_20261003 import score
    controls_path = A / 'causal_entry_exit_buffer_full_controls_v3_20261006/verification.json'
    controls = read(controls_path)
    assert controls['status'] == 'passed_full5635800_row_entry_exit_buffer_causal_and_zero_identity_controls'
    parent = A / 'optimization_20261003_r85'
    panel = A / 'connected_validation_20261002/combined_fold_frame.parquet'
    aliases = [parent / 'scoring_validation_only' / name for name in ('测试集_X.csv', '测试集_Y.csv')]
    # These immutable aliases contain training OOF rows, never the future X/Y.
    source_files = [Path(__file__), controls_path, A / 'score_calibrated_candidates_20261003.py',
        A / 'cross_round_official_score_reuse_20261003.py',
        A / 'official_validation_csv_parse_cache_20261003.py',
        A / 'identical_official_score_cache_20261003.py',
        A / 'connected_validation_20261002/return_mapping.py',
        ROOT / 'evaluate.py', ROOT / 'src/scoring.py', ROOT / 'run.py', *aliases]
    pins = {**controls['input_sha256'], **{str(path): sha(path) for path in source_files}}
    raw_training = str((ROOT / 'data/raw/训练集.csv').resolve())
    protocol = read(parent / 'protocol.json')
    # Original mapping reads only mature pre-2020 rows from this training file.
    expected_training_sha = protocol['input_sha256'].get(raw_training)
    pins[raw_training] = expected_training_sha or sha(raw_training)
    cases = controls['actual_all16_margin_controls']
    assert len(cases) == 16
    create(OUT / 'frozen_before_actual_official_scores.json', {
        'status': 'frozen16_case_full_continuous_training_official_return_mapped_pilot',
        'input_sha256': pins, 'cases': [{'margin': row['margin'],
            'controlled_prediction_numeric_bytes_sha256': row['full_prediction_numeric_bytes_sha256']} for row in cases],
        'training_parent_round': 85, 'parent_official_metrics': read(parent / 'calibrated_csv_official.json')['metrics'],
        'expected_rows_days_codes': [5635800, 1212, 4650],
        'official_input_aliases_are_training_OOF_data': True,
        'initial_available_host_bytes': available, 'CPU_threads': 4,
        'no_new_model_fits_or_GPU_work': True, 'test_labels_read': False,
        'full_candidate_freeze_inference_and_ranking_qualification_pending': True})
    results = []
    resources = []
    with LockedReadHashCache(pins):
        frame = pl.read_parquet(panel, columns=['ts_code', 'trade_date', 'flag_limit_up', 'y_ret_1d'])
        symbols = frame.select('ts_code').unique().sort('ts_code').with_row_index('code')
        coded = frame.join(symbols, on='ts_code', how='left', maintain_order='left')
        dates = frame['trade_date'].to_numpy()
        flags = frame['flag_limit_up'].to_numpy()
        codes = coded['code'].to_numpy()
        del coded
        assert (len(frame), len(np.unique(dates)), len(symbols)) == (5635800, 1212, 4650)
        assert int(dates.min()) >= 20200101 and int(dates.max()) <= 20241231
        raw = np.load(parent / 'selected_validation.npy', mmap_mode='r')
        scoring = OUT / 'scoring_validation_only'
        scoring.mkdir()
        for path in aliases: os.link(path, scoring / path.name)
        context = SimpleNamespace(frame=frame, dates=dates, scoring=scoring)
        for index, case in enumerate(cases):
            write(OUT / 'state.json', {'status': 'running_original_official_mature_mapped_training_comparison',
                'pid': os.getpid(), 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
                'completed_records': len(results), 'expected_records': 16, 'current_margin': case['margin'],
                'test_labels_read': False, 'full_release_pending': True})
            started = time.perf_counter()
            prediction = transform(raw, dates, flags, codes, case['margin'])
            assert hashlib.sha256(memoryview(np.ascontiguousarray(prediction)).cast('B')).hexdigest() == case['full_prediction_numeric_bytes_sha256']
            metrics = score(context, prediction)
            if index == 0:
                assert metrics == read(parent / 'calibrated_csv_official.json')['metrics']
            assert context.last_candidate_return_mapping['within_day_ranks_bit_identical']
            assert all(row['mapping_last_label_date'] < row['exclusive_cutoff'] for row in context.last_candidate_return_mapping['boundaries'])
            capsule = Path(context.last_official_score_cache['official_metrics_source'])
            row = {'margin': case['margin'], 'metrics': metrics,
                'connected_final_score': metrics['final_score'], 'prediction_numeric_bytes_sha256': case['full_prediction_numeric_bytes_sha256'],
                'official_score_cache': context.last_official_score_cache,
                'actual_return_mapping': context.last_candidate_return_mapping,
                'official_csv_parse_cache': context.last_validation_csv_parse_cache,
                'official_metric_capsule_sha256': sha(capsule), 'elapsed_seconds': time.perf_counter()-started,
                'same_train_only_rows_days_and_year_boundary_turnover': True,
                'candidate_future_qualification_pending': True, 'test_labels_read': False}
            results.append(row)
            create(OUT / f'case{index:02d}_official.json', row)
            process = psutil.Process()
            resources.append({'completed_records': len(results), 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
                'RSS_bytes': process.memory_info().rss, 'host_available_bytes': psutil.virtual_memory().available})
            create(OUT / f'case{index:02d}_resource.json', resources[-1])
            print(json.dumps({'case': index, 'margin': case['margin'], 'score': metrics['final_score'],
                'annual_excess': metrics['annual_excess'], 'turnover': metrics['mean_turnover']}, ensure_ascii=False), flush=True)
            del prediction
            gc.collect()
    best = max(results, key=lambda row: (row['connected_final_score'], -row['margin']))
    baseline = results[0]['connected_final_score']
    create(OUT / 'verification.json', {
        'status': 'completed_actual16_training_official_scores_full_submission_release_pending',
        'input_sha256': pins, 'records': results, 'best': best,
        'score_gain_over_frozen_parent': best['connected_final_score'] - baseline,
        'all8_baseline_metrics_exact': True, 'continuous_rows': 5635800, 'days': 1212, 'stocks': 4650,
        'all_final_outputs_mature_return_mapped_and_original_official_scored': True,
        'new_native_fits': 0, 'new_quality_score_records': 16,
        'test_labels_read': False, 'candidate_inference_and_full_ranking_qualification_pending': True,
        'not_added_to_completed_full_board_yet': True, 'global_resource_exhaustion_established': False})
    write(OUT / 'state.json', {'status': 'completed_official_pilot_full_release_pending', 'pid': os.getpid(),
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'completed_records': 16,
        'best_score': best['connected_final_score'], 'best_margin': best['margin'],
        'gain': best['connected_final_score'] - baseline, 'test_labels_read': False})


if __name__ == '__main__':
    try: main()
    except BaseException as exc:
        if OUT.exists() and not (OUT / 'failure.json').exists():
            create(OUT / 'failure.json', {'status': 'failed_preserved_official_buffer_pilot',
                'error': f'{type(exc).__name__}: {exc}'})
        raise
