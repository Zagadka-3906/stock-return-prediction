"""Register real76 scores, run unchanged complete ranking QA87, then publish verified main."""
from pathlib import Path
import os,sys,time
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
    assert allowed();closed('StockTop10Embedding176_selected_candidate_sealing_v1_20261010')
    closed('StockTop10Embedding175_complete47_family_v3_20261010')
    ready=read(A/'StockTop10Embedding176_selected_release_v1_20261010/selected_candidate_ready_for_registration.json')
    assert ready['status']=='passed_actual31_selected_candidate_full_graph_and_metrics_and_source_bytes' and ready['sealed_candidate_complete']
    import prepare_stock_top10_embedding176_full_registry_sources_v2_20261010 as routes
    base_source_paths=routes.source_paths
    routes.source_paths=lambda:list(dict.fromkeys([*base_source_paths(),Path(__file__),A/'run_StockTop10Embedding176_complete_family_v3_20261010.py',A/'verify_StockTop10Embedding176_full31_preflight_v3_20261010.py',A/'stock_top10_embedding176_full_family_preflight_v2_20261010.json']))
    inherited_routes=routes.source_paths
    routes.source_paths=lambda:list(dict.fromkeys([*inherited_routes(),*[A/n for n in ['prevent_Top10_large29_pointer_collision_and_cascade_routes_v5_20261010.py', 'normalize_completed_stock_top10_embedding_followup31_after175_v3_20261010.py', 'qualify_stock_top10_embedding31_selected_native14_v3_20261010.py', 'prepare_StockTop10Embedding176_selected_candidate_v3_20261010.py', 'stock_top10_embedding176_candidate_sources_preparation_v3_20261010.json', 'run_stock_top10_embedding_after174_large_allocation29_screen_v2_20261010.py', 'publish_stock_top10_embedding_after174_large_allocation29_completion_v72_20261010.py']]]))
    sources=routes.source_paths();assert all(p.is_file() for p in sources)
    assert read(A/'byte_exact_ranking_stream_benchmark_v1_20261010.json')['adopt']
    for proofname in ('stock_top10_embedding176_candidate_sources_preparation_v3_20261010.json','stock_top10_embedding176_full_registry_sources_preparation_v2_20261010.json'):
        for p,d in read(A/proofname)['input_sha256'].items():assert sha(p)==d,p
    from register_StockTop10Embedding176_round176_artifacts_v2_20261010 import main as register
    protocol=register();folder=A/'optimization_20261003_r176'
    assert protocol['expected_scored_records']==31 and protocol['explicit_parent_round']==175
    pins=protocol['input_sha256']
    create(folder/'frozen_before_actual_full_registration.json',{'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'registration_only':True,'current_qualified_comparison_parent_round':175,'original_selected_inference_and_all_parameter_bytes_preserved':True,'test_labels_read':False})
    import psutil
    while psutil.virtual_memory().available<9*2**30:assert allowed();time.sleep(15)
    scratch=Path('E:/赛题五_本机临时/第176轮_20261010/tmp/full162');scratch.mkdir(parents=True,exist_ok=True)
    for key in ('TEMP','TMP','TMPDIR','MPLCONFIGDIR'):os.environ[key]=str(scratch)
    import tempfile;tempfile.tempdir=str(scratch)
    from hidden_windows_child_creation_20261006 import install
    restore_children=install();held=[];restore_ranking=None;scope=None
    from lossless_chunked_safe_main_runtime_v1_20261009 import installed as safe
    from serial_main_publication_mutex_v1_20261009 import installed as serial
    from verified_TLS_Git_retry_runtime_v3_20261010 import installed as git_io
    from owned_idle_publication_wait_runtime_v1_20261010 import hold
    from byte_exact_ranking_stream_runtime_v1_20261010 import installed as stream_writer
    from byte_exact_publication_encoder_runtime_v1_20261010 import installed as encode_publication
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    log=Path('E:/赛题五_本机临时/第176轮_20261010/safe_full_main_v1_20261010')
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(k,v) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=k;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=v
    os.environ['GIT_CONFIG_COUNT']=str(count+2)
    try:
        with safe(log),serial(log/'serial_mutex.json') as mutex,git_io(log/'file_backed_git'),stream_writer(),encode_publication():
            mutex.acquire();assert allowed()
            parent,worker,idle=hold(read(A/'service_owned_workflows_20261006/main_publisher_v11_20261010/native_launch.json'),'    main (watch_validations_main_v7_20261006.py:71)')
            held.extend((worker,parent));create(folder/'actual_main7_idle_before_and_after_hold.json',idle)
            scope=LockedReadHashCache(pins);scope.__enter__()
            from publish_explicit_parent_training_round_v2_20261005 import publish
            publish(176,'提前分类29项与两完整锚点共31项验证','conditional_flag_residual_causal_checks.json',['实际171基线29项分类筛选及完整171和175锚点；连续官方S优先'])
            from lossless_ranking_runtime_adapter_round176_v2_20261008 import install as lossless
            restore_ranking=lossless(176)
            import build_all_model_rankings_20261003 as ranking
            import verify_all_model_rankings_20261003 as qa
            ranking.main();qa.main();scope.reverify()
            create(folder/'provenance_scope_execution.json',{'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'initial_full_hash_and_Windows_read_share_only_locks':True,'final_full_rehash_after_actual_full_ranking_QA':True,'sealed_input_files':len(pins),'cache_hits':scope.hits,'nonsealed_paths_rehashed':scope.fresh_calls,'actual1599600_row_model_reload_and_cold80_candidate_proofs_preserved':True,'exact_existing_candidate_confirmed_by_all_validation_bits_all_metrics_and_parameters':not ready['new_inference_claimed'],'selected_new_scheme_full_native_and_independent_replays_executed':ready['new_inference_claimed'],'all_original_six_view_browser_and_candidate_manifest_QA_passed':True,'registered_previously_executed_scope_not_new_inference_or_scientific_freeze':True,'new_model_fits':0,'new_quality_scores_by_registration':0,'test_labels_read':False})
            scope.close();scope=None
            assert allowed()
            from publish_StockTop10Embedding176_round176_full_validation_v2_20261010 import main as github
            github()
            receipt=read(A/'github_validation_sync_main_20261005/round176_receipt.json');assert receipt['scored_records']==31 and receipt['status']=='pushed_and_remote_head_verified'
            assert restore_ranking is not None
            restore_ranking();restore_ranking=None
            create(folder/'full_registration_execution.json',{'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'existing_official_scores_registered':31,'full_rankings_all_original_QA_and_main_publication_completed':True,'scientific_workers_suspended_stopped_or_restarted':0,'new_quality_scores_by_registration':0,'new_inference_claimed_by_registration':False,'selected_candidate_actual_new_inference':ready['new_inference_claimed'],'global_goal_or_resource_exhaustion_claimed':False,'test_labels_read':False})
    except BaseException as error:
        create(folder/'full_registration_failure.json',{'status':'failed_preserved_cross120170_full31_registration','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'error':f'{type(error).__name__}: {error}'})
        raise
    finally:
        if scope is not None:scope.close()
        if restore_ranking is not None:restore_ranking()
        for p in reversed(held):
            if p.is_running():p.resume()
        create(folder/'actual_hidden_registration_children.json',{'events':restore_children(),'scientific_workers_not_suspended_stopped_or_restarted':True})

if __name__=='__main__':
    from types import SimpleNamespace
    from stock_top10_embedding176_storage_v1_20261010 import installed_transfer
    from late_bound_dynamic_snapshot_encoder_runtime_v1_20261010 import installed
    receiver=SimpleNamespace(main=main)
    from frozen_external_official_capsule_publish_guard_runtime_v1_20261010 import installed as external_capsules
    with external_capsules(Path('E:/赛题五_本机临时/第176轮_20261010/frozen_external_capsule_publication_guard_v3.json')),installed_transfer(),installed(receiver,'publish_StockTop10Embedding176_round176_full_validation_v2_20261010',Path('E:/赛题五_本机临时/第176轮_20261010/late_snapshot_encoder_import.json')):
        receiver.main()
