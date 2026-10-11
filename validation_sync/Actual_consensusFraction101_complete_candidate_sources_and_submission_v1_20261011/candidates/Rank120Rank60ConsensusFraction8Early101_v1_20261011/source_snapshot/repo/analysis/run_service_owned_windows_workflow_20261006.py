"""Run a pinned workflow from a consoleless, service-owned venv launch root."""
from pathlib import Path
import ctypes
from ctypes import wintypes
import hashlib
import json
import os
import runpy
import sys
import time

import psutil

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def create(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    definition = Path(sys.argv[1]).resolve()
    run = json.loads(definition.read_text(encoding='utf-8-sig'))
    assert definition.is_relative_to(ROOT / 'analysis') and definition.drive.upper() == 'D:'
    output = definition.parent
    for filename, digest in run['input_sha256'].items():
        assert sha(filename) == digest, filename
    assert run['bootstrap_sha256'] == sha(__file__)
    scratch = Path(run['scratch']).resolve()
    assert scratch.drive.upper() in ('D:', 'E:')
    scratch.mkdir(parents=True, exist_ok=True)
    for key in ('TMP', 'TEMP', 'TMPDIR'):
        os.environ[key] = str(scratch)
    os.environ.update(PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1',
        OMP_NUM_THREADS='8', OPENBLAS_NUM_THREADS='8', MKL_NUM_THREADS='8', POLARS_MAX_THREADS='8')
    import tempfile
    tempfile.tempdir = str(scratch)
    process, kernel = psutil.Process(), ctypes.WinDLL('kernel32', use_last_error=True)
    parent, provider = process.parent(), process.parent().parent()
    kernel.OpenProcess.argtypes = (wintypes.DWORD, wintypes.BOOL, wintypes.DWORD)
    kernel.OpenProcess.restype = wintypes.HANDLE
    kernel.CloseHandle.argtypes = (wintypes.HANDLE,)
    kernel.IsProcessInJob.argtypes = (wintypes.HANDLE, wintypes.HANDLE, ctypes.POINTER(wintypes.BOOL))
    kernel.IsProcessInJob.restype = wintypes.BOOL
    kernel.GetConsoleWindow.restype = wintypes.HWND
    handle, attached = kernel.OpenProcess(0x1000, False, parent.pid), wintypes.BOOL()
    assert handle
    try:
        assert kernel.IsProcessInJob(handle, None, ctypes.byref(attached))
    finally:
        kernel.CloseHandle(handle)
    assert not attached.value and not kernel.GetConsoleWindow()
    assert provider.name().lower() == 'wmiprvse.exe'
    create(output / 'native_launch.json', {'name': run['name'], 'pid': parent.pid,
        'script': str(Path(__file__).resolve()), 'script_args': [str(definition)],
        'owned_worker_pid': process.pid, 'owned_worker_creation_time': process.create_time(),
        'owned_parent_creation_time': parent.create_time(),
        'service_provider_pid': provider.pid, 'service_provider_creation_time': provider.create_time(),
        'service_provider_name': provider.name(), 'independent_launch_root_in_any_job': False,
        'actual_native_console_handle': 0, 'original_driver': run['driver'],
        'original_arguments': run['arguments'], 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'stdout': str(output / 'stdout.log'), 'stderr': str(output / 'stderr.log')})
    failure = None
    with (output / 'stdout.log').open('x', encoding='utf-8', buffering=1) as stdout, (output / 'stderr.log').open('x', encoding='utf-8', buffering=1) as stderr:
        old_stdout, old_stderr, old_argv = sys.stdout, sys.stderr, sys.argv
        try:
            sys.stdout, sys.stderr, sys.argv = stdout, stderr, [run['driver'], *run['arguments']]
            print(json.dumps({'status': 'service_owned_consoleless_workflow_started', 'name': run['name'],
                'original_driver': run['driver'], 'root_outside_job': True, 'scratch': str(scratch)}), flush=True)
            runpy.run_path(run['driver'], run_name='__main__')
            for filename, digest in run['input_sha256'].items():
                assert sha(filename) == digest, filename
        except BaseException as error:
            failure = f'{type(error).__name__}: {error}'
            __import__('traceback').print_exc(file=stderr)
            raise
        finally:
            sys.stdout, sys.stderr, sys.argv = old_stdout, old_stderr, old_argv
            create(output / 'service_execution.json', {'status': 'passed' if failure is None else 'failed',
                'failure': failure, 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
                'definition_sha256': sha(definition), 'sources_and_native_mathematics_unchanged': True})


if __name__ == '__main__':
    main()
