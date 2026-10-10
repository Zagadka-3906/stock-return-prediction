"""Adopt tested R97 worker execution while only the empty controller is held."""
from pathlib import Path
from copy import deepcopy
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
from run_dependency_queue_v3_20261006 import read, create, sha, owned
from atomic_optimization_observer_writes_20261005 import write
from handoff_ready_goss_full_execution_20261006 import start_service, pair
from handoff_joint_goss_round97_full_execution_v2_20261006 import suspended_idle, retire_suspended

OUT = A / 'root_cached_round97_runtime_handoff_20261006'
QUEUE = A / 'service_owned_dependency_queue_v4_20261006'


def service(name):
    return read(A / f'service_owned_workflows_20261006/{name}/native_launch.json')


def main():
    assert not OUT.exists()
    assert not (QUEUE / 'activated_jobs/round97/launch.json').exists()
    serial = service('root_and_rank_cache_serial_window')
    assert owned(serial)
    serial_state = read(A / 'root_and_rank_cache_serial_window_20261006/state.json')
    assert serial_state['status'] == 'running_actual_full_Windows_scoring_worker_controls'
    old = service('dependency_queue_v10')
    neural = service('neural16384_annual')
    assert owned(neural)
    prep_path = A / 'root_cached_round97_dispatch_preparation_20261006.json'
    preparation = read(prep_path)
    pins = {**preparation['original_sources'], **preparation['new_sources'],
        str(prep_path): sha(prep_path), str(Path(__file__)): sha(__file__)}
    for path, digest in pins.items():
        assert sha(path) == digest, path
    OUT.mkdir()
    create(OUT / 'frozen_before_wait_and_empty_helper_reservation.json', {
        'input_sha256': pins, 'old_queue_identity': old, 'actual_worker_control_identity': serial,
        'preserved_neural_identity': neural, 'scientific_workers_held': 0,
        'all_original_scientific_routes_grids_and_markers_preserved': True})
    held = []
    new_queue = new_monitor = None
    retired = False
    snapshot = None
    old_monitor = service('progress_monitor_v34')
    try:
        parent, worker, idle = suspended_idle(old,
            '    main (run_dependency_queue_v3_20261006.py:141)')
        held.extend((worker, parent))
        assert not worker.children(recursive=True)
        create(OUT / 'actual_empty_scheduler_reservation.json', {
            'idle': idle, 'only_empty_helper_pair_held': True,
            'existing_serial_control_reservation_not_released_by_this_helper': True,
            'scientific_workers_held': 0})
        while owned(serial):
            assert owned(old) and owned(neural) and not worker.children(recursive=True)
            write(OUT / 'state.json', {'status': 'waiting_for_actual_worker_controls_natural_terminal_state',
                'pid': __import__('os').getpid(), 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
                'scientific_workers_held': 0, 'runtime_adopted': False})
            time.sleep(1)
        assert read(A / 'service_owned_workflows_20261006/root_and_rank_cache_serial_window/service_execution.json')['status'] == 'passed'
        assert read(A / 'root_and_rank_cache_serial_window_20261006/execution.json')['status'] == 'passed'
        full = A / 'bounded_root_replay_full_controls_20261006/verification.json'
        control = A / 'root_and_rank_cache_actual_worker_controls_20261006/verification.json'
        proof = read(control)
        assert proof['status'] == 'passed_actual_Windows_worker_combined_caches_full_bits_CSV8_metrics_and_changed_downstream_graph'
        assert proof['all5635800_raw_bits_and_complete_mapped_CSV_bytes_verified_each_call']
        assert proof['all8_original_official_metrics_exact_each_call']
        assert read(full)['warm_prediction_median_improved']
        pins.update({str(control): sha(control), str(full): sha(full),
            str(A / 'root_and_rank_cache_official_worker_adapter_20261006.py'):
                sha(A / 'root_and_rank_cache_official_worker_adapter_20261006.py'),
            str(A / 'bounded_root_replay_memoization_20261006.py'):
                sha(A / 'bounded_root_replay_memoization_20261006.py')})
        parent, process, idle = suspended_idle(old_monitor,
            '    main (monitor_actual_optimization_progress_v18_20261005.py:146)')
        held.extend((process, parent))
        create(OUT / 'actual_old_observer_idle.json', idle)
        assert not worker.children(recursive=True)
        snapshot = read(QUEUE / 'state.json')
        assert snapshot['pid'] == old['owned_worker_pid']
        assert not any(owned(v) for k, v in snapshot['activated_jobs'].items() if k.startswith('round'))
        create(OUT / 'original_queue_last_snapshot.json', snapshot)
        original_plan = read(QUEUE / 'queue_plan_v10.json')
        assert original_plan['deferred_jobs'] == preparation['original_deferred_jobs']
        plan = deepcopy(original_plan)
        plan.update(status='frozen_actual_queue11_R97_root_cache_execution_only',
            input_sha256={**plan['input_sha256'], **pins},
            previously_activated_jobs=deepcopy(snapshot['activated_jobs']),
            activation_handoff_commit_marker=str(OUT / 'handoff_commit.json'),
            prior_queue_plan=str(QUEUE / 'queue_plan_v10.json'))
        assert plan['deferred_jobs'] == original_plan['deferred_jobs']
        plan_path = QUEUE / 'queue_plan_v11.json'
        create(plan_path, plan)
        new_queue = start_service('dependency_queue_v11', 'run_dependency_queue_v11_20261006.py',
            [str(plan_path)], {**plan['input_sha256'], str(plan_path): sha(plan_path)})
        for _ in range(60):
            assert owned(new_queue)
            current = read(QUEUE / 'state.json')
            if current['pid'] == new_queue['owned_worker_pid']:
                assert current['activated_jobs'] == snapshot['activated_jobs']
                break
            time.sleep(.5)
        else:
            raise RuntimeError('Actual queue11 did not preserve the activated job snapshot')
        new_monitor = start_service('progress_monitor_v35', 'monitor_actual_optimization_progress_v35_20261006.py', [], pins)
        paths = [A / f for f in ('ongoing_optimization_state.json', 'resume_optimization_20261004.json', 'actual_optimization_monitor_state_20261005.json')]
        for _ in range(180):
            assert owned(new_monitor) and owned(new_queue)
            documents = [read(p) for p in paths]
            if all(v.get('actual_observer_version') == 35 and
                   v.get('dependency_queue_registry') == 'analysis/service_owned_workflows_20261006/dependency_queue_v11/native_launch.json'
                   for v in documents) and len({v.get('complete_observer_generation') for v in documents}) == 1:
                break
            time.sleep(1)
        else:
            raise RuntimeError('Actual observer35 did not produce one complete actual queue11 generation')
        assert owned(neural)
        retire_suspended(old, new_queue)
        retired = True
        retire_suspended(old_monitor, new_monitor)
        held.clear()
        create(OUT / 'handoff_commit.json', {'status': 'retired_original_controller_and_preserved_scientific_workers',
            'actual_queue': new_queue, 'actual_observer': new_monitor,
            'scientific_workers_stopped_or_restarted': 0, 'new_quality_scores': 0})
        create(OUT / 'verification.json', {'status': 'passed_actual_unstarted_R97_root_rank_worker_adoption_all_original_routes_preserved',
            'input_sha256': pins, 'actual_queue': new_queue, 'actual_observer': new_monitor,
            'preserved_neural_identity': neural, 'original_jobs_and_grids_exact': True,
            'only_R97_scoring_worker_execution_changed': True, 'runtime_adopted_for_unstarted_R97': True,
            'all151_comparisons_candidate_causal_full_ranking_and_main_publication_still_required': True,
            'scientific_workers_stopped_or_restarted': 0, 'new_quality_records': 0, 'new_native_fits': 0})
    except BaseException as exc:
        create(OUT / 'failure.json', {'status': 'failed_preserved_root_cached_dispatch_adoption',
            'error': f'{type(exc).__name__}: {exc}', 'original_controller_retired': retired})
        raise
    finally:
        if not retired:
            for identity in (new_monitor, new_queue):
                if identity is not None and owned(identity):
                    parent, process = pair(identity)
                    assert not process.children(recursive=True)
                    process.suspend()
                    parent.suspend()
                    retire_suspended(identity, {'reason': 'failed pre-dispatch helper adoption'})
            if snapshot is not None:
                write(QUEUE / 'state.json', snapshot)
        for process in reversed(held):
            if process.is_running():
                process.resume()


if __name__ == '__main__':
    main()
