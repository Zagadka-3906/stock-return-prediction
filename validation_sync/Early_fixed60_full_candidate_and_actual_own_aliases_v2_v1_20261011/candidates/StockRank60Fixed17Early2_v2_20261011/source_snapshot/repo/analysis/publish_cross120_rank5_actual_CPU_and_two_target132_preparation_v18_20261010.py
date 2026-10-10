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
    assert read(A/'cross120_rank5_real49153_mature_fixture_alignment_actual_CPU_controls_v1_20261010.json')['status'].startswith('passed')
    paths=[Path(__file__)]+[Path(p) for p in ['D:\\3.Study\\数据分析\\赛题五\\analysis\\prepare_cross120_recent252_rank5_own_sources_v1_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\Cross120Recent252Rank5Huber050_own_bank_controls_source_admission_v1_20261010.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_cross120_rank5_real_mature_fixture_alignment_v1_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\cross120_rank5_real49153_mature_fixture_alignment_actual_CPU_controls_v1_20261010.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\cross120_rank5_source_and_actual_CPU_metadata_clarification_v1_20261010.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\actual_Cross120Recent252Rank5Huber050_past_fixture_location_v2_20261010.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\run_cross120_recent252_rank5_own_controls_and_training_queue_v1_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\run_Cross120Recent252Rank5_after169_high_impact65_screen_v1_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\publish_Cross120Recent252Rank5_after169_65_completion_v30_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\cross120_two_target132_complete_comparison_selection_plan_v1_20261010.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_exact_E_TRAIN_selected169_all8_compatibility_queue_v1_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\actual_exact_E_TRAIN_selected169_all8_compatibility_queue_activation_v1_20261010.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\actual_optimization_fast_runtime_handoff_v40_20261010.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\monitor_fast_optimization_v34_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\observer33_retired_after_actual34_verified_v1_20261010.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\fast_high_gain_direction_priority_actual_evidence_v1_20261010.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\fast_high_gain_direction_priority_actual_evidence_v2_20261010.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\fast_high_gain_direction_priority_actual_progress_snapshot_v2_20261010.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\BF16Cross120Recent252Rank5Huber050174_complete_parent_native_stage_v1_20261009.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\neural_BF16_medium2048_cross120recent252rank5huber050_seed09_e64_native_v1_20261009.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\train_neural_BF16_medium2048_cross120recent252rank5huber050_seed09_e64_bank6_v1_20261009.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_BF16Cross120Recent252Rank5Huber050174_full5_independent_GPU_v1_20261009.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_BF16Cross120Recent252Rank5Huber050174_independent_small_CPU_v1_20261009.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_BF16Cross120Recent252Rank5Huber050174_native42_calendar_v1_20261009.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_neural_BF16_medium2048_cross120recent252rank5huber050_seed09_restart_v1_20261009.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\BF16Cross120Recent252Rank5Huber050174_complete_parent_native_stage_v1_20261009.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_BF16Cross120Recent252Rank5Huber050174_full5_independent_GPU_v1_20261009.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_BF16Cross120Recent252Rank5Huber050174_independent_small_CPU_v1_20261009.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_BF16Cross120Recent252Rank5Huber050174_native42_calendar_v1_20261009.py']]
    import publish_classifier_consensus_workflows_20261006 as h
    prefix=Path('validation_sync/cross120_rank5_actual_CPU_and_two_target132_preparation_v18_20261010'); payload={}; bindings={}
    for p in dict.fromkeys(paths):
        raw=p.read_bytes();assert not h.sync.SECRET.search(raw),p
        digest=hashlib.sha256(raw).hexdigest()
        rel=p.relative_to(ROOT) if p.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+p.name)
        name=(prefix/rel).as_posix(); data=raw
        if len(data)>=5*1024**2:data=gzip.compress(data,mtime=0);name+='.gz';assert gzip.decompress(data)==raw
        assert len(data)<95*1024**2;payload[name]=data;bindings[str(p)]={'path':name,'raw_sha256':digest}
    payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({'status':'passed_real49153_rank5_encoded120_independent_stock_date_and_Pandas_alignment_with_two_target132_plan_and_provisional169_E_guard_proof_queue_GPU_pending','files':bindings,'new_encoder120_GPU_models_and_quality_score_completion_not_claimed':True,'new_quality_scores_by_publication':0,'test_labels_read':False,'deadline_local':control['stop_at_local']})
    out=Path('E:/赛题五_本机临时/cross120_rank5_actual_CPU_and_two_target132_preparation_main_v18_20261010');out.mkdir(exist_ok=False)
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
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','保存120维5日排名模型49153行独立CPU校验、自有训练队列及双目标132项比较预案',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()}
            assert h.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);h.verify_main(commit);h.watcher.advance_source_index(commit)
            receipt={'status':'pushed_and_remote_head_verified','branch':'main','commit':commit,'raw_git_blobs_verified':len(hashes),'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()}
            create(out/'receipt.json',receipt);create(A/'cross120_rank5_actual_CPU_and_two_target132_preparation_main_receipt_v18_20261010.json',receipt);print(receipt,flush=True)
        finally:
            for p in (parent,worker):
                if p.is_running():p.resume()

if __name__=='__main__':
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(key,value) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=key;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=value
    os.environ['GIT_CONFIG_COUNT']=str(count+2)
    main()
