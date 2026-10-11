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
    closed('StockRankDual174_actual_rank_branch_TRAIN_reconstruction_v1_20261010')
    paths=['D:\\3.Study\\数据分析\\赛题五\\analysis\\publish_fast_Top10_schedule_and_large29_sources_v43_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\publish_stock_top10_verified_loss_and_runtime_main_v42_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\accelerate_independent_Top10_training_schedule_v3_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_stock_top10_embedding_small512_restart_memory_guard_v3_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\train_stock_top10_embedding_small512_BF16_bank6_memory_guard_v3_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\run_stock_top10_embedding_own_training_queue_v3_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\run_stock_top10_embedding_native42_and_after174_fast17_queue_v3_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\stock_top10_independent_training_schedule_admission_v3_20261010.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\actual_stock_top10_independent_training_acceleration_v3_20261010.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\prepare_Top10_large_allocation29_and_fast_runtime_v1_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\run_stock_top10_embedding_after174_large_allocation29_screen_v1_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\predict_stock_top10_embedding_complete_qualified_parent_scheme_v1_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\stock_top10_large_allocation29_predeclared_actual_CPU_admission_v1_20261010.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\publish_stock_top10_embedding_after174_large_allocation29_completion_v60_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\actual_stock_top10_large_allocation29_activation_v1_20261010.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\monitor_fast_optimization_v56_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\actual_fast_optimization_progress_v56_activation_20261010.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\actual_D_historical_reports_lossless_E_relocation_verification_v1_20261010.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\service_owned_workflows_20261006\\actual_stock_top10_embedding_own_training_queue_v3_20261010\\native_launch.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\service_owned_workflows_20261006\\actual_stock_top10_embedding_own_training_queue_v3_20261010\\job_definition.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\service_owned_workflows_20261006\\actual_stock_top10_embedding_native42_and_after174_fast17_queue_v3_20261010\\native_launch.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\service_owned_workflows_20261006\\actual_stock_top10_embedding_native42_and_after174_fast17_queue_v3_20261010\\job_definition.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\service_owned_workflows_20261006\\actual_stock_top10_embedding_after174_large_allocation29_screen_v1_20261010\\native_launch.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\service_owned_workflows_20261006\\actual_stock_top10_embedding_after174_large_allocation29_screen_v1_20261010\\job_definition.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\service_owned_workflows_20261006\\actual_stock_top10_embedding_after174_large_allocation29_completion_main_v60_20261010\\native_launch.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\service_owned_workflows_20261006\\actual_stock_top10_embedding_after174_large_allocation29_completion_main_v60_20261010\\job_definition.json', 'E:\\赛题五_本机临时\\D盘历史报告无损迁移_v1_20261010\\manifest.json', 'E:\\赛题五_本机临时\\D盘历史报告无损迁移_v1_20261010\\historical_reports_batch_v2.json']
    paths=[Path(p) for p in paths]
    import publish_classifier_consensus_workflows_20261006 as h
    prefix=Path('validation_sync/StockTop10Embedding_verified_BCE_loss_and_runtime_v43_20261010');payload={};bindings={}
    for p in dict.fromkeys(paths):
        raw=p.read_bytes();assert not h.sync.SECRET.search(raw),p
        digest=hashlib.sha256(raw).hexdigest();rel=p.relative_to(ROOT) if p.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+p.name)
        name=(prefix/rel).as_posix();data=raw
        if len(data)>=5*1024**2:data=gzip.compress(data,mtime=0);name+='.gz';assert gzip.decompress(data)==raw
        assert len(data)<95*1024**2;payload[name]=data;bindings[str(p)]={'path':name,'raw_sha256':digest}
    payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({'status':'passed_schedule3_independent_Top10_GPU_routes_started_predeclared29_large_CDF_allocation_actual28_TRAIN_codec_controls_full_classifier_scores_pending','files':bindings,'best_actual_stock_screen_S':.4513551448431997,'full173_future_candidate_submission_qualification_pending':True,'new_quality_scores_by_publication':0,'test_labels_read':False,'deadline_local':read(A/'current_user_runtime_control_20261010.json')['stop_at_local']})
    out=Path('E:/赛题五_本机临时/StockTop10Embedding_verified_BCE_loss_and_runtime_main_v43_20261010');out.mkdir(exist_ok=False)
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
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','提前启动独立Top10分类训练，保留内存保护和检查点；预声明29项大权重融合并完成28项真实TRAIN编解码控制，保存D盘历史报告无损迁移记录',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()};assert h.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);h.verify_main(commit);h.watcher.advance_source_index(commit)
            receipt={'status':'pushed_and_remote_head_verified','branch':'main','commit':commit,'raw_git_blobs_verified':len(hashes),'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()}
            create(out/'receipt.json',receipt);create(A/'StockTop10Embedding_verified_BCE_loss_and_runtime_main_receipt_v43_20261010.json',receipt);print(receipt,flush=True)
        finally:
            for p in (parent,worker):
                if p.is_running():p.resume()
if __name__=='__main__':
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(key,value) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=key;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=value
    os.environ['GIT_CONFIG_COUNT']=str(count+2);main()
