"""Main-only publication of actual candidate reconstruction and the queued36/173/QA84 flow."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import sys,os,hashlib,gzip
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed()
    paths=[Path(__file__),*[Path(p) for p in ['D:\\3.Study\\数据分析\\赛题五\\analysis\\benchmark_shared_immutable_ranking_loader_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\shared_immutable_ranking_loader_actual_complete180_benchmark_v1_20261011.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\closed_main_154180_browser_profile_cleanup_plan_v1_20261011.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\closed_main_154180_browser_profile_cleanup_auto_review_rejection_v1_20261011.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\build_lossless_ranking_display_v2_20261006.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\exact_native_pretty_JSON_archive_20261007.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\github_validation_sync_main_20261005\\round180_receipt.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\github_validation_sync_main_20261005\\round181_receipt.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\monitor_reboot_optimization_v98_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\progress_observer98_bridge_dependency_tracking_admission_v1_20261011.json']]]
    import publish_classifier_consensus_workflows_20261006 as h
    prefix=Path('validation_sync/shared_immutable_ranking_loader_benchmark_v1_20261011');payload={};bindings={}
    for p in dict.fromkeys(paths):
        raw=p.read_bytes();assert not h.sync.SECRET.search(raw),p
        digest=hashlib.sha256(raw).hexdigest();rel=p.relative_to(ROOT) if p.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+p.name)
        name=(prefix/rel).as_posix();data=raw
        if len(data)>=5*1024**2:data=gzip.compress(data,mtime=0);name+='.gz';assert gzip.decompress(data)==raw
        assert len(data)<95*1024**2;payload[name]=data;bindings[str(p)]={'path':name,'raw_sha256':digest}
    payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({**{'status': 'passed_actual_complete180_shared_loader_all_native_bytes_exact', 'actual_connected_records': 17062, 'source_round': 180, 'actual_original_native_bytes': 5408991411, 'actual_original_native_sha256': 'c5ce3e8478cea5762382e43f0e1cc333d607b1a28914ab8404b90b2a3721ac5d', 'actual_load_and_decode_seconds': 2.3054135000002134, 'actual_decoded_RSS_bytes': 699076608, 'actual_retained_RSS_bytes': 546271232, 'all_values_types_key_order_and_float_spellings_byte_exact': True, 'scientific_runtime_adoption_not_performed': True, 'same_dataset_original_decoder_speedup_not_claimed': True, 'eligible_for_separately_verified_runtime_adoption': True, 'new_quality_scores': 0, 'new_native_fits': 0, 'test_labels_read': False, 'browser_profile_cleanup_rejected_by_automatic_review_no_deletion': True},'files':bindings})
    out=Path('E:/赛题五_本机临时/shared_immutable_ranking_loader_benchmark_main_v1_20261011');out.mkdir(exist_ok=False)
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
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','验证第180轮完整榜共享节点读取：54亿原始报告字节完全一致、实际0.65GB内存；记录历史浏览器缓存清理被自动审批拒绝且未执行',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()};assert h.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);h.verify_main(commit);h.watcher.advance_source_index(commit)
            receipt={'status':'pushed_and_remote_head_verified','branch':'main','commit':commit,'raw_git_blobs_verified':len(hashes),'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()}
            create(out/'receipt.json',receipt);create(A/'shared_immutable_ranking_loader_benchmark_main_receipt_v1_20261011.json',receipt);print(receipt,flush=True)
        finally:
            for p in (parent,worker):
                if p.is_running():p.resume()
if __name__=='__main__':
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(key,value) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=key;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=value
    os.environ['GIT_CONFIG_COUNT']=str(count+2);main()
