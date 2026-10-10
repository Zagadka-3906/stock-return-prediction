"""Publish the actual disk-placement control while quality publication remains gated."""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
import sync_validated_rounds_github_20261005 as sync


def main():
    # The automatic publisher has no eligible new round during this separate control commit.
    assert not (ROOT / 'results/optimization_20261003_r61.json').exists()
    assert not sync.git('status', '--porcelain', '--untracked-files=no')
    assert not sync.git('diff', '--cached', '--name-only')
    source = ROOT / 'analysis/official_scoring_disk_placement_preflight_20261005'
    assert sync.read(source / 'verification.json')['status'] == 'passed'
    assert sync.read(source / 'placement_verification.json')['status'] == 'passed_new_output_alias_creation_only'
    directory = Path('validation_sync/compute_storage_controls_20261005')
    files = [(source / name, directory / name) for name in [
        'capability.json', 'frozen_before_actual_control.json', 'verification.json',
        'placement_frozen_before_creation.json', 'placement_verification.json']]
    for name in ['verify_official_scoring_disk_placement_20261005.py',
                 'prepare_official_scoring_disk_placement_20261005.py', Path(__file__).name]:
        files.append((ROOT / 'analysis' / name, Path('analysis') / name))
    paths, bindings = [], {}
    for original, destination in files:
        data = original.read_bytes()
        sync.atomic(sync.WORKTREE / destination, data)
        bindings[str(original)] = sync.sha(data)
        paths.append(destination.as_posix())
    readme = ('# 评分临时文件存放核验\n\n'
              'D 盘剩余约3.5 GiB、C盘剩余约148 GiB时，对完整5635800行训练验证CSV进行了实际写入与官方评分对照。'
              '跨盘符号链接保留，17位精度CSV字节及官方八项指标全部一致，连接分仍为0.450969086231263。\n\n'
              '第61—63轮各四个新worker的submission.csv已设置独立C盘目标文件；'
              '原评分输入的硬链接、算法、既有文件和冻结方案保持原样。'
              '这是执行存放位置的核验，不产生新候选评分或新训练模型；未来各worker的实际执行仍待完成。\n')
    sync.atomic(sync.WORKTREE / directory / 'README.md', readme.encode('utf-8'))
    paths.append((directory / 'README.md').as_posix())
    for path, digest in bindings.items():
        assert sync.sha(Path(path).read_bytes()) == digest
    sync.git('add', '--', *paths)
    assert set(sync.git('diff', '--cached', '--name-only').splitlines()) <= set(paths)
    sync.git('commit', '-m', '核验评分临时文件跨盘存放：5635800行CSV与官方八指标完全一致')
    commit = sync.git('rev-parse', 'HEAD')
    sync.git('push', 'origin', f'HEAD:refs/heads/{sync.BRANCH}')
    assert sync.git('ls-remote', '--heads', 'origin', f'refs/heads/{sync.BRANCH}').split()[0] == commit
    receipt = {'status': 'pushed_and_remote_head_verified', 'at_local': sync.now(),
               'commit': commit, 'control': 'actual_full_training_validation_csv_disk_placement',
               'url': f'https://github.com/Zagadka-3906/stock-return-prediction/tree/{sync.BRANCH}/{directory.as_posix()}',
               'source_sha256': bindings, 'new_model_fits': 0, 'new_quality_scores': 0,
               'test_labels_read': False}
    with (sync.OUT / 'storage_control_receipt.json').open('x', encoding='utf-8') as stream:
        json.dump(receipt, stream, ensure_ascii=False, indent=2)
    print(json.dumps({key: receipt[key] for key in ['status', 'commit', 'url']}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
