"""Validate real Windows scoring workers on original full R95 configurations."""
from pathlib import Path
import json
import os
import sys
import time
import types

for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'POLARS_MAX_THREADS'):
    os.environ[name] = '8'
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
FULL = A / 'bounded_root_replay_full_controls_20261006'
OUT = A / 'root_and_rank_cache_actual_worker_controls_20261006'
from run_dependency_queue_v3_20261006 import read, create, sha

CONTROLS = (('cold_baseline', 0), ('warm_baseline', 0), ('changed_downstream_roles', 4))


def initialize_observed(module_name, output, slots):
    import numpy as np
    import evaluate
    import root_and_rank_cache_official_worker_adapter_20261006 as adapter
    adapter.initialize(module_name, output, slots)
    ctx = adapter.original._CONTEXT
    ctx._control_original_score = ctx.score

    def observed_score(self, prediction):
        index = self._control_reference_index
        reference = np.load(FULL / f'reference_prediction_{index}.npy', mmap_mode='r')
        assert prediction.dtype == reference.dtype == np.dtype('float64')
        assert np.array_equal(prediction.view(np.uint64), reference.view(np.uint64))
        metrics = self._control_original_score(prediction)
        source = read(FULL / 'verification.json')['all5_reference_configurations'][index]['reference_metric_capsule']
        capsule = read(Path(source))
        assert metrics == capsule['metrics']
        assert self.last_official_score_cache['cache_hit']
        assert sha(Path(self.scoring) / 'submission.csv') == capsule['scope']['submission_csv_sha256']
        return metrics

    ctx.score = types.MethodType(observed_score, ctx)

    def unexpected_evaluator(*args, **kwargs):
        raise AssertionError('Control requires exact original official metrics capsules.')

    evaluate.evaluate = unexpected_evaluator


def evaluate_observed(job):
    import root_and_rank_cache_official_worker_adapter_20261006 as adapter
    adapter.original._CONTEXT._control_reference_index = dict(CONTROLS)[job[0]]
    return adapter.evaluate(job)


def main():
    import psutil
    import root_and_rank_cache_official_worker_adapter_20261006 as adapter
    from hidden_windows_child_creation_20261006 import install as hide
    from locked_read_hash_cache_20261004 import LockedReadHashCache
    assert not OUT.exists()
    assert psutil.virtual_memory().available >= 14 * 2**30, 'Conservative full-context admission guard'
    proof = adapter.read_control()
    frozen = read(FULL / 'frozen_before_full_controls.json')
    sources = [Path(__file__), Path(adapter.__file__), adapter.PROOF,
        FULL / 'frozen_before_full_controls.json',
        A / 'exact_rank_cache_official_worker_adapter_20261006.py',
        A / 'parallel_candidate_scoring_one_20261005.py',
        A / 'hidden_windows_child_creation_20261006.py',
        *[FULL / f'reference_prediction_{i}.npy' for i in (0, 4)]]
    pins = {**proof['input_sha256'], **{str(p): sha(p) for p in sources}}
    OUT.mkdir()
    scratch = ROOT / 'tmp/root_and_rank_cache_worker_20261006'
    scratch.mkdir(exist_ok=True)
    for name in ('TMP', 'TEMP', 'TMPDIR'):
        os.environ[name] = str(scratch)
    create(OUT / 'frozen_before_actual_worker_controls.json', {
        'input_sha256': pins, 'controls': list(CONTROLS),
        'all5635800_raw_prediction_bits_and_final_CSV_bytes_required': True,
        'all8_original_official_metrics_required': True,
        'new_quality_records': 0, 'new_native_fits': 0, 'test_labels_read': False})
    restore_children = hide()
    restore_adapter = adapter.install()
    adapter.original._initialize = initialize_observed
    adapter.original._evaluate = evaluate_observed
    rows, measurements = [], []
    try:
        with LockedReadHashCache(pins):
            jobs = [(key, frozen['cases'][i]['configuration']) for key, i in CONTROLS]
            started = time.perf_counter()
            for key, row in adapter.original.evaluate_many('optimize_training_round95_v3', jobs, OUT):
                elapsed = time.perf_counter() - started
                started = time.perf_counter()
                stats = row['bounded_root_execution']
                assert stats['installed_in_actual_Windows_scoring_worker']
                assert stats['after']['retained_payload_bytes'] <= 128 * 1024**2
                if key != 'cold_baseline':
                    assert stats['after']['hits'] > stats['before']['hits']
                    assert stats['after']['misses'] == stats['before']['misses']
                create(OUT / f'{key}_actual_complete_row.json', row)
                measurements.append({'control': key, 'complete_candidate_seconds': elapsed,
                    'initialization_included': key == 'cold_baseline',
                    'root_execution': stats, 'rank_execution': row['exact_daily_rank_execution']})
                rows.append(row)
                print(json.dumps(measurements[-1], ensure_ascii=False), flush=True)
            assert len(rows) == 3
            assert len({r['parallel_execution']['worker_pid'] for r in rows}) == 1
            assert rows[0]['metrics'] == rows[1]['metrics']
            assert rows[0]['construction'] == rows[1]['construction']
        create(OUT / 'verification.json', {
            'status': 'passed_actual_Windows_worker_combined_caches_full_bits_CSV8_metrics_and_changed_downstream_graph',
            'input_sha256': pins, 'actual_measurements': measurements,
            'all5635800_raw_bits_and_complete_mapped_CSV_bytes_verified_each_call': True,
            'all8_original_official_metrics_exact_each_call': True,
            'unexpected_official_evaluator_calls': 0,
            'runtime_adopted': False, 'new_quality_records': 0,
            'new_native_fits': 0, 'test_labels_read': False})
    except BaseException as exc:
        create(OUT / 'failure.json', {'status': 'failed_preserved_actual_combined_cache_worker_control',
            'error': f'{type(exc).__name__}: {exc}'})
        raise
    finally:
        adapter.original.shutdown()
        adapter.original._initialize, adapter.original._evaluate = adapter.initialize, adapter.evaluate
        restore_adapter()
        create(OUT / 'actual_hidden_child_creations.json', {'events': restore_children()})


if __name__ == '__main__':
    main()
