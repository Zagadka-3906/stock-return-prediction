"""Reclaim owned idle project pages only between completed full native years."""
from pathlib import Path
import argparse
import ctypes
from ctypes import wintypes
import datetime
import hashlib
import json
import os
import sys
import time

import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
OUT = A / 'neural16384_idle_admission_watch_20261005'
BANK = A / 'neural16384_full_bank_20261005'
MODEL = 'rank16384_drop000_seed07_e32'
RUN = A / 'neural16384_idle_admission_watch_run_20261005.json'
RESERVE = 14 * 2**30
sys.path.insert(0, str(A))
from finalize_main_branch_consolidation_20261005 import owned_pair


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def atomic(path, data):
    path.parent.mkdir(exist_ok=True, parents=True)
    scratch = path.with_name(path.name + f'.{os.getpid()}.tmp')
    scratch.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    os.replace(scratch, path)


def native_pair():
    job = next(row for row in read(A / 'recovery_qualified_workflow_handoff_20261005/verification.json')['jobs']
               if row['label'] == 'neural16384_annual')
    return owned_pair(job['pid'], Path(job['script']), job['script_args'])


def guard(process):
    completed = [year for year in range(2020, 2025) if (BANK / MODEL / f'info_{year}.json').exists()]
    state = {'at_local': datetime.datetime.now().isoformat(), 'pid': process.pid,
             'created': process.create_time(), 'command': process.cmdline(),
             'host_available_bytes': psutil.virtual_memory().available,
             'cpu_seconds': sum(process.cpu_times()[:2]), 'completed_years': completed,
             'eligible_for_idle_reclaim': False}
    if not completed or completed == list(range(2020, 2025)):
        state['reason'] = 'first_fit_or_all_annual_fits_not_an_idle_admission_target'
        return state
    assert completed == list(range(2020, completed[-1] + 1))
    last = completed[-1]
    next_boundary = BANK / f'boundary_control_{MODEL}_{last+1}.json'
    prefix = BANK / f'prefix_control_{MODEL}_{last}.json'
    if next_boundary.exists() or not prefix.exists() or time.time() - prefix.stat().st_mtime < 60:
        state['reason'] = 'next_year_execution_active_or_completed_prefix_control_not_yet_closed'
        return state
    info = read(BANK / MODEL / f'info_{last}.json')
    assert info['status'] == 'passed' and info['configuration']['epochs'] == 32
    assert info['model_reload_bit_identical'] and info['test_data_read'] is False
    assert read(prefix)['actual_saved_model_cold80_day_prefix_bit_identical']
    rows = [json.loads(line) for line in (BANK / 'actual_native_fit_measurements.jsonl').read_bytes().splitlines()]
    full = [row for row in rows if row['requested_epochs'] == 32]
    assert len(full) == len(completed)
    assert {row['context']['year'] for row in full} == set(completed)
    assert all(row['status'] == 'completed_original_requested_epochs' and row['completed_epochs'] == 32
               and row['parameter_count'] == 168894465 for row in full)
    state['native_fit_records'] = len(rows)
    if state['host_available_bytes'] >= RESERVE:
        state['reason'] = 'original14GiB_admission_condition_already_satisfied'
        return state
    state['eligible_for_idle_reclaim'] = True
    state['reason'] = 'actual_completed_year_and_cold_prefix_waiting_for_original14GiB_admission'
    return state


def trim(process):
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    kernel.OpenProcess.restype = wintypes.HANDLE
    kernel.K32EmptyWorkingSet.argtypes = [wintypes.HANDLE]
    kernel.K32EmptyWorkingSet.restype = wintypes.BOOL
    kernel.CloseHandle.argtypes = [wintypes.HANDLE]
    kernel.CloseHandle.restype = wintypes.BOOL
    before = {'pid': process.pid, 'created': process.create_time(), 'command': process.cmdline(),
              'rss': process.memory_info().rss, 'available': psutil.virtual_memory().available}
    handle = kernel.OpenProcess(0x1000 | 0x0100, False, process.pid)
    if not handle:
        raise ctypes.WinError(ctypes.get_last_error())
    try:
        if not kernel.K32EmptyWorkingSet(handle):
            raise ctypes.WinError(ctypes.get_last_error())
        return {'before': before, 'after_rss': process.memory_info().rss,
                'after_available': psutil.virtual_memory().available, 'API_succeeded': True}
    finally:
        kernel.CloseHandle(handle)


def actual_idle_reclaim(native, before):
    time.sleep(30)
    after = guard(native)
    if not after['eligible_for_idle_reclaim'] or after['completed_years'] != before['completed_years']:
        return {'status': 'skipped_admission_state_changed', 'before': before, 'after': after}
    assert after['created'] == before['created'] and after['command'] == before['command']
    if after['cpu_seconds'] - before['cpu_seconds'] >= 2:
        return {'status': 'skipped_native_CPU_activity', 'before': before, 'after': after}
    targets = {native.pid: native}
    jobs = [row for row in read(A / 'resumed_rounds_nystrom_locked_20261004.json') if row['round'] >= 67]
    jobs.append(read(A / 'neural16384_full_followup_launch_receipt_20261005.json')['future'])
    for filename in ('gradient_sampling_followups_20261005/verification.json',
                     'memory_efficient_neural_followups_20261005/verification.json',
                     'memory_efficient_mlp_gpu_recovery_v2_20261005/verification.json'):
        jobs.extend(row for row in read(A / filename).values()
                    if isinstance(row, dict) and 'pid' in row and 'script' in row)
    for job in jobs:
        if 'round' in job:
            state = read(A / f"ongoing_optimization_r{job['round']}_state.json")
            if state['status'] != 'running' or not state['stage'].startswith('waiting_for_'):
                continue
        try:
            _, child = owned_pair(job['pid'], Path(job['script']), job.get('script_args', []))
            targets[child.pid] = child
        except psutil.NoSuchProcess:
            continue
    publisher = psutil.Process(read(A / 'github_validation_sync_main_20261005/owner.lock')['pid'])
    _, child = owned_pair(publisher.parent().pid, A / 'watch_validations_main_v3_20261005.py')
    targets[child.pid] = child
    monitor = read(A / 'actual_optimization_monitor_launch_v13_20261005.json')
    _, child = owned_pair(monitor['pid'], Path(monitor['script']), monitor['script_args'])
    targets[child.pid] = child
    # While this native job is between years, every other model job still requires
    # its full annual/final closure. Check that those gates have not been replaced.
    assert not (BANK / 'training_execution_scope.json').exists()
    assert not (A / 'gradient_sampling_bank_20261005/protocol.json').exists()
    assert not (A / 'memory_efficient_mlp_gpu_controls_20261005/protocol.json').exists()
    records = []
    for process in targets.values():
        records.append(trim(process))
    return {'status': 'actual_owned_idle_reclaim_completed', 'before': before, 'after30seconds': after,
            'actions': records, 'original14GiB_admission_and_all32epoch_fits_preserved': True,
            'no_process_termination_or_restart': True, 'test_labels_read': False, 'new_quality_scores': 0}


def main(once=False):
    run = read(RUN)
    bindings = run['input_sha256']
    acted_years = set()
    while True:
        for filename, value in bindings.items():
            assert hashlib.sha256(Path(filename).read_bytes()).hexdigest() == value, filename
        try:
            _, native = native_pair()
        except psutil.NoSuchProcess:
            atomic(OUT / 'state.json', {'status': 'original_native_process_terminal_or_missing',
                'at_local': datetime.datetime.now().isoformat(), 'training_not_restarted': True})
            return
        state = guard(native)
        state['status'] = 'observing_original_native_admission'
        if once:
            atomic(OUT / 'actual_guard_preflight.json', state)
            assert not state['eligible_for_idle_reclaim'], 'Do not execute a reclaim in the preflight.'
            print(json.dumps(state, ensure_ascii=False), flush=True)
            return
        last = state['completed_years'][-1] if state['completed_years'] else None
        if state['eligible_for_idle_reclaim'] and last not in acted_years:
            result = actual_idle_reclaim(native, state)
            stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            with (OUT / f'actual_action_{stamp}.json').open('x', encoding='utf-8') as stream:
                json.dump(result, stream, ensure_ascii=False, indent=2)
                stream.write('\n')
            if result['status'] == 'actual_owned_idle_reclaim_completed':
                acted_years.add(last)
        state['reclaimed_after_completed_years'] = sorted(acted_years)
        atomic(OUT / 'state.json', state)
        time.sleep(30)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--once', action='store_true')
    main(parser.parse_args().once)
