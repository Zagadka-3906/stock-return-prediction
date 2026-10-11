"""Restore the declared GOSS scratch environment after a terminal launch error."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import os
import time

import psutil
from windows_hidden_process_launch_20261006 import launch

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
PREVIOUS = A / 'system_reboot_workflow_recovery_20261006/gradient_sampling_native'
OUT = A / 'system_reboot_workflow_recovery_20261006/gradient_sampling_native_v2'


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def create(path, value):
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    assert not OUT.exists()
    old_execution = json.loads((PREVIOUS / 'execution.json').read_text(encoding='utf-8'))
    assert old_execution['status'] == 'failed' and old_execution['failure'].startswith('AssertionError')
    old_launch = json.loads((PREVIOUS / 'launch.json').read_text(encoding='utf-8'))
    for pid in (old_launch['pid'], old_launch['owned_worker_pid']):
        if psutil.pid_exists(pid):
            process = psutil.Process(pid)
            assert old_launch['script'] not in process.cmdline(), 'Do not duplicate a live original job.'
    old_run = json.loads((PREVIOUS / 'run.json').read_text(encoding='utf-8'))
    storage = A / 'gradient_sampling_storage_20261005.json'
    scratch = Path(json.loads(storage.read_text(encoding='utf-8'))['temporary_directory'])
    assert scratch.drive.upper() in ('D:', 'E:')
    scratch.mkdir(parents=True, exist_ok=True)
    assert not (A / 'gradient_sampling_bank_20261005/training_execution_scope.json').exists()
    OUT.mkdir()
    sources = {str(path.resolve()): sha(path) for path in (
        Path(__file__), A / 'windows_hidden_process_launch_20261006.py',
        A / 'recovery_terminal_window_fix_20261006/verified_hidden_launch.json', storage,
        PREVIOUS / 'run.json', PREVIOUS / 'execution.json', PREVIOUS / 'stderr.log')}
    run = dict(old_run)
    run.update(name='gradient_sampling_native_v2',
               input_sha256={**old_run['input_sha256'], **sources},
               original_attempt_terminal_failure_preserved=True,
               restored_frozen_TMP_TEMP_TMPDIR=str(scratch))
    create(OUT / 'run.json', run)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1',
               OMP_NUM_THREADS='8', OPENBLAS_NUM_THREADS='8', MKL_NUM_THREADS='8', POLARS_MAX_THREADS='8')
    for name in ('TMP', 'TEMP', 'TMPDIR'):
        env[name] = str(scratch)
    arguments = [str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8',
                 str(A / 'run_reboot_recovery_attempt_20261006.py'), str(OUT / 'run.json')]
    with (OUT / 'stdout.log').open('xb') as out, (OUT / 'stderr.log').open('xb') as err:
        process = launch(arguments, cwd=ROOT, env=env, stdout=out, stderr=err)
    time.sleep(1)
    assert process.poll() is None, (OUT / 'stderr.log').read_text(encoding='utf-8')
    parent = psutil.Process(process.pid)
    children = [p for p in parent.children(recursive=True)
                if p.name().lower() == 'python.exe' and p.cmdline()[1:] == parent.cmdline()[1:]]
    assert len(children) == 1
    row = {'name': run['name'], 'pid': process.pid,
        'script': str(A / 'run_reboot_recovery_attempt_20261006.py'), 'script_args': [str(OUT / 'run.json')],
        'owned_worker_pid': children[0].pid, 'owned_worker_creation_time': children[0].create_time(),
        'stdout': str(OUT / 'stdout.log'), 'stderr': str(OUT / 'stderr.log'),
        'at_local': datetime.now().isoformat(timespec='seconds'), 'original_script': run['original_script'],
        'original_arguments': run['original_arguments'], 'hidden_consoleless_launch_verified': True}
    create(OUT / 'launch.json', row)
    create(OUT / 'verification.json', {'status': 'passed_terminal_launch_error_repaired_with_original_frozen_scratch_and_hidden_process',
        'job': row, 'input_sha256': sources, 'original_model_configuration_and_native_sources_unchanged': True,
        'new_model_fits_by_launcher': 0, 'new_quality_scores_by_launcher': 0, 'test_labels_read': False})
    print(json.dumps(row, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
