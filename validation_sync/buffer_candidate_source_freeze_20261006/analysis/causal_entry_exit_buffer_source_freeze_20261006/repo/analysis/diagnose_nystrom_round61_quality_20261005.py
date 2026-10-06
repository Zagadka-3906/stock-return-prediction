"""Attribute completed training-only R61 single-role losses using frozen scores."""
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
ROUND = ROOT / 'analysis/optimization_20261003_r61'
OUT = ROOT / 'analysis/nystrom_round61_quality_diagnostic_20261005'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def create(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    selection_path = ROUND / 'selection.json'
    selection, protocol = read(selection_path), read(ROUND / 'protocol.json')
    assert selection['status'] == 'frozen_before_test_prediction'
    assert selection['scored_records'] == protocol['expected_scored_records'] == 100
    assert len(selection['ranking']) == 100 and selection['score_gain'] == 0.
    OUT.mkdir(exist_ok=True)
    inputs = {str(p): sha(p) for p in (Path(__file__), selection_path, ROUND / 'protocol.json')}
    for row in selection['ranking']:
        source = Path(row['official_score_cache']['official_metrics_source'])
        digest = selection['frozen_sha256'][source.relative_to(ROOT).as_posix()]
        assert sha(source) == digest and read(source)['metrics'] == row['metrics']
        inputs[str(source)] = digest
    create(OUT / 'frozen_before_diagnostic.json', {
        'status': 'frozen_existing_training_only_scores', 'at_local': datetime.now().isoformat(),
        'input_sha256': inputs, 'scored_records': 100, 'new_quality_scores': 0,
        'new_model_fits': 0, 'test_labels_read': False})
    baseline = read(ROUND.parent / 'optimization_20261003_r60/selection.json')['winner']['metrics']
    groups = defaultdict(list)
    for row in selection['ranking']:
        node = next(layer for layer in row['nystrom_ridge_role_scheme_graph']['layers'] if layer['round'] == 61)
        active = [(role, spec) for role, spec in node['specs'].items() if spec['weight'] > 0]
        # Restrict to one new role and no simultaneous final limit adjustment.
        if len(active) != 1 or node['additional_delta'] != 0:
            continue
        role, spec = active[0]
        groups[(spec['model'], role)].append((row, spec['weight']))
    table = []
    for (model, role), rows in sorted(groups.items()):
        row, weight = max(rows, key=lambda item: item[0]['connected_final_score'])
        metrics = row['metrics']
        changes = {k: metrics[k] - baseline[k] for k in ('ic_mean', 'annual_excess', 'mean_turnover')}
        contributions = {'RankIC': .4 * changes['ic_mean'], 'annual_excess': .3 * changes['annual_excess'],
                         'turnover': -.3 * changes['mean_turnover']}
        loss = metrics['final_score'] - baseline['final_score']
        assert abs(sum(contributions.values()) - loss) < 1e-12
        table.append({'model': model, 'role': role, 'single_role_records': len(rows),
                      'best_weight': weight, 'best_score': metrics['final_score'], 'delta_vs_baseline': loss,
                      'metrics': metrics, 'metric_changes': changes, 'score_components': contributions,
                      'wave': row['wave'], 'arm': row['arm']})
    assert len(table) == 12 and all(row['delta_vs_baseline'] < 0 for row in table)
    for path, digest in inputs.items():
        assert sha(path) == digest, path
    result = {'status': 'passed_frozen_score_loss_diagnostic', 'at_local': datetime.now().isoformat(),
        'input_sha256': inputs, 'completed_training_official_records': 100,
        'baseline_metrics': baseline, 'model_role_table': table,
        'best_nonzero_single_role': max(table, key=lambda row: row['best_score']),
        'all_tested_nonzero_single_roles_below_baseline': True,
        'selected_all_three_new_kernel_weights_are_zero': True,
        'comparative_scope': 'Four declared64/128-landmark, lengthscale1, penalty.1 configurations and their declared complete output role grid only.',
        'broader_kernel_capacity_seed_lengthscale_and_penalty_uncovered': True,
        'standalone_round62_and_full_round61_closure_still_required': True,
        'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False}
    create(OUT / 'verification.json', result)
    lines = ['# 第61轮已冻结评分的核模型用途诊断', '',
             '100条训练内部官方评分已经完成，选中方案仍保持三种新增核模型用途权重为零。完整流程的校准、候选推理、因果与来源核验另行完成；本文件不冒充第61轮已完整结束。', '',
             '| 模型 | 用途 | 最佳非零权重 | 官方分相对基准变化 | IC分量 | 超额收益分量 | 换手分量 |',
             '| --- | --- | ---: | ---: | ---: | ---: | ---: |']
    for row in table:
        c = row['score_components']
        lines.append(f"| {row['model']} | {row['role']} | {row['best_weight']:.4f} | {row['delta_vs_baseline']:+.12f} | {c['RankIC']:+.12f} | {c['annual_excess']:+.12f} | {c['turnover']:+.12f} |")
    lines += ['', '只按单一新增用途、未同时调整最终涨停偏移的完整方案分组，排除复合行的贡献混淆。分量是官方公式对该完整方案指标变化的算术分解，未声称统计因果效应。', '',
              '该网格没有提升不能证明核方法整体不可行；更多核规模、种子、长度尺度与正则强度尚未覆盖，第62轮独立完整方案也仍需评分。未读取测试标签、训练新模型或计算新候选分数。']
    with (OUT / 'README.md').open('x', encoding='utf-8') as stream:
        stream.write('\n'.join(lines) + '\n')
    best = result['best_nonzero_single_role']
    print(json.dumps({'status': result['status'], 'model_role_groups': len(table),
        'best_nonzero_model': best['model'], 'best_nonzero_role': best['role'],
        'best_nonzero_gap': best['delta_vs_baseline']}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
