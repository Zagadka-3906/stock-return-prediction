"""Full training-only causal controls before official cohort comparison."""
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
    os.environ[key] = '4'
from run_dependency_queue_v3_20261006 import read, create, sha
from atomic_optimization_observer_writes_20261005 import write

OUT = A / 'cohort_rank_calibration_full_controls_20261006'


def numeric_sha(values):
    import numpy as np
    return hashlib.sha256(memoryview(np.ascontiguousarray(values)).cast('B')).hexdigest()


def main():
    import psutil
    assert psutil.virtual_memory().available >= 8 * 2**30
    assert psutil.disk_usage('D:/').free >= 2 * 2**30
    assert not OUT.exists()
    OUT.mkdir()
    scratch = ROOT / 'tmp/cohort_rank_calibration_controls_20261006'
    scratch.mkdir(exist_ok=True)
    for key in ('TMP', 'TEMP', 'TMPDIR'):
        os.environ[key] = str(scratch)
    import numpy as np
    import pandas as pd
    import polars as pl
    from scipy.stats import rankdata
    import cohort_rank_calibration_20261006 as method
    from run import fold_cutoff
    from locked_read_hash_cache_20261004 import LockedReadHashCache
    parent = A / 'optimization_20261003_r95'
    panel = A / 'connected_validation_20261002/combined_fold_frame.parquet'
    label_alias = parent / 'scoring_validation_only/测试集_Y.csv'
    sources = [Path(__file__), Path(method.__file__), ROOT / 'run.py', ROOT / '后续选模标准.md',
        ROOT / 'evaluate.py', panel, label_alias,
        parent / 'selected_validation.npy', parent / 'protocol.json',
        parent / 'selection.json', parent / 'calibrated_csv_official.json',
        A / 'round65_limit_up_gain_audit_v3_20261005/verification.json']
    pins = {str(p): sha(p) for p in sources}
    cases = [{'weight': 0., 'bins': None, 'pseudocount': None}]
    cases += [{'weight': weight, 'bins': bins, 'pseudocount': pseudo}
        for bins in (32, 128) for pseudo in (0., 200.) for weight in (.1, .25, .5, 1.)]
    create(OUT / 'frozen_before_actual_full_controls.json', {
        'input_sha256': pins, 'cases': cases, 'expected_rows_days_stocks': [5635800, 1212, 4650],
        'history_rule': 'All previous mature training OOF dates strictly before original fold_cutoff(year)',
        'first_validation_year_2020_unchanged_no_prior_complete_scheme_OOF': True,
        'all17_cases_nonflagged_order_and_ties_must_be_preserved_every_day': True,
        'official_final_mapped_output_scoring_and_candidate_qualification_pending': True,
        'test_labels_read': False, 'new_native_base_model_fits': 0})
    actual = []
    with LockedReadHashCache(pins):
        frame = pl.read_parquet(panel, columns=['ts_code', 'trade_date', 'flag_limit_up'])
        dates, flags = frame['trade_date'].to_numpy(), frame['flag_limit_up'].to_numpy()
        assert len(frame) == 5635800 and len(np.unique(dates)) == 1212
        assert len(frame['ts_code'].unique()) == 4650
        assert int(dates.min()) >= 20200101 and int(dates.max()) <= 20241231
        label_frame = pd.read_csv(label_alias).sort_values(['trade_date', 'ts_code']).reset_index(drop=True)
        assert np.array_equal(label_frame['trade_date'].to_numpy(), dates)
        assert np.array_equal(label_frame['ts_code'].to_numpy(), frame['ts_code'].to_numpy())
        labels = label_frame['y_ret_1d'].to_numpy(dtype=np.float64)
        assert not np.isinf(labels).any()
        del label_frame
        gc.collect()
        raw = np.load(parent / 'selected_validation.npy', mmap_mode='r')
        percentile = method.daily_percentile(raw, dates)
        targets = method.historical_label_percentile(labels, dates)
        models = {}
        poisoned_targets = targets.copy()
        poisoned_targets[dates >= 20240101] = np.nan
        for bins in (32, 128):
            for pseudo in (0., 200.):
                key = f'b{bins}_s{int(pseudo)}'
                annual = {'2020': None}
                for year in (2021, 2022, 2023, 2024):
                    cutoff = fold_cutoff(year)
                    curve = method.fit(percentile, targets, flags, dates, cutoff, bins, pseudo)
                    assert curve == method.fit(percentile, poisoned_targets, flags, dates, cutoff, bins, pseudo)
                    annual[str(year)] = curve
                models[key] = annual
                create(OUT / f'annual_models_{key}.json', {'annual_models': annual,
                    'actual_nonfallback_calibration_fits': 4,
                    'last_validation_year_label_poisoning_leaves_all_prior_fits_exact': True})
        np.save(OUT / 'parent_percentile.npy', percentile)
        np.save(OUT / 'historical_label_percentile.npy', targets)
        days, starts = np.unique(dates, return_index=True)
        ends = np.r_[starts[1:], len(dates)]
        for i, case in enumerate(cases):
            write(OUT / 'state.json', {'status': 'running_full_cohort_causal_and_eligible_order_controls',
                'pid': os.getpid(), 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
                'completed_cases': len(actual), 'expected_cases': 17, 'test_labels_read': False})
            key = None if i == 0 else f"b{case['bins']}_s{int(case['pseudocount'])}"
            annual = {} if i == 0 else models[key]
            output = method.transform(raw, dates, flags, annual, case['weight'], percentile=percentile)
            for left, right in zip(starts, ends):
                eligible = flags[left:right] == 0
                assert np.array_equal(rankdata(raw[left:right][eligible]), rankdata(output[left:right][eligible]))
            assert np.array_equal(output[dates < 20210101], raw[dates < 20210101])
            for count in (80, 260, 975):
                n = int(ends[count - 1])
                cold = method.transform(raw[:n], dates[:n], flags[:n], annual, case['weight'])
                assert np.array_equal(cold.view(np.uint64), output[:n].view(np.uint64))
            if i == 0:
                assert np.array_equal(output.view(np.uint64), np.asarray(raw).view(np.uint64))
            actual.append({**case, 'annual_model_key': key,
                'full_prediction_numeric_bytes_sha256': numeric_sha(output),
                'changed_values': int(np.count_nonzero(output != raw)),
                'all1212_nonflagged_orders_and_ties_exact': True,
                'actual_cold80_260_975_prefixes_bit_identical': True,
                'first_validation_year_bit_identical': True})
            del output
            gc.collect()
        diagnostics = []
        for year in (2020, 2021, 2022, 2023, 2024):
            for flag in (0, 1):
                mask = (dates // 10000 == year) & (flags == flag) & np.isfinite(targets)
                diagnostics.append({'year': year, 'flag_limit_up': flag, 'rows': int(mask.sum()),
                    'mean_prediction_percentile': float(percentile[mask].mean()),
                    'mean_historical_label_percentile': float(targets[mask].mean())})
        outputs = [OUT / 'parent_percentile.npy', OUT / 'historical_label_percentile.npy',
            *OUT.glob('annual_models_*.json')]
        create(OUT / 'verification.json', {'status': 'passed_full17_cohort_causal_prefix_and_nonflagged_order_controls',
            'input_sha256': pins, 'output_sha256': {str(p): sha(p) for p in outputs},
            'actual_cases': actual, 'actual_rows': len(raw), 'actual_days': len(days),
            'actual_stock_count': 4650, 'cohort_diagnostics_are_training_only_not_official_scores': diagnostics,
            'actual_annual_cohort_curve_fits': 16, 'new_native_base_model_fits': 0,
            'annual_maturity_cutoffs_original': True,
            'current_2024_labels_poisoning_leaves_all_annual_models_exact': True,
            'future_labels_not_used': True, 'official_scores_and_frozen_candidate_and_full_ranking_pending': True,
            'new_quality_score_records': 0, 'test_labels_read': False})
    print('passed_full17_cohort_causal_prefix_and_nonflagged_order_controls', flush=True)


if __name__ == '__main__':
    try:
        main()
    except BaseException as exc:
        if OUT.exists() and not (OUT / 'failure.json').exists():
            create(OUT / 'failure.json', {'status': 'failed_preserved_actual_cohort_full_controls',
                'error': f'{type(exc).__name__}: {exc}', 'test_labels_read': False})
        raise
