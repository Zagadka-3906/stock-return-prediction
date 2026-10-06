"""Test fixed lower Huber thresholds against the actual weighted47 winner."""
from pathlib import Path
import sys
import time

ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,owned,create
SOURCE=A/'run_robust_conditional_residual_comparison50_20261006.py'


def main():
    # Do not race any original complete-ranking writer or its registration QA.
    preceding=A/'service_owned_workflows_20261006/simplex_residual47_round106_full_registration_v3'
    while not (preceding/'native_launch.json').exists():time.sleep(15)
    identity=read(preceding/'native_launch.json')
    while owned(identity):time.sleep(15)
    assert read(preceding/'service_execution.json')['status']=='passed'
    assert read(A/'optimization_20261003_r106/full_registration_execution.json')['status']=='passed'
    selected=read(A/'simplex_residual47_release_20261006/selection.json')
    pilot=read(A/'residual_simplex47_official_comparison_20261006/verification.json')
    cfg=selected['chosen_postprocessor']
    repeated=pilot['ensembles'][cfg['model']]
    assert len(repeated)==4
    assert set(repeated)==set(selected['native_component_names'])
    assert {n:repeated.count(n) for n in set(repeated)}==selected['component_repeat_counts']
    bank=read(A/'lowalpha_huber_residual_bank20_20261006/verification.json')
    assert bank['status']=='passed_actual20_matched_lowalpha_Huber_conditional_residual_native_models_and_independent_codec'
    assert bank['actual_native_fits']==20 and len(bank['configurations'])==4
    assert {c['alpha'] for c in bank['configurations'].values()}=={.05,.1}
    text=SOURCE.read_text(encoding='utf-8')
    changes={
        'robust_conditional_residual_native_bank20':'lowalpha_huber_residual_native_bank20',
        'robust_conditional_residual_bank20_20261006':'lowalpha_huber_residual_bank20_20261006',
        'robust_conditional_residual_comparison50_20261006':'lowalpha_huber_residual_comparison50_20261006',
        'longer_residual74_release_20261006':'simplex_residual47_release_20261006',
        'conditional_residual128_256_comparison74_20261006':'residual_simplex47_official_comparison_20261006',
        "reference_names = selected['native_component_names']":"reference_names = read(A / 'residual_simplex47_official_comparison_20261006/verification.json')['ensembles'][cfg['model']]",
        'passed_actual20_matched_L1_Huber_conditional_residual_native_models_and_independent_codec':
            'passed_actual20_matched_lowalpha_Huber_conditional_residual_native_models_and_independent_codec',
        'passed_actual50_matched_L1_Huber_residual_and_ensemble_full_official_comparisons':
            'passed_actual50_fixed_lowalpha_Huber_residual_and_ensemble_full_official_comparisons',
        'failed_preserved_matched_L1_Huber_residual_comparison50':'failed_preserved_fixed_lowalpha_Huber_residual_comparison50',
    }
    for before in sorted(changes,key=len,reverse=True):
        assert before in text,before
        text=text.replace(before,changes[before])
    before="{f'equal_mean_{loss}_residuals': [n for n in original_models if bank['configurations'][n]['objective'] == objective]\\n"
    # Replace the exact quoted source fragments that generate the original bank groups.
    before="        \"    ensembles = {f'equal_mean_{loss}_residuals': [n for n in original_models if bank['configurations'][n]['objective'] == objective]\\n\"\n        \"        for loss, objective in [('l1', 'regression_l1'), ('huber', 'huber')]}\\n\""
    after="        \"    ensembles = {f'equal_mean_huber_a{int(alpha*1000):03d}_residuals': [n for n in original_models if bank['configurations'][n]['alpha'] == alpha]\\n\"\n        \"        for alpha in [.05, .1]}\\n\""
    assert text.count(before)==1
    text=text.replace(before,after)
    before='    evidence = [SOURCE,';assert text.count(before)==1
    text=text.replace(before,'    evidence = [*LOWALPHA_EVIDENCE, SOURCE,')
    # Additional patches apply to the actual original comparison body before
    # execution. All official scoring, chronology and prefix controls remain.
    before="    namespace = {'__file__': __file__,"
    assert text.count(before)==1
    addition="""    extra_patches = {
        'from locked_read_hash_cache_20261004 import LockedReadHashCache': 'from win32_read_handle_hash_cache_20261006 import LockedReadHashCache',
        "'native_bank_source': str(BANK / 'verification.json')": "'native_bank_source': str(MATCHED_REFERENCE_BANKS[MATCHED_REFERENCE_NAMES[0]] / 'verification.json') if index == 1 else str(BANK / 'verification.json')",
        "'score_gain_over_parent100': metrics['final_score'] - baseline['final_score'],": "'score_gain_over_parent100': metrics['final_score'] - baseline['final_score'], 'score_gain_over_selected47': metrics['final_score'] - read(MATCHED_RELEASE / 'calibrated_csv_official.json')['metrics']['final_score'],",
        "'cases': cases, 'ensembles': ensembles,": "'cases': cases, 'ensembles': ensembles, 'matched_reference_ordered_repeated_native_components': MATCHED_REFERENCE_NAMES, 'fixed_Huber_absolute_thresholds': [.05, .1],",
    }
    for before in sorted(extra_patches,key=len,reverse=True):
        assert before in text,before
        text=text.replace(before,extra_patches[before])
"""
    text=text.replace(before,addition+before)
    evidence=[Path(__file__),SOURCE,A/'train_lowalpha_huber_residual_bank20_20261006.py',
        A/'conditional_identity_regression_tree_codec_20261006.py',
        A/'win32_read_handle_hash_cache_20261006.py',A/'win32_read_handle_hash_cache_full104_preflight_20261006.json',
        A/'lowalpha_huber_residual20_frozen_hidden_admission_20261006.json',
        A/'simplex_residual47_unique_storage_arithmetic_preflight_20261006.json',
        A/'residual_simplex47_official_comparison_20261006'/f"{cfg['model']}_verification.json",
        preceding/'service_execution.json',A/'github_validation_sync_main_20261005/round106_receipt.json']
    namespace={'__file__':__file__,'__name__':'actual_fixed_lowalpha_Huber_full50_comparison',
        'LOWALPHA_EVIDENCE':evidence}
    exec(compile(text,str(SOURCE),'exec'),namespace)
    namespace['main']()


if __name__=='__main__':main()
