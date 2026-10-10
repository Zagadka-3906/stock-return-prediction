"""Publish the remaining source copies and state snapshot, verifying main alone."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

import psutil

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
import watch_validations_main_v2_20261005 as watcher
from publish_main_closeout_v2_20261005 import blob_hashes, names

sync = watcher.sync
PREFIX = Path('validation_sync/main_branch_final_verification_20261005')
OUT = ROOT / 'analysis/main_branch_final_verification_20261005'


def owned_pair(pid, script, script_args=None):
    parent = psutil.Process(pid)
    command = parent.cmdline()
    assert str(script) in command, pid
    if script_args:
        assert command[-len(script_args):] == script_args
    children = [p for p in parent.children(recursive=True)
                if p.name().lower() == 'python.exe' and p.cmdline()[1:] == command[1:]]
    assert len(children) == 1, pid
    return parent, children[0]


def verify_main(commit):
    assert sync.git('branch', '--show-current', cwd=ROOT) == 'main'
    assert sync.git('for-each-ref', '--format=%(refname)', 'refs/heads', cwd=ROOT) == 'refs/heads/main'
    assert sync.git('ls-remote', '--heads', 'origin').splitlines() == [f'{commit}\trefs/heads/main']
    assert sync.git('ls-remote', '--symref', 'origin', 'HEAD').splitlines() == [
        'ref: refs/heads/main\tHEAD', f'{commit}\tHEAD']
    assert sync.git('config', '--get-all', 'remote.origin.fetch', cwd=ROOT) == '+refs/heads/main:refs/remotes/origin/main'
    assert sync.git('config', '--get-all', 'remote.origin.push', cwd=ROOT) == 'refs/heads/main:refs/heads/main'
    heads = sync.read(ROOT / 'analysis/github_main_consolidation_20261005/frozen_before_branch_consolidation.json')['remote_heads']
    for head in heads.values():
        sync.git('merge-base', '--is-ancestor', head, commit)
    return heads


def main():
    assert not (OUT / 'receipt.json').exists(), 'This publication already completed.'
    publisher = psutil.Process(sync.read(sync.OUT / 'owner.lock')['pid'])
    publisher_pair = owned_pair(publisher.parent().pid,
                                ROOT / 'analysis/watch_validations_main_v3_20261005.py')
    assert publisher_pair[1].pid == publisher.pid
    monitor = sync.read(ROOT / 'analysis/actual_optimization_monitor_launch_v13_20261005.json')
    monitor_pair = owned_pair(monitor['pid'], Path(monitor['script']), monitor['script_args'])
    suspended = []
    try:
        for parent, child in (publisher_pair, monitor_pair):
            child.suspend()
            suspended.append(child)
            parent.suspend()
            suspended.append(parent)
            assert all(p.pid == child.pid or p.name().lower() == 'conhost.exe'
                       for p in parent.children(recursive=True)), 'Owned observer has an active child.'
        assert not sync.git('status', '--porcelain')
        previous = sync.git('rev-parse', 'HEAD')
        assert sync.git('rev-parse', 'HEAD', cwd=ROOT) == previous
        old_heads = verify_main(previous)
        tracked = names('ls-files')
        selected = names('ls-files', '--modified') | names('ls-files', '--others', '--exclude-standard')
        for folder in ('analysis', 'experiments', 'src', 'tests', 'config'):
            for path in (ROOT / folder).rglob('*.py'):
                name = path.relative_to(ROOT).as_posix()
                if '__pycache__' not in path.parts and name not in tracked:
                    selected.add(name)
        targets, captured = {}, {}
        for name in sorted(selected):
            source = ROOT / name
            assert source.is_file() and source.suffix in ('.py', '.json', '.md', '.yaml', '.yml', '.toml'), name
            data = source.read_bytes()
            assert len(data) < 5 * 1024**2 and not sync.SECRET.search(data), name
            if source.suffix == '.json':
                json.loads(data.decode('utf-8-sig'))
            targets[name] = data
            captured[name] = {'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}
        prior_receipt = ROOT / 'analysis/memory_efficient_neural_workflows_github_20261005/receipt.json'
        targets[(PREFIX / 'previous_publication_receipt.json').as_posix()] = prior_receipt.read_bytes()
        manifest = {'status': 'verified_main_only_with_all_old_branch_heads_retained',
                    'at_local': sync.now(), 'authorization': '调整GitHub分支，把所有东西都合并提交到主分支main，不要其他分支',
                    'previous_main': previous, 'files': captured,
                    'old_branch_heads_verified_ancestors': old_heads,
                    'local_branches': ['main'], 'remote_branches': ['main'], 'default_branch': 'main',
                    'future_validation_push_target': 'refs/heads/main',
                    'publisher_worktree_has_detached_HEAD': sync.git('branch', '--show-current') == '',
                    'training_processes_not_suspended_or_stopped': True,
                    'runtime_json_files_are_submission_time_snapshots': True,
                    'raw_data_weights_and_predictions_preserved_locally_D_or_E': True,
                    'test_labels_read': False, 'new_quality_scores': 0}
        targets[(PREFIX / 'manifest.json').as_posix()] = sync.encoded(manifest)
        targets[(PREFIX / 'README.md').as_posix()] = (
            '# main 分支最终核验\n\n'
            '全部历史分支提交已包含在 main；本地、GitHub 和远端默认分支均为 main。'
            '后续已完成验证继续直接提交 main。同步工作目录使用分离 HEAD，不产生其他分支。\n\n'
            '本次补齐未被广泛产物忽略规则纳入的验证用源码副本，并提交最新运行状态快照。'
            '逐文件核验提交的原始字节 SHA256；训练继续运行，状态快照不表示待完成验证已完成。'
            '数据、权重和预测文件按既定存储规则留在 D/E 盘。\n').encode('utf-8')
        for name, data in targets.items():
            sync.atomic(sync.WORKTREE / name, data)
        paths = sorted(targets)
        for offset in range(0, len(paths), 50):
            sync.git('add', '-f', '--', *paths[offset:offset + 50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(paths)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
                 '补齐全部验证源码副本及运行快照，核验仅保留main', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        expected = {name: hashlib.sha256(data).hexdigest() for name, data in targets.items()}
        assert blob_hashes(commit, expected) == expected
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        verify_main(commit)
        watcher.advance_source_index(commit)
        assert sync.git('rev-parse', 'HEAD', cwd=ROOT) == commit
        assert not sync.git('status', '--porcelain', cwd=ROOT)
        assert not sync.git('status', '--porcelain')
        receipt = {'status': 'pushed_verified_main_only_all_remaining_source_and_state_files',
                   'at_local': sync.now(), 'commit': commit, 'changed_files': len(staged),
                   'raw_git_blob_sha256_verified': len(expected),
                   'local_branches': ['main'], 'remote_branches': ['main'], 'default_branch': 'main',
                   'old_branch_history_preserved': True, 'source_worktree_clean_at_snapshot': True,
                   'url': f'https://github.com/Zagadka-3906/stock-return-prediction/commit/{commit}'}
        sync.atomic(OUT / 'receipt.json', sync.encoded(receipt))
        print(json.dumps(receipt, ensure_ascii=False), flush=True)
    finally:
        for process in reversed(suspended):
            if process.is_running():
                process.resume()


if __name__ == '__main__':
    main()
