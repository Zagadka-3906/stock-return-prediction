"""Publish corrected154 guard/bindings, actual151 complete receipt and independent69 Git reconciliation."""
from pathlib import Path
import sys,os,gzip,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
OUT=Path('E:/赛题五_本机临时/two_seed154_guard_verified_main_v70_20261009')
def main():
    import publish_classifier_consensus_workflows_20261006 as h
    from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
    assert read(A/'two_seed154_actual_controls_main_v69_reconciled_receipt_20261009.json')['actual_independently_reverified_git_blobs']==991
    assert read(A/'optimization_20261003_r151/full_registration_execution.json')['status']=='passed'
    OUT.mkdir(exist_ok=False)
    names=['prepare_BF16TwoSeed154_parent_guard_bindings_v2_20261009.py','BF16TwoSeed154_actual_parent_guard_controls_v2_20261009.json',
        'BF16TwoSeed154_complete_pipeline_preparation_v2_20261009.json','BF16TwoSeed154_parent_guard_corrected_hidden_handoff_v2_20261009.json',
        'prepare_BF16TwoSeed79_selected_candidate_v2_20261009.py','run_BF16TwoSeed79_round154_full_registration_v2_20261009.py',
        'run_BF16TwoSeed154_safe_registration_v2_20261009.py','verify_BF16TwoSeed79_round154_sources_v2_20261009.py',
        'dispatch_BF16TwoSeed154_complete_pipeline_v2_20261009.py','two_seed154_actual_controls_main_v69_reconciled_receipt_20261009.json',
        'reconcile_two_seed154_actual_main_v69_20261009.py','reconcile_two_seed154_actual_main_v69_v2_20261009.py',
        'optimization_20261003_r151/full_registration_execution.json','github_validation_sync_main_20261005/round151_receipt.json',
        'monitor_actual_chronological_optimization_progress_v62_20261009.py','start_actual_recovered_progress_v62_20261009.py',
        'actual_recovered_progress_hidden_launch_v62_20261009.json','latest_actual_optimization_progress_pointer_v62_20261009.json',
        'actual_recovered_progress_handoff_v62_20261009.json','optimization_live_progress_v62_20261009.json','optimization_live_progress_v62_20261009.md',
        'lossless_chunked_safe_main_runtime_v1_20261009.py','serial_main_publication_mutex_v1_20261009.py']
    sources=[Path(__file__),*(A/n for n in names),Path('E:/赛题五_本机临时/two_seed154_actual69_committed_blob_reconciliation_v2_20261009/verification.json')]
    for name in ('BF16TwoSeed154_complete_chronological_dispatch_v1_20261009','BF16TwoSeed154_complete_chronological_dispatch_v2_20261009',
        'two_seed154_actual_complete_controls_main_publication_v69_20261009','RFFSparse59_round151_full_registration_v3_20261009'):
        f=A/'service_owned_workflows_20261006'/name;sources.extend(p for p in f.iterdir() if p.suffix in ('.json','.log'))
    for n in names:
        q=A/n
        if q.suffix=='.json' and not q.name.startswith('optimization_live_progress'):
            for f,d in read(q).get('input_sha256',{}).items():
                assert sha(f)==d,f
                if Path(f).suffix in ('.py','.json','.md','.log'):sources.append(Path(f))
    sources=list(dict.fromkeys(sources));assert all(p.is_file() for p in sources)
    assert len(read(A/'BF16TwoSeed154_actual_parent_guard_controls_v2_20261009.json')['controls'])==16
    held=[]
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v10_20261009/native_launch.json');assert owned(row)
        parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        create(OUT/'actual_idle_watcher_hold.json',idle)
        sync=h.sync;previous=sync.git('rev-parse','HEAD');h.verify_main(previous);assert not sync.git('status','--porcelain')
        prefix=Path('validation_sync/two_seed154_guard_verified_v70_20261009');payload={};bindings={}
        for p in sources:
            raw=p.read_bytes();assert not sync.SECRET.search(raw),p
            digest=hashlib.sha256(raw).hexdigest();relative=p.relative_to(ROOT) if p.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+p.name)
            target=(prefix/relative).as_posix();data=raw
            if len(data)>=5*1024**2:data=gzip.compress(data,mtime=0);target+='.gz';assert gzip.decompress(data)==raw
            assert len(data)<95*1024**2;payload[target]=data;bindings[str(p)]={'published_path':target,'raw_sha256':digest,'original_bytes':len(raw)}
        payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
        payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'actual154_parent_guards_corrected_before_quality_and_actual69_git_reconciliation',
            'at_local':sync.now(),'files':bindings,'actual_comparison_parent_guard_controls':16,'actual154_existing_saved_states':12,
            'actual154_full_training_controls':73,'actual154_cold_training_controls':219,'actual154_native_cases':42,
            'actual154_prospective_sources':48,'actual154_graph_controls':1800,'actual154_quality_scores':0,
            'actual151_official_records':59,'actual151_complete_original_six_view_QA_and_main_passed':True,
            'actual69_all991_git_blobs_independently_reverified':True,'original_failed_local_receipt_and_preflight_attempts_preserved':True,
            'scientific_jobs_stopped_or_restarted':0,'actual154_fully_qualified_not_claimed':True,'test_labels_read':False})
        create(OUT/'frozen_before_main_publication.json',{'files':bindings})
        for name,data in payload.items():sync.atomic(sync.WORKTREE/name,data)
        targets=sorted(payload)
        for i in range(0,len(targets),50):sync.git('add','-f','--',*targets[i:i+50])
        assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(targets)
        sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','同步154全六父方案16接收边界检查与151完整验证及69提交独立991文件复核',timeout=180)
        commit=sync.git('rev-parse','HEAD');hashes={p:hashlib.sha256(data).hexdigest() for p,data in payload.items()};assert h.blob_hashes(commit,hashes)==hashes
        sync.git('push','origin','HEAD:refs/heads/main',timeout=180);h.verify_main(commit);h.watcher.advance_source_index(commit)
        value={'status':'pushed_and_remote_head_verified','at_local':sync.now(),'branch':'main','commit':commit,'raw_git_blobs_verified':len(hashes),
            'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()}
        create(OUT/'receipt.json',value);create(A/'two_seed154_guard_verified_main_v70_receipt_20261009.json',value);print(value,flush=True)
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
    log=Path('E:/赛题五_本机临时/two_seed154_guard_verified_safe_main_v70_20261009')
    with safe(log),serial(log/'serial_mutex.json'),git_io(log/'file_backed_git'):main()
