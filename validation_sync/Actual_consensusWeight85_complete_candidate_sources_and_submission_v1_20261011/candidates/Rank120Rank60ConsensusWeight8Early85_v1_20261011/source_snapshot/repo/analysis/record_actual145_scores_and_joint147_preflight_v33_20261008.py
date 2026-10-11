"""Record completed scoring separately from qualification and a finite pending frontier."""
from pathlib import Path
import sys,time,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
 import monitor_actual_chronological_optimization_progress_v32_20261008 as previous
 state=previous.snapshot();pilot=A/'CrossFamilyFine125_official_comparison_v1_20261008/verification.json';quality=read(pilot)
 prospective=A/'JointCrossHuberOrder185_prospective_routes_v1_20261008.json';p=read(prospective)
 assert len(quality['records'])==125 and p['actual_prospective_sources']==32 and p['actual_graph_controls']==1448
 storage=A/'Git_publisher_E_relocation_location_v10_20261008.json'
 inputs=[Path(__file__),pilot,prospective,storage,A/'JointCrossHuber147_dispatch_hidden_launch_v1_20261008.json',
  A/'optimization_20261003_r141/full_registration_execution.json',A/'github_validation_sync_main_20261005/round141_receipt.json',
  A/'actual_fine146_historical_controls_main_v30_receipt_20261008.json']
 create(A/'actual_optimization_checkpoint_v33_20261008.json',{'status':'actual125_scores_complete_new145_leader_not_yet_qualified_and_joint147_all32_receivers_preflighted',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'deadline_local':'2026-10-10T23:59:00+08:00','input_sha256':{str(f):sha(f) for f in inputs},
  'best_fully_qualified_at_record':state['best_fully_qualified'],'actual145_quality_records':125,'actual145_training_winner':quality['best'],
  'actual145_gain_over_qualified139':quality['best']['connected_final_score']-read(A/'optimization_20261003_r139/calibrated_csv_official.json')['metrics']['final_score'],
  'actual145_future_freeze_native_reload_independent_CSV_cold80_full_QA56_and_main_still_required':True,
  'actual141_all52_records_full_QA52_and_main_passed':True,'connected_full_records_at141':14280,
  'verified_D_worktree_duplicate_bytes_freed':7912316928,'D_publisher_path_is_verified_E_junction':True,
  'joint147_32_prospective_routes_passed':True,'joint147_1448_complete_parent_graph_controls_passed':True,
  'joint147_80_native_and181full543cold_jobs_wait_for_actual146_closure':True,'joint147_quality_receivers_prepared_dispatch_waiting_not_scores':True,
  'joint147_actual_official_scores':0,'joint147_actual_future_inference':0,'optional24GiB_RAM_start_wait_bound_seconds':300,
  'expired_20261007_shutdown_schedule_not_restarted':True,'global_feasible_direction_or_compute_exhaustion_claimed':False,
  'new_scores_by_checkpoint':0,'test_labels_read':False})
 old=A/'monitor_actual_chronological_optimization_progress_v32_20261008.py';s=old.read_text(encoding='utf8')
 s=s.replace('optimization_live_progress_v32_20261008','optimization_live_progress_v33_20261008')
 needle="146:('HuberCrossFamilyFine125',125,2)}";assert s.count(needle)==1
 s=s.replace(needle,"146:('HuberCrossFamilyFine125',125,2),147:('JointCrossHuberOrder185',185,1)}")
 s=s.replace("'complete_quality_receivers_not_yet_admitted':True","'complete_quality_receivers_not_yet_admitted':status('JointCrossHuberOrder185_round147_source_admission_v1_20261008')['status']!='passed'")
 s=s.replace("'actual147_official_scores':0","'actual147_official_scores':pipeline['147']['completed_cases']")
 s=s.replace("'remaining_generator_admission_phase_publisher_dispatch_and_prospective_checks_pending':True", "'complete_prospective_routes':status('JointCrossHuber147_complete_prospective_controls_v1_20261008'),'chronological_dispatch':status('JointCrossHuber147_complete_chronological_dispatch_v1_20261008'),'all_quality_receivers_preflighted':True")
 s=s.replace("'new_official_scores':0,'new_native_fits':0,'complete_prospective_controls'", "'actual_official_score_records':pipeline['145']['completed_cases'],'new_native_fits':0,'complete_prospective_controls'")
 s=s.replace('尚未官方评分。','实际官方评分见上表；预检查通过后还需等待原生和完整控制。')
 p=A/'monitor_actual_chronological_optimization_progress_v33_20261008.py';compile(s,str(p),'exec')
 with p.open('x',encoding='utf8',newline='') as f:f.write(s)
 pins={str(p):sha(p),str(Path(__file__)):sha(__file__)}
 from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
 row=start('actual_chronological_optimization_progress_observer_v33_20261008',p.name,[],pins)
 create(A/'latest_actual_optimization_progress_pointer_v33_20261008.json',{'status':'actual_completed145_scoring_and_joint147_preflight_observer','json':str(A/'optimization_live_progress_v33_20261008.json'),
  'markdown':str(A/'optimization_live_progress_v33_20261008.md'),'launch':row,'input_sha256':pins,'new_quality_scores':0})
 print(json.dumps({'observer':row['owned_worker_pid'],'actual145_scores':125,'joint147_prospective_routes':32,'fully_qualified_best':state['best_fully_qualified']}),flush=True)
if __name__=='__main__':main()
