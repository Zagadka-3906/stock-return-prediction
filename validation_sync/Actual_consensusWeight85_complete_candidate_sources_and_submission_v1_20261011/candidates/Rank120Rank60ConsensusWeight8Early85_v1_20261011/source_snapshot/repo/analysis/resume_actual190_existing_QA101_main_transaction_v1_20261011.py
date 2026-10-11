from pathlib import Path
import sys,hashlib,os
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def main():
 assert allowed()
 import publish_classifier_consensus_workflows_20261006 as h
 sync=h.sync;wt=sync.WORKTREE;mf=wt/'validation_sync/round190/manifest.json';manifest=read(mf)
 assert manifest['scored_records']==39 and manifest['connected_records']==17726 and manifest['actual_complete_QA_version']==101
 assert manifest['immutable_all_values_lossless_display_and_complete_original_QA_published']
 prov=A/'optimization_20261003_r190/provenance_scope_execution.json';assert read(prov)['status']=='passed'
 q=A/'lossless_ranking_display_qa_v101_20261010/round190/qa/interaction_result.json';qa=read(q)
 assert qa.get('status')=='passed',qa.get('status')
 out=Path('E:/赛题五_本机临时/Actual190_completed_QA101_resume_main_v1_20261011');out.mkdir(exist_ok=False)
 from serial_main_publication_mutex_v1_20261009 import installed as serial
 from verified_TLS_Git_retry_runtime_v3_20261010 import installed as git_io
 from owned_idle_publication_wait_reboot_dynamic_boundary_v3_20261011 import hold
 with serial(out/'serial_mutex.json') as mutex,git_io(out/'file_backed_git'):
  mutex.acquire();assert allowed()
  parent,worker,idle=hold(read(A/'service_owned_workflows_20261006/main_publisher_reboot_v12_20261011/native_launch.json'),'    main (watch_validations_main_v7_20261006.py:71)')
  try:
   h.verify_main(sync.git('rev-parse','HEAD'))
   hashes={n:v['sha256'] for n,v in manifest['exported_files'].items()}
   hashes['validation_sync/round190/manifest.json']=sha(mf)
   latest=wt/'validation_sync/latest.json';assert read(latest)['round']==190 and read(latest)['connected_records']==17726
   hashes['validation_sync/latest.json']=sha(latest)
   for n,d in hashes.items():assert sha(wt/n)==d,n
   create(out/'verified_existing_payload_before_resume.json',{'status':'all_existing_original_payload_SHA256_verified_after_disk_failure_original_QA_not_rerun','files':hashes,'provenance_sha256':sha(prov),'QA_sha256':sha(q),'new_scores':0,'new_inference':0})
   staged=set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines());assert staged<=set(hashes)
   names=sorted(hashes)
   for i in range(0,len(names),50):assert allowed();sync.git('add','-f','--',*names[i:i+50])
   staged=set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines());assert staged and staged<=set(hashes)
   sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','恢复第190轮已完成39项官方验证与17726条完整榜QA101：原始字节全量核验后main提交',timeout=190)
   commit=sync.git('rev-parse','HEAD');assert h.blob_hashes(commit,hashes)==hashes
   sync.git('push','origin','HEAD:refs/heads/main',timeout=190);h.verify_main(commit);h.watcher.advance_source_index(commit)
   receipt={'status':'pushed_and_remote_head_verified','round':190,'at_local':sync.now(),'commit':commit,'branch':'main','remote':sync.REMOTE,'official_score':manifest['metrics']['final_score'],'scored_records':39,'connected_records':17726,'raw_git_blobs_verified':len(hashes),'actual_full_QA_version':101,'full_immutable_ranking_and_all_original_QA_preserved':True,'original_official_pilot_records_registered':39,'new_quality_scores_by_registration':0,'scheme_url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/validation_sync/round190','actual_disk_failure_recovery_evidence':str(out)}
   create(A/'github_validation_sync_main_20261005/round190_receipt.json',receipt);create(out/'receipt.json',receipt)
   create(A/'optimization_20261003_r190/full_registration_execution_recovery65_v1_20261011.json',{'status':'passed','original_full_QA_and_provenance':str(prov),'main_receipt':receipt,'original_failed_services_preserved':True,'new_scientific_scores':0,'new_inference':0})
   print(receipt,flush=True)
  finally:
   for proc in (parent,worker):
    if proc.is_running():proc.resume()
if __name__=='__main__':
 c=int(os.environ.get('GIT_CONFIG_COUNT','0'))
 for i,(k,v) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{c+i}']=k;os.environ[f'GIT_CONFIG_VALUE_{c+i}']=v
 os.environ['GIT_CONFIG_COUNT']=str(c+2);main()
