"""Publish completed branch controls and start the main-only validation observer."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
import watch_validations_main_20261005 as watcher
sync = watcher.sync


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def create(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    verification = ROOT / 'analysis/github_main_consolidation_20261005/verification.json'
    proof = sync.read(verification)
    assert proof['status'] == 'passed_main_push_and_only_main_remains'
    assert sync.git('ls-remote', '--heads', 'origin').splitlines() == [f"{proof['commit']}\trefs/heads/main"]
    assert not sync.git('status', '--porcelain', '--untracked-files=no')
    assert not (sync.OUT / 'owner.lock').exists()
    sync.OUT.mkdir(exist_ok=True)
    script = ROOT / 'analysis/watch_validations_main_20261005.py'
    delegate = ROOT / 'analysis/sync_validated_rounds_main_20261005.py'
    run_path = sync.OUT / 'run.json'
    create(run_path, {'status': 'frozen_before_main_watcher_launch', 'at_local': sync.now(),
        'branch': 'main', 'worktree': str(sync.WORKTREE), 'publisher_worktree_detached': True,
        'history_rounds1_to61_already_on_main': True,
        'input_sha256': {str(p): digest(p) for p in (script, delegate, Path(__file__), verification)},
        'continues_future_qualified_round_auto_sync': True,
        'project_temp_drive': 'D', 'E_fallback_authorized': True})
    prefix = Path('validation_sync/main_consolidation_20261005')
    paths = []
    originals = [verification, run_path, Path(__file__)]
    for source in originals:
        relative = source.relative_to(ROOT)
        destination = relative if source.suffix == '.py' else prefix / relative
        data = source.read_bytes()
        assert not sync.SECRET.search(data)
        sync.atomic(sync.WORKTREE / destination, data)
        paths.append(destination.as_posix())
    sync.git('add', '--', *paths)
    assert set(sync.git('diff', '--cached', '--name-only').splitlines()) == set(paths)
    for source in originals[:-1]:
        relative = (prefix / source.relative_to(ROOT)).as_posix()
        blob = subprocess.check_output(['git', 'show', ':' + relative], cwd=sync.WORKTREE)
        assert sync.sha(blob) == digest(source)
    sync.git('commit', '-m', '记录main合并核验并冻结后续逐轮同步器')
    commit = sync.git('rev-parse', 'HEAD')
    sync.git('push', 'origin', 'HEAD:refs/heads/main')
    assert sync.git('ls-remote', '--heads', 'origin').splitlines() == [f'{commit}\trefs/heads/main']
    watcher.advance_source_index(commit)
    scratch = ROOT / 'tmp/github_main_sync_20261005'
    scratch.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    for key in ('TMP', 'TEMP', 'TMPDIR'):
        env[key] = str(scratch)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    stdout = ROOT / 'analysis/run_logs/github_validation_main_20261005.stdout.log'
    stderr = ROOT / 'analysis/run_logs/github_validation_main_20261005.stderr.log'
    with stdout.open('xb') as output, stderr.open('xb') as error:
        process = subprocess.Popen([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8', str(script)],
            cwd=ROOT, env=env, stdout=output, stderr=error, creationflags=subprocess.CREATE_NO_WINDOW)
    receipt = {'status': 'main_only_pushed_and_watcher_launched', 'at_local': sync.now(),
        'pid': process.pid, 'script': str(script), 'commit': commit, 'branch': 'main',
        'stdout': str(stdout), 'stderr': str(stderr),
        'url': f'https://github.com/Zagadka-3906/stock-return-prediction/commit/{commit}',
        'all_published_files_and_commit_history_preserved': True}
    create(sync.OUT / 'launch_receipt.json', receipt)
    print(json.dumps(receipt, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
