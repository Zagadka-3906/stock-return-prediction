"""Choose an authorized drive and launch a memory-reserved training-only experiment."""
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
    output = ROOT / 'analysis/nystrom_tuning_bank_20261005' if selected == 'D:/' else Path('E:/赛题五计算存储/nystrom_tuning_bank_20261005')
    scratch = ROOT / 'tmp/nystrom_tuning_20261005' if selected == 'D:/' else Path('E:/赛题五计算存储/tmp/nystrom_tuning_20261005')
    output.mkdir(parents=True, exist_ok=True)
    scratch.mkdir(parents=True, exist_ok=True)
    create(ROOT / 'analysis/nystrom_tuning_storage_20261005.json', {
        'status': 'selected_authorized_data_drive', 'at_local': datetime.datetime.now().isoformat(),
        'drive_free_bytes_at_selection': usage, 'D_to_E_fallback_threshold_bytes': threshold,
        'threshold_is_storage_policy_not_physical_limit': True,
        'output_directory': str(output), 'temporary_directory': str(scratch),
        'user_authorized_E_if_D_insufficient': True, 'project_data_on_C_forbidden': True})
    script = ROOT / 'analysis/run_nystrom_tuning_bank_20261005.py'
    sources = [Path(__file__), script, ROOT / 'analysis/train_nystrom_tuning_bank_20261005.py',
               ROOT / 'analysis/verify_nystrom_tuning_bank_20261005.py']
    digests = {}
    for path in sources:
        with path.open('rb') as stream:
            digests[str(path)] = hashlib.file_digest(stream, 'sha256').hexdigest()
    logs = ROOT / 'analysis/run_logs'
    stdout, stderr = logs / 'nystrom_tuning_bank_20261005.stdout.log', logs / 'nystrom_tuning_bank_20261005.stderr.log'
    env = os.environ.copy()
    for key in ('TMP', 'TEMP', 'TMPDIR'):
        env[key] = str(scratch)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'POLARS_MAX_THREADS'):
        env[key] = '8'
    with stdout.open('xb') as out, stderr.open('xb') as error:
        process = subprocess.Popen([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8', str(script)],
            cwd=ROOT, env=env, stdout=out, stderr=error, creationflags=subprocess.CREATE_NO_WINDOW)
    create(ROOT / 'analysis/nystrom_tuning_bank_run_20261005.json', {
        'status': 'launched_numerical_preflight_then_memory_reserved_annual_training',
        'at_local': datetime.datetime.now().isoformat(), 'pid': process.pid,
        'script': str(script), 'stdout': str(stdout), 'stderr': str(stderr), 'input_sha256': digests,
        'planned_configurations': 10, 'planned_annual_fits': 50,
        'fulltraining_future_and_complete_output_official_scores_are_separate_pending_steps': True,
        'test_labels_read': False})
    print(json.dumps({'status': 'launched', 'pid': process.pid, 'output_directory': str(output)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
