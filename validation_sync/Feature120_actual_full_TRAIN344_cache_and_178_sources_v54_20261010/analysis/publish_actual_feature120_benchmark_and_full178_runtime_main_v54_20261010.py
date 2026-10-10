"""Main-only publication of actual candidate reconstruction and the queued36/173/QA84 flow."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import sys,os,hashlib,gzip
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed()
    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import closed
    closed('actual_full178_feature_cache_benchmark_admission_queue_v3_20261010')
    pointer=A/'actual_feature120_verified_memoization_TRAIN344_location_v1_20261010.json'
    actual=Path(read(pointer)['output']);benchmark=read(actual/'verification.json')
    paths=[Path(__file__),pointer,*actual.glob('*.json'),*[A/n for n in ['activate_actual_feature_cache_main54_and_live66_v1_20261010.py', 'exact_verified_feature120_memoization_runtime_v1_20261010.py', 'benchmark_exact_feature120_memoization_actual_TRAIN344_v1_20261010.py', 'run_StockForward5Embedding178_selected_candidate_feature_cache_v3_20261010.py', 'admit_full178_feature_cache_after_actual_benchmark_v3_20261010.py', 'monitor_fast_optimization_v66_20261010.py', 'actual_feature120_verified_memoization_TRAIN344_activation_v1_20261010.json', 'actual_full178_feature_cache_benchmark_admission_queue_activation_v3_20261010.json']]]
    for n in ('stock_forward5_embedding178_feature_cache_sources_admission_v3_20261010.json','stock_forward5_embedding178_feature_cache_not_adopted_v3_20261010.json','run_StockForward5Embedding178_complete_family_v3_20261010.py','actual_StockForward5Embedding178_complete48_family_feature_cache_activation_v3_20261010.json'):
        if (A/n).exists():paths.append(A/n)
    import publish_classifier_consensus_workflows_20261006 as h
    prefix=Path('validation_sync/Feature120_actual_full_TRAIN344_cache_and_178_sources_v54_20261010');payload={};bindings={}
    for p in dict.fromkeys(paths):
        raw=p.read_bytes();assert not h.sync.SECRET.search(raw),p
        digest=hashlib.sha256(raw).hexdigest();rel=p.relative_to(ROOT) if p.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+p.name)
        name=(prefix/rel).as_posix();data=raw
        if len(data)>=5*1024**2:data=gzip.compress(data,mtime=0);name+='.gz';assert gzip.decompress(data)==raw
        assert len(data)<95*1024**2;payload[name]=data;bindings[str(p)]={'path':name,'raw_sha256':digest}
    payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({'status':'passed_actual1599600_TRAIN_feature120_native_Pandas_full_and_cold80_benchmark_conditional_idle178_runtime_admission_no_model_math_changed','files':bindings,'actual_benchmark':benchmark,'new_quality_scores':0,'full177_future_candidate_submission_qualification_pending':True,'new_quality_scores_by_publication':0,'test_labels_read':False,'deadline_local':read(A/'current_user_runtime_control_20261010.json')['stop_at_local']})
    out=Path('E:/赛题五_本机临时/Feature120_actual_full_TRAIN344_cache_and_178_sources_main_v54_20261010');out.mkdir(exist_ok=False)
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
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','保存实际1599600行TRAIN特征缓存逐位一致及速度基准，独立Pandas、cold80与输入变更核对；仅基准通过后接入未派发178轮推理',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()};assert h.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);h.verify_main(commit);h.watcher.advance_source_index(commit)
            receipt={'status':'pushed_and_remote_head_verified','branch':'main','commit':commit,'raw_git_blobs_verified':len(hashes),'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()}
            create(out/'receipt.json',receipt);create(A/'Feature120_actual_full_TRAIN344_cache_and_178_sources_main_receipt_v54_20261010.json',receipt);print(receipt,flush=True)
        finally:
            for p in (parent,worker):
                if p.is_running():p.resume()
if __name__=='__main__':
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(key,value) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=key;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=value
    os.environ['GIT_CONFIG_COUNT']=str(count+2);main()
