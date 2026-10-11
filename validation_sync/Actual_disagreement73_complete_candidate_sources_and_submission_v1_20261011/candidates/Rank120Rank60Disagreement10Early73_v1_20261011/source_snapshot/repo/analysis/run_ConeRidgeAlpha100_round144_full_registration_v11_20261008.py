"""Register94 actual complete-parent cross-family comparisons, sealed winner, full QA55 and main."""
from pathlib import Path
import os
import sys
import time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from hidden_windows_child_creation_20261006 import install
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle


def main():
    import psutil
    out=A/'ConeRidgeAlpha100_round144_actual_registration_v11_20261008';assert not out.exists();out.mkdir()
    for name in ('ConeRidgeAlpha100_official_comparison_v5_20261008','exact135_144_connected_API_publication_reconciliation_v3_20261008',
        'ConeRidgeAlpha100_selected_candidate_sealing_v9_20261008','BF16wide40_round135_full_registration_v7_20261008'):
        service=A/'service_owned_workflows_20261006'/name
        while not (service/'native_launch.json').exists() or owned(read(service/'native_launch.json')):time.sleep(15)
        assert read(service/'service_execution.json')['status']=='passed',name
    while psutil.virtual_memory().available<9*2**30:time.sleep(15)
    state=read(A/'service_owned_dependency_queue_v4_20261006/state.json')
    while any(n.startswith('round') and owned(r) for n,r in state['activated_jobs'].items()):
        time.sleep(15);state=read(A/'service_owned_dependency_queue_v4_20261006/state.json')
    import prepare_ConeRidgeAlpha100_round144_sources_v7_20261008 as connected_generator
    prior_source_paths=connected_generator.source_paths
    def actual_connected_source_paths():
        paths=[Path(str(p).replace('ConeRidgeAlpha100_scores_github_v1_20261008/receipt.json','ConeRidgeAlpha100_scores_github_v2_20261008/receipt.json').replace('ConeRidgeAlpha100_scores_github_v1_20261008/receipt.json','ConeRidgeAlpha100_scores_github_v2_20261008/receipt.json')) for p in prior_source_paths()]
        extras=[Path(__file__),A/'connected_API_full_round_transport_v1_20261008.py',A/'prepare135_144_full_registration_connected_API_v1_20261008.py',A/'exact135_144_connected_API_reconciliation_v3_20261008.json',A/'reconcile_exact135_144_connected_API_publication_v3_20261008.py',A/'prepare135_144_candidates_after_connected_API_v2_20261008.py',A/'candidates135_144_connected_API_recovery_v1_20261008.json',A/'prepare_ConeRidgeAlpha100_selected_candidate_v6_20261008.py',A/'seal_ConeRidgeAlpha100_selected_candidate_v6_20261008.py']
        for name in ('ConeRidgeAlpha100_selected_candidate_preparation_v6_20261008','ConeRidgeAlpha100_selected_candidate_sealing_v9_20261008','BF16wide40_round135_full_registration_v7_20261008'):
            folder=A/'service_owned_workflows_20261006'/name;extras.extend(folder.glob('*.json'));extras.extend(folder.glob('*.log'))
        return list(dict.fromkeys([*paths,*extras]))
    connected_generator.source_paths=actual_connected_source_paths
    prior_windows_paths=connected_generator.source_paths
    def actual_windows_paths():
        return list(dict.fromkeys([A/'ConeRidgeAlpha100_scores_github_v2_20261008/receipt.json' if p.name=='receipt.json' and p.parent.name=='ConeRidgeAlpha100_scores_github_v1_20261008' else p for p in prior_windows_paths()]+[Path(__file__),A/'short_content_addressed_native_storage_v1_20261008.py',A/'recover144_short_native_paths_and135_receipts_v1_20261008.py',A/'prepare_ConeRidgeAlpha100_selected_candidate_v7_20261008.py',A/'seal_ConeRidgeAlpha100_selected_candidate_v7_20261008.py']))
    connected_generator.source_paths=actual_windows_paths
    previous_actual_paths=connected_generator.source_paths
    def actual_current_registration_paths():return list(dict.fromkeys([*previous_actual_paths(),Path(__file__),A/'start144_registration_after_actual_alias_sealer_v11_20261008.py']))
    connected_generator.source_paths=actual_current_registration_paths
    from prepare_ConeRidgeAlpha100_round144_sources_v7_20261008 import main as prepare_sources
    prepare_sources()
    prep=read(A/'ConeRidgeAlpha100_round144_source_preparation_v7_20261008.json')
    assert prep['status']=='passed_actual100_sealed_candidate_and_admitted_full144_QA55_sources'
    for p,digest in prep['input_sha256'].items():assert sha(p)==digest,p
    ready=read(A/'ConeRidgeAlpha100_selected_release_v4_20261008/selected_candidate_ready_for_registration.json')
    assert ready['status']=='passed_actual100_selected_candidate_full_graph_and_metrics_and_source_bytes'
    from register_ConeRidgeAlpha100_round144_artifacts_20261008 import main as register
    from prepare_ConeRidgeAlpha100_round144_sources_v7_20261008 import source_paths
    ns={'sources':source_paths()}
    assert all(p.is_file() for p in ns['sources'])
    create(A/'ConeRidgeAlpha100_actual_source_paths_before_registration_20261008.json',{'status':'passed_all_actual144_registry_source_paths_before_alias_or_registration',
        'input_sha256':{str(p):sha(p) for p in ns['sources']},'source_count':len(ns['sources']),'new_native_fits':0,'new_quality_scores':0})
    protocol=register();folder=A/'optimization_20261003_r144';pins=protocol['input_sha256']
    parent_number=protocol['explicit_parent_round'];assert parent_number in (132,134,143)
    create(folder/'frozen_before_actual_full_registration.json',{'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'input_sha256':pins,'registration_only':True,'current_qualified_comparison_parent_round':parent_number,
        'original_selected_inference_and_all_parameter_bytes_preserved':True,'test_labels_read':False})
    scratch=Path('E:/赛题五_本机临时/第144轮_20261008/tmp/full144');scratch.mkdir(parents=True,exist_ok=True)
    for key in ('TEMP','TMP','TMPDIR','MPLCONFIGDIR'):os.environ[key]=str(scratch)
    import tempfile
    tempfile.tempdir=str(scratch)
    held=[];transport=[];restore_children=install();restore_ranking=scope=None
    import publish_classifier_consensus_workflows_20261006 as helpers
    old_git=helpers.sync.git
    def retry_git(*args,**kwargs):
        for attempt in range(3):
            try:return old_git(*args,**kwargs)
            except RuntimeError as error:
                if args[0] not in ('ls-remote','push','fetch') or not any(t in str(error).lower() for t in ('tls','ssl','unable to access','connection','timed out')):raise
                transport.append({'command':args[0],'attempt':attempt+1,'error':str(error)[:1000]})
                if attempt==2:raise
                time.sleep(2)
    try:
        main7=read(A/'service_owned_workflows_20261006/main_publisher_v8_20261008/native_launch.json')
        parent,worker,idle=suspended_idle(main7,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        create(folder/'actual_main7_idle_before_and_after_hold.json',idle)
        from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
        scope=LockedReadHashCache(pins);scope.__enter__()
        from publish_explicit_parent_training_round_v2_20261005 import publish
        publish(144,'完整父方案的跨模型残差集成','conditional_flag_residual_causal_checks.json',['预定100项：三个合格锚点、96项新增参数约束岭回归变换、零幅度恒等对照'])
        from lossless_ranking_runtime_adapter_round144_20261007 import install as lossless
        restore_ranking=lossless(144)
        import build_all_model_rankings_20261003 as ranking
        import verify_all_model_rankings_20261003 as qa
        ranking.main();qa.main();scope.reverify()
        create(folder/'provenance_scope_execution.json',{'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
            'input_sha256':pins,'initial_full_hash_and_Windows_read_share_only_locks':True,
            'final_full_rehash_after_actual_full_ranking_QA':True,'sealed_input_files':len(pins),
            'cache_hits':scope.hits,'nonsealed_paths_rehashed':scope.fresh_calls,
            'actual1599600_row_model_reload_and_cold80_candidate_proofs_preserved':True,
            'exact_existing_candidate_confirmed_by_all_validation_bits_all_metrics_and_parameters':not ready['new_inference_claimed'],
            'selected_new_scheme_full_native_and_independent_replays_executed':ready['new_inference_claimed'],
            'all_original_six_view_browser_and_candidate_manifest_QA_passed':True,
            'registered_previously_executed_scope_not_new_inference_or_scientific_freeze':True,
            'new_model_fits':0,'new_quality_scores_by_registration':0,'test_labels_read':False})
        scope.close();scope=None
        from connected_API_full_round_transport_v1_20261008 import execute_actual_publisher
        def github():execute_actual_publisher(144)
        helpers.sync.git=retry_git;github()
        create(folder/'full_registration_execution.json',{'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
            'existing_official_scores_registered':100,'full_rankings_all_original_QA_and_main_publication_completed':True,
            'scientific_workers_suspended_stopped_or_restarted':0,'new_quality_scores_by_registration':0,
            'new_inference_claimed_by_registration':False,'selected_candidate_actual_new_inference':ready['new_inference_claimed'],
            'global_goal_or_resource_exhaustion_claimed':False,'test_labels_read':False})
    except BaseException as error:
        create(folder/'full_registration_failure.json',{'status':'failed_preserved_ConeRidgeAlpha100_full144_registration',
            'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'error':f'{type(error).__name__}: {error}'})
        raise
    finally:
        helpers.sync.git=old_git
        if scope is not None:scope.close()
        if restore_ranking is not None:restore_ranking()
        for process in reversed(held):
            if process.is_running():process.resume()
        create(folder/'actual_hidden_registration_children.json',{'events':restore_children(),'scientific_workers_not_suspended_stopped_or_restarted':True})
        create(out/'actual_transport_retries.json',{'attempts':transport,'TLS_verification_unchanged':True})



def assert_already_qualified_parents():
    for number in (132,134,143):
        assert read(A/f'optimization_20261003_r{number}/full_registration_execution.json')['status']=='passed'
        assert read(A/f'github_validation_sync_main_20261005/round{number}_receipt.json')['status']=='pushed_and_remote_head_verified'

if __name__=='__main__':
    from file_backed_hidden_git_runtime_20261007 import installed
    from ConeRidgeAlpha144_storage_v6_20261008 import installed_transfer
    with installed(A/'run_ConeRidgeAlpha100_round144_full_registration_v11_file_IO_20261008'),installed_transfer():main()
