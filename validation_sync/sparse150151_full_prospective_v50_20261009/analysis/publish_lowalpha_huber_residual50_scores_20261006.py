"""Publish all50 actual official capsules after genuine science and bank publication."""
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
SOURCE=A/'publish_conditional_residual_evidence_20261006.py'


def main():
    text=SOURCE.read_text(encoding='utf-8')
    changes={
        'conditional_flag_residual_bank_20261006':'lowalpha_huber_residual_bank20_20261006',
        'conditional_flag_residual_official_comparison_20261006':'lowalpha_huber_residual_comparison50_20261006',
        "'conditional_flag_residual_native_bank'":"'lowalpha_huber_residual_native_bank20'",
        "'conditional_flag_residual_official_comparison'":"'lowalpha_huber_residual_comparison50_v2'",
        'passed_actual20_past_OOF_conditional_residual_native_models_and_independent_codec':'passed_actual20_matched_lowalpha_Huber_conditional_residual_native_models_and_independent_codec',
        'passed_actual49_conditional_residual_native_and_ensemble_full_official_comparisons':'passed_actual50_fixed_lowalpha_Huber_residual_and_ensemble_full_official_comparisons',
        "len(proof['records']) == 49":"len(proof['records']) == 50",
        "0 if phase == 'bank' else 49":"0 if phase == 'bank' else 50",
        'service_owned_workflows_20261006/conditional_flag_round101_full_registration_v2':'service_owned_workflows_20261006/simplex_residual47_round106_full_registration_v5',
        'service_owned_workflows_20261006/conditional_residual_bank_evidence_publication':'service_owned_workflows_20261006/lowalpha_huber_residual_bank20_evidence_publication_v2',
        'conditional_residual_{phase}_github_20261006':'lowalpha_huber_residual_{phase}_github_20261006',
        'validation_sync/conditional_residual_{phase}_20261006':'validation_sync/lowalpha_huber_residual_{phase}_20261006',
    }
    for before in sorted(changes,key=len,reverse=True):
        assert before in text,before
        text=text.replace(before,changes[before])
    before="    sources += [p for p in bank.rglob('*.json') if not p.name.startswith('model_dump_')]"
    assert text.count(before)==1
    text=text.replace(before,"    sources += [SCORES_PUBLICATION_SOURCE, A/'run_lowalpha_huber_residual_comparison50_v2_20261006.py', A/'run_lowalpha_huber_residual_comparison50_20261006.py', A/'lowalpha_huber_residual50_source_construction_preflight_20261006.json', A/'train_lowalpha_huber_residual_bank20_20261006.py', A/'publish_lowalpha_huber_residual20_evidence_v2_20261006.py', A/'lowalpha_huber_residual_bank_github_v2_20261006/receipt.json']\n"+before)
    start=text.index("        payload[(prefix / 'README.md').as_posix()] = (")
    end=text.index('        for name, data in payload.items():',start)
    text=text[:start]+"""        payload[(prefix / 'README.md').as_posix()] = (
            '# 固定较低Huber阈值条件残差：50项完整官方验证\\n\\n'
            'alpha0.05/0.1，各含仅父95百分位及63提供字段加百分位两个原生模型，'
            '加各alpha下两个模型的等权均值，共6个头；预定幅度0.1/0.25/0.5/0.75/1/1.25/1.5/2。'
            '另含父100和已实际验证的47项凸集成最佳方案两个锚点，共50项。'
            '参考锚点严格沿用原始重复分量顺序，不将不等权集成误作唯一分量的等权均值。'
            '验证为训练集内部2020—2024连续向前5635800行/1212日/4650股，'
            '每项最终过去收益率映射CSV调用原官方脚本；连续边界换手不重置。'
            '保留全部官方分数、原始评分胶囊、预冻结声明及80/260/975日前缀因果控制。'
            '本阶段不声称已完成候选冻结推理或完整榜资格；后续登记单独执行。'
            '真实测试标签及未来价格不参与选模，只提交main，模型和数据不上传。\\n'
        ).encode('utf-8')
"""+text[end:]
    ns={'__file__':__file__,'__name__':'actual_lowalpha50_main_scores_publication','SCORES_PUBLICATION_SOURCE':Path(__file__)}
    exec(compile(text,str(SOURCE),'exec'),ns);ns['main']('scores')


if __name__=='__main__':main()
