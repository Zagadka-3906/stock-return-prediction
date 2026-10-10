"""Main-only publication of actual candidate reconstruction and the queued36/173/QA84 flow."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import sys,os,hashlib,gzip
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed()
    paths=[Path(__file__),Path('D:\\3.Study\\数据分析\\赛题五\\analysis\\monitor_fast_optimization_v49_20261010.py'),Path('D:\\3.Study\\数据分析\\赛题五\\analysis\\prepare_stock_rank_embedding_own_sources_v1_20261010.py'),Path('D:\\3.Study\\数据分析\\赛题五\\analysis\\activate_stock_rank_embedding_checkpoint_yield_training_v2_20261010.py'),Path('D:\\3.Study\\数据分析\\赛题五\\analysis\\stock_rank_embedding_own_sources_and_actual_centered_target_admission_v1_20261010.json'),Path('D:\\3.Study\\数据分析\\赛题五\\analysis\\stock_rank_embedding_actual_priority173_runtime_admission_v2_20261010.json'),Path('D:\\3.Study\\数据分析\\赛题五\\analysis\\stock_rank_embedding_native_stage_and_fast17_sources_admission_v1_20261010.json'),Path('D:\\3.Study\\数据分析\\赛题五\\analysis\\actual_stock_rank_embedding_own_training_queue_activation_v2_20261010.json'),Path('D:\\3.Study\\数据分析\\赛题五\\analysis\\actual_stock_rank_embedding_native42_and_fast17_queue_activation_v1_20261010.json'),Path('D:\\3.Study\\数据分析\\赛题五\\analysis\\actual_stock_rank_embedding_small512_restart_location_v1_20261010.json'),Path('D:\\3.Study\\数据分析\\赛题五\\analysis\\admit_existing_stock_rank_stage_and_fast17_v2_20261010.py'),Path('D:\\3.Study\\数据分析\\赛题五\\analysis\\admit_existing_stock_rank_stage_and_fast17_v3_20261010.py'),Path('D:\\3.Study\\数据分析\\赛题五\\analysis\\admit_existing_stock_rank_stage_and_fast17_v4_20261010.py'),Path('D:\\3.Study\\数据分析\\赛题五\\analysis\\prepare_stock_rank_stage_and_fast17_v1_20261010.py'),Path('D:\\3.Study\\数据分析\\赛题五\\analysis\\run_stock_rank_embedding_after170_fast17_screen_v1_20261010.py'),Path('D:\\3.Study\\数据分析\\赛题五\\analysis\\run_stock_rank_embedding_native42_and_fast17_queue_v1_20261010.py'),Path('D:\\3.Study\\数据分析\\赛题五\\analysis\\run_stock_rank_embedding_own_training_queue_v2_20261010.py'),Path('D:\\3.Study\\数据分析\\赛题五\\analysis\\stock_rank_embedding_after_complete_qualified_parent_native_stage_v1_20261010.py'),Path('D:\\3.Study\\数据分析\\赛题五\\analysis\\stock_rank_embedding_mature_population_v1_20261010.py'),Path('D:\\3.Study\\数据分析\\赛题五\\analysis\\stock_rank_embedding_saved_tensor_decoder_v1_20261010.py'),Path('D:\\3.Study\\数据分析\\赛题五\\analysis\\stock_rank_embedding_small512_BF16_native_v1_20261010.py'),Path('D:\\3.Study\\数据分析\\赛题五\\analysis\\train_stock_rank_embedding_small512_BF16_bank6_checkpoint_yield_priority173_v2_20261010.py'),Path('D:\\3.Study\\数据分析\\赛题五\\analysis\\train_stock_rank_embedding_small512_BF16_bank6_checkpoint_yield_v1_20261010.py'),Path('D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_stock_rank_embedding_six_state_native42_v1_20261010.py'),Path('D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_stock_rank_embedding_small512_full5_independent_v1_20261010.py'),Path('D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_stock_rank_embedding_small512_restart_priority173_v2_20261010.py'),Path('D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_stock_rank_embedding_small512_restart_v1_20261010.py'),Path('D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_stock_rank_embedding_small512_small_CPU_v1_20261010.py'),Path('E:\\赛题五_本机临时\\GPU实测_20261009\\stock_rank_embedding_small512_restart_v1_20261010\\verification.json')]
    import publish_classifier_consensus_workflows_20261006 as h
    prefix=Path('validation_sync/StockRankEmbedding_actual_restart_and_predeclared17_v36_20261010');payload={};bindings={}
    for p in dict.fromkeys(paths):
        raw=p.read_bytes();assert not h.sync.SECRET.search(raw),p
        digest=hashlib.sha256(raw).hexdigest();rel=p.relative_to(ROOT) if p.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+p.name)
        name=(prefix/rel).as_posix();data=raw
        if len(data)>=5*1024**2:data=gzip.compress(data,mtime=0);name+='.gz';assert gzip.decompress(data)==raw
        assert len(data)<95*1024**2;payload[name]=data;bindings[str(p)]={'path':name,'raw_sha256':digest}
    payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({'status':'passed_actual_centered_rank_restart_controls_and_predeclared17_TRAIN_screen_six_fits_full5_native42_pending','files':bindings,'best_actual_stock_screen_S':.4513497468277574,'full173_future_candidate_submission_qualification_pending':True,'new_quality_scores_by_publication':0,'test_labels_read':False,'deadline_local':read(A/'current_user_runtime_control_20261010.json')['stop_at_local']})
    out=Path('E:/赛题五_本机临时/StockRankEmbedding_actual_restart_and_predeclared17_main_v36_20261010');out.mkdir(exist_ok=False)
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
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','保存股票排名目标嵌入模型真实断点恢复验证、训练来源与17项训练集评分对照；六年度训练和完整独立推理验证持续执行',timeout=180)
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
