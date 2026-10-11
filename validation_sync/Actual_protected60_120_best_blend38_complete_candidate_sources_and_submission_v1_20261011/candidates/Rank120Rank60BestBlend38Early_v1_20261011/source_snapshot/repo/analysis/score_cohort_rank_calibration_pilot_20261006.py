"""Score all 17 controlled cohort schemes on continuous training OOF rows."""
from pathlib import Path
from types import SimpleNamespace
import gc
import hashlib
import os
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A), str(A / 'connected_validation_20261002')]
for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'POLARS_MAX_THREADS'):
    os.environ[key] = '4'
from run_dependency_queue_v3_20261006 import read, create, sha, owned
from atomic_optimization_observer_writes_20261005 import write

OUT = A / 'cohort_rank_calibration_official_pilot_20261006'
CONTROL = A / 'cohort_rank_calibration_full_controls_20261006'


def main():
    import psutil
    assert psutil.virtual_memory().available >= 8 * 2**30
    assert psutil.disk_usage('D:/').free >= 3 * 2**30
    service = A / 'service_owned_workflows_20261006/cohort_rank_calibration_controls'
    assert not owned(read(service / 'native_launch.json'))
    assert read(service / 'service_execution.json')['status'] == 'passed'
    assert not OUT.exists()
    OUT.mkdir()
    scratch = ROOT / 'tmp/cohort_rank_calibration_official_pilot_20261006'
    scratch.mkdir(exist_ok=True)
    for key in ('TMP', 'TEMP', 'TMPDIR'):
        os.environ[key] = str(scratch)
    import numpy as np
    import polars as pl
    import cohort_rank_calibration_20261006 as method
    from score_calibrated_candidates_20261003 import score
    from locked_read_hash_cache_20261004 import LockedReadHashCache
    control = read(CONTROL / 'verification.json')
    assert control['status'] == 'passed_full17_cohort_causal_prefix_and_nonflagged_order_controls'
    parent = A / 'optimization_20261003_r95'
    aliases = [parent / 'scoring_validation_only' / f for f in ('测试集_X.csv', '测试集_Y.csv')]
    source_files = [Path(__file__), Path(method.__file__), CONTROL / 'verification.json',
        A / 'score_calibrated_candidates_20261003.py', A / 'cross_round_official_score_reuse_20261003.py',
        A / 'official_validation_csv_parse_cache_20261003.py', A / 'identical_official_score_cache_20261003.py',
        A / 'connected_validation_20261002/return_mapping.py', ROOT / 'evaluate.py', ROOT / 'src/scoring.py',
        ROOT / 'data/raw/训练集.csv', *aliases]
    pins = {**control['input_sha256'], **control['output_sha256'], **{str(p): sha(p) for p in source_files}}
    cases = control['actual_cases']
    assert len(cases) == 17
    baseline = read(parent / 'calibrated_csv_official.json')['metrics']
    create(OUT / 'frozen_before_actual_official_scores.json', {
        'input_sha256': pins, 'cases': cases, 'parent_round': 95,
        'parent_official_metrics': baseline, 'rows_days_stocks': [5635800, 1212, 4650],
        'selection_rule': 'Highest original official complete mapped-output S; exact ties prefer zero cohort weight',
        'training_OOF_aliases_only': True, 'annual_boundary_turnover_continuous': True,
        'all17_final_return_mapped_CSVs_original_official_scored': True,
        'official_scores_not_full_candidate_qualification': True, 'test_labels_read': False,
        'actual_annual_cohort_calibration_fits_reused': 16, 'new_native_base_model_fits': 0})
    rows = []
    with LockedReadHashCache(pins):
        frame = pl.read_parquet(A / 'connected_validation_20261002/combined_fold_frame.parquet',
            columns=['ts_code', 'trade_date', 'flag_limit_up', 'y_ret_1d'])
        dates, flags = frame['trade_date'].to_numpy(), frame['flag_limit_up'].to_numpy()
        assert len(frame) == 5635800 and len(np.unique(dates)) == 1212
        raw = np.load(parent / 'selected_validation.npy', mmap_mode='r')
        percentile = np.load(CONTROL / 'parent_percentile.npy', mmap_mode='r')
        scoring = OUT / 'scoring_validation_only'
        scoring.mkdir()
        for p in aliases:
            os.link(p, scoring / p.name)
        ctx = SimpleNamespace(frame=frame, dates=dates, scoring=scoring)
        for i, case in enumerate(cases):
            write(OUT / 'state.json', {'status': 'running_original_official_cohort_mapped_output_comparison',
                'pid': os.getpid(), 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
                'completed_records': len(rows), 'expected_records': 17, 'current_case': case,
                'test_labels_read': False, 'full_candidate_and_ranking_pending': True})
            started = time.perf_counter()
            model_path = CONTROL / f"annual_models_{case['annual_model_key']}.json" if i else None
            models = read(model_path)['annual_models'] if model_path else {}
            prediction = method.transform(raw, dates, flags, models, case['weight'], percentile=percentile)
            assert hashlib.sha256(memoryview(np.ascontiguousarray(prediction)).cast('B')).hexdigest() == case['full_prediction_numeric_bytes_sha256']
            metrics = score(ctx, prediction)
            if i == 0:
                assert metrics == baseline
            for field in ('annual_excess', 'mean_turnover', 'top1_annual_ret'):
                assert metrics[field] == baseline[field], field
            assert abs((metrics['final_score'] - baseline['final_score']) - .4 * (metrics['ic_mean'] - baseline['ic_mean'])) < 1e-15
            assert ctx.last_candidate_return_mapping['within_day_ranks_bit_identical']
            assert all(v['mapping_last_label_date'] < v['exclusive_cutoff'] for v in ctx.last_candidate_return_mapping['boundaries'])
            capsule = Path(ctx.last_official_score_cache['official_metrics_source'])
            row = {'case': i, 'configuration': {k: case[k] for k in ('weight', 'bins', 'pseudocount')},
                'annual_model_source': str(model_path) if model_path else None,
                'annual_model_sha256': sha(model_path) if model_path else None,
                'metrics': metrics, 'connected_final_score': metrics['final_score'],
                'score_gain_over_parent': metrics['final_score'] - baseline['final_score'],
                'prediction_numeric_bytes_sha256': case['full_prediction_numeric_bytes_sha256'],
                'official_score_cache': ctx.last_official_score_cache,
                'official_metric_capsule_sha256': sha(capsule),
                'actual_return_mapping': ctx.last_candidate_return_mapping,
                'all3_nonIC_terms_exactly_preserved': True,
                'elapsed_seconds': time.perf_counter() - started,
                'candidate_inference_and_full_ranking_pending': True, 'test_labels_read': False}
            rows.append(row)
            create(OUT / f'case{i:02d}_official.json', row)
            print(__import__('json').dumps({'case': i, 'parameters': row['configuration'],
                'score': metrics['final_score'], 'gain': row['score_gain_over_parent'],
                'IC': metrics['ic_mean'], 'seconds': row['elapsed_seconds']}, ensure_ascii=False), flush=True)
            del prediction
            gc.collect()
    best = min(rows, key=lambda r: (-r['connected_final_score'], r['configuration']['weight'], r['case']))
    create(OUT / 'verification.json', {'status': 'completed_actual17_cohort_original_official_scores_full_qualification_pending',
        'input_sha256': pins, 'records': rows, 'best': best,
        'score_gain_over_frozen_parent': best['connected_final_score'] - baseline['final_score'],
        'all_baseline8_metrics_exact': True, 'all17_return_turnover_terms_exact': True,
        'actual_annual_cohort_calibration_fits': 16, 'new_native_base_model_fits': 0,
        'new_quality_score_records': 17, 'test_labels_read': False,
        'all_candidate_freeze_inference_causal_and_complete_ranking_checks_still_required': True,
        'not_added_to_full_qualified_board_yet': True, 'global_resource_exhaustion_established': False})


if __name__ == '__main__':
    try:
        main()
    except BaseException as exc:
        if OUT.exists() and not (OUT / 'failure.json').exists():
            create(OUT / 'failure.json', {'status': 'failed_preserved_official_cohort_pilot',
                'error': f'{type(exc).__name__}: {exc}', 'test_labels_read': False})
        raise
