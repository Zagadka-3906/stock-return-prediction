"""Record actual completion and owned next stages; do not turn a score into qualification."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def main():
 s=A/'service_owned_workflows_20261006'
 completed=['AdaptiveJointCrossHuber242_official_comparison_v1_20261008',
  'AdaptiveJointCrossHuber242_scores_main_publication_v1_20261008',
  'AdaptiveJointCrossHuber242_selected_candidate_preparation_v2_20261009',
  'AdaptiveJointCrossHuber242_selected_candidate_sealing_v2_20261009',
  'actual148149_recovery_main_publication_v51_20261009']
 for n in completed:
  assert read(s/n/'service_execution.json')['status']=='passed' and not owned(read(s/n/'native_launch.json')),n
 names=['AdaptiveJointCrossHuber242_round148_full_registration_v2_20261009',
  'PureRFFHuber80_native_historical_calendar_controls_v4_20261009',
  'PureRFFHuber124_actual_full_historical_controls_v4_20261009',
  'Pure149_prior_complete_forecast_duplicate_audit_v3_20261009',
  'PureRFFHuber149_complete_chronological_dispatch_v6_20261009',
  'HuberSparse150_complete_chronological_dispatch_v3_20261009',
  'RFFSparse151_complete_chronological_dispatch_v2_20261009',
  'actual_chronological_optimization_progress_observer_v51_20261009',
  'main_publisher_v9_20261009']
 live={n:read(s/n/'native_launch.json') for n in names}
 for n,r in live.items():assert owned(r),n
 ready=A/'AdaptiveJointCrossHuber242_selected_release_v2_20261009/selected_candidate_ready_for_registration.json'
 value=read(ready);assert value['sealed_candidate_complete'] and value['new_inference_claimed']
 c=Path(value['source_candidate']);prediction=read(c/'verification.json')
 assert (prediction['rows'],prediction['days'],prediction['codes'])==(1599600,344,4650)
 for k in ('model_reload_bit_identical','pipeline_replay_bit_identical','csv_replay_byte_identical','cold80_day_prefix_bit_identical'):assert prediction[k]
 assert sha(c/'manifest.json')==value['source_manifest_sha256']
 receipt=A/'actual148149_recovery_main_v51_receipt_20261009.json'
 assert read(receipt)['status']=='pushed_and_remote_head_verified'
 proof=A/'AdaptiveJointCrossHuber242_official_comparison_v1_20261008/verification.json'
 assert len(read(proof)['records'])==242
 inputs=[Path(__file__),ready,c/'manifest.json',c/'verification.json',proof,receipt,
  *(s/n/'service_execution.json' for n in completed)]
 create(A/'actual_optimization_checkpoint_v51_20261009.json',{
  'status':'active_actual148242_scored_and_sealed_two_full_native_replays_full_registration_running',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in inputs},
  'best_fully_qualified':{'round':147,'score':0.4511896739186047,'main_commit':'1d5d0bffbafc468c9a7e928034ac6cffc8fee9d7'},
  'actual148_scoring_winner':{'case':175,'score':0.4511917507998099,'gain_over147':2.076881205181902e-6,'models':24},
  'actual148_candidate_native_reload_independent_CSV_two_full_and_cold80_passed':True,
  'actual148_candidate_sealed':True,'actual148_full_QA59_six_views_and_main_still_required':True,
  'candidate_csv_sha256':prediction['csv_sha256'],'current_main_receipt':read(receipt),
  'current_live_services':live,'actual149_receivers_use_recovered148_full_service':True,
  'actual150151_all20_annual_states90_native90_cold_and151_complete32_440_preflight_passed':True,
  'actual149150151_quality_scores':0,'optimization_exhaustion_proven':False,
  'old_failed148149_services_preserved':True,'previous20261008_stop_fulfilled_expired_schedule_not_restarted':True,
  'test_labels_read':False})
 print({'checkpoint':str(A/'actual_optimization_checkpoint_v51_20261009.json'),'actual148_scored':242,'actual148_candidate_sealed':True,'actual148_full_running':True},flush=True)
if __name__=='__main__':main()
