"""Main-only publication of actual candidate reconstruction and the queued36/173/QA84 flow."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import sys,os,hashlib,gzip
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed()
    paths=[Path(__file__),*[Path(p) for p in ['D:\3.Study\数据分析\赛题五\analysis\prepare_rank10_real_fixture_and_fast46_sources_main_v1_20261011.py', 'D:\3.Study\数据分析\赛题五\analysis\actual_stock_rank10_embedding_mature_fixture_location_v1_20261011.json', 'E:\赛题五_本机临时\stock_rank10_embedding_mature_fixture_v1_20261011\verification.json', 'D:\3.Study\数据分析\赛题五\analysis\stock_rank10_embedding_actual_restart_and_own6_sources_admission_v1_20261011.json', 'D:\3.Study\数据分析\赛题五\analysis\stock_rank10_embedding_native_stage_and_fast17_sources_admission_v1_20261011.json', 'D:\3.Study\数据分析\赛题五\analysis\rank10_fast46_and_actual183_inner_recovery_dispatch_v1_20261011.json', 'D:\3.Study\数据分析\赛题五\analysis\stock_rank10_embedding_actual_eleven_parent_callbacks_CPU_controls_v1_20261011.json', 'D:\3.Study\数据分析\赛题五\analysis\actual183_completed_inner_inference_rehashed_recovery_v1_20261011.json', 'D:\3.Study\数据分析\赛题五\analysis\verify_stock_rank10_embedding_actual_mature_fixture_v1_20261011.py', 'D:\3.Study\数据分析\赛题五\analysis\verify_stock_rank10_embedding_small512_restart_v1_20261011.py', 'D:\3.Study\数据分析\赛题五\analysis\verify_stock_rank10_embedding_small512_small_CPU_v1_20261011.py', 'D:\3.Study\数据分析\赛题五\analysis\train_stock_rank10_embedding_small512_BF16_bank6_own64_v1_20261011.py', 'D:\3.Study\数据分析\赛题五\analysis\verify_stock_rank10_embedding_small512_full5_independent_v1_20261011.py', 'D:\3.Study\数据分析\赛题五\analysis\run_stock_rank10_embedding_own_training_and_full5_queue_v2_20261011.py', 'D:\3.Study\数据分析\赛题五\analysis\run_stock_rank10_native42_and_fast46_queue_v1_20261011.py', 'D:\3.Study\数据分析\赛题五\analysis\prepare_rank10_fast46_and_actual183_recovery_v1_20261011.py', 'D:\3.Study\数据分析\赛题五\analysis\stock_rank5_embedding_after_complete_qualified_parent_native_stage_v1_20261010.py', 'D:\3.Study\数据分析\赛题五\analysis\verify_stock_rank5_embedding_six_state_native42_v1_20261010.py', 'D:\3.Study\数据分析\赛题五\analysis\run_stock_rank20long_embedding_after175_fast17_screen_v1_20261010.py', 'D:\3.Study\数据分析\赛题五\analysis\run_stock_rank20long_embedding_after175_large_allocation29_screen_v1_20261010.py', 'D:\3.Study\数据分析\赛题五\analysis\predict_stock_rank20_embedding_complete_qualified_parent_scheme_v1_20261010.py', 'D:\3.Study\数据分析\赛题五\analysis\verify_rank5_rank20_mixed_actual_eleven_parent_callbacks_CPU_v1_20261011.py', 'D:\3.Study\数据分析\赛题五\analysis\stock_rank10_embedding_after_complete_qualified_parent_native_stage_v1_20261011.py', 'D:\3.Study\数据分析\赛题五\analysis\verify_stock_rank10_embedding_six_state_native42_v1_20261011.py', 'D:\3.Study\数据分析\赛题五\analysis\run_stock_rank10_embedding_after175_fast17_screen_v1_20261011.py', 'D:\3.Study\数据分析\赛题五\analysis\run_stock_rank10_embedding_after175_large_allocation29_screen_v1_20261011.py', 'D:\3.Study\数据分析\赛题五\analysis\predict_stock_rank10_embedding_complete_qualified_parent_scheme_v1_20261011.py', 'D:\3.Study\数据分析\赛题五\analysis\verify_stock_rank10_embedding_actual_eleven_parent_callbacks_CPU_v1_20261011.py', 'D:\3.Study\数据分析\赛题五\analysis\prepare_stock_rank10_restart_and_own6_v1_20261011.py', 'D:\3.Study\数据分析\赛题五\analysis\verify_stock_rank5_embedding_small512_restart_v1_20261010.py', 'D:\3.Study\数据分析\赛题五\analysis\verify_stock_rank5_embedding_small512_small_CPU_v1_20261010.py', 'D:\3.Study\数据分析\赛题五\analysis\train_stock_rank5_embedding_small512_BF16_bank6_own64_v1_20261010.py', 'D:\3.Study\数据分析\赛题五\analysis\verify_stock_rank5_embedding_small512_full5_independent_v1_20261010.py', 'D:\3.Study\数据分析\赛题五\analysis\recent252_rank10_mature_population_actual_CPU_controls_v2_20261011.json', 'D:\3.Study\数据分析\赛题五\analysis\stock_rank10_embedding_own64_native_sources_preparation_v1_20261011.json']]]
    import publish_classifier_consensus_workflows_20261006 as h
    prefix=Path('validation_sync/Rank10_actual_fixture_callbacks11_fast46_sources_v1_20261011');payload={};bindings={}
    for p in dict.fromkeys(paths):
        raw=p.read_bytes();assert not h.sync.SECRET.search(raw),p
        digest=hashlib.sha256(raw).hexdigest();rel=p.relative_to(ROOT) if p.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+p.name)
        name=(prefix/rel).as_posix();data=raw
        if len(data)>=5*1024**2:data=gzip.compress(data,mtime=0);name+='.gz';assert gzip.decompress(data)==raw
        assert len(data)<95*1024**2;payload[name]=data;bindings[str(p)]={'path':name,'raw_sha256':digest}
    payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({**{'status': 'actual49153_mature_fixture_and11_callbacks_passed_new_rank10_own6_training_sources46_screen_frozen', 'actual_mature_fixture_rows': 49153, 'actual_callback_CPU_checks': 11, 'new_native_fits': 0, 'new_quality_scores': 0, 'actual_GPU_restart_fixture_and_annual_training_pending': True, 'mean10_label_horizon': 10, 'feature120_stockID16_reused_architecture_new_target_not_old_bank_weights': True, 'test_labels_read': False},'files':bindings})
    out=Path('E:/赛题五_本机临时/Rank10_actual_fixture_callbacks11_fast46_sources_main_v1_20261011');out.mkdir(exist_ok=False)
    create(out/'frozen_before_publication.json',{'files':bindings})
    from lossless_chunked_safe_main_runtime_v1_20261009 import installed as safe
    from serial_main_publication_mutex_v1_20261009 import installed as serial
    from verified_TLS_Git_retry_runtime_v3_20261010 import installed as git_io
    from owned_idle_publication_wait_runtime_v1_20261010 import hold
    with serial(out/'serial_mutex.json') as mutex,safe(out/'safe'),git_io(out/'file_backed_git'):
        mutex.acquire();assert allowed()
        parent,worker,idle=hold(read(A/'service_owned_workflows_20261006/main_publisher_reboot_v12_20261011/native_launch.json'),'    main (watch_validations_main_v7_20261006.py:71)')
        try:
            sync=h.sync;h.verify_main(sync.git('rev-parse','HEAD'));assert not sync.git('status','--porcelain')
            for name,data in payload.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(payload)
            for i in range(0,len(names),50):sync.git('add','-f','--',*names[i:i+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','十日排序模型：49153真实成熟样本与11父方案回调CPU验证通过，独立六年度训练及46融合评分源冻结；尚未完成训练评分',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()};assert h.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);h.verify_main(commit);h.watcher.advance_source_index(commit)
            receipt={'status':'pushed_and_remote_head_verified','branch':'main','commit':commit,'raw_git_blobs_verified':len(hashes),'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()}
            create(out/'receipt.json',receipt);create(A/'Rank10_actual_fixture_callbacks11_fast46_sources_main_receipt_v1_20261011.json',receipt);print(receipt,flush=True)
        finally:
            for p in (parent,worker):
                if p.is_running():p.resume()
if __name__=='__main__':
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(key,value) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=key;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=value
    os.environ['GIT_CONFIG_COUNT']=str(count+2);main()
