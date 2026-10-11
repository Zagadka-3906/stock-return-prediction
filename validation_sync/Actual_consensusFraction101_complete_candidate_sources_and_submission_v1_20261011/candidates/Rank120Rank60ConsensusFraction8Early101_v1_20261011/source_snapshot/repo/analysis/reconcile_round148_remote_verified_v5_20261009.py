"""Publish the verified148 tree with lossless16MiB report chunks, excluding rejected history."""
from pathlib import Path
import sys,os,time,subprocess,json,hashlib,gzip,io
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
OUT=Path('E:/赛题五_本机临时/round148_remote_verified_reconcile_v5_20261009')
def main():
 import publish_classifier_consensus_workflows_20261006 as helpers
 from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
 old=A/'service_owned_workflows_20261006/AdaptiveJointCrossHuber242_round148_full_registration_v2_20261009'
 assert not owned(read(old/'native_launch.json')) and read(old/'service_execution.json')['status']=='failed'
 failure=read(old/'service_execution.json')['failure'];assert 'GH001' in failure and '101.70 MB' in failure
 folder=A/'optimization_20261003_r148'
 evidence=read(folder/'provenance_scope_execution.json');assert evidence['status']=='passed' and evidence['all_original_six_view_browser_and_candidate_manifest_QA_passed']
 ready=read(A/'AdaptiveJointCrossHuber242_selected_release_v2_20261009/selected_candidate_ready_for_registration.json');assert ready['sealed_candidate_complete']
 assert not (folder/'full_registration_execution.json').exists()
 receipt=A/'github_validation_sync_main_20261005/round148_receipt.json';assert not receipt.exists()
 OUT.mkdir(exist_ok=False);sync=helpers.sync;work=sync.WORKTREE;resolved=work.resolve()
 assert resolved.drive.upper()=='E:' and work.resolve()!=ROOT.resolve()
 index=OUT/'recovery.index';env=dict(os.environ,GIT_INDEX_FILE=str(index));held=[];commands=[]
 def git(*args,data=None,isolated=False,timeout=300):
  for attempt in range(5):
   r=subprocess.run(['git','-c','http.proxy=http://127.0.0.1:7897','-c','http.version=HTTP/1.1',*args],cwd=work,input=data,capture_output=True,env=env if isolated else None,
    timeout=timeout,creationflags=subprocess.CREATE_NO_WINDOW)
   commands.append({'arguments':list(args),'exit_code':r.returncode,'attempt':attempt+1})
   if r.returncode==0:return r.stdout
   message=r.stderr.decode('utf8',errors='replace')
   transient=args[0] in ('push','ls-remote') and 'GH001' not in message and any(
    text in message.lower() for text in ('tls connect error','ssl routines','rpc failed','http2 framing','unexpected eof','connection reset','could not resolve host'))
   if not transient or attempt==4:raise RuntimeError(message[-3000:])
   time.sleep(min(15,2**attempt))
 def value(*args,**kwargs):return git(*args,**kwargs).decode('utf8').strip()
 def tree(commit):
  result={}
  for entry in git('ls-tree','-r','-z',commit).split(b'\0'):
   if not entry:continue
   left,name=entry.split(b'\t',1);mode,kind,digest=left.split();assert kind==b'blob'
   result[name.decode('utf8')]=(mode.decode(),digest.decode())
  return result
 try:
  identity=read(A/'service_owned_workflows_20261006/main_publisher_v9_20261009/native_launch.json');assert owned(identity)
  parent,worker,idle=suspended_idle(identity,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
  create(OUT/'owned_idle_main_hold.json',{'identity':identity,'stack':idle,'scientific_workers_held':0})
  proof_path=Path('E:/赛题五_本机临时/round148_chunked_main_recovery_v3_20261009/before_remote_push.json')
  proof=read(proof_path);rejected=proof['rejected_commit'];commit=proof['new_commit']
  parent_commit=proof['remote_parent'];descriptor=proof['descriptor']
  assert value('rev-parse','HEAD')==rejected
  assert value('rev-parse',commit+'^')==parent_commit
  assert value('rev-parse',rejected+'^')==parent_commit
  previous_tree=tree(rejected);actual=tree(commit)
  prefix='validation_sync/round148/'
  large=prefix+'complete_ranking_display/lossless_ranking_display_v2_20261006/round148/full_report_reconstructed_for_publication.json.gz'
  manifest_path=prefix+'manifest.json';original=work/large
  assert all(actual[name]==item for name,item in previous_tree.items() if name not in (large,manifest_path))
  expected=proof['new_artifact_blobs'];assert large not in actual
  assert set(actual)==(set(previous_tree)-{large})|set(expected)
  for name,digest in expected.items():
   blob=git('show',commit+':'+name)
   assert hashlib.sha256(blob).hexdigest()==digest
   assert sha(work/name)==digest,name
  manifest=read(work/manifest_path)
  assert manifest['scored_records']==242 and manifest['connected_records']==14957
  assert manifest['original_full_ranking_sha256']==descriptor['original_report_sha256']
  assert sha(original)==descriptor['compressed_sha256']
  assert sha(A/'lossless_ranking_display_v2_20261006/round148/full_report_reconstructed_for_publication.json.gz')==descriptor['compressed_sha256']
  h=hashlib.sha256();size=0
  for item in descriptor['parts']:
   block=(original.parent/item['path']).read_bytes()
   assert len(block)==item['bytes'] and hashlib.sha256(block).hexdigest()==item['sha256']
   h.update(block);size+=len(block)
  assert size==descriptor['compressed_bytes'] and h.hexdigest()==descriptor['compressed_sha256']
  remote=value('ls-remote','origin','refs/heads/main').split()[0]
  assert remote in (parent_commit,commit),remote
  create(OUT/'verified_existing_commit_before_push.json',{'proof':str(proof_path),'proof_sha256':sha(proof_path),
    'commit':commit,'remote_before':remote,'original_tree_and_all_new_bytes_verified':True,
    'explicit_existing_loopback_proxy':True,'TLS_verification_enabled':True,'root_index_untouched':True})
  if remote!=commit:git('push','origin',commit+':refs/heads/main',timeout=1200)
  assert value('ls-remote','origin','refs/heads/main').split()[0]==commit
  assert value('rev-parse','refs/heads/main')==parent_commit
  head_path=Path(value('rev-parse','--git-path','HEAD'))
  if not head_path.is_absolute():head_path=work/head_path
  assert head_path.read_text(encoding='ascii').strip()==rejected
  git('update-ref','refs/heads/main',commit,parent_commit)
  git('update-ref','--no-deref','HEAD',commit,rejected);git('read-tree',commit)
  assert original.resolve().is_relative_to(resolved)
  original.unlink() # Only the rejected private publication duplicate; the immutable scientific original stays on E.
  assert not value('status','--porcelain')
  helpers.watcher.advance_source_index(commit)
  value_receipt={'status':'pushed_and_remote_head_verified','round':148,'at_local':sync.now(),'commit':commit,'branch':'main','remote':sync.REMOTE,
   'official_score':manifest['metrics']['final_score'],'scored_records':242,'connected_records':14957,
   'raw_git_blobs_verified':len(actual),'actual_full_QA_version':59,'full_immutable_ranking_and_all_original_QA_preserved':True,
   'original_official_pilot_records_registered':242,'new_quality_scores_by_registration':0,
   'original_full_report_losslessly_chunked':descriptor,'publication_recovery_service':'AdaptiveJointCrossHuber242_round148_full_registration_v7_20261009',
   'scheme_url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/validation_sync/round148'}
  create(receipt,value_receipt);create(OUT/'receipt.json',value_receipt)
  create(folder/'full_registration_execution.json',{'status':'passed','at_local':sync.now(),'existing_official_scores_registered':242,
   'full_rankings_all_original_QA_and_main_publication_completed':True,'recovered_publication_after_prior_actual_full_QA':True,
   'prior_QA_service_failed_only_on_GH001_preserved':str(old),'original_provenance_scope_sha256':sha(folder/'provenance_scope_execution.json'),
   'original_candidate_sealed_two_full_native_independent_CSV_and_cold80_preserved':True,'current_main_commit':commit,
   'scientific_workers_suspended_stopped_or_restarted':0,'new_quality_scores_by_registration':0,'new_native_fits':0,
   'global_goal_or_resource_exhaustion_claimed':False,'test_labels_read':False})
  print(value_receipt,flush=True)
 finally:
  for p in reversed(held):
   if p.is_running():p.resume()
  create(OUT/'recovery_commands_and_idle_release.json',{'commands':commands,'main_idle_resumed_in_finally':True,'scientific_workers_held':0})
if __name__=='__main__':main()
