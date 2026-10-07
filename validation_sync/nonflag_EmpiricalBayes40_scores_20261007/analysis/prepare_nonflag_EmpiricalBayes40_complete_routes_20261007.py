"""Prepare true37/111 controls and complete40-record future130 routes for new Bayes models."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from nonflag_EmpiricalBayes40_round130_mapping_20261007 import convert

def main():
    pairs={name:convert(name) for name in [
      'run_nonflag_RidgeFine52_official_comparison_v1_20261007.py','run_nonflag_RidgeFine52_admitted_comparison_v1_20261007.py',
      'prepare_nonflag_RidgeFine52_selected_candidate_v1_20261007.py','seal_nonflag_RidgeFine52_selected_candidate_v1_20261007.py',
      'publish_nonflag_RidgeFine52_evidence_v1_20261007.py','run_nonflag_RidgeFine52_round128_full_registration_v1_20261007.py',
      'verify_nonflag_RidgeFine52_round128_sources_v1_20261007.py','verify_nonflag_residual_RidgeFine49_transform_20261007.py',
      'predict_nonflag_residual_RidgeFine_complete_scheme_20261007.py','nonflag_residual_RidgeFine_compatible_parent_20261007.py',
      'nonflag_residual_Ridge_native_stage_20261007.py','run_nonflag_residual_Ridge_hook3_after_bank_20261007.py',
      'verify_nonflag_RidgeFine52_prospective_routes_v2_20261007.py']}
    sources=[Path(__file__),A/'nonflag_EmpiricalBayes40_round130_mapping_20261007.py',
      A/'prepare_nonflag_EmpiricalBayes40_round130_sources_v1_20261007.py',A/'nonflag_empirical_Bayes64_codec_20261007.py']
    for before,after in pairs.items():
        old=A/before;new=A/after;assert not new.exists(),new
        text=convert(old.read_text(encoding='utf8'))
        if before.startswith('nonflag_residual_RidgeFine_compatible'):
            text=text.replace("    value.pop('nonflag_CPU_EmpiricalBayes64_residual_CDF',None)",
              "    value.pop('nonflag_CPU_EmpiricalBayes64_residual_CDF',None)\n    value.pop('nonflag_CPU_Ridge_residual_CDF',None)")
        if before.startswith('verify_nonflag_RidgeFine52_round'):
            text=text.replace("'nonflag_CPU_HGB_residual_CDF':{'old_branch':'must_be_removed'}",
              "'nonflag_CPU_HGB_residual_CDF':{'old_branch':'must_be_removed'},'nonflag_CPU_Ridge_residual_CDF':{'old_Ridge':'remove'}")
            text=text.replace("assert 'nonflag_CPU_HGB_residual_CDF' not in graph and",
              "assert 'nonflag_CPU_HGB_residual_CDF' not in graph and 'nonflag_CPU_Ridge_residual_CDF' not in graph and")
        if before.startswith('verify_nonflag_RidgeFine52_prospective'):
            text=text.replace("'nonflag_CPU_HGB_residual_CDF':{'old':'remove'}",
              "'nonflag_CPU_HGB_residual_CDF':{'old':'remove'},'nonflag_CPU_Ridge_residual_CDF':{'old_Ridge':'remove'}")
            text=text.replace("'nonflag_CPU_HGB_residual_CDF','nonflag_CPU_RFFRidge_residual_CDF'",
              "'nonflag_CPU_HGB_residual_CDF','nonflag_CPU_Ridge_residual_CDF','nonflag_CPU_RFFRidge_residual_CDF'")
            # The numeric native and control proofs are required to exist by actual source admission.
            marker="    graph_controls=[];generated_hashes={};path_controls=[];issues=[]"
            assert text.count(marker)==1
            text=text.replace(marker,"    future |= {A/'nonflag_residual_EmpiricalBayes64_bank10_20261007/verification.json',A/'nonflag_residual_EmpiricalBayes64_native_hook3_preflight_20261007/verification.json',A/'github_validation_sync_main_20261005/round129_receipt.json'}\n"+marker)
        if before.startswith('publish_'):
            text=text.replace("A/'prepare_nonflag_EmpiricalBayes40_science_routes_20261007.py'","A/'prepare_nonflag_EmpiricalBayes40_complete_routes_20261007.py'")
            text=text.replace("A/'finalize_nonflag_EmpiricalBayes40_pre_admission_routes_20261007.py'","A/'prepare_nonflag_EmpiricalBayes40_complete_routes_20261007.py'")
            text=text.replace('nonflag_EmpiricalBayes40_science_route_preparation_v2_20261007.json','nonflag_EmpiricalBayes40_science_route_preparation_v1_20261007.json')
            text=text.replace('nonflag_EmpiricalBayes40_science_route_preparation_v3_20261007.json','nonflag_EmpiricalBayes40_science_route_preparation_v1_20261007.json')
            text=text.replace('nonflag_EmpiricalBayes40_science_route_preparation_20261007.json','nonflag_EmpiricalBayes40_science_route_preparation_v1_20261007.json')
        if before.startswith('verify_nonflag_RidgeFine52_round'):
            text=text.replace('nonflag_EmpiricalBayes40_science_route_preparation_v3_20261007.json','nonflag_EmpiricalBayes40_science_route_preparation_v1_20261007.json')
        compile(text,str(new),'exec');new.write_text(text,encoding='utf8',newline='\n');sources.extend((old,new))
    plan=read(A/'nonflag_RidgeFine52_plan_20261007.json');heads=list(read(A/'nonflag_residual_EmpiricalBayes6410_plan_20261007.json')['configurations'])
    original=read(A/'nonflag_Ridge40_plan_20261007.json')
    plan.update(status='frozen_empirical_Bayes40_before_actual_controls_or_official_scoring',
      at_local=time.strftime('%Y-%m-%dT%H:%M:%S'),round=130,wave=413,after_round=129,qualified_anchor_rounds=[112,128,129],
      single_native_heads=heads,ensembles={'nonflag_residual_empirical_bayes64_equal_mean_two':heads},weights=original['weights'],
      existing_native_bank='nonflag_residual_EmpiricalBayes64_bank10_20261007',expected_scored_records=40,
      expected_full_transform_controls=37,expected_cold_prefix_controls=111,new_branch='nonflag_CPU_EmpiricalBayes64_residual_CDF',
      selection='highest_full_connected_official_score_after_actual129_closure_and_actual130_source_admission',
      full_future_candidate_native_replays_and_QA41_required=True,
      training_solver_recipe='fixed8192_centered_Gram64_empirical_Bayes_scalar_or_diagonal_v1')
    plan.pop('full_future_candidate_native_replays_and_QA39_required',None)
    path=A/'nonflag_EmpiricalBayes40_plan_20261007.json';create(path,plan);sources.append(path)
    create(A/'nonflag_EmpiricalBayes40_science_route_preparation_v1_20261007.json',{
      'status':'compiled_new_empirical_Bayes40_complete130_QA41_science_routes',
      'input_sha256':{str(p):sha(p) for p in sources},'new_quality_scores':0,'test_labels_read':False})
    from verify_nonflag_EmpiricalBayes40_prospective_routes_v2_20261007 import main as prospective
    prospective()

if __name__=='__main__':main()
