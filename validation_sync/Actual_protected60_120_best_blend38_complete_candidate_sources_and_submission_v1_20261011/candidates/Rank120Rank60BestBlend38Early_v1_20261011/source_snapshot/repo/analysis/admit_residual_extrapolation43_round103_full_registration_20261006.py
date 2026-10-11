"""Close the complete43-case registry and every original QA after real inference."""
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
    prep = A / 'residual_extrapolation43_workflow_preparation_20261006.json'
    pins = read(prep)['input_sha256']
    services = {name: A / 'service_owned_workflows_20261006' / name for name in (
        'residual_extrapolation43_candidate_inference', 'residual_extrapolation43_candidate_sealing')}
    identities = {name: read(folder / 'native_launch.json') for name, folder in services.items()}
    out = A / 'residual_extrapolation43_round103_registration_admission_20261006'
    assert not out.exists()
    out.mkdir()
    # The original R87 writer was live during preparation. Let it finish all
    # scientific stages naturally before another full-board writer starts.
    queue = A / 'service_owned_dependency_queue_v4_20261006'
    prior = read(queue / 'state.json')['activated_jobs'].get('round87')
    while True:
        closed = {name: not owned(row) for name, row in identities.items()}
        passed = all(closed.values()) and all((f / 'service_execution.json').exists()
            and read(f / 'service_execution.json')['status'] == 'passed' for f in services.values())
        prior_closed = prior is None or not owned(prior)
        available = psutil.virtual_memory().available / 2**30
        write(out / 'waiting_status.json', {'status': 'waiting_for_real_candidate_seal_and_original87_writer_and_memory',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'preceding_services_closed': closed,
            'preceding_services_passed': passed, 'original87_writer_closed': prior_closed,
            'available_RAM_GiB': available})
        if passed and prior_closed and available >= 8: break
        time.sleep(30)
    for path, digest in pins.items(): assert sha(path) == digest, path
    create(out / 'actual_admission.json', {'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'input_sha256': pins, 'original87_writer_naturally_terminal': prior_closed,
        'scientific_workers_stopped_or_restarted': 0, 'test_labels_read': False})
    runpy.run_path(str(A / 'run_residual_extrapolation43_round103_full_registration_20261006.py'), run_name='__main__')


if __name__ == '__main__': main()
