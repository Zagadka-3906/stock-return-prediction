"""Publish all47 real convex-mixture scores on main after preceding main holders."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
SOURCE = A / 'publish_conditional_residual_evidence_20261006.py'


def main():
    text = SOURCE.read_text(encoding='utf-8')
    patches = {
        'conditional_flag_residual_bank_20261006': 'conditional_residual128_256_bank40_20261006',
        'conditional_flag_residual_official_comparison_20261006': 'residual_simplex47_official_comparison_20261006',
        "'conditional_flag_residual_official_comparison')": "'residual_simplex47_official_comparison')",
        'passed_actual49_conditional_residual_native_and_ensemble_full_official_comparisons':
            'passed_actual47_convex_simplex_residual_ensemble_full_official_comparisons',
        '== 49': '== 47', 'else 49': 'else 47',
        'service_owned_workflows_20261006/conditional_flag_round101_full_registration_v2':
            'service_owned_workflows_20261006/robust_residual50_round105_full_registration',
        'service_owned_workflows_20261006/conditional_residual_bank_evidence_publication':
            'service_owned_workflows_20261006/conditional_residual128_256_bank40_evidence_publication',
        'conditional_residual_{phase}_github_20261006': 'residual_simplex47_{phase}_github_20261006',
        'validation_sync/conditional_residual_{phase}_20261006': 'validation_sync/residual_simplex47_{phase}_20261006',
        "'actual_native_model_fits': 20": "'existing_native_bank_fits': 40, 'actual_new_native_model_fits': 0",
    }
    for before in sorted(patches, key=len, reverse=True):
        assert before in text, before
        text = text.replace(before, patches[before])
    before = "    sources += [p for p in bank.rglob('*.json') if not p.name.startswith('model_dump_')]"
    assert text.count(before) == 1
    text = text.replace(before,
        "    sources += [PUBLICATION_TEMPLATE, A / 'run_residual_simplex47_official_comparison_20261006.py',\n"
        "        A / 'conditional_flag_residual_extrapolation_transform_20261006.py',\n"
        "        A / 'train_conditional_residual128_256_bank40_20261006.py',\n"
        "        A / 'residual_simplex47_hidden_admission_20261006.json']\n" + before)
    # The bank comparison retains all true info/control JSON, while the actual
    # ensemble source is added above rather than claiming a new native fit.
    start = text.index("        payload[(prefix / 'README.md').as_posix()] = (")
    end = text.index('        for name, data in payload.items():', start)
    text = text[:start] + """        payload[(prefix / 'README.md').as_posix()] = (
            '# 三个残差模型的非等权凸集成：47项完整官方比较\\n\\n'
            '复用已实际拟合并核验的leaf7/15/31三个256棵树残差模型。'
            '预先固定全部15组非负整数权重，和为4，按四分之一步长覆盖三模型单纯形；'
            '每组测试0.75/1/1.25残差幅度，再加入父100与此前74项验证获胜方案两个锚点。'
            '计算按leaf7/15/31顺序重复相应次数，浮点64逐项求和后除4；'
            '保留重复加法的真实顺序，后续候选推理需准确复现该算术。\\n\\n'
            '全部5635800行连接验证使用过去收益率映射和原官方评分脚本；'
            '检查1212日非涨停顺序、2020与非涨停逐位不变及80/260/975日前缀。'
            '原获胜锚点的全部预测和八项指标逐位复核。'
            '本轮没有新原生拟合；冻结候选、独立推理及完整榜另行完成。'
            '只发布main，保留记录、分数、源码与失败，不上传数据或模型权重。\\n'
        ).encode('utf-8')
""" + text[end:]
    namespace = {'__file__': __file__, '__name__': 'actual_simplex47_scores_main_publication', 'PUBLICATION_TEMPLATE': SOURCE}
    exec(compile(text, str(SOURCE), 'exec'), namespace)
    namespace['main']('scores')


if __name__ == '__main__':
    main()
