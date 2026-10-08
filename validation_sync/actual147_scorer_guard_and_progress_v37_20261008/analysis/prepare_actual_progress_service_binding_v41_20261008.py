"""Bind operational progress to successful recovery services without changing scientific artifacts."""
from pathlib import Path
import importlib.util
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start


def main():
    original = A / 'monitor_actual_chronological_optimization_progress_v40_20261008.py'
    destination = A / 'monitor_actual_chronological_optimization_progress_v41_20261008.py'
    assert not destination.exists()
    source = original.read_text(encoding='utf8')
    marker = "        if (folder/'verification.json').exists():"
    assert source.count(marker) == 1
    correction = """        if number==146:
            row['selected_candidate']=status('HuberCrossFamilyFine125_selected_candidate_preparation_v4_20261008')
            row['candidate_sealing']=status('HuberCrossFamilyFine125_selected_candidate_sealing_v4_20261008')
            row['full_registration']=status('HuberCrossFamilyFine125_round146_full_registration_v4_20261008')
"""
    source = source.replace(marker, correction + marker).replace('progress_v40_20261008', 'progress_v41_20261008')
    with destination.open('x', encoding='utf8', newline='') as stream:
        stream.write(source)
    specification = importlib.util.spec_from_file_location('actual_observer_binding41', destination)
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    actual = module.snapshot()
    row = actual['pipeline']['146']
    assert row['completed_cases'] == 125
    assert all(row[key]['status'] == 'passed' for key in ('quality', 'selected_candidate', 'candidate_sealing', 'full_registration'))
    assert actual['best_fully_qualified']['round'] == 146
    pins = {str(path): sha(path) for path in (Path(__file__), original, destination)}
    launch = start('actual_chronological_optimization_progress_observer_v41_20261008', destination.name, [], pins)
    assert owned(launch)
    create(A/'latest_actual_optimization_progress_pointer_v41_20261008.json', {
        'json': str(A/'optimization_live_progress_v41_20261008.json'),
        'markdown': str(A/'optimization_live_progress_v41_20261008.md'),
        'launch': launch, 'new_quality_scores': 0})
    old = read(A/'service_owned_workflows_20261006/actual_chronological_optimization_progress_observer_v40_20261008/native_launch.json')
    parent, worker, idle = suspended_idle(old, '    main (monitor_actual_chronological_optimization_progress_v40_20261008.py:100)')
    try:
        assert not worker.children() and owned(launch)
        worker.terminate(); worker.wait(timeout=10)
        parent.terminate(); parent.wait(timeout=10)
    finally:
        for process in (parent, worker):
            if process.is_running(): process.resume()
    create(A/'actual_progress146_service_binding_corrected_v41_20261008.json', {
        'status': 'corrected_only_operational146_recovery_service_binding',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins,
        'actual146': row, 'old_observer': old, 'old_observer_idle_stack': idle,
        'original_failed_attempts_preserved': True, 'new_observer': launch,
        'scientific_workers_stopped': 0, 'new_quality_scores': 0,
        'scientific_sources_parameters_and_candidate_bytes_changed': False})
    print({'status': 'progress41_running_with_actual146_passed', 'worker': launch['owned_worker_pid']}, flush=True)


if __name__ == '__main__':
    main()
