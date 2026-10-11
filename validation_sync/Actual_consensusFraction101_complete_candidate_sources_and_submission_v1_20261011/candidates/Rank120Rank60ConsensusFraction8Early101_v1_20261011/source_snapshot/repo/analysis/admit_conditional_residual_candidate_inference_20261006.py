"""Admit the frozen residual winner after serialized ranking completion and memory."""
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
    source = A / 'freeze_and_infer_conditional_residual_candidate_20261006.py'
    freeze = A / 'conditional_residual_source_freeze_20261006/manifest.json'
    expected = read(freeze)['files'][source.relative_to(ROOT).as_posix()]['sha256']
    services = {name: A / 'service_owned_workflows_20261006' / name for name in (
        'conditional_flag_round101_full_registration_v3', 'conditional_residual_scores_evidence_publication_v2')}
    identities = {name: read(folder / 'native_launch.json') for name, folder in services.items()}
    out = A / 'conditional_residual_candidate_admission_20261006'
    assert not out.exists()
    out.mkdir()
    while True:
        closed = {name: not owned(row) for name, row in identities.items()}
        passed = all(closed.values()) and all((folder / 'service_execution.json').exists()
            and read(folder / 'service_execution.json')['status'] == 'passed' for folder in services.values())
        available = psutil.virtual_memory().available / 2**30
        write(out / 'waiting_status.json', {'status': 'waiting_for_full101_and49_main_closure_and_memory',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'preceding_services_closed': closed,
            'preceding_services_passed': passed, 'available_RAM_GiB': available,
            'scientific_processes_stopped_or_restarted': 0})
        if passed and available >= 8.5:
            break
        assert sha(source) == expected
        time.sleep(30)
    assert sha(source) == expected
    create(out / 'actual_admission.json', {'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'available_RAM_GiB': available, 'driver_sha256': expected,
        'source_freeze_manifest_sha256': sha(freeze), 'scientific_processes_stopped_or_restarted': 0,
        'test_labels_read': False})
    runpy.run_path(str(source), run_name='__main__')


if __name__ == '__main__':
    main()
