"""Publish corrected154 guard/bindings, actual151 complete receipt and independent69 Git reconciliation."""
from pathlib import Path
import sys,os,gzip,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
OUT=Path('E:/赛题五_本机临时/seed10_155_and_actual152_153_guard_main_v73_20261009')
def main():
    import publish_classifier_consensus_workflows_20261006 as h
    from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
    assert read(A/'two_seed154_actual_controls_main_v69_reconciled_receipt_20261009.json')['actual_independently_reverified_git_blobs']==991
    assert read(A/'optimization_20261003_r151/full_registration_execution.json')['status']=='passed'
    OUT.mkdir(exist_ok=False)
    assert read(A/'BF16Seed10_80_prospective_routes_v1_20261009.json')['prospective_sources']==56
    assert len(read(A/'BF16Seed10_80_prospective_routes_v1_20261009.json')['graph_controls'])==2100
    sources=[Path(__file__),A/'publish_seed10_155_and_actual152_153_guard_main_v72_20261009.py',A/'github_validation_sync_main_20261005/round152_receipt.json',A/'optimization_20261003_r152/full_registration_execution.json']
    for pattern in ('*BF16Seed10*20261009.py','*BF16Seed10*20261009.json','*SparseAfter148152*v40*','*BF16Medium153*v41*',
        'monitor_actual_chronological_optimization_progress_v63_20261009.py','start_actual_recovered_progress_v63_20261009.py',
        'actual_recovered_progress*v63*','latest_actual_optimization_progress_pointer_v63*','optimization_live_progress_v63*'):
        sources.extend(p for p in A.glob(pattern) if p.is_file() and p.suffix in ('.py','.json','.md'))
    sources += [A/'SparseAfter14829_official_comparison_v1_20261009/verification.json',A/'SparseAfter14829_official_comparison_v1_20261009/frozen_plan.json'] if (A/'SparseAfter14829_official_comparison_v1_20261009/frozen_plan.json').exists() else [A/'SparseAfter14829_official_comparison_v1_20261009/verification.json']
    for directory in (A/'service_owned_workflows_20261006').iterdir():
        if any(x in directory.name for x in ('BF16Seed10','SparseAfter14829','SparseAfter14855','BF16Medium153_complete_chronological_dispatch_guard_v41','seed10_155_and_actual152_153_guard_main_publication_v72')):
            sources.extend(p for p in directory.iterdir() if p.is_file() and p.suffix in ('.json','.log'))
    for pointer in ('actual_BF16Seed10_155_full73_training_location_v1_20261009.json','actual_BF16Seed10_155_native42_calendar_location_v1_20261009.json'):
        q=A/pointer;sources.append(q);folder=Path(read(q)['output']);assert sha(folder/'verification.json')==read(q)['verification_sha256']
        sources.extend(p for p in folder.rglob('*.json') if p.is_file())
    seen=set();queue=list(sources)
    while queue:
        q=queue.pop()
        if q in seen:continue
        seen.add(q);assert q.is_file(),q
        if q.suffix=='.json':
            value=read(q)
            if isinstance(value,dict):
                for field in ('input_sha256',):
                    for f,d in value.get(field,{}).items():
                        p=Path(f);assert p.is_file() and sha(p)==d,f
                        if p.suffix in ('.py','.json','.md','.log'):queue.append(p)
    sources=sorted(seen,key=str)
    held=[]
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v10_20261009/native_launch.json');assert owned(row)
        parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        create(OUT/'actual_idle_watcher_hold.json',idle)
        sync=h.sync;previous=sync.git('rev-parse','HEAD');h.verify_main(previous);assert not sync.git('status','--porcelain')
        prefix=Path('validation_sync/seed10_155_and_actual152_153_guard_v73_20261009');payload={};bindings={}
        for p in sources:
            raw=p.read_bytes();assert not sync.SECRET.search(raw),p
            digest=hashlib.sha256(raw).hexdigest();relative=p.relative_to(ROOT) if p.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+p.name)
            target=(prefix/relative).as_posix();data=raw
            if len(data)>=5*1024**2:data=gzip.compress(data,mtime=0);target+='.gz';assert gzip.decompress(data)==raw
            assert len(data)<95*1024**2;payload[target]=data;bindings[str(p)]={'published_path':target,'raw_sha256':digest,'original_bytes':len(raw)}
        payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
        payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'actual155_training_controls_and152_153_receiver_recovery_before155_quality',
            'at_local':sync.now(),'files':bindings,'actual155_reused_annual_models':6,'actual155_new_fits':0,
            'actual155_full_training_controls':73,'actual155_cold_training_controls':219,'actual155_native_cases':42,
            'actual155_prospective_sources':56,'actual155_graph_controls':2100,'actual155_quality_scores':0,
            'actual152_official_records':29,'actual152_legacy55_alias_executes_actual25_not55':True,
            'actual153_label_guard_controls':4,'all40_original153_generated_programs_preserved':True,
            'all_original_failed_attempts_preserved':True,'scientific_jobs_stopped_or_restarted':0,
            'actual155_fully_qualified_not_claimed':True,'test_labels_read':False})
        create(OUT/'frozen_before_main_publication.json',{'files':bindings})
        for name,data in payload.items():sync.atomic(sync.WORKTREE/name,data)
        targets=sorted(payload)
        for i in range(0,len(targets),50):sync.git('add','-f','--',*targets[i:i+50])
        assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(targets)
        sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','同步155单种子73完整219截断56流程2100图及152实际29评分和153接收修复证据',timeout=180)
        commit=sync.git('rev-parse','HEAD');hashes={p:hashlib.sha256(data).hexdigest() for p,data in payload.items()};assert h.blob_hashes(commit,hashes)==hashes
        sync.git('push','origin','HEAD:refs/heads/main',timeout=180);h.verify_main(commit);h.watcher.advance_source_index(commit)
        value={'status':'pushed_and_remote_head_verified','at_local':sync.now(),'branch':'main','commit':commit,'raw_git_blobs_verified':len(hashes),
            'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()}
        create(OUT/'receipt.json',value);create(A/'seed10_155_and_actual152_153_guard_main_v73_receipt_20261009.json',value);print(value,flush=True)
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
    log=Path('E:/赛题五_本机临时/seed10_155_and_actual152_153_guard_safe_main_v73_20261009')
    with safe(log),serial(log/'serial_mutex.json'),git_io(log/'file_backed_git'):main()
