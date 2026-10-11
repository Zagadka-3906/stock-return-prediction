"""Reclaim one positively owned idle working set without changing frozen training."""
from pathlib import Path
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
OUT = A / 'neural16384_idle_memory_admission_20261005'
BANK = A / 'neural16384_full_bank_20261005'
MODEL = 'rank16384_drop000_seed07_e32'
RESERVE = 14 * 2**30


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def save(name, value):
    OUT.mkdir(exist_ok=True)
    with (OUT / name).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def observation(process):
    return {'at_local': datetime.datetime.now().isoformat(), 'pid': process.pid,
            'created': process.create_time(), 'command': process.cmdline(),
            'status': process.status(), 'cpu_seconds': sum(process.cpu_times()[:2]),
            'rss_bytes': process.memory_info().rss,
            'host_available_bytes': psutil.virtual_memory().available,
            'next_boundary_exists': (BANK / f'boundary_control_{MODEL}_2021.json').exists(),
            'native_fit_record_count': len((BANK / 'actual_native_fit_measurements.jsonl').read_bytes().splitlines())}


def main():
    assert os.name == 'nt'
    assert not (OUT / 'frozen_before_action.json').exists(), 'Preserve the existing attempt.'
    job = next(row for row in read(A / 'recovery_qualified_workflow_handoff_20261005/verification.json')['jobs']
               if row['label'] == 'neural16384_annual')
    parent = psutil.Process(job['pid'])
    assert parent.cmdline()[4:] == [job['script'], *job['script_args']]
    children = [p for p in parent.children(recursive=True)
                if p.name().lower() == 'python.exe' and p.cmdline()[1:] == parent.cmdline()[1:]]
    assert len(children) == 1
    process = children[0]
    info_path = BANK / MODEL / 'info_2020.json'
    info = read(info_path)
    assert info['status'] == 'passed' and info['configuration']['epochs'] == 32
    assert info['configuration']['hidden'] == [16384, 8192, 4096]
    assert info['model_reload_bit_identical'] and info['test_data_read'] is False
    prefix = BANK / f'prefix_control_{MODEL}_2020.json'
    assert read(prefix)['actual_saved_model_cold80_day_prefix_bit_identical']
    assert read(BANK / f'boundary_control_{MODEL}_2020.json')['boundary_future_label_poisoning_bit_identical']
    assert digest(BANK / MODEL / 'model_2020.joblib') == info['model_sha256']
    assert digest(BANK / MODEL / 'raw_2020.parquet') == info['prediction_sha256']
    first = observation(process)
    time.sleep(30)
    second = observation(process)
    assert first['created'] == second['created'] and first['command'] == second['command']
    assert second['cpu_seconds'] - first['cpu_seconds'] < 2., 'Actual fit may be running.'
    assert all(row['host_available_bytes'] < RESERVE and not row['next_boundary_exists']
               and row['native_fit_record_count'] == 3 for row in (first, second))
    inputs = [Path(__file__), BANK / 'protocol.json', info_path, prefix,
              BANK / f'boundary_control_{MODEL}_2020.json',
              A / 'run_neural16384_full_bank_20261005.py',
              A / 'train_neural16384_full_bank_20261005.py',
              A / 'train_diverse_backbones_20261003.py',
              A / 'neural16384_actual_resource_recorder_20261005.py',
              ROOT / '后续选模标准.md']
    hashes = {str(path): digest(path) for path in inputs}
    save('frozen_before_action.json', {
        'status': 'frozen_after_actual32_epoch2020_fit_and_idle14GiB_admission_wait',
        'observations': [first, second], 'input_sha256': hashes,
        'actual_completed_annual_fits': 1, 'remaining_full_annual_fits': 4,
        'API': 'K32EmptyWorkingSet', 'one_owned_idle_process_only': True,
        'official_API_documentation': 'https://learn.microsoft.com/en-us/windows/win32/api/psapi/nf-psapi-emptyworkingset',
        'official_working_set_documentation': 'https://learn.microsoft.com/en-us/windows/win32/memory/working-set',
        'scientific_files_parameters_and14GiB_reserve_not_changed': True,
        'working_set_reclaim_is_not_a_physical_capacity_boundary_or_a_score': True,
        'test_labels_read': False, 'new_quality_scores': 0})
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    kernel.OpenProcess.restype = wintypes.HANDLE
    kernel.K32EmptyWorkingSet.argtypes = [wintypes.HANDLE]
    kernel.K32EmptyWorkingSet.restype = wintypes.BOOL
    kernel.CloseHandle.argtypes = [wintypes.HANDLE]
    kernel.CloseHandle.restype = wintypes.BOOL
    handle = kernel.OpenProcess(0x1000 | 0x0100, False, process.pid)
    if not handle:
        raise ctypes.WinError(ctypes.get_last_error())
    suspended = False
    try:
        process.suspend()
        suspended = True
        before_action = observation(process)
        assert before_action['created'] == first['created']
        assert before_action['command'] == first['command']
        assert not before_action['next_boundary_exists'] and before_action['native_fit_record_count'] == 3
        assert before_action['host_available_bytes'] < RESERVE
        if not kernel.K32EmptyWorkingSet(handle):
            raise ctypes.WinError(ctypes.get_last_error())
        after_action = observation(process)
        save('actual_action.json', {'status': 'owned_idle_working_set_reclaim_returned_success',
                                   'before': before_action, 'after': after_action,
                                   'native_process_identity_retained': True})
    finally:
        if suspended and process.is_running():
            process.resume()
        kernel.CloseHandle(handle)
    samples = []
    deadline = time.monotonic() + 120
    while time.monotonic() < deadline:
        row = observation(process)
        samples.append(row)
        log = Path(job['stdout']).read_text(encoding='utf-8')
        if 'fold2021: fitting' in log or row['native_fit_record_count'] > 3:
            break
        time.sleep(5)
    assert all(digest(path) == value for path, value in hashes.items())
    started = 'fold2021: fitting' in Path(job['stdout']).read_text(encoding='utf-8') or samples[-1]['native_fit_record_count'] > 3
    proof = {'status': 'passed_owned_reclaim_and_actual_next_year_execution_started' if started
             else 'passed_owned_reclaim_next_year_execution_still_pending',
             'at_local': datetime.datetime.now().isoformat(), 'process_observations_after_action': samples,
             'next_year_execution_started': started, 'frozen_input_sha256_reverified': hashes,
             'native_full_completed_annual_fits': 1, 'all5_annual_and1_final_gate_remains_required': True,
             'original_process_not_restarted': True, 'reserve14GiB_not_changed': True,
             'test_labels_read': False, 'new_quality_scores': 0}
    save('verification.json', proof)
    print(json.dumps({k: v for k, v in proof.items() if k not in
                      ('process_observations_after_action', 'frozen_input_sha256_reverified')}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
