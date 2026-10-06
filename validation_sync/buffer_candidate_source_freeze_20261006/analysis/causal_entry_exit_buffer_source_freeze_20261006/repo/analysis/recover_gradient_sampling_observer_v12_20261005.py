"""Retain native jobs and verify the actual new coverage refresh before observing."""
from pathlib import Path
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
    assert not psutil.pid_exists(read(A / 'actual_optimization_monitor_launch_v11_20261005.json')['pid'])
    assert not (A / 'actual_optimization_monitor_run_v12_20261005.json').exists()
    out = A / 'gradient_sampling_followups_20261005'
    assert not (out / 'verification.json').exists()
    native = read(A / 'gradient_sampling_bank_run_v2_20261005.json')
    future = read(A / 'gradient_sampling_future_run_20261005.json')
    jobs = [j for j in read(A / 'resumed_rounds_nystrom_locked_20261004.json') if j['round'] in (75, 76)]
    for job in (native, future, *jobs):
        processes(job)
        assert not Path(job['stderr']).read_text(encoding='utf-8')
    old_guard = read(A / 'actual_optimization_monitor_run_v11_20261005.json')['input_sha256']
    for source, digest in old_guard.items():
        assert sha(source) == digest, source
    boundary_script = A / 'refresh_optimization_boundary_evidence_v11_20261005.py'
    source = (A / 'refresh_optimization_boundary_evidence_v9_20261005.py').read_text(encoding='utf-8-sig')
    source = source.replace("ROOT = Path(__file__).resolve().parents[1]", "from refresh_optimization_boundary_evidence_20261004 import complete_round_evidence\n\nROOT = Path(__file__).resolve().parents[1]")
    needle = "    from refresh_optimization_boundary_evidence_20261004 import complete_round_evidence\n    plan ="
    assert needle in source
    source = source.replace(needle, "    from refresh_optimization_boundary_evidence_20261004 import complete_round_evidence\n    import refresh_gradient_sampling_cost_evidence_20261005 as costs\n    with operational_writes('refresh_gradient_sampling_cost_evidence_20261005'):\n        costs.main()\n    plan =")
    with boundary_script.open('x', encoding='utf-8', newline='') as stream:
        stream.write(source)
    monitor_script = A / 'monitor_actual_optimization_progress_v12_20261005.py'
    source = (A / 'monitor_actual_optimization_progress_v11_20261005.py').read_text(encoding='utf-8-sig')
    source = source.replace('monitor_actual_optimization_progress_v11_20261005', 'monitor_actual_optimization_progress_v12_20261005')
    source = source.replace('actual_optimization_monitor_run_v11_20261005', 'actual_optimization_monitor_run_v12_20261005')
    source = source.replace('refresh_optimization_boundary_evidence_v10_20261005', 'refresh_optimization_boundary_evidence_v11_20261005')
    with monitor_script.open('x', encoding='utf-8', newline='') as stream:
        stream.write(source)
    for path in (boundary_script, monitor_script):
        compile(path.read_text(encoding='utf-8'), str(path), 'exec')
    import qualified_round_recovery_evidence_v2_20261005 as qualification
    import refresh_optimization_boundary_evidence_20261004 as base
    base.complete_round_evidence = qualification.complete_round_evidence
    try:
        import importlib
        boundary = importlib.import_module(boundary_script.stem)
        assert callable(boundary.complete_round_evidence)
        # Exercise the real old-producer -> new-cost -> new-coverage sequence before launch.
        boundary.main()
        cost = read(A / 'optimization_fit_cost_evidence_20261004.json')
        evidence = read(A / 'optimization_boundary_evidence_20261004.json')
        assert cost['configurations'] == 180 and cost['gradient_sampling_actual_annual_fits'] == 0
        assert evidence['gradient_sampling_coverage_evidence']['remaining_required_official_rounds'] == [75, 76]
    finally:
        qualification.close()
    proof_path = A / 'gradient_sampling_observer_integration_preflight_v12_20261005/verification.json'
    create(proof_path, {'status': 'passed_actual_producer_cost_and_coverage_integration',
        'actual_declared_configurations': cost['configurations'],
        'actual_new_annual_fits': cost['total_actual_new_annual_fits'],
        'actual_GOSS_complete_fits': cost['gradient_sampling_actual_annual_fits'],
        'remaining_GOSS_quality_rounds': [75, 76], 'new_quality_scores': 0,
        'source_sha256': {str(p): sha(p) for p in (Path(__file__), boundary_script, monitor_script)}})
    run_path = A / 'actual_optimization_monitor_run_v12_20261005.json'
    inputs = {**old_guard, **{str(p): sha(p) for p in (Path(__file__), boundary_script, monitor_script, proof_path)}}
    create(run_path, {'original_driver': str(monitor_script), 'original_arguments': [],
        'input_sha256': inputs, 'monitors_through_actual_qualified_round': 76,
        'goal_completion_not_inferred': True})
    env = dict(os.environ)
    for key in ('TMP', 'TEMP', 'TMPDIR'):
        env[key] = read(A / 'gradient_sampling_storage_20261005.json')['temporary_directory']
    launcher = A / 'run_recovery_qualified_workflow_20261005.py'
    monitor = launch(launcher, [str(monitor_script), str(run_path)], 'actual_optimization_monitor_v12_20261005', env)
    create(A / 'actual_optimization_monitor_launch_v12_20261005.json', monitor)
    time.sleep(6)
    processes(monitor)
    assert not Path(monitor['stderr']).read_text(encoding='utf-8')
    create(out / 'verification.json', {'status': 'passed_owned_native_scheduling_and_followup_launches',
        'native': native, 'future': future, 'quality_rounds': jobs, 'monitor': monitor,
        'all_existing_scientific_jobs_retained_without_restart': True,
        'original_observer_errors_retained': [str(A / f'run_logs/actual_optimization_monitor_v{n}_20261005.stderr.log') for n in (10, 11)],
        'actual_cost_and_coverage_integration_verified_before_launch': str(proof_path),
        'only_publication_branch': 'main', 'actual_full_GOSS_fits_at_launch': 0,
        'actual_pilots_excluded_from_annual_counts': True, 'new_quality_scores': 0, 'test_labels_read': False})
    print('Actual GOSS jobs retained; verified cost/coverage observer restored through76', flush=True)


if __name__ == '__main__':
    main()
