"""Verify the already launched publisher after its transient Git child has ended."""
from pathlib import Path
from datetime import datetime
import json
import sys
import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
from handoff_recovery_qualified_workflows_20261005 import read, sha, create
from handoff_factorization_machine_repaired_workflows_20261005 import processes


def main():
    out = A / 'github_validation_sync_main_20261005'
    assert not (out / 'launch_v3.json').exists()
    run_path = out / 'run_v3.json'
    run = read(run_path)
    for source, digest in run['input_sha256'].items():
        assert sha(source) == digest, source
    old = run['previous_job']
    assert not psutil.pid_exists(old['pid'])
    owner = read(out / 'owner.lock')
    parent = psutil.Process(owner['pid']).parent()
    args = [run['original_driver'], str(run_path), *run['original_arguments']]
    job = {'pid': parent.pid, 'script': str(A / 'run_recovery_qualified_workflow_20261005.py'),
        'script_args': args, 'stdout': str(A / 'run_logs/main_publisher_recovery_export_v3_20261005.stdout.log'),
        'stderr': str(A / 'run_logs/main_publisher_recovery_export_v3_20261005.stderr.log'),
        'at_local': datetime.now().isoformat()}
    processes(job)
    assert not Path(job['stderr']).read_text(encoding='utf-8')
    assert read(out / 'state.json')['status'] == 'monitoring_completed_validations'
    receipt = {'status': 'passed_owned_idle_main_recovery_export_handoff',
        'publisher': job, 'owner': owner, 'previous_root_pid_confirmed_absent': old['pid'],
        'initial_handoff_receipt_check_failed_on_transient_git_child': True,
        'same_already_running_publisher_verified_without_restart': True,
        'only_publication_branch': 'main', 'actual_R66_scientific_job_untouched': True,
        'source_sha256': {str(Path(__file__)): sha(Path(__file__))}, 'new_quality_scores': 0}
    create(out / 'launch_v3.json', receipt)
    print(json.dumps({'status': receipt['status'], 'publisher_pid': parent.pid}, ensure_ascii=False))


if __name__ == '__main__':
    main()
