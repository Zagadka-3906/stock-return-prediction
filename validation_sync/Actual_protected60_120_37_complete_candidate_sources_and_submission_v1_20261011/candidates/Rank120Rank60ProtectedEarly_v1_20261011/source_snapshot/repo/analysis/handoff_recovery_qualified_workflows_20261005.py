"""Hand off only owned unstarted jobs, plus the main publisher and observer."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import os
import subprocess
import sys
import time
import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
OUT = A / 'recovery_qualified_workflow_handoff_20261005'
sys.path.insert(0, str(A))
from handoff_factorization_machine_repaired_workflows_20261005 import processes, stop


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def create(path, value):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)


def main():
    assert not OUT.exists(), 'Inspect existing handoff; never duplicate live jobs.'
    proof_path = A / 'recovery_qualification_bridge_preflight_20261005/verification.json'
    proof = read(proof_path)
    assert proof['status'].startswith('passed')
    for path, digest in proof['source_sha256'].items():
        assert sha(path) == digest, path
    registry_path = A / 'resumed_rounds_nystrom_locked_20261004.json'
    registry = read(registry_path)
    rows = [job for job in registry if 67 <= job['round'] <= 74]
    assert len(rows) == 8
    for job in rows:
        number = job['round']
        assert not (A / f'optimization_20261003_r{number}/protocol.json').exists()
        assert read(A / f'ongoing_optimization_r{number}_state.json')['stage'].startswith('waiting')
    native = read(A / 'neural16384_full_launch_receipt_20261005.json')
    assert not (A / 'neural16384_full_bank_20261005/protocol.json').exists()
    publisher_pid = read(A / 'github_validation_sync_main_20261005/owner.lock')['pid']
    publisher = {'pid': psutil.Process(publisher_pid).parent().pid,
                 'script': str(A / 'watch_validations_main_v2_20261005.py'), 'script_args': []}
    monitor = read(A / 'actual_optimization_monitor_run_v9_20261005.json')
    old_jobs = [('neural16384_annual', native), *[(f'round{j["round"]}', j) for j in rows],
                ('main_publisher', publisher), ('operational_monitor', monitor)]
    for _, job in old_jobs:
        processes(job)
    worktree = ROOT.parent / '赛题五_GitHub验证同步_20261005'
    assert not subprocess.check_output(['git', 'status', '--porcelain'], cwd=worktree)
    for number in range(63, 75):
        protocol = A / f'optimization_20261003_r{number}/protocol.json'
        if protocol.exists():
            assert str(registry_path) not in read(protocol)['input_sha256']
    science = read(A / 'round66_root_source_recovery_launch_20261005.json')
    assert science['script'] in psutil.Process(science['pid']).cmdline()
    bindings = {str(p): sha(p) for p in (Path(__file__), proof_path,
        A / 'neural16384_full_launch_receipt_20261005.json',
        A / 'neural16384_full_run_20261005.json',
        A / 'actual_optimization_monitor_run_v9_20261005.json',
        A / 'github_validation_sync_main_20261005/run_v2.json',
        A / 'round66_root_source_recovery_launch_20261005.json')}
    create(OUT / 'frozen_before_handoff.json', {'status': 'frozen_before_owned_unstarted_handoff',
        'input_sha256': bindings, 'old_jobs': old_jobs, 'actual_R66_recovery': science,
        'original_frozen_sources_protocols_and_failed_proofs_preserved': True,
        'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})
    for number in range(67, 75):
        (OUT / f'prior_round{number}_state.json').write_bytes((A / f'ongoing_optimization_r{number}_state.json').read_bytes())
    stopped = []
    for label, job in old_jobs:
        stopped.extend(stop(job))
        print(f'stopped owned unstarted/operational {label}', flush=True)
    env = dict(os.environ)
    scratch = ROOT / 'analysis/runtime_scratch/recovery_qualified_workflows_20261005'
    scratch.mkdir(parents=True, exist_ok=True)
    assert scratch.drive.upper() in ('D:', 'E:')
    for key in ('TMP', 'TEMP', 'TMPDIR'):
        env[key] = str(scratch)
    for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'POLARS_MAX_THREADS'):
        env[key] = '8'
    launcher = A / 'run_recovery_qualified_workflow_20261005.py'
    sources = (launcher, Path(__file__), proof_path,
        A / 'qualified_round_recovery_evidence_20261005.py',
        A / 'qualified_round_recovery_evidence_v2_20261005.py',
        A / 'standalone_root_source_adapter_20261005.py',
        A / 'standalone_root_source_adapter_preflight_20261005/verification.json',
        A / 'locked_read_hash_cache_20261004.py',
        A / 'frozen_provenance_execution_scope_20261004.py')
    jobs = []
    for label, old in old_jobs:
        original = Path(old['script']).resolve()
        arguments = old.get('script_args', [])
        run_path = OUT / f'{label}_run.json'
        create(run_path, {'status': 'frozen_before_actual_recovery_qualified_driver',
            'original_driver': str(original), 'original_arguments': arguments,
            'input_sha256': {str(p): sha(p) for p in (*sources, original)},
            'previous_job': old, 'only_publication_branch': 'main',
            'all_original_scientific_gates_preserved': True,
            'actual_closed_R66_recovery_required': True, 'test_labels_read': False})
        stdout = A / f'run_logs/{label}_recovery_qualified_20261005.stdout.log'
        stderr = A / f'run_logs/{label}_recovery_qualified_20261005.stderr.log'
        args = [str(original), str(run_path), *arguments]
        with stdout.open('xb') as output, stderr.open('xb') as error:
            process = subprocess.Popen([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8',
                str(launcher), *args], cwd=ROOT, env=env, stdout=output, stderr=error,
                creationflags=subprocess.CREATE_NO_WINDOW)
        job = {'label': label, 'pid': process.pid, 'script': str(launcher), 'script_args': args,
            'stdout': str(stdout), 'stderr': str(stderr), 'run': str(run_path),
            'at_local': datetime.now().isoformat(), 'previous_root_pid': old['pid']}
        if 'round' in old:
            job.update(round=old['round'], expected_scored_records=old['expected_scored_records'],
                status='waiting_for_actual_native_gates_and_recovery_qualified_predecessor')
        jobs.append(job)
    updated = [j for j in registry if not 67 <= j['round'] <= 74] + [j for j in jobs if 'round' in j]
    temporary = registry_path.with_suffix('.recovery_qualified.tmp')
    temporary.write_text(json.dumps(updated, ensure_ascii=False, indent=2), encoding='utf-8')
    temporary.replace(registry_path)
    time.sleep(8)
    for job in jobs:
        processes(job)
        assert not Path(job['stderr']).read_text(encoding='utf-8'), job['stderr']
    assert science['script'] in psutil.Process(science['pid']).cmdline()
    for path, digest in bindings.items():
        assert sha(path) == digest, path
    receipt = {'status': 'passed_owned_unstarted_and_operational_handoff',
        'at_local': datetime.now().isoformat(), 'jobs': jobs,
        'stopped_owned_processes': stopped, 'actual_R66_recovery_untouched': science,
        'new_main_owner': read(A / 'github_validation_sync_main_20261005/owner.lock'),
        'only_publication_branch': 'main', 'new_model_fits_by_handoff': 0,
        'new_quality_scores_by_handoff': 0, 'test_labels_read': False}
    create(OUT / 'verification.json', receipt)
    print(json.dumps({'status': receipt['status'], 'new_root_pids': [j['pid'] for j in jobs]}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
