"""Actual full parent graph and cold-prefix controls for the NumPy daily-rank operator."""
from pathlib import Path
import gc
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A), str(A / 'connected_validation_20261002')]
from run_dependency_queue_v3_20261006 import read, sha, create
from atomic_optimization_observer_writes_20261005 import write


def main():
    import numpy as np
    import psutil
    from exact_numpy_daily_ranks_20261007 import install
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    out = A / 'numpy_daily_ranks_full_parent_graph_preflight_20261007'
    assert not out.exists()
    out.mkdir()
    from run_dependency_queue_v3_20261006 import owned
    prerequisite = A / 'service_owned_workflows_20261006/CPU_ELASTIC44_round114_full_registration'
    while owned(read(prerequisite / 'native_launch.json')):
        time.sleep(15)
    assert read(prerequisite / 'service_execution.json')['status'] == 'passed'
    assert read(A / 'github_validation_sync_main_20261005/round114_receipt.json')['actual_full_QA_version'] == 25
    while psutil.virtual_memory().available < 11 * 2**30:
        time.sleep(15)
    import optimize_training_round88_v2 as module
    from whole_scheme_replay_runtime_20261004 import slice_context
    proof=read(A / 'exact_numpy_daily_ranks_benchmark_20261007/verification.json')
    assert proof['status']=='passed_actual_three_full5635800_heads_two_opposite_orders_daily_rank_and_cold_prefix_controls'
    folder = A / 'optimization_20261003_r88'
    protocol = read(folder / 'protocol.json')
    paths = [Path(__file__), A / 'exact_numpy_daily_ranks_20261007.py',
        A / 'whole_scheme_replay_runtime_20261004.py', A / 'role_layer_replay_20261004.py',
        A / 'connected_validation_20261002/optimize_wave15.py', folder / 'protocol.json', folder / 'selection.json',
        folder / 'selected_validation.npy', ROOT / '后续选模标准.md',
        A / 'exact_numpy_daily_ranks_benchmark_20261007/verification.json',
        A / 'github_validation_sync_main_20261005/round114_receipt.json',
        prerequisite / 'service_execution.json']
    pins = {**protocol['input_sha256'], **{str(p): sha(p) for p in paths}}
    create(out / 'frozen_before_actual_parent_controls.json', {'input_sha256': pins,
        'actual_complete_parent_round': 88, 'rank_operator_retained_full_prediction_cache_bytes': 0,
        'new_model_fits': 0, 'new_official_selection_scores': 0, 'test_labels_read': False})
    restore = None
    with LockedReadHashCache(pins) as scope:
        winner = read(folder / 'selection.json')['winner']
        ctx = module.Context(fixture=winner)
        expected = np.load(folder / 'selected_validation.npy', mmap_mode='r')
        assert len(ctx.dates) == len(expected) == 5635800
        timings = []
        def replay(current, label, expected_values):
            write(out / 'actual_stage.json', {'status': 'actual_parent_graph_bit_controls',
                'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'control': label})
            started = time.perf_counter()
            pred, _ = current.predict(current.donor(current.finished('baseline')), 0., 0.)
            assert np.array_equal(pred.view(np.uint64), expected_values.view(np.uint64)), label
            timings.append({'control': label, 'rows': len(pred),
                'actual_seconds': time.perf_counter()-started, 'raw_float64_bits_exact': True})
            del pred
            gc.collect()
        replay(ctx, 'original_full5635800', expected)
        cache, restore = install()
        try:
            replay(ctx, 'numpy_first_full5635800', expected)
            before = cache.statistics()
            replay(ctx, 'numpy_repeated_full5635800', expected)
            after = cache.statistics()
            assert after['fast_calls'] > before['fast_calls']
            dates = np.unique(ctx.dates)
            cold_controls = []
            for days in (80, 260, 975):
                n = int(np.searchsorted(ctx.dates, dates[days-1], side='right'))
                # No retained full-array rank output survives into the cold prefix.
                prefix = slice_context(ctx, n, cold=True)
                replay(prefix, f'numpy_day_local_root_cache_cold{days}', expected[:n])
                cold_controls.append({'days': days, 'rows': n, 'rank_cache_empty_before_prefix': True,
                    'root_and_layer_caches_cold': True, 'full_prefix_raw_bits_exact': True,
                    'actual_cache_statistics': cache.statistics()})
                del prefix
                gc.collect()
            scope.reverify()
            create(out / 'verification.json', {'status': 'passed_actual_R88_parent5635800_numpy_daily_ranks_and_cold80_260_975_bits',
                'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins,
                'timings': timings, 'cold_prefixes': cold_controls, 'warm_before': before,
                'warm_after': after, 'final_cache_statistics': cache.statistics(),
                'day_local_usable_subset_and_tie_mean_controls_inherited': True,
                'maximum_retained_rank_prediction_cache_bytes': 0, 'official_evaluator_or_math_changed': False,
                'new_model_fits': 0, 'new_official_selection_scores': 0,
                'whole_goal_speedup_not_measured': True,
                'full1599600_future_graph_and_all8_official_metrics_not_verified_by_this_parent_control': True,
                'new_operator_not_adopted_in_frozen_scientific_workflows': True, 'test_labels_read': False})
        finally:
            if restore is not None:
                statistics = restore()
                create(out / 'actual_bindings_restoration.json', {'status': 'passed_original_rank_bindings_restored',
                    'statistics': statistics, 'new_quality_scores': 0})


if __name__ == '__main__':
    main()
