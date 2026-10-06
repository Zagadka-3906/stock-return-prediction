"""Replace the positively owned idle publisher with an explicit recovery export."""
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
from handoff_factorization_machine_repaired_workflows_20261005 import processes, stop
from handoff_recovery_qualified_workflows_20261005 import read, sha, create


def main():
    out = A / 'github_validation_sync_main_20261005'
    run_path = out / 'run_v3.json'
    assert not run_path.exists()
    handoff = read(A / 'recovery_qualified_workflow_handoff_20261005/verification.json')
    old = next(j for j in handoff['jobs'] if j['label'] == 'main_publisher')
    processes(old)
    assert not subprocess.check_output(['git', 'status', '--porcelain'],
        cwd=ROOT.parent / '赛题五_GitHub验证同步_20261005')
    launcher = A / 'run_recovery_qualified_workflow_20261005.py'
    driver = A / 'watch_validations_main_v3_20261005.py'
    arguments = [str(A / 'watch_validations_main_v2_20261005.py')]
    sources = (Path(__file__), launcher, driver,
        A / 'recovered_round66_publication_adapter_20261005.py',
        A / 'qualified_round_recovery_evidence_20261005.py',
        A / 'qualified_round_recovery_evidence_v2_20261005.py',
        A / 'standalone_root_source_adapter_20261005.py',
        A / 'standalone_root_source_adapter_preflight_20261005/verification.json',
        A / 'watch_validations_main_v2_20261005.py',
        A / 'sync_validated_rounds_main_20261005.py')
    create(run_path, {'status': 'frozen_before_explicit_actual_recovery_export',
        'original_driver': str(driver), 'original_arguments': arguments,
        'input_sha256': {str(p): sha(p) for p in sources}, 'previous_job': old,
        'only_publication_branch': 'main', 'original_scientific_scopes_preserved': True})
    stopped = stop(old)
    stdout = A / 'run_logs/main_publisher_recovery_export_v3_20261005.stdout.log'
    stderr = A / 'run_logs/main_publisher_recovery_export_v3_20261005.stderr.log'
    env = dict(os.environ)
    for key in ('TMP', 'TEMP', 'TMPDIR'):
        env[key] = str(A / 'runtime_scratch/recovery_qualified_workflows_20261005')
    args = [str(driver), str(run_path), *arguments]
    with stdout.open('xb') as output, stderr.open('xb') as error:
        process = subprocess.Popen([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8',
            str(launcher), *args], cwd=ROOT, env=env, stdout=output, stderr=error,
            creationflags=subprocess.CREATE_NO_WINDOW)
    job = {'pid': process.pid, 'script': str(launcher), 'script_args': args,
        'stdout': str(stdout), 'stderr': str(stderr), 'at_local': datetime.now().isoformat()}
    time.sleep(5)
    processes(job)
    assert not stderr.read_text(encoding='utf-8')
    receipt = {'status': 'passed_owned_idle_main_recovery_export_handoff',
        'stopped_owned_processes': stopped, 'publisher': job,
        'owner': read(out / 'owner.lock'), 'only_publication_branch': 'main',
        'actual_R66_scientific_job_untouched': True, 'new_quality_scores': 0}
    create(out / 'launch_v3.json', receipt)
    print(json.dumps({'status': receipt['status'], 'publisher_pid': process.pid}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
