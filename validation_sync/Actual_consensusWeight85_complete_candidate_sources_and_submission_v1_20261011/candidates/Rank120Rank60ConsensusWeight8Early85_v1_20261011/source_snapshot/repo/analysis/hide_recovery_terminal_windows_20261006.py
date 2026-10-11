"""Hide only verified project recovery terminals; preserve all scientific jobs."""
from pathlib import Path
from datetime import datetime
import ctypes
import hashlib
import json
import time

import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
OUT = A / 'recovery_terminal_window_fix_20261006'
RECOVERY = A / 'system_reboot_workflow_recovery_20261006/verification.json'


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def create(path, value):
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    assert not OUT.exists()
    OUT.mkdir()
    jobs = json.loads(RECOVERY.read_text(encoding='utf-8'))['jobs']
    started = min(datetime.fromisoformat(row['at_local']).timestamp() for row in jobs)
    owned, identities = set(), {}
    for row in jobs:
        try:
            parent = psutil.Process(row['pid'])
            command = parent.cmdline()
            if row['script'] not in command or command[-len(row['script_args']):] != row['script_args']:
                continue
            for process in [parent, *parent.children(recursive=True)]:
                owned.add(process.pid)
            worker = psutil.Process(row['owned_worker_pid'])
            if worker.create_time() == row['owned_worker_creation_time']:
                identities[worker.pid] = {'creation_time': worker.create_time(), 'command': worker.cmdline()}
        except psutil.Error:
            continue
    user = ctypes.WinDLL('user32', use_last_error=True)
    callback_type = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)
    user.EnumWindows.argtypes = [callback_type, ctypes.c_void_p]
    user.IsWindowVisible.argtypes = [ctypes.c_void_p]
    user.GetWindowThreadProcessId.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_ulong)]
    user.GetClassNameW.argtypes = [ctypes.c_void_p, ctypes.c_wchar_p, ctypes.c_int]
    user.GetWindowTextW.argtypes = [ctypes.c_void_p, ctypes.c_wchar_p, ctypes.c_int]
    user.ShowWindowAsync.argtypes = [ctypes.c_void_p, ctypes.c_int]
    windows = []

    @callback_type
    def collect(handle, _):
        if not user.IsWindowVisible(handle):
            return 1
        pid = ctypes.c_ulong()
        user.GetWindowThreadProcessId(handle, ctypes.byref(pid))
        kind, title = ctypes.create_unicode_buffer(128), ctypes.create_unicode_buffer(512)
        user.GetClassNameW(handle, kind, 128)
        user.GetWindowTextW(handle, title, 512)
        project_console = pid.value in owned and kind.value in ('PseudoConsoleWindow', 'ConsoleWindowClass')
        terminal = False
        if kind.value == 'CASCADIA_HOSTING_WINDOW_CLASS':
            try:
                process = psutil.Process(pid.value)
                terminal = (process.name().lower() == 'windowsterminal.exe'
                            and process.create_time() >= started-3
                            and title.value.replace('/', '\\').lower() == str(ROOT / '.venv/Scripts/python.exe').lower())
            except psutil.Error:
                pass
        if project_console or terminal:
            windows.append({'handle': int(handle), 'pid': pid.value, 'class': kind.value,
                            'title': title.value, 'verified_project_terminal': terminal})
        return 1

    assert user.EnumWindows(collect, None)
    create(OUT / 'frozen_before_window_hide.json', {
        'status': 'frozen_before_reversible_owned_project_window_hide',
        'at_local': datetime.now().isoformat(timespec='seconds'),
        'source_sha256': {str(Path(__file__).resolve()): sha(__file__), str(RECOVERY): sha(RECOVERY)},
        'windows': windows, 'owned_scientific_worker_identities': identities,
        'cause': 'CREATE_NO_WINDOW is ignored when combined with DETACHED_PROCESS; virtual-environment child opened console.',
        'reference': 'https://learn.microsoft.com/en-us/windows/win32/procthread/process-creation-flags',
        'requested_action': 'hide windows only; no close message, termination, or training restart'})
    for row in windows:
        assert user.ShowWindowAsync(row['handle'], 0), row
    time.sleep(.3)
    assert all(not user.IsWindowVisible(row['handle']) for row in windows)
    for pid, row in identities.items():
        process = psutil.Process(pid)
        assert process.create_time() == row['creation_time'] and process.cmdline() == row['command']
    proof = {'status': 'passed_project_recovery_windows_hidden_with_all_scientific_workers_preserved',
        'at_local': datetime.now().isoformat(timespec='seconds'),
        'hidden_visible_terminal_windows': sum(row['verified_project_terminal'] for row in windows),
        'hidden_pseudoconsole_windows': sum(not row['verified_project_terminal'] for row in windows),
        'scientific_worker_identities_preserved': len(identities),
        'processes_closed_or_restarted': 0, 'training_and_quality_mathematics_changed': False,
        'test_labels_read': False, 'new_model_fits': 0, 'new_quality_scores': 0}
    create(OUT / 'verification.json', proof)
    print(json.dumps(proof, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
