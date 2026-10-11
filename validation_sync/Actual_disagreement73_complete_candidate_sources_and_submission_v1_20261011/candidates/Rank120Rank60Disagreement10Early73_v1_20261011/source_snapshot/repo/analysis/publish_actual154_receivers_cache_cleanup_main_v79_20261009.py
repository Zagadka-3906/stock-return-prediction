"""Publish actual154 successful gate repair and the bounded historical-cache cleanup."""
from pathlib import Path
import sys,os,gzip,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
OUT=Path('E:/赛题五_本机临时/actual154_corrected_receivers_cache_cleanup_main_v79_20261009')
def main():
    import publish_classifier_consensus_workflows_20261006 as h
    from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
    assert read(A/'service_owned_workflows_20261006/BF16TwoSeed79_round154_source_admission_v2_20261009/service_execution.json')['status']=='passed'
    cleanup=read(A/'historical_inactive_browser_cache_cleanup_v78_20261009.json')
    assert cleanup['model_and_score_files_deleted']==0 and cleanup['application_processes_stopped']==0
    assert read(A/'optimization_20261003_r153/full_registration_execution.json')['status']=='passed'
    OUT.mkdir(exist_ok=False)
    sources=[Path(__file__),A/'BF16TwoSeed154_complete_pipeline_preparation_v5_20261009.json',
        A/'BF16TwoSeed154_duplicate_pointer_namespace_correction_v50_20261009.json',
        A/'BF16TwoSeed154_corrected_admission_hidden_dispatch_v50_20261009.json',
        A/'round153_original_watcher_receipt_before_full_QA_reconciliation_v48_20261009.json',
        A/'historical_inactive_browser_cache_candidates_v78_20261009.json',
        A/'historical_inactive_browser_cache_cleanup_v78_20261009.json',
        A/'clear_historical_inactive_browser_cache_v78_20261009.ps1',
        A/'actual153_complete_and_dropout156_controls_main_v77_receipt_20261009.json']
    meta=read(A/'BF16TwoSeed154_complete_pipeline_preparation_v5_20261009.json')
    sources += [A/driver for _,driver,_ in meta['receiver_specs']]
    for pattern in ('*progress*v66_20261009.py','*progress*v66_20261009.json','*progress*v66_20261009.md'):
        sources.extend(A.glob(pattern))
    for service in ('BF16TwoSeed79_round154_source_admission_v1_20261009','BF16TwoSeed79_round154_source_admission_v2_20261009','BF16TwoSeed154_complete_chronological_dispatch_v5_20261009','actual_chronological_optimization_progress_observer_v66_20261009'):
        directory=A/'service_owned_workflows_20261006'/service
        sources.extend(p for p in directory.glob('*') if p.is_file() and p.suffix in ('.json','.log'))
    sources=list(dict.fromkeys(sources));assert all(p.is_file() for p in sources)
    held=[]
    try:
        launch=read(A/'service_owned_workflows_20261006/main_publisher_v10_20261009/native_launch.json');assert owned(launch)
        parent,worker,idle=suspended_idle(launch,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        create(OUT/'actual_idle_watcher_hold.json',idle)
        sync=h.sync;previous=sync.git('rev-parse','HEAD');h.verify_main(previous);assert not sync.git('status','--porcelain')
        prefix=Path('validation_sync/actual154_corrected_receivers_cache_cleanup_v79_20261009');payload={};bindings={}
        for p in sources:
            raw=p.read_bytes();assert not sync.SECRET.search(raw),p
            digest=hashlib.sha256(raw).hexdigest();relative=p.relative_to(ROOT)
            target=(prefix/relative).as_posix();data=raw
            if len(data)>=5*1024**2:data=gzip.compress(data,mtime=0);target+='.gz';assert gzip.decompress(data)==raw
            assert len(data)<95*1024**2;payload[target]=data;bindings[str(p)]={'published_path':target,'raw_sha256':digest,'original_bytes':len(raw)}
        payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
        payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'actual154_admission2_passed_namespace_repair_and_inactive_cache_cleanup','at_local':sync.now(),'files':bindings,'artifact_filenames_preserved':True,'actual153_old_watcher_receipt_preserved':True,'cache_cleanup':cleanup,'original_scientific_models_and_scoring_unchanged':True,'new_scores_by_publication':0,'test_labels_read':False,'global_search_exhaustion_proven':False})
        create(OUT/'frozen_before_main_publication.json',{'files':bindings})
        for name,data in payload.items():sync.atomic(sync.WORKTREE/name,data)
        targets=sorted(payload)
        for i in range(0,len(targets),50):sync.git('add','-f','--',*targets[i:i+50])
        assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(targets)
        sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','同步154准入修复及实际进度和138项历史浏览器缓存清理证据',timeout=180)
        commit=sync.git('rev-parse','HEAD');hashes={p:hashlib.sha256(data).hexdigest() for p,data in payload.items()};assert h.blob_hashes(commit,hashes)==hashes
        sync.git('push','origin','HEAD:refs/heads/main',timeout=180);h.verify_main(commit);h.watcher.advance_source_index(commit)
        value={'status':'pushed_and_remote_head_verified','at_local':sync.now(),'branch':'main','commit':commit,'raw_git_blobs_verified':len(hashes),'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()}
        create(OUT/'receipt.json',value);create(A/'actual154_corrected_receivers_cache_cleanup_main_v79_receipt_20261009.json',value);print(value,flush=True)
    finally:
        for process in reversed(held):
            if process.is_running():process.resume()
        create(OUT/'actual_idle_watcher_resumed.json',{'resumed_in_finally':True,'scientific_workers_held':0})
if __name__=='__main__':
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(key,value) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=key;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=value
    os.environ['GIT_CONFIG_COUNT']=str(count+2)
    from lossless_chunked_safe_main_runtime_v1_20261009 import installed as safe
    from serial_main_publication_mutex_v1_20261009 import installed as serial
    from verified_TLS_Git_retry_runtime_v2_20261008 import installed as git_io
    log=Path('E:/赛题五_本机临时/actual154_corrected_receivers_cache_cleanup_safe_main_v79_20261009')
    with safe(log),serial(log/'serial_mutex.json'),git_io(log/'file_backed_git'):main()
