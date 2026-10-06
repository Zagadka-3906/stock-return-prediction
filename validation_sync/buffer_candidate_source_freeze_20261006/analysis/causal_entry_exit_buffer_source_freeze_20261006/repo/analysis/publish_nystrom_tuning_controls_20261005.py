"""Publish real kernel preflight and main-observer controls while quality remains pending."""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
import watch_validations_main_v2_20261005 as watcher
sync = watcher.sync


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    assert not (ROOT / 'results/optimization_20261003_r62.json').exists()
    assert not sync.git('status', '--porcelain', '--untracked-files=no')
    head = sync.git('rev-parse', 'HEAD')
    assert sync.git('ls-remote', '--heads', 'origin').splitlines() == [f'{head}\trefs/heads/main']
    proof_path = ROOT / 'analysis/nystrom_tuning_preflight_20261005/verification.json'
    proof = sync.read(proof_path)
    assert proof['status'] == 'passed_independent_numerical_and_actual_maturity_controls'
    assert proof['configurations'] == len(proof['controls']) == 10
    assert proof['actual_annual_fits'] == proof['new_quality_scores'] == 0
    for source, expected in proof['source_sha256'].items():
        assert digest(source) == expected, source
    handoff = ROOT / 'analysis/main_sync_monotone_handoff_20261005/verification.json'
    assert sync.read(handoff)['status'] == 'passed_actual_history_receipts_and_owned_observer_handoff'
    originals = {p for folder in ('nystrom_tuning_preflight_20261005', 'main_sync_monotone_handoff_20261005')
                 for p in (ROOT / 'analysis' / folder).glob('*.json')}
    originals.update(ROOT / 'analysis' / name for name in (
        'nystrom_tuning_storage_20261005.json', 'nystrom_tuning_bank_run_20261005.json',
        'nystrom_tuning_future_run_20261005.json', 'github_validation_sync_main_20261005/run_v2.json'))
    sources = [ROOT / 'analysis' / name for name in (
        'train_nystrom_tuning_bank_20261005.py', 'verify_nystrom_tuning_bank_20261005.py',
        'prepare_nystrom_tuning_bank_20261005.py', 'run_nystrom_tuning_bank_20261005.py',
        'verify_nystrom_tuning_future_20261005.py', 'prepare_nystrom_tuning_future_20261005.py',
        'watch_validations_main_v2_20261005.py', 'handoff_main_sync_v2_20261005.py', Path(__file__).name)]
    prefix = Path('validation_sync/nystrom_tuning_controls_20261005')
    paths, bindings = [], {}
    sync.atomic(sync.WORKTREE / prefix / '.gitattributes', b'* -text\n')
    paths.append((prefix / '.gitattributes').as_posix())
    for source in sorted(originals):
        destination = prefix / source.relative_to(ROOT)
        data = source.read_bytes()
        assert len(data) < 5 * 1024**2 and not sync.SECRET.search(data)
        sync.atomic(sync.WORKTREE / destination, data)
        paths.append(destination.as_posix())
        bindings[str(source)] = sync.sha(data)
    for source in sources:
        destination = source.relative_to(ROOT)
        data = source.read_bytes()
        assert not sync.SECRET.search(data)
        sync.atomic(sync.WORKTREE / destination, data)
        paths.append(destination.as_posix())
        bindings[str(source)] = sync.sha(data)
    sync.atomic(sync.WORKTREE / prefix / 'manifest.json', sync.encoded({
        'status': 'passed_actual_numerical_maturity_and_main_receipt_controls', 'at_local': sync.now(),
        'native_configurations': 10, 'planned_annual_fits': 50, 'planned_fulltraining_fits': 10,
        'annual_training_in_progress': True, 'fulltraining_and_complete_output_quality_pending': True,
        'source_sha256': bindings, 'new_quality_scores': 0, 'test_labels_read': False}))
    paths.append((prefix / 'manifest.json').as_posix())
    text = ('# 扩展核参数与主分支持续同步核验\n\n'
        '固定比较256核规模、长度尺度0.5/2、正则强度0.001/1，对照原128核、长度尺度1、正则0.1；'
        '排序和单日收益两个目标，共10配置。独立库代数、模型重载、固定块边界前缀、'
        '标签置换不改变核基、实际成熟训练行边界扰动检查均通过。\n\n'
        '50次年度向前拟合已开始，10次成熟最终拟合及完整未来X推理核验已排队。'
        '本归档没有新增官方质量分；完整方案的融合和独立主模型比较、选择冻结、'
        '收益映射官方复核、因果检查、候选推理和完整榜更新仍需继续。\n\n'
        'main同步器V2已用实际历史提交验证：旧轮次收据和当前收据均不改变较新的main或本地索引。'
        '下一轮真实提交将进一步验证向前更新。原V1源和记录保留。\n\n'
        '所有输出和临时文件使用D盘；启动时D空闲不足20 GiB则选择授权E盘。'
        '20 GiB空间阈值和14 GiB可用内存保留均为调度政策，不代表机器物理极限。\n')
    sync.atomic(sync.WORKTREE / prefix / 'README.md', text.encode('utf-8'))
    paths.append((prefix / 'README.md').as_posix())
    for source, expected in bindings.items():
        assert digest(source) == expected, source
    assert not (ROOT / 'results/optimization_20261003_r62.json').exists()
    assert sync.git('rev-parse', 'HEAD') == head
    for offset in range(0, len(paths), 50):
        sync.git('add', '--', *paths[offset:offset + 50])
    staged = set(sync.git('diff', '--cached', '--name-only').splitlines())
    assert staged and staged <= set(paths)
    for source in originals:
        destination = (prefix / source.relative_to(ROOT)).as_posix()
        blob = sync.subprocess.check_output(['git', 'show', ':' + destination], cwd=sync.WORKTREE)
        assert sync.sha(blob) == bindings[str(source)]
    sync.git('commit', '-m', '核验十组扩展核参数并修正main逐轮同步的旧收据处理')
    commit = sync.git('rev-parse', 'HEAD')
    sync.git('push', 'origin', 'HEAD:refs/heads/main')
    assert sync.git('ls-remote', '--heads', 'origin').splitlines() == [f'{commit}\trefs/heads/main']
    watcher.advance_source_index(commit)
    assert not sync.git('status', '--porcelain', '--untracked-files=no')
    with (sync.OUT / 'nystrom_tuning_controls_receipt.json').open('x', encoding='utf-8') as stream:
        json.dump({'status': 'pushed_and_only_main_remote_verified', 'at_local': sync.now(),
            'commit': commit, 'files': len(paths), 'new_quality_scores': 0,
            'url': f'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/{prefix.as_posix()}'}, stream, ensure_ascii=False, indent=2)
    print(json.dumps({'status': 'pushed_expanded_kernel_and_main_observer_controls', 'commit': commit,
                      'files': len(paths)}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
