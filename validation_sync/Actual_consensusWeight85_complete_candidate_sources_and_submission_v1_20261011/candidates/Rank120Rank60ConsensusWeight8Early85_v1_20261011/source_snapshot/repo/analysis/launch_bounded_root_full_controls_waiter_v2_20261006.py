"""Supersede only the proved idle helper; retain the full scientific harness."""
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from handoff_ready_goss_full_execution_20261006 import start_service, pair
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle

OUT = A / 'bounded_root_waiter_safe_publication_adoption_20261006'
WAIT = A / 'bounded_root_full_controls_waiter_v2_20261006'


def main():
    assert not OUT.exists() and not WAIT.exists()
    assert not (A / 'bounded_root_replay_full_controls_20261006').exists()
    prep = read(A / 'bounded_root_waiter_safe_publication_preparation_20261006.json')
    for path, digest in {**prep['original_sources'], **prep['new_sources']}.items():
        assert sha(path) == digest, path
    old = read(A / 'service_owned_workflows_20261006/bounded_root_full_controls_waiter/native_launch.json')
    preserved = {'neural16384_annual': read(A / 'service_owned_workflows_20261006/neural16384_annual/native_launch.json')}
    state = read(A / 'service_owned_dependency_queue_v4_20261006/state.json')
    preserved.update({k: v for k, v in state['activated_jobs'].items()
                      if k.startswith('round') and owned(v)})
    assert all(owned(value) for value in preserved.values())
    OUT.mkdir()
    pins = {**prep['original_sources'], **prep['new_sources'],
        str(Path(__file__)): sha(__file__),
        str(A / 'bounded_root_waiter_safe_publication_preparation_20261006.json'):
            sha(A / 'bounded_root_waiter_safe_publication_preparation_20261006.json')}
    create(OUT / 'frozen_before_adoption.json', {
        'old_waiter': old, 'preserved_scientific_workers': preserved,
        'input_sha256': pins, 'only_idle_helper_may_be_retired': True,
        'full_control_harness_unchanged': True, 'runtime_adopted': False})
    held = []
    retired = False
    successor = None
    try:
        parent, worker, idle = suspended_idle(old,
            '    main (wait_bounded_root_full_controls_20261006.py:84)')
        held.extend((worker, parent))
        assert not worker.children(recursive=True)
        assert not (A / 'bounded_root_replay_full_controls_20261006').exists()
        create(OUT / 'actual_old_waiter_idle_before_and_after_hold.json', idle)
        successor = start_service('bounded_root_full_controls_waiter_v2',
            'wait_bounded_root_full_controls_v2_20261006.py', [], pins)
        assert owned(successor) and not WAIT.exists()
        assert successor['actual_native_console_handle'] == 0
        assert not successor['independent_launch_root_in_any_job']
        assert all(owned(v) for v in preserved.values())
        assert not worker.children(recursive=True)
        worker.terminate()
        worker.wait(timeout=15)
        parent.terminate()
        parent.wait(timeout=15)
        retired = True
        held.clear()
        create(Path(old['script_args'][0]).parent / 'administrative_supersession_safe_publication_v2_20261006.json', {
            'status': 'administratively_retired_verified_idle_helper',
            'old_identity': old, 'successor': successor,
            'original_pending_full_scientific_scope_preserved': True,
            'scientific_workers_stopped_or_restarted': 0})
        assert all(owned(v) for v in preserved.values())
        create(OUT / 'activation.json', {
            'status': 'committed_safe_publication_waiter_adoption',
            'old_waiter_retired_only_after_idle_proof': True,
            'successor': successor, 'preserved_scientific_workers': preserved,
            'input_sha256': pins, 'scientific_workers_stopped_or_restarted': 0,
            'new_quality_scores': 0, 'new_native_fits': 0})
        for _ in range(60):
            assert owned(successor)
            if (WAIT / 'state.json').exists():
                break
            time.sleep(.5)
        actual = read(WAIT / 'state.json')
        assert actual['pid'] == successor['owned_worker_pid']
        assert actual['full_controls_started'] is False
        assert actual['scientific_processes_held'] == 0
        create(WAIT / 'actual_launch_control.json', {
            'status': 'passed_actual_consoleless_waiter_preserving_live_scientific_processes',
            'actual_waiter': successor, 'initial_actual_state': actual,
            'preserved_scientific_workers': preserved,
            'actual_idle_helper_adoption': str(OUT / 'activation.json'),
            'unchanged_admission_policy_original_control': str(A / 'bounded_root_full_controls_waiter_20261006/actual_launch_control.json'),
            'full_controls_started': False, 'runtime_adopted': False,
            'new_quality_scores': 0, 'scientific_workers_stopped_or_restarted': 0})
        print('passed_actual_idle_waiter_adoption_and_consoleless_successor', flush=True)
    except BaseException as exc:
        create(OUT / 'failure.json', {'status': 'failed_preserved_safe_publication_waiter_adoption',
            'error': f'{type(exc).__name__}: {exc}', 'old_waiter_retired': retired,
            'successor': successor, 'scientific_workers_stopped_or_restarted': 0})
        raise
    finally:
        for process in reversed(held):
            if process.is_running():
                process.resume()


if __name__ == '__main__':
    main()
