"""Reserve the already empty scheduler across two naturally serial controls."""
from pathlib import Path
import os
import sys
import time

import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
from run_dependency_queue_v3_20261006 import read, create, sha, owned
from atomic_optimization_observer_writes_20261005 import write
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
from windows_hidden_process_launch_20261006 import launch

OUT = A / 'root_and_rank_cache_serial_window_20261006'
CONTROL = A / 'root_and_rank_cache_actual_worker_controls_20261006'
FIRST = A / 'bounded_root_full_controls_waiter_v2_20261006'


def main():
    assert not OUT.exists() and not CONTROL.exists()
    assert not (A / 'service_owned_dependency_queue_v4_20261006/activated_jobs/round97/launch.json').exists()
    first_identity = read(A / 'service_owned_workflows_20261006/bounded_root_full_controls_waiter_v2/native_launch.json')
    first = read(FIRST / 'state.json')
    assert first['status'] == 'running_actual_full_root_cache_controls_with_idle_queue_reserved'
    assert owned(first_identity) and first['pid'] == first_identity['owned_worker_pid']
    queue = first['queue_identity']
    assert owned(queue)
    initial = read(FIRST / 'actual_full_control_launch.json')
    child_identity = psutil.Process(initial['pid'])
    assert child_identity.create_time() == initial['creation_time']
    assert child_identity.cmdline() == initial['command']
    neural = read(A / 'service_owned_workflows_20261006/neural16384_annual/native_launch.json')
    assert owned(neural)
    OUT.mkdir()
    pins = {str(p): sha(p) for p in (Path(__file__),
        A / 'root_and_rank_cache_official_worker_adapter_20261006.py',
        A / 'verify_root_and_rank_cache_worker_20261006.py',
        A / 'bounded_root_replay_memoization_20261006.py',
        A / 'verify_bounded_root_replay_full_controls_20261006.py')}
    create(OUT / 'frozen_before_actual_scheduler_reservation.json', {
        'input_sha256': pins, 'queue_identity': queue,
        'first_actual_waiter_identity': first_identity, 'first_actual_control_identity': initial,
        'preserved_neural_identity': neural, 'scientific_workers_held': 0,
        'full_grid_and_candidate_QA_routes_unchanged': True,
        'purpose': 'Keep the empty helper reserved until original full controls and then actual spawn controls naturally finish.'})
    held = []
    child = None
    try:
        parent, worker, idle = suspended_idle(queue,
            '    main (run_dependency_queue_v3_20261006.py:141)')
        held.extend((worker, parent))
        assert not worker.children(recursive=True)
        create(OUT / 'actual_empty_helper_before_and_after_additional_reservation.json', {
            'idle': idle, 'only_empty_queue_helper_pair_held': True,
            'existing_first_control_reservation_record': str(FIRST / 'actual_idle_queue_reservation.json'),
            'existing_control_and_GPU_worker_not_held': True})
        while owned(first_identity):
            assert owned(queue) and owned(neural) and not worker.children(recursive=True)
            write(OUT / 'state.json', {'status': 'waiting_for_original_full_control_and_its_publication_natural_completion',
                'pid': os.getpid(), 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
                'original_control_waiter_owned_live': True, 'scientific_workers_held': 0})
            time.sleep(1)
        assert read(A / 'service_owned_workflows_20261006/bounded_root_full_controls_waiter_v2/service_execution.json')['status'] == 'passed'
        result = read(A / 'bounded_root_replay_full_controls_20261006/verification.json')
        assert result['status'] == 'passed_actual_full_root_cache_bits8_metrics_cold_prefix_poisoning_and_root_mutation_controls'
        if not result['warm_prediction_median_improved']:
            create(OUT / 'execution.json', {'status': 'closed_without_adoption_no_matched_warm_speed_improvement',
                'actual_full_result': str(A / 'bounded_root_replay_full_controls_20261006/verification.json'),
                'no_worker_control_started': True, 'runtime_adopted': False})
            return
        while psutil.virtual_memory().available < 14 * 2**30:
            assert owned(queue) and owned(neural) and not worker.children(recursive=True)
            write(OUT / 'state.json', {'status': 'waiting_for_14GiB_actual_worker_control_admission',
                'pid': os.getpid(), 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
                'available_host_bytes': psutil.virtual_memory().available,
                'guard_is_scheduling_policy_not_physical_boundary': True, 'scientific_workers_held': 0})
            time.sleep(1)
        for path, digest in pins.items():
            assert sha(path) == digest, path
        with (OUT / 'stdout.log').open('xb') as stdout, (OUT / 'stderr.log').open('xb') as stderr:
            child = launch([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8',
                str(A / 'verify_root_and_rank_cache_worker_20261006.py')], cwd=ROOT,
                env=dict(os.environ), stdout=stdout, stderr=stderr)
            process = psutil.Process(child.pid)
            create(OUT / 'actual_worker_control_launch.json', {'pid': child.pid,
                'creation_time': process.create_time(), 'command': process.cmdline(), 'CREATE_NO_WINDOW': True})
            while child.poll() is None:
                assert owned(queue) and owned(neural)
                write(OUT / 'state.json', {'status': 'running_actual_full_Windows_scoring_worker_controls',
                    'pid': os.getpid(), 'control_root_pid': child.pid,
                    'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
                    'scientific_workers_held': 0, 'runtime_adopted': False})
                time.sleep(1)
        create(OUT / 'execution.json', {'status': 'passed' if child.returncode == 0 else 'failed_preserved',
            'returncode': child.returncode, 'runtime_adopted': False,
            'actual_control_folder': str(CONTROL), 'scientific_workers_stopped_or_restarted': 0,
            'new_quality_records': 0, 'new_native_fits': 0, 'test_labels_read': False})
    except BaseException as exc:
        create(OUT / 'failure.json', {'status': 'failed_preserved_serial_worker_window_control',
            'error': f'{type(exc).__name__}: {exc}', 'runtime_adopted': False})
        raise
    finally:
        if child is not None and child.poll() is None:
            child.wait()
        for process in reversed(held):
            if process.is_running():
                process.resume()
        create(OUT / 'actual_empty_scheduler_release.json', {
            'own_empty_helper_reservation_released': True, 'queue_owned': owned(queue),
            'scientific_workers_stopped_or_restarted': 0, 'runtime_adopted': False})


if __name__ == '__main__':
    main()
