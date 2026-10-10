"""Use real independent Windows services to verify normal and abrupt-owner recovery on synthetic schedulers."""
from pathlib import Path
import json
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
OUT = A / 'scheduler_fit_guard_controls_v2_20261006'


def main():
    from handoff_distribution_views_progress_monitor_20261006 import read, sha, create
    from run_dependency_queue_v3_20261006 import owned
    from launch_service_owned_workflow_with_pwsh_20261006 import launch
    assert not OUT.exists()
    OUT.mkdir()
    sources = [Path(__file__), A / 'owned_scheduler_native_fit_hold_v2_20261006.py',
        A / 'scheduler_hold_dummy_heartbeat_20261006.py', A / 'scheduler_hold_synthetic_owner_20261006.py',
        A / 'watch_owned_scheduler_fit_lease_20261006.py', A / 'run_service_owned_windows_workflow_20261006.py',
        A / 'launch_service_owned_workflow_with_pwsh_20261006.py', A / 'launch_service_owned_windows_workflow_20261006.ps1']
    bindings = {str(p.resolve()): sha(p) for p in sources}
    create(OUT / 'protocol.json', {'status': 'frozen_before_real_independent_service_normal_and_abrupt_owner_exit_controls',
        'input_sha256': bindings, 'touch_actual_scientific_or_dependency_workers': False,
        'new_native_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})
    def start(label, driver, arguments):
        service = OUT / label
        service.mkdir()
        definition = service / 'job_definition.json'
        create(definition, {'name': 'synthetic_scheduler_hold_' + label, 'driver': str(A / driver), 'arguments': arguments,
            'scratch': str(ROOT / 'tmp/synthetic_scheduler_fit_guard_controls_20261006'),
            'input_sha256': bindings, 'bootstrap_sha256': sha(A / 'run_service_owned_windows_workflow_20261006.py'),
            'command_line': subprocess.list2cmdline([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8',
                str(A / 'run_service_owned_windows_workflow_20261006.py'), str(definition)])})
        launch(definition, Path('C:/Users/esesl/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/powershell/pwsh.exe'))
        deadline = time.monotonic() + 60
        while not (service / 'native_launch.json').exists():
            assert time.monotonic() < deadline
            time.sleep(.1)
        row = read(service / 'native_launch.json')
        assert owned(row) and row['actual_native_console_handle'] == 0 and not row['independent_launch_root_in_any_job']
        return service, row
    dummy, dummy_row = start('dummy_scheduler', 'scheduler_hold_dummy_heartbeat_20261006.py', [str(OUT)])
    heartbeat = OUT / 'dummy_heartbeat.jsonl'
    deadline = time.monotonic() + 30
    while not heartbeat.exists() or heartbeat.stat().st_size == 0:
        assert owned(dummy_row) and time.monotonic() < deadline
        time.sleep(.1)
    checks = []
    try:
        for mode in ('normal', 'abrupt_exit'):
            service, row = start(mode + '_owner', 'scheduler_hold_synthetic_owner_20261006.py',
                                 [str(OUT), mode, str(dummy / 'native_launch.json')])
            held = OUT / f'{mode}_actual_owner_control.json'
            deadline = time.monotonic() + 45
            while not held.exists():
                assert owned(row) and time.monotonic() < deadline
                time.sleep(.1)
            lease_folder = OUT / ('scheduler_fit_hold_' + mode)
            terminal = (service / 'service_execution.json') if mode == 'normal' else (lease_folder / 'lease_emergency_resume.json')
            while not terminal.exists():
                assert time.monotonic() < deadline
                time.sleep(.1)
            if mode == 'normal':
                assert read(terminal)['status'] == 'passed'
            else:
                assert read(terminal)['status'] == 'exact_scheduler_resumed_after_capacity_owner_exit'
                assert set(read(terminal)['resumed_only_scheduler_pids']) == {dummy_row['pid'], dummy_row['owned_worker_pid']}
            last = heartbeat.stat().st_size
            deadline = time.monotonic() + 10
            while heartbeat.stat().st_size <= last:
                assert owned(dummy_row) and time.monotonic() < deadline
                time.sleep(.1)
            guard = read(lease_folder / 'independent_guard_service/native_launch.json')
            lease = read(lease_folder / 'lease.json')
            assert lease['actual_owner_native_worker_in_any_job'] is True
            assert guard['actual_native_console_handle'] == 0 and not guard['independent_launch_root_in_any_job']
            checks.append({'mode': mode, 'actual_native_owner_in_venv_job': True,
                'independent_WMI_guard_root_outside_any_job': True,
                'heartbeat_actually_paused_and_resumed': True, 'terminal': read(terminal),
                'actual_independent_guard': guard, 'only_synthetic_scheduler_touched': True})
    finally:
        create(OUT / 'dummy_finish.json', {'status': 'finish_only_synthetic_scheduler'})
        deadline = time.monotonic() + 15
        while not (dummy / 'service_execution.json').exists():
            assert time.monotonic() < deadline
            time.sleep(.1)
        assert read(dummy / 'service_execution.json')['status'] == 'passed'
    for path, digest in bindings.items():
        assert sha(path) == digest
    create(OUT / 'verification.json', {'status': 'passed_actual_independent_WMI_guard_normal_and_abrupt_venv_owner_exit',
        'input_sha256': bindings, 'checks': checks, 'only_synthetic_scheduler_and_owners_used': True,
        'actual_scientific_or_dependency_workers_touched': 0,
        'new_native_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})


if __name__ == '__main__':
    main()
