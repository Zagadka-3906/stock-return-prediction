"""Publish the verified148 tree with lossless16MiB report chunks, excluding rejected history."""
from pathlib import Path
import sys,os,time,subprocess,json,hashlib,gzip,io
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
OUT=Path('E:/赛题五_本机临时/round148_chunked_main_recovery_v1_20261009')
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
 def git(*args,data=None,isolated=False,timeout=180):
  r=subprocess.run(['git',*args],cwd=work,input=data,capture_output=True,env=env if isolated else None,
   timeout=timeout,creationflags=subprocess.CREATE_NO_WINDOW)
  commands.append({'arguments':list(args),'exit_code':r.returncode})
  assert r.returncode==0,r.stderr.decode('utf8',errors='replace')[-3000:]
  return r.stdout
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
  rejected=value('rev-parse','HEAD');remote=value('ls-remote','origin','refs/heads/main').split()[0]
  assert value('rev-parse',rejected+'^')==remote
  assert not value('status','--porcelain')
  previous_tree=tree(rejected);prefix='validation_sync/round148/'
  large=prefix+'complete_ranking_display/lossless_ranking_display_v2_20261006/round148/full_report_reconstructed_for_publication.json.gz'
  original=work/large;data=original.read_bytes();digest=hashlib.sha256(data).hexdigest()
  assert len(data)>100*1024**2
  assert sha(A/'lossless_ranking_display_v2_20261006/round148/full_report_reconstructed_for_publication.json.gz')==digest
  manifest_path=prefix+'manifest.json';manifest=read(work/manifest_path)
  assert manifest['exported_files'][large]['sha256']==digest
  assert manifest['scored_records']==242 and manifest['connected_records']==14957
  original_info=manifest['exported_files'][large]
  raw_sha=hashlib.sha256();raw_size=0
  with gzip.GzipFile(fileobj=io.BytesIO(data)) as stream:
   while block:=stream.read(4*1024**2):raw_sha.update(block);raw_size+=len(block)
  assert raw_sha.hexdigest()==manifest['original_full_ranking_sha256']
  git('read-tree',rejected,isolated=True);git('update-index','--force-remove','--',large,isolated=True)
  added={};parts=[]
  for offset in range(0,len(data),16*1024**2):
   chunk=data[offset:offset+16*1024**2];name=large+f'.part{len(parts):03d}'
   added[name]=chunk;parts.append({'path':Path(name).name,'bytes':len(chunk),'sha256':hashlib.sha256(chunk).hexdigest()})
  assembled=b''.join(added[large+f'.part{i:03d}'] for i in range(len(parts)))
  assert assembled==data and hashlib.sha256(assembled).hexdigest()==digest
  descriptor={'status':'lossless_chunked_original_gzip','original_filename':Path(large).name,'compressed_bytes':len(data),
   'compressed_sha256':digest,'original_report_bytes':raw_size,'original_report_sha256':raw_sha.hexdigest(),'parts':parts,
   'rejected_unpublished_commit':rejected,'remote_parent':remote,'original_scientific_QA_unchanged':True}
  descriptor_name=large+'.parts.json';added[descriptor_name]=sync.encoded(descriptor)
  reconstruct='''from pathlib import Path\nimport json,hashlib\np=Path(__file__).parent\nm=json.loads((p/'full_report_reconstructed_for_publication.json.gz.parts.json').read_text(encoding='utf8'))\nout=p/m['original_filename']\nassert not out.exists()\nh=hashlib.sha256();size=0\nwith out.open('xb') as f:\n for item in m['parts']:\n  data=(p/item['path']).read_bytes()\n  assert len(data)==item['bytes'] and hashlib.sha256(data).hexdigest()==item['sha256']\n  f.write(data);h.update(data);size+=len(data)\nassert size==m['compressed_bytes'] and h.hexdigest()==m['compressed_sha256']\nprint(out)\n'''
  added=strict_added=added
  added[str(Path(large).parent/'reconstruct_full_report.py')]=reconstruct.encode()
  del manifest['exported_files'][large]
  manifest['chunked_original_artifacts']={large:{**original_info,'descriptor':descriptor_name,'parts':parts,'reassembled_original_bytes_exact':True}}
  manifest['publication_recovery']={'reason':'GitHub GH001 compressed_report_over100MiB','rejected_unpublished_commit':rejected,
   'remote_parent':remote,'chunk_size':16*1024**2,'original_full_six_view_QA_not_rerun_or_changed':True,
   'original_candidate_inference_and_all242_scores_unchanged':True}
  for name,blob in added.items():manifest['exported_files'][name]={'bytes':len(blob),'sha256':hashlib.sha256(blob).hexdigest()}
  added[manifest_path]=sync.encoded(manifest)
  for name,blob in added.items():
   target=work/name;target.parent.mkdir(parents=True,exist_ok=True)
   with target.open('wb') as f:f.write(blob)
   object_id=value('hash-object','-w','--stdin',data=blob)
   git('update-index','--add','--cacheinfo','100644',object_id,name,isolated=True)
  new_tree=value('write-tree',isolated=True)
  commit=value('commit-tree',new_tree,'-p',remote,data='登记第148轮242项完整评分与六视图验证，原始大报告分块无损保留\n'.encode())
  actual=tree(commit)
  assert all(actual[name]==item for name,item in previous_tree.items() if name not in (large,manifest_path))
  assert large not in actual and set(actual)==(set(previous_tree)-{large})|set(added)
  expected={n:hashlib.sha256(b).hexdigest() for n,b in added.items()};assert helpers.blob_hashes(commit,expected)==expected
  create(OUT/'before_remote_push.json',{'status':'original148_scientific_tree_preserved_except_lossless_transport_chunking',
   'rejected_commit':rejected,'new_commit':commit,'remote_parent':remote,'descriptor':descriptor,
   'unchanged_original_blob_count':len(previous_tree)-2,'new_artifact_blobs':expected,'primary_root_index_untouched':True})
  git('push','origin',commit+':refs/heads/main',timeout=300)
  assert value('ls-remote','origin','refs/heads/main').split()[0]==commit
  git('update-ref','refs/heads/main',commit,rejected);git('read-tree',commit)
  assert original.resolve().is_relative_to(resolved)
  original.unlink() # Only the rejected private publication duplicate; the immutable scientific original stays on E.
  assert not value('status','--porcelain')
  helpers.watcher.advance_source_index(commit)
  value_receipt={'status':'pushed_and_remote_head_verified','round':148,'at_local':sync.now(),'commit':commit,'branch':'main','remote':sync.REMOTE,
   'official_score':manifest['metrics']['final_score'],'scored_records':242,'connected_records':14957,
   'raw_git_blobs_verified':len(actual),'actual_full_QA_version':59,'full_immutable_ranking_and_all_original_QA_preserved':True,
   'original_official_pilot_records_registered':242,'new_quality_scores_by_registration':0,
   'original_full_report_losslessly_chunked':descriptor,'publication_recovery_service':'AdaptiveJointCrossHuber242_round148_full_registration_v3_20261009',
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
