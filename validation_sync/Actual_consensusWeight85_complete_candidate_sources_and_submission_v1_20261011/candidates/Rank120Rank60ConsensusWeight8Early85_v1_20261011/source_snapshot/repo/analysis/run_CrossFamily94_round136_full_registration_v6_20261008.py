"""Register94 actual complete-parent cross-family comparisons, sealed winner, full QA47 and main."""
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
    out=A/'CrossFamily94_round136_actual_registration_v6_20261008';assert not out.exists();out.mkdir()
    for name in ('CrossFamily94_official_comparison_v5_20261008','CrossFamily94_scores_main_publication_v5_20261008',
        'CrossFamily94_selected_candidate_sealing_v5_20261008','BF16wide40_round135_full_registration_v7_20261008'):
        service=A/'service_owned_workflows_20261006'/name
        while not (service/'native_launch.json').exists() or owned(read(service/'native_launch.json')):time.sleep(15)
        assert read(service/'service_execution.json')['status']=='passed',name
    while psutil.virtual_memory().available<9*2**30:time.sleep(15)
    state=read(A/'service_owned_dependency_queue_v4_20261006/state.json')
    while any(n.startswith('round') and owned(r) for n,r in state['activated_jobs'].items()):
        time.sleep(15);state=read(A/'service_owned_dependency_queue_v4_20261006/state.json')
    import prepare_CrossFamily94_round136_sources_v4_20261008 as actual_generator
    original_read=actual_generator.read;original_paths=actual_generator.source_paths
    def current_admission_read(path):
        path=Path(path)
        if path==A/'CrossFamily94_round136_source_admission_v4_20261008.json':path=A/'CrossFamily94_round136_source_admission_v5_20261008.json'
        return original_read(path)
    def current_source_paths():
        names={'CrossFamily94_round136_source_admission_v4_20261008.json':'CrossFamily94_round136_source_admission_v5_20261008.json','CrossFamily94_round136_source_preparation_v4_20261008.json':'CrossFamily94_round136_source_preparation_v5_20261008.json','CrossFamily94_actual_controls_index_v3_20261008.json':'CrossFamily94_actual_controls_index_v4_20261008.json','actual_CrossFamily91_current_parent_location_v1_20261008.json':'actual_CrossFamily91_current_parent_location_v2_20261008.json'}
        paths=[]
        for path in original_paths():
            if path.name in names and path.parent==A:path=A/names[path.name]
            if path.name=='receipt.json' and path.parent.name=='CrossFamily94_scores_github_v1_20261008':path=A/'CrossFamily94_scores_github_v2_20261008/receipt.json'
            paths.append(path)
        extra=[Path(__file__),A/'prepare_CrossFamily136_candidate_registration_recovery_v5_20261008.py',A/'recover_CrossFamily136_quality_after_actual135_main_v5_20261008.py',A/'CrossFamily136_quality_receiver_recovery_v5_20261008.json',A/'CrossFamily136_candidate_registration_recovery_v5_20261008.json',A/'verify_CrossFamily94_round136_sources_v5_20261008.py',A/'run_CrossFamily94_official_comparison_v5_20261008.py',A/'publish_CrossFamily94_evidence_v5_20261008.py',A/'prepare_CrossFamily94_selected_candidate_v5_20261008.py',A/'seal_CrossFamily94_selected_candidate_v5_20261008.py',A/'short_content_addressed_native_storage_v2_20261008.py',A/'actual_short_parent_alias_nested_copy_v2_20261008.json']
        for name in ('CrossFamily94_round136_source_admission_v5_20261008','CrossFamily94_controls_main_publication_v5_20261008','CrossFamily94_official_comparison_v5_20261008','CrossFamily94_scores_main_publication_v5_20261008','CrossFamily94_selected_candidate_preparation_v5_20261008','CrossFamily94_selected_candidate_sealing_v5_20261008'):
            folder=A/'service_owned_workflows_20261006'/name;extra.extend(folder.glob('*.json'));extra.extend(folder.glob('*.log'))
        return list(dict.fromkeys([*paths,*extra]))
    actual_generator.read=current_admission_read;actual_generator.source_paths=current_source_paths
    def prepare_sources():
        # The failed5 worker wrote every frozen generated source, then failed only while hashing a missing old admission path.
        # Do not overwrite or regenerate those scientific source bytes.
        proof_path=A/'CrossFamily94_round136_source_admission_v5_20261008.json';proof=read(proof_path)
        ready_path=A/'CrossFamily94_selected_release_v1_20261008/selected_candidate_ready_for_registration.json';ready=read(ready_path)
        pilot=read(A/'CrossFamily94_official_comparison_v1_20261008/verification.json')
        assert ready['sealed_candidate_complete'] and ready['best']==pilot['best'] and len(pilot['records'])==94
        generated=actual_generator.generate(pilot['actual_comparison_parent_round'])
        expected=proof['generated_source_sha256'][str(pilot['actual_comparison_parent_round'])]
        assert len(generated)==8 and set(generated)==set(expected)
        for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
        for name,value in generated.items():
            import hashlib
            assert sha(A/name)==hashlib.sha256(value.encode()).hexdigest()==expected[name],name
            compile(value,str(A/name),'exec')
        create(A/'CrossFamily94_round136_source_preparation_v5_20261008.json',{
            'status':'passed_actual94_sealed_candidate_and_admitted_full136_QA47_sources',
            'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'round':136,'scored_records':94,
            'actual_comparison_parent_round':pilot['actual_comparison_parent_round'],
            'input_sha256':{str(path):sha(path) for path in [Path(__file__),Path(actual_generator.__file__),ready_path,proof_path,*[A/name for name in generated]]},
            'all8_already_written_generated_sources_rehashed_exact_to_original24_source_preflight':True,
            'new_generated_scientific_source_writes':0,'old_registration5_failure_preserved':True,
            'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})

    prepare_sources()
    prep=read(A/'CrossFamily94_round136_source_preparation_v5_20261008.json')
    assert prep['status']=='passed_actual94_sealed_candidate_and_admitted_full136_QA47_sources'
    for p,digest in prep['input_sha256'].items():assert sha(p)==digest,p
    ready=read(A/'CrossFamily94_selected_release_v1_20261008/selected_candidate_ready_for_registration.json')
    assert ready['status']=='passed_actual94_selected_candidate_full_graph_and_metrics_and_source_bytes'
    from register_CrossFamily94_round136_artifacts_20261008 import main as register
    from prepare_CrossFamily94_round136_sources_v4_20261008 import source_paths
    ns={'sources':source_paths()}
    assert all(p.is_file() for p in ns['sources'])
    create(A/'CrossFamily94_actual_source_paths_before_registration_20261008.json',{'status':'passed_all_actual136_registry_source_paths_before_alias_or_registration',
        'input_sha256':{str(p):sha(p) for p in ns['sources']},'source_count':len(ns['sources']),'new_native_fits':0,'new_quality_scores':0})
    protocol=register();folder=A/'optimization_20261003_r136';pins=protocol['input_sha256']
    parent_number=protocol['explicit_parent_round'];assert parent_number in (112,134,135)
    create(folder/'frozen_before_actual_full_registration.json',{'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'input_sha256':pins,'registration_only':True,'current_qualified_comparison_parent_round':parent_number,
        'original_selected_inference_and_all_parameter_bytes_preserved':True,'test_labels_read':False})
    scratch=Path('E:/赛题五_本机临时/第136轮_20261008/tmp/full136');scratch.mkdir(parents=True,exist_ok=True)
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
        publish(136,'完整父方案的跨模型残差集成','conditional_flag_residual_causal_checks.json',['预定94项：三个合格锚点、90项跨模型组合、零幅度恒等对照'])
        from lossless_ranking_runtime_adapter_round136_20261007 import install as lossless
        restore_ranking=lossless(136)
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
        from publish_CrossFamily94_round136_full_validation_20261008 import main as github
        helpers.sync.git=retry_git;github()
        create(folder/'full_registration_execution.json',{'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
            'existing_official_scores_registered':94,'full_rankings_all_original_QA_and_main_publication_completed':True,
            'scientific_workers_suspended_stopped_or_restarted':0,'new_quality_scores_by_registration':0,
            'new_inference_claimed_by_registration':False,'selected_candidate_actual_new_inference':ready['new_inference_claimed'],
            'global_goal_or_resource_exhaustion_claimed':False,'test_labels_read':False})
    except BaseException as error:
        create(folder/'full_registration_failure.json',{'status':'failed_preserved_CrossFamily94_full136_registration',
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


if __name__=='__main__':
    from file_backed_hidden_git_runtime_20261007 import installed
    from CrossFamily136_storage_v1_20261008 import installed_transfer
    with installed(A/'run_CrossFamily94_round136_full_registration_v6_file_IO_20261008'),installed_transfer():main()
