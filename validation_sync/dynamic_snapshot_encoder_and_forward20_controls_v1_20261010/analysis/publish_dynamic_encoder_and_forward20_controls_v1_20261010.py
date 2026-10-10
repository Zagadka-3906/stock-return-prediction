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
    assert len(read(A/'dynamic_snapshot_encoder_binding_actual_controls_v1_20261010.json')['records'])==20
    assert len(read(A/'actual165_dynamic_snapshot_encoder_binding_controls_v1_20261010.json')['records'])==3
    assert len(read(A/'forward20_mature_training_labels_actual_CPU_controls_v1_20261010.json')['records'])==7
    paths=[Path(__file__),ROOT/'后续选模标准.md']+[A/name for name in ['byte_exact_dynamic_snapshot_encoder_runtime_v1_20261010.py', 'verify_dynamic_snapshot_encoder_binding_v1_20261010.py', 'dynamic_snapshot_encoder_binding_actual_controls_v1_20261010.json', 'verify_actual165_dynamic_snapshot_encoder_binding_v1_20261010.py', 'actual165_dynamic_snapshot_encoder_binding_controls_v1_20261010.json', 'build_reused_return_neural_frontier_v13_20261010.py', 'return_frontier13_actual_template_injection_controls_v1_20261010.json', 'run_new_return_dynamic_publication_controller_v21_20261010.py', 'return_dynamic_encoder_controller_handoff_v21_20261010.json', 'verified_TLS_Git_retry_runtime_v3_20261010.py', 'reconcile_stock33_already_pushed_main_v1_20261010.py', 'high_impact_priority_huber65_main_receipt_v14_20261010.json', 'forward20_mature_training_labels_v1_20261010.py', 'verify_forward20_mature_training_labels_v1_20261010.py', 'forward20_mature_training_labels_actual_CPU_controls_v1_20261010.json']]
    paths.extend(Path('E:/赛题五_本机临时/stock33_already_pushed_main_reconciliation_v1_20261010').glob('*.json'))
    import publish_classifier_consensus_workflows_20261006 as h
    prefix=Path('validation_sync/dynamic_snapshot_encoder_and_forward20_controls_v1_20261010'); payload={}; bindings={}
    for p in dict.fromkeys(paths):
        raw=p.read_bytes();assert not h.sync.SECRET.search(raw),p
        digest=hashlib.sha256(raw).hexdigest()
        rel=p.relative_to(ROOT) if p.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+p.name)
        name=(prefix/rel).as_posix(); data=raw
        if len(data)>=5*1024**2:data=gzip.compress(data,mtime=0);name+='.gz';assert gzip.decompress(data)==raw
        assert len(data)<95*1024**2;payload[name]=data;bindings[str(p)]={'path':name,'raw_sha256':digest}
    payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({'status':'passed_actual_dynamic_encoder_and_future20_label_CPU_controls_pending166_runtime','files':bindings,'actual_dynamic_namespace_byte_cases':20,'actual_published165_metadata_byte_cases':3,'existing_full_parameter_byte_proof_rows':15595,'actual_forward20_label_cases':7,'forward20_annual_fits':0,'new_quality_scores':0,'stock33_already_pushed_remote_receipt_reconciled_without_rescoring':True,'new_166_encoding_speed_not_yet_measured':True,'test_labels_read':False,'deadline_local':control['stop_at_local']})
    out=Path('E:/赛题五_本机临时/dynamic_snapshot_encoder_and_forward20_controls_main_v1_20261010');out.mkdir(exist_ok=False)
    create(out/'frozen_before_publication.json',{'files':bindings})
    from lossless_chunked_safe_main_runtime_v1_20261009 import installed as safe
    from serial_main_publication_mutex_v1_20261009 import installed as serial
    from verified_TLS_Git_retry_runtime_v3_20261010 import installed as git_io
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
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','保存20项动态命名空间字节检查、真实165模块校验、7项20日标签成熟检查与main回执修复',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()}
            assert h.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);h.verify_main(commit);h.watcher.advance_source_index(commit)
            receipt={'status':'pushed_and_remote_head_verified','branch':'main','commit':commit,'raw_git_blobs_verified':len(hashes),'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()}
            create(out/'receipt.json',receipt);create(A/'dynamic_snapshot_encoder_and_forward20_controls_main_receipt_v1_20261010.json',receipt);print(receipt,flush=True)
        finally:
            for p in (parent,worker):
                if p.is_running():p.resume()

if __name__=='__main__':
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(key,value) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=key;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=value
    os.environ['GIT_CONFIG_COUNT']=str(count+2)
    main()
