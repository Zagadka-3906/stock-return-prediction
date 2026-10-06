"""Prespecify first-order andlow-rank factorization grid and launch with scratch on authorizedD/E only."""
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


def main():
    threshold = 20 * 2**30
    usage = {drive: psutil.disk_usage(drive).free for drive in ('D:/', 'E:/')}
    selected = 'D:/' if usage['D:/'] >= threshold else 'E:/'
    assert usage[selected] >= threshold
    output = ROOT / 'analysis/factorization_machine_bank_20261005' if selected == 'D:/' else Path('E:/赛题五计算存储/factorization_machine_bank_20261005')
    scratch = ROOT / 'tmp/factorization_machine_20261005' if selected == 'D:/' else Path('E:/赛题五计算存储/tmp/factorization_machine_20261005')
    output.mkdir(parents=True, exist_ok=True)
    scratch.mkdir(parents=True, exist_ok=True)
    create(ROOT / 'analysis/factorization_machine_storage_20261005.json', {
        'status': 'selected_authorized_data_drive', 'at_local': datetime.datetime.now().isoformat(),
        'drive_free_bytes_at_selection': usage, 'D_to_E_fallback_threshold_bytes': threshold,
        'threshold_is_storage_policy_not_physical_boundary': True,
        'output_directory': str(output), 'temporary_directory': str(scratch),
        'user_authorized_E_if_D_insufficient': True, 'project_data_on_C_forbidden': True})
    script = ROOT / 'analysis/run_factorization_machine_bank_20261005.py'
    sources = [Path(__file__), script, ROOT / 'analysis/train_factorization_machine_bank_20261005.py',
        ROOT / 'analysis/verify_factorization_machine_bank_20261005.py']
    digests = {}
    for source in sources:
        with source.open('rb') as stream:
            digests[str(source)] = hashlib.file_digest(stream, 'sha256').hexdigest()
    logs = ROOT / 'analysis/run_logs'
    stdout, stderr = logs / 'factorization_machine_bank_20261005.stdout.log', logs / 'factorization_machine_bank_20261005.stderr.log'
    env = os.environ.copy()
    for key in ('TMP', 'TEMP', 'TMPDIR'):
        env[key] = str(scratch)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'POLARS_MAX_THREADS'):
        env[key] = '8'
    with stdout.open('xb') as out, stderr.open('xb') as error:
        process = subprocess.Popen([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8', str(script)],
            cwd=ROOT, env=env, stdout=out, stderr=error, creationflags=subprocess.CREATE_NO_WINDOW)
    create(ROOT / 'analysis/factorization_machine_bank_run_20261005.json', {
        'status': 'launched_actual_preflight_then_memory_reserved30_annual_fits',
        'at_local': datetime.datetime.now().isoformat(), 'pid': process.pid, 'script': str(script),
        'stdout': str(stdout), 'stderr': str(stderr), 'input_sha256': digests,
        'planned_configurations': 6, 'planned_annual_fits': 30,
        'fulltraining_future_and_complete_output_official_scores_are_separate_pending_steps': True,
        'test_labels_read': False})
    print(json.dumps({'status': 'launched', 'pid': process.pid,
        'output_directory': str(output)}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
