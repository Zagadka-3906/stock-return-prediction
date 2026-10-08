"""Record actual140 full/main completion and current146/147 controls, never turn queued work into a pass."""
from pathlib import Path
import sys,time,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
 files=[Path(__file__),A/'optimization_20261003_r140/full_registration_execution.json',A/'github_validation_sync_main_20261005/round140_receipt.json',
  A/'optimization_20261003_r139/full_registration_execution.json',A/'github_validation_sync_main_20261005/round139_receipt.json',A/'latest_verified_submission_delivery_v2_20261008.json',
  A/'HuberCrossFamilyFine125_prospective_routes_v3_20261008.json',A/'JointCrossHuberOrder185_round147_proposal_v1_20261008.json',
  A/'actual_JointCrossHuber181_synthetic_location_v1_20261008.json',A/'actual_JointCrossHuber35_existing_native_location_v1_20261008.json',
  A/'actual_idle_optional_benchmark_handoff_v2_20261008.json',A/'actual_resource_bounded_serialization_handoff_hidden_launches_v2_20261008.json',
  A/'JointCrossHuber80_native_calendar_hidden_launch_v2_20261008.json',A/'JointCrossHuber181_full_historical_hidden_launch_v1_20261008.json']
 assert read(files[1])['status']=='passed';receipt=read(files[2]);assert receipt['status']=='pushed_and_remote_head_verified' and receipt['connected_records']==14228
 assert read(files[3])['status']=='passed' and read(files[4])['status']=='pushed_and_remote_head_verified'
 p=read(files[6]);assert p['actual_prospective_sources']==32 and p['actual_graph_controls']==968
 synthetic=Path(read(files[8])['output'])/'verification.json';native=Path(read(files[9])['output'])/'verification.json'
 assert read(synthetic)['actual_cases']==181 and read(synthetic)['actual_cold_cases']==543
 assert read(native)['actual_saved_model_count']==35 and not read(native)['new_native_replay_claimed']
 files.extend([synthetic,native]);score=read(A/'optimization_20261003_r139/calibrated_csv_official.json')['metrics']['final_score']
 create(A/'actual_optimization_checkpoint_v32_20261008.json',{'status':'actual140_complete_141_scoring_and146_preflight_passed_joint147_synthetic_and_existing35_evidence_complete',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'deadline_local':'2026-10-10T23:59:00+08:00','input_sha256':{str(f):sha(f) for f in files},
  'fully_qualified_best_round':139,'fully_qualified_best_score':score,'fully_qualified_best_physical_models':24,
  'actual140_existing_official_cases':52,'actual140_full_QA51_and_main_passed':True,'actual140_main_commit':receipt['commit'],'connected_full_records_at140':14228,
  'actual146_prospective_sources':32,'actual146_prospective_graph_controls':968,'actual146_official_scoring_not_started_at_record':True,
  'actual147_synthetic_cases':181,'actual147_synthetic_cold_cases':543,'actual147_existing_native_states_rehashed':35,
  'new_native35_replay_not_claimed':True,'native14780_and_full147181_jobs_only_queued':True,'actual147_quality_receivers_still_to_prepare':True,
  'optional24GiB_memory_wait_bounded_to300seconds_after145':True,'original_20261007_shutdown_schedule_not_restarted':True,
  'new_quality_scores_by_checkpoint':0,'test_labels_read':False,'global_optimization_or_compute_exhaustion_claimed':False})
 print(json.dumps({'actual140_main_commit':receipt['commit'],'full_records':14228,'best_round':139,'best_score':score}),flush=True)
if __name__=='__main__':main()
