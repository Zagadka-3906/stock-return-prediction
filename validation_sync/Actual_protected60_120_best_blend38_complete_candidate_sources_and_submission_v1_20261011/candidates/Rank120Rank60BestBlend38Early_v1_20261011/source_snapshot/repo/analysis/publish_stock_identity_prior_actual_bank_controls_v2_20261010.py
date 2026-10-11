"""Publish the actual independent Huber restart controls, before any quality claim."""
from pathlib import Path
from datetime import datetime, timezone, timedelta
import sys, os, gzip, hashlib, time
A=Path(__file__).resolve().parent; ROOT=A.parent
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def main():
    read(A/'current_user_runtime_control_20261009.json')
    control=read(A/'current_user_runtime_control_20261010.json')
    assert control['status']=='optimization_active_after_explicit_manual_resume'
    assert datetime.now(timezone(timedelta(hours=8)))<datetime.fromisoformat(control['stop_at_local'])
    folder=A/'service_owned_workflows_20261006/actual_stock_identity_excess_prior_bank6_v3_20261010'
    while not (folder/'service_execution.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(10)
    assert read(folder/'service_execution.json')['status']=='passed'
    bank=Path(read(A/'actual_stock_identity_excess_prior_bank6_location_v3_20261010.json')['output'])
    proof=read(bank/'verification.json');assert proof['actual_native_fits']==6 and proof['actual_full_independent_OOF_cases']==5 and proof['actual_cold_prefix_cases']==15
    paths=[Path(__file__),ROOT/'后续选模标准.md',A/'completed158_to161_transient_score_csv_cleanup_v1_20261010/verification.json',A/'cleanup_completed158_to161_transient_score_csv_v1_20261010.py']
    for pattern in ('*stock_identity*prior*.py','*stock_identity*prior*.json'):
        paths.extend(p for p in A.glob(pattern) if p.is_file())
    paths.extend(A/name for name in ('monitor_fast_optimization_v21_20261010.py','actual_fast_optimization_progress_v21_handoff_v1_20261010.json','actual_optimization_fast_runtime_handoff_v17_20261010.json'))
    paths.extend(bank.rglob('*.json'))
    for name in ('actual_stock_identity_excess_prior_bank6_v1_20261010','actual_stock_identity_excess_prior_bank6_v2_20261010','actual_stock_identity_excess_prior_bank6_v3_20261010','actual_stock_identity_prior_after163_screen33_v1_20261010','actual_stock_identity_prior_after163_screen33_v2_20261010'):
        folder=A/'service_owned_workflows_20261006'/name;paths.extend(folder.glob('*.json'));paths.extend(folder.glob('*.log'))
    import publish_classifier_consensus_workflows_20261006 as h
    prefix=Path('validation_sync/stock_identity_prior_actual_bank_controls_v2_20261010'); payload={}; bindings={}
    for p in dict.fromkeys(paths):
        raw=p.read_bytes();assert not h.sync.SECRET.search(raw),p
        digest=hashlib.sha256(raw).hexdigest()
        rel=p.relative_to(ROOT) if p.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+p.name)
        name=(prefix/rel).as_posix(); data=raw
        if len(data)>=5*1024**2:data=gzip.compress(data,mtime=0);name+='.gz';assert gzip.decompress(data)==raw
        assert len(data)<95*1024**2;payload[name]=data;bindings[str(p)]={'path':name,'raw_sha256':digest}
    payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({'status':'passed_actual6_mature_stock_identity_fits_full5_independent_and15_prefixes_not_scored','files':bindings,'actual_CPU_fit_formula_controls':4,'actual_native_fits':6,'full_independent_OOF_cases':5,'cold_prefix_cases':15,'training_target':'per_day_demeaned_clipped_y_ret_1d','target_promoted_Float64_before_aggregation':True,'window_days':756,'zero_prior_pseudo_days':252,'new_quality_scores':0,'original_failed_attempts_retained':True,'model_tensors_raw_features_labels_not_uploaded':True,'submission_qualified':False,'test_labels_read':False,'deadline_local':control['stop_at_local']})
    out=Path('E:/赛题五_本机临时/stock_identity_prior_actual_bank_controls_main_v2_20261010');out.mkdir(exist_ok=False)
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
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','保存股票身份超额收益先验六项真实成熟拟合、全量独立前缀验证及失败尝试记录',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()}
            assert h.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);h.verify_main(commit);h.watcher.advance_source_index(commit)
            receipt={'status':'pushed_and_remote_head_verified','branch':'main','commit':commit,'raw_git_blobs_verified':len(hashes),'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()}
            create(out/'receipt.json',receipt);create(A/'stock_identity_prior_actual_bank_controls_main_receipt_v2_20261010.json',receipt);print(receipt,flush=True)
        finally:
            for p in (parent,worker):
                if p.is_running():p.resume()

if __name__=='__main__':
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(key,value) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=key;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=value
    os.environ['GIT_CONFIG_COUNT']=str(count+2)
    main()
