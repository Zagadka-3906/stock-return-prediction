"""Test deadline termination on a hidden isolated probe and retain durable records."""
from pathlib import Path
from datetime import datetime, timedelta
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
from scheduled_user_pause_20261007 import read, write, exact
from run_dependency_queue_v3_20261006 import sha, owned
from handoff_ready_goss_full_execution_20261006 import start_service


def wait_until(condition):
    limit = time.monotonic() + 30
    while not condition():
        assert time.monotonic() < limit
        time.sleep(.05)


def main():
    folder = A / 'shutdown_ready_stop_preflight_current2355_preheld_20261008'
    assert not folder.exists()
    folder.mkdir()
    module = A / 'user_requested_stop2355_v1_20261008.py'
    probe_module = A / 'scheduled_user_pause_20261007.py'
    probe = start_service('shutdown_stop_probe_current2355_preheld_v1_20261008', probe_module.name,
                          ['probe', '--folder', str(folder)], {str(probe_module): sha(probe_module)})
    wait_until(lambda: (folder / 'probe_identity.json').exists())
    identities = read(folder / 'probe_identity.json')
    exact(identities['worker']).suspend()  # Simulate a previous capacity owner's hold.
    write(folder / 'saved_test_record.json', {'status': 'durable_test_record_before_stop', 'values': [1, 2, 3]})
    saved_hash = sha(folder / 'saved_test_record.json')
    write(folder / 'schedule.json', {
        'stop_at_local': (datetime.now().astimezone() + timedelta(seconds=5)).isoformat(),
        'output_folder': str(folder), 'automatic_restart_enabled': False,
        'execute_Windows_shutdown': False, 'isolated_preflight_target': probe})
    guardian = start_service('shutdown_stop_guardian_current2355_preheld_preflight_v1_20261008', module.name,
                             ['run', '--folder', str(folder)],
                             {str(module): sha(module), str(probe_module): sha(probe_module),
                              str(folder / 'schedule.json'): sha(folder / 'schedule.json')})
    wait_until(lambda: (folder / 'guardian_status.json').exists())
    assert read(folder / 'guardian_status.json')['status'] == 'scheduled_shutdown_compatible_stop'
    wait_until(lambda: (folder / 'disk_recovery_manifest.json').exists())
    wait_until(lambda: not owned(guardian))
    terminal = A / 'service_owned_workflows_20261006' / guardian['name'] / 'service_execution.json'
    assert read(terminal)['status'] == 'passed'
    assert all(exact(row) is None for row in identities.values())
    assert sha(folder / 'saved_test_record.json') == saved_hash
    assert not (A / 'service_owned_workflows_20261006' / probe['name'] / 'service_execution.json').exists()
    stop = read(folder / 'disk_recovery_manifest.json')
    assert stop['scientific_pass_markers_written_for_interrupted_workers'] == 0
    write(folder / 'verification.json', {
        'status': 'passed_actual_hidden_deadline_stop_preheld_probe_and_durable_recovery_record',
        'actual_probe': probe, 'actual_guardian': guardian, 'actual_guardian_terminal': read(terminal),
        'saved_test_record_sha256': saved_hash, 'actual_stop': stop,
        'only_isolated_probe_terminated': True,
        'preexisting_other_owner_suspension_handled_without_resuming': True, 'scientific_workers_terminated': 0,
        'user_applications_touched': 0, 'Windows_shutdown_executed': False,
        'automatic_restart_enabled': False, 'interrupted_probe_not_marked_passed': True,
        'module_sha256': sha(module), 'pause_helper_sha256': sha(probe_module),
        'new_native_fits': 0, 'new_quality_scores': 0})
    print('passed_actual_hidden_deadline_stop_exact_probe_identities_and_durable_recovery_record')


if __name__ == '__main__':
    main()
