"""Actual full parent graph and cold-prefix proof for bounded rank memoization."""
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
    import optimize_training_round88_v2 as module
    from exact_daily_rank_memoization_20261006 import install
    from whole_scheme_replay_runtime_20261004 import slice_context
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    out = A / 'parent_graph_rank_cache_preflight_v2_20261007'
    assert not out.exists()
    out.mkdir()
    while psutil.virtual_memory().available < 11 * 2**30:
        time.sleep(15)
    folder = A / 'optimization_20261003_r88'
    protocol = read(folder / 'protocol.json')
    paths = [Path(__file__), A / 'exact_daily_rank_memoization_20261006.py',
        A / 'whole_scheme_replay_runtime_20261004.py', A / 'role_layer_replay_20261004.py',
        A / 'optimize_wave15.py', folder / 'protocol.json', folder / 'selection.json',
        folder / 'selected_validation.npy', ROOT / '后续选模标准.md',
        A / 'verify_parent_graph_rank_cache_20261007.py',
        A / 'service_owned_workflows_20261006/parent_graph_rank_cache_preflight/service_execution.json']
    pins = {**protocol['input_sha256'], **{str(p): sha(p) for p in paths}}
    create(out / 'frozen_before_actual_parent_controls.json', {'input_sha256': pins,
        'actual_complete_parent_round': 88, 'maximum_cache_bytes': 2**30,
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
        cache, restore = install(maximum_bytes=2**30)
        try:
            replay(ctx, 'cache_cold_full5635800', expected)
            before = cache.statistics()
            replay(ctx, 'cache_warm_full5635800', expected)
            after = cache.statistics()
            assert after['hits'] > before['hits']
            dates = np.unique(ctx.dates)
            cold_controls = []
            for days in (80, 260, 975):
                n = int(np.searchsorted(ctx.dates, dates[days-1], side='right'))
                # No retained full-array rank output survives into the cold prefix.
                cache.entries.clear()
                cache.bytes = 0
                prefix = slice_context(ctx, n, cold=True)
                replay(prefix, f'empty_rank_and_root_cache_cold{days}', expected[:n])
                cold_controls.append({'days': days, 'rows': n, 'rank_cache_empty_before_prefix': True,
                    'root_and_layer_caches_cold': True, 'full_prefix_raw_bits_exact': True,
                    'actual_cache_statistics': cache.statistics()})
                del prefix
                gc.collect()
            scope.reverify()
            create(out / 'verification.json', {'status': 'passed_actual_R88_parent5635800_and_empty_cache_cold80_260_975_bits',
                'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins,
                'timings': timings, 'cold_prefixes': cold_controls, 'warm_before': before,
                'warm_after': after, 'final_cache_statistics': cache.statistics(),
                'all_rank_inputs_content_mask_dates_dtype_and_shape_hashed': True,
                'maximum_retained_rank_bytes': 2**30, 'official_evaluator_or_math_changed': False,
                'new_model_fits': 0, 'new_official_selection_scores': 0,
                'whole_goal_speedup_not_measured': True, 'test_labels_read': False})
        finally:
            if restore is not None:
                statistics = restore()
                create(out / 'actual_bindings_restoration.json', {'status': 'passed_original_rank_bindings_restored',
                    'statistics': statistics, 'new_quality_scores': 0})


if __name__ == '__main__':
    main()
