"""Publish all naturally completed43 full-score trials without qualifying early."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
SOURCE = A / 'publish_conditional_residual_evidence_20261006.py'


def main():
    text = SOURCE.read_text(encoding='utf-8')
    patches = {
        'conditional_flag_residual_official_comparison_20261006': 'conditional_residual_extrapolation43_official_20261006',
        "else 'conditional_flag_residual_official_comparison')": "else 'conditional_residual_extrapolation43_official_comparison')",
        'passed_actual49_conditional_residual_native_and_ensemble_full_official_comparisons':
            'passed_actual43_conditional_residual_extrapolation_full_official_comparisons',
        "== 49": "== 43", "else 49": "else 43",
        'service_owned_workflows_20261006/conditional_flag_round101_full_registration_v2':
            'service_owned_workflows_20261006/progress_monitor_v36_recovery_publication',
        'conditional_residual_{phase}_github_20261006': 'conditional_residual_extrapolation43_{phase}_github_20261006',
        'validation_sync/conditional_residual_{phase}_20261006': 'validation_sync/conditional_residual_extrapolation43_{phase}_20261006',
        '父方案是已完整合格第100轮。': '比较基准是已完整合格第102轮，残差计算沿用第100轮。',
        '49项质量比较': '43项质量比较',
        '分别测试0.01/0.025/0.05/0.1/0.25/0.5/0.75/1，加一个父方案锚点。':
            '分别测试1.25/1.5/2/3/4/6/8，加一个第102轮完整方案锚点；无新增原生拟合。',
        'scores是49项自然结束后': 'scores是43项自然结束后'}
    for before in sorted(patches, key=len, reverse=True):
        assert before in text, before
        text = text.replace(before, patches[before])
    # Keep the original comparator source as the scientific control template,
    # and include the actual extended runner and its declared domain too.
    text = text.replace("'run_conditional_residual_extrapolation43_official_20261006.py'",
                        "'run_conditional_flag_residual_official_comparison_20261006.py'")
    marker = "    sources += [p for p in bank.rglob('*.json') if not p.name.startswith('model_dump_')]"
    assert text.count(marker) == 1
    text = text.replace(marker,
        "    sources += [PUBLICATION_TEMPLATE, A / 'run_conditional_residual_extrapolation43_comparison_20261006.py', A / 'conditional_flag_residual_extrapolation_transform_20261006.py', A / 'github_validation_sync_main_20261005/round102_receipt.json']\n" + marker)
    namespace = {'__file__': __file__, '__name__': 'actual_residual_extrapolation43_evidence_publication',
                 'PUBLICATION_TEMPLATE': SOURCE}
    exec(compile(text, str(SOURCE), 'exec'), namespace)
    namespace['main']('scores')


if __name__ == '__main__':
    main()
