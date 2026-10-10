"""Main-only publication of actual candidate reconstruction and the queued36/173/QA84 flow."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import sys,os,hashlib,gzip
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed()
    paths=[Path(__file__),*[Path(p) for p in ['D:\\3.Study\\数据分析\\赛题五\\analysis\\publish_additional_cached_mixed_ensembles_stages_main_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\publish_StockRank20_actual_own6_full5_main_v66_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\后续选模标准.md', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\cached_mixed_near_pure_and_long_window49_admission_v1_20261011.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\mixed_horizon_native14_predictor_CPU11_sources_admission_v1_20261011.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\prepare_cached_mixed_near_pure_and_long_window49_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\run_rank5_rank20_after175_mixed_horizon49_screen_v2_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\rank5_rank20_near_pure49_predeclared_plan_v1_20261011.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\rank20_short_long_mixed_window49_predeclared_plan_v1_20261011.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\run_rank5_rank20_after175_near_pure49_screen_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\run_rank20_short_long_after175_mixed_window49_screen_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\prepare_mixed_horizon_native14_predictor_CPU11_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\rank20_two_seed_after_qualified_parent_native_stage_v1_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\predict_rank20_two_seed_complete_qualified_parent_scheme_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_rank20_two_seed_actual_eleven_parent_callbacks_CPU_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_rank5_rank20_mixed_actual_eleven_parent_callbacks_CPU_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\rank5_rank20_mixed_after_qualified_parent_native_stage_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\predict_rank5_rank20_mixed_complete_qualified_parent_scheme_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_rank20_two_seed_protected_selected_native14_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_rank5_rank20_mixed_selected_native14_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\rank5_rank20_mixed_actual_eleven_parent_callbacks_CPU_controls_v1_20261011.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\complete180_registered_continuation_routes_v13_20261011.json', 'E:\\赛题五_本机临时\\stock_rank20_embedding_small512_BF16_bank6_v1_20261010\\2020\\info.json', 'E:\\赛题五_本机临时\\stock_rank20_embedding_small512_BF16_bank6_v1_20261010\\2021\\info.json', 'E:\\赛题五_本机临时\\stock_rank20_embedding_small512_BF16_bank6_v1_20261010\\2022\\info.json', 'E:\\赛题五_本机临时\\stock_rank20_embedding_small512_BF16_bank6_v1_20261010\\2023\\info.json', 'E:\\赛题五_本机临时\\stock_rank20_embedding_small512_BF16_bank6_v1_20261010\\2024\\info.json', 'E:\\赛题五_本机临时\\stock_rank20_embedding_small512_BF16_bank6_v1_20261010\\2025\\info.json', 'E:\\赛题五_本机临时\\stock_rank5_embedding_small512_BF16_bank6_v1_20261010\\2020\\info.json', 'E:\\赛题五_本机临时\\stock_rank5_embedding_small512_BF16_bank6_v1_20261010\\2021\\info.json', 'E:\\赛题五_本机临时\\stock_rank5_embedding_small512_BF16_bank6_v1_20261010\\2022\\info.json', 'E:\\赛题五_本机临时\\stock_rank5_embedding_small512_BF16_bank6_v1_20261010\\2023\\info.json', 'E:\\赛题五_本机临时\\stock_rank5_embedding_small512_BF16_bank6_v1_20261010\\2024\\info.json', 'E:\\赛题五_本机临时\\stock_rank5_embedding_small512_BF16_bank6_v1_20261010\\2025\\info.json']]]
    import publish_classifier_consensus_workflows_20261006 as h
    prefix=Path('validation_sync/additional_cached_mixed_sources_v1_20261011');payload={};bindings={}
    for p in dict.fromkeys(paths):
        raw=p.read_bytes();assert not h.sync.SECRET.search(raw),p
        digest=hashlib.sha256(raw).hexdigest();rel=p.relative_to(ROOT) if p.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+p.name)
        name=(prefix/rel).as_posix();data=raw
        if len(data)>=5*1024**2:data=gzip.compress(data,mtime=0);name+='.gz';assert gzip.decompress(data)==raw
        assert len(data)<95*1024**2;payload[name]=data;bindings[str(p)]={'path':name,'raw_sha256':digest}
    payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({**{'status': 'actual_phase_evidence_preserved', 'phase': 'sources', 'official_score_records': 0, 'actual_full_Pandas_controls': 0, 'actual_prefix_controls': 0, 'native14_actual_only': False, 'CPU_callback_count': 11, 'new_fits': 0, 'new_scores_by_publication': 0, 'training_populations_equal_not_claimed': True, 'future_candidate_qualification_pending': True, 'test_labels_read': False, 'global_exhaustion_proven': False},'files':bindings})
    out=Path('E:/赛题五_本机临时/additional_cached_mixed_sources_main_v1_20261011');out.mkdir(exist_ok=False)
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
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','保存缓存模型小比例跨目标融合、252与504日窗口融合和各自实际独立控制：sources；未完成未来资格不记通过',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()};assert h.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);h.verify_main(commit);h.watcher.advance_source_index(commit)
            receipt={'status':'pushed_and_remote_head_verified','branch':'main','commit':commit,'raw_git_blobs_verified':len(hashes),'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()}
            create(out/'receipt.json',receipt);create(A/'additional_cached_mixed_sources_main_receipt_v1_20261011.json',receipt);print(receipt,flush=True)
        finally:
            for p in (parent,worker):
                if p.is_running():p.resume()
if __name__=='__main__':
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(key,value) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=key;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=value
    os.environ['GIT_CONFIG_COUNT']=str(count+2);main()
