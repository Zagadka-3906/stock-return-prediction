"""Launch closed native evidence publication with frozen code andD/E scratch."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]


def main():
    run = ROOT / 'analysis/linear_leaf_native_github_run_20261005.json'
    assert not run.exists()
    storage = json.loads((ROOT / 'analysis/linear_leaf_storage_20261005.json').read_text(encoding='utf-8'))
    script = ROOT / 'analysis/publish_linear_leaf_completed_native_20261005.py'
    compile(script.read_text(encoding='utf-8'), str(script), 'exec')
    paths = [Path(__file__), script, ROOT / 'analysis/watch_validations_main_v2_20261005.py',
        ROOT / 'analysis/sync_validated_rounds_main_20261005.py',
        ROOT / 'analysis/linear_leaf_storage_20261005.json']
    bindings = {}
    for path in paths:
        with path.open('rb') as stream:
            bindings[str(path)] = hashlib.file_digest(stream, 'sha256').hexdigest()
    env = os.environ.copy()
    for key in ('TMP', 'TEMP', 'TMPDIR'):
        env[key] = storage['temporary_directory']
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    stdout = ROOT / 'analysis/run_logs/linear_leaf_native_github_20261005.stdout.log'
    stderr = ROOT / 'analysis/run_logs/linear_leaf_native_github_20261005.stderr.log'
    with stdout.open('xb') as output, stderr.open('xb') as error:
        process = subprocess.Popen([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8', str(script)],
            cwd=ROOT, env=env, stdout=output, stderr=error, creationflags=subprocess.CREATE_NO_WINDOW)
    with run.open('x', encoding='utf-8') as stream:
        json.dump({'status': 'launched_waiting_for_actual_closed_native_training_and_future_scopes',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'pid': process.pid, 'script': str(script),
            'stdout': str(stdout), 'stderr': str(stderr), 'input_sha256': bindings,
            'only_publication_branch': 'main', 'source_or_training_math_not_changed': True,
            'user_authorized_publish_after_each_completed_validation': True,
            'new_quality_scores': 0, 'test_labels_read': False}, stream, ensure_ascii=False, indent=2)
    print(json.dumps({'status': 'native_scope_publisher_launched', 'pid': process.pid}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
