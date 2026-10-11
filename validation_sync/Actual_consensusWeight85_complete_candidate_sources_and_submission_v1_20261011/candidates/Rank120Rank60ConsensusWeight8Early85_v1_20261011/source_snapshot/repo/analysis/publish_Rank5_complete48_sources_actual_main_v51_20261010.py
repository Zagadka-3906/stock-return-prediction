"""Main-only publication of actual candidate reconstruction and the queued36/173/QA84 flow."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import sys,os,hashlib,gzip
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed()
    paths=[Path(__file__),*[A/n for n in ['prepare_StockRank5Embedding177_complete48_pipeline_v1_20261010.py', 'prepare_stock_rank5_large29_and_complete48_plan_v1_20261010.py', 'stock_rank5_embedding177_candidate_sources_preparation_v2_20261010.json', 'stock_rank5_embedding177_full_registry_sources_preparation_v2_20261010.json', 'stock_rank5_embedding177_full_execution_sources_admission_v2_20261010.json', 'run_StockRank5Embedding177_complete_family_v2_20261010.py', 'run_StockRank5Embedding177_full_registration_v2_20261010.py', 'verify_StockRank5Embedding177_full48_preflight_v2_20261010.py', 'publish_stock_rank5_embedding_after171_large29_completion_v65_20261010.py', 'monitor_fast_optimization_v63_20261010.py', 'activate_Rank5_complete48_main51_and_live63_v1_20261010.py', 'register_StockRank5Embedding177_round177_artifacts_v2_20261010.py', 'publish_StockRank5Embedding177_round177_full_validation_v2_20261010.py', 'optimize_training_round177.py', 'finalize_training_round177.py', 'lossless_ranking_runtime_adapter_round177_v2_20261008.py', 'build_lossless_ranking_display_round177_v2_20261008.py', 'verify_lossless_ranking_display_round177_v2_20261008.py', 'collect_full_lossless_round177_qa88_20261010.py', 'prepare_StockRank5Embedding177_selected_candidate_v2_20261010.py', 'seal_StockRank5Embedding177_selected_candidate_v1_20261010.py', 'stock_rank5_embedding177_storage_v1_20261010.py', 'normalize_completed_stock_rank5_embedding_complete48_after176_v2_20261010.py', 'qualify_stock_rank5_embedding48_selected_native14_v2_20261010.py', 'stock_rank5_embedding_complete48_after176_selection_plan_v1_20261010.json', 'run_stock_rank5_embedding_after171_large_allocation29_screen_v1_20261010.py', 'predict_stock_rank5_embedding_complete_qualified_parent_scheme_v1_20261010.py', 'stock_rank5_embedding_actual_eight_parent_callbacks_CPU_controls_v1_20261010.json', 'stock_rank5_embedding_native_stage_and_fast17_sources_admission_v1_20261010.json']]]
    import publish_classifier_consensus_workflows_20261006 as h
    prefix=Path('validation_sync/StockRank5Embedding_complete48_sources_v51_20261010');payload={};bindings={}
    for p in dict.fromkeys(paths):
        raw=p.read_bytes();assert not h.sync.SECRET.search(raw),p
        digest=hashlib.sha256(raw).hexdigest();rel=p.relative_to(ROOT) if p.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+p.name)
        name=(prefix/rel).as_posix();data=raw
        if len(data)>=5*1024**2:data=gzip.compress(data,mtime=0);name+='.gz';assert gzip.decompress(data)==raw
        assert len(data)<95*1024**2;payload[name]=data;bindings[str(p)]={'path':name,'raw_sha256':digest}
    payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({'status':'compiled_rank5_e64_complete48_normalizer_selected14_candidate_freeze_two_replay_registry_QA88_main_sources_actual17_and29_scoring_pending','files':bindings,'rank5_quality_improvement_not_yet_established':True,'full177_future_candidate_submission_qualification_pending':True,'new_quality_scores_by_publication':0,'test_labels_read':False,'deadline_local':read(A/'current_user_runtime_control_20261010.json')['stop_at_local']})
    out=Path('E:/赛题五_本机临时/StockRank5Embedding_complete48_sources_main_v51_20261010');out.mkdir(exist_ok=False)
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
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','保存股票身份五日排名64轮模型的48项选优、14原生因果检查、冻结后两次完整推理、QA88及main来源；分数与未来候选待实际验证',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()};assert h.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);h.verify_main(commit);h.watcher.advance_source_index(commit)
            receipt={'status':'pushed_and_remote_head_verified','branch':'main','commit':commit,'raw_git_blobs_verified':len(hashes),'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()}
            create(out/'receipt.json',receipt);create(A/'StockRank5Embedding_complete48_sources_main_receipt_v51_20261010.json',receipt);print(receipt,flush=True)
        finally:
            for p in (parent,worker):
                if p.is_running():p.resume()
if __name__=='__main__':
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(key,value) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=key;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=value
    os.environ['GIT_CONFIG_COUNT']=str(count+2);main()
