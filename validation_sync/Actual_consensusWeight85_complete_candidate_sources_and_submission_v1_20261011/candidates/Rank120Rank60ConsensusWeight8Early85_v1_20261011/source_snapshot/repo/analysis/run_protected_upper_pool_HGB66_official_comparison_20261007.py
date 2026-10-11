"""66 predeclared official comparisons of complete parent forecasts and lower-pool CDF."""
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
    os.environ[key] = '2'
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from atomic_optimization_observer_writes_20261005 import write

OUT = A / 'protected_upper_pool_HGB66_official_comparison_20261007'
BANK = A / 'cpu_full_universe_HGB_bank24_recovery_v2_20261007'


def closed(name):
    service = A / 'service_owned_workflows_20261006' / name
    while owned(read(service / 'native_launch.json')):
        time.sleep(15)
    assert read(service / 'service_execution.json')['status'] == 'passed', name


def main():
    import numpy as np
    import polars as pl
    import psutil
    from protected_upper_pool_HGB_CDF_transform_20261007 import prepare, prepare_heads, apply_prepared, transform
    from score_calibrated_candidates_20261003 import score
    from official_date_index_dataframe_adapter_20261007 import installed
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    assert not OUT.exists()
    OUT.mkdir()
    for name in ('protected_upper_pool_HGB_CDF_full_preflight', 'cpu_full_universe_HGB24_bank_evidence_publication_v2',
        'CPU_HGB44_round112_full_registration_v2', 'CPU_FULL_HGB44_round113_full_registration_v3',
        'CPU_ELASTIC44_round114_full_registration_v2'):
        closed(name)
    for number, version in ((112, 23), (113, 24), (114, 25)):
        assert read(A / f'optimization_20261003_r{number}/full_registration_execution.json')['status'] == 'passed'
        assert read(A / f'github_validation_sync_main_20261005/round{number}_receipt.json')['actual_full_QA_version'] == version
    while psutil.virtual_memory().available < 11 * 2**30:
        time.sleep(15)
    plan_path = A / 'protected_upper_pool_HGB_CDF_plan_20261007.json'
    proof_path = A / 'protected_upper_pool_HGB_CDF_preflight_20261007/verification.json'
    plan, proof = read(plan_path), read(proof_path)
    assert proof['status'] == 'passed_actual63_full5635800_lower_pool_CDF_independent_oracle_and_cold80_260_975_controls'
    bank = read(BANK / 'verification.json')
    assert bank['actual_native_fits'] == 24
    parents = {n: A / f'optimization_20261003_r{n}' for n in plan['qualified_comparison_parent_candidates']}
    baseline = {n: read(p / 'calibrated_csv_official.json')['metrics'] for n, p in parents.items()}
    parent_number = min(parents, key=lambda n: (-baseline[n]['final_score'], n))
    components = {name: [name] for name in plan['single_native_heads']}
    components.update(plan['ensembles'])
    cases = [{'anchor_round': n, 'model': None, 'weight': 0., 'lower_fraction': None} for n in parents]
    cases += [{'anchor_round': parent_number, 'model': name, 'weight': weight, 'lower_fraction': fraction}
        for name in components for fraction in plan['lower_fractions'] for weight in plan['weights']]
    assert len(cases) == plan['expected_scored_records'] == 66
    frame_path = A / 'connected_validation_20261002/combined_fold_frame.parquet'
    sources = [Path(__file__), plan_path, proof_path, A / 'protected_upper_pool_HGB_CDF_transform_20261007.py',
        A / 'score_calibrated_candidates_20261003.py', A / 'official_date_index_dataframe_adapter_20261007.py',
        ROOT / 'evaluate.py', ROOT / '后续选模标准.md', frame_path, BANK / 'verification.json']
    sources += list(BANK.glob('*/raw_oof_predictions.npy')) + list(BANK.glob('*/info_*.json'))
    sources += list(BANK.glob('*/model_*.joblib')) + list(BANK.glob('*/independent_hist_tree_state_*.json'))
    for n, p in parents.items():
        sources += [p / name for name in ('selection.json', 'protocol.json', 'selected_validation.npy',
            'calibrated_csv_official.json', 'full_registration_execution.json')]
        sources += [A / f'github_validation_sync_main_20261005/round{n}_receipt.json']
    scoring_source = A / 'optimization_20261003_r95/scoring_validation_only'
    sources += [scoring_source / name for name in ('测试集_X.csv', '测试集_Y.csv')]
    pins = {**bank['input_sha256'], **{str(p): sha(p) for p in sources}}
    create(OUT / 'frozen_before_actual_full_controls_and_official_scores.json', {
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins, 'cases': cases,
        'actual_complete_qualified_comparison_parent_round': parent_number, 'baseline_official_metrics': baseline,
        'components': components, 'rows_days_stocks': [5635800, 1212, 4650],
        'new_native_model_fits': 0, 'no_extra_single_metric_Top_worst_year_or_significance_elimination': True,
        'selection_bias_uncorrected': True, 'test_labels_read': False})
    records = []
    with LockedReadHashCache(pins) as scope:
        frame = pl.read_parquet(frame_path, columns=['ts_code', 'trade_date', 'flag_limit_up', 'price_valid', 'y_ret_1d'])
        dates, flags, valid = [frame[c].to_numpy() for c in ('trade_date', 'flag_limit_up', 'price_valid')]
        assert (len(frame), frame['trade_date'].n_unique(), frame['ts_code'].n_unique()) == (5635800, 1212, 4650)
        raw = np.load(parents[parent_number] / 'selected_validation.npy', mmap_mode='r')
        heads = {name: np.load(BANK / name / 'raw_oof_predictions.npy', mmap_mode='r') for name in plan['single_native_heads']}
        scoring = OUT / 'scoring_validation_only'
        scoring.mkdir()
        for name in ('测试集_X.csv', '测试集_Y.csv'):
            os.link(scoring_source / name, scoring / name)
        ctx = SimpleNamespace(frame=frame, dates=dates, scoring=scoring)
        days, starts = np.unique(dates, return_index=True)
        ends = np.r_[starts[1:], len(dates)]
        prepared = {fraction: prepare(raw, dates, flags, valid, fraction) for fraction in plan['lower_fractions']}
        selected = {}
        for fraction, groups in prepared.items():
            selected[fraction] = np.zeros(len(raw), dtype=bool)
            for positions, _, _, _ in groups:
                selected[fraction][positions] = True
        head_cache = {}
        for index, cfg in enumerate(cases):
            if cfg['model'] is None:
                values = np.asarray(np.load(parents[cfg['anchor_round']] / 'selected_validation.npy', mmap_mode='r'))
            else:
                fraction = cfg['lower_fraction']
                model_heads = [heads[name] for name in components[cfg['model']]]
                key = (cfg['model'], fraction)
                if key not in head_cache:
                    head_cache[key] = prepare_heads(model_heads, prepared[fraction])
                values = apply_prepared(raw, cfg['weight'], prepared[fraction], head_cache[key])
                assert np.array_equal(values[~selected[fraction]].view(np.uint64), raw[~selected[fraction]].view(np.uint64))
                for positions, _, _, ordered in prepared[fraction]:
                    assert values[positions].min() >= ordered[0] and values[positions].max() <= ordered[-1]
                for count in (80, 260, 975):
                    n = int(ends[count - 1])
                    cold = transform(raw[:n], dates[:n], flags[:n], valid[:n], [h[:n] for h in model_heads], cfg['weight'], fraction)
                    assert np.array_equal(cold.view(np.uint64), values[:n].view(np.uint64))
            write(OUT / 'actual_stage.json', {'status': 'actual_complete_official_scoring',
                'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'case': index, 'configuration': cfg,
                'actual_completed_cases': len(records), 'expected_cases': 66})
            with installed(scoring / 'submission.csv') as date_index:
                metrics = score(ctx, values)
            if cfg['model'] is None:
                assert metrics == baseline[cfg['anchor_round']]
            capsule = Path(ctx.last_official_score_cache['official_metrics_source'])
            item = {'case': index, 'configuration': cfg, 'metrics': metrics,
                'connected_final_score': metrics['final_score'],
                'score_gain_over_qualified_parent': metrics['final_score'] - baseline[parent_number]['final_score'],
                'actual_comparison_parent_round': parent_number,
                'prediction_numeric_bytes_sha256': hashlib.sha256(memoryview(np.ascontiguousarray(values)).cast('B')).hexdigest(),
                'official_date_index_runtime': dict(date_index), 'official_score_cache': ctx.last_official_score_cache,
                'official_metric_capsule_sha256': sha(capsule), 'actual_return_mapping': ctx.last_candidate_return_mapping,
                'upper_boundary_ties_flags_and_invalid_parent_forecasts_bits_preserved': cfg['model'] is not None,
                'lower_forecasts_stay_in_selected_parent_range': cfg['model'] is not None,
                'actual_cold80_260_975_bits_exact': cfg['model'] is not None,
                'qualified_anchor_all8_metrics_exact': cfg['model'] is None,
                'native_bank_source': str(BANK / 'verification.json'), 'ordered_native_components': components.get(cfg['model']),
                'official_Top_invariance_not_used_as_selection_gate': True, 'test_labels_read': False,
                'selected_freeze_full_future_candidate_and_complete_QA_still_required': True}
            create(OUT / f'case{index:02d}_official.json', item)
            records.append(item)
            print({'case': index, 'score': metrics['final_score'], 'gain': item['score_gain_over_qualified_parent']}, flush=True)
            del values
            gc.collect()
        scope.reverify()
    best = min(records, key=lambda r: (-r['connected_final_score'], r['configuration']['weight'], r['case']))
    create(OUT / 'verification.json', {
        'status': 'passed_actual66_lower_pool_CPU_HGB_CDF_full_official_comparisons',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins, 'records': records,
        'best': best, 'components': components, 'actual_comparison_parent_round': parent_number,
        'existing_native_model_fits': 24, 'new_native_model_fits_by_comparison': 0,
        'new_quality_score_records': 66, 'all63_nonanchors_actual_full_and_three_cold_prefix_controls': True,
        'selected_candidate_full_future_inference_ranking_and_main_qualification_pending': True,
        'global_feasible_direction_or_resource_boundary_not_established': True, 'test_labels_read': False})


if __name__ == '__main__':
    main()
