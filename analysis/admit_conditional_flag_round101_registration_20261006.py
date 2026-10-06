"""Serialize actual37 full registration after full100 and its phase publisher."""
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
    out = A / 'conditional_flag_round101_actual_admission_20261006'
    assert not out.exists()
    out.mkdir()
    prep = A / 'conditional_flag_round101_registration_source_preparation_20261006.json'
    expected = read(prep)['input_sha256']
    expected[str(prep)] = sha(prep)
    driver = A / 'run_conditional_flag_round101_full_registration_20261006.py'
    services = {name: A / 'service_owned_workflows_20261006' / name for name in (
        'extended_cohort_round100_full_registration', 'conditional_flag_rank_official_evidence_publication',
        'conditional_flag_rank_candidate_sealing')}
    identities = {name: read(folder / 'native_launch.json') for name, folder in services.items()}
    receipt100 = A / 'github_validation_sync_main_20261005/round100_receipt.json'
    receipt37 = A / 'conditional_flag_rank_official_comparison_github_20261006/receipt.json'
    seal = A / 'conditional_flag_rank_release_20261006/source_package_verification.json'
    create(out / 'frozen_before_admission_wait.json', {
        'input_sha256': expected, 'preceding_service_identities': identities,
        'actual_full100_main_and_completed37_phase_publication_and_native14_seal_required': True,
        'only_branch': 'main', 'minimum_available_RAM_GiB': 8,
        'scientific_processes_suspended_or_restarted': 0, 'test_labels_read': False})
    while True:
        closed = {name: not owned(row) for name, row in identities.items()}
        passed = all(closed.values()) and all((folder / 'service_execution.json').exists()
            and read(folder / 'service_execution.json')['status'] == 'passed' for folder in services.values())
        published = passed and all(p.exists() and read(p)['status'] == 'pushed_and_remote_head_verified'
            for p in (receipt100, receipt37))
        sealed = published and seal.exists() and read(seal)['status'] == 'passed_sealed_actual_conditional_native14_candidate'
        available = psutil.virtual_memory().available / 2**30
        write(out / 'waiting_status.json', {
            'status': 'waiting_for_serialized100_and37_main_and_native14_seal_and_memory',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'preceding_services_closed': closed,
            'preceding_services_passed': passed, 'preceding_main_receipts_present': published,
            'actual_native14_seal_passed': sealed, 'available_RAM_GiB': available})
        if sealed and available >= 8:
            break
        time.sleep(30)
    assert not (A / 'optimization_20261003_r101').exists()
    for path, digest in expected.items():
        assert sha(path) == digest, path
    create(out / 'actual_admission.json', {
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'available_RAM_GiB': available,
        'preceding_main_receipts': [read(receipt100), read(receipt37)],
        'actual_native14_seal': read(seal), 'driver_sha256': sha(driver),
        'scientific_processes_suspended_or_restarted': 0, 'test_labels_read': False})
    runpy.run_path(str(driver), run_name='__main__')


if __name__ == '__main__':
    main()
