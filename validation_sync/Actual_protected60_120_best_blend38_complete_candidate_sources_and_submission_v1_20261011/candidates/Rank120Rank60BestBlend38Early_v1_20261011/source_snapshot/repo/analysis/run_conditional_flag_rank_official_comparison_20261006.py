"""Compare 37 complete specialist outputs using only continuous training OOF."""
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
OUT = A / 'conditional_flag_rank_official_comparison_20261006'
BANK = A / 'conditional_flag_rank_bank_20261006'


def main():
    import psutil
    assert not OUT.exists()
    OUT.mkdir()
    service = A / 'service_owned_workflows_20261006/conditional_flag_rank_native_bank'
    while owned(read(service / 'native_launch.json')):
        time.sleep(30)
    assert read(service / 'service_execution.json')['status'] == 'passed'
    bank = read(BANK / 'verification.json')
    assert bank['status'] == 'passed_actual18_mature_flag_specialists_native_and_independent_codec_controls'
    while psutil.virtual_memory().available < 9 * 2**30:
        time.sleep(30)
    import numpy as np
    import polars as pl
    from scipy.stats import rankdata
    from run import fold_cutoff
    import cohort_rank_calibration_20261006 as curve
    from conditional_flag_rank_transform_20261006 import transform
    from score_calibrated_candidates_20261003 import score
    from locked_read_hash_cache_20261004 import LockedReadHashCache
    parent = A / 'optimization_20261003_r99'
    sources = [Path(__file__), A / 'conditional_flag_rank_transform_20261006.py',
        A / 'cohort_rank_calibration_20261006.py', BANK / 'verification.json',
        BANK / 'actual_target_and_feature_alignment.json', *BANK.glob('*/flagged_oof_predictions.npy'),
        *BANK.glob('*/info_*.json'), *BANK.glob('*/model_*.txt'), *BANK.glob('*/model_dump_*.json'),
        parent / 'selected_validation.npy', parent / 'selection.json', parent / 'calibrated_csv_official.json',
        A / 'connected_validation_20261002/combined_fold_frame.parquet',
        A / 'cohort_rank_calibration_full_controls_20261006/historical_label_percentile.npy',
        A / 'score_calibrated_candidates_20261003.py', ROOT / 'evaluate.py', ROOT / '后续选模标准.md',
        A / 'optimization_20261003_r95/scoring_validation_only/测试集_X.csv',
        A / 'optimization_20261003_r95/scoring_validation_only/测试集_Y.csv']
    pins = {**bank['input_sha256'], **{str(p): sha(p) for p in sources}}
    cases = [{'model': None, 'weight': 0., 'first_year_slope': None}]
    cases += [{'model': name, 'weight': weight, 'first_year_slope': slope}
        for name in bank['configurations'] for slope in (.08, .125, .2) for weight in (.1, .25, .5, 1.)]
    assert len(cases) == 37
    baseline = read(parent / 'calibrated_csv_official.json')['metrics']
    create(OUT / 'frozen_before_actual_controls_and_official_scores.json', {
        'input_sha256': pins, 'cases': cases, 'explicit_parent_round': 99,
        'baseline_official_metrics': baseline, 'rows_days_stocks': [5635800, 1212, 4650],
        'eligible_order_preserved_and_all_cold80_260_975_prefixes_required': True,
        'first2020_native_predictor_uses_only_mature_pre2020_training_labels': True,
        'first2020_common_curve_is_declared_positive_affine_prior': True,
        'later_common_curves_use_only_mature_earlier_OOF_label_ranks': True,
        'all37_final_past_return_mapped_CSVs_original_official_scored': True,
        'selection_rule': 'Highest original official complete output S; exact ties prefer lower specialist weight',
        'no_new_native_fits_by_this_comparator': True, 'test_labels_read': False})
    records = []
    with LockedReadHashCache(pins):
        frame = pl.read_parquet(A / 'connected_validation_20261002/combined_fold_frame.parquet',
            columns=['ts_code', 'trade_date', 'flag_limit_up', 'y_ret_1d'])
        dates, flags = frame['trade_date'].to_numpy(), frame['flag_limit_up'].to_numpy()
        assert len(frame) == 5635800 and len(np.unique(dates)) == 1212
        raw = np.load(parent / 'selected_validation.npy', mmap_mode='r')
        p = curve.daily_percentile(raw, dates)
        target = np.load(A / 'cohort_rank_calibration_full_controls_20261006/historical_label_percentile.npy', mmap_mode='r')
        annual = {'2020': None}
        for year in (2021, 2022, 2023, 2024):
            cutoff = fold_cutoff(year)
            fit = curve.fit(p, target, flags, dates, cutoff, 32, 0.)
            poisoned = np.asarray(target).copy()
            poisoned[dates >= 20240101] = np.nan
            assert fit == curve.fit(p, poisoned, flags, dates, cutoff, 32, 0.)
            annual[str(year)] = fit
            del poisoned
        create(OUT / 'annual_common_rank_curves.json', {
            'annual_models': annual, 'actual_annual_pair_fits': 4,
            'global_curves_used_flagged_curve_not_used': True,
            'current2024_label_poisoning_leaves_all_mature_annual_fits_exact': True})
        np.save(OUT / 'parent_percentile.npy', p)
        scoring = OUT / 'scoring_validation_only'
        scoring.mkdir()
        for filename in ('测试集_X.csv', '测试集_Y.csv'):
            os.link(A / 'optimization_20261003_r95/scoring_validation_only' / filename, scoring / filename)
        ctx = SimpleNamespace(frame=frame, dates=dates, scoring=scoring)
        days, starts = np.unique(dates, return_index=True)
        ends = np.r_[starts[1:], len(dates)]
        for index, case in enumerate(cases):
            predictor = np.load(BANK / case['model'] / 'flagged_oof_predictions.npy', mmap_mode='r') if case['model'] else np.zeros(len(raw))
            values = transform(raw, dates, flags, predictor, annual, case['weight'], case['first_year_slope'], percentile=p)
            for left, right in zip(starts, ends):
                eligible = flags[left:right] == 0
                assert np.array_equal(rankdata(raw[left:right][eligible]), rankdata(values[left:right][eligible]))
            for count in (80, 260, 975):
                n = int(ends[count - 1])
                cold = transform(raw[:n], dates[:n], flags[:n], predictor[:n], annual, case['weight'], case['first_year_slope'])
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
                'score_gain_over_parent99': metrics['final_score'] - baseline['final_score'],
                'prediction_numeric_bytes_sha256': hashlib.sha256(memoryview(np.ascontiguousarray(values)).cast('B')).hexdigest(),
                'official_score_cache': ctx.last_official_score_cache, 'official_metric_capsule_sha256': sha(capsule),
                'actual_return_mapping': ctx.last_candidate_return_mapping,
                'all1212_nonflagged_orders_and_ties_exact': True, 'actual_cold80_260_975_bits_exact': True,
                'native_bank_source': str(BANK / 'verification.json'), 'test_labels_read': False,
                'full_frozen_candidate_and_complete_ranking_still_required': True}
            create(OUT / f'case{index:02d}_official.json', item)
            records.append(item)
            print(__import__('json').dumps({'case': index, 'configuration': case, 'official_score': metrics['final_score'],
                'gain_over_parent99': item['score_gain_over_parent99']}, ensure_ascii=False), flush=True)
            del values, predictor
            gc.collect()
    best = min(records, key=lambda r: (-r['connected_final_score'], r['configuration']['weight'], r['case']))
    create(OUT / 'verification.json', {
        'status': 'passed_actual37_conditional_flag_full_controls_and_original_official_scores',
        'input_sha256': pins, 'records': records, 'best': best, 'existing_native_bank_fits': 18,
        'actual_common_curve_pair_fits': 4, 'new_native_fits_by_comparison': 0,
        'new_quality_score_records': 37, 'test_labels_read': False,
        'full_frozen_candidate_inference_and_complete_ranking_and_main_publication_pending': True,
        'global_feasible_direction_or_resource_boundary_not_established': True})


if __name__ == '__main__':
    try:
        main()
    except BaseException as exc:
        if OUT.exists() and not (OUT / 'failure.json').exists():
            create(OUT / 'failure.json', {'status': 'failed_preserved_conditional_flag_official_comparison',
                'error': f'{type(exc).__name__}: {exc}', 'test_labels_read': False})
        raise
