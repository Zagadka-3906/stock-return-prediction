"""Exercise the real one-worker initializer through Windows multiprocessing spawn."""
from pathlib import Path
from datetime import datetime
import json
import os
import sys
import time

for variable in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'POLARS_MAX_THREADS'):
    os.environ[variable] = '8'
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A), str(A / 'connected_validation_20261002')]
OUT = A / 'exact_rank_cache_windows_scoring_initializer_20261006'
from handoff_distribution_views_progress_monitor_20261006 import read, sha, create
from locked_read_hash_cache_20261004 import LockedReadHashCache


def replay(mode):
    import numpy as np
    import psutil
    import parallel_candidate_scoring_one_20261005 as pool
    import exact_rank_cache_official_worker_adapter_20261006 as adapter
    from verify_exact_rank_cache_complete_scheme_20261006 import clear_case_caches
    selected = read(A / 'optimization_20261003_r65/selection.json')
    ctx = pool._CONTEXT
    assert pool._SLOT == 0 and adapter._CACHE is not None
    ctx.configure(selected['winner'])
    cleared = clear_case_caches(ctx)
    before = adapter._CACHE.statistics()
    started = time.perf_counter()
    prediction, construction = ctx.predict(ctx.donor(ctx.finished('baseline')), 0., 0.)
    seconds = time.perf_counter() - started
    expected = np.load(A / 'optimization_20261003_r65/selected_validation.npy', mmap_mode='r')
    assert prediction.dtype == expected.dtype == np.dtype('float64')
    assert np.array_equal(prediction.view(np.uint64), expected.view(np.uint64))
    if mode == 'warm':
        assert adapter._CACHE.hits - before['hits'] == 23
        assert adapter._CACHE.misses == before['misses']
    return {'mode': mode, 'prediction_seconds': seconds, 'worker_pid': os.getpid(),
        'worker_creation_time': psutil.Process().create_time(), 'worker_slot': pool._SLOT,
        'actual_private_training_only_scoring_directory': str(ctx.scoring),
        'all5635800_float64_bits_identical': True, 'cache_before': before,
        'cache_after': adapter._CACHE.statistics(), 'cleared_case_caches': cleared,
        'complete_construction': construction}


def main():
    import multiprocessing
    from concurrent.futures import ProcessPoolExecutor
    import psutil
    import exact_rank_cache_official_worker_adapter_20261006 as adapter
    from hidden_windows_child_creation_20261006 import install as hide_children
    assert not OUT.exists()
    assert psutil.virtual_memory().available >= 6 * 1024**3
    prior = A / 'exact_rank_cache_complete_scheme_v2_20261006/verification.json'
    proof = read(prior)
    assert proof['status'] == 'passed_actual_full_scheme_original_cold_warm_and_official_CSV_bytes'
    bindings = dict(proof['input_sha256'])
    for path in (Path(__file__).resolve(), Path(adapter.__file__).resolve(), prior,
                 A / 'parallel_candidate_scoring_one_20261005.py', A / 'hidden_windows_child_creation_20261006.py'):
        bindings[str(path)] = sha(path)
    OUT.mkdir()
    create(OUT / 'frozen_before_actual_spawn.json', {'at_local': datetime.now().isoformat(timespec='seconds'),
        'input_sha256': bindings, 'full_original_scoring_initializer_required': True,
        'new_quality_scores': 0, 'test_labels_read': False})
    restore_children = hide_children()
    restore_adapter = adapter.install()
    try:
        with LockedReadHashCache(bindings):
            spawn = multiprocessing.get_context('spawn')
            slots = spawn.Queue()
            slots.put(0)
            with ProcessPoolExecutor(max_workers=1, mp_context=spawn,
                    initializer=adapter.original._initialize,
                    initargs=('optimize_training_round65', str(OUT), slots)) as executor:
                measurements = []
                for mode in ('cold', 'warm'):
                    row = executor.submit(replay, mode).result()
                    measurements.append(row)
                    create(OUT / (mode + '.json'), row)
                    print(json.dumps({k: v for k, v in row.items() if k != 'complete_construction'}, ensure_ascii=False), flush=True)
                assert measurements[0]['worker_pid'] == measurements[1]['worker_pid']
                assert measurements[0]['complete_construction'] == measurements[1]['complete_construction']
            slots.close()
            slots.join_thread()
        events = restore_children()
        restore_children = None
        create(OUT / 'verification.json', {
            'status': 'passed_actual_Windows_spawn_original_scoring_initializer_full_scheme_bits',
            'at_local': datetime.now().isoformat(timespec='seconds'), 'input_sha256': bindings,
            'actual_measurements': measurements, 'actual_hidden_child_creations': events,
            'all5635800_rows_recomputed_twice_in_same_original_initialized_worker': True,
            'actual_one_worker_private_scoring_provenance_preserved': True,
            'quality_scores_and_evaluator_calls_this_control': 0, 'new_model_fits': 0,
            'test_labels_read': False, 'production_workflow_adoption_still_pending': True})
    except BaseException as error:
        create(OUT / 'failure.json', {'status': 'failed_preserved_actual_spawn_control', 'error': f'{type(error).__name__}: {error}'})
        raise
    finally:
        restore_adapter()
        if restore_children:
            create(OUT / 'actual_hidden_child_creations_failure.json', {'events': restore_children()})


if __name__ == '__main__':
    main()
