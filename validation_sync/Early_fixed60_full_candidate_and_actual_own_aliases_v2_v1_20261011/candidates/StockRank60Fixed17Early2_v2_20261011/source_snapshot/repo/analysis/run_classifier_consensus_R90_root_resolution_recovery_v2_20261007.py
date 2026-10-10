"""Resume the frozen138 R90 cases after actual full-context controls; retain both failures."""
from pathlib import Path
import ast,runpy,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def main():
    import psutil
    control=A/'R90_dynamic_score_context_v2_preflight_20261007/verification.json'
    service=A/'service_owned_workflows_20261006/R90_dynamic_score_context_v2_preflight'
    while not (service/'service_execution.json').exists() or owned(read(service/'native_launch.json')):time.sleep(15)
    assert read(service/'service_execution.json')['status']=='passed'
    assert read(control)['status']=='passed_actual_two_full5635800_scheme_original8_metric_bits_and_Windows_reset_safe_score_hooks'
    admission=A/'classifier_consensus_R90_root_resolution_recovery_v2_admission_20261007.json'
    for path,digest in read(admission)['input_sha256'].items():assert sha(path)==digest,path
    prior=A/'service_owned_workflows_20261006/classifier_consensus_R90_root_resolution_recovery'
    assert not owned(read(prior/'native_launch.json')) and read(prior/'service_execution.json')['status']=='failed'
    state=read(A/'service_owned_dependency_queue_v4_20261006/state.json')
    assert not any(n.startswith('round') and owned(r) for n,r in state['activated_jobs'].items())
    while psutil.virtual_memory().available<9*2**30:time.sleep(15)
    out=A/'classifier_consensus_R90_root_resolution_recovery_v2_20261007';assert not out.exists();out.mkdir()
    folder=A/'optimization_20261003_r90';proto=folder/'protocol.json';failed=folder/'provenance_scope_execution.json'
    archive=folder/'provenance_scope_execution_failed_root_recovery_20261007.json'
    location=folder/'provenance_scope_execution_failed_root_recovery_location_v2_20261007.json'
    audit_path=A/'R90_failed_root_recovery_scope_non_pinning_audit_v2_20261007.json';audit=read(audit_path)
    assert audit['matched_files']==[] and sha(failed)==sha(archive)==audit['canonical_failed_scope_sha256']
    assert not location.exists() and read(failed)['actual_original138_quality_records']==1
    waves=list(folder.glob('wave*_results.json'));assert len(waves)==1
    partial=read(waves[0]);assert set(partial['results'])=={'baseline'}
    baseline=partial['results']['baseline'];selected=read(A/'optimization_20261003_r89/selection.json')['winner']
    assert baseline['metrics']==selected['metrics'] and baseline['whole_scheme_graph']==selected['whole_scheme_graph']
    assert read(folder/'component_audit.json')['status']=='passed'
    prototype=A/'run_classifier_consensus_round90_with_precise_gate_and_parent_cache_20261007.py'
    old=prototype.read_text(encoding='utf-8');proto_sha=sha(proto)
    assert proto_sha=='2bf36c66466260f977b66c86dec8285c070ed946c2a4acd35ababeeb15de05f4'
    patches=[("    assert not (A / 'optimization_20261003_r90/protocol.json').exists()","    assert sha(A / 'optimization_20261003_r90/protocol.json') == "+repr(proto_sha)),('    import classifier_consensus_recovery_official_speed_adapter_20261007 as speed','    import classifier_consensus_recovery_official_speed_adapter_v2_20261007 as speed')]
    effective=old
    for before,after in patches:assert effective.count(before)==1;effective=effective.replace(before,after)
    reverse=effective
    for before,after in reversed(patches):reverse=reverse.replace(after,before)
    assert reverse==old;ast.parse(effective)
    bridge=out/'effective_original_R90_bridge_v2.txt';bridge.write_text(effective,encoding='utf-8')
    launcher=A/'run_recovery_qualified_workflow_v2_20261006.py';old_launcher=launcher.read_text(encoding='utf-8')
    log_before="'hidden_child_process_launches.json'";log_after="'hidden_child_process_launches_root_recovery_v2_20261007.json'"
    assert old_launcher.count(log_before)==1
    launch_effective=old_launcher.replace(log_before,log_after);assert launch_effective.replace(log_after,log_before)==old_launcher;ast.parse(launch_effective)
    launcher_bridge=out/'effective_original_recovery_launcher_unique_log_v2.txt';launcher_bridge.write_text(launch_effective,encoding='utf-8')
    sources=[Path(__file__),admission,control,A/'R90_dynamic_score_context_v2_preflight_20261007/frozen_before_actual_control.json',A/'classifier_consensus_recovery_official_speed_adapter_v2_20261007.py',A/'classifier_consensus_standalone_root_resolution_runtime_20261007.py',A/'classifier_consensus_R90_root_resolution_preflight_20261007/verification.json',audit_path,archive,prior/'native_launch.json',prior/'service_execution.json',proto,bridge,launcher_bridge,folder/'component_audit.json']
    pins={**read(proto)['input_sha256'],**{str(p.resolve()):sha(p) for p in sources}}
    frozen=out/'frozen_before_actual_root_resolution_recovery_v2.json'
    create(frozen,{'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'existing_protocol_sha256':proto_sha,'failed_root_recovery_scope_sha256':sha(archive),'only_original_bridge_patches':patches,'only_launcher_log_filename_patch':[log_before,log_after],'reverse_original_sources_exact':True,'verified_existing_baseline_records':1,'all138_original_cases_required':True,'original_scientific_sources_and_protocol_unchanged':True,'new_fits':0,'test_labels_read':False})
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    import frozen_provenance_execution_scope_20261004 as provenance
    original_factory=provenance.FrozenProvenanceExecutionScope;original_args=sys.argv;original_run_path=runpy.run_path
    from hidden_windows_child_creation_20261006 import install as hidden
    restore_children=hidden();restore_roots=None
    with LockedReadHashCache({**pins,str(frozen):sha(frozen)}) as extra_scope:
        assert failed.resolve().is_relative_to(ROOT) and location.resolve().is_relative_to(ROOT)
        assert sha(failed)==sha(archive);failed.rename(location);assert sha(location)==sha(archive) and not failed.exists()
        create(out/'actual_failed_scope_location_archival_v2.json',{'status':'failed_root_recovery_scope_moved_byte_identical_without_edit','archive_path':str(location),'sha256':sha(location),'original_quality_records':1,'prior_owned_worker_closed_failed':True})
        import optimize_training_round90_v3
        from classifier_consensus_standalone_root_resolution_runtime_20261007 import install
        restore_roots,root_metadata=install()
        def supplement(module,extra_sources,metadata,analysis_root):
            scope=original_factory(module,extra_sources,metadata,analysis_root);old_close=scope.close
            def close(failed=False):
                report=old_close(failed=failed)
                assert sha(proto)==proto_sha and sha(location)==sha(archive)==audit['canonical_failed_scope_sha256']
                if not failed:extra_scope.reverify()
                report.update({'actual_root_resolution_recovery_v2':True,'actual_reset_safe_score_context_preflight':str(control),'unique_child_log_runtime_patch':str(launcher_bridge),'failed_root_recovery_scope_archive_path':str(archive),'failed_root_recovery_scope_location_archive_path':str(location),'failed_root_recovery_scope_sha256':sha(archive),'existing_original_protocol_sha256':proto_sha,'existing_original_protocol_bytes_unchanged':True,'additional_actual_recovery_input_sha256':pins,'additional_raw_Windows_read_only_locks_and_final_full_rehash':not failed,'original138_math_params_and_samples_unchanged':True,'root_read_order_installation':root_metadata,'new_model_fits':0})
                return report
            scope.close=close;return scope
        provenance.FrozenProvenanceExecutionScope=supplement
        def routed_run_path(path,*args,**kwargs):
            if Path(path).resolve()!=launcher:return original_run_path(path,*args,**kwargs)
            assert not args and kwargs=={'run_name':'__main__'}
            namespace={'__file__':str(launcher),'__name__':'__main__'}
            exec(compile(launch_effective,str(launcher_bridge),'exec'),namespace);return namespace
        runpy.run_path=routed_run_path
        namespace={'__file__':str(prototype),'__name__':'actual_reset_safe_R90_existing_protocol_recovery_v2'}
        try:
            exec(compile(effective,str(bridge),'exec'),namespace)
            sys.argv=[str(prototype),str(A/'run_training_round90_v3_pipeline.py'),str(A/'service_owned_dependency_queue_v12_local_cache_20261007/activated_jobs/round90/qualified_run.json')]
            namespace['main']()
            actual=read(folder/'provenance_scope_execution.json')
            assert actual['status']=='passed' and actual['actual_original138_quality_records']==138
            assert actual['additional_raw_Windows_read_only_locks_and_final_full_rehash'] and sha(proto)==proto_sha
            extra_scope.reverify()
            create(out/'verification.json',{'status':'passed_actual_original138_science_candidate_full_QA_reset_safe_root_recovery_v2','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'original_protocol_sha256':proto_sha,'actual_closed_scope_sha256':sha(folder/'provenance_scope_execution.json'),'actual_quality_records':138,'new_native_fits':0,'all_original_failed_scope_archives_preserved':True,'main_publication_still_required':True,'test_labels_read':False})
        finally:
            runpy.run_path=original_run_path;sys.argv=original_args;provenance.FrozenProvenanceExecutionScope=original_factory
            if restore_roots is not None:restore_roots()
            create(out/'actual_hidden_recovery_v2_children.json',{'events':restore_children(),'scientific_workers_not_stopped_or_restarted':True})
if __name__=='__main__':main()
