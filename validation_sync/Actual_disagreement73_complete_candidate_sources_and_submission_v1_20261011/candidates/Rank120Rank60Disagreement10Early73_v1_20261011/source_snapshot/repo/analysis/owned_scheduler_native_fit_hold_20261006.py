"""Briefly defer new dependency dispatch during a measured native fit; never suspend scientific children."""
from pathlib import Path
import ctypes
import os
import time
import psutil
from handoff_distribution_views_progress_monitor_20261006 import read, create
from run_dependency_queue_v3_20261006 import owned
from windows_hidden_process_launch_20261006 import launch

ROOT = Path(__file__).resolve().parents[1]


class FitHold:
    def __init__(self, output, controller, label):
        self.folder = Path(output).resolve() / ('scheduler_fit_hold_' + label)
        assert self.folder.is_relative_to(ROOT / 'analysis') and not self.folder.exists()
        self.folder.mkdir()
        self.controller = controller
        self.suspended = []
        self.guard = None
        self.streams = []

    def __enter__(self):
        assert owned(self.controller)
        root = psutil.Process(self.controller['pid'])
        worker = psutil.Process(self.controller['owned_worker_pid'])
        assert root.create_time() == self.controller['owned_parent_creation_time']
        assert root.cmdline()[1:] == worker.cmdline()[1:]
        # The owner is a consoleless WMI service, so its watchdog also survives
        # outside the command session job. It does not run another model.
        attached = ctypes.c_int()
        kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        kernel.GetCurrentProcess.restype = ctypes.c_void_p
        kernel.IsProcessInJob.argtypes = (ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(ctypes.c_int))
        kernel.IsProcessInJob.restype = ctypes.c_int
        assert kernel.IsProcessInJob(kernel.GetCurrentProcess(), None, ctypes.byref(attached))
        assert not attached.value
        row = lambda process: {'pid': process.pid, 'creation_time': process.create_time(), 'command_line': process.cmdline()}
        release = self.folder / 'released.json'
        lease = self.folder / 'lease.json'
        create(lease, {'owner': row(psutil.Process()), 'schedulers': [row(worker), row(root)],
            'release_marker': str(release), 'scientific_children_never_suspended': True})
        for name in ('stdout.log', 'stderr.log'):
            self.streams.append((self.folder / name).open('xb'))
        self.guard = launch([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8',
            str(ROOT / 'analysis/watch_owned_scheduler_fit_lease_20261006.py'), str(lease)],
            cwd=ROOT, env=os.environ.copy(), stdout=self.streams[0], stderr=self.streams[1])
        assert self.guard.poll() is None
        try:
            for process in (worker, root):
                process.suspend()
                self.suspended.append(process)
            assert owned(self.controller)
            self.started = time.monotonic()
            create(self.folder / 'actual_hold.json', {'status': 'only_exact_controller_dispatch_temporarily_deferred',
                'scheduler_pids': [p.pid for p in self.suspended], 'guard_pid': self.guard.pid,
                'guard_root_creation_time': psutil.Process(self.guard.pid).create_time(),
                'scientific_worker_processes_suspended': 0})
            return self
        except BaseException:
            self.__exit__(None, None, None)
            raise

    def __exit__(self, kind, error, traceback):
        resumed = []
        try:
            for process in reversed(self.suspended):
                if process.is_running():
                    process.resume()
                    resumed.append(process.pid)
            create(self.folder / 'released.json', {'status': 'exact_dependency_dispatch_resumed',
                'resumed_scheduler_pids': resumed, 'held_seconds': time.monotonic() - getattr(self, 'started', time.monotonic()),
                'scientific_workers_touched': 0, 'fit_failed': kind is not None})
            if self.guard is not None:
                self.guard.wait(timeout=15)
                assert self.guard.returncode == 0
        finally:
            for stream in self.streams:
                stream.close()
