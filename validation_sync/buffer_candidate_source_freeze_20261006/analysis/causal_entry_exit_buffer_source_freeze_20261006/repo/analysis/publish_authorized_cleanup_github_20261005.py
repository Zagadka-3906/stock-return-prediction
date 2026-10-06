"""Publish storage withdrawal and completed user-authorized cache cleanup."""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
import sync_validated_rounds_github_20261005 as sync


def main():
    assert not (ROOT / 'results/optimization_20261003_r61.json').exists()
    assert not sync.git('status', '--porcelain', '--untracked-files=no')
    assert not sync.git('diff', '--cached', '--name-only')
    cleanup = ROOT / 'analysis/authorized_history_cache_cleanup_20261005'
    verification = sync.read(cleanup / 'verification.json')
    assert verification['status'] == 'passed_authorized_history_andunused_cache_cleanup'
    assert verification['no_new_missing_protected_dependencies']
    assert verification['C_project_scratch_absent']
    withdrawal = ROOT / 'analysis/official_scoring_disk_placement_preflight_20261005/placement_withdrawal_20261005.json'
    assert sync.read(withdrawal)['status'] == 'withdrawn_and_C_scratch_deleted'
    files = [(cleanup / name, Path('validation_sync/authorized_cleanup_20261005') / name)
             for name in ('plan.json', 'deletions.jsonl', 'verification.json')]
    files += [(withdrawal, Path('validation_sync/compute_storage_controls_20261005') / withdrawal.name)]
    files += [(ROOT / 'analysis' / name, Path('analysis') / name)
              for name in ('cleanup_uploaded_history_unused_caches_20261005.py', Path(__file__).name)]
    paths, bindings = [], {}
    for original, destination in files:
        data = original.read_bytes()
        sync.atomic(sync.WORKTREE / destination, data)
        paths.append(destination.as_posix())
        bindings[str(original)] = sync.sha(data)
    storage_readme = (
        '# 评分临时文件存放核验与撤回\n\n'
        '早前完整5635800行CSV跨盘写入对照通过，字节和官方八项指标一致。'
        '2026年10月5日04:54，按用户指示撤回C盘存放安排，删除14个别名及C盘专用项目临时目录。'
        '早前控制记录保留为历史证据，后续评分使用D盘，空间不足时可用E盘。\n\n'
        '已完成历史副本与弃用缓存清理，当前方案、原始数据和继续验证所需模型保留。'
        '详情见 placement_withdrawal_20261005.json 与 ../authorized_cleanup_20261005/verification.json。\n')
    cleanup_readme = (
        '# 用户授权的历史副本与弃用缓存清理\n\n'
        f"删除{verification['deleted_files']}个文件，实际释放D盘"
        f"{verification['D_free_bytes_change'] / 2**30:.2f} GiB；清理完成时剩余"
        f"{verification['D_free_bytes_after'] / 2**30:.2f} GiB。\n\n"
        'GitHub历史归档保留；本地同步工作树的旧归档文件设为skip-worktree后删除，'
        '后续每轮验证仍继续自动提交。当前最佳方案、正式交付、原始数据及4273个受保护依赖保留。'
        '原模型库中被冻结验证引用的文件继续保留；重复模型副本记录了可恢复的相同原模型路径。\n\n'
        'plan.json为删除前清单，deletions.jsonl为逐文件删除日志，verification.json为结果。'
        '本次清理没有训练新模型、产生新候选分数或读取测试标签。\n')
    for destination, content in [
        (Path('validation_sync/compute_storage_controls_20261005/README.md'), storage_readme),
        (Path('validation_sync/authorized_cleanup_20261005/README.md'), cleanup_readme)]:
        sync.atomic(sync.WORKTREE / destination, content.encode('utf-8'))
        paths.append(destination.as_posix())
    for name, digest in bindings.items():
        assert sync.sha(Path(name).read_bytes()) == digest
    sync.git('add', '--', *paths)
    assert set(sync.git('diff', '--cached', '--name-only').splitlines()) == set(paths)
    sync.git('commit', '-m', '按用户要求撤回C盘存放并清理历史副本和弃用缓存')
    commit = sync.git('rev-parse', 'HEAD')
    sync.git('push', 'origin', f'HEAD:refs/heads/{sync.BRANCH}')
    assert sync.git('ls-remote', '--heads', 'origin', f'refs/heads/{sync.BRANCH}').split()[0] == commit
    assert not sync.git('status', '--porcelain', '--untracked-files=no')
    receipt = {'status': 'pushed_and_remote_head_verified', 'at_local': sync.now(),
               'commit': commit, 'source_sha256': bindings,
               'url': f'https://github.com/Zagadka-3906/stock-return-prediction/tree/{sync.BRANCH}/validation_sync/authorized_cleanup_20261005',
               'remote_history_retained': True, 'C_storage_withdrawal_published': True}
    with (sync.OUT / 'authorized_cleanup_receipt.json').open('x', encoding='utf-8') as stream:
        json.dump(receipt, stream, ensure_ascii=False, indent=2)
    print(json.dumps({key: receipt[key] for key in ('status', 'commit', 'url')}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
