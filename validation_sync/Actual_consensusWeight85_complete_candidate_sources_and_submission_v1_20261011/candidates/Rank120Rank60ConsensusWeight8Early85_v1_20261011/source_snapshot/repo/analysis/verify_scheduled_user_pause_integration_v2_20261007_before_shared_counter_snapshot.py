"""Exercise the real hidden timer on a dedicated probe, never on scientific workers."""
from pathlib import Path
from datetime import datetime, timedelta
import json
import sys
import time
import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
from run_dependency_queue_v3_20261006 import read, sha, owned
from handoff_ready_goss_full_execution_20261006 import start_service
from scheduled_user_pause_20261007 import write, exact, resume, identity, read


def wait_until(condition):
    limit = time.monotonic() + 30
    while not condition():
        assert time.monotonic() < limit
        time.sleep(.05)


def main():
    folder = A / 'scheduled_user_pause_integration_preflight_v2_20261007'
    assert not folder.exists()
    folder.mkdir()
    module = A / 'scheduled_user_pause_20261007.py'
    pins = {str(module): sha(module)}
    initial = {p.pid: identity(p) for p in psutil.process_iter()
               if p.name().lower().startswith('qemu') or p.name().lower() in ('java.exe', 'javaw.exe')}
    probe = start_service('isolated_preflight_probe_v2', module.name,
                          ['probe', '--folder', str(folder)], pins)
    wait_until(lambda: (folder / 'probe_heartbeat.json').exists())
    pause_at = datetime.now().astimezone() + timedelta(seconds=5)
    config = {'pause_at_local': pause_at.isoformat(),
              'resume_policy': 'only_after_actual_user_continue',
              'automatic_resume_enabled': False, 'resume_at_local': None,
              'isolated_preflight_target': probe}
    write(folder / 'schedule.json', config)
    guardian = start_service('isolated_user_pause_timer_preflight_v2', module.name,
                             ['run', '--folder', str(folder)],
                             {**pins, str(folder / 'schedule.json'): sha(folder / 'schedule.json')})
    wait_until(lambda: (folder / 'guardian_status.json').exists())
    assert read(folder / 'guardian_status.json')['status'] == 'scheduled_running_until_deadline'
    wait_until(lambda: read(folder / 'guardian_status.json')['status'] == 'paused_waiting_for_actual_user_continue')
    snapshot = read(folder / 'probe_identity.json')
    assert all(exact(row).status() == psutil.STATUS_STOPPED for row in snapshot.values())
    counter = read(folder / 'probe_heartbeat.json')['counter']
    time.sleep(.6)
    assert read(folder / 'probe_heartbeat.json')['counter'] == counter
    assert not (folder / 'manual_resume_requested.json').exists()
    resume(folder, user_continue=True)  # Explicitly labelled test-only by the scheduler.
    wait_until(lambda: read(folder / 'probe_heartbeat.json')['counter'] > counter)
    assert all(exact(row) is not None for row in snapshot.values())
    write(folder / 'probe_stop.json', {'stop_only_this_test_probe': True})
    services = A / 'service_owned_workflows_20261006'
    for row in (probe, guardian):
        terminal = services / row['name'] / 'service_execution.json'
        wait_until(lambda: terminal.exists() and not owned(row))
        assert read(terminal)['status'] == 'passed'
    assert all(exact(row) is not None for row in initial.values())
    write(folder / 'verification.json', {
        'status': 'passed_actual_hidden_timer_deadline_pause_no_auto_resume_and_manual_same_identity_resume',
        'actual_probe_launch': probe, 'actual_guardian_launch': guardian,
        'actual_pause_at_local': pause_at.isoformat(),
        'actual_guardian_at_pause': read(folder / 'guardian_status.json'),
        'actual_manual_resume': read(folder / 'manual_resume_receipt.json'),
        'actual_service_terminals': {row['name']: read(services / row['name'] / 'service_execution.json')
                                     for row in (probe, guardian)},
        'only_isolated_probe_suspended': True, 'automatic_resume_enabled': False,
        'scientific_workers_touched': 0, 'user_applications_touched': 0,
        'new_native_fits': 0, 'new_quality_scores': 0,
        'module_sha256': sha(module)})
    print('passed_actual_hidden_timer_deadline_pause_no_auto_resume_and_manual_same_identity_resume')


if __name__ == '__main__':
    try:
        main()
    except BaseException as error:
        folder = A / 'scheduled_user_pause_integration_preflight_v2_20261007'
        if folder.exists():
            write(folder / 'actual_test_failure.json', {
                'status': 'failed_actual_isolated_timer_preflight_v2',
                'error': f'{type(error).__name__}: {error}',
                'scientific_workers_touched': 0})
            if (folder / 'schedule.json').exists():
                resume(folder, user_continue=True)
            write(folder / 'probe_stop.json', {'stop_only_this_test_probe': True})
        raise
