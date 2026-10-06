"""Freeze and launch the full16384 experiment after independent actual controls."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess

import psutil

ROOT = Path(__file__).resolve().parents[1]


def create(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    run_path = ROOT / 'analysis/neural16384_full_run_20261005.json'
    assert not run_path.exists(), 'Inspect the existing live handle; never launch a duplicate.'
    free = {drive: psutil.disk_usage(drive).free for drive in ('D:/', 'E:/')}
    threshold = 20 * 2**30
    drive = 'D:/' if free['D:/'] >= threshold else 'E:/'
    assert free[drive] >= threshold
    output = ROOT / 'analysis/neural16384_full_bank_20261005' if drive == 'D:/' else Path('E:/赛题五计算存储/neural16384_full_bank_20261005')
    scratch = ROOT / 'tmp/neural16384_full_20261005' if drive == 'D:/' else Path('E:/赛题五计算存储/tmp/neural16384_full_20261005')
    output.mkdir(parents=True, exist_ok=True)
    scratch.mkdir(parents=True, exist_ok=True)
    storage = ROOT / 'analysis/neural16384_full_storage_20261005.json'
    create(storage, {'status': 'selected_authorized_data_drive',
        'at_local': datetime.datetime.now().isoformat(), 'drive_free_bytes_at_selection': free,
        'output_directory': str(output), 'temporary_directory': str(scratch),
        'D_to_E_threshold_bytes': threshold, 'storage_threshold_is_not_physical_exhaustion': True,
        'user_authorized_E_fallback': True, 'project_data_on_C_forbidden': True})
    env = os.environ.copy()
    for key in ('TMP', 'TEMP', 'TMPDIR'):
        env[key] = str(scratch)
    for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'POLARS_MAX_THREADS'):
        env[key] = '8'
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    preflight = ROOT / 'analysis/verify_neural16384_full_preflight_20261005.py'
    python = str(ROOT / '.venv/Scripts/python.exe')
    subprocess.run([python, '-B', '-X', 'utf8', str(preflight)], cwd=ROOT, env=env, check=True)
    proof = ROOT / 'analysis/neural16384_full_preflight_20261005/verification.json'
    verification = json.loads(proof.read_text(encoding='utf-8'))
    assert verification['status'] == 'passed_actual_matched_instrumentation_and_architecture_controls'
    sources = [Path(__file__), preflight, proof, storage,
        ROOT / 'analysis/run_neural16384_full_bank_20261005.py',
        ROOT / 'analysis/train_neural16384_full_bank_20261005.py',
        ROOT / 'analysis/neural16384_actual_resource_recorder_20261005.py',
        ROOT / 'analysis/train_diverse_backbones_20261003.py',
        ROOT / 'analysis/frozen_provenance_execution_scope_20261004.py',
        ROOT / 'analysis/locked_read_hash_cache_20261004.py']
    bindings = {str(path): sha(path) for path in sources}
    script = ROOT / 'analysis/run_neural16384_full_bank_20261005.py'
    stdout = ROOT / 'analysis/run_logs/neural16384_full_20261005.stdout.log'
    stderr = ROOT / 'analysis/run_logs/neural16384_full_20261005.stderr.log'
    create(run_path, {'status': 'frozen_before_waiting_for_qualified66_then_five_actual_full_fits',
        'at_local': datetime.datetime.now().isoformat(), 'script': str(script),
        'stdout': str(stdout), 'stderr': str(stderr), 'input_sha256': bindings,
        'planned_annual_fits': 5, 'epochs_each_actual_full_fit': 32,
        'planned_fulltraining_and_complete_scheme_quality_are_separate_pending_steps': True,
        'one_step_pilot_is_not_full_training_evidence': True, 'test_labels_read': False})
    with stdout.open('xb') as out, stderr.open('xb') as error:
        process = subprocess.Popen([python, '-B', '-X', 'utf8', str(script)],
            cwd=ROOT, env=env, stdout=out, stderr=error, creationflags=subprocess.CREATE_NO_WINDOW)
    create(ROOT / 'analysis/neural16384_full_launch_receipt_20261005.json', {
        'status': 'passed_actual_controls_and_owned_lazy_waiter_launched',
        'at_local': datetime.datetime.now().isoformat(), 'pid': process.pid,
        'script': str(script), 'stdout': str(stdout), 'stderr': str(stderr),
        'output_directory': str(output), 'actual_full16384_annual_fits': 0,
        'new_quality_scores': 0, 'test_labels_read': False})
    print(json.dumps({'status': 'launched_verified_preflight_then_lazy_full16384_training',
        'pid': process.pid, 'output_directory': str(output)}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
