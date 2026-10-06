"""Use a genuinely independent WMI watchdog even when the venv native worker belongs to its redirector job."""
from pathlib import Path
import ctypes
import json
import os
import subprocess
import time

import psutil
from handoff_distribution_views_progress_monitor_20261006 import read, sha, create
from run_dependency_queue_v3_20261006 import owned
from launch_service_owned_workflow_with_pwsh_20261006 import launch

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'


class FitHold:
    def __init__(self, output, controller, label):
        self.folder = Path(output).resolve() / ('scheduler_fit_hold_' + label)
        assert self.folder.is_relative_to(A) and not self.folder.exists()
        self.folder.mkdir()
        self.controller = controller
        self.suspended = []
        self.guard = None

    def __enter__(self):
        assert owned(self.controller)
        root = psutil.Process(self.controller['pid'])
        worker = psutil.Process(self.controller['owned_worker_pid'])
        assert root.create_time() == self.controller['owned_parent_creation_time']
        assert root.cmdline()[1:] == worker.cmdline()[1:]
        attached = ctypes.c_int()
        kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        kernel.GetCurrentProcess.restype = ctypes.c_void_p
        kernel.IsProcessInJob.argtypes = (ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(ctypes.c_int))
        kernel.IsProcessInJob.restype = ctypes.c_int
        assert kernel.IsProcessInJob(kernel.GetCurrentProcess(), None, ctypes.byref(attached))
        row = lambda process: {'pid': process.pid, 'creation_time': process.create_time(), 'command_line': process.cmdline()}
        owner = row(psutil.Process())
        release = self.folder / 'released.json'
        lease = self.folder / 'lease.json'
        create(lease, {'owner': owner, 'schedulers': [row(worker), row(root)],
            'release_marker': str(release), 'scientific_children_never_suspended': True,
            'actual_owner_native_worker_in_any_job': bool(attached.value),
            'independent_watchdog_launch_required_regardless_of_owner_native_job': True})
        guard_service = self.folder / 'independent_guard_service'
        guard_service.mkdir()
        definition = guard_service / 'job_definition.json'
        driver = A / 'watch_owned_scheduler_fit_lease_20261006.py'
        create(definition, {'name': 'independent_scheduler_fit_guard_' + self.folder.name,
            'driver': str(driver), 'arguments': [str(lease)],
            'scratch': str(ROOT / 'tmp/independent_scheduler_fit_guard_20261006'),
            'input_sha256': {str(lease): sha(lease), str(driver): sha(driver)},
            'bootstrap_sha256': sha(A / 'run_service_owned_windows_workflow_20261006.py'),
            'command_line': subprocess.list2cmdline([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8',
                str(A / 'run_service_owned_windows_workflow_20261006.py'), str(definition)])})
        receipt = launch(definition, Path('C:/Users/esesl/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/powershell/pwsh.exe'))
        create(guard_service / 'verified_hidden_launch.json', receipt)
        deadline = time.monotonic() + 60
        while not (guard_service / 'native_launch.json').exists():
            assert time.monotonic() < deadline
            assert psutil.pid_exists(receipt['actual_launch_result']['ProcessId'])
            time.sleep(.1)
        self.guard = read(guard_service / 'native_launch.json')
        assert owned(self.guard)
        assert not self.guard['independent_launch_root_in_any_job'] and self.guard['actual_native_console_handle'] == 0
        assert self.guard['pid'] not in (owner['pid'], owner.get('parent_pid'))
        assert psutil.Process(self.guard['pid']).ppid() == self.guard['service_provider_pid']
        try:
            for process in (worker, root):
                process.suspend()
                self.suspended.append(process)
            self.started = time.monotonic()
            create(self.folder / 'actual_hold.json', {'status': 'only_exact_controller_dispatch_temporarily_deferred',
                'scheduler_pids': [p.pid for p in self.suspended], 'actual_independent_guard_service': self.guard,
                'actual_owner_native_worker_in_any_job': bool(attached.value),
                'scientific_worker_processes_suspended': 0})
            return self
        except BaseException as error:
            self.__exit__(type(error), error, error.__traceback__)
            raise

    def __exit__(self, kind, error, traceback):
        resumed = []
        for process in reversed(self.suspended):
            if process.is_running():
                process.resume()
                resumed.append(process.pid)
        create(self.folder / 'released.json', {'status': 'exact_dependency_dispatch_resumed',
            'resumed_scheduler_pids': resumed, 'held_seconds': time.monotonic() - getattr(self, 'started', time.monotonic()),
            'scientific_workers_touched': 0, 'fit_failed': kind is not None})
        if self.guard is not None:
            terminal = self.folder / 'independent_guard_service/service_execution.json'
            deadline = time.monotonic() + 15
            while not terminal.exists():
                assert owned(self.guard), 'Independent recovery guard exited without terminal evidence.'
                assert time.monotonic() < deadline
                time.sleep(.1)
            assert read(terminal)['status'] == 'passed'
