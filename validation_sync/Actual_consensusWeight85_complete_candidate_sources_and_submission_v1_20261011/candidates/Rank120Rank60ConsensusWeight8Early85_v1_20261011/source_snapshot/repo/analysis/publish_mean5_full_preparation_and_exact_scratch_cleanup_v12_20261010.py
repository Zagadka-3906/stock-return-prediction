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
    paths=[Path(__file__)]+[Path(p) for p in ['D:\\3.Study\\数据分析\\赛题五\\analysis\\prepare_Recent252Forward5_own_bank_sources_v1_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\forward20_mature_training_labels_v1_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\recent252_forward20_mature_training_population_v1_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_forward20_mature_training_labels_v1_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_recent252_forward20_mature_population_v1_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\neural_BF16_medium2048_recent252forward20huber050_seed09_e64_native_v1_20261009.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\neural_BF16_medium2048_recent252forward20huber050_seed09_independent_forward_v2_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_medium_forward20_Huber050_targets_and_loss_v1_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_neural_BF16_medium2048_recent252forward20huber050_seed09_restart_v1_20261009.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_BF16Recent252Forward20Huber050170_independent_small_CPU_v1_20261009.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_BF16Recent252Forward20Huber050170_full5_independent_GPU_v1_20261009.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\BF16Recent252Forward20Huber050170_complete_parent_native_stage_v1_20261009.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_BF16Recent252Forward20Huber050170_native42_calendar_v1_20261009.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\train_neural_BF16_medium2048_recent252forward20huber050_seed09_e64_bank6_v1_20261009.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\forward5_mature_training_labels_v1_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\recent252_forward5_mature_training_population_v1_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_forward5_mature_training_labels_v1_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_recent252_forward5_mature_population_v1_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\neural_BF16_medium2048_recent252forward5huber050_seed09_e64_native_v1_20261009.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\neural_BF16_medium2048_recent252forward5huber050_seed09_independent_forward_v2_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_medium_forward5_Huber050_targets_and_loss_v1_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_neural_BF16_medium2048_recent252forward5huber050_seed09_restart_v1_20261009.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_BF16Recent252Forward5Huber050171_independent_small_CPU_v1_20261009.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_BF16Recent252Forward5Huber050171_full5_independent_GPU_v1_20261009.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\BF16Recent252Forward5Huber050171_complete_parent_native_stage_v1_20261009.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_BF16Recent252Forward5Huber050171_native42_calendar_v1_20261009.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\train_neural_BF16_medium2048_recent252forward5huber050_seed09_e64_bank6_v1_20261009.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\forward5_model_target_plan_v1_20261010.json', 'E:\\赛题五_本机临时\\Recent252Forward5Huber050_past_fixture_v2_20261010\\verification.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\forward5_mature_training_labels_actual_CPU_controls_v1_20261010.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\recent252_forward5_mature_population_actual_CPU_controls_v1_20261010.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\Forward5Huber050_independent_targets_loss_gradient_controls_v1_20261010.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\cleanup_completed_after167_score_csv_v1_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\completed_after167_score_csv_cleanup_v1_20261010\\frozen_before_exact_file_deletion.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\completed_after167_score_csv_cleanup_v1_20261010\\verification.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\Recent252Forward5Huber050_own_bank_controls_source_admission_v1_20261010.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\run_recent252_forward5_own_controls_and_training_queue_v1_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\run_Recent252Forward5_after168_high_impact65_screen_v1_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\publish_Recent252Forward5_after168_65_completion_v25_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\publish_Recent252Forward5_after168_65_completion_v26_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\Recent252Forward5_after168_E_scoring65_source_preparation_v1_20261010.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\service_owned_workflows_20261006\\actual_Recent252Forward5_after168_65_completion_main_v25_20261010\\service_execution.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\service_owned_workflows_20261006\\actual_Recent252Forward5_after168_65_completion_main_v25_20261010\\stderr.log', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\actual_BF16_medium2048_recent252forward5huber050_seed09_restart_location_v1_20261009.json', 'E:\\赛题五_本机临时\\GPU实测_20261009\\BF16_medium2048_recent252forward5huber050_seed09_restart_v1\\verification.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\actual_Recent252Forward5Huber050_past_fixture_location_v2_20261010.json', 'E:\\赛题五_本机临时\\BF16Recent252Forward5Huber050171_independent_small_CPU_v1_20261009\\verification.json']]
    import publish_classifier_consensus_workflows_20261006 as h
    prefix=Path('validation_sync/mean5_full_preparation_and_exact_scratch_cleanup_v12_20261010'); payload={}; bindings={}
    for p in dict.fromkeys(paths):
        raw=p.read_bytes();assert not h.sync.SECRET.search(raw),p
        digest=hashlib.sha256(raw).hexdigest()
        rel=p.relative_to(ROOT) if p.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+p.name)
        name=(prefix/rel).as_posix(); data=raw
        if len(data)>=5*1024**2:data=gzip.compress(data,mtime=0);name+='.gz';assert gzip.decompress(data)==raw
        assert len(data)<95*1024**2;payload[name]=data;bindings[str(p)]={'path':name,'raw_sha256':digest}
    payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({'status':'passed_mean5_14_population20_loss_CPU49153_fixture_and_own_restart_CPU10017_and_prepared65_official_screen_audited444470849_bytes_scratch_cleanup','files':bindings,'new_mean5_six_fit_and_score_completion_not_claimed':True,'new_quality_scores_by_publication':0,'test_labels_read':False,'deadline_local':control['stop_at_local']})
    out=Path('E:/赛题五_本机临时/mean5_full_preparation_and_exact_scratch_cleanup_main_v12_20261010');out.mkdir(exist_ok=False)
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
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','保存新5日目标训练与65项评分队列、GPU恢复和CPU10017检查及已完成评分CSV精确清理',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()}
            assert h.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);h.verify_main(commit);h.watcher.advance_source_index(commit)
            receipt={'status':'pushed_and_remote_head_verified','branch':'main','commit':commit,'raw_git_blobs_verified':len(hashes),'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()}
            create(out/'receipt.json',receipt);create(A/'mean5_full_preparation_and_exact_scratch_cleanup_main_receipt_v12_20261010.json',receipt);print(receipt,flush=True)
        finally:
            for p in (parent,worker):
                if p.is_running():p.resume()

if __name__=='__main__':
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(key,value) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=key;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=value
    os.environ['GIT_CONFIG_COUNT']=str(count+2)
    main()
