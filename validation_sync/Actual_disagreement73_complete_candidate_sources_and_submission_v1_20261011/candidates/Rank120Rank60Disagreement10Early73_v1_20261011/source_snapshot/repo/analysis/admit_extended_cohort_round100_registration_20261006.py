"""Admit full registration after the existing ranking writer naturally closes."""
from pathlib import Path
import runpy
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, create, sha, owned
from atomic_optimization_observer_writes_20261005 import write


def main():
    import psutil
    out = A / 'extended_cohort_round100_actual_admission_20261006'
    assert not out.exists()
    out.mkdir()
    predecessor = A / 'service_owned_dependency_queue_v4_20261006/activated_jobs/round97'
    identity = read(predecessor / 'launch.json')
    preparation = A / 'extended_cohort_round100_registration_source_preparation_20261006.json'
    expected = read(preparation)['input_sha256']
    expected[str(preparation)] = sha(preparation)
    driver = A / 'run_extended_cohort_round100_full_registration_20261006.py'
    assert str(driver) in expected
    assert not (A / 'optimization_20261003_r100').exists()
    create(out / 'frozen_before_admission_wait.json', {
        'input_sha256': expected, 'predecessor_identity': identity,
        'predecessor_natural_success_and_actual_main_receipt_required': True,
        'minimum_available_RAM_GiB': 8, 'test_labels_read': False,
        'scientific_processes_suspended_or_restarted': 0})
    while True:
        execution = predecessor / 'execution.json'
        provenance = A / 'optimization_20261003_r97/provenance_scope_execution.json'
        receipt = A / 'github_validation_sync_main_20261005/round97_receipt.json'
        closed = not owned(identity)
        done = closed and execution.exists() and read(execution)['status'] == 'passed'
        qualified = done and provenance.exists() and read(provenance)['status'] == 'passed'
        synced = qualified and receipt.exists() and read(receipt)['status'] == 'pushed_and_remote_head_verified'
        available = psutil.virtual_memory().available / 2**30
        write(out / 'waiting_status.json', {
            'status': 'waiting_for_natural_predecessor_closure_and_main_and_memory',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'predecessor_live': not closed, 'predecessor_execution_passed': done,
            'predecessor_provenance_passed': qualified,
            'predecessor_actual_full_main_receipt_present': synced,
            'available_RAM_GiB': available, 'scientific_processes_changed': 0})
        if synced and available >= 8:
            break
        time.sleep(30)
    for path, digest in expected.items():
        assert sha(path) == digest, path
    create(out / 'actual_admission.json', {
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'available_RAM_GiB': available, 'predecessor_execution': read(execution),
        'predecessor_main_receipt': read(receipt), 'driver_sha256': sha(driver),
        'scientific_processes_suspended_or_restarted': 0, 'test_labels_read': False})
    runpy.run_path(str(driver), run_name='__main__')


if __name__ == '__main__':
    main()
