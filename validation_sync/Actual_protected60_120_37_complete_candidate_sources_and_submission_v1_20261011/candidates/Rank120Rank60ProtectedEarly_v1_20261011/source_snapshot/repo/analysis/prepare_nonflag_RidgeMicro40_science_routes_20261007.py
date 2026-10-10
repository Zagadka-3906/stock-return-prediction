"""Freeze twelve new small amplitudes and all prospective131 routes before scoring."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from nonflag_RidgeMicro40_round131_mapping_20261007 import convert

def main():
    names=[
      'run_nonflag_RidgeFine52_official_comparison_v1_20261007.py','run_nonflag_RidgeFine52_admitted_comparison_v1_20261007.py',
      'prepare_nonflag_RidgeFine52_selected_candidate_v1_20261007.py','seal_nonflag_RidgeFine52_selected_candidate_v1_20261007.py',
      'publish_nonflag_RidgeFine52_evidence_v1_20261007.py','run_nonflag_RidgeFine52_round128_full_registration_v1_20261007.py',
      'verify_nonflag_RidgeFine52_round128_sources_v1_20261007.py','verify_nonflag_residual_RidgeFine49_transform_20261007.py',
      'predict_nonflag_residual_RidgeFine_complete_scheme_20261007.py','nonflag_residual_RidgeFine_compatible_parent_20261007.py',
      'verify_nonflag_RidgeFine52_prospective_routes_v2_20261007.py']
    pins=[Path(__file__),A/'nonflag_RidgeMicro40_round131_mapping_20261007.py',A/'prepare_nonflag_RidgeMicro40_round131_sources_v1_20261007.py']
    for name in names:
        old=A/name;new=A/convert(name);text=convert(old.read_text(encoding='utf8'))
        for before in ['prepare_nonflag_RidgeMicro40_admission_and_publication_20261007.py','finalize_nonflag_RidgeMicro40_pre_admission_routes_20261007.py']:
            text=text.replace(before,Path(__file__).name)
        for before in ['nonflag_RidgeMicro40_science_route_preparation_20261007.json','nonflag_RidgeMicro40_science_route_preparation_v2_20261007.json','nonflag_RidgeMicro40_science_route_preparation_v3_20261007.json']:
            text=text.replace(before,'nonflag_RidgeMicro40_science_route_preparation_v1_20261007.json')
        if name.startswith('verify_nonflag_RidgeFine52_prospective'):
            marker='    graph_controls=[];generated_hashes={};path_controls=[];issues=[]'
            assert text.count(marker)==1
            text=text.replace(marker,"    future |= {A/f'github_validation_sync_main_20261005/round{n}_receipt.json' for n in (129,130)}\n"+marker)
        if name.startswith('verify_nonflag_RidgeFine52'):
            text=text.replace("'nonflag_CPU_HGB_residual_CDF':{'old':'remove'}", "'nonflag_CPU_HGB_residual_CDF':{'old':'remove'},'nonflag_CPU_EmpiricalBayes64_residual_CDF':{'old_Bayes':'remove'}")
            text=text.replace("'nonflag_CPU_HGB_residual_CDF':{'old_branch':'must_be_removed'}", "'nonflag_CPU_HGB_residual_CDF':{'old_branch':'must_be_removed'},'nonflag_CPU_EmpiricalBayes64_residual_CDF':{'old_Bayes':'remove'}")
            text=text.replace("assert 'nonflag_CPU_HGB_residual_CDF' not in graph and", "assert 'nonflag_CPU_EmpiricalBayes64_residual_CDF' not in graph and 'nonflag_CPU_HGB_residual_CDF' not in graph and")
            text=text.replace("('nonflag_CPU_HGB_residual_CDF','nonflag_CPU_RFFRidge_residual_CDF'", "('nonflag_CPU_EmpiricalBayes64_residual_CDF','nonflag_CPU_HGB_residual_CDF','nonflag_CPU_RFFRidge_residual_CDF'")
        compile(text,str(new),'exec');assert not new.exists(),new;new.write_text(text,encoding='utf8',newline='\n');pins.extend((old,new))
    oldplan=read(A/'nonflag_RidgeFine52_plan_20261007.json');original=read(A/'nonflag_Ridge40_plan_20261007.json')
    weights=[.0019,.001925,.00195,.001975,.00199,.00201,.002025,.00205,.002075,.0021,.00215,.0022]
    prior=set(oldplan['weights'])|set(original['weights']);assert not prior.intersection(weights) and len(weights)==12
    bank=A/'nonflag_residual_Ridge_bank10_20261007/verification.json';native=A/'nonflag_residual_Ridge_native_hook3_preflight_20261007/verification.json'
    plan={
      'status':'frozen_micro40_new_weights_before_actual_controls_and_official_scores','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
      'round':131,'wave':414,'after_round':130,'qualified_anchor_rounds':[112,129,130],
      'single_native_heads':oldplan['single_native_heads'],'ensembles':oldplan['ensembles'],'weights':weights,
      'universe':'all_current_raw_forecasts','existing_native_bank':'nonflag_residual_Ridge_bank10_20261007',
      'expected_scored_records':40,'expected_full_transform_controls':37,'expected_cold_prefix_controls':111,
      'teacher_round':106,'preserve_complete_parent_flag_and2020_raw_bits':True,'new_branch':'nonflag_CPU_Ridge_residual_CDF',
      'new_native_fits_by_comparison':0,'native_bank_and_existing_hook3_proofs_reused_without_new_inference_claims':True,
      'micro_weights_all_disjoint_from_previous40_and52_grids':True,'refinement_basis_actual128_case29_score_only':.45111336969856725,
      'selection':'highest_full_connected_official_score_after_actual130_main_closure_and_actual131_admission',
      'full_future_candidate_native_replays_and_QA42_required':True,'selection_bias_uncorrected':True,
      'global_resource_exhaustion_established':False,'test_labels_read':False,
      'input_sha256':{str(p):sha(p) for p in [Path(__file__),bank,native,A/'nonflag_RidgeFine52_official_comparison_v1_20261007/verification.json']}}
    path=A/'nonflag_RidgeMicro40_plan_20261007.json';create(path,plan);pins.append(path)
    create(A/'nonflag_RidgeMicro40_science_route_preparation_v1_20261007.json',{
      'status':'compiled_fresh_micro40_complete131_QA42_routes_before_quality_scores','input_sha256':{str(p):sha(p) for p in pins},
      'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    from verify_nonflag_RidgeMicro40_prospective_routes_v2_20261007 import main as prospective
    prospective()

if __name__=='__main__':main()
