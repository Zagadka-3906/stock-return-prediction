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
    assert read(A/'service_owned_workflows_20261006/BF16Recent252Forward20Huber050170_independent_small_CPU_v1_20261009/service_execution.json')['status']=='passed'
    paths=[Path(__file__),ROOT/'后续选模标准.md']+[A/name for name in ['prepare_recent252_protected_fine31_after167_v1_20261010.py', 'run_RecentReturn252_after167_protected_fine31_screen_v1_20261010.py', 'RecentReturn252_after167_protected_fine31_source_admission_v1_20261010.json', 'publish_RecentReturn252_after167_protected_fine31_completion_v22_20261010.py', 'cleanup_completed_Forward20_after163_score_csv_v1_20261010.py', 'completed_Forward20_after163_score_csv_cleanup_v1_20261010/frozen_before_exact_file_deletion.json', 'completed_Forward20_after163_score_csv_cleanup_v1_20261010/verification.json', 'run_Recent252Forward20_after168_high_impact65_screen_v1_20261010.py', 'publish_Recent252Forward20_after168_65_completion_v21_20261010.py', 'complete_recent252_forward20_qualified_screen_and_main_queue_v1_20261010.py', 'Recent252Forward20_after168_E_scoring65_source_preparation_v1_20261010.json', 'RecentReturn252Protected168_actual_candidate_readonly_stack_v1_20261010.json', 'RecentReturn252Protected168_actual_full_registration_readonly_stack_v1_20261010.json', 'actual_BF16_medium2048_recent252forward20huber050_seed09_restart_location_v1_20261009.json']]
    paths.extend([Path('E:\\赛题五_本机临时\\BF16Recent252Forward20Huber050170_independent_small_CPU_v1_20261009\\verification.json'),Path('E:\\赛题五_本机临时\\GPU实测_20261009\\BF16_medium2048_recent252forward20huber050_seed09_restart_v1\\verification.json')])
    import publish_classifier_consensus_workflows_20261006 as h
    prefix=Path('validation_sync/fine31_E_scoring_and_joint_GPU_controls_v9_20261010'); payload={}; bindings={}
    for p in dict.fromkeys(paths):
        raw=p.read_bytes();assert not h.sync.SECRET.search(raw),p
        digest=hashlib.sha256(raw).hexdigest()
        rel=p.relative_to(ROOT) if p.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+p.name)
        name=(prefix/rel).as_posix(); data=raw
        if len(data)>=5*1024**2:data=gzip.compress(data,mtime=0);name+='.gz';assert gzip.decompress(data)==raw
        assert len(data)<95*1024**2;payload[name]=data;bindings[str(p)]={'path':name,'raw_sha256':digest}
    payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({'status':'passed_joint_recent252_mean20_small32_wide2_GPU_restart_and_CPU10017_oracle_fine31_and_E_only_screen_preparation_audited_scratch_cleanup','files':bindings,'new_recent252_mean20_GPU_and_round168_full_candidate_completion_not_claimed':True,'new_quality_scores_by_publication':0,'test_labels_read':False,'deadline_local':control['stop_at_local']})
    out=Path('E:/赛题五_本机临时/fine31_E_scoring_and_joint_GPU_controls_main_v9_20261010');out.mkdir(exist_ok=False)
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
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','保存近期252日与20日收益联合方案GPU可恢复训练和CPU10017检查、31项局部参数验证与E盘评分准备、已完成评分CSV清理',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()}
            assert h.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);h.verify_main(commit);h.watcher.advance_source_index(commit)
            receipt={'status':'pushed_and_remote_head_verified','branch':'main','commit':commit,'raw_git_blobs_verified':len(hashes),'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()}
            create(out/'receipt.json',receipt);create(A/'fine31_E_scoring_and_joint_GPU_controls_main_receipt_v9_20261010.json',receipt);print(receipt,flush=True)
        finally:
            for p in (parent,worker):
                if p.is_running():p.resume()

if __name__=='__main__':
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(key,value) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=key;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=value
    os.environ['GIT_CONFIG_COUNT']=str(count+2)
    main()
