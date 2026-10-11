"""Record real frontier movement and current handles without claiming exhaustion."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def main():
 services=A/'service_owned_workflows_20261006'
 names=['PureRFFHuber80_native_historical_calendar_controls_v4_20261009',
  'PureRFFHuber124_actual_full_historical_controls_v4_20261009','Pure149_prior_complete_forecast_duplicate_audit_v3_20261009',
  'PureRFFHuber20_year2023_native_supplement_v1_20261009','PureRFFHuber25_all5_annual_native_coverage_v1_20261009',
  'PureRFFHuber149_complete_chronological_dispatch_v7_20261009',
  'SparseAfter14860_native_historical_calendar_controls_v1_20261009','SparseAfter14825_full_historical_controls_v1_20261009',
  'actual149_all5_and152_historical_main_publication_v52_20261009',
  'HuberSparse150_complete_chronological_dispatch_v3_20261009','RFFSparse151_complete_chronological_dispatch_v2_20261009',
  'actual_chronological_optimization_progress_observer_v52_20261009','main_publisher_v9_20261009']
 actual={}
 for n in names:
  launch=read(services/n/'native_launch.json');p=services/n/'service_execution.json'
  if p.exists():actual[n]={'execution':read(p),'identity':launch}
  else:assert owned(launch),n;actual[n]={'currently_owned':True,'identity':launch}
 full_service='AdaptiveJointCrossHuber242_round148_full_registration_v2_20261009'
 f=services/full_service;p=f/'service_execution.json';launch=read(f/'native_launch.json')
 if p.exists():actual[full_service]={'execution':read(p),'identity':launch}
 else:assert owned(launch);actual[full_service]={'currently_owned':True,'identity':launch}
 full=A/'optimization_20261003_r148/full_registration_execution.json'
 receipt=A/'github_validation_sync_main_20261005/round148_receipt.json'
 qualified148=full.exists() and receipt.exists() and read(full)['status']=='passed' and read(receipt)['status']=='pushed_and_remote_head_verified'
 best={'round':148,'score':0.4511917507998099,'main_commit':read(receipt)['commit']} if qualified148 else {
  'round':147,'score':0.4511896739186047,'main_commit':'1d5d0bffbafc468c9a7e928034ac6cffc8fee9d7'}
 sources=[Path(__file__),A/'Pure149_all5_annual_native_receiver_binding_v8_20261009.json',
  A/'SparseAfter14829_round152_proposal_v1_20261009.json',A/'SparseAfter14829_synthetic25_and_state10_metadata_v1_20261009.json',
  A/'SparseAfter148152_historical_receiver_preparation_v1_20261009.json',A/'SparseAfter148152_complete_native_predictor_preparation_v1_20261009.json',
  A/'actual148149_recovery_main_v51_receipt_20261009.json']
 for proof in sources[1:-1]:
  for path,digest in read(proof)['input_sha256'].items():assert sha(path)==digest,path
 create(A/'actual_optimization_checkpoint_v52_20261009.json',{
  'status':'active149_missing2023_native_binding_and_new152_sparse_after_complete148_frontier',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'previous_goal_turn_classification':'progress_actual148_complete_scoring_inference_sealing_and_main_recovery_evidence',
  'input_sha256':{str(p):sha(p) for p in sources},'best_fully_qualified':best,
  'actual148_candidate_two_full_native_reload_independent_CSV_and_cold80_and_sealing_passed':True,
  'actual148_full_registration_terminal_qualified':qualified148,
  'actual149_original80_replay_missing2023_five_states':True,'actual149_additional20_native20_cold_queued_before_quality':True,
  'actual149_current_dispatch7_preserves_native4_full4_duplicate3':True,
  'actual152_new_scientific_direction':'separate_signed_L1_Elastic_sparse_CDF_correction_after_complete148_parent',
  'actual152_proposal_quality_cases':29,'actual152_synthetic_cases_passed':25,'actual152_synthetic_prefixes_passed':75,
  'actual152_mature_saved_state_metadata_passed':10,'actual152_parent148_predictor_adapter_ABI_passed':True,
  'actual152_native60_and_full25_prefix75_owned_receivers_queued':True,
  'actual152_complete_quality_receivers_prior_forecast_duplicate_audit_and_official_score_freeze_inference_QA_main_still_required':True,
  'actual152_official_scores':0,'actual152_future_X_read':False,'new_native_fits':0,
  'new149152_validation_main_sync_actual_owned_handle':actual['actual149_all5_and152_historical_main_publication_v52_20261009'],
  'actual_current_jobs':actual,'current_main_recovery_receipt':read(sources[-1]),
  'previous20261008_stop_fulfilled_expired_schedule_not_restarted':True,'optimization_exhaustion_proven':False,'test_labels_read':False})
 print({'best':best,'new152_synthetic25_prefix75_passed':True,'actual148_full_qualified':qualified148,'checkpoint':str(A/'actual_optimization_checkpoint_v52_20261009.json')},flush=True)
if __name__=='__main__':main()
