"""Main-only publication of actual candidate reconstruction and the queued36/173/QA84 flow."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import sys,os,hashlib,gzip
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed()
    paths=[Path(__file__),*[Path(p) for p in ['D:\\3.Study\\数据分析\\赛题五\\analysis\\prepare_complete199_sources_main_package_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\rank60_rank20_mixed199_full_execution_sources_admission_v1_20261011.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\prepare_Rank60Rank20Mixed199_complete51_pipeline_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\register_Rank60Rank20Mixed199_round199_artifacts_v4_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\publish_Rank60Rank20Mixed199_round199_full_validation_v4_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\optimize_training_round199_v4_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\finalize_training_round199_v4_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\lossless_ranking_runtime_adapter_round199_v4_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\build_lossless_ranking_display_round199_v4_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_lossless_ranking_display_round199_v4_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\collect_full_lossless_round199_qa110_v4_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\normalize_completed_rank60_rank20_mixed51_after198_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\qualify_rank60_rank20_mixed51_selected_native14_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\rank60_rank20_mixed199_storage_v4_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\prepare_Rank60Rank20Mixed199_selected_candidate_v4_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\seal_Rank60Rank20Mixed199_selected_candidate_v4_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\run_Rank60Rank20Mixed199_complete_family_v4_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\run_Rank60Rank20Mixed199_full_registration_v4_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_Rank60Rank20Mixed199_full51_preflight_v4_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\run_Rank60Rank20Mixed199_selected_candidate_feature_cache_v4_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\rank60_rank20_mixed199_candidate_sources_preparation_v4_20261011.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\rank60_rank20_mixed199_full_registry_sources_preparation_v4_20261011.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\rank60_rank20_mixed_complete51_after198_plan_v1_20261011.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\predict_rank60_rank20_mixed_complete_qualified183_scheme_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\rank60_rank20_mixed_actual_twelve_parent_callbacks_CPU_controls_v1_20261011.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\rank60_rank20_mixed_after_qualified183_native_stage_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\rank60_rank20_mixed51_normalization_native14_sources_admission_v1_20261011.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\rank60_rank20_mixed49_native14_predictor_sources_admission_v1_20261011.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\rank20_two_seed_raw_signal_v1_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\rank20_two_seed_raw_signal_actual_CPU_controls_v1_20261010.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\exact_verified_feature120_memoization_runtime_v1_20261010.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\actual_feature120_verified_memoization_TRAIN344_location_v1_20261010.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verified_shared_publication_board_loader_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\late_bound_shared_snapshot_encoder_runtime_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verified_shared_publication_board_loader_actual_complete180_controls_v1_20261011.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\actual_latest183_parent196198_routes37_v1_20261011.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\rank60_rank20_after183_mixed49_predeclared_sources_admission_v1_20261011.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\compress_new_completed_main_browser_profiles_v3_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\service_owned_workflows_20261006\\actual_rank60_rank20_mixed51_after198_normalization_v1_20261011\\job_definition.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\service_owned_workflows_20261006\\actual_rank60_rank20_mixed51_after198_normalization_v1_20261011\\native_launch.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\normalize_completed_rank60_rank20_mixed51_after198_v1_20261011_current37_wrapper.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\service_owned_workflows_20261006\\actual_rank60_rank20_mixed51_selected_native14_v1_20261011\\job_definition.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\service_owned_workflows_20261006\\actual_rank60_rank20_mixed51_selected_native14_v1_20261011\\native_launch.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\qualify_rank60_rank20_mixed51_selected_native14_v1_20261011_current37_wrapper.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\service_owned_workflows_20261006\\Rank60Rank20Mixed199_complete51_family_v4_20261011\\job_definition.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\service_owned_workflows_20261006\\Rank60Rank20Mixed199_complete51_family_v4_20261011\\native_launch.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\run_Rank60Rank20Mixed199_complete_family_v4_20261011_current37_wrapper.py']]]
    import publish_classifier_consensus_workflows_20261006 as h
    prefix=Path('validation_sync/Complete199_actual51_sources_v1_20261011_v1_20261011');payload={};bindings={}
    for p in dict.fromkeys(paths):
        raw=p.read_bytes();assert not h.sync.SECRET.search(raw),p
        digest=hashlib.sha256(raw).hexdigest();rel=p.relative_to(ROOT) if p.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+p.name)
        name=(prefix/rel).as_posix();data=raw
        if len(data)>=5*1024**2:data=gzip.compress(data,mtime=0);name+='.gz';assert gzip.decompress(data)==raw
        assert len(data)<95*1024**2;payload[name]=data;bindings[str(p)]={'path':name,'raw_sha256':digest}
    payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({**{'status': 'actual199_source_factory_compiled_and_three_queues_launched_before_scientific_completion', 'expected_official_records': 51, 'expected_connected_board': 18114, 'anchors': [183, 198], 'horizons': [20, 60], 'new_fits_by_publication': 0, 'new_scores_by_publication': 0, 'native14_and_future_and_main_round199_pending': True, 'test_labels_read': False},'files':bindings})
    out=Path('E:/赛题五_本机临时/Complete199_actual51_sources_v1_20261011_main_v1_20261011');out.mkdir(exist_ok=False)
    create(out/'frozen_before_publication.json',{'files':bindings})
    from lossless_chunked_safe_main_runtime_v1_20261009 import installed as safe
    from serial_main_publication_mutex_v1_20261009 import installed as serial
    from verified_TLS_Git_retry_runtime_v3_20261010 import installed as git_io
    from owned_idle_publication_wait_reboot_identity_v2_20261011 import hold
    with serial(out/'serial_mutex.json') as mutex,safe(out/'safe'),git_io(out/'file_backed_git'):
        mutex.acquire();assert allowed()
        parent,worker,idle=hold(read(A/'service_owned_workflows_20261006/main_publisher_reboot_v12_20261011/native_launch.json'),'    main (watch_validations_main_v7_20261006.py:71)')
        try:
            sync=h.sync;h.verify_main(sync.git('rev-parse','HEAD'));assert not sync.git('status','--porcelain')
            for name,data in payload.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(payload)
            for i in range(0,len(names),50):sync.git('add','-f','--',*names[i:i+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','冻结第199轮20/60日混合完整51项流程源码及真实队列凭据；评分与候选资格仍待完成',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()};assert h.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);h.verify_main(commit);h.watcher.advance_source_index(commit)
            receipt={'status':'pushed_and_remote_head_verified','branch':'main','commit':commit,'raw_git_blobs_verified':len(hashes),'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()}
            create(out/'receipt.json',receipt);create(A/'Complete199_actual51_sources_v1_20261011_main_receipt_v1_20261011.json',receipt);print(receipt,flush=True)
        finally:
            for p in (parent,worker):
                if p.is_running():p.resume()
if __name__=='__main__':
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(key,value) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=key;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=value
    os.environ['GIT_CONFIG_COUNT']=str(count+2);main()
