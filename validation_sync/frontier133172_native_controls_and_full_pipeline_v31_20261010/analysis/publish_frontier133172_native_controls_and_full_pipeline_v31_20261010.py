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
    from prepare_frontier233171_full_registry_sources_v1_20261010 import source_paths
    from prepare_frontier133172_full_registry_sources_v2_20261010 import source_paths
    paths=[Path(__file__),*source_paths()]+[A/n for n in ['frontier133_native_single_leaf_and_complete_parent_predictor_sources_preparation_v1_20261010.json', 'frontier133_after_complete_qualified_parent_native_stage_v1_20261010.py', 'predict_frontier133_complete_qualified_parent_scheme_v1_20261010.py', 'verify_frontier133_actual_nested_parent_hooks_CPU_v1_20261010.py', 'frontier133_actual_three_nested_parent_hooks_CPU_controls_v1_20261010.json', 'verify_frontier133_actual42_TRAIN_native_stage_v1_20261010.py', 'frontier133_actual42_TRAIN_native_and84_cold_controls_v1_20261010.json', 'actual_frontier133_2020_TRAIN_native42_controls_activation_v1_20261010.json', 'normalize_completed_frontier133_after171_v1_20261010.py', 'frontier133_after171_predeclared_training_only_selection_plan_v1_20261010.json', 'actual_frontier133_after171_normalization_activation_v1_20261010.json', 'qualify_frontier133_selected_native14_v1_20261010.py', 'frontier133_selected_six_state_native14_sources_preparation_v1_20261010.json', 'actual_frontier133_selected_native14_activation_v1_20261010.json', 'frontier133172_candidate_sources_preparation_v1_20261010.json', 'frontier133172_actual_candidate_explicit_universe_admission_v2_20261010.json', 'frontier133172_full_registry_sources_preparation_v1_20261010.json', 'frontier133172_actual_single_leaf_registry_import_admission_v2_20261010.json', 'frontier133172_full_execution_sources_preparation_v1_20261010.json', 'frontier133172_actual_local_import_and_scalar_route_admission_v2_20261010.json', 'actual_frontier133172_complete133_family_activation_v2_20261010.json', 'run_Frontier133172_complete_family_v2_20261010.py', 'run_Frontier133172_full_registration_v2_20261010.py', 'verify_Frontier133172_full133_preflight_v2_20261010.py', 'monitor_fast_optimization_v44_20261010.py', 'actual_fast_optimization_progress_v44_activation_20261010.json', 'observer43_retired_after_actual44_verified_v1_20261010.json', 'actual_optimization_fast_runtime_handoff_v70_20261010.json']]
    for pointer in ('actual_BF16Cross120RecentReturn252Huber050175_full5_independent_location_v1_20261009.json','actual_BF16Cross120RecentReturn252Huber050175_native42_calendar_location_v1_20261009.json'):
        p=A/pointer;folder=Path(read(p)['output']);paths += [p,*folder.glob('*.json')]
    bank=Path('E:/赛题五_本机临时/neural_BF16_medium2048_cross120recent252returnhuber050_seed09_e64_bank6_v1_20261009')
    paths += [bank/'verification.json',*[bank/str(y)/'info.json' for y in range(2020,2026)]]
    for p,d in read(A/'frontier233171_actual_local_import_routes_admission_v2_20261010.json')['input_sha256'].items():assert sha(p)==d,p

    import publish_classifier_consensus_workflows_20261006 as h
    prefix=Path('validation_sync/frontier133172_native_controls_and_full_pipeline_v31_20261010'); payload={}; bindings={}
    for p in dict.fromkeys(paths):
        raw=p.read_bytes();assert not h.sync.SECRET.search(raw),p
        digest=hashlib.sha256(raw).hexdigest()
        rel=p.relative_to(ROOT) if p.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+p.name)
        name=(prefix/rel).as_posix(); data=raw
        if len(data)>=5*1024**2:data=gzip.compress(data,mtime=0);name+='.gz';assert gzip.decompress(data)==raw
        assert len(data)<95*1024**2;payload[name]=data;bindings[str(p)]={'path':name,'raw_sha256':digest}
    payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({'status':'passed_actual_own_return120_six_full5_native42_and_new_single_leaf42_native84_cold_controls133_full_pipeline_queued','files':bindings,'new_encoder120_GPU_models_and_quality_score_completion_not_claimed':True,'new_quality_scores_by_publication':0,'test_labels_read':False,'deadline_local':control['stop_at_local']})
    out=Path('E:/赛题五_本机临时/frontier133172_native_controls_and_full_pipeline_main_v31_20261010');out.mkdir(exist_ok=False)
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
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','保存一日收益120维六年度完整独立检查与新单模型阶段42项原生84项冷启动控制、133比较及完整172冻结推理QA83流程，正式候选资格待完成',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()}
            assert h.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);h.verify_main(commit);h.watcher.advance_source_index(commit)
            receipt={'status':'pushed_and_remote_head_verified','branch':'main','commit':commit,'raw_git_blobs_verified':len(hashes),'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()}
            create(out/'receipt.json',receipt);create(A/'frontier133172_native_controls_and_full_pipeline_main_receipt_v31_20261010.json',receipt);print(receipt,flush=True)
        finally:
            for p in (parent,worker):
                if p.is_running():p.resume()

if __name__=='__main__':
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(key,value) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=key;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=value
    os.environ['GIT_CONFIG_COUNT']=str(count+2)
    main()
