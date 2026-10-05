"""Restart only a verified terminal future workflow with a corrected direct router."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess

import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def create(path, payload):
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(payload, stream, ensure_ascii=False, indent=2)


def main():
    old_job = read(A / 'factorization_machine_followup_launch_receipt_20261005.json')['future']
    assert not psutil.pid_exists(old_job['pid']), 'Do not restart a live future controller.'
    failed = A / 'factorization_machine_future_qa_20261005'
    assert read(failed / 'resource_summary.json')['failure'] == "KeyError: 'hidden'"
    assert "KeyError: 'hidden'" in Path(old_job['stderr']).read_text(encoding='utf-8')
    proof = A / 'factorization_machine_direct_router_preflight_v2_20261005/verification.json'
    checked = read(proof)
    assert checked['status'] == 'passed' and len(checked['checks']) == 30
    for source, value in checked['source_sha256'].items():
        assert sha(source) == value, source
    storage = read(A / 'factorization_machine_storage_20261005.json')
    bank = Path(storage['output_directory'])
    assert read(bank / 'training_execution_scope.json')['status'] == 'passed'
    assert read(bank / 'oof_audit.json')['actual_annual_fits'] == 30
    existing = sorted(bank.glob('*/info_2025.json'))
    assert len(existing) == 1 and read(existing[0])['model'] == 'rank_fm_k0_e32'
    assert read(existing[0])['completed_training_epochs'] == 32
    script = A / 'verify_factorization_machine_full_future_v2_20261005.py'
    sources = {script, Path(__file__), proof, A / 'factorization_machine_model_sources_v2_20261005.py',
               A / 'train_factorization_machine_bank_20261005.py', bank / 'protocol.json',
               bank / 'training_execution_scope.json', bank / 'oof_audit.json', *existing,
               failed / 'protocol.json', failed / 'resource_summary.json', Path(old_job['stderr'])}
    bindings = {str(path.resolve()): sha(path) for path in sources}
    create(A / 'factorization_machine_future_run_v2_20261005.json', {
        'status': 'frozen_before_repaired_fullfuture_execution',
        'at_local': datetime.datetime.now().isoformat(), 'input_sha256': bindings,
        'actual30_annual_models_preserved': True, 'existing_actual32_epoch_final_models': 1,
        'remaining_new32_epoch_final_fits': 5, 'fullfuture_controls_still_required_for_all6': True,
        'original_failed_workflow_and_resources_preserved': True,
        'failure_is_dispatch_error_not_physical_resource_exhaustion': True,
        'new_quality_scores': 0, 'test_labels_read': False})
    env = dict(os.environ)
    for name in ('TMP', 'TEMP', 'TMPDIR'):
        env[name] = storage['temporary_directory']
    for name in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'POLARS_MAX_THREADS'):
        env[name] = '8'
    stdout = A / 'run_logs/factorization_machine_full_future_v2_20261005.stdout.log'
    stderr = A / 'run_logs/factorization_machine_full_future_v2_20261005.stderr.log'
    with stdout.open('xb') as output, stderr.open('xb') as error:
        process = subprocess.Popen([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8', str(script)],
            cwd=ROOT, env=env, stdout=output, stderr=error, creationflags=subprocess.CREATE_NO_WINDOW)
    receipt = {'pid': process.pid, 'script': str(script), 'script_args': [],
               'stdout': str(stdout), 'stderr': str(stderr),
               'at_local': datetime.datetime.now().isoformat(), 'input_sha256': bindings,
               'new_quality_scores': 0, 'test_labels_read': False}
    create(A / 'factorization_machine_future_launch_v2_20261005.json', receipt)
    print(json.dumps({'status': 'launched_repaired_fullfuture', 'pid': process.pid}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
