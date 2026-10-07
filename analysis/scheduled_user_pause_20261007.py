"""Suspend this project's verified workers at the user's deadline; resume only on request.

This is operational scheduling. It never marks a scientific job passed, kills a
training process, edits a model source, or implements automatic morning resume.
"""
from pathlib import Path
from datetime import datetime, timedelta
import argparse
import ctypes
import hashlib
import json
import mmap
import os
import struct
import subprocess
import sys
import time

import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
DEFAULT = A / 'user_pause_until_manual_continue_20261007'


def read(path):
    for attempt in range(100):
        try:
            return json.loads(Path(path).read_text(encoding='utf-8-sig'))
        except PermissionError:
            if attempt == 99:
                raise
            time.sleep(.02)


def write(path, value):
    path = Path(path).resolve()
    assert path.is_relative_to(A) and path.suffix == '.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + f'.pause-{os.getpid()}.tmp')
    with temporary.open('w', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())
    for attempt in range(100):
        try:
            os.replace(temporary, path)
            return
        except PermissionError:
            if attempt == 99:
                raise
            time.sleep(.05)


def now():
    return datetime.now().astimezone().isoformat(timespec='seconds')


def identity(process):
    return {'pid': process.pid, 'creation_time': process.create_time(),
            'command_line': process.cmdline(), 'name': process.name()}


def exact(row):
    try:
        process = psutil.Process(row['pid'])
        if (process.create_time() == row['creation_time']
                and process.cmdline() == row['command_line']):
            return process
    except psutil.Error:
        pass
    return None


def protected(process):
    name = process.name().lower()
    return (name in ('java.exe', 'javaw.exe', 'wmiprvse.exe')
            or name.startswith('qemu') or 'codex' in name)


def verified_pair(row):
    try:
        worker, parent = psutil.Process(row['owned_worker_pid']), psutil.Process(row['pid'])
        args = row['script_args']
        script = Path(row['script']).resolve()
        assert script.is_relative_to(A) and args
        assert Path(args[0]).resolve().is_relative_to(A)
        assert worker.create_time() == row['owned_worker_creation_time']
        assert parent.create_time() == row['owned_parent_creation_time']
        assert worker.cmdline()[-len(args):] == args
        assert worker.cmdline()[1:] == parent.cmdline()[1:]
        assert worker.ppid() == parent.pid
        assert not protected(worker) and not protected(parent)
        return worker, parent
    except (psutil.Error, KeyError, AssertionError, IndexError, TypeError):
        return None


def inventory(full=False):
    paths = list((A / 'service_owned_workflows_20261006').glob('*/native_launch.json'))
    if full:
        paths += list(A.rglob('native_launch.json'))
    candidates = []
    for path in dict.fromkeys(paths):
        try:
            row = read(path)
            if Path(row['script_args'][0]).resolve().parent != path.resolve().parent:
                continue  # Archived launch copies do not establish ownership.
            candidates.append((row, str(path.resolve())))
        except (OSError, ValueError, KeyError, IndexError):
            continue
    queue = A / 'service_owned_dependency_queue_v4_20261006/state.json'
    if queue.exists():
        for row in read(queue).get('activated_jobs', {}).values():
            candidates.append((row, str(queue)))
    live = {}
    for row, evidence in candidates:
        pair = verified_pair(row)
        if pair is not None:
            worker, parent = pair
            if worker.pid == os.getpid() or parent.pid == os.getpid():
                continue  # The guardian must remain running to retain RAM and report status.
            live[(worker.pid, worker.create_time())] = {
                'name': row['name'], 'evidence': evidence, 'launch': row,
                'worker': identity(worker), 'parent': identity(parent),
                'worker_status': worker.status(), 'parent_status': parent.status()}
    return sorted(live.values(), key=lambda row: row['name'])


class Journal:
    def __init__(self, folder):
        self.path = folder / 'suspension_journal.json'
        self.data = read(self.path) if self.path.exists() else {
            'status': 'created', 'entries': [], 'events': [],
            'scientific_jobs_terminated': 0, 'user_applications_touched': 0}

    def flush(self):
        self.data['at_local'] = now()
        write(self.path, self.data)

    def suspend(self, process, owner, role):
        row = identity(process)
        assert not protected(process) and process.pid != os.getpid()
        existing = next((e for e in self.data['entries'] if
                         e['identity'] == row and e['phase'] in ('pending', 'suspended')), None)
        if existing is not None:
            if process.status() == psutil.STATUS_STOPPED:
                return
            # An existing owner's finalizer may have resumed a dispatcher.
            existing['phase'] = 'pending'
            self.flush()
            process.suspend()
            assert process.status() == psutil.STATUS_STOPPED
            existing['phase'] = 'suspended'
            existing['resuspended_at_local'] = now()
            self.flush()
            return
        if process.status() == psutil.STATUS_STOPPED:
            if not any(e.get('identity') == row and e.get('event') ==
                       'already_suspended_by_another_owner' for e in self.data['events']):
                self.data['events'].append({'event': 'already_suspended_by_another_owner',
                                            'identity': row, 'owner': owner, 'at_local': now()})
                self.flush()
            return
        entry = {'identity': row, 'owner': owner, 'role': role,
                 'previous_status': process.status(), 'phase': 'pending', 'at_local': now()}
        self.data['entries'].append(entry)
        self.flush()  # Durable write-ahead identity, before touching the process.
        process = exact(row)
        if process is None:
            entry['phase'] = 'exited_before_suspend'
        else:
            process.suspend()
            assert process.status() == psutil.STATUS_STOPPED
            entry['phase'] = 'suspended'
        self.flush()

    def suspend_pair(self, row, quiet_only=False):
        pair = verified_pair(row['launch'])
        if pair is None:
            return False
        worker, parent = pair
        before = len(self.data['entries'])
        self.suspend(worker, row['name'], 'worker')
        self.suspend(parent, row['name'], 'launch_parent')
        children = [p for p in parent.children(recursive=True)
                    if p.pid != worker.pid and p.name().lower() != 'conhost.exe']
        if quiet_only and children:
            # Allow in-flight Git/browser subprocesses to finish before midnight.
            for entry in reversed(self.data['entries'][before:]):
                process = exact(entry['identity'])
                if process is not None and entry['phase'] in ('pending', 'suspended'):
                    process.resume()
                entry['phase'] = 'reverted_for_active_subprocess'
            self.flush()
            return False
        # The worker and launcher are frozen, so they cannot race new children.
        for process in sorted(children, key=lambda p: len(p.parents()), reverse=True):
            if not protected(process):
                self.suspend(process, row['name'], 'owned_descendant')
            else:
                raise RuntimeError('Protected application found in an owned task subtree')
        return True

    def resume(self):
        entries = [e for e in self.data['entries'] if e['phase'] in ('pending', 'suspended')]
        # Descendants and scientific workers resume before dispatchers.
        entries.sort(key=lambda e: (e['role'] != 'owned_descendant',
                                    'queue' in e['owner'] or 'publisher' in e['owner']
                                    or 'monitor' in e['owner'],
                                    e['role'] == 'launch_parent'))
        for entry in entries:
            process = exact(entry['identity'])
            if process is None:
                entry['phase'] = 'missing_at_manual_resume'
            elif process.status() == psutil.STATUS_STOPPED:
                process.resume()
                entry['phase'] = 'resumed_by_explicit_user_request'
            else:
                entry['phase'] = 'already_running_at_manual_resume'
            entry['manual_resume_at_local'] = now()
            self.flush()
        self.data['status'] = 'resumed_only_recorded_exact_identities_on_explicit_request'
        self.flush()


def run(folder):
    config = read(folder / 'schedule.json')
    deadline = datetime.fromisoformat(config['pause_at_local'])
    fixture = config.get('isolated_preflight_target')
    if fixture is not None:
        assert folder.name.startswith('scheduled_user_pause_integration_preflight_')
        assert fixture['name'].startswith('isolated_preflight_probe')
        assert Path(fixture['original_driver']).resolve() == Path(__file__).resolve()
        assert fixture['original_arguments'] == ['probe', '--folder', str(folder)]
    quiesce = deadline - timedelta(seconds=.25 if fixture else 300)
    assert config['resume_policy'] == 'only_after_actual_user_continue'
    journal = Journal(folder)
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.SetThreadExecutionState.argtypes = [ctypes.c_uint32]
    kernel.SetThreadExecutionState.restype = ctypes.c_uint32
    assert kernel.SetThreadExecutionState(0x80000001)  # Screen may turn off; retain RAM.
    last_full = 0
    rows = []
    try:
        while not (folder / 'manual_resume_requested.json').exists():
            current = datetime.now().astimezone()
            if current >= quiesce:
                full = time.monotonic() - last_full >= 300
                if fixture is None:
                    rows = inventory(full=full)
                else:
                    rows = [{'name': fixture['name'], 'launch': fixture}]
                if full:
                    last_full = time.monotonic()
                for row in rows:
                    controller = 'dependency_queue' in row['name']
                    publisher = 'publisher' in row['name'] or 'publication' in row['name']
                    if current >= deadline or controller or publisher:
                        try:
                            journal.suspend_pair(row, quiet_only=current < deadline)
                        except psutil.NoSuchProcess:
                            pass  # Actual completion during collection is retained.
                journal.data['status'] = ('paused_waiting_for_actual_user_continue'
                                          if current >= deadline else 'quiescing_dispatch_and_publication')
                journal.flush()
                status = journal.data['status']
            else:
                status = 'scheduled_running_until_deadline'
            write(folder / 'guardian_status.json', {
                'status': status, 'at_local': now(), 'guardian': identity(psutil.Process()),
                'pause_at_local': config['pause_at_local'],
                'resume_policy': config['resume_policy'],
                'resume_at_local': None, 'automatic_resume_enabled': False,
                'suspended_entries': sum(e['phase'] == 'suspended' for e in journal.data['entries']),
                'scientific_jobs_terminated': 0, 'user_applications_touched': 0,
                'system_awake_request_active': True})
            time.sleep(.05 if fixture else (5 if current >= quiesce else 20))
        write(folder / 'guardian_exit_for_manual_resume.json', {
            'status': 'scheduler_exited_on_explicit_manual_resume_marker', 'at_local': now(),
            'resume_request': read(folder / 'manual_resume_requested.json'),
            'processes_resumed_by_scheduler': 0})
    finally:
        kernel.SetThreadExecutionState(0x80000000)


def resume(folder, user_continue):
    assert user_continue, 'Actual user continue is required; no timed morning resume.'
    if not (folder / 'manual_resume_requested.json').exists():
        test_only = bool(read(folder / 'schedule.json').get('isolated_preflight_target'))
        write(folder / 'manual_resume_requested.json', {
            'actual_user_instruction': 'simulated_continue_in_isolated_preflight' if test_only else '继续',
            'test_only': test_only, 'at_local': now(),
            'created_by_explicit_resume_command': True})
    status = folder / 'guardian_status.json'
    if status.exists():
        owner = read(status)['guardian']
        limit = time.monotonic() + 45
        while exact(owner) is not None:
            assert time.monotonic() < limit, 'Guardian has not exited; no process resumed.'
            time.sleep(.2)
    journal = Journal(folder)
    journal.resume()
    write(folder / 'manual_resume_receipt.json', {
        'status': journal.data['status'], 'at_local': now(),
        'resume_requested_by_user': True, 'entries': journal.data['entries'],
        'restarted_jobs': 0, 'user_applications_touched': 0})


def probe(folder):
    process = psutil.Process()
    parent = process.parent()
    write(folder / 'probe_identity.json', {'worker': identity(process), 'parent': identity(parent)})
    tagname = f'Local\\Saiti5PauseProbe_{process.pid}_{int(process.create_time() * 1000000)}'
    counter_memory = mmap.mmap(-1, 8, tagname=tagname)
    write(folder / 'probe_shared_counter.json', {'tagname': tagname})
    counter = 0
    try:
        while not (folder / 'probe_stop.json').exists():
            counter += 1
            counter_memory[:] = struct.pack('<Q', counter)
            write(folder / 'probe_heartbeat.json', {'counter': counter, 'at_local': now()})
            time.sleep(.15)
    finally:
        counter_memory.close()


def preflight(folder):
    assert not folder.exists()
    folder.mkdir()
    startup = subprocess.STARTUPINFO()
    startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startup.wShowWindow = subprocess.SW_HIDE
    child = subprocess.Popen([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8',
                              str(Path(__file__)), 'probe', '--folder', str(folder)],
                             cwd=ROOT, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL, startupinfo=startup,
                             creationflags=subprocess.CREATE_NO_WINDOW)
    pair = None
    try:
        limit = time.monotonic() + 15
        while not (folder / 'probe_identity.json').exists():
            assert child.poll() is None and time.monotonic() < limit
            time.sleep(.05)
        pair = read(folder / 'probe_identity.json')
        assert pair['parent']['pid'] == child.pid
        worker, parent = exact(pair['worker']), exact(pair['parent'])
        assert worker is not None and parent is not None
        journal = Journal(folder)
        journal.suspend(worker, 'isolated_preflight_probe', 'worker')
        journal.suspend(parent, 'isolated_preflight_probe', 'launch_parent')
        paused_counter = read(folder / 'probe_heartbeat.json')['counter']
        cpu = list(worker.cpu_times())
        time.sleep(1.5)
        assert read(folder / 'probe_heartbeat.json')['counter'] == paused_counter
        assert list(worker.cpu_times()) == cpu and worker.status() == psutil.STATUS_STOPPED
        journal.resume()
        time.sleep(.5)
        assert read(folder / 'probe_heartbeat.json')['counter'] > paused_counter
        assert exact(pair['worker']) is not None
        bad_time = {**pair['worker'], 'creation_time': pair['worker']['creation_time'] + 1}
        bad_command = {**pair['worker'], 'command_line': [*pair['worker']['command_line'], 'wrong']}
        assert exact(bad_time) is None and exact(bad_command) is None
        worker.suspend()  # A prior owner, outside this new journal, holds the probe.
        prior = Journal(folder / 'prior_owner_case')
        prior.suspend(worker, 'isolated_preflight_probe', 'worker')
        prior.resume()
        assert worker.status() == psutil.STATUS_STOPPED and not prior.data['entries']
        worker.resume()
        write(folder / 'probe_stop.json', {'stop_only_this_test_probe': True})
        assert child.wait(timeout=10) == 0
        write(folder / 'verification.json', {
            'status': 'passed_actual_hidden_probe_suspend_same_identity_resume_and_prior_owner_preserved',
            'paused_heartbeat_unchanged': True, 'paused_CPU_times_unchanged': True,
            'resumed_same_PID_birth_and_command': True, 'wrong_birth_and_command_rejected': True,
            'prior_owner_suspend_not_resumed': True, 'probe': pair,
            'scientific_workers_touched': 0, 'user_applications_touched': 0,
            'new_model_fits': 0, 'new_quality_scores': 0,
            'scheduler_resumes_automatically': False, 'at_local': now()})
    finally:
        if child.poll() is None and pair is not None:
            for row in pair.values():
                process = exact(row)
                if process is not None and process.status() == psutil.STATUS_STOPPED:
                    process.resume()
            write(folder / 'probe_stop.json', {'stop_only_this_test_probe': True})
            child.wait(timeout=10)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['run', 'resume', 'preflight', 'inventory', 'probe'])
    parser.add_argument('--folder', type=Path, default=DEFAULT)
    parser.add_argument('--user-continue', action='store_true')
    args = parser.parse_args()
    folder = args.folder.resolve()
    assert folder.is_relative_to(A) and folder.drive.upper() in ('D:', 'E:')
    if args.mode == 'inventory':
        print(json.dumps(inventory(full=True), ensure_ascii=False, indent=2))
    elif args.mode == 'run':
        run(folder)
    elif args.mode == 'resume':
        resume(folder, args.user_continue)
    elif args.mode == 'preflight':
        preflight(folder)
    else:
        probe(folder)


if __name__ == '__main__':
    main()
