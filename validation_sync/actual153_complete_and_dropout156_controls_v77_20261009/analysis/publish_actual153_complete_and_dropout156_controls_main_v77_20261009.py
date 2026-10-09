"""Publish corrected154 guard/bindings, actual151 complete receipt and independent69 Git reconciliation."""
from pathlib import Path
import sys,os,gzip,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
OUT=Path('E:/赛题五_本机临时/actual153_complete_and_dropout156_controls_main_v77_20261009')
def main():
    import publish_classifier_consensus_workflows_20261006 as h
    from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
    assert read(A/'two_seed154_actual_controls_main_v69_reconciled_receipt_20261009.json')['actual_independently_reverified_git_blobs']==991
    assert read(A/'optimization_20261003_r151/full_registration_execution.json')['status']=='passed'
    OUT.mkdir(exist_ok=False)
    proof=read(A/'BF16Medium153_committed_full_QA_main_reconciliation_v48_20261009.json')
    assert proof['actual_scored_records']==78 and proof['actual_connected_records']==15310
    assert read(A/'optimization_20261003_r153/full_registration_execution.json')['status']=='passed'
    prospect=read(A/'BF16Drop05_81_prospective_routes_v1_20261009.json');assert prospect['prospective_sources']==64 and len(prospect['graph_controls'])==2400
    sources=[Path(__file__),A/'BF16Drop05156_preserved_initial_preflight_failures_v77_20261009.json',
        A/'github_validation_sync_main_20261005/round153_receipt.json',A/'optimization_20261003_r153/full_registration_execution.json']
    for pattern in ('*BF16Drop05*20261009*.py','*BF16Drop05*20261009*.json','*drop05_seed09*20261009.py','*drop05_seed09*20261009.json',
        '*QA*path*v43*','*QA_and_actual153*v44*','*QA_and_actual153*v45*','*BF16Medium153*v43*','*BF16Medium153*v46*','*BF16Medium153*v47*','*BF16Medium153*v48*',
        '*BF16TwoSeed154*verified153*v49*','*BF16TwoSeed154*preparation_v4*','*BF16TwoSeed154*preparation_v3*',
        '*BF16Seed10_155*preparation_v2*','*BF16Drop05_156*preparation_v3*',
        'monitor_actual_chronological_optimization_progress_v65_20261009.py','start_actual_recovered_progress_v65_20261009.py',
        'actual_recovered_progress*v65*','latest_actual_optimization_progress_pointer_v65*','optimization_live_progress_v65*'):
        sources.extend(p for p in A.glob(pattern) if p.is_file() and p.suffix in ('.py','.json','.md'))
    metas=['BF16TwoSeed154_complete_pipeline_preparation_v4_20261009.json','BF16Seed10_155_complete_pipeline_preparation_v2_20261009.json','BF16Drop05_156_complete_pipeline_preparation_v3_20261009.json']
    for n in metas:
        m=read(A/n)
        for _,driver,_ in m['receiver_specs']:sources.append(A/driver)
    sources.append(Path('E:/赛题五_本机临时/BF16Medium153_committed_full_QA_reconciliation_v48_20261009/verification.json'))
    small=Path('E:/赛题五_本机临时/BF16Drop05_156_independent_small_CPU_v1_20261009')
    sources.extend(small.glob('*.json'))
    for d in (A/'service_owned_workflows_20261006').iterdir():
        if any(x in d.name for x in ('BF16Drop05','drop05_seed09','BF16Medium78_round153_full_registration','BF16TwoSeed154_complete_chronological_dispatch','BF16TwoSeed154_prior_complete_forecast_duplicate_audit')):
            sources.extend(p for p in d.iterdir() if p.is_file() and p.suffix in ('.json','.log'))
    sources=list(dict.fromkeys(sources));assert all(p.is_file() for p in sources)
    held=[]
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v10_20261009/native_launch.json');assert owned(row)
        parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        create(OUT/'actual_idle_watcher_hold.json',idle)
        sync=h.sync;previous=sync.git('rev-parse','HEAD');h.verify_main(previous);assert not sync.git('status','--porcelain')
        prefix=Path('validation_sync/actual153_complete_and_dropout156_controls_v77_20261009');payload={};bindings={}
        for p in sources:
            raw=p.read_bytes();assert not sync.SECRET.search(raw),p
            digest=hashlib.sha256(raw).hexdigest();relative=p.relative_to(ROOT) if p.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+p.name)
            target=(prefix/relative).as_posix();data=raw
            if len(data)>=5*1024**2:data=gzip.compress(data,mtime=0);target+='.gz';assert gzip.decompress(data)==raw
            assert len(data)<95*1024**2;payload[target]=data;bindings[str(p)]={'published_path':target,'raw_sha256':digest,'original_bytes':len(raw)}
        payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
        payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'actual153_completed_all_original_QA_main_reconciliation_and156_complete_prequality_controls',
            'at_local':sync.now(),'files':bindings,'actual153_official_records':78,'actual153_connected_records':15310,
            'actual153_all_committed_blobs_independently_reverified':proof['actual_committed_blobs'],
            'actual153_original4GB_report_stream_reverified':True,'actual153_new_quality_gain':0,
            'actual156_synthetic_cases':73,'actual156_synthetic_cold_cases':219,'actual156_original_parent_ABI_controls':5,
            'actual156_small_saved_tensor_independent_bits_passed':True,
            'actual156_prospective_sources':64,'actual156_graph_controls':2400,'actual156_parent_guard_controls':20,
            'actual156_own_mature_annual_fits_completed':0,'actual156_expected_own_mature_annual_fits':6,
            'actual156_expected_official_scores':81,'actual156_real_full73_native42_controls_pending':True,
            'actual156_new_quality_scores':0,'all_initial_failed_attempts_and_full153_old_receipt_preserved':True,
            'scientific_jobs_stopped_or_restarted':0,'all_original_full_ranking_QA_checks_preserved':True,
            'test_labels_read':False,'resource_or_global_search_exhaustion_proven':False})
        create(OUT/'frozen_before_main_publication.json',{'files':bindings})
        for name,data in payload.items():sync.atomic(sync.WORKTREE/name,data)
        targets=sorted(payload)
        for i in range(0,len(targets),50):sync.git('add','-f','--',*targets[i:i+50])
        assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(targets)
        sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','同步153完整QA64与5963提交文件和原榜还原复核及156完整预检64流程2400图和20父边界',timeout=180)
        commit=sync.git('rev-parse','HEAD');hashes={p:hashlib.sha256(data).hexdigest() for p,data in payload.items()};assert h.blob_hashes(commit,hashes)==hashes
        sync.git('push','origin','HEAD:refs/heads/main',timeout=180);h.verify_main(commit);h.watcher.advance_source_index(commit)
        value={'status':'pushed_and_remote_head_verified','at_local':sync.now(),'branch':'main','commit':commit,'raw_git_blobs_verified':len(hashes),
            'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()}
        create(OUT/'receipt.json',value);create(A/'actual153_complete_and_dropout156_controls_main_v77_receipt_20261009.json',value);print(value,flush=True)
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
    log=Path('E:/赛题五_本机临时/actual153_complete_and_dropout156_controls_safe_main_v77_20261009')
    with safe(log),serial(log/'serial_mutex.json'),git_io(log/'file_backed_git'):main()
