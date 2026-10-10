"""Main-only publication of actual candidate reconstruction and the queued36/173/QA84 flow."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import sys,os,hashlib,gzip
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed()
    from prepare_stock_embedding173_full_registry_sources_v2_20261010 import source_paths
    proof=A/'stock_embedding173_actual_local_import_and_scalar_routes_admission_v4_20261010.json'
    controls=A/'stock_embedding173_actual_candidate_TRAIN_reconstruction_CPU_controls_v1_20261010.json'
    assert read(proof)['status'].startswith('passed') and read(controls)['status'].startswith('passed')
    for p,d in read(controls)['input_sha256'].items():assert sha(p)==d,p
    paths=[Path(__file__),*source_paths(),proof,controls,A/'admit_and_activate_StockEmbedding173_actual_full_pipeline_v3_20261010.py',A/'admit_existing_StockEmbedding173_full_pipeline_v4_20261010.py',A/'verify_StockEmbedding173_actual_candidate_TRAIN_reconstruction_v1_20261010.py',A/'stock_embedding173_actual_execution_routes_admission_v2_20261010.json',A/'run_StockEmbedding173_complete_family_v3_20261010.py',A/'run_StockEmbedding173_full_registration_v3_20261010.py',A/'verify_StockEmbedding173_full36_preflight_v3_20261010.py',A/'actual_StockEmbedding173_complete36_family_activation_v3_20261010.json',A/'actual_stock_embedding36_after172_normalization_activation_v1_20261010.json',A/'actual_stock_embedding36_selected_native14_activation_v1_20261010.json',A/'stock_embedding17_after170_completion_main_receipt_v53_20261010.json',A/'stock_embedding173_full_registry_sources_preparation_v2_20261010.json']
    import publish_classifier_consensus_workflows_20261006 as h
    prefix=Path('validation_sync/StockEmbedding173_actual_complete_pipeline_preparation_v35_20261010');payload={};bindings={}
    for p in dict.fromkeys(paths):
        raw=p.read_bytes();assert not h.sync.SECRET.search(raw),p
        digest=hashlib.sha256(raw).hexdigest();rel=p.relative_to(ROOT) if p.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+p.name)
        name=(prefix/rel).as_posix();data=raw
        if len(data)>=5*1024**2:data=gzip.compress(data,mtime=0);name+='.gz';assert gzip.decompress(data)==raw
        assert len(data)<95*1024**2;payload[name]=data;bindings[str(p)]={'path':name,'raw_sha256':digest}
    payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({'status':'passed_actual4_TRAIN_candidate_transform_cases_and_full5635800_winner_reconstruction_266_local_import_routes_complete36_selected14_and_full173_QA84_main_queued','files':bindings,'best_actual_stock_screen_S':.4513497468277574,'full173_future_candidate_submission_qualification_pending':True,'new_quality_scores_by_publication':0,'test_labels_read':False,'deadline_local':read(A/'current_user_runtime_control_20261010.json')['stop_at_local']})
    out=Path('E:/赛题五_本机临时/StockEmbedding173_actual_complete_pipeline_preparation_main_v35_20261010');out.mkdir(exist_ok=False)
    create(out/'frozen_before_publication.json',{'files':bindings})
    from lossless_chunked_safe_main_runtime_v1_20261009 import installed as safe
    from serial_main_publication_mutex_v1_20261009 import installed as serial
    from verified_TLS_Git_retry_runtime_v3_20261010 import installed as git_io
    from owned_idle_publication_wait_runtime_v1_20261010 import hold
    with serial(out/'serial_mutex.json') as mutex,safe(out/'safe'),git_io(out/'file_backed_git'):
        mutex.acquire();assert allowed()
        parent,worker,idle=hold(read(A/'service_owned_workflows_20261006/main_publisher_v11_20261010/native_launch.json'),'    main (watch_validations_main_v7_20261006.py:71)')
        try:
            sync=h.sync;h.verify_main(sync.git('rev-parse','HEAD'));assert not sync.git('status','--porcelain')
            for name,data in payload.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(payload)
            for i in range(0,len(names),50):sync.git('add','-f','--',*names[i:i+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','保存股票嵌入提分方案真实5635800行训练预测逐位重建、266条本地模块路由检查，以及36比较到完整173冻结推理QA84主分支发布流程',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()};assert h.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);h.verify_main(commit);h.watcher.advance_source_index(commit)
            receipt={'status':'pushed_and_remote_head_verified','branch':'main','commit':commit,'raw_git_blobs_verified':len(hashes),'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()}
            create(out/'receipt.json',receipt);create(A/'StockEmbedding173_actual_complete_pipeline_preparation_main_receipt_v35_20261010.json',receipt);print(receipt,flush=True)
        finally:
            for p in (parent,worker):
                if p.is_running():p.resume()
if __name__=='__main__':
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(key,value) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=key;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=value
    os.environ['GIT_CONFIG_COUNT']=str(count+2);main()
