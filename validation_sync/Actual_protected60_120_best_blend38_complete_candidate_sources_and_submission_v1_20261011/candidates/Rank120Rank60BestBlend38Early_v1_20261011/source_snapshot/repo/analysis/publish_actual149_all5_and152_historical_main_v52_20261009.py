"""Synchronize actual149 missing-year closure and actual152 historical controls to main."""
from pathlib import Path
import sys,time,hashlib,gzip
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def closed(n):
 f=A/'service_owned_workflows_20261006'/n
 while not (f/'service_execution.json').exists():time.sleep(10)
 while owned(read(f/'native_launch.json')):time.sleep(1)
 assert read(f/'service_execution.json')['status']=='passed',n
def main():
 jobs=['AdaptiveJointCrossHuber242_round148_full_registration_v2_20261009',
  'PureRFFHuber80_native_historical_calendar_controls_v4_20261009',
  'PureRFFHuber20_year2023_native_supplement_v1_20261009','PureRFFHuber25_all5_annual_native_coverage_v1_20261009',
  'SparseAfter14860_native_historical_calendar_controls_v1_20261009','SparseAfter14825_full_historical_controls_v1_20261009']
 for n in jobs:closed(n)
 pointers=[A/n for n in ['actual_PureRFFHuber80_native_calendar_location_v2_20261008.json',
  'actual_PureRFFHuber20_year2023_native_supplement_location_v1_20261009.json',
  'actual_SparseAfter14860_native_calendar_location_v1_20261009.json','actual_SparseAfter14825_parent148_location_v1_20261009.json']]
 proofs=[A/'Pure149_all25_annual_native_coverage_v1_20261009.json',
  A/'SparseAfter14829_synthetic25_and_state10_metadata_v1_20261009.json',
  A/'SparseAfter148152_historical_receiver_preparation_v1_20261009.json',
  A/'Pure149_all5_annual_native_receiver_binding_v8_20261009.json']
 sources=[Path(__file__),*pointers,*proofs,A/'Pure149_all5_annual_native_hidden_launches_v8_20261009.json',
  A/'Pure149_all5_annual_native_old_dispatch6_retired_v8_20261009.json',A/'SparseAfter148152_historical_hidden_launches_v1_20261009.json',
  A/'github_validation_sync_main_20261005/round148_receipt.json',A/'optimization_20261003_r148/full_registration_execution.json']
 for p in pointers:
  out=Path(read(p)['output']);v=out/'verification.json';assert sha(v)==read(p)['verification_sha256']
  proofs.append(v);sources.extend(out.glob('*.json'))
 for p in proofs:
  for f,d in read(p)['input_sha256'].items():
   assert sha(f)==d,f
   if Path(f).suffix in ('.py','.json','.md'):sources.append(Path(f))
 for pattern in ('*SparseAfter148*','*Pure149_all5*','*Pure149_all25*','*bind_Pure149_all5*'):
  sources.extend(p for p in A.glob(pattern) if p.is_file() and p.suffix in ('.py','.json'))
 for n in jobs:
  f=A/'service_owned_workflows_20261006'/n;sources.extend(p for p in f.iterdir() if p.suffix in ('.json','.log'))
 sources=list(dict.fromkeys(sources));assert all(p.is_file() for p in sources)
 coverage=read(A/'Pure149_all25_annual_native_coverage_v1_20261009.json')
 assert coverage['actual_head_year_states']==25 and coverage['actual_native_cases']==coverage['actual_cold_cases']==100
 native=read(Path(read(pointers[2])['output'])/'verification.json')
 full=read(Path(read(pointers[3])['output'])/'verification.json')
 assert (native['actual_historical_cases'],native['actual_calendar_cases'],native['actual_cold_cases'])==(48,12,60)
 assert (full['actual_stage_base_round'],full['actual_full_cases_including_identity'],full['actual_cold_cases_including_identity'])==(148,25,75)
 from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
 from verified_TLS_Git_retry_runtime_v2_20261008 import installed
 import publish_classifier_consensus_workflows_20261006 as helpers
 out=Path('E:/赛题五_本机临时/actual149_all5_and152_historical_main_v52_20261009');out.mkdir(exist_ok=False);held=[]
 try:
  row=read(A/'service_owned_workflows_20261006/main_publisher_v9_20261009/native_launch.json');assert owned(row)
  parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
  create(out/'main_watcher_idle_hold.json',{'identity':row,'stack':idle,'scientific_workers_held':0})
  sync=helpers.sync;prefix=Path('validation_sync/actual149_all5_and152_historical_v52_20261009');payload={};bindings={}
  for source in sources:
   data=source.read_bytes();assert not sync.SECRET.search(data),source
   digest=hashlib.sha256(data).hexdigest();relative=source.relative_to(ROOT) if source.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+source.name)
   target=(prefix/relative).as_posix();size=len(data)
   if size>=5*1024**2:data=gzip.compress(data,mtime=0);target+='.gz';assert hashlib.sha256(gzip.decompress(data)).hexdigest()==digest
   payload[target]=data;bindings[str(source)]={'published_path':target,'raw_sha256':digest,'original_bytes':size}
  payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
  payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'actual149_all25_annual_native100_cold100_and152_native60_full25_cold75_historical_controls',
   'at_local':sync.now(),'files':bindings,'actual149_all5_annual_states':25,'actual149_native_controls':100,'actual149_cold_native_controls':100,
   'actual152_stage_base_round':148,'actual152_all5_annual_states':10,'actual152_native_controls':60,'actual152_cold_native_controls':60,
   'actual152_full_historical_cases':25,'actual152_full_prefix_cases':75,'actual152_official_scores':0,'actual152_future_X_read':False,
   'new_native_fits':0,'test_labels_read':False,'primary_workspace_dirty_index_preserved':True,'search_exhaustion_claimed':False})
  create(out/'frozen_before_main_publication.json',{'files':bindings,'actual152_official_scores':0})
  with installed(out/'file_backed_git'):
   previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous);assert not sync.git('status','--porcelain')
   for n,d in payload.items():sync.atomic(sync.WORKTREE/n,d)
   names=sorted(payload)
   for left in range(0,len(names),50):sync.git('add','-f','--',*names[left:left+50])
   assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
   sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','同步149全五年度100原生及152在完整148上稀疏修正25历史75因果验证',timeout=180)
   commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()};assert helpers.blob_hashes(commit,hashes)==hashes
   sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit)
   value={'status':'pushed_and_remote_head_verified','at_local':sync.now(),'branch':'main','commit':commit,'raw_git_blobs_verified':len(hashes),
    'actual149_all25_annual_states100_native100_cold':True,'actual152_native60_full25_prefix75':True,'actual152_official_scores':0,
    'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()}
   create(out/'receipt.json',value);create(A/'actual149_all5_and152_historical_main_v52_receipt_20261009.json',value);print(value,flush=True)
 finally:
  for p in reversed(held):
   if p.is_running():p.resume()
  create(out/'idle_publisher_resumed.json',{'held_processes':len(held),'resumed_in_finally':True,'scientific_workers_held':0})
if __name__=='__main__':main()
