"""Fit20 fresh matched Huber residual models at fixed absolute alpha0.05/0.1."""
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
SOURCE=A/'train_robust_conditional_residual_bank20_20261006.py'


def main():
    text=SOURCE.read_text(encoding='utf-8')
    changes={
        'robust_conditional_residual_bank20_20261006':'lowalpha_huber_residual_bank20_20261006',
        'service_owned_workflows_20261006/longer_residual74_candidate_sealing':
            'service_owned_workflows_20261006/simplex_residual47_candidate_sealing',
        'longer_residual74_release_20261006/source_package_verification.json':
            'simplex_residual47_release_20261006/source_package_verification.json',
        'passed_actual20_matched_L1_Huber_conditional_residual_native_models_and_independent_codec':
            'passed_actual20_matched_lowalpha_Huber_conditional_residual_native_models_and_independent_codec',
        "for loss, objective in [('l1', 'regression_l1'), ('huber', 'huber')]:":
            "for loss, objective in [('huber_a005', 'huber'), ('huber_a010', 'huber')]:",
        "**({'alpha': .9} if loss == 'huber' else {})":"**{'alpha': FIXED_ALPHAS[loss]}",
        "params['alpha'] == .9":"params['alpha'] == cfg['alpha']",
        'L2 objective becomes regression_l1 or huber with alpha0.9; same128 rounds and all other native parameters':
            'L2 objective becomes huber with fixed absolute alpha0.05 or0.1; same128 rounds and all other native parameters',
        "'robust_loss_alpha_not_selected_from_validation': 0.9":"'fixed_absolute_huber_alphas_not_selected_from_validation': [0.05, 0.1]",
        'L1/Huber x rank-only/full63pluspercentile leaf7 x four annual and one final windows':
            'Huber alpha0.05/0.1 x rank-only/full63pluspercentile leaf7 x four annual and one final windows',
        'failed_preserved_actual_L1_Huber_conditional_residual_bank20':'failed_preserved_actual_lowalpha_Huber_conditional_residual_bank20',
    }
    for before in sorted(changes,key=len,reverse=True):
        assert before in text,before
        text=text.replace(before,changes[before])
    before="    evidence = [SOURCE, REFERENCE / 'verification.json',"
    assert text.count(before)==1
    text=text.replace(before,
        "    evidence = [SOURCE, LOWALPHA_SOURCE, A / 'conditional_identity_regression_tree_codec_20261006.py',\n"
        "        A / 'lowalpha_huber_residual20_frozen_hidden_admission_20261006.json', REFERENCE / 'verification.json',")
    before="    namespace = {'__file__': __file__, '__name__': 'actual_robust_conditional_residual_bank20',"
    assert text.count(before)==1
    text=text.replace(before,
        "    before = 'from conditional_flag_rank_codec_20261006 import clean_matrix, predict_dump'\n"
        "    assert text.count(before) == 1\n"
        "    text = text.replace(before, 'from conditional_identity_regression_tree_codec_20261006 import clean_matrix, predict_dump')\n"
        "    namespace = {'__file__': __file__, '__name__': 'actual_lowalpha_Huber_conditional_residual_bank20',")
    before="'MATCHED_REFERENCE_EVIDENCE': evidence, 'MATCHED_REFERENCE': REFERENCE}"
    assert text.count(before)==1
    text=text.replace(before,
        "'MATCHED_REFERENCE_EVIDENCE': evidence, 'MATCHED_REFERENCE': REFERENCE, 'FIXED_ALPHAS': FIXED_ALPHAS}")
    namespace={'__file__':__file__,'__name__':'actual_fresh_lowalpha_Huber_native_bank20',
        'FIXED_ALPHAS':{'huber_a005':.05,'huber_a010':.1},'LOWALPHA_SOURCE':Path(__file__)}
    exec(compile(text,str(SOURCE),'exec'),namespace)
    namespace['main']()


if __name__=='__main__':main()
