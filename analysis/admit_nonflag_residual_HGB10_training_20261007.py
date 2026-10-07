"""Admit genuine two-model codecs and explicit nonflag mature-window training sources."""
from pathlib import Path
import ast,sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def main():
    import time
    f=A/'service_owned_workflows_20261006/nonflag_residual_HGB_codec2_preflight'
    while owned(read(f/'native_launch.json')):time.sleep(10)
    assert read(f/'service_execution.json')['status']=='passed'
    diag=A/'nonflag_residual_HGB_codec2_preflight_20261007/verification.json';proof=read(diag)
    assert proof['status']=='passed_actual2_nonflag_residual_HGB_historical_codec_controls' and proof['actual_diagnostic_fits']==len(proof['records'])==2
    plan_path=A/'nonflag_residual_HGB10_plan_20261007.json';plan=read(plan_path)
    assert len(plan['configurations'])==2 and plan['prospective_native_fits']==10 and plan['native_fit_years']==[2021,2022,2023,2024,2025]
    assert plan['fixed_parameters']['max_iter']==96 and plan['fixed_parameters']['early_stopping'] is False
    source=A/'train_nonflag_residual_HGB_bank10_20261007.py';text=source.read_text(encoding='utf8');ast.parse(text)
    for needle in ["full.filter(pl.col('flag_limit_up')!=1)","train=(kd<cutoff)&eligible",'last<cutoff and label_end<=cutoff',
      'prep=fit_preprocessing(window);bx=prepare(window,prep)',".filter(pl.col('is_train')",'model.n_iter_==96',"range(0,len(test),65536)",
      'native256(saved,block)','codec.predict_decoded(state,block)',"flags"]:
        if needle=='flags':continue
        assert needle in text,needle
    paths=[Path(__file__),diag,plan_path,source,A/'verify_nonflag_residual_HGB_codec2_20261007.py',A/'nonflag_residual_HGB_preprocessing_20261007.py',
      A/'nonflag_residual_HGB10_complete_training_source_preparation_20261007.json']
    pins={**proof['input_sha256'],**{str(p):sha(p) for p in paths}}
    create(A/'nonflag_residual_HGB10_source_admission_20261007.json',{'status':'passed_actual2_codec_controls_and10_mature_nonflag_fit_source_admission',
      'input_sha256':pins,'actual_diagnostic_fits':2,'prospective_selection_fits':10,'actual_official_scores':0,
      'all_original_labels_training_population_and_maturity_masks_required':True,'round120_complete_inference_and_scoring_pipeline_not_yet_admitted':True,'test_labels_read':False})
    print({'status':'admitted','diagnostic_fits':2,'prospective_selection_fits':10},flush=True)
if __name__=='__main__':main()
