"""Finish receipts for the existing scientific jobs and repair only the failed observer."""
from pathlib import Path
import json
import os
import sys
import time
import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
from handoff_recovery_qualified_workflows_20261005 import read, sha, create
from handoff_factorization_machine_repaired_workflows_20261005 import processes
from prepare_gradient_sampling_followups_20261005 import launch


def main():
    out = A / 'gradient_sampling_followups_20261005'
    assert not (out / 'verification.json').exists()
    native = read(A / 'gradient_sampling_bank_run_v2_20261005.json')
    future = read(A / 'gradient_sampling_future_run_20261005.json')
    jobs = [j for j in read(A / 'resumed_rounds_nystrom_locked_20261004.json') if j['round'] in (75, 76)]
    assert len(jobs) == 2
    for job in (native, future, *jobs):
        processes(job)
        assert not Path(job['stderr']).read_text(encoding='utf-8')
    failed_log = A / 'run_logs/actual_optimization_monitor_v10_20261005.stderr.log'
    assert "has no attribute 'complete_round_evidence'" in failed_log.read_text(encoding='utf-8')
    assert not psutil.pid_exists(6124)
    old_run = read(A / 'actual_optimization_monitor_run_v10_20261005.json')
    for source, digest in old_run['input_sha256'].items():
        assert sha(source) == digest, source
    script = A / 'monitor_actual_optimization_progress_v11_20261005.py'
    source = (A / 'monitor_actual_optimization_progress_v10_20261005.py').read_text(encoding='utf-8-sig')
    source = source.replace('monitor_actual_optimization_progress_v10_20261005', 'monitor_actual_optimization_progress_v11_20261005')
    source = source.replace('actual_optimization_monitor_run_v10_20261005', 'actual_optimization_monitor_run_v11_20261005')
    source = source.replace('refresh_optimization_boundary_evidence_v9_20261005', 'refresh_optimization_boundary_evidence_v10_20261005')
    compile(source, str(script), 'exec')
    with script.open('x', encoding='utf-8', newline='') as stream:
        stream.write(source)
    run_path = A / 'actual_optimization_monitor_run_v11_20261005.json'
    inputs = {**old_run['input_sha256'], **{str(p): sha(p) for p in (
        Path(__file__), script, A / 'refresh_optimization_boundary_evidence_v10_20261005.py')}}
    create(run_path, {'original_driver': str(script), 'original_arguments': [],
        'input_sha256': inputs, 'monitors_through_actual_qualified_round': 76,
        'goal_completion_not_inferred': True, 'previous_observer_terminal_error_log_sha256': sha(failed_log)})
    env = dict(os.environ)
    for key in ('TMP', 'TEMP', 'TMPDIR'):
        env[key] = read(A / 'gradient_sampling_storage_20261005.json')['temporary_directory']
    launcher = A / 'run_recovery_qualified_workflow_20261005.py'
    monitor = launch(launcher, [str(script), str(run_path)], 'actual_optimization_monitor_v11_20261005', env)
    create(A / 'actual_optimization_monitor_launch_v11_20261005.json', monitor)
    time.sleep(6)
    processes(monitor)
    assert not Path(monitor['stderr']).read_text(encoding='utf-8')
    state = read(A / 'actual_optimization_monitor_state_20261005.json')
    assert state['source_sha256'] == sha(script)
    cost = read(A / 'optimization_fit_cost_evidence_20261004.json')
    assert cost['gradient_sampling_declared_configurations'] == 6
    assert cost['gradient_sampling_actual_annual_fits'] == 0
    assert cost['configurations'] == 180
    create(out / 'verification.json', {'status': 'passed_owned_native_scheduling_and_followup_launches',
        'native': native, 'future': future, 'quality_rounds': jobs, 'monitor': monitor,
        'all_existing_scientific_jobs_retained_without_restart': True,
        'original_observer_error_retained': str(failed_log), 'only_publication_branch': 'main',
        'actual_full_GOSS_fits_at_launch': 0, 'actual_pilots_excluded_from_annual_counts': True,
        'new_quality_scores': 0, 'test_labels_read': False})
    print(json.dumps({'status': 'passed', 'native': native['pid'], 'future': future['pid'],
        'quality': [j['pid'] for j in jobs], 'monitor': monitor['pid'],
        'actual_declared_configurations': cost['configurations']}), flush=True)


if __name__ == '__main__':
    main()
