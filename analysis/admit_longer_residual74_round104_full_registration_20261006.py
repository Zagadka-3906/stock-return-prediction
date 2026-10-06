"""Serialize the complete74-case board after genuine candidate seal and original R88."""
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
    prep = A / 'longer_residual74_full_registration_preparation_20261006.json'
    pins = read(prep)['input_sha256']
    services = {name: A / 'service_owned_workflows_20261006' / name for name in (
        'longer_residual74_candidate_inference', 'longer_residual74_candidate_sealing',
        'residual_extrapolation43_round103_full_registration')}
    identities = {name: read(folder / 'native_launch.json') for name, folder in services.items()}
    queue = A / 'service_owned_dependency_queue_v4_20261006'
    original88 = read(queue / 'state.json')['activated_jobs'].get('round88')
    assert original88 is not None
    out = A / 'longer_residual74_round104_registration_admission_20261006'
    assert not out.exists()
    out.mkdir()
    create(out / 'original_writer_identity_before_wait.json', original88)
    while True:
        closed = {name: not owned(row) for name, row in identities.items()}
        passed = all(closed.values()) and all((folder / 'service_execution.json').exists()
            and read(folder / 'service_execution.json')['status'] == 'passed' for folder in services.values())
        original_closed = not owned(original88)
        available = psutil.virtual_memory().available / 2**30
        write(out / 'waiting_status.json', {
            'status': 'waiting_for_real_selected74_candidate_seal_full103_and_original88_writer',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'preceding_services_naturally_closed': closed, 'preceding_services_naturally_passed': passed,
            'original88_writer_closed': original_closed, 'available_RAM_GiB': available,
            'scientific_workers_suspended_stopped_or_restarted': 0,
        })
        if passed and original_closed and available >= 8: break
        time.sleep(30)
    for path, digest in pins.items(): assert sha(path) == digest, path
    create(out / 'actual_admission.json', {
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins,
        'original88_writer_naturally_terminal': original_closed,
        'scientific_workers_suspended_stopped_or_restarted': 0, 'test_labels_read': False,
    })
    runpy.run_path(str(A / 'run_longer_residual74_round104_full_registration_20261006.py'), run_name='__main__')


if __name__ == '__main__': main()
