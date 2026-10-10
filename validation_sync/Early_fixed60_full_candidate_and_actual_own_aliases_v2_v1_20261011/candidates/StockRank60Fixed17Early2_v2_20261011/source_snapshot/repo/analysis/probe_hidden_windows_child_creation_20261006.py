"""Check real subprocess and multiprocessing children have no console window."""
from pathlib import Path
import ctypes
import hashlib
import json
import multiprocessing
import os
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'


def console():
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.GetConsoleWindow.restype = ctypes.c_void_p
    return kernel.GetConsoleWindow() or 0


def spawn_child(connection):
    connection.send({'pid': os.getpid(), 'console_handle': console()})
    connection.close()


def main():
    from hidden_windows_child_creation_20261006 import install
    out = A / 'hidden_windows_child_creation_preflight_20261006'
    assert not out.exists()
    out.mkdir()
    inputs = {str(p): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in (Path(__file__).resolve(), A / 'hidden_windows_child_creation_20261006.py')}
    with (out / 'frozen_before_actual_children.json').open('x', encoding='utf-8') as stream:
        json.dump({'input_sha256': inputs, 'no_training_or_scoring_by_control': True}, stream, indent=2)
    scratch = ROOT / 'tmp/hidden_child_creation_preflight_20261006'
    scratch.mkdir(parents=True, exist_ok=True)
    for name in ('TMP', 'TEMP', 'TMPDIR'):
        os.environ[name] = str(scratch)
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
    restore = install()
    failure, checks = None, []
    try:
        code = 'import ctypes,json,os; k=ctypes.WinDLL("kernel32"); k.GetConsoleWindow.restype=ctypes.c_void_p; print(json.dumps({"pid":os.getpid(),"console_handle":k.GetConsoleWindow() or 0}))'
        result = subprocess.run([sys.executable, '-B', '-X', 'utf8', '-c', code],
            capture_output=True, text=True, encoding='utf-8', check=True, timeout=20)
        actual = json.loads(result.stdout)
        assert actual['console_handle'] == 0
        checks.append({'kind': 'actual_stdlib_subprocess_default_flags', **actual})
        context = multiprocessing.get_context('spawn')
        receive, send = context.Pipe(duplex=False)
        process = context.Process(target=spawn_child, args=(send,))
        process.start()
        send.close()
        try:
            assert receive.poll(20), 'Real spawned child did not send its actual console handle.'
            actual = receive.recv()
            process.join(20)
            assert process.exitcode == 0 and actual['console_handle'] == 0
            checks.append({'kind': 'actual_multiprocessing_spawn_default_flags', **actual})
        finally:
            receive.close()
            if process.is_alive():
                process.terminate()
                process.join(10)
        assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest() == d for p, d in inputs.items())
    except BaseException as error:
        failure = f'{type(error).__name__}: {error}'
        raise
    finally:
        events = restore()
        proof = {'status': 'passed_actual_subprocess_and_multiprocessing_consoleless_children' if failure is None else 'failed_preserved_actual_hidden_child_preflight',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'failure': failure,
            'checks': checks, 'actual_CreateProcess_calls': events, 'original_CreateProcess_restored': True,
            'input_sha256': inputs, 'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False}
        with (out / 'verification.json').open('x', encoding='utf-8') as stream:
            json.dump(proof, stream, ensure_ascii=False, indent=2)
            stream.write('\n')
        print(json.dumps(proof, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
