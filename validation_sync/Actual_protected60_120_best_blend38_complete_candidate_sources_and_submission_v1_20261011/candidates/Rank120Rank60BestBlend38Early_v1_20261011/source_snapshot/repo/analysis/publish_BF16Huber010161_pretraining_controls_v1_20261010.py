"""Publish the actual independent Huber restart controls, before any quality claim."""
from pathlib import Path
from datetime import datetime, timezone, timedelta
import sys, os, gzip, hashlib
A=Path(__file__).resolve().parent; ROOT=A.parent
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    control=read(A/'current_user_runtime_control_20261010.json')
    assert control['status']=='optimization_active_after_explicit_manual_resume'
    assert datetime.now(timezone(timedelta(hours=8)))<datetime.fromisoformat(control['stop_at_local'])
    restart=Path(read(A/'actual_BF16_medium2048_huber010_seed09_restart_location_v1_20261009.json')['output'])
    small=Path('E:/赛题五_本机临时/BF16Huber010161_independent_small_CPU_v1_20261009')
    assert len(read(restart/'verification.json')['records'])==2
    assert read(small/'verification.json')['rows']==10017
    paths=[Path(__file__),ROOT/'后续选模标准.md',A/'run_continuous_fast_reused_frontiers_v9_20261010.py',A/'build_reused_neural_frontier_v6_20261010.py',A/'monitor_fast_optimization_v7_20261010.py',A/'actual_optimization_fast_runtime_handoff_v8_20261010.json',A/'remaining_feasible_optimization_frontier_fast_v5_20261010.json',A/'actual_full_ranking_decode_remaining_speed_direction_v1_20261010.json']
    for pattern in ('*huber010*.py','*huber010*.json','*Huber010161*.py','*Huber010161*.json'):
        paths.extend(p for p in A.glob(pattern) if p.is_file())
    paths.extend(restart.rglob('*.json'));paths.extend(small.glob('*.json'))
    for name in ('actual_BF16_medium2048_huber010_seed09_restart_control_v1_20261009','BF16Huber010161_independent_small_CPU_v1_20261009'):
        folder=A/'service_owned_workflows_20261006'/name
        assert read(folder/'service_execution.json')['status']=='passed'
        paths.extend(folder.glob('*.json'))
    import publish_classifier_consensus_workflows_20261006 as h
    prefix=Path('validation_sync/BF16Huber010161_pretraining_controls_v1_20261010'); payload={}; bindings={}
    for p in dict.fromkeys(paths):
        raw=p.read_bytes();assert not h.sync.SECRET.search(raw),p
        digest=hashlib.sha256(raw).hexdigest()
        rel=p.relative_to(ROOT) if p.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+p.name)
        name=(prefix/rel).as_posix(); data=raw
        if len(data)>=5*1024**2:data=gzip.compress(data,mtime=0);name+='.gz';assert gzip.decompress(data)==raw
        assert len(data)<95*1024**2;payload[name]=data;bindings[str(p)]={'path':name,'raw_sha256':digest}
    payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({'status':'actual_pretraining_controls_passed_not_scored_candidate','files':bindings,'own_Huber_delta':.1,'rank_target':True,'actual_restart_controls':['small32','wide2'],'actual_independent_CPU_rows':10017,'actual_CPU_prefix_lengths':[0,1,4097,8192],'complete_annual_training_not_yet_claimed':True,'quality_score_records':0,'future_X_read':False,'test_labels_read':False,'deadline_local':control['stop_at_local']})
    out=Path('E:/赛题五_本机临时/BF16Huber010161_pretraining_main_v1_20261010');out.mkdir(exist_ok=False)
    create(out/'frozen_before_publication.json',{'files':bindings})
    from lossless_chunked_safe_main_runtime_v1_20261009 import installed as safe
    from serial_main_publication_mutex_v1_20261009 import installed as serial
    from verified_TLS_Git_retry_runtime_v2_20261008 import installed as git_io
    from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
    with serial(out/'serial_mutex.json') as mutex,safe(out/'safe'),git_io(out/'file_backed_git'):
        mutex.acquire()
        assert datetime.now(timezone(timedelta(hours=8)))<datetime.fromisoformat(read(A/'current_user_runtime_control_20261010.json')['stop_at_local'])
        launch=read(A/'service_owned_workflows_20261006/main_publisher_v11_20261010/native_launch.json')
        parent,worker,idle=suspended_idle(launch,'    main (watch_validations_main_v7_20261006.py:71)')
        try:
            sync=h.sync;h.verify_main(sync.git('rev-parse','HEAD'));assert not sync.git('status','--porcelain')
            for name,data in payload.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(payload)
            for i in range(0,len(names),50):sync.git('add','-f','--',*names[i:i+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','保存新神经Huber排序损失公式、两项实际断点恢复及10017行独立CPU推理控制，尚未计分',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()}
            assert h.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);h.verify_main(commit);h.watcher.advance_source_index(commit)
            receipt={'status':'pushed_and_remote_head_verified','branch':'main','commit':commit,'raw_git_blobs_verified':len(hashes),'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()}
            create(out/'receipt.json',receipt);create(A/'BF16Huber010161_pretraining_controls_main_receipt_v1_20261010.json',receipt);print(receipt,flush=True)
        finally:
            for p in (parent,worker):
                if p.is_running():p.resume()

if __name__=='__main__':
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(key,value) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=key;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=value
    os.environ['GIT_CONFIG_COUNT']=str(count+2)
    main()
