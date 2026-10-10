"""Queue actual self-contained rank and return composite artifact construction."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import time

import psutil

ROOT = Path(__file__).resolve().parents[1]


def create(path, value):
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    threshold = 20 * 2**30
    usage = {drive: psutil.disk_usage(drive).free for drive in ('D:/', 'E:/')}
    selected = 'D:/' if usage['D:/'] >= threshold else 'E:/'
    assert usage[selected] >= threshold
    output = ROOT / 'analysis/linear_leaf_ensemble_bank_20261005' if selected == 'D:/' else Path('E:/赛题五计算存储/linear_leaf_ensemble_bank_20261005')
    scratch = ROOT / 'tmp/linear_leaf_ensemble_20261005' if selected == 'D:/' else Path('E:/赛题五计算存储/tmp/linear_leaf_ensemble_20261005')
    output.mkdir(parents=True, exist_ok=True)
    scratch.mkdir(parents=True, exist_ok=True)
    storage = ROOT / 'analysis/linear_leaf_ensemble_storage_20261005.json'
    create(storage, {'status': 'selected_authorized_data_drive', 'output_directory': str(output),
        'temporary_directory': str(scratch), 'drive_free_bytes_at_selection': usage,
        'D_to_E_threshold_bytes': threshold, 'threshold_is_storage_policy': True,
        'user_authorized_E_if_D_insufficient': True, 'project_data_on_C_forbidden': True})
    script = ROOT / 'analysis/run_linear_leaf_ensemble_bank_20261005.py'
    sources = [Path(__file__), script, ROOT / 'analysis/build_linear_leaf_ensemble_bank_20261005.py',
        ROOT / 'analysis/linear_leaf_ensemble_complete_search_plan_20261005.json', storage,
        ROOT / 'analysis/linear_leaf_ensemble_complementarity_v2_20261005/verification.json']
    bindings = {}
    for source in sources:
        if source.suffix == '.py':
            compile(source.read_text(encoding='utf-8'), str(source), 'exec')
        with source.open('rb') as stream:
            bindings[str(source)] = hashlib.file_digest(stream, 'sha256').hexdigest()
    env = os.environ.copy()
    for key in ('TMP', 'TEMP', 'TMPDIR'):
        env[key] = str(scratch)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):
        env[key] = '8'
    stdout = ROOT / 'analysis/run_logs/linear_leaf_ensemble_bank_20261005.stdout.log'
    stderr = ROOT / 'analysis/run_logs/linear_leaf_ensemble_bank_20261005.stderr.log'
    with stdout.open('xb') as output_stream, stderr.open('xb') as error:
        process = subprocess.Popen([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8', str(script)],
            cwd=ROOT, env=env, stdout=output_stream, stderr=error, creationflags=subprocess.CREATE_NO_WINDOW)
    create(ROOT / 'analysis/linear_leaf_ensemble_bank_run_20261005.json', {
        'status': 'launched_waiting_for_actual30_parent_annual_fits_then40_composite_outputs',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'pid': process.pid, 'script': str(script),
        'stdout': str(stdout), 'stderr': str(stderr), 'input_sha256': bindings,
        'planned_virtual_configs': 8, 'planned_virtual_annual_outputs': 40,
        'planned_new_native_fits': 0, 'fullfuture_and_official_scheme_quality_are_separate_pending_steps': True,
        'test_labels_read': False})
    print(json.dumps({'status': 'actual_virtual_bank_waiter_launched', 'pid': process.pid,
        'new_native_fits': 0}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
