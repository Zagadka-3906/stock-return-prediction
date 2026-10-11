"""Reclaim idle owned observer working sets and verify actual native continuation."""
from pathlib import Path
import ctypes
from ctypes import wintypes
import datetime
import hashlib
import json
import sys
import time

import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
OUT = A / 'operational_observer_memory_reclaim_20261005'
sys.path.insert(0, str(A))
from resume_idle_neural16384_memory_admission_20261005 import read, observation, RESERVE
from finalize_main_branch_consolidation_20261005 import owned_pair


def save(name, value):
    OUT.mkdir(exist_ok=True)
    with (OUT / name).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    assert not OUT.exists()
    publisher = psutil.Process(read(A / 'github_validation_sync_main_20261005/owner.lock')['pid'])
    publisher_pair = owned_pair(publisher.parent().pid, A / 'watch_validations_main_v3_20261005.py')
    assert publisher_pair[1].pid == publisher.pid
    job = read(A / 'actual_optimization_monitor_launch_v13_20261005.json')
    monitor_pair = owned_pair(job['pid'], Path(job['script']), job['script_args'])
    native = psutil.Process(32148)
    before_native = observation(native)
    assert not before_native['next_boundary_exists'] and before_native['native_fit_record_count'] == 3
    sources = [Path(__file__), A / 'resume_idle_neural16384_memory_admission_20261005.py',
               A / 'finalize_main_branch_consolidation_20261005.py',
               A / 'actual_optimization_monitor_launch_v13_20261005.json',
               A / 'neural16384_idle_memory_admission_20261005/verification.json']
    hashes = {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in sources}
    save('frozen_before_action.json', {'status': 'frozen_before_owned_observer_reclaim',
        'original_native_before': before_native, 'input_sha256': hashes,
        'target_owned_children': [child.pid for _, child in (publisher_pair, monitor_pair)],
        'API': 'K32EmptyWorkingSet', 'native_model_parameters_and_reserve_unchanged': True,
        'no_process_termination_or_restart': True, 'test_labels_read': False, 'new_quality_scores': 0})
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    kernel.OpenProcess.restype = wintypes.HANDLE
    kernel.K32EmptyWorkingSet.argtypes = [wintypes.HANDLE]
    kernel.K32EmptyWorkingSet.restype = wintypes.BOOL
    kernel.CloseHandle.argtypes = [wintypes.HANDLE]
    kernel.CloseHandle.restype = wintypes.BOOL
    actions, suspended = [], []
    try:
        for parent, child in (publisher_pair, monitor_pair):
            child.suspend()
            suspended.append(child)
            parent.suspend()
            suspended.append(parent)
            assert all(p.pid == child.pid or p.name().lower() == 'conhost.exe'
                       for p in parent.children(recursive=True)), 'Observer currently owns an active command.'
            before = {'pid': child.pid, 'created': child.create_time(), 'command': child.cmdline(),
                      'rss': child.memory_info().rss, 'available': psutil.virtual_memory().available}
            handle = kernel.OpenProcess(0x1000 | 0x0100, False, child.pid)
            if not handle:
                raise ctypes.WinError(ctypes.get_last_error())
            try:
                if not kernel.K32EmptyWorkingSet(handle):
                    raise ctypes.WinError(ctypes.get_last_error())
                actions.append({'before': before, 'after_rss': child.memory_info().rss,
                                'after_available': psutil.virtual_memory().available, 'API_succeeded': True})
            finally:
                kernel.CloseHandle(handle)
        save('actual_actions.json', {'status': 'both_owned_idle_observer_reclaims_succeeded', 'actions': actions})
    finally:
        for process in reversed(suspended):
            if process.is_running():
                process.resume()
    samples = []
    deadline = time.monotonic() + 120
    while time.monotonic() < deadline:
        row = observation(native)
        samples.append(row)
        if row['next_boundary_exists'] or row['native_fit_record_count'] > 3:
            break
        time.sleep(5)
    assert all(hashlib.sha256(Path(path).read_bytes()).hexdigest() == value for path, value in hashes.items())
    started = samples[-1]['next_boundary_exists'] or samples[-1]['native_fit_record_count'] > 3
    proof = {'status': 'passed_actual_observer_reclaim_and_original_next_year_execution_started' if started
             else 'passed_actual_observer_reclaim_original_admission_still_pending',
             'at_local': datetime.datetime.now().isoformat(), 'next_year_execution_started': started,
             'actual_native_observations_after': samples, 'input_sha256': hashes,
             'both_owned_observers_resumed': all(child.status() != psutil.STATUS_STOPPED
                                               for _, child in (publisher_pair, monitor_pair)),
             'reserve14GiB_not_changed': True, 'original_native_not_restarted': True,
             'test_labels_read': False, 'new_quality_scores': 0}
    save('verification.json', proof)
    print(json.dumps({k: v for k, v in proof.items() if k not in
                      ('actual_native_observations_after', 'input_sha256')}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
