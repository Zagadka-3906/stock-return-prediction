"""Main-only publication of actual candidate reconstruction and the queued36/173/QA84 flow."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import sys,os,hashlib,gzip
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed()
    paths=[Path(p) for p in ['D:\\3.Study\\数据分析\\赛题五\\analysis\\prepare_flag17_sources_main_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\prepare_flag17_raw_completed_records_main_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\run_publish_rank60_flag17_after183_completed17_main_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\rank60_flag17_raw_sources_predeclared_v1_20261011.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\prepare_rank60_flag17_raw_and_gain_candidate_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\run_stock_rank60_embedding_after183_direct_allocation33_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\run_rank60_flag17_after183_direct17_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_stock_rank60medium_best33_native14_v2_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\prepare_StockRank60MediumBest33Early_selected_candidate_v2_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\run_StockRank60MediumBest33Early_selected_candidate_feature_cache_v2_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\seal_StockRank60MediumBest33Early_selected_candidate_v2_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\seal_StockRank60MediumBest33Early_selected_candidate_v3_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\stock_rank60medium_best33_early_storage_v2_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\rank60medium2048_early_candidate_recipes_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\run_rank60medium2048_gain_selected_full_candidate_queue_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\publish_actual_rank60medium2048_best33_complete_candidate_main_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\prepare_verified_rank60medium2048_best33_alternate_submission_delivery_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_stock_rank60_flag17_native14_v2_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\prepare_StockRank60FlagOnlyBest17Early_selected_candidate_v2_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\run_StockRank60FlagOnlyBest17Early_selected_candidate_feature_cache_v2_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\seal_StockRank60FlagOnlyBest17Early_selected_candidate_v2_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\seal_StockRank60FlagOnlyBest17Early_selected_candidate_v3_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\stock_rank60_flag17_early_storage_v2_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\rank60_flag17_early_candidate_recipes_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\run_rank60_flag17_gain_selected_full_candidate_queue_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\publish_actual_rank60_flag17_best17_complete_candidate_main_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\prepare_verified_rank60_flag17_best17_alternate_submission_delivery_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\stock_rank60_actual_twelve_parent183_callbacks_CPU_controls_v2_20261011.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\actual_StockRank60EmbeddingSmall512_full5_independent_location_v1_20261011.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\rank60_flag17_best17_full_candidate_sources_admission_v1_20261011.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\rank60_flag17_actual_runtime_import_admission_v1_20261011.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\flag17_exact_existing_controller_aliases_admission_v1_20261011.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_flag17_exact_existing_controller_aliases_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\service_owned_workflows_20261006\\actual_stock_rank60_flag17_after183_direct17_v1_20261011\\native_launch.json']]
    import publish_classifier_consensus_workflows_20261006 as h
    prefix=Path('validation_sync/Actual_flag17_frozen_sources_v1_20261011');payload={};bindings={}
    for p in dict.fromkeys(paths):
        raw=p.read_bytes();assert not h.sync.SECRET.search(raw),p
        digest=hashlib.sha256(raw).hexdigest();rel=p.relative_to(ROOT) if p.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+p.name)
        name=(prefix/rel).as_posix();data=raw
        if len(data)>=5*1024**2:data=gzip.compress(data,mtime=0);name+='.gz';assert gzip.decompress(data)==raw
        assert len(data)<95*1024**2;payload[name]=data;bindings[str(p)]={'path':name,'raw_sha256':digest}
    payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({'status':'actual9_flag_only17_runtime_module_imports_and_exact_actual_controller_aliases_passed_existing_small512_bank_reused_full16_prefix48_scoring_and_gain_only_native14_complete36_cold80_pipeline_predeclared_no_science_claim','new_scientific_scores_claimed_by_publication':0,'all_actual_scientific_assertions_retained':True,'selected_future_qualification_pending':True,'test_labels_read':False,'files':bindings})
    out=Path('E:/赛题五_本机临时/Actual_flag17_frozen_sources_main_v1_20261011');out.mkdir(exist_ok=False)
    create(out/'frozen_before_publication.json',{'files':bindings})
    from lossless_chunked_safe_main_runtime_v1_20261009 import installed as safe
    from serial_main_publication_mutex_v1_20261009 import installed as serial
    from verified_TLS_Git_retry_runtime_v3_20261010 import installed as git_io
    from owned_idle_publication_wait_reboot_dynamic_boundary_v3_20261011 import hold
    with serial(out/'serial_mutex.json') as mutex,safe(out/'safe'),git_io(out/'file_backed_git'):
        mutex.acquire();assert allowed()
        parent,worker,idle=hold(read(A/'service_owned_workflows_20261006/main_publisher_reboot_v12_20261011/native_launch.json'),'    main (watch_validations_main_v7_20261006.py:71)')
        try:
            sync=h.sync;h.verify_main(sync.git('rev-parse','HEAD'));assert not sync.git('status','--porcelain')
            for name,data in payload.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(payload)
            for i in range(0,len(names),50):sync.git('add','-f','--',*names[i:i+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','冻结涨停股排序17项新方案；复用已核验512模型，官方全量及因果对照、提分后完整36模型核验保留',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()};assert h.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);h.verify_main(commit);h.watcher.advance_source_index(commit)
            receipt={'status':'pushed_and_remote_head_verified','branch':'main','commit':commit,'raw_git_blobs_verified':len(hashes),'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()}
            create(out/'receipt.json',receipt);create(A/'Actual_flag17_frozen_sources_main_receipt_v1_20261011.json',receipt);print(receipt,flush=True)
        finally:
            for p in (parent,worker):
                if p.is_running():p.resume()
if __name__=='__main__':
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(key,value) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=key;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=value
    os.environ['GIT_CONFIG_COUNT']=str(count+2);main()
