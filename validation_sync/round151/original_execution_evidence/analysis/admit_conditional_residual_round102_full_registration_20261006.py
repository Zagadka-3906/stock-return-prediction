"""Run full102 registration after actual naturally passed16 inference and sealing."""
from pathlib import Path
import runpy
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from atomic_optimization_observer_writes_20261005 import write


def main():
    import psutil
    preparation = A / 'conditional_residual_round102_registration_source_preparation_20261006.json'
    pins = read(preparation)['input_sha256']
    driver = A / 'run_conditional_residual_round102_full_registration_20261006.py'
    services = {name: A / 'service_owned_workflows_20261006' / name for name in (
        'conditional_flag_round101_full_publication_v6',
        'conditional_residual_candidate_inference_v2', 'conditional_residual_candidate_sealing_v2')}
    identities = {name: read(folder / 'native_launch.json') for name, folder in services.items()}
    out = A / 'conditional_residual_round102_registration_admission_20261006'
    assert not out.exists()
    out.mkdir()
    while True:
        closed = {name: not owned(row) for name, row in identities.items()}
        passed = all(closed.values()) and all((folder / 'service_execution.json').exists()
            and read(folder / 'service_execution.json')['status'] == 'passed' for folder in services.values())
        available = psutil.virtual_memory().available / 2**30
        write(out / 'waiting_status.json', {'status': 'waiting_for_actual_sealed16_and_full101_and_memory',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'preceding_services_closed': closed,
            'preceding_services_passed': passed, 'available_RAM_GiB': available})
        if passed and available >= 8:
            break
        assert sha(driver) == pins[str(driver)]
        time.sleep(30)
    for path, digest in pins.items():
        assert sha(path) == digest, path
    assert read(A / 'conditional_residual_release_20261006/source_package_verification.json')['status'] == 'passed_sealed_actual_conditional_residual_candidate'
    create(out / 'actual_admission.json', {'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'available_RAM_GiB': available, 'input_sha256': pins,
        'all_original_scientific_workers_preserved': True, 'test_labels_read': False})
    runpy.run_path(str(driver), run_name='__main__')


if __name__ == '__main__':
    main()
