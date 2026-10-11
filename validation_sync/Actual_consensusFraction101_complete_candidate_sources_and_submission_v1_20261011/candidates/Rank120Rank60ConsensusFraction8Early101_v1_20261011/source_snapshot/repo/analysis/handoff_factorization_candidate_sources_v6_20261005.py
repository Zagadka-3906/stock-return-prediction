"""Replace only the two positively owned, unstarted FM quality waiters."""
from pathlib import Path
from datetime import datetime
import json
import os
import subprocess
import sys
import time
import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
from handoff_recovery_qualified_workflows_20261005 import read, sha, create
from handoff_factorization_machine_repaired_workflows_20261005 import processes, stop


def require_owned(job):
    owned = processes(job)
    for process in owned:
        assert process.cmdline()[-len(job['script_args']):] == job['script_args']
    return owned


def main():
    out = A / 'factorization_machine_candidate_source_handoff_v6_20261005'
    assert not out.exists(), 'Inspect an existing handoff instead of duplicating jobs.'
    proof_path = A / 'factorization_machine_candidate_source_preflight_v6_20261005/verification.json'
    proof = read(proof_path)
    assert proof['status'].startswith('passed')
    assert proof['planned_official_records_unchanged'] == {'73': 124, '74': 138}
    for path, expected in proof['source_sha256'].items():
        assert sha(path) == expected, path
    registry_path = A / 'resumed_rounds_nystrom_locked_20261004.json'
    registry = read(registry_path)
    old = [job for job in registry if job['round'] in (73, 74)]
    retained = [job for job in registry if job['round'] not in (73, 74)]
    assert len(old) == 2
    for job in old:
        number = job['round']
        require_owned(job)
        assert f'round{number}_v5_pipeline.py' in job['script_args'][0]
        assert not (A / f'optimization_20261003_r{number}/protocol.json').exists()
        assert not list((A / f'optimization_20261003_r{number}').glob('wave*_results.json'))
        assert read(A / f'ongoing_optimization_r{number}_state.json')['stage'].startswith('waiting')
        assert job['expected_scored_records'] == (124 if number == 73 else 138)
    native_job = read(A / 'recovery_qualified_workflow_handoff_20261005/verification.json')['jobs'][0]
    assert native_job['script_args'][0].endswith('run_neural16384_full_bank_20261005.py')
    native_process = psutil.Process(native_job['pid'])
    assert native_job['script_args'][0] in native_process.cmdline()
    native_identity = {'pid': native_process.pid, 'create_time': native_process.create_time(), 'cmdline': native_process.cmdline()}
    create(out / 'frozen_before_handoff.json', {
        'status': 'frozen_before_owned_unstarted_candidate_source_handoff', 'old_jobs': old,
        'retained_registry_jobs': retained, 'untouched_actual_wide_training': native_identity,
        'source_sha256': {str(Path(__file__)): sha(Path(__file__)), str(proof_path): sha(proof_path)},
        'native_models_forecast_math_and_official_grids_unchanged': True, 'new_quality_scores': 0})
    run_path = A / 'factorization_machine_quality_run_v6_20261005.json'
    inputs = dict(read(A / 'factorization_machine_quality_run_v5_20261005.json')['input_sha256'])
    extra = [Path(__file__), proof_path, A / 'run_factorization_machine_round_v6_20261005.py',
        A / 'predict_factorization_machine_scheme_v5_20261005.py',
        A / 'factorization_machine_candidate_source_generation_v6_20261005.json']
    extra += [A / f'{prefix}{number}{suffix}.py' for number in (73, 74)
        for prefix, suffix in (('finalize_training_round', '_v6'), ('run_training_round', '_v6_pipeline'))]
    inputs.update({str(path): sha(path) for path in extra})
    create(run_path, {'status': 'frozen_before_actual_canonical_release_and_candidate_packaging',
        'input_sha256': inputs, 'planned_records': {'73': 124, '74': 138},
        'actual_native30_annual6_final_fullfuture_controls_required': True,
        'same_actual_full_predecessor_requirements': [72, 73],
        'publication_canonical_import_and_candidate_sources_checked': True, 'test_labels_read': False})
    stopped = []
    for job in old:
        require_owned(job)
        stopped.extend(stop(job))
    env = dict(os.environ)
    scratch = Path(read(A / 'factorization_machine_storage_20261005.json')['temporary_directory'])
    assert scratch.resolve().drive.upper() in ('D:', 'E:')
    for key in ('TMP', 'TEMP', 'TMPDIR'):
        env[key] = str(scratch)
    for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'POLARS_MAX_THREADS'):
        env[key] = '8'
    launcher = A / 'run_recovery_qualified_workflow_20261005.py'
    jobs = []
    for number in (73, 74):
        driver = A / f'run_training_round{number}_v6_pipeline.py'
        job_run = out / f'round{number}_run.json'
        create(job_run, {'original_driver': str(driver), 'original_arguments': [],
            'input_sha256': {str(path): sha(path) for path in (launcher, driver, run_path, proof_path,
                A / 'qualified_round_recovery_evidence_20261005.py',
                A / 'qualified_round_recovery_evidence_v2_20261005.py',
                A / 'standalone_root_source_adapter_20261005.py')}, 'test_labels_read': False})
        stdout = A / f'run_logs/round{number}_factorization_candidate_v6_20261005.stdout.log'
        stderr = A / f'run_logs/round{number}_factorization_candidate_v6_20261005.stderr.log'
        arguments = [str(driver), str(job_run)]
        with stdout.open('xb') as output, stderr.open('xb') as error:
            process = subprocess.Popen([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8', str(launcher), *arguments],
                cwd=ROOT, env=env, stdout=output, stderr=error, creationflags=subprocess.CREATE_NO_WINDOW)
        jobs.append({'round': number, 'pid': process.pid, 'script': str(launcher), 'script_args': arguments,
            'stdout': str(stdout), 'stderr': str(stderr), 'at_local': datetime.now().isoformat(),
            'expected_scored_records': 124 if number == 73 else 138,
            'status': 'waiting_for_native_controls_and_complete_predecessor_verified_canonical_release_and_candidate'})
    temporary = registry_path.with_suffix('.fm_candidate_v6.tmp')
    temporary.write_text(json.dumps(retained + jobs, ensure_ascii=False, indent=2), encoding='utf-8')
    temporary.replace(registry_path)
    time.sleep(5)
    for job in jobs:
        require_owned(job)
        assert not Path(job['stderr']).read_text(encoding='utf-8')
    assert [job for job in read(registry_path) if job['round'] not in (73, 74)] == retained
    assert native_process.is_running() and native_process.create_time() == native_identity['create_time']
    for path, expected in proof['source_sha256'].items():
        assert sha(path) == expected
    create(out / 'verification.json', {
        'status': 'passed_owned_unstarted_canonical_release_and_candidate_source_handoff',
        'jobs': jobs, 'stopped_owned_processes': stopped, 'untouched_actual_wide_training': native_identity,
        'all_other_registry_jobs_unchanged': True, 'original_frozen_sources_preserved': True,
        'actual_correct73_74_publication_and_candidate_sources_required': True,
        'only_publication_branch': 'main', 'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})
    print(json.dumps({'status': 'passed', 'new_fm_root_pids': [job['pid'] for job in jobs]}), flush=True)


if __name__ == '__main__':
    main()
