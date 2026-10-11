"""Publish every remaining source and fresh audit snapshot on main only."""
from pathlib import Path
import gzip
import hashlib
import json
import datetime
import os
import subprocess
import sys

import psutil

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
import watch_validations_main_v2_20261005 as watcher

sync = watcher.sync
PREFIX = Path('validation_sync/main_unified_followup_20261005')
OUT = ROOT / 'analysis/main_unified_followup_20261005'


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def git_names(*args):
    raw = subprocess.check_output(['git', *args, '-z'], cwd=ROOT)
    return {name.decode('utf-8') for name in raw.split(b'\0') if name}


def git_blob_digests(commit, names):
    names = sorted(names)
    request = ''.join(f'{commit}:{name}\n' for name in names).encode('utf-8')
    result = subprocess.run(['git', 'cat-file', '--batch'], cwd=sync.WORKTREE,
                            input=request, capture_output=True, check=True)
    offset, hashes = 0, {}
    for name in names:
        end = result.stdout.index(b'\n', offset)
        header = result.stdout[offset:end].split()
        assert len(header) == 3 and header[1] == b'blob', name
        size = int(header[2])
        start = end + 1
        hashes[name] = hashlib.sha256(result.stdout[start:start + size]).hexdigest()
        offset = start + size + 1
    assert offset == len(result.stdout)
    return hashes


def main():
    OUT.mkdir(exist_ok=True)
    assert not (OUT / 'receipt.json').exists(), 'Already published; inspect receipt.'
    assert sync.git('branch', '--show-current', cwd=ROOT) == 'main'
    assert sync.git('branch', '--show-current') == ''
    observer = psutil.Process(sync.read(sync.OUT / 'owner.lock')['pid'])
    script = str(ROOT / 'analysis/watch_validations_main_v2_20261005.py')
    assert script in observer.cmdline()
    parent = observer.parent()
    assert parent is not None and parent.cmdline()[1:] == observer.cmdline()[1:]
    suspended = []
    try:
        native_run = sync.read(ROOT / 'analysis/linear_leaf_native_github_run_20261005.json')
        native_parent = psutil.Process(native_run['pid'])
        assert native_run['script'] in native_parent.cmdline()
        native_workers = [p for p in native_parent.children(recursive=True)
                          if p.cmdline()[1:] == native_parent.cmdline()[1:]]
        assert len(native_workers) == 1
        for process in (observer, parent, native_workers[0], native_parent):
            process.suspend()
            suspended.append(process)
        assert all(p.pid == observer.pid or p.name().lower() == 'conhost.exe'
                   for p in parent.children(recursive=True)), 'Publisher busy; retry when idle.'
        assert all(p.pid == native_workers[0].pid or p.name().lower() == 'conhost.exe'
                   for p in native_parent.children(recursive=True)), 'Native publisher busy; retry.'
        assert not sync.git('status', '--porcelain')
        head = sync.git('rev-parse', 'HEAD')
        assert sync.git('rev-parse', 'refs/heads/main', cwd=ROOT) == head
        assert sync.git('ls-remote', '--heads', 'origin').splitlines() == [f'{head}\trefs/heads/main']
        assert sync.git('for-each-ref', '--format=%(refname)', 'refs/heads', cwd=ROOT) == 'refs/heads/main'
        original = sync.read(ROOT / 'analysis/github_main_consolidation_20261005/frozen_before_branch_consolidation.json')
        for old_head in original['remote_heads'].values():
            sync.git('merge-base', '--is-ancestor', old_head, head)

        names = git_names('ls-files', '--modified') | git_names('ls-files', '--others', '--exclude-standard')
        tracked = git_names('ls-files')
        historical_sources = set()
        for folder in ('analysis', 'experiments', 'src', 'tests', 'config'):
            for source in (ROOT / folder).rglob('*.py'):
                if '__pycache__' not in source.parts:
                    relative = source.relative_to(ROOT).as_posix()
                    if relative not in tracked:
                        historical_sources.add(relative)
        names |= historical_sources
        since = datetime.datetime.fromisoformat(sync.read(ROOT / 'analysis/main_workspace_followup_20261005/receipt.json')['at_local']).timestamp()
        evidence = {p.relative_to(ROOT).as_posix() for p in (ROOT / 'analysis').rglob('*')
                    if p.is_file() and p.suffix in ('.json', '.jsonl', '.md', '.yaml', '.yml', '.toml')
                    and p.stat().st_mtime >= since}
        names |= evidence
        names |= {'results/all_model_rankings_20261003.json', 'results/all_model_rankings_20261003.html'}
        assert all((ROOT / name).is_file() for name in names)
        publication = sync.read(ROOT / 'results/optimization_20261003_r64.json')
        completed = sync.complete_round_evidence(64)
        assert completed is not None and publication['scored_records'] == 104
        assert publication['test_labels_read_this_round'] is False
        latest = sync.read(sync.WORKTREE / 'validation_sync/latest.json')
        assert latest['round'] >= 64

        bindings, paths, compressed = {}, [], []
        sync.atomic(sync.WORKTREE / PREFIX / '.gitattributes', b'* -text\n')
        paths.append((PREFIX / '.gitattributes').as_posix())
        for name in sorted(names):
            source = ROOT / name
            assert source.suffix not in ('.csv', '.parquet', '.pt', '.joblib', '.log'), name
            if source.stat().st_size > 5 * 1024**2:
                assert name.startswith(('results/', 'analysis/')), name
                destination = PREFIX / (name + '.gz')
                target = sync.WORKTREE / destination
                target.parent.mkdir(parents=True, exist_ok=True)
                hasher, count = hashlib.sha256(), 0
                with source.open('rb') as stream, target.open('wb') as output:
                    with gzip.GzipFile(filename='', mode='wb', fileobj=output,
                                       mtime=0, compresslevel=6) as archive:
                        while chunk := stream.read(1024**2):
                            assert not sync.SECRET.search(chunk), name
                            hasher.update(chunk)
                            count += len(chunk)
                            archive.write(chunk)
                with gzip.open(target, 'rb') as stream:
                    assert hashlib.file_digest(stream, 'sha256').hexdigest() == hasher.hexdigest()
                assert target.stat().st_size < 90 * 1024**2
                item = {'sha256': hasher.hexdigest(), 'bytes': count, 'encoding': 'gzip_lossless',
                        'published_sha256': digest(target), 'published_bytes': target.stat().st_size}
                compressed.append(name)
                print(json.dumps({'archived': name, 'bytes': count,
                                  'compressed_bytes': target.stat().st_size}), flush=True)
            else:
                data = source.read_bytes()
                assert not sync.SECRET.search(data), name
                if source.suffix == '.json':
                    json.loads(data.decode('utf-8-sig'))
                destination = PREFIX / Path(name) if name in evidence and name not in tracked and '/' in name.removeprefix('analysis/') else Path(name)
                sync.atomic(sync.WORKTREE / destination, data)
                item = {'sha256': sync.sha(data), 'bytes': len(data),
                        'encoding': 'original_bytes', 'published_sha256': sync.sha(data)}
            item['published_path'] = destination.as_posix()
            item['observational_snapshot'] = name in evidence or source.suffix == '.json' and (
                '/ongoing_' in name or '/resume_' in name or '/resumed_' in name or
                'monitor_state' in name or '/next_experiment_' in name or
                'optimization_boundary_evidence' in name or 'optimization_fit_cost_evidence' in name
                or name in evidence)
            bindings[name] = item
            paths.append(destination.as_posix())

        ignore_path = ROOT / '.gitignore'
        old_ignore = ignore_path.read_bytes()
        ignored = old_ignore.decode('utf-8-sig').splitlines()
        additions = [f'/{name}' for name in compressed if f'/{name}' not in ignored]
        updated_ignore = old_ignore
        if additions:
            updated_ignore += ('\n# Further complete rankings are stored as verified lossless archives.\n'
                               + '\n'.join(additions) + '\n').encode('utf-8')
            sync.atomic(sync.WORKTREE / '.gitignore', updated_ignore)
            paths.append('.gitignore')
        manifest = {
            'status': 'captured_remaining_sources_and_byte_verified_report_archives',
            'at_local': sync.now(), 'previous_main': head, 'authorization':
                '调整GitHub分支，把所有东西都合并提交到主分支main，不要其他分支',
            'previous_remote_branch_heads_verified_ancestors': original['remote_heads'],
            'source_sha256': bindings, 'previously_ignored_python_sources': len(historical_sources),
            'recent_audit_snapshots': len(evidence),
            'completed_round_at_snapshot': 64, 'completed_round64_records': 104,
            'completed_connected_ranking_records': 9432,
            'new_quality_scores_created_by_this_publication': 0,
            'ongoing_records_are_snapshots_not_completion_certificates': True,
            'original_data_models_predictions_retained_local_D_or_E': True,
            'only_local_and_remote_branch': 'main', 'publisher_worktree_detached': True,
            'live_scientific_jobs_not_suspended_or_restarted': True}
        sync.atomic(sync.WORKTREE / PREFIX / 'manifest.json', sync.encoded(manifest))
        paths.append((PREFIX / 'manifest.json').as_posix())
        document = (
            '# main 主分支补齐记录\n\n'
            '所有历史提交与验证记录都已归入 main；本地和 GitHub 仅保留这一分支，后续完整验证继续直接同步 main。\n\n'
            '本次补齐尚未在原目录提交的源码、冻结运行清单、最新状态与第64轮报告，并保存上次统一提交后新增的审计记录。'
            '进行中的第65—70轮记录仅表示提交时状态，不代表验证已经完成。\n\n'
            '完整排名的大文件以 gzip 无损保存。manifest.json 记录原始字节数、SHA256、'
            '归档位置及归档SHA256，每份文件均已实际解压核对。'
            '最新可直接查看的累计完整榜见 [第64轮完整榜](../round64/ranking_all.csv)，共9,432条已完成评分。\n\n'
            '原始数据、训练权重、预测CSV及环境缓存继续保存在本地D盘，必要时使用E盘。\n')
        sync.atomic(sync.WORKTREE / PREFIX / 'README.md', document.encode('utf-8'))
        paths.append((PREFIX / 'README.md').as_posix())
        for name, item in bindings.items():
            if not item['observational_snapshot']:
                assert digest(ROOT / name) == item['sha256'], name
        for offset in range(0, len(paths), 50):
            sync.git('add', '-f', '--', *paths[offset:offset + 50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(paths)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
                 '统一main并补齐全部剩余源码、运行审计与第64轮完整榜', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        actual = git_blob_digests(commit, {item['published_path'] for item in bindings.values()})
        assert all(actual[item['published_path']] == item['published_sha256']
                   for item in bindings.values()), 'Committed blob digest mismatch'
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=240)
        assert sync.git('ls-remote', '--heads', 'origin').splitlines() == [f'{commit}\trefs/heads/main']
        assert sync.git('ls-remote', '--symref', 'origin', 'HEAD').splitlines() == [
            'ref: refs/heads/main\tHEAD', f'{commit}\tHEAD']
        assert ignore_path.read_bytes() == old_ignore
        if additions:
            sync.atomic(ignore_path, updated_ignore)
        watcher.advance_source_index(commit)
        sync.git('config', '--local', '--replace-all', 'remote.origin.fetch',
                 '+refs/heads/main:refs/remotes/origin/main', cwd=ROOT)
        sync.git('config', '--local', '--replace-all', 'remote.origin.push',
                 'refs/heads/main:refs/heads/main', cwd=ROOT)
        assert sync.git('for-each-ref', '--format=%(refname)', 'refs/heads', cwd=ROOT) == 'refs/heads/main'
        assert not sync.git('status', '--porcelain')
        receipt = {'status': 'pushed_verified_only_main_and_all_selected_git_blob_hashes',
            'at_local': sync.now(), 'commit': commit, 'changed_files': len(staged),
            'selected_files': len(paths), 'previously_ignored_python_sources': len(historical_sources),
            'lossless_archives': len(compressed), 'recent_audit_snapshots': len(evidence), 'local_branches': ['main'], 'remote_branches': ['main'],
            'remote_default_branch': 'main', 'old_branch_history_preserved': True,
            'default_fetch_and_push_target': 'main', 'scientific_jobs_untouched': True,
            'commit_url': f'https://github.com/Zagadka-3906/stock-return-prediction/commit/{commit}'}
        sync.atomic(OUT / 'receipt.json', sync.encoded(receipt))
        print(json.dumps(receipt, ensure_ascii=False), flush=True)
    finally:
        for process in reversed(suspended):
            if process.is_running():
                process.resume()


if __name__ == '__main__':
    main()
