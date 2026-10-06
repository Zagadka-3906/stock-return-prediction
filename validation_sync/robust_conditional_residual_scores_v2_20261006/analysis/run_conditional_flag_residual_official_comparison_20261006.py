"""Compare four genuine residual models and two ensembles with the full scorer."""
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
from run_dependency_queue_v3_20261006 import read, create, sha, owned
OUT = A / 'conditional_flag_residual_official_comparison_20261006'
BANK = A / 'conditional_flag_residual_bank_20261006'


def main():
    import psutil
    assert not OUT.exists()
    OUT.mkdir()
    service = A / 'service_owned_workflows_20261006/conditional_flag_residual_native_bank'
    identity = read(service / 'native_launch.json')
    while owned(identity):
        time.sleep(30)
    assert read(service / 'service_execution.json')['status'] == 'passed'
    bank = read(BANK / 'verification.json')
    assert bank['status'] == 'passed_actual20_past_OOF_conditional_residual_native_models_and_independent_codec'
    assert bank['actual_native_fits'] == 20
    while psutil.virtual_memory().available < 9 * 2**30:
        time.sleep(30)
    import numpy as np
    import polars as pl
    from scipy.stats import rankdata
    from conditional_flag_residual_transform_20261006 import transform
    from score_calibrated_candidates_20261003 import score
    from locked_read_hash_cache_20261004 import LockedReadHashCache
    parent = A / 'optimization_20261003_r100'
    original_models = list(bank['configurations'])
    supplied_feature_models = [name for name in original_models if not bank['configurations'][name]['rank_only']]
    ensembles = {'equal_mean_three_feature_residuals': supplied_feature_models,
        'equal_mean_all_four_residuals': original_models}
    heads = [*original_models, *ensembles]
    cases = [{'model': None, 'weight': 0.}]
    cases += [{'model': model, 'weight': weight} for model in heads
        for weight in (.01, .025, .05, .1, .25, .5, .75, 1.)]
    assert len(cases) == 49
    baseline = read(parent / 'calibrated_csv_official.json')['metrics']
    sources = [Path(__file__), A / 'conditional_flag_residual_transform_20261006.py',
        BANK / 'verification.json', *BANK.glob('*/flagged_oof_predictions.npy'),
        *BANK.glob('*/info_*.json'), *BANK.glob('*/model_*.txt'), *BANK.glob('*/model_dump_*.json'),
        parent / 'selected_validation.npy', parent / 'selection.json', parent / 'calibrated_csv_official.json',
        A / 'connected_validation_20261002/combined_fold_frame.parquet',
        A / 'score_calibrated_candidates_20261003.py', ROOT / 'evaluate.py', ROOT / '后续选模标准.md',
        A / 'optimization_20261003_r95/scoring_validation_only/测试集_X.csv',
        A / 'optimization_20261003_r95/scoring_validation_only/测试集_Y.csv']
    pins = {**bank['input_sha256'], **{str(p): sha(p) for p in sources}}
    create(OUT / 'frozen_before_actual_controls_and_official_scores.json', {
        'input_sha256': pins, 'cases': cases, 'ensembles': ensembles,
        'explicit_parent_round': 100, 'baseline_official_metrics': baseline,
        'rows_days_stocks': [5635800, 1212, 4650], 'native_bank_fits': 20,
        'first2020_and_all_nonflagged_raw_values_exact_parent_identity_required': True,
        'all49_final_past_return_mapped_CSVs_original_official_scored': True,
        'all_cold80_260_975_and_all1212_nonflagged_orders_and_ties_required': True,
        'selection_rule': 'Highest complete original official S; exact ties prefer lower weight then case',
        'new_native_fits_by_this_comparison': 0, 'test_labels_read': False})
    records = []
    with LockedReadHashCache(pins):
        head_paths = {name: BANK / name / 'flagged_oof_predictions.npy' for name in original_models}
        for name, components in ensembles.items():
            values = np.zeros(5635800, dtype=np.float64)
            for component in components:
                values += np.load(head_paths[component], mmap_mode='r')
            values /= len(components)
            path = OUT / f'{name}.npy'
            np.save(path, values)
            head_paths[name] = path
            create(OUT / f'{name}_verification.json', {
                'status': 'passed_exact_declared_component_order_equal_mean',
                'components': components, 'weight_per_component': 1. / len(components),
                'source_sha256': {str(head_paths[c]): sha(head_paths[c]) for c in components},
                'prediction_array_sha256': sha(path), 'new_native_fits': 0, 'test_labels_read': False})
            del values
        frame = pl.read_parquet(A / 'connected_validation_20261002/combined_fold_frame.parquet',
            columns=['ts_code', 'trade_date', 'flag_limit_up', 'y_ret_1d'])
        dates, flags = frame['trade_date'].to_numpy(), frame['flag_limit_up'].to_numpy()
        assert len(frame) == 5635800 and frame['trade_date'].n_unique() == 1212
        raw = np.load(parent / 'selected_validation.npy', mmap_mode='r')
        scoring = OUT / 'scoring_validation_only'
        scoring.mkdir()
        for filename in ('测试集_X.csv', '测试集_Y.csv'):
            os.link(A / 'optimization_20261003_r95/scoring_validation_only' / filename, scoring / filename)
        ctx = SimpleNamespace(frame=frame, dates=dates, scoring=scoring)
        days, starts = np.unique(dates, return_index=True)
        ends = np.r_[starts[1:], len(dates)]
        for index, case in enumerate(cases):
            residual = np.load(head_paths[case['model']], mmap_mode='r') if case['model'] else np.zeros(len(raw))
            assert np.all(residual[flags == 0] == 0.) and np.all(residual[dates < 20210101] == 0.)
            values = transform(raw, dates, flags, residual, case['weight'])
            assert np.array_equal(values[flags == 0].view(np.uint64), np.asarray(raw)[flags == 0].view(np.uint64))
            assert np.array_equal(values[dates < 20210101].view(np.uint64), np.asarray(raw)[dates < 20210101].view(np.uint64))
            for left, right in zip(starts, ends):
                eligible = flags[left:right] == 0
                assert np.array_equal(rankdata(raw[left:right][eligible]), rankdata(values[left:right][eligible]))
            for count in (80, 260, 975):
                n = int(ends[count - 1])
                cold = transform(raw[:n], dates[:n], flags[:n], residual[:n], case['weight'])
                assert np.array_equal(cold.view(np.uint64), values[:n].view(np.uint64))
            if index == 0:
                assert np.array_equal(values.view(np.uint64), np.asarray(raw).view(np.uint64))
            metrics = score(ctx, values)
            if index == 0:
                assert metrics == baseline
            for field in ('annual_excess', 'mean_turnover', 'top1_annual_ret'):
                assert metrics[field] == baseline[field], field
            assert abs((metrics['final_score'] - baseline['final_score']) - .4*(metrics['ic_mean'] - baseline['ic_mean'])) < 1e-15
            capsule = Path(ctx.last_official_score_cache['official_metrics_source'])
            item = {'case': index, 'configuration': case, 'metrics': metrics,
                'connected_final_score': metrics['final_score'],
                'score_gain_over_parent100': metrics['final_score'] - baseline['final_score'],
                'prediction_numeric_bytes_sha256': hashlib.sha256(memoryview(np.ascontiguousarray(values)).cast('B')).hexdigest(),
                'official_score_cache': ctx.last_official_score_cache, 'official_metric_capsule_sha256': sha(capsule),
                'actual_return_mapping': ctx.last_candidate_return_mapping,
                'first2020_and_nonflagged_raw_values_exact': True,
                'all1212_nonflagged_orders_and_ties_exact': True, 'actual_cold80_260_975_bits_exact': True,
                'native_bank_source': str(BANK / 'verification.json'),
                'ensemble_components': ensembles.get(case['model']), 'test_labels_read': False,
                'full_frozen_candidate_and_complete_ranking_still_required': True}
            create(OUT / f'case{index:02d}_official.json', item)
            records.append(item)
            print(__import__('json').dumps({'case': index, 'configuration': case,
                'official_score': metrics['final_score'], 'gain_over_parent100': item['score_gain_over_parent100']}, ensure_ascii=False), flush=True)
            del values, residual
            gc.collect()
    best = min(records, key=lambda r: (-r['connected_final_score'], r['configuration']['weight'], r['case']))
    create(OUT / 'verification.json', {
        'status': 'passed_actual49_conditional_residual_native_and_ensemble_full_official_comparisons',
        'input_sha256': pins, 'records': records, 'best': best, 'existing_native_bank_fits': 20,
        'new_native_fits_by_comparison': 0, 'new_quality_score_records': 49,
        'ensembles': ensembles, 'test_labels_read': False,
        'full_frozen_candidate_inference_and_complete_ranking_and_main_publication_pending': True,
        'global_feasible_direction_or_resource_boundary_not_established': True})


if __name__ == '__main__':
    try:
        main()
    except BaseException as error:
        if OUT.exists() and not (OUT / 'failure.json').exists():
            create(OUT / 'failure.json', {'status': 'failed_preserved_conditional_residual_official_comparison',
                'error': f'{type(error).__name__}: {error}', 'test_labels_read': False})
        raise
