"""Publish actual mixtures, preserve the failed precursor, and label quality pending."""
from pathlib import Path
import hashlib
import json
import sys

import psutil

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
import watch_validations_main_v2_20261005 as watcher

sync = watcher.sync
PREFIX = Path('validation_sync/linear_leaf_ensemble_controls_20261005')


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    receipt_path = sync.OUT / 'linear_leaf_ensemble_controls_receipt.json'
    assert not receipt_path.exists()
    out = ROOT / 'analysis/linear_leaf_ensemble_complementarity_v2_20261005'
    proof = sync.read(out / 'verification.json')
    assert proof['status'] == 'passed_actual_five_year_mixture_native_reload_and_prefix_controls'
    for source, value in proof['source_sha256'].items():
        assert sha(source) == value, source
    for row in proof['mixture_controls']:
        assert sha(out / f"{row['mixture']}_raw.npy") == row['full_oof_raw_sha256']
        assert sha(out / f"{row['mixture']}_actual2020.joblib") == row['serialized_actual2020_composite_sha256']
        assert row['full_oof_rows'] == 5635800 and not row['bit_identical_to_any_single_parent']
    assert len(proof['mixture_controls']) == 4 and proof['actual_new_annual_fits'] == proof['new_quality_scores'] == 0
    plan = ROOT / 'analysis/linear_leaf_ensemble_complete_search_plan_20261005.json'
    assert len(sync.read(plan)['model_configurations']) == 8
    owner = psutil.Process(sync.read(sync.OUT / 'owner.lock')['pid'])
    assert str(ROOT / 'analysis/watch_validations_main_v2_20261005.py') in owner.cmdline()
    parent = owner.parent()
    assert parent is not None and parent.cmdline()[1:] == owner.cmdline()[1:]
    native_run = sync.read(ROOT / 'analysis/linear_leaf_native_github_run_20261005.json')
    native_parent = psutil.Process(native_run['pid'])
    command = native_parent.cmdline()
    assert native_run['script'] in command
    workers = [p for p in native_parent.children(recursive=True) if p.cmdline()[1:] == command[1:]]
    assert len(workers) == 1
    suspended = []
    try:
        for process in (owner, parent, workers[0], native_parent):
            process.suspend()
            suspended.append(process)
        for root, worker in ((parent, owner), (native_parent, workers[0])):
            assert all(p.pid == worker.pid or p.name().lower() == 'conhost.exe' for p in root.children(recursive=True))
        assert not sync.git('status', '--porcelain')
        head = sync.git('rev-parse', 'HEAD')
        assert sync.git('ls-remote', '--heads', 'origin').splitlines() == [f'{head}\trefs/heads/main']
        sources = {Path(__file__), ROOT / 'analysis/verify_linear_leaf_ensemble_complementarity_20261005.py',
                   ROOT / 'analysis/verify_linear_leaf_ensemble_complementarity_v2_20261005.py', plan}
        evidence = {p for folder in ('linear_leaf_ensemble_complementarity_20261005',
            'linear_leaf_ensemble_complementarity_v2_20261005')
            for p in (ROOT / 'analysis' / folder).glob('*.json')}
        paths, bindings = [], {}
        sync.atomic(sync.WORKTREE / PREFIX / '.gitattributes', b'* -text\n')
        paths.append((PREFIX / '.gitattributes').as_posix())
        for source in sorted(sources | evidence):
            data = source.read_bytes()
            assert len(data) < 5 * 1024**2 and not sync.SECRET.search(data)
            relative = source.relative_to(ROOT)
            destination = relative if source in sources else PREFIX / relative
            sync.atomic(sync.WORKTREE / destination, data)
            paths.append(destination.as_posix())
            bindings[str(source)] = sha(source)
        manifest = {'status': 'passed_actual_rank_mixture_controls_with_original_failed_expression_preserved',
            'at_local': sync.now(), 'input_sha256': bindings,
            'actual_verified_rank_mixtures': proof['mixture_controls'],
            'actual_daily_rank_correlations_without_labels': proof['daily_rank_correlations_no_labels'],
            'raw_array_and_serialized_actual_model_hashes_verified': True,
            'original762TB_request_was_expression_shape_failure_not_physical_resource_boundary': True,
            'prespecified_rank_and_return_virtual_configs': 8,
            'expected_virtual_annual_outputs': 40, 'new_native_annual_fits': 0,
            'expected_complete_official_records': {'71': 148, '72': 178},
            'all8_composite_bank_and_quality_execution_not_yet_implemented_or_started': True,
            'rank_only_controls_do_not_certify_return_composites': True,
            'correlation_diagnostic_does_not_replace_official_score_selection': True,
            'only_branch': 'main', 'new_quality_scores': 0, 'test_labels_read': False}
        sync.atomic(sync.WORKTREE / PREFIX / 'manifest.json', sync.encoded(manifest))
        paths.append((PREFIX / 'manifest.json').as_posix())
        text = (
            '# 普通树叶与线性树叶的原始预测集成预检\n\n'
            '使用已实际训练的15个排名目标年度模型，比较三模型等权、两档线性正则等权、'
            '普通树与lambda1线性树等权、普通树与lambda10线性树等权。'
            '四种组合均覆盖全部5,635,800条五年OOF记录，且均不同于单个父模型。\n\n'
            '真实300轮父模型被序列化为复合模型，重新推理2020年4096条记录并逐位复现完整组合数组；'
            '1、80、257、4095条前缀检查全部通过。没有新增模型拟合，也没有新增官方评分。\n\n'
            '日排名相关性仅使用有效价格行并不加载收益标签：普通树与线性树均值约0.970/0.971，'
            '两档线性正则约0.988；与第64轮完整输出约0.840/0.842。相关性不会成为额外采用门槛。\n\n'
            '同样四种权重也预先登记用于收益率目标，共8种集成、40个年度组合输出、8个最终复合模型。'
            '第71/72轮完整方案分别计划148/178条官方评分；其完整代码与执行仍待完成。'
            '本预检只覆盖排名目标，不能宣称收益率组合或完整方案已验证。\n\n'
            '原始Polars表达式构造错误和失败源码保留；异常762TB分配请求不是物理内存边界证据。'
            '模型与原始组合数组留在本地，GitHub只上传源码、清单和检查结果。\n')
        sync.atomic(sync.WORKTREE / PREFIX / 'README.md', text.encode('utf-8'))
        paths.append((PREFIX / 'README.md').as_posix())
        for source, expected in bindings.items():
            assert sha(source) == expected, source
        for offset in range(0, len(paths), 50):
            sync.git('add', '--', *paths[offset:offset + 50])
        changed = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert changed and changed <= set(paths)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            '核验四种线性树集成全五年预测和真实模型重载，登记八种后续比较', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        assert sync.git('ls-remote', '--heads', 'origin').splitlines() == [f'{commit}\trefs/heads/main']
        watcher.advance_source_index(commit)
        result = {'status': 'pushed_verified_only_main', 'at_local': sync.now(), 'commit': commit,
            'files': len(paths), 'actual_rank_mixtures_verified': 4, 'new_quality_scores': 0,
            'url': f'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/{PREFIX.as_posix()}'}
        sync.atomic(receipt_path, sync.encoded(result))
        print(json.dumps(result, ensure_ascii=False), flush=True)
    finally:
        for process in reversed(suspended):
            if process.is_running():
                process.resume()


if __name__ == '__main__':
    main()
