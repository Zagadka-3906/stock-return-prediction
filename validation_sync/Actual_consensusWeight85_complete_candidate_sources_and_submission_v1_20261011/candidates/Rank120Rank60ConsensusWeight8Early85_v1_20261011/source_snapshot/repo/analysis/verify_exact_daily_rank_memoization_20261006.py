"""Check exact full five-year ranking outputs, mutation safety and bounded retention."""
from pathlib import Path
from datetime import datetime
import json
import sys
import time
import numpy as np
import polars as pl

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A), str(A / 'connected_validation_20261002')]
from exact_daily_rank_memoization_20261006 import DailyRankCache
from handoff_distribution_views_progress_monitor_20261006 import read, sha, create
from locked_read_hash_cache_20261004 import LockedReadHashCache
from optimize_wave15 import daily_ranks


def identical(left, right):
    assert left.dtype == right.dtype == np.dtype('float64') and left.shape == right.shape
    assert np.array_equal(left.view(np.uint64), right.view(np.uint64))


def main():
    out = A / 'exact_daily_rank_memoization_preflight_20261006'
    assert not out.exists()
    signals = ['rank_lgb_quantile_a050_r300', 'return_lgb_quantile_a010_r300',
               'return_lgb_quantile_a050_r300', 'return_lgb_quantile_a090_r300']
    # Use actual complete prediction files; no labels or future-X performance selection.
    bank = A / 'quantile_tree_memmap_complete_bank_20261006'
    selected = A / 'optimization_20261003_r65/selected_validation.npy'
    dates_csv = A / 'optimization_20261003_r65/scoring_validation_only/测试集_X.csv'
    paths = [Path(__file__).resolve(), A / 'exact_daily_rank_memoization_20261006.py',
        A / 'connected_validation_20261002/optimize_wave15.py', selected, dates_csv]
    paths += [bank / name / f'raw_{year}.parquet' for name in signals for year in range(2020, 2025)]
    assert all(path.exists() for path in paths)
    inputs = {str(path.resolve()): sha(path) for path in paths}
    out.mkdir()
    create(out / 'frozen_before_actual_full_inputs.json', {
        'at_local': datetime.now().isoformat(timespec='seconds'), 'input_sha256': inputs,
        'required_full_signals': ['selected_r65', *signals], 'expected_rows': 5635800,
        'new_quality_scores': 0, 'new_model_fits': 0, 'test_labels_read': False,
        'mathematical_rank_function_unchanged': True})
    checks = []
    with LockedReadHashCache(inputs):
        dates = pl.read_csv(dates_csv, columns=['trade_date'])['trade_date'].to_numpy()
        assert len(dates) == 5635800 and len(np.unique(dates)) == 1212
        valid = np.ones(len(dates), dtype=bool)
        cache = DailyRankCache(daily_ranks, maximum_bytes=256 * 1024**2)
        for name in ['selected_r65', *signals]:
            if name == 'selected_r65':
                values = np.load(selected, mmap_mode='r')
            else:
                frame = pl.concat([pl.read_parquet(bank / name / f'raw_{year}.parquet',
                    columns=['trade_date', 'pred_raw']) for year in range(2020, 2025)])
                assert np.array_equal(frame['trade_date'].to_numpy(), dates)
                values = frame['pred_raw'].to_numpy()
            started = time.perf_counter()
            reference = daily_ranks(values, valid, dates)
            original_seconds = time.perf_counter() - started
            started = time.perf_counter()
            cold = cache(values, valid, dates)
            cold_seconds = time.perf_counter() - started
            identical(reference, cold)
            started = time.perf_counter()
            warm = cache(values.copy(), valid.copy(), dates.copy())
            warm_seconds = time.perf_counter() - started
            identical(reference, warm)
            # Returned arrays must remain independent mutable arrays.
            warm[0] = 12345.0
            identical(reference, cache(values, valid, dates))
            checks.append({'signal': name, 'rows': len(values), 'days': 1212,
                'original_seconds': original_seconds, 'cold_seconds': cold_seconds,
                'warm_seconds_including_copied_inputs': warm_seconds,
                'all5635800_output_float64_bits_identical': True,
                'mutable_return_does_not_corrupt_cached_values': True})
            print(json.dumps(checks[-1], ensure_ascii=False), flush=True)
            del reference, cold, warm, values
            if name != 'selected_r65':
                del frame
        # Deliberately exercise changed values, masks, dates, dtype, layout, and object fallback.
        toy = np.array([-10., -9., -8.999, np.inf, -np.inf, np.nan, 0., -0., 1., 1., 2.])
        toy_dates = np.array([20200102, 20200103, 20200102, 20200103, 20200102,
            20200103, 20200102, 20200103, 20200102, 20200103, 20200102])
        toy_valid = np.ones(len(toy), dtype=bool)
        variants = [(toy, toy_valid, toy_dates), (toy[::-1], toy_valid[::-1], toy_dates[::-1]),
            (toy.astype(np.float32), toy_valid, toy_dates),
            (toy, toy_valid, toy_dates.astype(object)),
            (toy, toy_valid, (toy_dates-20200102).astype('datetime64[D]'))]
        changed_values, changed_valid, changed_dates = toy.copy(), toy_valid.copy(), toy_dates.copy()
        changed_values[-1], changed_valid[2], changed_dates[-1] = 3., False, 20200103
        variants += [(changed_values, toy_valid, toy_dates), (toy, changed_valid, toy_dates),
                     (toy, toy_valid, changed_dates)]
        small = DailyRankCache(daily_ranks, maximum_bytes=len(toy) * 8)
        for values, mask, grouping in variants:
            identical(daily_ranks(values, mask, grouping), small(values, mask, grouping))
            identical(daily_ranks(values, mask, grouping), small(values, mask, grouping))
            assert small.bytes <= small.maximum_bytes
        assert small.evictions > 0 and small.uncacheable > 0
        # Prefix and changed later dates/values remain governed by same-day ranking only.
        prefix = dates <= np.unique(dates)[79]
        values = np.load(selected, mmap_mode='r')
        full = cache(values, valid, dates)
        prefix_output = cache(values[prefix], valid[prefix], dates[prefix])
        identical(full[prefix], prefix_output)
        poisoned = np.array(values, copy=True)
        poisoned[~prefix] = -poisoned[~prefix] + .125
        identical(cache(poisoned, valid, dates)[prefix], prefix_output)
        proof = {'status': 'passed_full5635800_row_rank_bits_mutation_dtype_and_prefix_controls',
            'at_local': datetime.now().isoformat(timespec='seconds'), 'input_sha256': inputs,
            'actual_full_signal_checks': checks, 'actual_full_signal_count': len(checks),
            'actual_edge_case_checks': len(variants), 'whole80_day_prefix_and_modified_tail_bits_identical': True,
            'memory_cap_bytes': cache.maximum_bytes, 'actual_cache_statistics': cache.statistics(),
            'actual_edge_cache_statistics': small.statistics(),
            'complete_scheme_and_official_CSV_adoption_still_pending': True,
            'new_quality_scores': 0, 'new_model_fits': 0, 'test_labels_read': False}
        create(out / 'verification.json', proof)
    print('Passed actual full-input exact daily ranking cache controls.', flush=True)


if __name__ == '__main__':
    main()
