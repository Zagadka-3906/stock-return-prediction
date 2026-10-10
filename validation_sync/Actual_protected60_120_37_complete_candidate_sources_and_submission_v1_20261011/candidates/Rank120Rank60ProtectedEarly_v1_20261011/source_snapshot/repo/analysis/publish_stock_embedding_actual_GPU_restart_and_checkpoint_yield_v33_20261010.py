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
    paths=[Path(p) for p in ['D:\\3.Study\\数据分析\\赛题五\\analysis\\publish_stock_embedding_GPU_admission_and_observer_handoff_v33_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\actual_optimization_fast_runtime_handoff_v74_20261010.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\observers44_and45_retired_after_actual46_verified_v1_20261010.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\activate_stock_embedding_admission_and_publications_v4_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\activate_stock_embedding_native42_and_progress_v46_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\admit_stock_embedding_checkpoint_yield_training_v5_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\predict_stock_embedding_complete_qualified_parent_scheme_v1_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\prepare_stock_embedding_actual_full5_routes_v2_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\prepare_stock_embedding_CPU_output_and_screen17_v2_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\prepare_stock_embedding_E_cache_safe_runtime_v3_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\prepare_stock_embedding_native_stage_and_predictor_v1_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\prepare_stock_embedding_small512_sources_v1_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\publish_stock_embedding17_completion_v49_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\publish_stock_embedding_actual_CPU_preparation_v33_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\run_stock_embedding_after172_high_impact17_screen_v1_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\run_stock_embedding_checkpoint_yield_queue_v5_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\run_stock_embedding_small512_own_training_queue_v1_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\run_stock_embedding_small512_own_training_queue_v3_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\run_stock_embedding_small512_own_training_queue_v4_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\stock_embedding_after_complete_qualified_parent_native_stage_v1_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\stock_embedding_saved_tensor_decoder_v1_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\stock_embedding_small512_BF16_native_v1_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\train_stock_embedding_small512_BF16_bank6_checkpoint_yield_v5_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\train_stock_embedding_small512_BF16_bank6_v1_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\train_stock_embedding_small512_BF16_bank6_v3_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_stock_embedding_actual_four_nested_parent_hooks_CPU_v1_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_stock_embedding_mature_fixture_and_CPU_v1_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_stock_embedding_mature_fixture_and_CPU_v2_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_stock_embedding_six_state_native42_v1_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_stock_embedding_six_state_native42_v2_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_stock_embedding_small512_full5_independent_v1_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_stock_embedding_small512_full5_independent_v2_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_stock_embedding_small512_full5_independent_v3_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_stock_embedding_small512_restart_v1_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_stock_embedding_small512_restart_v3_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_stock_embedding_small512_small_CPU_v2_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_stock_embedding_small512_small_CPU_v3_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\stock_embedding_actual_four_hooks_native42_and_observer_admission_v46_20261010.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\stock_embedding_actual_full5_routes_admission_v2_20261010.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\stock_embedding_actual_queue_and_publication_routes_admission_v4_20261010.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\stock_embedding_checkpoint_yield_training_admission_v5_20261010.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\stock_embedding_E_cache_safe_runtime_admission_v3_20261010.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\stock_embedding_native_stage_and_four_parent_routes_admission_v1_20261010.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\stock_embedding_small512_sources_admission_v1_20261010.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\actual_stock_embedding17_completion_publication_activation_v49_20261010.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\actual_stock_embedding17_screen_activation_v1_20261010.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\actual_stock_embedding_checkpoint_yield_training_queue_activation_v5_20261010.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\actual_stock_embedding_CPU_preparation_main_activation_v33_20261010.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\actual_stock_embedding_own_training_queue_activation_v4_20261010.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\actual_stock_embedding_six_state_native42_activation_v2_20261010.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\actual_fast_optimization_progress_v46_activation_20261010.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\monitor_fast_optimization_v46_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\stock_embedding_actual_four_nested_parent_hooks_CPU_controls_v1_20261010.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\actual_stock_embedding_small512_restart_location_v1_20261010.json', 'E:\\赛题五_本机临时\\GPU实测_20261009\\stock_embedding_small512_restart_v1_20261010\\actual_hidden_children.json', 'E:\\赛题五_本机临时\\GPU实测_20261009\\stock_embedding_small512_restart_v1_20261010\\frozen_before_actual_controls.json', 'E:\\赛题五_本机临时\\GPU实测_20261009\\stock_embedding_small512_restart_v1_20261010\\verification.json', 'E:\\赛题五_本机临时\\GPU实测_20261009\\stock_embedding_small512_restart_v1_20261010\\small32\\first_actual.json', 'E:\\赛题五_本机临时\\GPU实测_20261009\\stock_embedding_small512_restart_v1_20261010\\small32\\verification.json', 'E:\\赛题五_本机临时\\GPU实测_20261009\\stock_embedding_small512_restart_v1_20261010\\wide2\\first_actual.json', 'E:\\赛题五_本机临时\\GPU实测_20261009\\stock_embedding_small512_restart_v1_20261010\\wide2\\verification.json', 'E:\\赛题五_本机临时\\StockEmbeddingSmall512_independent_small_CPU_v1_20261009\\frozen_before_actual_controls.json', 'E:\\赛题五_本机临时\\StockEmbeddingSmall512_independent_small_CPU_v1_20261009\\verification.json']]
    import publish_classifier_consensus_workflows_20261006 as h
    prefix=Path('validation_sync/stock_embedding_actual_GPU_restart_and_checkpoint_yield_preparation_v33_20261010'); payload={}; bindings={}
    for p in dict.fromkeys(paths):
        raw=p.read_bytes();assert not h.sync.SECRET.search(raw),p
        digest=hashlib.sha256(raw).hexdigest()
        rel=p.relative_to(ROOT) if p.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+p.name)
        name=(prefix/rel).as_posix(); data=raw
        if len(data)>=5*1024**2:data=gzip.compress(data,mtime=0);name+='.gz';assert gzip.decompress(data)==raw
        assert len(data)<95*1024**2;payload[name]=data;bindings[str(p)]={'path':name,'raw_sha256':digest}
    payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({'status':'passed_actual_two_stock_embedding_fresh_process_GPU_restart_controls_saved_tensors_exact_four_parent_CPU_hooks_checkpoint_yield_training_active_quality_pending','files':bindings,'new_encoder120_GPU_models_and_quality_score_completion_not_claimed':True,'new_quality_scores_by_publication':0,'test_labels_read':False,'deadline_local':control['stop_at_local']})
    out=Path('E:/赛题五_本机临时/stock_embedding_actual_GPU_restart_and_checkpoint_yield_preparation_main_v33_20261010');out.mkdir(exist_ok=False)
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
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','保存股票嵌入网络两项实际GPU断点续训、独立解码与四种完整父模型回调检查，利用空闲GPU按8epoch检查点让位加速训练',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()}
            assert h.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);h.verify_main(commit);h.watcher.advance_source_index(commit)
            receipt={'status':'pushed_and_remote_head_verified','branch':'main','commit':commit,'raw_git_blobs_verified':len(hashes),'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()}
            create(out/'receipt.json',receipt);create(A/'stock_embedding_actual_GPU_restart_and_checkpoint_yield_preparation_main_receipt_v33_20261010.json',receipt);print(receipt,flush=True)
        finally:
            for p in (parent,worker):
                if p.is_running():p.resume()

if __name__=='__main__':
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(key,value) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=key;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=value
    os.environ['GIT_CONFIG_COUNT']=str(count+2)
    main()
