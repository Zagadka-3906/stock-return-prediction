"""Publish verified corrected generators and the two evidence-gated quality waiters."""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
import watch_validations_main_v2_20261005 as watcher
sync = watcher.sync


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    assert not (ROOT / 'results/optimization_20261003_r63.json').exists()
    assert not sync.git('status', '--porcelain', '--untracked-files=no')
    head = sync.git('rev-parse', 'HEAD')
    assert sync.git('ls-remote', '--heads', 'origin').splitlines() == [f'{head}\trefs/heads/main']
    proof = sync.read(ROOT / 'analysis/nystrom_tuning_search_generator_preflight_v2_20261005/verification.json')
    assert proof['status'] == 'passed' and proof['new_quality_scores'] == 0
    for source, digest in proof['source_sha256'].items():
        assert sha(source) == digest
    originals = {p for folder in ('nystrom_tuning_search_generator_preflight_20261005', 'nystrom_tuning_search_generator_preflight_v2_20261005')
                 for p in (ROOT / 'analysis' / folder).glob('*.json')}
    originals.update(ROOT / 'analysis' / name for name in (
        'nystrom_tuning_complete_search_plan_20261005.json', 'nystrom_tuning_quality_run_20261005.json',
        'nystrom_tuning_quality_queue_adoption_20261005.json'))
    sources = {p for p in (ROOT / 'analysis').glob('*nystrom_tuning*.py')}
    sources.update(ROOT / 'analysis' / f'{prefix}{number}{suffix}.py'
        for number in (65, 66) for prefix, suffix in (
            ('optimize_training_round', ''), ('optimize_training_round', '_v2'),
            ('finalize_training_round', ''), ('run_training_round', '_pipeline'), ('run_training_round', '_v2_pipeline')))
    prefix = Path('validation_sync/nystrom_tuning_quality_queue_20261005')
    paths, bindings = [], {}
    sync.atomic(sync.WORKTREE / prefix / '.gitattributes', b'* -text\n')
    paths.append((prefix / '.gitattributes').as_posix())
    for source in sorted(originals | sources):
        relative = source.relative_to(ROOT)
        destination = relative if source.suffix == '.py' else prefix / relative
        data = source.read_bytes()
        assert len(data) < 5 * 1024**2 and not sync.SECRET.search(data)
        sync.atomic(sync.WORKTREE / destination, data)
        paths.append(destination.as_posix())
        bindings[str(source)] = sync.sha(data)
    sync.atomic(sync.WORKTREE / prefix / 'manifest.json', sync.encoded({
        'status': 'passed_actual_reference_schema_and_synthetic_ordering_generator_controls',
        'at_local': sync.now(), 'controls': proof['controls'], 'source_sha256': bindings,
        'original_failed_generator_and_sources_retained': True,
        'rounds65_66_wait_for50_actual_annual10_final_fits_and_qualified_predecessors': True,
        'official_quality_records_expected': 390, 'official_quality_of_new_models_pending': True,
        'new_quality_scores': 0, 'test_labels_read': False}))
    paths.append((prefix / 'manifest.json').as_posix())
    document = ('# 第65、66轮扩展核完整方案流程\n\n'
        '第65轮预定172条用途融合记录，第66轮预定218条独立完整主模型记录。'
        '原V1生成器发现波次文件名未随编号改变，在任何官方质量评分前失败；原源、冻结与失败记录完整保留。'
        'V2实际生成全部三条控制分支：用途融合172条、独立方案未胜出218条、独立方案胜出218条；'
        '排序控制值为合成值，未冒充官方分数。\n\n'
        '实际图结构来自已冻结第61轮，只用于检查源与生成器。真实评分必须等待第64或65轮完整通过后，'
        '重新读取实际赢家，保留有效的同日意见门控，冻结真实参数和全部模型来源。'
        '50次年度拟合与10个成熟最终模型的完整未来X、重载和冷前缀核验另行完成，随后才允许评分。\n\n'
        '每轮在评分前先复现上一轮5635800行完整验证向量和官方八指标、1599600行未来CSV，'
        '再检查全部新增模型的用途或独立方案因果前缀与修改后的完整未来输出。'
        '选择后继续收益映射官方复核、候选推理、因果检查、执行来源核验和完整榜更新，再自动推送main。\n\n'
        '实际评分代码每个私有上下文覆盖写一份CSV，不保留每条候选的大CSV；当前D盘空间足够。'
        'D盘不足时可使用授权E盘，临时目录不使用C盘。有限参数网格与内存调度保留不代表全局优化或物理资源极限。\n')
    sync.atomic(sync.WORKTREE / prefix / 'README.md', document.encode('utf-8'))
    paths.append((prefix / 'README.md').as_posix())
    for source, digest in bindings.items():
        assert sha(source) == digest
    assert not (ROOT / 'results/optimization_20261003_r63.json').exists()
    assert sync.git('rev-parse', 'HEAD') == head
    for offset in range(0, len(paths), 50):
        sync.git('add', '--', *paths[offset:offset + 50])
    staged = set(sync.git('diff', '--cached', '--name-only').splitlines())
    assert staged and staged <= set(paths)
    sync.git('commit', '-m', '冻结扩展核完整方案390项验证流程并保留生成器修复证据')
    commit = sync.git('rev-parse', 'HEAD')
    sync.git('push', 'origin', 'HEAD:refs/heads/main')
    assert sync.git('ls-remote', '--heads', 'origin').splitlines() == [f'{commit}\trefs/heads/main']
    watcher.advance_source_index(commit)
    receipt = {'status': 'pushed_and_only_main_verified', 'at_local': sync.now(),
        'commit': commit, 'files': len(paths), 'new_quality_scores': 0,
        'url': f'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/{prefix.as_posix()}'}
    with (sync.OUT / 'nystrom_tuning_quality_queue_receipt.json').open('x', encoding='utf-8') as stream:
        json.dump(receipt, stream, ensure_ascii=False, indent=2)
    print(json.dumps(receipt, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
