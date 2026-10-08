"""Complete146 deterministic registry routes; comparisons vary, scientific stage base136 stays fixed."""
from pathlib import Path
import hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_HuberCrossFamilyFine146_complete_receivers_v1_20261008 import convert
import prepare_CrossFamilyFine125_round145_sources_v2_20261008 as original
NAMES={old:convert(new) for old,new in original.NAMES.items()}
SOURCE_NAMES=['HuberCrossFamilyFine146_storage_v1_20261008.py', 'verify_HuberCrossFamilyFine146_D_scoring_scope_v1_20261008.py', 'run_HuberCrossFamilyFine125_official_comparison_v1_20261008.py', 'prepare_HuberCrossFamilyFine125_selected_candidate_v1_20261008.py', 'seal_HuberCrossFamilyFine125_selected_candidate_v1_20261008.py', 'run_HuberCrossFamilyFine125_round146_full_registration_v1_20261008.py', 'publish_HuberCrossFamilyFine125_evidence_v1_20261008.py', 'verify_HuberCrossFamilyFine125_round146_sources_v1_20261008.py', 'verify_HuberCrossFamilyFine125_prospective_routes_v1_20261008.py', 'dispatch_HuberCrossFamilyFine146_complete_pipeline_v1_20261008.py', 'predict_HuberCrossFamilyFine_complete_parent_scheme_v1_20261008.py', 'verify_HuberCrossFamilyFine_multiyear_native_calendar_v1_20261008.py', 'prepare_HuberCrossFamilyFine146_complete_receivers_v1_20261008.py', 'HuberCrossFamilyFine146_complete_receiver_preparation_v1_20261008.json', 'HuberCrossFamilyFine125_round146_plan_v2_20261008.json', 'HuberCrossFamilyFine125_round146_proposal_v1_20261008.json', 'HuberCrossFamilyFine_complete_parent_CDF_v1_20261008.py', 'HuberCrossFamilyFine_complete_parent_native_stage_v1_20261008.py', 'verify_HuberCrossFamilyFine30_native_historical_hooks_v1_20261008.py', 'verify_HuberCrossFamilyFine121_full_historical_controls_v1_20261008.py', 'actual_HuberCrossFamilyFine_bank15_location_v1_20261008.json', 'actual_HuberCrossFamilyFine30_native_hooks_location_v1_20261008.json', 'actual_HuberCrossFamilyFine121_parent136_location_v1_20261008.json', 'actual_HuberCrossFamilyFine_multiyear_calendar_location_v1_20261008.json', 'HuberCrossFamilyFine146_D_scoring_scope_v1_20261008.json', 'HuberCrossFamilyFine125_prospective_routes_v1_20261008.json', 'HuberCrossFamilyFine125_actual_controls_index_v1_20261008.json', 'HuberCrossFamilyFine125_round146_source_admission_v1_20261008.json', 'HuberCrossFamilyFine125_round146_source_preparation_v1_20261008.json', 'HuberCrossFamilyFine125_selected_release_v1_20261008/selected_candidate_ready_for_registration.json', 'HuberCrossFamilyFine125_scores_github_v1_20261008/receipt.json', 'prepare_HuberCrossFamilyFine146_historical_controls_v1_20261008.py', 'prepare_HuberCrossFamilyFine146_historical_controls_v2_20261008.py', 'recover_HuberCrossFamilyFine146_historical_factory_v2_20261008.py', 'HuberCrossFamilyFine146_first_factory_failure_v1_20261008.json', 'HuberCrossFamilyFine146_historical_receiver_preparation_v1_20261008.json', 'prepare_CrossFamilyFine125_round145_sources_v2_20261008.py', 'prepare_CrossFamilyFine125_round145_sources_v1_20261008.py', 'prepare_CrossFamilyFine145_complete_receivers_v1_20261008.py', 'prepare_CrossFamily94_round136_sources_v4_20261008.py', 'prepare_BF16wide40_round135_sources_v4_20261008.py', 'short_content_addressed_native_storage_v2_20261008.py', 'actual_short_parent_alias_nested_copy_v2_20261008.json', 'verified_TLS_Git_retry_runtime_v2_20261008.py', 'exact_native_JSON_archive_runtime_20261007.py', 'exact_native_pretty_JSON_archive_20261007.py', 'exact_native_JSON_archive_runtime_full_preflight_20261007/runtime_verification.json', 'publish_explicit_parent_training_round_v2_20261005.py', 'all_forecast_percentile_runtime_20261007.py', 'cached_official_spearman_runtime_20261007.py', 'resolve_sealed_scientific_protocol_v2_20261007.py']
def source_paths():
    return list(dict.fromkeys([Path(__file__),*(A/n for n in SOURCE_NAMES),*(A/n for n in NAMES.values())]))
def generate(parent):
    assert parent in (136,139,141,145)
    result={convert(n):convert(s) for n,s in original.generate(134).items()}
    for n,s in result.items():
        s=s.replace('_r136/',f'_r{parent}/').replace('PREVIOUS_NUMBER = 136',f'PREVIOUS_NUMBER = {parent}')
        s=s.replace("'explicit_parent_round': 136",f"'explicit_parent_round': {parent}").replace('explicit_comparison_parent_round=136',f'explicit_comparison_parent_round={parent}')
        compile(s,str(A/n),'exec');result[n]=s
    assert len(result)==8;return result
def main():
    ready_path=A/'HuberCrossFamilyFine125_selected_release_v1_20261008/selected_candidate_ready_for_registration.json';ready=read(ready_path)
    assert ready['status']=='passed_actual125_selected_candidate_full_graph_and_metrics_and_source_bytes' and ready['sealed_candidate_complete']
    pilot=read(A/'HuberCrossFamilyFine125_official_comparison_v1_20261008/verification.json');assert len(pilot['records'])==125 and pilot['best']==ready['best']
    admission=A/'HuberCrossFamilyFine125_round146_source_admission_v1_20261008.json';proof=read(admission)
    assert proof['status']=='passed_actual15_heads121_fixed_base_CDF363cold30hooks_and32_prospective146_sources'
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    generated=generate(pilot['actual_comparison_parent_round']);expected=proof['generated_source_sha256'][str(pilot['actual_comparison_parent_round'])]
    assert set(generated)==set(expected)
    for n,s in generated.items():assert not (A/n).exists() and hashlib.sha256(s.encode()).hexdigest()==expected[n],n
    for n,s in generated.items():(A/n).write_text(s,encoding='utf8',newline='\n')
    create(A/'HuberCrossFamilyFine125_round146_source_preparation_v1_20261008.json',{'status':'passed_actual125_sealed_candidate_and_admitted_full146_QA57_sources',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'round':146,'scored_records':125,'actual_comparison_parent_round':pilot['actual_comparison_parent_round'],
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),ready_path,admission,*(A/n for n in generated)]},'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
if __name__=='__main__':main()
