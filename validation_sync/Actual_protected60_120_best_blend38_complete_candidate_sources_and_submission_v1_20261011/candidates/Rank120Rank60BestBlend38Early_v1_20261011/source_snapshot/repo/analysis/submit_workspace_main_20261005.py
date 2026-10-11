"""Commit the research workspace and byte-verifiable large reports to main only."""
from pathlib import Path
import ast
import gzip
import hashlib
import json
import os
import subprocess
import sys
import time

import psutil

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
import watch_validations_main_v2_20261005 as watcher

sync = watcher.sync
PREFIX = Path('validation_sync/workspace_snapshot_20261005')
OUT = ROOT / 'analysis/workspace_main_submission_20261005'


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def create(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    OUT.mkdir(exist_ok=True)
    assert not (OUT / 'receipt.json').exists(), 'Already submitted; inspect the receipt.'
    assert sync.git('branch', '--show-current', cwd=ROOT) == 'main'
    assert sync.git('branch', '--show-current') == ''
    assert not sync.git('status', '--porcelain')
    head = sync.git('rev-parse', 'HEAD')
    assert sync.git('rev-parse', 'refs/heads/main', cwd=ROOT) == head
    assert sync.git('ls-remote', '--heads', 'origin').splitlines() == [f'{head}\trefs/heads/main']

    proof_path = ROOT / 'analysis/nystrom_tuning_cost_inventory_qa_20261005/verification.json'
    proof = sync.read(proof_path)
    assert proof['status'] == 'passed_actual_artifact_inventory_and_idempotent_refresh'
    for source, value in proof['source_sha256'].items():
        assert digest(source) == value, source
    handoff = sync.read(ROOT / 'analysis/actual_monitor_v4_handoff_20261005/verification.json')
    assert handoff['status'] == 'passed_owned_observer_handoff'
    for name in ('train_neural16384_full_bank_20261005.py', 'run_neural16384_full_bank_20261005.py'):
        ast.parse((ROOT / 'analysis' / name).read_text(encoding='utf-8'))

    raw = subprocess.check_output(['git', 'ls-files', '--others', '--exclude-standard', '-z'], cwd=ROOT)
    sources = {ROOT / item.decode('utf-8') for item in raw.split(b'\0') if item}
    delivery = {p for p in sources if p.relative_to(ROOT).parts[0] == 'delivery_day_connected_20261003'}
    sources -= delivery
    sources.add(ROOT / 'README.md')
    supplementary = {p for folder in ('nystrom_tuning_cost_inventory_qa_20261005', 'actual_monitor_v4_handoff_20261005')
                     for p in (ROOT / 'analysis' / folder).glob('*.json')}
    create(OUT / 'frozen_before_commit.json', {
        'status': 'frozen_before_main_workspace_submission', 'at_local': sync.now(),
        'authorization': '调整GitHub分支，把所有东西都合并提交到主分支main，不要其他分支',
        'previous_main': head, 'ordinary_files_selected': len(sources),
        'local_delivery_files_retained': [str(p.relative_to(ROOT)) for p in sorted(delivery)],
        'data_models_predictions_and_runtime_caches_remain_local': True,
        'passed_cost_inventory_counts': proof['central_counts'],
        'new16384_sources_syntax_only_not_launched': True,
        'scientific_jobs_continue': True})
    supplementary.add(OUT / 'frozen_before_commit.json')
    bindings, paths, compressed = {}, [], []
    sync.atomic(sync.WORKTREE / PREFIX / '.gitattributes', b'* -text\n')
    paths.append((PREFIX / '.gitattributes').as_posix())
    for source in sorted(sources | supplementary):
        relative = source.relative_to(ROOT)
        snapshot_evidence = source in supplementary
        destination = PREFIX / relative if snapshot_evidence else relative
        if source.stat().st_size > 5 * 1024**2:
            assert relative.parts[0] == 'results', f'Unexpected large upload: {relative}'
            destination = PREFIX / Path(relative.as_posix() + '.gz')
            target = sync.WORKTREE / destination
            target.parent.mkdir(parents=True, exist_ok=True)
            hasher = hashlib.sha256()
            count = 0
            with source.open('rb') as stream, target.open('wb') as output:
                with gzip.GzipFile(filename='', mode='wb', fileobj=output, mtime=0, compresslevel=6) as archive:
                    while chunk := stream.read(1024**2):
                        assert not sync.SECRET.search(chunk)
                        hasher.update(chunk)
                        count += len(chunk)
                        archive.write(chunk)
            with gzip.open(target, 'rb') as stream:
                assert hashlib.file_digest(stream, 'sha256').hexdigest() == hasher.hexdigest()
            assert target.stat().st_size < 90 * 1024**2
            bindings[relative.as_posix()] = {'snapshot_sha256': hasher.hexdigest(), 'bytes': count,
                'published_path': destination.as_posix(), 'encoding': 'gzip_lossless',
                'compressed_bytes': target.stat().st_size, 'archive_sha256': digest(target)}
            compressed.append(relative.as_posix())
        else:
            data = source.read_bytes()
            assert not sync.SECRET.search(data), relative
            if source.suffix == '.json':
                json.loads(data.decode('utf-8-sig'))
            sync.atomic(sync.WORKTREE / destination, data)
            bindings[relative.as_posix()] = {'snapshot_sha256': sync.sha(data), 'bytes': len(data),
                'published_path': destination.as_posix(), 'encoding': 'ordinary_git_file'}
        paths.append(destination.as_posix())
    ignore_path = ROOT / '.gitignore'
    ignore = ignore_path.read_bytes()
    additions = ('\n# Large research reports are losslessly archived under validation_sync.\n' +
                 '\n'.join('/' + name for name in compressed) +
                 '\n# Local formal delivery data and predictions.\n/delivery_day_connected_20261003/\n').encode('utf-8')
    updated_ignore = ignore + additions
    sync.atomic(sync.WORKTREE / '.gitignore', updated_ignore)
    paths.append('.gitignore')
    document = ('# 主分支工作区汇总\n\n'
        '全部已上传验证历史与当前源码统一保存在main，后续完整验证也只推送main。'
        '这里补充此前未提交的研究报告、运行记录及通过的实际模型计数复核。\n\n'
        '大于5 MiB的报告以gzip无损归档，manifest.json记录原始路径、字节数、SHA256及压缩文件位置；'
        '每份归档已经实际解压并核对SHA256。其余文件在原目录提交。运行记录是提交时的快照，'
        '当前进行中的验证与拟合继续运行，快照不代表它们已经完成。\n\n'
        '16384宽度完整训练的两个新增源文件仅通过语法解析，尚未启动，不能算作已完成模型或评分。'
        '原始比赛数据、训练权重、预测CSV和运行环境继续存储于本地D盘，必要时使用E盘。\n')
    sync.atomic(sync.WORKTREE / PREFIX / 'README.md', document.encode('utf-8'))
    paths.append((PREFIX / 'README.md').as_posix())
    manifest = {'status': 'captured_workspace_and_verified_lossless_report_archives', 'at_local': sync.now(),
        'previous_main': head, 'files': bindings, 'passed_cost_inventory_counts': proof['central_counts'],
        'cost_inventory_and_monitor_handoff_passed': True, 'large_reports_verified_by_real_decompression': True,
        'new16384_full_training_pending': True, 'new_quality_scores_created_by_this_submission': 0,
        'ordinary_git_text_line_endings_follow_existing_gitattributes': True,
        'scientific_jobs_untouched': True, 'only_publication_branch': 'main'}
    sync.atomic(sync.WORKTREE / PREFIX / 'manifest.json', sync.encoded(manifest))
    paths.append((PREFIX / 'manifest.json').as_posix())
    print(json.dumps({'status': 'snapshot_ready', 'files': len(paths), 'lossless_archives': len(compressed)}, ensure_ascii=False), flush=True)

    # Suspend only the positively identified idle Git observer while committing.
    lock = sync.read(sync.OUT / 'owner.lock')
    observer = psutil.Process(lock['pid'])
    assert str(ROOT / 'analysis/watch_validations_main_v2_20261005.py') in observer.cmdline()
    parent = observer.parent()
    assert parent is not None and parent.cmdline()[1:] == observer.cmdline()[1:]
    owned = [observer, parent]
    suspended = []
    try:
        for process in owned:
            process.suspend()
            suspended.append(process)
        children = parent.children(recursive=True)
        assert all(p.pid == observer.pid or p.name().lower() == 'conhost.exe' for p in children), 'Publisher busy; retry after it finishes.'
        assert sync.git('rev-parse', 'HEAD') == head
        assert sync.git('rev-parse', 'refs/heads/main', cwd=ROOT) == head
        assert sync.git('ls-remote', '--heads', 'origin').splitlines() == [f'{head}\trefs/heads/main']
        for offset in range(0, len(paths), 50):
            sync.git('add', '--', *paths[offset:offset + 50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(paths)
        sync.git('commit', '-m', '统一main提交剩余源码、全部研究报告与无损完整榜归档')
        commit = sync.git('rev-parse', 'HEAD')
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=240)
        assert sync.git('ls-remote', '--heads', 'origin').splitlines() == [f'{commit}\trefs/heads/main']
        # Apply only the authorized ignore edits locally; retain all scientific inputs.
        assert ignore_path.read_bytes() == ignore
        sync.atomic(ignore_path, updated_ignore)
        watcher.advance_source_index(commit)
        assert sync.git('for-each-ref', '--format=%(refname)', 'refs/heads', cwd=ROOT) == 'refs/heads/main'
        receipt = {'status': 'pushed_verified_only_main', 'at_local': sync.now(), 'commit': commit,
            'staged_changed_files': len(staged), 'selected_files': len(paths), 'lossless_report_archives': len(compressed),
            'source_local_branch': 'main', 'remote_branches': ['main'], 'prior_history_preserved': True,
            'scientific_jobs_untouched': True, 'future_completed_validation_publication': 'main',
            'url': f'https://github.com/Zagadka-3906/stock-return-prediction/commit/{commit}'}
        create(OUT / 'receipt.json', receipt)
        print(json.dumps(receipt, ensure_ascii=False), flush=True)
    finally:
        for process in reversed(suspended):
            if process.is_running():
                process.resume()


if __name__ == '__main__':
    main()
