"""Check the service-owned launch root separately from a venv child job."""
from pathlib import Path
import ctypes
from ctypes import wintypes
import hashlib
import json
import time

import psutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'analysis/independent_windows_background_probe_v2_20261006'


def main():
    assert OUT.exists() and not (OUT / 'native_started.json').exists()
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.GetCurrentProcess.restype = wintypes.HANDLE
    kernel.OpenProcess.argtypes = (wintypes.DWORD, wintypes.BOOL, wintypes.DWORD)
    kernel.OpenProcess.restype = wintypes.HANDLE
    kernel.CloseHandle.argtypes = (wintypes.HANDLE,)
    kernel.IsProcessInJob.argtypes = (wintypes.HANDLE, wintypes.HANDLE, ctypes.POINTER(wintypes.BOOL))
    kernel.IsProcessInJob.restype = wintypes.BOOL
    kernel.GetConsoleWindow.restype = wintypes.HWND
    process = psutil.Process()
    parent = process.parent()
    provider = parent.parent()
    child_job, parent_job = wintypes.BOOL(), wintypes.BOOL()
    assert kernel.IsProcessInJob(kernel.GetCurrentProcess(), None, ctypes.byref(child_job))
    handle = kernel.OpenProcess(0x1000, False, parent.pid)
    assert handle
    try:
        assert kernel.IsProcessInJob(handle, None, ctypes.byref(parent_job))
    finally:
        kernel.CloseHandle(handle)
    data = {'pid': process.pid, 'creation_time': process.create_time(), 'parent_pid': parent.pid,
        'parent_name': parent.name(), 'parent_creation_time': parent.create_time(),
        'service_provider_pid': provider.pid, 'service_provider_name': provider.name(),
        'service_provider_creation_time': provider.create_time(),
        'console_handle': int(kernel.GetConsoleWindow() or 0),
        'actual_child_in_job_object': bool(child_job.value),
        'independently_created_root_in_any_job_object': bool(parent_job.value),
        'argv': process.cmdline(), 'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'new_model_fits': 0, 'new_quality_scores': 0}
    with (OUT / 'native_started.json').open('x', encoding='utf-8') as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2)
    assert not parent_job.value and not data['console_handle']
    assert provider.name().lower() == 'wmiprvse.exe'
    with (OUT / 'actual_native_heartbeats.jsonl').open('x', encoding='utf-8') as stream:
        for index in range(40):
            stream.write(json.dumps({'pid': process.pid, 'index': index,
                'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'monotonic': time.monotonic()}) + '\n')
            stream.flush()
            time.sleep(1)
    with (OUT / 'native_completed.json').open('x', encoding='utf-8') as stream:
        json.dump({'status': 'passed_service_owned_root_outside_job_and_consoleless_native40_heartbeats',
            **data, 'completed_at_local': time.strftime('%Y-%m-%dT%H:%M:%S')}, stream, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main()
