"""Main-only publication of actual candidate reconstruction and the queued36/173/QA84 flow."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import sys,os,hashlib,gzip
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed()
    paths=[Path(__file__),*[Path(p) for p in ['D:\\3.Study\\数据分析\\赛题五\\analysis\\publish_rank60_direct33_predeclared_CPU_sources_main_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\stock_rank60_after183_direct33_predeclared_sources_v1_20261011.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\stock_rank60_actual_twelve_parent183_callbacks_CPU_controls_v2_20261011.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\actual_stock_rank60_after183_direct33_activation_v1_20261011.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\actual_rank60_after183_completed33_main_activation_v1_20261011.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\run_publish_rank60_after183_completed33_main_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\prepare_rank60_after183_direct33_sources_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\stock_rank60_embedding_after_complete_qualified_parent_native_stage_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\stock_rank60_embedding_after_complete_qualified_parent_native_stage_v2_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\predict_stock_rank60_embedding_complete_qualified_parent_scheme_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\predict_stock_rank60_embedding_complete_qualified_parent_scheme_v2_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_stock_rank20class10_actual_twelve_parent_callbacks_CPU_v2_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_stock_rank60_actual_twelve_parent183_callbacks_CPU_v2_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\run_stock_rank20class10_embedding_after183_exact_latest_anchor17_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\run_stock_rank60_embedding_after183_direct_allocation33_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\optimization_20261003_r183\\calibrated_csv_official.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\github_validation_sync_main_20261005\\round183_receipt.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\stock_rank60_new60_horizon_source_pipeline_admission_v1_20261011.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\stock_rank20seed10_embedding_actual_eleven_parent_callbacks_CPU_controls_v1_20261011.json', 'D:\\3.Study\\数据分析\\赛题五\\candidates\\optimization_20261003_r183\\verification.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\publish_frozen_Actual183_parent37_and_mixed60_49_sources_main_v1_20261011.py']]]
    import publish_classifier_consensus_workflows_20261006 as h
    prefix=Path('validation_sync/Rank60_direct33_actual12_CPU_predeclared_sources_v1_20261011');payload={};bindings={}
    for p in dict.fromkeys(paths):
        raw=p.read_bytes();assert not h.sync.SECRET.search(raw),p
        digest=hashlib.sha256(raw).hexdigest();rel=p.relative_to(ROOT) if p.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+p.name)
        name=(prefix/rel).as_posix();data=raw
        if len(data)>=5*1024**2:data=gzip.compress(data,mtime=0);name+='.gz';assert gzip.decompress(data)==raw
        assert len(data)<95*1024**2;payload[name]=data;bindings[str(p)]={'path':name,'raw_sha256':digest}
    payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({**{'status': 'actual12_complete_parent_CPU_callback_controls_and_frozen33_pure_H60_after183_hypotheses_before_scores', 'actual_parent_CPU_checks': 12, 'expected_official_records': 33, 'parent_round': 183, 'horizon': 60, 'new_fits_or_scores_by_publication': 0, 'score_and_selected_native14_and_future_qualification_pending': True, 'test_labels_read': False},'files':bindings})
    out=Path('E:/赛题五_本机临时/Rank60_direct33_actual12_CPU_predeclared_sources_main_v1_20261011');out.mkdir(exist_ok=False)
    create(out/'frozen_before_publication.json',{'files':bindings})
    from lossless_chunked_safe_main_runtime_v1_20261009 import installed as safe
    from serial_main_publication_mutex_v1_20261009 import installed as serial
    from verified_TLS_Git_retry_runtime_v3_20261010 import installed as git_io
    from owned_idle_publication_wait_reboot_identity_v2_20261011 import hold
    with serial(out/'serial_mutex.json') as mutex,safe(out/'safe'),git_io(out/'file_backed_git'):
        mutex.acquire();assert allowed()
        parent,worker,idle=hold(read(A/'service_owned_workflows_20261006/main_publisher_reboot_v12_20261011/native_launch.json'),'    main (watch_validations_main_v7_20261006.py:71)')
        try:
            sync=h.sync;h.verify_main(sync.git('rev-parse','HEAD'));assert not sync.git('status','--porcelain')
            for name,data in payload.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(payload)
            for i in range(0,len(names),50):sync.git('add','-f','--',*names[i:i+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','纯60日信号对完整183方案的33项大小权重及保护顶部排序预声明；12项实际父回调CPU通过',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()};assert h.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);h.verify_main(commit);h.watcher.advance_source_index(commit)
            receipt={'status':'pushed_and_remote_head_verified','branch':'main','commit':commit,'raw_git_blobs_verified':len(hashes),'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()}
            create(out/'receipt.json',receipt);create(A/'Rank60_direct33_actual12_CPU_predeclared_sources_main_receipt_v1_20261011.json',receipt);print(receipt,flush=True)
        finally:
            for p in (parent,worker):
                if p.is_running():p.resume()
if __name__=='__main__':
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(key,value) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=key;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=value
    os.environ['GIT_CONFIG_COUNT']=str(count+2);main()
