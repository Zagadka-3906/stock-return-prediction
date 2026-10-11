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
    assert read(A/'immutable_prepared_rank_panel_cache_actual_full_TRAIN_benchmark_v1_20261010.json')['status'].startswith('passed')
    assert read(A/'dual_target_rank_consensus_actual13950_TRAIN_and_ties_CPU_controls_v1_20261010.json')['status'].startswith('passed')
    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import closed
    closed('FastNeuralFrontier169_round169_full_registration_external_capsule_resume_v3_20261010')
    paths=[Path(__file__)]+[A/name for name in ['prepare_cross120_recent252_return1d_own_sources_v1_20261010.py', 'resume_cross120_return1d_generated_admission_and_queue_v2_20261010.py', 'Cross120RecentReturn252Huber050_own_bank_controls_source_admission_v1_20261010.json', 'cross120_return1d_preparation_queue_gate_two_literal_references_recovery_v2_20261010.json', 'actual_Cross120RecentReturn252Huber050_past_fixture_location_v1_20261010.json', 'run_cross120_recent252_return_own_controls_and_training_queue_v2_20261010.py', 'actual_cross120_recent252_return_own_controls_and_training_queue_activation_v2_20261010.json', 'run_Cross120RecentReturn252_after169_high_impact81_screen_v1_20261010.py', 'cross120_return1d81_predeclared_training_only_selection_plan_v1_20261010.json', 'actual_cross120_return1d81_TRAIN_only_screen_activation_v1_20261010.json', 'publish_cross120_return1d81_completion_v40_20261010.py', 'run_parent170_causal_Top_stability19_screen_v1_20261010.py', 'parent170_causal_Top_stability19_predeclared_joint_application_plan_v1_20261010.json', 'actual_parent170_causal_Top_stability19_screen_activation_v1_20261010.json', 'publish_parent170_causal_Top_stability19_completion_v41_20261010.py', 'frontier233_after169_and170_complete_comparison_predeclared_plan_v1_20261010.json', 'normalize_completed_frontier233_after169_and170_v1_20261010.py', 'actual_frontier233_after169_and170_normalization_activation_v1_20261010.json', 'monitor_fast_optimization_v40_20261010.py', 'observer39_retired_after_actual40_verified_v1_20261010.json', 'actual_optimization_fast_runtime_handoff_v58_20261010.json', 'parent169_causal_Top_stability19_completion_main_receipt_v39_20261010.json']]
    paths.extend(Path(path) for path in read(A/'Cross120RecentReturn252Huber050_own_bank_controls_source_admission_v1_20261010.json')['input_sha256'] if Path(path).suffix=='.py')
    paths.append(Path(read(A/'actual_Cross120RecentReturn252Huber050_past_fixture_location_v1_20261010.json')['output'])/'verification.json')
    import publish_classifier_consensus_workflows_20261006 as h
    prefix=Path('validation_sync/actual_return1d120_81_and_joint_stability233_preparation_v25_20261010'); payload={}; bindings={}
    for p in dict.fromkeys(paths):
        raw=p.read_bytes();assert not h.sync.SECRET.search(raw),p
        digest=hashlib.sha256(raw).hexdigest()
        rel=p.relative_to(ROOT) if p.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+p.name)
        name=(prefix/rel).as_posix(); data=raw
        if len(data)>=5*1024**2:data=gzip.compress(data,mtime=0);name+='.gz';assert gzip.decompress(data)==raw
        assert len(data)<95*1024**2;payload[name]=data;bindings[str(p)]={'path':name,'raw_sha256':digest}
    payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({'status':'passed_actual49153_return1d120_mature_feature_admission_predeclared81_and_completed_parent16919_positive_evidence_predeclared233_future_qualification_pending','files':bindings,'new_encoder120_GPU_models_and_quality_score_completion_not_claimed':True,'new_quality_scores_by_publication':0,'test_labels_read':False,'deadline_local':control['stop_at_local']})
    out=Path('E:/赛题五_本机临时/actual_return1d120_81_and_joint_stability233_preparation_main_v25_20261010');out.mkdir(exist_ok=False)
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
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','保存120维一天收益模型49153条真实成熟训练特征与完整独立准入及81项预定验证；追加持仓稳定叠加与完整233选模流程',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()}
            assert h.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);h.verify_main(commit);h.watcher.advance_source_index(commit)
            receipt={'status':'pushed_and_remote_head_verified','branch':'main','commit':commit,'raw_git_blobs_verified':len(hashes),'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()}
            create(out/'receipt.json',receipt);create(A/'actual_return1d120_81_and_joint_stability233_preparation_main_receipt_v25_20261010.json',receipt);print(receipt,flush=True)
        finally:
            for p in (parent,worker):
                if p.is_running():p.resume()

if __name__=='__main__':
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(key,value) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=key;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=value
    os.environ['GIT_CONFIG_COUNT']=str(count+2)
    main()
