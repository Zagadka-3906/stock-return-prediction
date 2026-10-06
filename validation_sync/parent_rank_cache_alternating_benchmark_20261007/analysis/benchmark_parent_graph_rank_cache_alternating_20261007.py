"""Measure rank-cache phases after actual pending official writers complete."""
from pathlib import Path
import gc
import sys
import time
import statistics

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A), str(A / 'connected_validation_20261002')]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from atomic_optimization_observer_writes_20261005 import write


def main():
    import psutil
    out = A / 'parent_rank_cache_alternating_benchmark_20261007'
    assert not out.exists()
    out.mkdir()
    # This diagnostic cannot steal RAM from the scheduled official comparisons.
    while True:
        state = read(A / 'service_owned_dependency_queue_v4_20261006/state.json')
        row = state['activated_jobs'].get('round90')
        receipt = A / 'github_validation_sync_main_20261005/round90_receipt.json'
        scope90 = A / 'optimization_20261003_r90/provenance_scope_execution.json'
        close110 = A / 'optimization_20261003_r110/full_registration_execution.json'
        complete = (row is not None and not owned(row) and receipt.exists()
            and scope90.exists() and read(scope90).get('status') == 'passed'
            and close110.exists() and read(close110).get('status') == 'passed')
        busy = any(owned(r) for n, r in state['activated_jobs'].items() if n.startswith('round'))
        if complete and not busy and psutil.virtual_memory().available >= 11 * 2**30:
            import qualified_round_recovery_evidence_v4_20261007 as qualification
            try:
                evidence = qualification.complete_round_evidence(90)
            finally:
                qualification.close()
            if evidence is not None:
                break
        write(out / 'actual_stage.json', {'status': 'waiting_actual_full90_main_and_full110_and11GiB_RAM',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'actual_round90_activation_exists': row is not None,
            'actual_pending_writer_live': busy, 'available_RAM_GiB': psutil.virtual_memory().available / 2**30,
            'new_fits': 0, 'new_quality_scores': 0})
        time.sleep(15)
    import numpy as np
    import optimize_training_round88_v2 as module
    from exact_daily_rank_memoization_20261006 import install
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    folder = A / 'optimization_20261003_r88'
    proof = A / 'parent_graph_rank_cache_preflight_v3_20261007/verification.json'
    assert read(proof)['status'] == 'passed_actual_R88_parent5635800_and_empty_cache_cold80_260_975_bits'
    paths = [Path(__file__), proof, receipt, scope90, close110,
        A / 'exact_daily_rank_memoization_20261006.py', folder / 'protocol.json',
        folder / 'selection.json', folder / 'selected_validation.npy', ROOT / '后续选模标准.md']
    pins = {**read(folder / 'protocol.json')['input_sha256'], **{str(p): sha(p) for p in paths}}
    create(out / 'frozen_before_actual_benchmark.json', {'input_sha256': pins,
        'predeclared_repeats': 2, 'orders': ['original_then_cache', 'cache_then_original'],
        'Context_inherited_internal_layers_warmed_equally_before_timed_controls': True,
        'cold_rank_cache_prewarm_cost_measured_separately': True,
        'new_model_fits': 0, 'new_official_selection_scores': 0, 'test_labels_read': False})
    timings = []
    with LockedReadHashCache(pins) as scope:
        ctx = module.Context(fixture=read(folder / 'selection.json')['winner'])
        expected = np.load(folder / 'selected_validation.npy', mmap_mode='r')
        assert len(expected) == len(ctx.dates) == 5635800

        def replay(label, repeat):
            write(out / 'actual_stage.json', {'status': 'actual_alternating_parent_rank_cache_benchmark',
                'control': label, 'repeat': repeat, 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S')})
            start = time.perf_counter()
            pred, _ = ctx.predict(ctx.donor(ctx.finished('baseline')), 0., 0.)
            elapsed = time.perf_counter() - start
            assert np.array_equal(pred.view(np.uint64), expected.view(np.uint64)), label
            del pred
            gc.collect()
            return {'control': label, 'repeat': repeat, 'actual_seconds': elapsed,
                'rows': len(expected), 'raw_float64_bits_exact': True}

        create(out / 'unmeasured_context_warmup_control.json', replay('initial_context_warmup', -1))
        for repeat in range(2):
            if repeat == 0:
                timings.append(replay('original_internal_context_warm', repeat))
            cache, restore = install(maximum_bytes=2**30)
            try:
                timings.append(replay('cache_cold_rank_internal_context_warm', repeat))
                before = cache.statistics()
                timings.append(replay('cache_warm_rank_internal_context_warm', repeat))
                after = cache.statistics()
                assert after['hits'] > before['hits'] and after['misses'] == before['misses']
                create(out / f'repeat{repeat}_cache_statistics.json', {'before': before, 'after': after})
            finally:
                restored = restore()
                create(out / f'repeat{repeat}_original_bindings_restored.json', {'statistics': restored})
            if repeat == 1:
                timings.append(replay('original_internal_context_warm', repeat))
        assert len(timings) == 6
        medians = {label: statistics.median(r['actual_seconds'] for r in timings if r['control'] == label)
            for label in {r['control'] for r in timings}}
        scope.reverify()
        create(out / 'verification.json', {'status': 'passed_actual_two_alternating_repeats_full5635800_bits_and_original_restoration',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins,
            'timings': timings, 'median_seconds': medians,
            'median_warm_rank_phase_speedup': medians['original_internal_context_warm'] / medians['cache_warm_rank_internal_context_warm'],
            'median_cold_rank_phase_speedup': medians['original_internal_context_warm'] / medians['cache_cold_rank_internal_context_warm'],
            'single_host_original_GPU_and_scientific_workers_not_suspended_stopped_or_restarted': True,
            'whole_goal_or_whole_pipeline_speedup_not_measured': True,
            'inherited_actual_empty_cache80_260_975_prefix_control': str(proof),
            'new_model_fits': 0, 'new_official_selection_scores': 0, 'test_labels_read': False})


if __name__ == '__main__':
    main()
