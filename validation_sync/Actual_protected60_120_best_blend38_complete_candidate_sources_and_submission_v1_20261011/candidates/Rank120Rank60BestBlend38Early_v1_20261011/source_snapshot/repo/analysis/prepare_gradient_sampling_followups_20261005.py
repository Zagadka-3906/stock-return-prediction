"""Queue complete GOSS fits/quality and hand off the observer without changing live science."""
from pathlib import Path
from datetime import datetime
import json
import os
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
from handoff_recovery_qualified_workflows_20261005 import read, sha, create
from handoff_factorization_machine_repaired_workflows_20261005 import processes, stop


def launch(script, arguments, label, env):
    stdout = A / f'run_logs/{label}.stdout.log'
    stderr = A / f'run_logs/{label}.stderr.log'
    with stdout.open('xb') as output, stderr.open('xb') as error:
        process = subprocess.Popen([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8', str(script), *arguments],
            cwd=ROOT, env=env, stdout=output, stderr=error, creationflags=subprocess.CREATE_NO_WINDOW)
    return {'pid': process.pid, 'script': str(script), 'script_args': arguments,
        'stdout': str(stdout), 'stderr': str(stderr), 'at_local': datetime.now().isoformat()}


def main():
    out = A / 'gradient_sampling_followups_20261005'
    assert not out.exists()
    proofs = [A / f'{folder}/verification.json' for folder in ('gradient_sampling_preflight_20261005',
        'gradient_sampling_direct_router_preflight_20261005', 'gradient_sampling_search_generator_preflight_20261005')]
    for proof_path in proofs:
        proof = read(proof_path)
        assert proof['status'].startswith('passed')
        for path, digest in proof.get('source_sha256', {}).items():
            assert sha(path) == digest, path
    assert [row['generated_records'] for row in read(proofs[-1])['controls']] == [124, 138, 138]
    bank_run = read(A / 'gradient_sampling_bank_run_20261005.json')
    processes(bank_run)
    assert not (Path(read(A / 'gradient_sampling_storage_20261005.json')['output_directory']) / 'protocol.json').exists()
    previous_monitor = next(j for j in read(A / 'recovery_qualified_workflow_handoff_20261005/verification.json')['jobs']
        if j['label'] == 'operational_monitor')
    processes(previous_monitor)
    # Preserve the already executed pilots and avoid overlapping two large native fit families.
    bank_driver = A / 'run_gradient_sampling_bank_v2_20261005.py'
    source = (A / 'run_gradient_sampling_bank_20261005.py').read_text(encoding='utf-8-sig')
    source = source.replace('gradient_sampling_bank_run_20261005.json', 'gradient_sampling_bank_run_v2_20261005.json')
    needle = "    print('Actual wide annual attempt closed: ' + bank.read(wide)['status'], flush=True)"
    replacement = needle + '''
    if bank.read(wide)['status'] == 'passed':
        wide_future = A / 'neural16384_full_future_qa_20261005/resource_summary.json'
        while not wide_future.exists():
            time.sleep(10)
        print('Actual wide final attempt closed: ' + bank.read(wide_future)['status'], flush=True)
'''
    assert needle in source
    source = source.replace(needle, replacement)
    source = source.replace("'wide_training_attempt_closed_before_first_full_GOSS_fit': True",
        "'wide_training_attempt_closed_before_first_full_GOSS_fit': True,\n        'actual_wide_final_attempt_closure_required_when_annual_passes': True")
    with bank_driver.open('x', encoding='utf-8', newline='') as stream:
        stream.write(source)
    compile(source, str(bank_driver), 'exec')
    create(out / 'frozen_before_handoff.json', {'status': 'frozen_before_owned_idle_scheduling_handoff',
        'previous_native_job': bank_run, 'previous_monitor': previous_monitor,
        'source_sha256': {str(Path(__file__)): sha(Path(__file__))},
        'all_GOSS_pilot_artifacts_preserved': True, 'all_R66_and_other_live_scientific_jobs_untouched': True,
        'actual_full_GOSS_fits_at_handoff': 0, 'new_quality_scores': 0})
    stopped = stop(bank_run) + stop(previous_monitor)
    env = dict(os.environ)
    storage = read(A / 'gradient_sampling_storage_20261005.json')
    for key in ('TMP', 'TEMP', 'TMPDIR'):
        env[key] = storage['temporary_directory']
    for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'POLARS_MAX_THREADS'):
        env[key] = '8'
    native_inputs = dict(bank_run['input_sha256'])
    native_inputs.update({str(p): sha(p) for p in (Path(__file__), bank_driver, proofs[0],
        A / 'gradient_sampling_bank_run_20261005.json')})
    native = launch(bank_driver, [], 'gradient_sampling_bank_v2_20261005', env)
    create(A / 'gradient_sampling_bank_run_v2_20261005.json', {**native, 'input_sha256': native_inputs,
        'same30_annual300_round_fits_required': True, 'original_pilots_reused_not_counted_as_full_fits': True})
    all_sources = set(A.glob('*gradient_sampling*20261005.py'))
    all_sources.update(A / f'{prefix}{n}{suffix}.py' for n in (75, 76)
        for prefix, suffix in (('optimize_training_round', ''), ('finalize_training_round', ''),
            ('run_training_round', '_pipeline'), ('run_training_round', '_v2_pipeline')))
    all_sources.update((*proofs, A / 'gradient_sampling_complete_search_plan_20261005.json',
        A / 'gradient_sampling_bank_run_v2_20261005.json'))
    inputs = {str(p): sha(p) for p in all_sources}
    quality_run = A / 'gradient_sampling_quality_run_v2_20261005.json'
    create(quality_run, {'status': 'frozen_before_actual_GOSS_native_and_quality_waiters',
        'input_sha256': inputs, 'planned_records': {'75': 124, '76': 138},
        'actual_full_predecessors74_75_required': True, 'actual30_annual6_final_controls_required': True,
        'new_quality_scores': 0, 'test_labels_read': False})
    future_script = A / 'verify_gradient_sampling_full_future_20261005.py'
    future = launch(future_script, [], 'gradient_sampling_full_future_20261005', env)
    create(A / 'gradient_sampling_future_run_20261005.json', {**future, 'input_sha256': inputs,
        'actual_fulltraining_fits_required': 6, 'actual_rows_required': 1599600,
        'cold80_and_native_direct_controls_required': True, 'test_labels_read': False})
    launcher = A / 'run_recovery_qualified_workflow_20261005.py'
    jobs = []
    for number in (75, 76):
        driver = A / f'run_training_round{number}_v2_pipeline.py'
        run_path = out / f'round{number}_run.json'
        create(run_path, {'original_driver': str(driver), 'original_arguments': [],
            'input_sha256': {str(p): sha(p) for p in (launcher, driver, quality_run,
                A / 'qualified_round_recovery_evidence_20261005.py',
                A / 'qualified_round_recovery_evidence_v2_20261005.py',
                A / 'standalone_root_source_adapter_20261005.py')}, 'test_labels_read': False})
        job = launch(launcher, [str(driver), str(run_path)], f'round{number}_gradient_sampling_v2_20261005', env)
        jobs.append({'round': number, **job, 'expected_scored_records': 124 if number == 75 else 138,
            'status': 'waiting_for_actual_native_controls_and_qualified_predecessor'})
    registry_path = A / 'resumed_rounds_nystrom_locked_20261004.json'
    registry = read(registry_path)
    assert not any(j['round'] in (75, 76) for j in registry)
    temporary = registry_path.with_suffix('.goss.tmp')
    temporary.write_text(json.dumps(registry + jobs, ensure_ascii=False, indent=2), encoding='utf-8')
    temporary.replace(registry_path)
    monitor_script = A / 'monitor_actual_optimization_progress_v10_20261005.py'
    monitor_run = A / 'actual_optimization_monitor_run_v10_20261005.json'
    old_guard = read(A / 'actual_optimization_monitor_run_v9_20261005.json')['input_sha256']
    monitor_inputs = {**old_guard, **{str(p): sha(p) for p in (monitor_script, Path(__file__), *proofs,
        A / 'refresh_gradient_sampling_cost_evidence_20261005.py',
        A / 'refresh_optimization_boundary_evidence_v9_20261005.py')}}
    create(monitor_run, {'original_driver': str(monitor_script), 'original_arguments': [],
        'input_sha256': monitor_inputs, 'monitors_through_actual_qualified_round': 76,
        'goal_completion_not_inferred': True})
    monitor = launch(launcher, [str(monitor_script), str(monitor_run)], 'actual_optimization_monitor_v10_20261005', env)
    time.sleep(6)
    for job in (native, future, *jobs, monitor):
        processes(job)
        assert not Path(job['stderr']).read_text(encoding='utf-8'), job['stderr']
    create(out / 'verification.json', {'status': 'passed_owned_native_scheduling_and_followup_launches',
        'native': native, 'future': future, 'quality_rounds': jobs, 'monitor': monitor,
        'stopped_owned_idle_processes': stopped, 'only_publication_branch': 'main',
        'actual_full_GOSS_fits_at_launch': 0, 'small_control_fits_not_counted_as_full': True,
        'new_quality_scores': 0, 'test_labels_read': False})
    print(json.dumps({'status': 'passed', 'native': native['pid'], 'future': future['pid'],
        'quality': [j['pid'] for j in jobs], 'monitor': monitor['pid']}), flush=True)


if __name__ == '__main__':
    main()
