"""Predeclare32 complete ordered185 receivers; the scientific base134 remains fixed."""
from pathlib import Path
import sys,time,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import adapt
import prepare_HuberCrossFamilyFine125_round146_sources_v3_20261008 as original
NAMES={'register_HuberCrossFamilyFine125_round146_artifacts_20261008.py': 'register_JointCrossHuberOrder185_round147_artifacts_20261008.py', 'publish_HuberCrossFamilyFine125_round146_full_validation_20261008.py': 'publish_JointCrossHuberOrder185_round147_full_validation_20261008.py', 'optimize_training_round146.py': 'optimize_training_round147.py', 'finalize_training_round146.py': 'finalize_training_round147.py', 'lossless_ranking_runtime_adapter_round146_v1_20261008.py': 'lossless_ranking_runtime_adapter_round147_v1_20261008.py', 'build_lossless_ranking_display_round146_v1_20261008.py': 'build_lossless_ranking_display_round147_v1_20261008.py', 'verify_lossless_ranking_display_round146_v1_20261008.py': 'verify_lossless_ranking_display_round147_v1_20261008.py', 'collect_full_lossless_round146_qa57_20261007.py': 'collect_full_lossless_round147_qa58_20261007.py'}
SOURCE_NAMES=['prepare_JointCrossHuber147_registry_and_phase_receivers_v1_20261008.py', 'prepare_JointCrossHuber147_core_receivers_v1_20261008.py', 'JointCrossHuber147_core_receiver_preparation_v1_20261008.json', 'JointCrossHuber147_candidate_status_contract_recovery_v2_20261008.json', 'JointCrossHuber147_registry_phase_preparation_v1_20261008.json', 'JointCrossHuberOrder185_round147_plan_v1_20261008.json', 'JointCrossHuberOrder185_round147_proposal_v1_20261008.json', 'JointCrossHuber147_storage_v1_20261008.py', 'verify_JointCrossHuber147_D_scoring_scope_v1_20261008.py', 'JointCrossHuber147_D_scoring_scope_v1_20261008.json', 'JointCrossHuber_ordered_CDF_v1_20261008.py', 'JointCrossHuber_ordered_native_stage_v1_20261008.py', 'predict_JointCrossHuber_complete_parent_scheme_v1_20261008.py', 'JointCrossHuber_complete_native_predictor_preparation_v1_20261008.json', 'run_JointCrossHuberOrder185_official_comparison_v1_20261008.py', 'prepare_JointCrossHuberOrder185_selected_candidate_v3_20261008.py', 'seal_JointCrossHuberOrder185_selected_candidate_v1_20261008.py', 'run_JointCrossHuberOrder185_round147_full_registration_v3_20261008.py', 'publish_JointCrossHuberOrder185_evidence_v2_20261008.py', 'verify_JointCrossHuberOrder185_round147_sources_v1_20261008.py', 'verify_JointCrossHuberOrder185_prospective_routes_v1_20261008.py', 'dispatch_JointCrossHuber147_complete_pipeline_v1_20261008.py', 'verify_JointCrossHuber181_synthetic_controls_v1_20261008.py', 'actual_JointCrossHuber181_synthetic_location_v1_20261008.json', 'prepare_JointCrossHuber35_reused_evidence_and_native80_v2_20261008.py', 'actual_JointCrossHuber35_existing_native_location_v1_20261008.json', 'recover_JointCrossHuber80_source_indentation_v3_20261008.py', 'JointCrossHuber80_factory3_final_print_failure_reconciled_v4_20261008.json', 'verify_JointCrossHuber80_native_historical_calendar_v2_20261008.py', 'verify_JointCrossHuber181_full_historical_controls_v1_20261008.py', 'actual_JointCrossHuber80_native_calendar_location_v2_20261008.json', 'actual_JointCrossHuber181_parent134_location_v1_20261008.json', 'JointCrossHuberOrder185_prospective_routes_v1_20261008.json', 'JointCrossHuberOrder185_actual_controls_index_v1_20261008.json', 'JointCrossHuberOrder185_round147_source_admission_v1_20261008.json', 'JointCrossHuberOrder185_round147_source_preparation_v1_20261008.json', 'JointCrossHuberOrder185_selected_release_v1_20261008/selected_candidate_ready_for_registration.json', 'JointCrossHuberOrder185_scores_github_v1_20261008/receipt.json', 'short_content_addressed_native_storage_v2_20261008.py', 'actual_short_parent_alias_nested_copy_v2_20261008.json', 'verified_TLS_Git_retry_runtime_v2_20261008.py', 'exact_native_JSON_archive_runtime_20261007.py', 'exact_native_pretty_JSON_archive_20261007.py', 'exact_native_JSON_archive_runtime_full_preflight_20261007/runtime_verification.json', 'publish_explicit_parent_training_round_v2_20261005.py', 'all_forecast_percentile_runtime_20261007.py', 'cached_official_spearman_runtime_20261007.py', 'resolve_sealed_scientific_protocol_v2_20261007.py', 'prepare_HuberCrossFamilyFine125_round146_sources_v3_20261008.py', 'HuberCrossFamilyFine146_storage_v1_20261008.py', 'verify_HuberCrossFamilyFine146_D_scoring_scope_v1_20261008.py', 'run_HuberCrossFamilyFine125_official_comparison_v2_20261008.py', 'prepare_HuberCrossFamilyFine125_selected_candidate_v2_20261008.py', 'seal_HuberCrossFamilyFine125_selected_candidate_v2_20261008.py', 'run_HuberCrossFamilyFine125_round146_full_registration_v3_20261008.py', 'publish_HuberCrossFamilyFine125_evidence_v3_20261008.py', 'verify_HuberCrossFamilyFine125_round146_sources_v3_20261008.py', 'verify_HuberCrossFamilyFine125_prospective_routes_v4_20261008.py', 'dispatch_HuberCrossFamilyFine146_complete_pipeline_v3_20261008.py', 'predict_HuberCrossFamilyFine_complete_parent_scheme_v1_20261008.py', 'verify_HuberCrossFamilyFine_multiyear_native_calendar_v1_20261008.py', 'prepare_HuberCrossFamilyFine146_complete_receivers_v1_20261008.py', 'HuberCrossFamilyFine_complete_parent_CDF_v1_20261008.py', 'HuberCrossFamilyFine_complete_parent_native_stage_v1_20261008.py', 'verify_HuberCrossFamilyFine30_native_historical_hooks_v1_20261008.py', 'verify_HuberCrossFamilyFine121_full_historical_controls_v1_20261008.py', 'prepare_HuberCrossFamilyFine146_historical_controls_v1_20261008.py', 'prepare_HuberCrossFamilyFine146_historical_controls_v2_20261008.py', 'recover_HuberCrossFamilyFine146_historical_factory_v2_20261008.py', 'prepare_CrossFamilyFine125_round145_sources_v2_20261008.py', 'prepare_CrossFamilyFine125_round145_sources_v1_20261008.py', 'prepare_CrossFamilyFine145_complete_receivers_v1_20261008.py', 'prepare_CrossFamily94_round136_sources_v4_20261008.py', 'prepare_BF16wide40_round135_sources_v4_20261008.py', 'prepare_HuberCrossFamilyFine125_round146_sources_v1_20261008.py', 'recover_HuberCrossFamilyFine146_three_head_registry_v2_20261008.py', 'verify_HuberCrossFamilyFine125_prospective_routes_v2_20261008.py', 'prepare_HuberCrossFamilyFine125_round146_sources_v2_20261008.py', 'recover_HuberCrossFamilyFine146_actual_admission_paths_v3_20261008.py']

def source_paths():return list(dict.fromkeys([Path(__file__),A/'recover_JointCrossHuber147_graph_key_preflight_v2_20261008.py',A/'JointCrossHuber147_graph_key_preflight_recovery_v2_20261008.json',*(A/n for n in SOURCE_NAMES),*(A/n for n in NAMES.values())]))
def generate(parent):
 assert parent in (139,141,145,146)
 result={adapt(n):adapt(s) for n,s in original.generate(139).items()}
 for n,s in result.items():
  s=s.replace('prepare_JointCrossHuberOrder185_round147_sources_v3_20261008','prepare_JointCrossHuberOrder185_round147_sources_v2_20261008')
  for stem in ('official_comparison','scores_main_publication','selected_candidate_preparation','selected_candidate_sealing'):
   s=s.replace('JointCrossHuberOrder185_'+stem+'_v2_20261008','JointCrossHuberOrder185_'+stem+'_v1_20261008')
  s=s.replace('passed_actual185_HuberCrossFamily_complete_parent_full_official_comparisons','passed_actual185_JointCrossHuber_complete_parent_full_official_comparisons')
  s=s.replace('_r139/',f'_r{parent}/').replace('PREVIOUS_NUMBER = 139',f'PREVIOUS_NUMBER = {parent}')
  s=s.replace("'explicit_parent_round': 139",f"'explicit_parent_round': {parent}").replace('explicit_comparison_parent_round=139',f'explicit_comparison_parent_round={parent}')
  s=s.replace('existing_HuberCrossFamily_saved_native_heads','existing_JointCrossHuber_saved_native_heads').replace("'existing_JointCrossHuber_saved_native_heads': 15","'existing_JointCrossHuber_saved_native_heads': 35")
  s=s.replace('actual15_HuberCrossFamily_saved_native_heads_source','actual35_JointCrossHuber_saved_native_heads_source')
  s=s.replace('HuberCrossFamily_complete_parent_native_replay_verification.json','JointCrossHuber_complete_parent_native_replay_verification.json')
  s=s.replace('all125_full_numeric','all185_full_numeric').replace('actual_all125_controls','actual_all185_controls')
  s=s.replace(':02d}_official.json',':03d}_official.json')
  if n.startswith('register_'):
   start=s.index("            assert 'nonflag_CPU_joint_Cross_Huber_ordered_complete_parent_CDF' not in graph");end=s.index('        row = ',start)
   s=s[:start]+"""            from JointCrossHuber_ordered_CDF_v1_20261008 import GRAPH_KEY,required
            assert GRAPH_KEY not in graph
            assert 'nonflag_CPU_CrossFamily_complete_parent_CDF' not in graph and 'nonflag_CPU_HuberCrossFamily_complete_parent_CDF' not in graph
            assert measured['ordered_native_components']==required(cfg['configuration'])
            if cfg['weight']==0.:
                assert measured['ordered_native_components']==[] and all(cfg['configuration'][h]['amplitude']==0. for h in ('cross','huber'))
            else:
                assert measured['first2020_identity'] and len(measured['ordered_native_components']) in (3,4,7)
                graph[GRAPH_KEY]={**cfg,'configuration':cfg['configuration'],'total_absolute_amplitude':cfg['weight'],
                    'universe':cfg['universe'],'first2020_identity':True,'position':'ordered_composite_after_complete_qualified134_parent',
                    'teacher_feature':'qualified106_current_forecast_average_rank_over_N',
                    'ordered_native_component_heads':measured['ordered_native_components'],'actual_annual_native_bank':measured['native_bank_source'],
                    'original_complete_parent_round':134,'original_complete_parent_graph_preserved':True,
                    'transformation':'explicit_order_two_current_all_universe_inverseCDF_stages_each_with_its_original_saved_residual_heads',
                    'future_candidate_not_inferred_for_nonselected_comparison':True}
"""+s[end:]
  if n.startswith('publish_'):
   s=s.replace('136、139、141、145','139、141、145、146').replace('120项新细权重及零幅度对照','181项两类后处理的幅度、比例和顺序联合对照')
   s=s.replace('重调固定136完整父方案后的原跨模型阶段','在固定134完整父方案后按明确顺序执行两个阶段')
   s=s.replace('复用15个成熟年度原生模型；121完整/363冷前缀及30原生/30冷检查','复用35个成熟年度原生模型；181完整/543冷前缀及80原生/80冷检查')
  compile(s,str(A/n),'exec');result[n]=s
 assert len(result)==8;return result
def main():
 ready_path=A/'JointCrossHuberOrder185_selected_release_v1_20261008/selected_candidate_ready_for_registration.json';ready=read(ready_path)
 assert ready['status']=='passed_actual185_selected_candidate_full_graph_and_metrics_and_source_bytes' and ready['sealed_candidate_complete']
 pilot=read(A/'JointCrossHuberOrder185_official_comparison_v1_20261008/verification.json');assert len(pilot['records'])==185 and pilot['best']==ready['best']
 admission=A/'JointCrossHuberOrder185_round147_source_admission_v1_20261008.json';proof=read(admission)
 assert proof['status']=='passed_actual35_states181full543cold80native_and32_prospective147_sources'
 for p,d in proof['input_sha256'].items():assert sha(p)==d,p
 generated=generate(pilot['actual_comparison_parent_round']);expected=proof['generated_source_sha256'][str(pilot['actual_comparison_parent_round'])]
 assert set(generated)==set(expected)
 for n,s in generated.items():assert not (A/n).exists() and hashlib.sha256(s.encode()).hexdigest()==expected[n],n
 for n,s in generated.items():(A/n).write_text(s,encoding='utf8',newline='\n')
 create(A/'JointCrossHuberOrder185_round147_source_preparation_v1_20261008.json',{'status':'passed_actual185_sealed_candidate_and_admitted_full147_QA58_sources',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'round':147,'scored_records':185,'actual_comparison_parent_round':pilot['actual_comparison_parent_round'],
  'input_sha256':{str(p):sha(p) for p in [Path(__file__),ready_path,admission,*(A/n for n in generated)]},'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
if __name__=='__main__':main()
