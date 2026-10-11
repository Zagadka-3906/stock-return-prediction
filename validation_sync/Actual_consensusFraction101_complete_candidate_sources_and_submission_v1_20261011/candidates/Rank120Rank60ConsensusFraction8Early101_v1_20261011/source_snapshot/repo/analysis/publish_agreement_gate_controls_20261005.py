"""Publish actual primitive controls and the gated full-scheme experiment sources."""
from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
import sync_validated_rounds_github_20261005 as sync


def main():
    assert not (ROOT / 'results/optimization_20261003_r61.json').exists()
    assert not sync.git('status', '--porcelain', '--untracked-files=no')
    prefix = Path('validation_sync/agreement_gate_controls_20261005')
    proof = sync.read(ROOT / 'analysis/agreement_gate_preflight_v2_20261005/verification.json')
    assert proof['status'] == 'passed_actual_mature_oof_gate_controls'
    assert proof['actual_nonzero_gate_cases'] == 180 and proof['actual_zero_strength_weight_cases'] == 20
    source_control = sync.read(ROOT / 'analysis/agreement_gate_round64_source_preflight_20261005/verification.json')
    assert source_control['status'] == 'passed_actual_reference_graph_and_synthetic_generator_checks'
    folders = ('agreement_gate_preflight_20261005', 'agreement_gate_preflight_v2_20261005',
               'agreement_gate_round64_source_preflight_20261005', 'actual_monitor_v3_handoff_20261005')
    originals = {p for folder in folders for p in (ROOT / 'analysis' / folder).glob('*.json')}
    originals.update(ROOT / 'analysis' / name for name in (
        'agreement_gate_round64_run_20261005.json', 'actual_optimization_monitor_run_v3_20261005.json'))
    source_names = (
        'agreement_gated_weights_20261005.py', 'verify_agreement_gated_weights_20261005.py',
        'verify_agreement_gated_weights_v2_20261005.py', 'optimize_training_round64.py',
        'predict_agreement_scheme_20261005.py', 'finalize_training_round64.py',
        'check_agreement_scheme_20261005.py', 'run_training_round64_pipeline.py',
        'prepare_agreement_round64_20261005.py', 'refresh_optimization_boundary_evidence_v2_20261005.py',
        'monitor_actual_optimization_progress_v3_20261005.py', 'handoff_actual_monitor_v3_20261005.py', Path(__file__).name)
    paths, bindings = [], {}
    attrs = prefix / '.gitattributes'
    sync.atomic(sync.WORKTREE / attrs, b'* -text\n')
    paths.append(attrs.as_posix())
    for original in sorted(originals):
        data = original.read_bytes()
        assert len(data) < 5 * 1024**2 and not sync.SECRET.search(data)
        destination = prefix / original.relative_to(ROOT)
        sync.atomic(sync.WORKTREE / destination, data)
        paths.append(destination.as_posix())
        bindings[str(original)] = sync.sha(data)
    for name in source_names:
        original, destination = ROOT / 'analysis' / name, Path('analysis') / name
        data = original.read_bytes()
        assert not sync.SECRET.search(data)
        sync.atomic(sync.WORKTREE / destination, data)
        paths.append(destination.as_posix())
        bindings[str(original)] = sync.sha(data)
    manifest = {'status': 'passed_primitive_and_generator_controls_full_quality_pending', 'at_local': sync.now(),
        'source_sha256': bindings, 'actual_mature_annual_oof_years': [2020, 2021, 2022, 2023, 2024],
        'actual_nonzero_gate_cases': 180, 'actual_zero_strength_weight_cases': 20,
        'conditional_reference_gate_axes': len(source_control['actual_reference_gate_axes']),
        'conditional_reference_scored_records': source_control['conditional_reference_scored_records'],
        'actual_gate_axes_and_count_refreeze_after_qualified_round63_required': True,
        'initial_preflight_failure': 'After all actual controls, string paths were passed to the hash helper; original source and freeze retained, v2 reran all cases with Path conversion.',
        'complete_output_fullfuture_and_official_quality_still_required': True,
        'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False}
    sync.atomic(sync.WORKTREE / prefix / 'manifest.json', sync.encoded(manifest))
    paths.append((prefix / 'manifest.json').as_posix())
    readme = ('# 同日模型意见分歧的自适应用途权重\n\n'
        '两种方向分别保留意见一致或意见分散时的模型权重；只用同日成熟模型预测的股票横截面百分位，'
        '不使用标签、未来价格或标签缺失信息。五个年度实际样本外数据的180项非零参数检查与20项关闭门控检查通过，'
        '日期前缀逐位一致，未来预测源扰动不会改变早期权重。\n\n'
        '源与生成器核验基于当前实际参考图的5个有效用途轴，对应129条预定评分记录；生成器排序控制值为合成值，'
        '没有产生新官方质量分。第64轮完整流程已排队，等待第63轮完整验证与执行来源核验通过后，'
        '重新冻结实际轴数、参数、模型字节，再进行完整连续向前官方评分、冻结、因果检查、候选推理及完整榜更新。\n\n'
        '原型实现通过不表示质量提高；本轮未训练新模型或读取测试标签。所有临时文件均使用D盘，空间不足时才可使用E盘。\n')
    sync.atomic(sync.WORKTREE / prefix / 'README.md', readme.encode('utf-8'))
    paths.append((prefix / 'README.md').as_posix())
    for source, digest in bindings.items():
        assert sync.sha(Path(source).read_bytes()) == digest, source
    for offset in range(0, len(paths), 50):
        sync.git('add', '--', *paths[offset:offset + 50])
    assert set(sync.git('diff', '--cached', '--name-only').splitlines()) == set(paths)
    for original in originals:
        path = (prefix / original.relative_to(ROOT)).as_posix()
        blob = sync.git('rev-parse', ':' + path)
        data = subprocess.check_output(['git', 'cat-file', 'blob', blob], cwd=sync.WORKTREE)
        assert sync.sha(data) == bindings[str(original)]
    sync.git('commit', '-m', '核验模型意见门控的五年样本外因果性并排队第64轮完整官方验证')
    commit = sync.git('rev-parse', 'HEAD')
    sync.git('push', 'origin', f'HEAD:refs/heads/{sync.BRANCH}')
    assert sync.git('ls-remote', '--heads', 'origin', f'refs/heads/{sync.BRANCH}').split()[0] == commit
    assert not sync.git('status', '--porcelain', '--untracked-files=no')
    receipt = {'status': 'pushed_and_remote_head_verified', 'at_local': sync.now(), 'commit': commit,
        'files': len(paths), 'new_quality_scores': 0, 'url': f'https://github.com/Zagadka-3906/stock-return-prediction/tree/{sync.BRANCH}/{prefix.as_posix()}'}
    with (sync.OUT / 'agreement_gate_controls_receipt.json').open('x', encoding='utf-8') as stream:
        json.dump(receipt, stream, ensure_ascii=False, indent=2)
    print(json.dumps(receipt, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
