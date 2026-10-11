from pathlib import Path
import sys,os,time
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def main():
 assert allowed();proof=read(A/'actual187_publication_only_resume47_sources_admission_v1_20261011.json')
 for p,d in proof['input_sha256'].items():assert sha(p)==d,p
 folder=A/'optimization_20261003_r187';scope=read(folder/'provenance_scope_execution.json');assert scope['status']=='passed'
 for p,d in scope['input_sha256'].items():assert sha(p)==d,p
 native=read(A/'shared_live_ranking_report_round187_execution_v1_20261011.json');assert sha(ROOT/'results/all_model_rankings_20261003.json')==native['native_sha256']
 import psutil
 while psutil.virtual_memory().available<11*2**30:assert allowed();time.sleep(10)
 log=Path('E:/赛题五_本机临时/第187轮_20261010/publication_only_resume47_v1_20261011');log.mkdir(exist_ok=False)
 from lossless_chunked_safe_main_runtime_v1_20261009 import installed as safe
 from serial_main_publication_mutex_v1_20261009 import installed as serial
 from verified_TLS_Git_retry_runtime_v3_20261010 import installed as git_io
 from owned_idle_publication_wait_reboot_identity_v2_20261011 import hold
 from byte_exact_publication_encoder_runtime_v1_20261010 import installed as encode
 with serial(log/'serial_mutex.json') as mutex,safe(log/'safe'),git_io(log/'file_backed_git'),encode():
  mutex.acquire();assert allowed();parent,worker,idle=hold(read(A/'service_owned_workflows_20261006/main_publisher_reboot_v12_20261011/native_launch.json'),'    main (watch_validations_main_v7_20261006.py:71)')
  try:
   assert sha(ROOT/'results/all_model_rankings_20261003.json')==native['native_sha256']
   from publish_Rank20TwoSeed187_round187_full_validation_v3_20261011 import main as publish
   publish();receipt=read(A/'github_validation_sync_main_20261005/round187_receipt.json')
   assert receipt['status']=='pushed_and_remote_head_verified' and (receipt['scored_records'],receipt['connected_records'])==(88,17490)
   create(folder/'full_registration_execution.json',{'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'existing_official_scores_registered':88,'full_rankings_all_original_QA_and_main_publication_completed':True,'new_quality_scores_by_registration':0,'selected_candidate_actual_new_inference':read(A/'Rank20TwoSeed187_selected_release_v1_20261010/selected_candidate_ready_for_registration.json')['new_inference_claimed'],'completed_native_QA_provenance_reused_exactly':True,'actual_service':'actual187_completed_QA_publication_only_resume47_v1_20261011','original45_failure_retained':True,'test_labels_read':False})
  finally:
   for p in (parent,worker):
    if p.is_running():p.resume()
 from maintain_best_fully_qualified_submission_delivery_v4_20261011 import update
 update();create(log/'passed.json',{'status':'passed_existing_actual187_QA_and_sources_main_and_full_registration','receipt':receipt,'new_fits_or_scores':0})

if __name__=='__main__':
 count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
 for i,(k,v) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=k;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=v
 os.environ['GIT_CONFIG_COUNT']=str(count+2)
 from types import SimpleNamespace
 from late_bound_shared_snapshot_encoder_runtime_v1_20261011 import installed
 receiver=SimpleNamespace(main=main)
 with installed(receiver,'publish_Rank20TwoSeed187_round187_full_validation_v3_20261011',Path('E:/赛题五_本机临时/第187轮_20261010/late_snapshot_encoder_resume47.json')):receiver.main()
