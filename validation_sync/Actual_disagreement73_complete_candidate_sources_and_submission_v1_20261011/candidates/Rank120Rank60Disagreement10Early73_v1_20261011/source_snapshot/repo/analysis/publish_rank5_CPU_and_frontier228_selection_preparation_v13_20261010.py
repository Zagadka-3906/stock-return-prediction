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
    paths=[Path(__file__)]+[Path(p) for p in ['D:\\3.Study\\数据分析\\赛题五\\analysis\\prepare_Recent252Rank5_own_bank_sources_v1_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\neural_BF16_medium2048_recent252forward5huber050_seed09_e64_native_v1_20261009.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\neural_BF16_medium2048_recent252forward5huber050_seed09_independent_forward_v2_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_medium_forward5_Huber050_targets_and_loss_v1_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_neural_BF16_medium2048_recent252forward5huber050_seed09_restart_v1_20261009.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_BF16Recent252Forward5Huber050171_independent_small_CPU_v1_20261009.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_BF16Recent252Forward5Huber050171_full5_independent_GPU_v1_20261009.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\BF16Recent252Forward5Huber050171_complete_parent_native_stage_v1_20261009.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_BF16Recent252Forward5Huber050171_native42_calendar_v1_20261009.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\train_neural_BF16_medium2048_recent252forward5huber050_seed09_e64_bank6_v1_20261009.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\neural_BF16_medium2048_recent252rank5huber050_seed09_e64_native_v1_20261009.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\neural_BF16_medium2048_recent252rank5huber050_seed09_independent_forward_v2_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_medium_rank5_Huber050_targets_and_loss_v1_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_neural_BF16_medium2048_recent252rank5huber050_seed09_restart_v1_20261009.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_BF16Recent252Rank5Huber050172_independent_small_CPU_v1_20261009.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_BF16Recent252Rank5Huber050172_full5_independent_GPU_v1_20261009.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\BF16Recent252Rank5Huber050172_complete_parent_native_stage_v1_20261009.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_BF16Recent252Rank5Huber050172_native42_calendar_v1_20261009.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\train_neural_BF16_medium2048_recent252rank5huber050_seed09_e64_bank6_v1_20261009.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\rank5_model_target_plan_v1_20261010.json', 'E:\\赛题五_本机临时\\Recent252Rank5Huber050_past_fixture_v2_20261010\\verification.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\recent252_rank5_mature_training_population_v1_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\recent252_rank5_mature_population_actual_CPU_controls_v1_20261010.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\Rank5Huber050_independent_targets_loss_gradient_controls_v1_20261010.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_recent252_rank5_mature_population_v1_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\Recent252Rank5Huber050_own_bank_controls_source_admission_v1_20261010.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\run_recent252_rank5_own_controls_and_training_queue_v1_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\run_Recent252Rank5_after168_high_impact65_screen_v1_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\publish_Recent252Rank5_after168_65_completion_v27_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\Recent252Rank5_after168_E_scoring65_source_preparation_v1_20261010.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\fast_neural_frontier228_selection_plan_v1_20261010.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\high_impact_priority_huber65_main_receipt_v23_20261010.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\actual_fast_optimization_progress_v31_activation_v1_20261010.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\monitor_fast_optimization_v31_20261010.py']]
    import publish_classifier_consensus_workflows_20261006 as h
    prefix=Path('validation_sync/rank5_CPU_and_frontier228_selection_preparation_v13_20261010'); payload={}; bindings={}
    for p in dict.fromkeys(paths):
        raw=p.read_bytes();assert not h.sync.SECRET.search(raw),p
        digest=hashlib.sha256(raw).hexdigest()
        rel=p.relative_to(ROOT) if p.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+p.name)
        name=(prefix/rel).as_posix(); data=raw
        if len(data)>=5*1024**2:data=gzip.compress(data,mtime=0);name+='.gz';assert gzip.decompress(data)==raw
        assert len(data)<95*1024**2;payload[name]=data;bindings[str(p)]={'path':name,'raw_sha256':digest}
    payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({'status':'passed_new_rank5_scalar_tied_rank7_and_loss_gradient20_CPU_controls_real49153_fixture_and_predeclared4_family228_complete_selection','files':bindings,'new_rank5_GPU_models_and_four_family_all_scores_and_full169_completion_not_claimed':True,'new_quality_scores_by_publication':0,'test_labels_read':False,'deadline_local':control['stop_at_local']})
    out=Path('E:/赛题五_本机临时/rank5_CPU_and_frontier228_selection_preparation_main_v13_20261010');out.mkdir(exist_ok=False)
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
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','保存新5日收益排名目标独立CPU因果与损失检查、GPU队列及4族228项正式选模准备',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()}
            assert h.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);h.verify_main(commit);h.watcher.advance_source_index(commit)
            receipt={'status':'pushed_and_remote_head_verified','branch':'main','commit':commit,'raw_git_blobs_verified':len(hashes),'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()}
            create(out/'receipt.json',receipt);create(A/'rank5_CPU_and_frontier228_selection_preparation_main_receipt_v13_20261010.json',receipt);print(receipt,flush=True)
        finally:
            for p in (parent,worker):
                if p.is_running():p.resume()

if __name__=='__main__':
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(key,value) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=key;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=value
    os.environ['GIT_CONFIG_COUNT']=str(count+2)
    main()
