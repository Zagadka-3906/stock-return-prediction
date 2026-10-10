"""Publish all real low-alpha Huber matched native controls on main."""
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
SOURCE=A/'publish_conditional_residual_evidence_20261006.py'


def main():
    text=SOURCE.read_text(encoding='utf-8')
    changes={
        'conditional_flag_residual_bank_20261006':'lowalpha_huber_residual_bank20_20261006',
        "'conditional_flag_residual_native_bank'":"'lowalpha_huber_residual_native_bank20'",
        'passed_actual20_past_OOF_conditional_residual_native_models_and_independent_codec':
            'passed_actual20_matched_lowalpha_Huber_conditional_residual_native_models_and_independent_codec',
        'service_owned_workflows_20261006/conditional_flag_round101_full_registration_v2':
            'service_owned_workflows_20261006/simplex_residual47_round106_full_registration',
        'conditional_residual_{phase}_github_20261006':'lowalpha_huber_residual_{phase}_github_20261006',
        'validation_sync/conditional_residual_{phase}_20261006':'validation_sync/lowalpha_huber_residual_{phase}_20261006'}
    for before in sorted(changes,key=len,reverse=True):
        assert before in text,before
        text=text.replace(before,changes[before])
    before="    sources += [p for p in bank.rglob('*.json') if not p.name.startswith('model_dump_')]"
    assert text.count(before)==1
    text=text.replace(before,
        "    sources += [PUBLICATION_TEMPLATE, A / 'train_lowalpha_huber_residual_bank20_20261006.py',\n"
        "        A / 'train_robust_conditional_residual_bank20_20261006.py',\n"
        "        A / 'conditional_identity_regression_tree_codec_20261006.py',\n"
        "        A / 'lowalpha_huber_residual20_frozen_hidden_admission_20261006.json',\n"
        "        A / 'lowalpha_huber_residual20_hidden_launch_20261006.json']\n"+before)
    start=text.index("        payload[(prefix / 'README.md').as_posix()] = (")
    end=text.index('        for name, data in payload.items():',start)
    text=text[:start]+"""        payload[(prefix / 'README.md').as_posix()] = (
            '# 固定较低阈值Huber条件残差：20个真实原生模型核验\\n\\n'
            '预先固定Huber绝对梯度阈值alpha0.05与0.1，各包含仅父95百分位及63个提供字段加百分位两种特征。'
            '2021—2024向前验证及2025最终模型，共20次新拟合，全部128棵树；不复用失败运行的部分拟合。'
            '与既有L2参照逐项核对目标、成熟训练窗口、训练行数、特征及除损失和alpha以外的参数。'
            '原生保存重载、独立树解码和80/260/975日前缀检查必须实际完成。'
            '保持2020与非涨停原始预测为父方案，未来特征和标签不参与训练。\\n\\n'
            '本阶段仅记录真实训练及核验；尚需完整官方比较、候选冻结推理、完整榜及主分支发布。'
            '只提交main，保留记录、分数、失败与源码，不上传模型或数据。\\n'
        ).encode('utf-8')
"""+text[end:]
    namespace={'__file__':__file__,'__name__':'actual_lowalpha_Huber_native20_main_evidence','PUBLICATION_TEMPLATE':SOURCE}
    exec(compile(text,str(SOURCE),'exec'),namespace)
    namespace['main']('bank')


if __name__=='__main__':main()
