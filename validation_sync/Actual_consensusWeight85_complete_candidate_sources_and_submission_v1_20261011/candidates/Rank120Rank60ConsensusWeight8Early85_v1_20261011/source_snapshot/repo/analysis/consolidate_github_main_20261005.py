"""Preserve all published history, switch to main, then remove the merged branch."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess
import sys
import psutil

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
import sync_validated_rounds_main_20261005 as sync

OUT = ROOT / 'analysis/github_main_consolidation_20261005'


def file_sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def create(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def tree(commit):
    raw = subprocess.check_output(['git', 'ls-tree', '-r', '-z', commit], cwd=sync.WORKTREE)
    return {part.split(b'\t', 1)[1].decode('utf-8'): part.split(b'\t', 1)[0].decode('ascii')
            for part in raw.split(b'\0') if part}


def main():
    OUT.mkdir(exist_ok=True)
    assert not sync.git('status', '--porcelain', '--untracked-files=no')
    assert sync.git('branch', '--show-current') == 'codex/validated-rounds'
    assert sync.git('branch', '--show-current', cwd=ROOT) == 'main'
    assert sync.git('status', '--porcelain', '--untracked-files=no', cwd=ROOT) in ('M README.md', ' M README.md')
    refs = dict(line.split()[::-1] for line in sync.git('ls-remote', '--heads', 'origin').splitlines())
    assert set(refs) == {'refs/heads/main', 'refs/heads/codex/validated-rounds'}
    old_main, old_validated = refs['refs/heads/main'], refs['refs/heads/codex/validated-rounds']
    assert sync.git('rev-parse', 'HEAD') == old_validated
    assert sync.git('rev-parse', 'refs/heads/main', cwd=ROOT) == old_main
    sync.git('merge-base', '--is-ancestor', old_main, old_validated)
    original_tree = tree(old_validated)
    old_run_path = ROOT / 'analysis/github_validation_sync_20261005/backfill_watch_run_v2.json'
    old_run = sync.read(old_run_path)
    script = Path(old_run['script'])
    assert file_sha(script) == old_run['source_sha256']
    parent = psutil.Process(old_run['pid'])
    command = parent.cmdline()
    assert str(script) in command
    children = parent.children(recursive=True)
    workers = [p for p in children if p.cmdline()[1:] == command[1:]]
    assert len(workers) == 1 and all(p in workers or p.name().lower() == 'conhost.exe' for p in children)
    state = sync.read(ROOT / 'analysis/github_validation_sync_20261005/state.json')
    assert state['status'] == 'monitoring_completed_validations' and state['pid'] == workers[0].pid
    assert state['latest_synced']['round'] == 61
    assert not (ROOT / 'results/optimization_20261003_r62.json').exists()
    readme = ROOT / 'README.md'
    readme_bytes, readme_sha = readme.read_bytes(), file_sha(readme)
    (OUT / 'retained_source_README_before_merge.md').write_bytes(readme_bytes)
    create(OUT / 'frozen_before_branch_consolidation.json', {
        'status': 'frozen_before_verified_owned_publisher_handoff', 'at_local': sync.now(),
        'authorization': '调整GitHub分支，把所有东西都合并提交到主分支main，不要其他分支',
        'remote_heads': refs, 'old_publisher': old_run, 'old_publisher_state': state,
        'old_owned_processes': [{'pid': p.pid, 'create_time': p.create_time(), 'command': p.cmdline()} for p in [workers[0], parent]],
        'published_tree_files': len(original_tree), 'retained_user_README_sha256': readme_sha,
        'scientific_jobs_continue': True, 'new_quality_scores': 0, 'test_labels_read': False})
    owned = [workers[0], parent]
    for process in owned:
        process.terminate()
    _, alive = psutil.wait_procs(owned, timeout=10)
    assert not alive
    assert not sync.git('status', '--porcelain', '--untracked-files=no')
    sync.git('checkout', '--detach', old_validated)

    paths = []
    inputs = {}
    sources = set(ROOT.glob('*.py'))
    for folder in ('analysis', 'experiments', 'src'):
        sources.update((ROOT / folder).glob('*.py'))
    sources.update((ROOT / 'config').glob('*.json'))
    sources.update(ROOT.glob('requirements*.txt'))
    sources.add(ROOT / '后续选模标准.md')
    sources.add(readme)
    for source in sorted(sources):
        relative = source.relative_to(ROOT)
        data = source.read_bytes()
        assert len(data) < 5 * 1024**2 and not sync.SECRET.search(data)
        sync.atomic(sync.WORKTREE / relative, data)
        inputs[str(source)] = sync.sha(data)
        paths.append(relative.as_posix())

    prefix = Path('validation_sync/main_consolidation_20261005')
    sync.atomic(sync.WORKTREE / prefix / '.gitattributes', b'* -text\n')
    paths.append((prefix / '.gitattributes').as_posix())
    diagnostic = ROOT / 'analysis/nystrom_round61_quality_diagnostic_20261005/verification.json'
    d = sync.read(diagnostic)
    assert d['status'] == 'passed_frozen_score_loss_diagnostic'
    for source, digest in d['input_sha256'].items():
        assert file_sha(source) == digest
    baseline = ROOT / 'analysis/optimization_20261003_r60/selection.json'
    protocol61 = sync.read(ROOT / 'analysis/optimization_20261003_r61/protocol.json')
    assert protocol61['input_sha256'][str(baseline.resolve())] == file_sha(baseline)
    assert sync.read(baseline)['winner']['metrics'] == d['baseline_metrics']
    evidence = sync.complete_round_evidence(61)
    assert evidence is not None
    folders = ('nystrom_round61_quality_diagnostic_20261005', 'nystrom_round62_qualified_handoff_20261005')
    supplement = {p for folder in folders for p in (ROOT / 'analysis' / folder).glob('*') if p.suffix in ('.json', '.md')}
    supplement.update([OUT / 'frozen_before_branch_consolidation.json',
                       ROOT / 'analysis/nystrom_tuning_storage_20261005.json',
                       ROOT / 'analysis/nystrom_tuning_bank_run_20261005.json'])
    for source in sorted(supplement):
        data = source.read_bytes()
        assert len(data) < 5 * 1024**2 and not sync.SECRET.search(data)
        destination = prefix / source.relative_to(ROOT)
        sync.atomic(sync.WORKTREE / destination, data)
        inputs[str(source)] = sync.sha(data)
        paths.append(destination.as_posix())
    audit = {'status': 'all_published_history_ancestry_preserved_main_handoff_prepared',
        'at_local': sync.now(), 'previous_main': old_main, 'previous_validation_head': old_validated,
        'published_tree_files_retained': len(original_tree), 'complete_round61_evidence': evidence,
        'round61_diagnostic_baseline_transitively_pinned_by_original_protocol': True,
        'expanded_nystrom_grid': {'configurations': 10, 'annual_fits_planned': 50, 'quality_pending': True},
        'all_future_publication_branch': 'main', 'source_sha256': inputs,
        'local_source_files_preserved_index_only_fast_forward': True,
        'new_quality_scores': 0, 'test_labels_read': False}
    sync.atomic(sync.WORKTREE / prefix / 'manifest.json', sync.encoded(audit))
    paths.append((prefix / 'manifest.json').as_posix())
    doc = sync.WORKTREE / 'validation_sync/README.md'
    document = doc.read_text(encoding='utf-8')
    document += ('\n\n## 主分支统一维护\n\n2026-10-05依用户要求，所有已上传代码、第1—61轮方案、'
                 '历史验证归档与完整榜统一并入`main`；后续每轮验证完成后也只推送`main`。'
                 '旧冻结协议中的原分支名称保留为历史记录。\n\n'
                 '后台入口为`analysis/watch_validations_main_20261005.py`。'
                 '数据、训练权重与大预测CSV仍由本地D盘管理，D盘不足时可用E盘，项目缓存不使用C盘。'
                 '最新方案见[latest.json](latest.json)，完整榜见[第61轮累计榜](round61/ranking_all.csv)。\n')
    sync.atomic(doc, document.encode('utf-8'))
    paths.append('validation_sync/README.md')
    for source, digest in inputs.items():
        assert file_sha(source) == digest, source
    assert file_sha(readme) == readme_sha
    for offset in range(0, len(paths), 60):
        sync.git('add', '--', *paths[offset:offset + 60])
    changed = set(sync.git('diff', '--cached', '--name-only').splitlines())
    assert changed and changed <= set(paths)
    sync.git('commit', '-m', '统一main：合并全部验证历史、保留本地说明并切换后续逐轮同步')
    commit = sync.git('rev-parse', 'HEAD')
    new_tree = tree(commit)
    assert set(original_tree) <= set(new_tree)
    assert all(new_tree[path] == value for path, value in original_tree.items() if path not in changed)
    sync.git('merge-base', '--is-ancestor', old_validated, commit)
    sync.git('push', 'origin', 'HEAD:refs/heads/main')
    assert sync.git('ls-remote', '--heads', 'origin', 'refs/heads/main').split()[0] == commit
    # The exact old branch is deleted only after its full commit ancestry is on main.
    assert sync.git('ls-remote', '--heads', 'origin', 'refs/heads/codex/validated-rounds').split()[0] == old_validated
    sync.git('push', 'origin', '--delete', 'codex/validated-rounds')
    sync.git('fetch', '--prune', 'origin')
    assert sync.git('ls-remote', '--heads', 'origin').splitlines() == [f'{commit}\trefs/heads/main']
    assert sync.git('branch', '--show-current') == ''
    sync.git('branch', '-D', 'codex/validated-rounds', cwd=ROOT)
    import watch_validations_main_20261005 as watcher
    watcher.advance_source_index(commit)
    assert sync.git('branch', '--format=%(refname:short)', cwd=ROOT) == 'main'
    assert file_sha(readme) == readme_sha
    assert not sync.git('status', '--porcelain', '--untracked-files=no')
    create(OUT / 'verification.json', {'status': 'passed_main_push_and_only_main_remains',
        'at_local': sync.now(), 'commit': commit, 'previous_main': old_main,
        'previous_validation_head': old_validated, 'original_published_files': len(original_tree),
        'committed_files': len(new_tree), 'changed_review_files': len(changed),
        'old_publisher_stopped': True, 'all_original_source_files_and_README_preserved': True,
        'main_url': 'https://github.com/Zagadka-3906/stock-return-prediction/tree/main',
        'local_index_advanced_without_checkout_of_cleaned_history': True})
    print(json.dumps({'status': 'main_consolidated', 'commit': commit,
        'remote_and_local_branches': ['main'], 'files': len(new_tree)}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
