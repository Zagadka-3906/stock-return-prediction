"""Publish every real L1/Huber native control and all50 official comparisons on main."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
SOURCE = A / 'publish_conditional_residual_evidence_20261006.py'


def main(phase):
    assert phase in ('bank', 'scores')
    text = SOURCE.read_text(encoding='utf-8')
    patches = {
        'conditional_flag_residual_bank_20261006': 'robust_conditional_residual_bank20_20261006',
        'conditional_flag_residual_official_comparison_20261006': 'robust_conditional_residual_comparison50_20261006',
        "'conditional_flag_residual_native_bank'": "'robust_conditional_residual_native_bank20'",
        "else 'conditional_flag_residual_official_comparison')": "else 'robust_conditional_residual_comparison50')",
        'passed_actual20_past_OOF_conditional_residual_native_models_and_independent_codec': 'passed_actual20_matched_L1_Huber_conditional_residual_native_models_and_independent_codec',
        'passed_actual49_conditional_residual_native_and_ensemble_full_official_comparisons': 'passed_actual50_matched_L1_Huber_residual_and_ensemble_full_official_comparisons',
        '== 49': '== 50', 'else 49': 'else 50',
        'service_owned_workflows_20261006/conditional_flag_round101_full_registration_v2': 'service_owned_workflows_20261006/conditional_residual128_256_scores74_evidence_publication',
        'service_owned_workflows_20261006/conditional_residual_bank_evidence_publication': 'service_owned_workflows_20261006/robust_conditional_residual_bank20_evidence_publication',
        'conditional_residual_{phase}_github_20261006': 'robust_conditional_residual_{phase}_github_20261006',
        'validation_sync/conditional_residual_{phase}_20261006': 'validation_sync/robust_conditional_residual_{phase}_20261006',
    }
    for before in sorted(patches, key=len, reverse=True):
        assert before in text, before
        text = text.replace(before, patches[before])
    text = text.replace("'train_robust_conditional_residual_bank20_20261006.py'", "'train_conditional_flag_residual_bank_20261006.py'")
    text = text.replace("'run_robust_conditional_residual_comparison50_20261006.py'", "'run_conditional_flag_residual_official_comparison_20261006.py'")
    marker = "    sources += [p for p in bank.rglob('*.json') if not p.name.startswith('model_dump_')]"
    assert text.count(marker) == 1
    text = text.replace(marker,
        "    sources += [PUBLICATION_TEMPLATE, A / 'train_robust_conditional_residual_bank20_20261006.py', A / 'run_robust_conditional_residual_comparison50_20261006.py', A / 'conditional_flag_residual_extrapolation_transform_20261006.py']\n" + marker)
    start = text.index("        payload[(prefix / 'README.md').as_posix()] = (")
    end = text.index('        for name, data in payload.items():', start)
    text = text[:start] + """        payload[(prefix / 'README.md').as_posix()] = (
            '# L1与Huber条件残差：实际核验与官方比较\\n\\n'
            '四个配置为L1/Huber两种损失，各包含仅父95百分位及63个因果字段加该百分位两种特征。'
            '相对于已完成L2模型只改变训练损失（Huber固定alpha0.9），保持相同128棵树上限、'
            '训练窗口、目标、特征和其余原生参数。四个配置各有2021—2024及2025最终模型，共20次真实拟合。'
            '所有原生、重载、独立树遍历和80/260/975日前缀检查必须实际完成。\\n\\n'
            '50项比较包括四个新原生头、两个按损失等权集成，各测试0.1/0.25/0.5/0.75/1/1.25/1.5/2，'
            '再加入父100与74项比较完整选中的方案两个锚点。原方案全部5635800行原始预测和八项指标逐位复核。'
            '最终过去收益率映射CSV使用原官方脚本评分；不重置年度换手，不增加单指标或显著性淘汰门槛。\\n\\n'
            f'本目录阶段为{phase}，完整候选推理、冻结、完整榜QA及发布另行完成。'
            '不宣称全局优化或资源边界已经完成。只发布main，保留所有源码、失败、分数与控制证据，不上传权重或数据。\\n'
        ).encode('utf-8')
""" + text[end:]
    namespace = {'__file__': __file__, '__name__': 'actual_robust_conditional_residual_evidence_publication', 'PUBLICATION_TEMPLATE': SOURCE}
    exec(compile(text, str(SOURCE), 'exec'), namespace)
    namespace['main'](phase)


if __name__ == '__main__': main(sys.argv[1])
