"""Replace only two owned unstarted FM waiters with correct release dispatch."""
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


def main():
    out = A / 'factorization_machine_release_dispatch_handoff_v5_20261005'
    assert not out.exists()
    proof_path = A / 'factorization_machine_release_dispatch_preflight_v5_20261005/verification.json'
    proof = read(proof_path)
    assert proof['status'].startswith('passed')
    for path, digest in proof['source_sha256'].items():
        assert sha(path) == digest, path
    registry_path = A / 'resumed_rounds_nystrom_locked_20261004.json'
    registry = read(registry_path)
    old = [j for j in registry if j['round'] in (73, 74)]
    assert len(old) == 2
    for job in old:
        processes(job)
        assert not (A / f'optimization_20261003_r{job["round"]}/protocol.json').exists()
        assert read(A / f'ongoing_optimization_r{job["round"]}_state.json')['stage'].startswith('waiting')
    create(out / 'frozen_before_handoff.json', {'status': 'frozen_before_owned_unstarted_handoff',
        'old_jobs': old, 'source_sha256': {str(Path(__file__)): sha(Path(__file__)), str(proof_path): sha(proof_path)},
        'training_parameters_and_actual_native_models_unchanged': True,
        'R66_recovery_and_all_other_jobs_untouched': True, 'new_quality_scores': 0})
    stopped = []
    for job in old:
        stopped.extend(stop(job))
    run_path = A / 'factorization_machine_quality_run_v5_20261005.json'
    inputs = dict(read(A / 'factorization_machine_quality_run_v4_20261005.json')['input_sha256'])
    inputs.update({str(p): sha(p) for p in (
        Path(__file__), proof_path, A / 'run_factorization_machine_round_v5_20261005.py',
        A / 'finalize_training_round73_v5.py', A / 'finalize_training_round74_v5.py')})
    create(run_path, {'status': 'frozen_before_actual_correct_release_dispatch',
        'input_sha256': inputs, 'planned_records': {'73': 124, '74': 138},
        'actual_native30_annual6_final_fullfuture_controls_required': True,
        'same_actual_full_predecessor_requirements': [72, 73], 'test_labels_read': False})
    env = dict(os.environ)
    scratch = Path(read(A / 'factorization_machine_storage_20261005.json')['temporary_directory'])
    for key in ('TMP', 'TEMP', 'TMPDIR'):
        env[key] = str(scratch)
    for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'POLARS_MAX_THREADS'):
        env[key] = '8'
    launcher = A / 'run_recovery_qualified_workflow_20261005.py'
    jobs = []
    for number in (73, 74):
        driver = A / f'run_training_round{number}_v5_pipeline.py'
        job_run = out / f'round{number}_run.json'
        create(job_run, {'original_driver': str(driver), 'original_arguments': [],
            'input_sha256': {str(p): sha(p) for p in (launcher, driver, run_path, proof_path,
                A / 'qualified_round_recovery_evidence_20261005.py',
                A / 'qualified_round_recovery_evidence_v2_20261005.py',
                A / 'standalone_root_source_adapter_20261005.py')}, 'test_labels_read': False})
        stdout = A / f'run_logs/round{number}_factorization_release_v5_20261005.stdout.log'
        stderr = A / f'run_logs/round{number}_factorization_release_v5_20261005.stderr.log'
        args = [str(driver), str(job_run)]
        with stdout.open('xb') as output, stderr.open('xb') as error:
            process = subprocess.Popen([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8', str(launcher), *args],
                cwd=ROOT, env=env, stdout=output, stderr=error, creationflags=subprocess.CREATE_NO_WINDOW)
        jobs.append({'round': number, 'pid': process.pid, 'script': str(launcher), 'script_args': args,
            'stdout': str(stdout), 'stderr': str(stderr), 'at_local': datetime.now().isoformat(),
            'expected_scored_records': 124 if number == 73 else 138,
            'status': 'waiting_for_actual_native_gates_and_complete_predecessor_correct_release'})
    temporary = registry_path.with_suffix('.fm_release_v5.tmp')
    temporary.write_text(json.dumps([j for j in registry if j['round'] not in (73, 74)] + jobs,
        ensure_ascii=False, indent=2), encoding='utf-8')
    temporary.replace(registry_path)
    time.sleep(5)
    for job in jobs:
        processes(job)
        assert not Path(job['stderr']).read_text(encoding='utf-8')
    create(out / 'verification.json', {'status': 'passed_owned_unstarted_release_dispatch_handoff',
        'jobs': jobs, 'stopped_owned_processes': stopped, 'original_frozen_sources_preserved': True,
        'actual_correct73_74_release_required': True, 'only_publication_branch': 'main',
        'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})
    print(json.dumps({'status': 'passed', 'new_fm_root_pids': [j['pid'] for j in jobs]}))


if __name__ == '__main__':
    main()
