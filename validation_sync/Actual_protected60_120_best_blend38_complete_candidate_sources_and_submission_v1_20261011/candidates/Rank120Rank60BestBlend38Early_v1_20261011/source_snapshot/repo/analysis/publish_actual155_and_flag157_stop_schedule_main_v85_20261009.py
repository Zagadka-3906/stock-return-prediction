"""Publish actual155 completion, frozen157 train-only frontier and the verified explicit stop."""
from pathlib import Path
from datetime import datetime
import sys,os,gzip,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
OUT=Path('E:/赛题五_本机临时/actual155_flag157_and_stop_schedule_main_v85_20261009')
def main():
    assert datetime.now().astimezone()<datetime.fromisoformat(read(A/'current_user_runtime_control_20261009.json')['stop_at_local'])
    import publish_classifier_consensus_workflows_20261006 as h
    from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
    assert read(A/'optimization_20261003_r155/full_registration_execution.json')['status']=='passed'
    receipt155=read(A/'github_validation_sync_main_20261005/round155_receipt.json');assert receipt155['scored_records']==80 and receipt155['actual_full_QA_version']==66
    syn=read(A/'BF16FlagAfter15217_synthetic17_cold51_v1_20261009.json');assert (syn['actual_cases'],syn['actual_cold_cases'])==(17,51)
    schedule=A/'user_requested_stop2355_until_manual_continue_v1_20261009'
    stop=read(schedule/'schedule.json');assert stop['stop_at_local']=='2026-10-09T23:55:00+08:00' and not stop['automatic_restart_enabled']
    for directory in ('shutdown_ready_stop_preflight_current2355_20261009','shutdown_ready_stop_preflight_current2355_preheld_20261009'):
        proof=read(A/directory/'verification.json');assert proof['only_isolated_probe_terminated'] and proof['scientific_workers_terminated']==0
    OUT.mkdir(exist_ok=False)
    sources=[Path(__file__),ROOT/'AGENTS.md',A/'current_user_runtime_control_20261009.json',A/'current_user_runtime_control_20261008.json',
        A/'user_requested_stop2355_v1_20261009.py',A/'activate_actual_user_stop2355_v1_20261009.py',
        A/'verify_user_requested_stop2355_v1_20261009.py',A/'verify_user_requested_stop2355_preheld_v1_20261009.py',
        A/'optimization_20261003_r155/full_registration_execution.json',A/'github_validation_sync_main_20261005/round155_receipt.json',
        A/'lossless_ranking_display_qa_v66_20261009/round155/verification.json']
    for pattern in ('*BF16FlagAfter152*20261009*.py','*BF16FlagAfter152*20261009*.json','*progress*v69_20261009.py','*progress*v69_20261009.json','*progress*v69_20261009.md'):
        sources.extend(p for p in A.glob(pattern) if p.is_file())
    for directory in (schedule,A/'shutdown_ready_stop_preflight_current2355_20261009',A/'shutdown_ready_stop_preflight_current2355_preheld_20261009'):
        sources.extend(directory.glob('*.json'))
    for directory in (A/'service_owned_workflows_20261006').iterdir():
        if any(x in directory.name for x in ('BF16FlagAfter152','BF16Seed10_80_round155_full_registration','actual_user_stop2355_wait_manual_continue_v1_20261009','shutdown_stop_guardian_current2355','shutdown_stop_probe_current2355')):
            sources.extend(p for p in directory.glob('*') if p.is_file() and p.suffix in ('.json','.log'))
    sources=list(dict.fromkeys(sources));assert all(p.is_file() for p in sources)
    held=[]
    try:
        launch=read(A/'service_owned_workflows_20261006/main_publisher_v10_20261009/native_launch.json');assert owned(launch)
        parent,worker,idle=suspended_idle(launch,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        create(OUT/'actual_idle_watcher_hold.json',idle)
        sync=h.sync;previous=sync.git('rev-parse','HEAD');h.verify_main(previous);assert not sync.git('status','--porcelain')
        prefix=Path('validation_sync/actual155_flag157_and_explicit_stop_v85_20261009');payload={};bindings={}
        for p in sources:
            raw=p.read_bytes();assert not sync.SECRET.search(raw),p
            digest=hashlib.sha256(raw).hexdigest();target=(prefix/p.relative_to(ROOT)).as_posix();data=raw
            if len(data)>=5*1024**2:data=gzip.compress(data,mtime=0);target+='.gz';assert gzip.decompress(data)==raw
            assert len(data)<95*1024**2;payload[target]=data;bindings[str(p)]={'published_path':target,'raw_sha256':digest,'original_bytes':len(raw)}
        payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
        payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'actual155_complete_QA66_main_and157_frozen_frontier_and_explicit_October9_stop',
            'at_local':sync.now(),'files':bindings,'actual155_official_records':80,'actual155_full_QA':66,'actual155_main_commit':receipt155['commit'],
            'actual155_connected_records':receipt155['connected_records'],'actual157_synthetic_cases':17,'actual157_synthetic_prefixes':51,
            'actual157_full_controls_pending':True,'actual157_expected_quality_cases':22,'actual157_new_fits':0,'actual157_future_X_read':False,
            'explicit_stop_at_local':stop['stop_at_local'],'actual_isolated_deadline_tests_passed':2,
            'scientific_workers_stopped_by_schedule_activation':0,'goal_not_paused_before_deadline':True,
            'manual_continue_required_after_stop':True,'automatic_restart_enabled':False,
            'test_labels_read':False,'new_scores_by_publication':0,'global_search_exhaustion_proven':False})
        create(OUT/'frozen_before_main_publication.json',{'files':bindings})
        for name,data in payload.items():sync.atomic(sync.WORKTREE/name,data)
        targets=sorted(payload)
        for i in range(0,len(targets),50):sync.git('add','-f','--',*targets[i:i+50])
        assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(targets)
        sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','同步155完整80评分与QA66及157新152涨停修正方向17检查和23点55停工实测',timeout=180)
        commit=sync.git('rev-parse','HEAD');hashes={p:hashlib.sha256(data).hexdigest() for p,data in payload.items()};assert h.blob_hashes(commit,hashes)==hashes
        sync.git('push','origin','HEAD:refs/heads/main',timeout=180);h.verify_main(commit);h.watcher.advance_source_index(commit)
        value={'status':'pushed_and_remote_head_verified','at_local':sync.now(),'branch':'main','commit':commit,'raw_git_blobs_verified':len(hashes),
            'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()}
        create(OUT/'receipt.json',value);create(A/'actual155_flag157_and_stop_schedule_main_v85_receipt_20261009.json',value);print(value,flush=True)
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
    log=Path('E:/赛题五_本机临时/actual155_flag157_and_stop_schedule_safe_main_v85_20261009')
    with safe(log),serial(log/'serial_mutex.json'),git_io(log/'file_backed_git'):main()
