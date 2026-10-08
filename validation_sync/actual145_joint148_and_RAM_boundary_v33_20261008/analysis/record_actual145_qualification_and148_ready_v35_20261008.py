"""Record qualified145 delivery, prepared148 receivers and actual bounded optional RAM evidence."""
from pathlib import Path
import sys,time,json,ast
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
 full=A/'optimization_20261003_r145/full_registration_execution.json';receipt=A/'github_validation_sync_main_20261005/round145_receipt.json'
 delivery=A/'latest_verified_submission_delivery_v2_20261008.json';d=read(delivery);r=read(receipt)
 assert read(full)['status']=='passed' and r['status']=='pushed_and_remote_head_verified' and d['selected_round']==145
 csv=Path(d['output'])/'submission.csv';assert sha(csv)==d['csv_sha256']
 prospective=A/'AdaptiveJointCrossHuber242_prospective_routes_v2_20261008.json';p=read(prospective)
 assert p['actual_prospective_sources']==32 and p['actual_graph_controls']==1904
 resource=Path('E:/赛题五_本机临时/full_board_deferred_resource_budget_v3_20261008/verification.json');boundary=read(resource)
 assert boundary['benchmark_encodes_executed']==0 and not boundary['new_runtime_adopted'] and boundary['samples'][-1]['elapsed_seconds']>=300
 # Small original resource record is preserved byte-for-byte for the already queued main31 evidence export.
 archived=A/'actual_deferred_serialization_RAM_boundary_v3_20261008.json'
 with archived.open('xb') as f:f.write(resource.read_bytes())
 assert sha(archived)==sha(resource)
 inputs=[Path(__file__),full,receipt,delivery,prospective,resource,archived,
  A/'service_owned_workflows_20261006/HuberCrossFamilyFine125_round146_source_admission_v2_20261008/service_execution.json',
  A/'service_owned_workflows_20261006/HuberCrossFamilyFine125_controls_main_publication_v2_20261008/service_execution.json']
 create(A/'actual_optimization_checkpoint_v35_20261008.json',{'status':'actual145_fully_qualified_and_delivered_146_scores_active_147_and148_complete_receivers_preflighted',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'deadline_local':'2026-10-10T23:59:00+08:00','input_sha256':{str(f):sha(f) for f in inputs},
  'best_fully_qualified_round':145,'official_training_score':d['official_score'],'actual_unique_native_models':22,'main_commit':r['commit'],
  'actual_QA56_all_six_views_and_main_passed':True,'connected_records':14405,'candidate_CSV':str(csv),'candidate_CSV_sha256':d['csv_sha256'],
  'competition_upload_performed':False,'all125_actual145_scores_and_two_full_native_independent_reload_CSV_cold80_passed':True,
  'actual146_source_admission_and_controls_main_passed_scores_started':True,
  'actual147_complete32_routes1448_graphs_and_all_four_previous_report_paths_passed':True,
  'actual148_complete32_routes1904_graphs_passed':True,'actual148_synthetic238_and714cold_passed':True,
  'actual147_and148_native_and_full_controls_only_queued_after_actual_previous_full_closure':True,
  'actual_optional_RAM_start_boundary':boundary,'optional_encoding_runs':0,'new_execution_runtime_adopted':False,
  'expired_20261007_shutdown_schedule_not_restarted':True,'new_quality_scores_by_checkpoint':0,'test_labels_read':False,
  'global_feasible_direction_or_compute_exhaustion_claimed':False})
 old=A/'monitor_actual_chronological_optimization_progress_v34_20261008.py';s=old.read_text(encoding='utf8').replace('optimization_live_progress_v34','optimization_live_progress_v35')
 s=s.replace("147:('JointCrossHuberOrder185',185,1)}","147:('JointCrossHuberOrder185',185,1),148:('AdaptiveJointCrossHuber242',242,1)}")
 s=s.replace("'actual148_official_scores':0,'complete_quality_receivers_not_yet_prepared':True", "'actual148_official_scores':pipeline['148']['completed_cases'],'complete_quality_receivers_preflighted':status('AdaptiveJointCrossHuber148_complete_prospective_controls_v2_20261008'),'chronological_dispatch':status('AdaptiveJointCrossHuber148_complete_chronological_dispatch_v2_20261008')")
 s=s.replace('242项正式评分流程仍待准备。','242项正式评分接收流程已通过32条程序检查，等待原生及完整历史控制。')
 p=A/'monitor_actual_chronological_optimization_progress_v35_20261008.py';compile(s,str(p),'exec')
 with p.open('x',encoding='utf8',newline='') as f:f.write(s)
 from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
 pins={str(p):sha(p),str(Path(__file__)):sha(__file__)};row=start('actual_chronological_optimization_progress_observer_v35_20261008',p.name,[],pins)
 create(A/'latest_actual_optimization_progress_pointer_v35_20261008.json',{'json':str(A/'optimization_live_progress_v35_20261008.json'),
  'markdown':str(A/'optimization_live_progress_v35_20261008.md'),'launch':row,'input_sha256':pins,'new_quality_scores':0})
 print(json.dumps({'best':145,'score':d['official_score'],'models':22,'observer':row['owned_worker_pid'],'optional_RAM_samples':len(boundary['samples'])}),flush=True)
if __name__=='__main__':main()
