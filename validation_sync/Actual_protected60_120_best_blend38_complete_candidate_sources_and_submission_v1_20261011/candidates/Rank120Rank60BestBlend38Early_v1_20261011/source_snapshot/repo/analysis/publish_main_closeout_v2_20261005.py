"""Close the remaining main-only publication gap without changing scientific jobs."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

import psutil

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
import watch_validations_main_v2_20261005 as watcher

sync = watcher.sync
PREFIX = Path('validation_sync/main_closeout_v2_20261005')
OUT = ROOT / 'analysis/main_closeout_v2_20261005'
QA = ROOT / 'analysis/factorization_machine_publication_blob_qa_20261005'


def names(*args):
    raw = subprocess.check_output(['git', *args, '-z'], cwd=ROOT)
    return {item.decode('utf-8') for item in raw.split(b'\0') if item}


def blob_hashes(commit, paths):
    paths = sorted(paths)
    request = ''.join(f'{commit}:{path}\n' for path in paths).encode('utf-8')
    response = subprocess.run(['git', 'cat-file', '--batch'], cwd=ROOT,
                              input=request, capture_output=True, check=True).stdout
    offset, result = 0, {}
    for path in paths:
        end = response.index(b'\n', offset)
        header = response[offset:end].split()
        assert len(header) == 3 and header[1] == b'blob', path
        start, size = end + 1, int(header[2])
        result[path] = hashlib.sha256(response[start:start + size]).hexdigest()
        offset = start + size + 1
    assert offset == len(response)
    return result


def owned_publisher(root_pid, script):
    parent = psutil.Process(root_pid)
    assert str(script) in parent.cmdline(), root_pid
    children = [p for p in parent.children(recursive=True)
                if p.name().lower() == 'python.exe' and p.cmdline()[1:] == parent.cmdline()[1:]]
    assert len(children) == 1, root_pid
    return parent, children[0]


def main():
    OUT.mkdir(exist_ok=True)
    assert not (OUT / 'receipt.json').exists()
    prior_receipt = sync.read(sync.OUT / 'factorization_machine_workflow_receipt.json')
    prior_commit = prior_receipt['commit']
    prior_prefix = Path('validation_sync/factorization_machine_workflow_20261005')
    manifest_bytes = subprocess.check_output(
        ['git', 'show', f'{prior_commit}:{prior_prefix.as_posix()}/manifest.json'], cwd=ROOT)
    prior_manifest = json.loads(manifest_bytes)
    expected = {}
    for source, item in prior_manifest['input_files'].items():
        source_path = Path(source)
        assert source_path.is_relative_to(ROOT), source
        relative = source_path.relative_to(ROOT)
        destination = relative if source_path.suffix == '.py' else prior_prefix / relative
        expected[destination.as_posix()] = item['sha256']
    actual = blob_hashes(prior_commit, expected)
    assert actual == expected, 'Historical committed bytes differ from the frozen manifest.'
    QA.mkdir(exist_ok=True)
    assert not (QA / 'verification.json').exists()
    sync.atomic(QA / 'verification.json', sync.encoded({
        'status': 'passed_all_manifest_input_git_blob_sha256', 'at_local': sync.now(),
        'commit': prior_commit, 'verified_input_count': len(expected),
        'git_blob_sha256': actual, 'historical_source_bytes_not_changed': True,
        'new_quality_scores': 0, 'test_labels_read': False}))

    observer = psutil.Process(sync.read(sync.OUT / 'owner.lock')['pid'])
    observer_parent = observer.parent()
    assert observer_parent is not None
    observer_parent, observer_child = owned_publisher(
        observer_parent.pid, ROOT / 'analysis/watch_validations_main_v2_20261005.py')
    assert observer_child.pid == observer.pid
    native_run = sync.read(ROOT / 'analysis/factorization_machine_native_github_run_20261005.json')
    native_parent, native_child = owned_publisher(native_run['pid'], Path(native_run['script']))
    suspended = []
    try:
        for process in (observer_child, observer_parent, native_child, native_parent):
            process.suspend()
            suspended.append(process)
        for parent, child in ((observer_parent, observer_child), (native_parent, native_child)):
            assert all(p.pid == child.pid or p.name().lower() == 'conhost.exe'
                       for p in parent.children(recursive=True)), 'Publisher busy; retry when idle.'
        assert not sync.git('status', '--porcelain')
        head = sync.git('rev-parse', 'HEAD')
        assert sync.git('rev-parse', 'refs/heads/main', cwd=ROOT) == head
        assert sync.git('branch', '--show-current', cwd=ROOT) == 'main'
        assert sync.git('branch', '--show-current') == ''
        assert sync.git('for-each-ref', '--format=%(refname)', 'refs/heads', cwd=ROOT) == 'refs/heads/main'
        assert sync.git('ls-remote', '--heads', 'origin').splitlines() == [f'{head}\trefs/heads/main']
        old_heads = sync.read(ROOT / 'analysis/github_main_consolidation_20261005/frozen_before_branch_consolidation.json')['remote_heads']
        for old_head in old_heads.values():
            sync.git('merge-base', '--is-ancestor', old_head, head)

        pending = names('ls-files', '--modified') | names('ls-files', '--others', '--exclude-standard')
        # Preserve historical generated sources that the broad artifact ignore rule can hide.
        tracked = names('ls-files')
        for folder in ('analysis', 'experiments', 'src', 'tests', 'config'):
            if (ROOT / folder).is_dir():
                pending.update(p.relative_to(ROOT).as_posix() for p in (ROOT / folder).rglob('*.py')
                               if '__pycache__' not in p.parts and p.relative_to(ROOT).as_posix() not in tracked)
        pending.add('analysis/factorization_machine_publication_blob_qa_20261005/verification.json')
        paths, captured = [], {}
        sync.atomic(sync.WORKTREE / PREFIX / '.gitattributes', b'* -text\n')
        paths.append((PREFIX / '.gitattributes').as_posix())
        for name in sorted(pending):
            source = ROOT / name
            assert source.is_file(), name
            assert source.suffix in ('.py', '.json', '.md', '.toml', '.yaml', '.yml'), name
            data = source.read_bytes()
            assert len(data) < 5 * 1024**2 and not sync.SECRET.search(data), name
            if source.suffix == '.json':
                json.loads(data.decode('utf-8-sig'))
            destination = PREFIX / name if name.startswith('analysis/factorization_machine_publication_blob_qa_') else Path(name)
            sync.atomic(sync.WORKTREE / destination, data)
            paths.append(destination.as_posix())
            captured[name] = {'published_path': destination.as_posix(),
                              'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data),
                              'state_snapshot': source.suffix == '.json' and (
                                  'state' in source.stem or 'resume' in source.stem or
                                  source.stem.startswith(('optimization_boundary', 'optimization_fit_cost', 'next_experiment')))}
        closeout = {'status': 'captured_all_remaining_versionable_workspace_files',
                    'at_local': sync.now(), 'previous_main': head, 'files': captured,
                    'previous_branch_heads_verified_ancestors': old_heads,
                    'local_and_remote_only_branch': 'main', 'publisher_worktree_detached': True,
                    'live_scientific_jobs_untouched': True,
                    'ongoing_state_is_snapshot_not_completion_certificate': True,
                    'raw_data_weights_predictions_remain_local_D_or_E': True,
                    'new_quality_scores': 0, 'test_labels_read': False}
        sync.atomic(sync.WORKTREE / PREFIX / 'manifest.json', sync.encoded(closeout))
        sync.atomic(sync.WORKTREE / PREFIX / 'README.md', (
            '# main 主分支补齐\n\n全部历史分支提交保留在 main，本地和 GitHub 仅保留 main。'
            '本次补齐最新运行清单、旧版生成源文件及运行状态，并逐文件核验上一批已提交文件的 SHA256。'
            '运行状态表示提交时快照，后续完成的验证继续直接提交 main。'
            '原始数据、训练权重和预测仍保存在 D/E 盘。\n').encode('utf-8'))
        paths.extend(((PREFIX / 'manifest.json').as_posix(), (PREFIX / 'README.md').as_posix()))
        for name, item in captured.items():
            if not item['state_snapshot']:
                assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == item['sha256'], name
        for offset in range(0, len(paths), 50):
            sync.git('add', '-f', '--', *paths[offset:offset + 50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(paths)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
                 '补齐main的全部剩余运行清单、历史生成源与已提交字节审计', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        wanted = {item['published_path']: item['sha256'] for item in captured.values()}
        assert blob_hashes(commit, wanted) == wanted
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        assert sync.git('ls-remote', '--heads', 'origin').splitlines() == [f'{commit}\trefs/heads/main']
        assert sync.git('ls-remote', '--symref', 'origin', 'HEAD').splitlines() == [
            'ref: refs/heads/main\tHEAD', f'{commit}\tHEAD']
        watcher.advance_source_index(commit)
        assert sync.git('config', '--get-all', 'remote.origin.fetch', cwd=ROOT) == '+refs/heads/main:refs/remotes/origin/main'
        assert sync.git('config', '--get-all', 'remote.origin.push', cwd=ROOT) == 'refs/heads/main:refs/heads/main'
        assert not sync.git('status', '--porcelain')
        result = {'status': 'pushed_verified_main_only', 'at_local': sync.now(),
                  'commit': commit, 'changed_files': len(staged), 'captured_files': len(captured),
                  'previous_publication_git_blobs_verified': len(expected),
                  'local_branches': ['main'], 'remote_branches': ['main'],
                  'remote_default_branch': 'main', 'old_branch_history_preserved': True,
                  'scientific_jobs_untouched': True,
                  'url': f'https://github.com/Zagadka-3906/stock-return-prediction/commit/{commit}'}
        sync.atomic(OUT / 'receipt.json', sync.encoded(result))
        print(json.dumps(result, ensure_ascii=False), flush=True)
    finally:
        for process in reversed(suspended):
            if process.is_running():
                process.resume()


if __name__ == '__main__':
    main()
