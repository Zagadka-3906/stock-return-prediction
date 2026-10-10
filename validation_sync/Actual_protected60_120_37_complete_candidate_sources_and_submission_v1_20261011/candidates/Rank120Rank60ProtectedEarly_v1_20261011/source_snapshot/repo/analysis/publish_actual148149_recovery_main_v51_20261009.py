"""Publish completed242 scores and path/ABI recovery evidence to main, preserving failures."""
from pathlib import Path
import sys,time,hashlib,gzip
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def main():
 meta=[A/n for n in ['Adaptive148_candidate_entry_recovery_v6_20261009.json','Pure149_actual148_gate_recovery_v7_20261009.json',
  'actual148149_recovery_observer_preparation_v51_20261009.json']]
 sources=[Path(__file__),*meta,A/'AdaptiveJointCrossHuber242_scores_github_v1_20261008/receipt.json',
  A/'actual148149_recovery_observer_hidden_launch_v51_20261009.json',A/'actual_old_progress50_retired_after51_v1_20261009.json',
  A/'Adaptive148_candidate_entry_hidden_launches_v6_20261009.json',A/'Pure149_actual148_gate_hidden_launches_v7_20261009.json']
 for p in meta:
  for f,d in read(p)['input_sha256'].items():
   assert sha(f)==d,f
   if Path(f).suffix in ('.py','.json'):sources.append(Path(f))
 failed=['AdaptiveJointCrossHuber242_selected_candidate_preparation_v1_20261008',
  'AdaptiveJointCrossHuber242_selected_candidate_sealing_v1_20261008','AdaptiveJointCrossHuber242_round148_full_registration_v1_20261008',
  'PureRFFHuber80_native_historical_calendar_controls_v3_20261009','PureRFFHuber124_actual_full_historical_controls_v3_20261009',
  'Pure149_prior_complete_forecast_duplicate_audit_v2_20261009','PureRFFHuber149_complete_chronological_dispatch_v5_20261009']
 for n in failed:
  f=A/'service_owned_workflows_20261006'/n
  assert not owned(read(f/'native_launch.json')) and read(f/'service_execution.json')['status']=='failed'
  sources.extend(p for p in f.iterdir() if p.suffix in ('.json','.log'))
 for launch in [A/'Adaptive148_candidate_entry_hidden_launches_v6_20261009.json',A/'Pure149_actual148_gate_hidden_launches_v7_20261009.json']:
  for n in read(launch):
   f=A/'service_owned_workflows_20261006'/n
   sources.extend(f/p for p in ('native_launch.json','job_definition.json','verified_hidden_launch.json'))
 sources=list(dict.fromkeys(sources));assert all(p.is_file() for p in sources)
 receipt=read(A/'AdaptiveJointCrossHuber242_scores_github_v1_20261008/receipt.json')
 assert receipt['status']=='pushed_and_remote_head_verified' and receipt['official_score_records']==242
 from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
 from verified_TLS_Git_retry_runtime_v2_20261008 import installed
 import publish_classifier_consensus_workflows_20261006 as helpers
 out=Path('E:/赛题五_本机临时/actual148149_recovery_main_v51_20261009');out.mkdir(exist_ok=False);held=[]
 try:
  row=read(A/'service_owned_workflows_20261006/main_publisher_v9_20261009/native_launch.json');assert owned(row)
  parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
  create(out/'main_watcher_idle_hold.json',{'identity':row,'stack':idle,'scientific_workers_held':0})
  sync=helpers.sync;prefix=Path('validation_sync/actual148149_recovery_v51_20261009');payload={};bindings={}
  for source in sources:
   data=source.read_bytes();assert not sync.SECRET.search(data),source
   digest=hashlib.sha256(data).hexdigest();relative=source.relative_to(ROOT) if source.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+source.name)
   target=(prefix/relative).as_posix();size=len(data)
   if size>=5*1024**2:data=gzip.compress(data,mtime=0);target+='.gz';assert hashlib.sha256(gzip.decompress(data)).hexdigest()==digest
   payload[target]=data;bindings[str(source)]={'published_path':target,'raw_sha256':digest,'original_bytes':size}
  payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
  payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'actual148_all242_scores_main_and_path_only_recovery_with149_upstream_rebinding',
   'at_local':sync.now(),'files':bindings,'actual148_score_records':242,'actual148_best_score':0.4511917507998099,
   'candidate_winner_not_yet_fully_qualified':True,'original_failed_services_preserved':failed,
   'original_scientific_cases_and32_prospective_sources_unchanged':True,'actual5_parent_ABI_controls_per_family':True,
   'new_native_fits':0,'new_official_scores_by_publication':0,'test_labels_read':False,
   'primary_workspace_dirty_index_preserved':True,'search_exhaustion_claimed':False})
  create(out/'frozen_before_main_publication.json',{'files':bindings,'winner_fully_qualified':False})
  with installed(out/'file_backed_git'):
   previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous);assert not sync.git('status','--porcelain')
   for n,d in payload.items():sync.atomic(sync.WORKTREE/n,d)
   names=sorted(payload)
   for left in range(0,len(names),50):sync.git('add','-f','--',*names[left:left+50])
   assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
   sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','同步148完成242评分及候选入口恢复和149前序准入修复证据',timeout=180)
   commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()};assert helpers.blob_hashes(commit,hashes)==hashes
   sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit)
   value={'status':'pushed_and_remote_head_verified','at_local':sync.now(),'branch':'main','commit':commit,'raw_git_blobs_verified':len(hashes),
    'actual148_official_scores':242,'candidate_not_yet_fully_qualified':True,'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()}
   create(out/'receipt.json',value);create(A/'actual148149_recovery_main_v51_receipt_20261009.json',value);print(value,flush=True)
 finally:
  for p in reversed(held):
   if p.is_running():p.resume()
  create(out/'idle_publisher_resumed.json',{'held_processes':len(held),'resumed_in_finally':True,'scientific_workers_held':0})
if __name__=='__main__':main()
