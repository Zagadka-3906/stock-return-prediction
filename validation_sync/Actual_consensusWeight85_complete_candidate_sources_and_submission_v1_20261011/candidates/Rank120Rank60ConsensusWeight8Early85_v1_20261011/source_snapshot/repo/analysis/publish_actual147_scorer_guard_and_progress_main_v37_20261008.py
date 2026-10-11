"""Publish actual recovery failures, verified E storage and pending joint147 controls after the prior main30 publisher closes."""
from pathlib import Path
import datetime,gzip,hashlib,json,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def closed(n):
 p=A/'service_owned_workflows_20261006'/n
 while not (p/'service_execution.json').exists():time.sleep(15)
 while owned(read(p/'native_launch.json')):time.sleep(1)
 assert read(p/'service_execution.json')['status']=='passed',n
def main():
 for n in ('actual14780_149_preflight_and2355_main_publication_v36_20261008','HuberCrossFamilyFine125_round146_full_registration_v4_20261008'):closed(n)
 from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
 from verified_TLS_Git_retry_runtime_v2_20261008 import installed
 import publish_classifier_consensus_workflows_20261006 as helpers
 out=Path('E:/赛题五_本机临时/actual147_scorer_guard_and_progress_main_v37_20261008');out.mkdir(exist_ok=False);held=[]
 try:
  for n,needle in [('main_publisher_v8_20261008','    main (watch_validations_main_v7_20261006.py:71)')]:
   row=read(A/'service_owned_workflows_20261006'/n/'native_launch.json');assert owned(row)
   parent,worker,proof=suspended_idle(row,needle);held.extend((worker,parent));create(out/(n+'_idle_hold.json'),{'identity':row,'stack':proof,'scientific_workers_held':0})
  since=datetime.datetime(2026,10,8,22,44).timestamp()
  sources=[Path(__file__),A/'actual_optimization_checkpoint_v42_20261008.json',A/'Joint147_actual_scorer_upstream_recovery_v6_20261008.json',A/'actual_progress41_idle_line_failure_v1_20261008.json',A/'actual_progress146_and147_receiver_binding_v42_20261008.json',A/'actual_optimization_checkpoint_v32_20261008.json',A/'optimization_20261003_r140/full_registration_execution.json',
   A/'github_validation_sync_main_20261005/round140_receipt.json',A/'HuberCrossFamilyFine125_prospective_routes_v3_20261008.json',
   A/'JointCrossHuberOrder185_round147_proposal_v1_20261008.json',A/'Git_publisher_E_relocation_location_v10_20261008.json']
  sources += [A/'actual_optimization_checkpoint_v35_20261008.json',A/'optimization_20261003_r145/full_registration_execution.json',A/'github_validation_sync_main_20261005/round145_receipt.json',A/'latest_verified_submission_delivery_v2_20261008.json',A/'AdaptiveJointCrossHuber242_prospective_routes_v2_20261008.json',A/'actual_deferred_serialization_RAM_boundary_v3_20261008.json']
  sources += [A/'actual_optimization_checkpoint_v36_20261008.json',A/'PureRFFHuber128_round149_proposal_v1_20261008.json',A/'PureRFFHuber149_synthetic_receiver_recovery_v2_20261008.json']
  sources += [A/'actual_optimization_checkpoint_v38_20261008.json',A/'optimization_20261003_r146/full_registration_execution.json',A/'github_validation_sync_main_20261005/round146_receipt.json',A/'actual_obsolete_progress_readers_retired_v37_20261008.json',A/'actual_old_progress37_retired_after38_v1_20261008.json']
  sources.extend(p for p in A.iterdir() if p.is_file() and p.suffix in ('.py','.json','.md') and p.stat().st_mtime>=since)
  for f in (A/'service_owned_workflows_20261006').iterdir():
   if not f.is_dir():continue
   entries=[p for p in f.iterdir() if p.is_file() and p.suffix in ('.json','.log')]
   if any(p.stat().st_mtime>=since for p in entries):sources.extend(entries)
  for pointer in ('actual_JointCrossHuber35_existing_native_location_v1_20261008.json','actual_JointCrossHuber181_synthetic_location_v1_20261008.json','actual_AdaptiveJointCrossHuber238_synthetic_location_v2_20261008.json','actual_PureRFFHuber124_synthetic_location_v2_20261008.json','actual_PureRFFHuber25_existing_native_location_v1_20261008.json','actual_JointCrossHuber80_native_calendar_location_v3_20261008.json'):
   f=Path(read(A/pointer)['output']);sources.extend(f.glob('*.json'))
  for directory in ('shutdown_ready_stop_preflight_current2355_20261008','shutdown_ready_stop_preflight_current2355_preheld_20261008','user_requested_stop2355_until_manual_continue_20261008'):
   sources.extend((A/directory).glob('*.json'))
  for version in (4,5,6,7,8,9,10):
   f=Path(f'E:/赛题五_本机临时/Git_publisher_E_relocation_v{version}_20261008')
   if f.is_dir():sources.extend(f.glob('*.json'))
  resource=Path('E:/赛题五_本机临时/full_board_deferred_resource_budget_v3_20261008')
  if resource.is_dir():sources.extend(resource.glob('*.json'))
  storage=Path(read(A/'Git_publisher_E_relocation_location_v10_20261008.json')['output'])/'verification.json';v=read(storage)
  assert v['status']=='passed_E_publisher_relocation_original_D_identity_all_raw_records_main_and_scores_preserved'
  assert Path(v['original_access_path']).is_junction() and Path(v['original_access_path']).resolve()==Path(v['physical_E_path']).resolve()
  native=read(Path(read(A/'actual_JointCrossHuber35_existing_native_location_v1_20261008.json')['output'])/'verification.json');assert native['actual_saved_model_count']==35 and not native['new_native_replay_claimed']
  synthetic=read(Path(read(A/'actual_JointCrossHuber181_synthetic_location_v1_20261008.json')['output'])/'verification.json');assert synthetic['actual_cases']==181 and synthetic['actual_cold_cases']==543
  sync=helpers.sync;prefix=Path('validation_sync/actual147_scorer_guard_and_progress_v37_20261008');payload={};bindings={}
  for source in dict.fromkeys(sources):
   data=source.read_bytes();assert not sync.SECRET.search(data),source
   digest=hashlib.sha256(data).hexdigest();size=len(data);relative=source.relative_to(ROOT) if source.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+source.name)
   target=(prefix/relative).as_posix()
   if size>=5*1024**2:data=gzip.compress(data,mtime=0);target+='.gz';assert hashlib.sha256(gzip.decompress(data)).hexdigest()==digest
   payload[target]=data;bindings[str(source)]={'published_path':target,'raw_sha256':digest,'original_bytes':size,'captured_at_local':sync.now()}
  payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
  qualified=read(A/'github_validation_sync_main_20261005/round145_receipt.json');prosp=read(A/'AdaptiveJointCrossHuber242_prospective_routes_v2_20261008.json');resource_proof=read(resource/'verification.json')
  payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'actual_verified_storage_and_existing35_and_synthetic181_evidence_with_all_retained_failures',
   'at_local':sync.now(),'files':bindings,'actual140_official_cases':52,'actual140_original_QA51_and_main_completed':True,
   'actual_E_relocation_D_freed_bytes':v['D_freed_bytes'],'all_original_raw_legacy_records_kept_on_E':True,'primary_workspace_dirty_index_preserved':True,
   'actual147_existing_native_states_rehashed':35,'new147_native35_replay_not_claimed':True,'actual147_synthetic_cases':181,'actual147_synthetic_cold_cases':543,
   'actual145_qualified_main_commit':qualified['commit'],'actual145_qualified_score':qualified['official_score'],'actual145_qualified_physical_models':22,'connected_records_at145':14405,'actual148_prospective_sources':prosp['actual_prospective_sources'],'actual148_prospective_graph_controls':prosp['actual_graph_controls'],'actual_optional_RAM_boundary':resource_proof,'actual147_full_historical_and_native_jobs_have_their_own_actual_statuses':True,'no147_quality_or_future_inference_claimed':True,
   'all_failed_receivers_and_launcher_failures_preserved':True,'running_logs_are_frozen_snapshots_at_capture':True,'optional_benchmark_memory_wait_bounded':True,
   'actual149_synthetic_cases':124,'actual149_synthetic_cold_cases':372,'actual149_zero_Ridge_reference_forecast_bits_equal':True,'actual149_existing25_state_subset_audit_completed_not_new_native_replay':True,'actual149_historical_native80_full124_queued_actual_status_in_snapshots':True,'actual149_32_source992_graph_preflight_completed':True,'actual149_duplicate_audit_and_actual_native_full_controls_still_pending':True,'actual147_80_native_controls_completed':True,'actual147_scorer_upstream_corrected_before_any185_score':True,'all_scorer_numeric_calculations_and_case_grid_preserved':True,'progress146_successful_recovery_service_binding_corrected':True,'progress_idle_line_failure_preserved_and_two_old_observers_retired':True,'actual_user2355_stop_schedule_live_not_paused_early':True,'actual_user_stop_at_local':'2026-10-08T23:55:00+08:00','automatic_restart_enabled':False,'actual146125_quality_and_selected_new_candidate_two_full_replays_QA57_and_main_completed':True,'actual146_retry_failures_preserved':True,'actual149_official_scores':0,'actual149_future_inference':0,'new_quality_scores_by_publication':0,'test_labels_read':False,'global_search_or_compute_exhaustion_claimed':False})
  create(out/'frozen_before_main_publication.json',{'files':bindings,'all_passed_failed_running_and_proposed_scopes_distinct':True,'new_quality_scores':0})
  with installed(out/'file_backed_git'):
   previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous);assert not sync.git('status','--porcelain')
   for n,data in payload.items():sync.atomic(sync.WORKTREE/n,data)
   names=sorted(payload)
   for left in range(0,len(names),50):sync.git('add','-f','--',*names[left:left+50])
   assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
   sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','同步147轮评分前依赖修正、真实进度及观察器失败恢复记录',timeout=180)
   commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()};assert helpers.blob_hashes(commit,hashes)==hashes
   sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit)
   receipt={'status':'pushed_and_remote_head_verified','at_local':sync.now(),'branch':'main','commit':commit,'raw_git_blobs_verified':len(hashes),
    'new_quality_scores':0,'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()}
   create(out/'receipt.json',receipt);create(A/'actual147_scorer_guard_and_progress_main_v37_receipt_20261008.json',receipt);print(json.dumps(receipt,ensure_ascii=False),flush=True)
 finally:
  for p in reversed(held):
   if p.is_running():p.resume()
  create(out/'actual_idle_publishers_resumed.json',{'held_processes':len(held),'resumed_in_finally':True,'scientific_workers_held':0})
if __name__=='__main__':main()
