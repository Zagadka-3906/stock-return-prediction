"""Queue the native future controls without editing a frozen active training source."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import datetime

ROOT = Path(__file__).resolve().parents[1]


def main():
    storage = json.loads((ROOT / 'analysis/nystrom_tuning_storage_20261005.json').read_text(encoding='utf-8'))
    script = ROOT / 'analysis/verify_nystrom_tuning_future_20261005.py'
    compile(script.read_text(encoding='utf-8'), str(script), 'exec')
    env = os.environ.copy()
    for key in ('TMP', 'TEMP', 'TMPDIR'):
        env[key] = storage['temporary_directory']
    for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'POLARS_MAX_THREADS'):
        env[key] = '8'
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    sources = [Path(__file__), script, ROOT / 'analysis/train_nystrom_tuning_bank_20261005.py']
    hashes = {}
    for source in sources:
        with source.open('rb') as stream:
            hashes[str(source)] = hashlib.file_digest(stream, 'sha256').hexdigest()
    stdout = ROOT / 'analysis/run_logs/nystrom_tuning_future_20261005.stdout.log'
    stderr = ROOT / 'analysis/run_logs/nystrom_tuning_future_20261005.stderr.log'
    with stdout.open('xb') as output, stderr.open('xb') as error:
        process = subprocess.Popen([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8', str(script)],
            cwd=ROOT, env=env, stdout=output, stderr=error, creationflags=subprocess.CREATE_NO_WINDOW)
    receipt = {'status': 'waiting_for_actual50_annual_fits_and_then_native_future_controls',
        'at_local': datetime.datetime.now().isoformat(), 'pid': process.pid, 'script': str(script),
        'stdout': str(stdout), 'stderr': str(stderr), 'input_sha256': hashes,
        'planned_fulltraining_fits': 10, 'new_quality_scores': 0, 'test_labels_read': False}
    with (ROOT / 'analysis/nystrom_tuning_future_run_20261005.json').open('x', encoding='utf-8') as stream:
        json.dump(receipt, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    print(json.dumps({'status': receipt['status'], 'pid': process.pid}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
