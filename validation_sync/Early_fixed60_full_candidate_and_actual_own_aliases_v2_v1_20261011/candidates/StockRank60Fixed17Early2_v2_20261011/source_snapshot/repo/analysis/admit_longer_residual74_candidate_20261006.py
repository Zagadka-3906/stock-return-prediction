"""Freeze all sources and infer the selected74-case scheme after full scoring."""
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
    prep = A / 'longer_residual74_candidate_workflow_preparation_20261006.json'
    pins = read(prep)['input_sha256']
    services = {name: A / 'service_owned_workflows_20261006' / name for name in (
        'conditional_residual128_256_comparison74', 'conditional_residual128_256_scores74_evidence_publication')}
    identities = {name: read(folder / 'native_launch.json') for name, folder in services.items()}
    out = A / 'longer_residual74_candidate_admission_20261006'
    assert not out.exists()
    out.mkdir()
    while True:
        closed = {name: not owned(row) for name, row in identities.items()}
        passed = all(closed.values()) and all((f / 'service_execution.json').exists()
            and read(f / 'service_execution.json')['status'] == 'passed' for f in services.values())
        available = psutil.virtual_memory().available / 2**30
        write(out / 'waiting_status.json', {'status': 'waiting_for_full74_official_scores_and_main_and_memory',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'preceding_services_closed': closed,
            'preceding_services_passed': passed, 'available_RAM_GiB': available})
        if passed and available >= 8.5: break
        time.sleep(30)
    for path, digest in pins.items(): assert sha(path) == digest, path
    runpy.run_path(str(A / 'freeze_longer_residual74_candidate_sources_20261006.py'), run_name='__main__')
    driver = A / 'freeze_and_infer_longer_residual74_candidate_20261006.py'
    freeze = A / 'longer_residual74_source_freeze_20261006/manifest.json'
    expected = read(freeze)['files'][driver.relative_to(ROOT).as_posix()]['sha256']
    assert sha(driver) == expected
    create(out / 'actual_admission.json', {'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'source_snapshot_manifest_sha256': sha(freeze), 'driver_sha256': expected,
        'available_RAM_GiB': available, 'actual_all74_scores_naturally_passed_before_freeze': True,
        'native_component_count_follows_selected_winner': True,
        'scientific_workers_stopped_or_restarted': 0, 'test_labels_read': False})
    runpy.run_path(str(driver), run_name='__main__')


if __name__ == '__main__': main()
