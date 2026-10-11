"""Prepare new73 controls and all76 full129 routes before source admission or official scoring."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from nonflag_RFF128StreamMid129_route_mapping_20261007 import convert

def main():
    names=['run_nonflag_RFF128Hi76_official_comparison_v1_20261007.py',
      'prepare_nonflag_RFF128Hi76_selected_candidate_v1_20261007.py','seal_nonflag_RFF128Hi76_selected_candidate_v1_20261007.py',
      'run_nonflag_RFF128Hi76_admitted_comparison_v1_20261007.py','run_nonflag_RFF128Hi76_round127_full_registration_v1_20261007.py',
      'publish_nonflag_RFF128Hi76_evidence_v1_20261007.py','verify_nonflag_RFF128Hi76_round127_sources_v1_20261007.py',
      'verify_nonflag_RFF128Hi76_prospective_routes_v2_20261007.py','predict_nonflag_residual_RFF128Hi_complete_scheme_20261007.py',
      'run_nonflag_residual_RFF128Hi_hook6_after_bank_20261007.py','verify_nonflag_residual_RFF128Hi73_transform_20261007.py',
      'run_nonflag_RFF128Hi_actual_controls_20261007.py']
    paths=[Path(__file__),A/'nonflag_RFF128StreamMid129_route_mapping_20261007.py',
      A/'prepare_nonflag_RFF128StreamMid76_round129_sources_v1_20261007.py',
      A/'nonflag_RFF128_streamed_gram_fitter_20261007.py']
    for name in names:
        old=A/name;new=A/convert(name);assert not new.exists(),new
        text=convert(old.read_text(encoding='utf8'))
        if name.startswith('publish_'):
            text=text.replace('nonflag_RFF128StreamMid76_science_route_preparation_v2_20261007.json',
                              'nonflag_RFF128StreamMid76_science_route_preparation_v1_20261007.json')
            text=text.replace('frozen_fresh_RFF128Hi','frozen_fresh_RFF128StreamMid')
            text=text.replace("A/'actual_user_resume_until2355_20261007.json',",
                              "A/'actual_user_resume_until2355_20261007.json',A/'nonflag_RFF128_streamed_gram_fitter_20261007.py',")
        compile(text,str(new),'exec');new.write_text(text,encoding='utf8',newline='\n');paths.extend((old,new))
    plan=read(A/'nonflag_RFF128Hi76_plan_20261007.json');heads=list(read(A/'nonflag_residual_RFF128StreamMid10_plan_20261007.json')['configurations'])
    plan.update(status='frozen_new_streamed128_mid_gamma76_before_controls_and_official_scores',
      at_local=time.strftime('%Y-%m-%dT%H:%M:%S'),round=129,wave=412,after_round=128,qualified_anchor_rounds=[112,127,128],
      single_native_heads=heads,ensembles={'nonflag_residual_rff128streammid_equal_mean_two':heads},
      existing_native_bank='nonflag_residual_RFF128StreamMid_bank10_20261007',
      selection='highest_full_connected_official_score_after_actual128_closure_and_actual129_source_admission',
      training_solver_recipe='fixed8192_padded_RBF128_centered_float64_Gram_cholesky_v1',
      full_future_candidate_native_replays_and_QA40_required=True)
    plan.pop('full_future_candidate_native_replays_and_QA38_required',None)
    plan_path=A/'nonflag_RFF128StreamMid76_plan_20261007.json';create(plan_path,plan);paths.append(plan_path)
    # Preserves documented ancestry while freezing the new numerical training source explicitly.
    create(A/'nonflag_RFF128StreamMid76_science_route_preparation_v1_20261007.json',{
      'status':'compiled_new_streamed128_mid_gamma_complete129_QA40_routes_before_official_scores',
      'input_sha256':{str(p):sha(p) for p in paths},'new_quality_scores':0,'test_labels_read':False})
    from verify_nonflag_RFF128StreamMid76_prospective_routes_v2_20261007 import main as prospective
    prospective()
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    pins={str(p):sha(p) for p in paths}
    row=start('nonflag_RFF128StreamMid_actual_hook6_and_full73_controls','run_nonflag_RFF128StreamMid_actual_controls_20261007.py',[],pins)
    create(A/'nonflag_RFF128StreamMid_actual_controls_hidden_launch_20261007.json',{
      'status':'started_actual6_native_hooks73_full219_cold_controls_after_native_bank',
      'identity':row,'input_sha256':pins,'new_quality_scores':0,'test_labels_read':False})

if __name__=='__main__':main()
