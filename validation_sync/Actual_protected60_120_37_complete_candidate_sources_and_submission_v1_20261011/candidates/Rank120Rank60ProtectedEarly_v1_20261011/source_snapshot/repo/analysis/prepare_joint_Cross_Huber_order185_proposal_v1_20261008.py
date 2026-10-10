"""Freeze an uncovered joint amplitude/share/order grid; no185 quality or native controls claimed."""
from pathlib import Path
import sys,time,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
 sources=[Path(__file__),A/'CrossFamilyFine125_round145_proposal_v1_20261008.json',A/'HuberCrossFamilyFine125_round146_proposal_v1_20261008.json',
  A/'optimization_20261003_r134/full_registration_execution.json',A/'optimization_20261003_r136/full_registration_execution.json',
  A/'optimization_20261003_r139/full_registration_execution.json',A/'HuberCrossFamily112_official_comparison_v1_20261008/verification.json',
  A/'CrossFamilyFine_complete_parent_CDF_v1_20261008.py',A/'HuberCrossFamilyFine_complete_parent_CDF_v1_20261008.py',ROOT/'evaluate.py',ROOT/'后续选模标准.md']
 cross=read(sources[1]);huber=read(sources[2]);assert cross['scientific_stage_base_round']==134 and huber['scientific_stage_base_round']==136
 for p in sources[3:6]:assert read(p)['status']=='passed'
 winner=read(sources[6])['best'];assert winner['configuration']['group']==4 and winner['configuration']['share']==.5 and winner['configuration']['weight']==.0025
 options=[{'group':4,'share':s,'amplitude':w} for s in (.375,.5,.625) for w in (.001,.0025,.00325)]
 zero={'group':4,'share':.5,'amplitude':0.}
 cases=[{'order':['cross','huber'],'cross':zero,'huber':zero}]
 cases.extend({'order':['cross','huber'],'cross':c,'huber':zero} for c in options)
 cases.extend({'order':['cross','huber'],'cross':zero,'huber':h} for h in options)
 cases.extend({'order':order,'cross':c,'huber':h} for order in (['cross','huber'],['huber','cross']) for c in options for h in options)
 assert len(cases)==181 and len({json.dumps(c,sort_keys=True) for c in cases})==181
 heads={**cross['heads'],**huber['heads']};assert len(heads)==7
 graph=read(ROOT/'candidates/optimization_20261003_r134/verification.json')['whole_scheme_graph']
 assert 'nonflag_CPU_CrossFamily_complete_parent_CDF' not in graph and 'nonflag_CPU_HuberCrossFamily_complete_parent_CDF' not in graph
 p=A/'JointCrossHuberOrder185_round147_proposal_v1_20261008.json'
 create(p,{'status':'frozen_bounded_uncovered_joint_order_proposal_not_admitted_not_scored_not_dispatched',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'target_round':147,'deadline_local':'2026-10-10T23:59:00+08:00',
  'scientific_stage_base_round':134,'anchor_rounds':[139,141,145,146],'expected_official_cases':185,'new_case_count':181,'new_cases':cases,'heads':heads,
  'graph_key':'nonflag_CPU_joint_Cross_Huber_ordered_complete_parent_CDF',
  'operation':'append_one_explicit_two_stage_composite_over_the_entire_qualified134_graph_with_all_existing_branches_retained',
  'evidence':{'fully_qualified136_score':read(A/'optimization_20261003_r136/calibrated_csv_official.json')['metrics']['final_score'],
   'fully_qualified139_score':read(A/'optimization_20261003_r139/calibrated_csv_official.json')['metrics']['final_score'],
   'separate145_and146_scans_do_not_cover_joint_amplitudes_or_swapped_order':True,
   'single_stage_positive_polarity_is_supported_by_actual136_and139_winners':True},
  'previous_exact134_136_139_configurations_are_explicit_identity_reproduction_controls_not_new_model_fits':True,
  'existing_native_heads':35,'full_OOF_heads':7,'new_native_fits_needed':0,
  'required_before_quality':['actual145_and146_full_qualification_and_main_receipts',
   'complete147_scoring_registry_inference_and_original_full_QA_receivers_frozen_and_prospectively_verified',
   'actual181_full_two_stage_independent_native_and_Pandas_controls_and543_cold_prefix_controls',
   'own_cross_and_huber_saved_state_maturity_yearly_native_reload_and_independent_controls_in_both_orders',
   'exact134_136_139_prediction_and_all8_official_metric_controls',
   'zero_stage_identity_and_physical_SHA_union_count_controls',
   'prospective_actual2025_final_models_on_multiyear_dates_and_prefit_date_rejection',
   'all_original_official_scoring_and_train_only_mature_return_mapping_gates'],
  'required_after_selection':['freeze_selected_order_parameters_native_sources_and_return_mapping_before_future_X',
   'two_full1599600_native_and_independent_replays_reload_CSV_and_cold80_or_truthful_qualified_anchor_reuse',
   'all_original_full_board_six_view_browser_QA_and_actual_main_publication'],
  'final_selection_rule':'official_S_desc_unique_physical_model_SHA_count_asc_sum_absolute_amplitudes_asc_case_asc',
  'all_transform_percentiles_use_entire_current_raw_forecast_universe':True,
  'both_stages_use_original_qualified106_teacher_feature_and_own_mature_saved_models':True,
  'first2020_flag1_and_invalid_training_forecast_bits_preserved':True,
  'training_grid_selection_bias_uncorrected_and_no_blind_test_quality_claimed':True,
  'new_official_scores':0,'new_future_inference':0,'test_labels_read':False,
  'global_search_or_resource_exhaustion_claimed':False,'source_receivers_not_yet_prepared':True,
  'input_sha256':{str(f):sha(f) for f in sources}})
 print('Prepared185-case joint two-stage and order proposal with7 existing annual native heads; no quality/inference executed.',flush=True)
if __name__=='__main__':main()
