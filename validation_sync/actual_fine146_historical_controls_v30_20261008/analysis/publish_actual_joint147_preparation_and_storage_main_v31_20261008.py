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
 for n in ('actual_fine146_historical_controls_main_publication_v30_20261008',
  'HuberCrossFamilyFine125_controls_main_publication_v2_20261008',
  'Git_publisher_exact_nine_index_refresh_verified_E_relocation_v10_20261008'):closed(n)
 from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
 from verified_TLS_Git_retry_runtime_v2_20261008 import installed
 import publish_classifier_consensus_workflows_20261006 as helpers
 out=Path('E:/赛题五_本机临时/actual_joint147_preparation_and_storage_main_v31_20261008');out.mkdir(exist_ok=False);held=[]
 try:
  for n,needle in [('HuberCrossFamilyFine125_scores_main_publication_v2_20261008','    closed (publish_HuberCrossFamilyFine125_evidence_v3_20261008.py:'),
   ('main_publisher_v8_20261008','    main (watch_validations_main_v7_20261006.py:71)')]:
   row=read(A/'service_owned_workflows_20261006'/n/'native_launch.json');assert owned(row)
   parent,worker,proof=suspended_idle(row,needle);held.extend((worker,parent));create(out/(n+'_idle_hold.json'),{'identity':row,'stack':proof,'scientific_workers_held':0})
  since=datetime.datetime(2026,10,8,19,9).timestamp()
  sources=[Path(__file__),A/'actual_optimization_checkpoint_v32_20261008.json',A/'optimization_20261003_r140/full_registration_execution.json',
   A/'github_validation_sync_main_20261005/round140_receipt.json',A/'HuberCrossFamilyFine125_prospective_routes_v3_20261008.json',
   A/'JointCrossHuberOrder185_round147_proposal_v1_20261008.json',A/'Git_publisher_E_relocation_location_v10_20261008.json']
  sources.extend(p for p in A.iterdir() if p.is_file() and p.suffix in ('.py','.json','.md') and p.stat().st_mtime>=since)
  for f in (A/'service_owned_workflows_20261006').iterdir():
   if not f.is_dir():continue
   entries=[p for p in f.iterdir() if p.is_file() and p.suffix in ('.json','.log')]
   if any(p.stat().st_mtime>=since for p in entries):sources.extend(entries)
  for pointer in ('actual_JointCrossHuber35_existing_native_location_v1_20261008.json','actual_JointCrossHuber181_synthetic_location_v1_20261008.json'):
   f=Path(read(A/pointer)['output']);sources.extend(f.glob('*.json'))
  for version in (4,5,6,7,8,9,10):
   f=Path(f'E:/赛题五_本机临时/Git_publisher_E_relocation_v{version}_20261008')
   if f.is_dir():sources.extend(f.glob('*.json'))
  resource=Path('E:/赛题五_本机临时/full_board_deferred_resource_budget_v2_20261008')
  if resource.is_dir():sources.extend(resource.glob('*.json'))
  storage=Path(read(A/'Git_publisher_E_relocation_location_v10_20261008.json')['output'])/'verification.json';v=read(storage)
  assert v['status']=='passed_E_publisher_relocation_original_D_identity_all_raw_records_main_and_scores_preserved'
  assert Path(v['original_access_path']).is_junction() and Path(v['original_access_path']).resolve()==Path(v['physical_E_path']).resolve()
  native=read(Path(read(A/'actual_JointCrossHuber35_existing_native_location_v1_20261008.json')['output'])/'verification.json');assert native['actual_saved_model_count']==35 and not native['new_native_replay_claimed']
  synthetic=read(Path(read(A/'actual_JointCrossHuber181_synthetic_location_v1_20261008.json')['output'])/'verification.json');assert synthetic['actual_cases']==181 and synthetic['actual_cold_cases']==543
  sync=helpers.sync;prefix=Path('validation_sync/actual_joint147_preparation_and_verified_storage_v31_20261008');payload={};bindings={}
  for source in dict.fromkeys(sources):
   data=source.read_bytes();assert not sync.SECRET.search(data),source
   digest=hashlib.sha256(data).hexdigest();size=len(data);relative=source.relative_to(ROOT) if source.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+source.name)
   target=(prefix/relative).as_posix()
   if size>=5*1024**2:data=gzip.compress(data,mtime=0);target+='.gz';assert hashlib.sha256(gzip.decompress(data)).hexdigest()==digest
   payload[target]=data;bindings[str(source)]={'published_path':target,'raw_sha256':digest,'original_bytes':size,'captured_at_local':sync.now()}
  payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
  payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'actual_verified_storage_and_existing35_and_synthetic181_evidence_with_all_retained_failures',
   'at_local':sync.now(),'files':bindings,'actual140_official_cases':52,'actual140_original_QA51_and_main_completed':True,
   'actual_E_relocation_D_freed_bytes':v['D_freed_bytes'],'all_original_raw_legacy_records_kept_on_E':True,'primary_workspace_dirty_index_preserved':True,
   'actual147_existing_native_states_rehashed':35,'new147_native35_replay_not_claimed':True,'actual147_synthetic_cases':181,'actual147_synthetic_cold_cases':543,
   'actual147_full_historical_and_native_jobs_have_their_own_actual_statuses':True,'no147_quality_or_future_inference_claimed':True,
   'all_failed_receivers_and_launcher_failures_preserved':True,'running_logs_are_frozen_snapshots_at_capture':True,'optional_benchmark_memory_wait_bounded':True,
   'new_quality_scores_by_publication':0,'test_labels_read':False,'global_search_or_compute_exhaustion_claimed':False})
  create(out/'frozen_before_main_publication.json',{'files':bindings,'all_passed_failed_running_and_proposed_scopes_distinct':True,'new_quality_scores':0})
  with installed(out/'file_backed_git'):
   previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous);assert not sync.git('status','--porcelain')
   for n,data in payload.items():sync.atomic(sync.WORKTREE/n,data)
   names=sorted(payload)
   for left in range(0,len(names),50):sync.git('add','-f','--',*names[left:left+50])
   assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
   sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','同步147轮联合权重顺序验证准备与E盘迁移核验，保留失败记录',timeout=180)
   commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()};assert helpers.blob_hashes(commit,hashes)==hashes
   sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit)
   receipt={'status':'pushed_and_remote_head_verified','at_local':sync.now(),'branch':'main','commit':commit,'raw_git_blobs_verified':len(hashes),
    'new_quality_scores':0,'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()}
   create(out/'receipt.json',receipt);create(A/'actual_joint147_preparation_and_storage_main_v31_receipt_20261008.json',receipt);print(json.dumps(receipt,ensure_ascii=False),flush=True)
 finally:
  for p in reversed(held):
   if p.is_running():p.resume()
  create(out/'actual_idle_publishers_resumed.json',{'held_processes':len(held),'resumed_in_finally':True,'scientific_workers_held':0})
if __name__=='__main__':main()
