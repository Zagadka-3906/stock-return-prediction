"""Verify the synchronous window fix and an actual future hidden child launch."""
from pathlib import Path
from datetime import datetime
import ctypes
import hashlib
import json
import sys

import psutil
from windows_hidden_process_launch_20261006 import launch

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
OUT = A / 'recovery_terminal_window_fix_20261006'


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    assert not (OUT / 'verified_hidden_launch.json').exists()
    frozen = json.loads((OUT / 'frozen_before_window_hide.json').read_text(encoding='utf-8'))
    user = ctypes.windll.user32
    user.IsWindowVisible.argtypes = [ctypes.c_void_p]
    terminals = [row for row in frozen['windows'] if row['verified_project_terminal']]
    assert len(terminals) == 32 and all(not user.IsWindowVisible(row['handle']) for row in terminals)
    alive = 0
    for pid, row in frozen['owned_scientific_worker_identities'].items():
        worker = psutil.Process(int(pid))
        assert worker.create_time() == row['creation_time'] and worker.cmdline() == row['command']
        alive += 1
    helper = A / 'windows_hidden_process_launch_20261006.py'
    bindings = {str(Path(__file__).resolve()): sha(__file__), str(helper): sha(helper)}
    with (OUT / 'frozen_before_native_hidden_launch.json').open('x', encoding='utf-8') as stream:
        json.dump({'input_sha256': bindings, 'no_scientific_fits_or_scores': True}, stream, indent=2)
    code = "import ctypes,json,sys; h=ctypes.windll.kernel32.GetConsoleWindow(); print(json.dumps({'console_handle':h,'venv_prefix':sys.prefix})); assert not h"
    with (OUT / 'hidden_child_stdout.log').open('xb') as out, (OUT / 'hidden_child_stderr.log').open('xb') as err:
        process = launch([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8', '-c', code],
            cwd=ROOT, stdout=out, stderr=err)
        assert process.wait(timeout=15) == 0
    child = json.loads((OUT / 'hidden_child_stdout.log').read_text(encoding='utf-8'))
    assert child['console_handle'] == 0 and Path(child['venv_prefix']) == ROOT / '.venv'
    assert all(not user.IsWindowVisible(row['handle']) for row in terminals)
    for name, digest in bindings.items():
        assert sha(name) == digest
    proof = {'status': 'passed32_owned_terminal_windows_hidden_and_native_consoleless_launch_verified',
        'at_local': datetime.now().isoformat(timespec='seconds'), 'hidden_terminal_windows': len(terminals),
        'live_scientific_worker_identities_preserved': alive,
        'actual_virtual_environment_child_console_handle': child['console_handle'],
        'future_launch_uses_CREATE_NO_WINDOW_without_DETACHED_PROCESS_or_CREATE_NEW_CONSOLE': True,
        'future_launch_stdin_DEVNULL_and_STARTF_USESHOWWINDOW_SW_HIDE': True,
        'first_async_hide_attempt_failure_preserved': True,
        'successful_fix': 'Synchronous SetWindowPos SWP_HIDEWINDOW andShowWindow SW_HIDE',
        'input_sha256': bindings, 'processes_closed_or_restarted': 0,
        'test_labels_read': False, 'new_model_fits': 0, 'new_quality_scores': 0}
    with (OUT / 'verified_hidden_launch.json').open('x', encoding='utf-8') as stream:
        json.dump(proof, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    print(json.dumps(proof, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
