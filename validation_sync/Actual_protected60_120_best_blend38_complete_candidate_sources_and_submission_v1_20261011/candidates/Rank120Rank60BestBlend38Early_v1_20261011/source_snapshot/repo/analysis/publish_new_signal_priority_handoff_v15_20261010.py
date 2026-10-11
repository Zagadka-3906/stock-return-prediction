"""Publish the actual independent Huber restart controls, before any quality claim."""
from pathlib import Path
from datetime import datetime, timezone, timedelta
import sys, os, gzip, hashlib
A=Path(__file__).resolve().parent; ROOT=A.parent
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    read(A/'current_user_runtime_control_20261009.json')
    control=read(A/'current_user_runtime_control_20261010.json')
    assert control['status']=='optimization_active_after_explicit_manual_resume'
    assert datetime.now(timezone(timedelta(hours=8)))<datetime.fromisoformat(control['stop_at_local'])
    proof=read(A/'ReturnHuber050_independent_targets_loss_gradient_controls_v1_20261010.json')
    assert len(proof['records'])==20 and proof['status'].startswith('passed20_CPU')
    admission=read(A/'ReturnHuber050_own_bank_controls_source_admission_v1_20261010.json')
    for p,d in admission['input_sha256'].items():assert sha(p)==d,p
    fixture=Path(read(A/'actual_ReturnHuber050_past_fixture_location_v1_20261010.json')['output'])
    paths=[Path(__file__),A/'prepare_ReturnHuber050_CPU_evidence_publication_v1_20261010.py',A/'ReturnHuber050_independent_targets_loss_gradient_controls_v1_20261010.json',A/'ReturnHuber050_own_bank_controls_source_admission_v1_20261010.json',A/'actual_ReturnHuber050_past_fixture_location_v1_20261010.json',fixture/'verification.json',ROOT/'后续选模标准.md']
    for pattern in ('*returnhuber050*.py','*returnhuber050*.json','*ReturnHuber050*.py','*ReturnHuber050*.json','prepare_medium_return_Huber050*.py','verify_medium_return_Huber050*.py','prepare_returnHuber050*.py'):
        paths.extend(p for p in A.glob(pattern) if p.is_file())
    paths.extend(A/name for name in ['record_and_publish_new_signal_priority_v15_20261010.py', 'actual_optimization_fast_runtime_handoff_v15_20261010.json', 'round164_actual_scope_prose_correction_v1_20261010.json', 'prepare_new_return_priority_controller_v19_20261010.py', 'run_continuous_fast_reused_frontiers_v19_20261010.py', 'handoff_new_return_priority_controller_v19_20261010.py', 'new_return_priority_handoff_v19_20261010/verification.json', 'new_return_priority_handoff_v19_20261010/frozen_before_handoff.json', 'prepare_progress_observer19_new_return_v1_20261010.py', 'monitor_fast_optimization_v19_20261010.py', 'actual_fast_optimization_progress_v19_handoff_v1_20261010.json', 'prepare_TopWeighted65_completion_main_v12_20261010.py', 'publish_TopWeighted_after163_65_completion_v12_20261010.py', 'TopWeighted_after163_65_completion_main_hidden_launch_v12_20261010.json', 'completed164_temporal73_transient_csv_cleanup_v1_20261010/verification.json'])
    import publish_classifier_consensus_workflows_20261006 as h
    prefix=Path('validation_sync/new_signal_priority_handoff_v15_20261010'); payload={}; bindings={}
    for p in dict.fromkeys(paths):
        raw=p.read_bytes();assert not h.sync.SECRET.search(raw),p
        digest=hashlib.sha256(raw).hexdigest()
        rel=p.relative_to(ROOT) if p.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+p.name)
        name=(prefix/rel).as_posix(); data=raw
        if len(data)>=5*1024**2:data=gzip.compress(data,mtime=0);name+='.gz';assert gzip.decompress(data)==raw
        assert len(data)<95*1024**2;payload[name]=data;bindings[str(p)]={'path':name,'raw_sha256':digest}
    payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({'status':'actual_CPU20_target_loss_gradient_checks_and_real_mature_fixture_passed','files':bindings,'actual_CPU_controls':20,'target':'y_ret_1d','target_scale':20.,'train_only_winsor_quantiles':[.005,.995],'Huber_delta':.5,'GPU_restart_checks_not_yet_executed':True,'actual_annual_fits':0,'quality_score_records':0,'future_X_read':False,'test_labels_read':False,'raw_fixture_arrays_uploaded':False,'deadline_local':control['stop_at_local']})
    out=Path('E:/赛题五_本机临时/new_signal_priority_handoff_main_v15_20261010');out.mkdir(exist_ok=False)
    create(out/'frozen_before_publication.json',{'files':bindings})
    from lossless_chunked_safe_main_runtime_v1_20261009 import installed as safe
    from serial_main_publication_mutex_v1_20261009 import installed as serial
    from verified_TLS_Git_retry_runtime_v2_20261008 import installed as git_io
    from owned_idle_publication_wait_runtime_v1_20261010 import hold as suspended_idle
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
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','优先新训练目标并保留科学进程：Top加权与直接收益率宽网络，修正164轮继承说明文字',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()}
            assert h.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);h.verify_main(commit);h.watcher.advance_source_index(commit)
            receipt={'status':'pushed_and_remote_head_verified','branch':'main','commit':commit,'raw_git_blobs_verified':len(hashes),'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()}
            create(out/'receipt.json',receipt);create(A/'new_signal_priority_handoff_main_receipt_v15_20261010.json',receipt);print(receipt,flush=True)
        finally:
            for p in (parent,worker):
                if p.is_running():p.resume()

if __name__=='__main__':
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(key,value) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=key;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=value
    os.environ['GIT_CONFIG_COUNT']=str(count+2)
    main()
