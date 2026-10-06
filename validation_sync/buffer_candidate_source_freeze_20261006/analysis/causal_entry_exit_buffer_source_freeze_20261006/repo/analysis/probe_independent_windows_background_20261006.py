"""Observe a service-created consoleless process after its command session exits."""
from pathlib import Path
import ctypes
from ctypes import wintypes
import hashlib
import json
import os
import time

import psutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'analysis/independent_windows_background_probe_20261006'


def main():
    assert OUT.exists() and not (OUT / 'native_started.json').exists()
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.GetCurrentProcess.restype = wintypes.HANDLE
    kernel.IsProcessInJob.argtypes = (wintypes.HANDLE, wintypes.HANDLE, ctypes.POINTER(wintypes.BOOL))
    kernel.IsProcessInJob.restype = wintypes.BOOL
    kernel.GetConsoleWindow.restype = wintypes.HWND
    attached = wintypes.BOOL()
    assert kernel.IsProcessInJob(kernel.GetCurrentProcess(), None, ctypes.byref(attached))
    process = psutil.Process()
    parent = process.parent()
    data = {'pid': process.pid, 'creation_time': process.create_time(), 'parent_pid': parent.pid,
        'parent_name': parent.name(), 'parent_creation_time': parent.create_time(),
        'console_handle': kernel.GetConsoleWindow(), 'in_any_job_object': bool(attached.value),
        'argv': process.cmdline(), 'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'new_model_fits': 0, 'new_quality_scores': 0}
    with (OUT / 'native_started.json').open('x', encoding='utf-8') as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2)
    assert not attached.value and not data['console_handle']
    with (OUT / 'actual_native_heartbeats.jsonl').open('x', encoding='utf-8') as stream:
        for index in range(40):
            stream.write(json.dumps({'pid': process.pid, 'index': index,
                'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'monotonic': time.monotonic()}) + '\n')
            stream.flush()
            time.sleep(1)
    with (OUT / 'native_completed.json').open('x', encoding='utf-8') as stream:
        json.dump({'status': 'passed_consoleless_non_job_native_process40_actual_heartbeats',
            **data, 'completed_at_local': time.strftime('%Y-%m-%dT%H:%M:%S')}, stream, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main()
