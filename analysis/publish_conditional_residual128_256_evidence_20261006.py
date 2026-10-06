"""Publish actual longer-tree native controls or74 full-score comparisons to main."""
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
        'conditional_flag_residual_bank_20261006': 'conditional_residual128_256_bank40_20261006',
        'conditional_flag_residual_official_comparison_20261006': 'conditional_residual128_256_comparison74_20261006',
        "'conditional_flag_residual_native_bank'": "'conditional_residual128_256_native_bank40'",
        "else 'conditional_flag_residual_official_comparison')": "else 'conditional_residual128_256_comparison74')",
        'passed_actual20_past_OOF_conditional_residual_native_models_and_independent_codec':
            'passed_actual40_matched128_256_conditional_residual_native_models_and_independent_codec',
        'passed_actual49_conditional_residual_native_and_ensemble_full_official_comparisons':
            'passed_actual74_matched128_256_residual_and_ensemble_full_official_comparisons',
        '== 20': '== 40', '== 49': '== 74', 'else 49': 'else 74',
        "'actual_native_model_fits': 20": "'actual_native_model_fits': 40",
        'service_owned_workflows_20261006/conditional_flag_round101_full_registration_v2':
            'service_owned_workflows_20261006/residual_extrapolation43_round103_full_registration',
        'service_owned_workflows_20261006/conditional_residual_bank_evidence_publication':
            'service_owned_workflows_20261006/conditional_residual128_256_bank40_evidence_publication',
        'conditional_residual_{phase}_github_20261006': 'conditional_residual128_256_{phase}_github_20261006',
        'validation_sync/conditional_residual_{phase}_20261006': 'validation_sync/conditional_residual128_256_{phase}_20261006',
        '每个模型完成2021—2024四个年度模型及2025最终模型，共20次真实CPU拟合，':
            '八个配置各完成2021—2024四个年度模型及2025最终模型，共40次真实CPU拟合，',
        '预定最多64轮；': '预定128或256轮，并逐项验证完整前64棵树与已有64轮模型相同；',
        '49项质量比较为四个原生残差、三个特征模型的等权平均及全部四个模型的等权平均，':
            '74项质量比较为八个原生残差、各轮数下三个特征模型及四个模型的等权平均，',
        '分别测试0.01/0.025/0.05/0.1/0.25/0.5/0.75/1，加一个父方案锚点。':
            '分别测试0.5/0.75/1/1.25/1.5/2，加实际100及完整合格102两个锚点。',
        'scores是49项自然结束后': 'scores是74项自然结束后'}
    for before in sorted(patches, key=len, reverse=True):
        assert before in text, before
        text = text.replace(before, patches[before])
    # The original templates stay available alongside the actual new runners.
    text = text.replace("'train_conditional_residual128_256_bank40_20261006.py'", "'train_conditional_flag_residual_bank_20261006.py'")
    text = text.replace("'run_conditional_residual128_256_comparison74_20261006.py'", "'run_conditional_flag_residual_official_comparison_20261006.py'")
    marker = "    sources += [p for p in bank.rglob('*.json') if not p.name.startswith('model_dump_')]"
    assert text.count(marker) == 1
    text = text.replace(marker,
        "    sources += [PUBLICATION_TEMPLATE, A / 'train_conditional_residual128_256_bank40_20261006.py', A / 'run_conditional_residual128_256_comparison74_20261006.py', A / 'conditional_flag_residual_extrapolation_transform_20261006.py']\n" + marker)
    namespace = {'__file__': __file__, '__name__': 'actual_matched_longer_residual_evidence_publication',
                 'PUBLICATION_TEMPLATE': SOURCE}
    exec(compile(text, str(SOURCE), 'exec'), namespace)
    namespace['main'](phase)


if __name__ == '__main__': main(sys.argv[1])
