"""Try reclaiming only verified idle project waiters; retain all process identities."""
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
OUT = A / 'owned_waiter_memory_reclaim_20261005'
sys.path.insert(0, str(A))
from resume_idle_neural16384_memory_admission_20261005 import read, observation, BANK, MODEL, RESERVE


def save(name, data):
    OUT.mkdir(exist_ok=True)
    with (OUT / name).open('x', encoding='utf-8') as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    assert not OUT.exists()
    sources = [Path(__file__), A / 'resume_idle_neural16384_memory_admission_20261005.py',
               A / 'resumed_rounds_nystrom_locked_20261004.json',
               A / 'neural16384_full_followup_launch_receipt_20261005.json',
               A / 'gradient_sampling_followups_20261005/verification.json',
               A / 'memory_efficient_neural_followups_20261005/verification.json',
               A / 'memory_efficient_mlp_gpu_recovery_v2_20261005/verification.json']
    jobs = [row for row in read(sources[2]) if row['round'] >= 67]
    for job in jobs:
        state = read(A / f"ongoing_optimization_r{job['round']}_state.json")
        assert state['status'] == 'running' and state['stage'].startswith('waiting_for_')
        assert not (ROOT / f"results/optimization_20261003_r{job['round']}.json").exists()
    jobs.append(read(sources[3])['future'])
    goss = read(sources[4])
    memory = read(sources[5])
    # Resolve real registry field names rather than inferring them from filenames.
    for document in (goss, memory, read(sources[6])):
        jobs.extend(row for key, row in document.items()
                    if isinstance(row, dict) and 'pid' in row and 'script' in row and key not in ('monitor',))
    assert not (A / 'gradient_sampling_bank_20261005/protocol.json').exists()
    assert not (A / 'memory_efficient_mlp_gpu_controls_20261005/protocol.json').exists()
    assert not (BANK / 'training_execution_scope.json').exists()
    pairs = {}
    for job in jobs:
        parent = psutil.Process(job['pid'])
        command = parent.cmdline()
        assert job['script'] in command
        args = job.get('script_args', [])
        if args:
            assert command[-len(args):] == args
        children = [p for p in parent.children(recursive=True)
                    if p.name().lower() == 'python.exe' and p.cmdline()[1:] == command[1:]]
        assert len(children) == 1
        child = children[0]
        assert child.pid != 32148, 'Do not reclaim the native trainer twice.'
        pairs[child.pid] = (parent, child)
    def snapshot(process):
        return {'pid': process.pid, 'parent': process.ppid(), 'created': process.create_time(),
                'command': process.cmdline(), 'cpu_seconds': sum(process.cpu_times()[:2]),
                'rss_bytes': process.memory_info().rss, 'status': process.status()}
    first = {pid: snapshot(child) for pid, (_, child) in pairs.items()}
    time.sleep(20)
    second = {pid: snapshot(child) for pid, (_, child) in pairs.items()}
    for pid in pairs:
        assert first[pid]['created'] == second[pid]['created']
        assert first[pid]['command'] == second[pid]['command']
        assert second[pid]['cpu_seconds'] - first[pid]['cpu_seconds'] < 5.
    native = psutil.Process(32148)
    before_native = observation(native)
    assert before_native['host_available_bytes'] < RESERVE
    assert not before_native['next_boundary_exists'] and before_native['native_fit_record_count'] == 3
    hashes = {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in sources}
    save('frozen_before_action.json', {'status': 'frozen_before_owned_idle_waiter_working_set_reclaim',
        'observations_before': first, 'observations_after20seconds': second,
        'original_native_before': before_native, 'input_sha256': hashes,
        'excludes_original_native_trainer_and_GitHub_publisher_and_progress_monitor': True,
        'API': 'K32EmptyWorkingSet', 'scientific_files_and_admission_policies_preserved': True,
        'test_labels_read': False, 'new_quality_scores': 0})
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    kernel.OpenProcess.restype = wintypes.HANDLE
    kernel.K32EmptyWorkingSet.argtypes = [wintypes.HANDLE]
    kernel.K32EmptyWorkingSet.restype = wintypes.BOOL
    kernel.CloseHandle.argtypes = [wintypes.HANDLE]
    kernel.CloseHandle.restype = wintypes.BOOL
    results = []
    for pid, (_, child) in pairs.items():
        # Recheck immediately; never terminate or restart a process for this action.
        current = snapshot(child)
        assert current['created'] == first[pid]['created'] and current['command'] == first[pid]['command']
        handle = kernel.OpenProcess(0x1000 | 0x0100, False, pid)
        if not handle:
            raise ctypes.WinError(ctypes.get_last_error())
        try:
            if not kernel.K32EmptyWorkingSet(handle):
                raise ctypes.WinError(ctypes.get_last_error())
            results.append({'before': current, 'after': snapshot(child), 'API_succeeded': True})
        finally:
            kernel.CloseHandle(handle)
    save('actual_actions.json', {'status': 'all_owned_idle_waiter_API_calls_returned_success', 'actions': results})
    samples = []
    deadline = time.monotonic() + 120
    while time.monotonic() < deadline:
        row = observation(native)
        samples.append(row)
        if row['next_boundary_exists'] or row['native_fit_record_count'] > 3:
            break
        time.sleep(5)
    assert all(hashlib.sha256(Path(path).read_bytes()).hexdigest() == expected for path, expected in hashes.items())
    started = samples[-1]['next_boundary_exists'] or samples[-1]['native_fit_record_count'] > 3
    proof = {'status': 'passed_actual_owned_waiter_reclaim_with_original_next_year_execution_started' if started
             else 'passed_actual_owned_waiter_reclaim_original_admission_still_pending',
             'at_local': datetime.datetime.now().isoformat(), 'actual_waiter_count': len(pairs),
             'next_year_execution_started': started, 'original_native_observations_after': samples,
             'input_sha256': hashes, 'all_process_identities_retained': True,
             'reserve14GiB_preserved': True, 'new_quality_scores': 0, 'test_labels_read': False}
    save('verification.json', proof)
    print(json.dumps({k: v for k, v in proof.items() if k not in
                      ('original_native_observations_after', 'input_sha256')}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
