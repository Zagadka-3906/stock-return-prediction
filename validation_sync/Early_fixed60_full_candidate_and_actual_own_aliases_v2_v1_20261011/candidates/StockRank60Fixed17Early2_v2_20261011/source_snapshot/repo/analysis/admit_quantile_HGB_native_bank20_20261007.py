"""Admit actual four quantile codec controls and the explicit mature20-fit source plan."""
from pathlib import Path
import ast
import sys
import time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def main():
    folder=A/'service_owned_workflows_20261006/quantile_HGB_codec4_preflight'
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(10)
    assert read(folder/'service_execution.json')['status']=='passed'
    proof_path=A/'quantile_HGB_codec_preflight_20261007/verification.json';proof=read(proof_path)
    assert proof['status']=='passed_actual_four_historical_quantile_HGB_codec_controls'
    assert proof['actual_diagnostic_fits']==len(proof['records'])==4 and proof['actual_selection_model_fits']==proof['actual_official_scores']==0
    plan_path=A/'quantile_HGB_native_bank20_plan_20261007.json';plan=read(plan_path)
    assert len(plan['configurations'])==4 and plan['prospective_native_model_fits']==20
    assert plan['fixed_parameters']['max_iter']==128 and plan['fixed_parameters']['min_samples_leaf']==64 and plan['fixed_parameters']['early_stopping'] is False
    assert {(cfg['quantile'],cfg['max_leaf_nodes']) for cfg in plan['configurations'].values()}=={(.25,7),(.25,15),(.75,7),(.75,15)}
    assert all(cfg['loss']=='quantile' for cfg in plan['configurations'].values())
    trainer=A/'train_quantile_HGB_native_bank20_20261007.py';text=trainer.read_text(encoding='utf8');ast.parse(text)
    requirements=["train = (kd < cutoff) & available_label",'last < cutoff and label_end <= cutoff',
      'preprocessing = fit_preprocessing(x[train])','model.fit(bx, y[train])',
      "model.n_iter_ == plan['fixed_parameters']['max_iter']",'range(2021, 2026)',
      "pl.col('is_train') & (pl.col('flag_limit_up') == 1)","first2020_and_nonflag_identity_zero_residual"]
    for needle in requirements:assert needle in text,needle
    sources=[Path(__file__),plan_path,proof_path,trainer,A/'verify_quantile_HGB_codec_preflight_20261007.py',
      A/'quantile_HGB_native_bank20_source_preparation_20261007.json',A/'cpu_conditional_residual_hgb_codec_20261007.py']
    pins={**proof['input_sha256'],**{str(p):sha(p) for p in sources}}
    for p,d in pins.items():assert sha(p)==d,p
    create(A/'quantile_HGB_native_bank20_admission_20261007.json',{'status':'passed_actual4_quantile_codec_fits_and20_mature_window_plan_source_admission',
      'input_sha256':pins,'configurations':plan['configurations'],'prospective_selection_native_fits':20,
      'actual_diagnostic_fits':4,'actual_selection_fits_at_admission':0,'actual_official_scores_at_admission':0,
      'target_teacher106_current_X_and_mature_training_labels_only':True,'final_native_models_not_future_predictions':True,
      'full119_scoring_freeze_candidate_QA30_main_still_required':True,'test_labels_read':False})
    print({'status':'admitted','actual_diagnostic_fits':4,'prospective_selection_fits':20},flush=True)

if __name__=='__main__':main()
