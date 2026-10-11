"""Resume original138-case R90 from exact frozen protocol, archive its unpinned failed attempt."""
from pathlib import Path
import ast
import sys
import time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def main():
    import psutil
    out=A/'classifier_consensus_R90_root_resolution_recovery_20261007';assert not out.exists();out.mkdir()
    admission=read(A/'classifier_consensus_R90_root_resolution_recovery_admission_20261007.json')
    for path,digest in admission['input_sha256'].items():assert sha(path)==digest,path
    preflight=A/'classifier_consensus_R90_root_resolution_preflight_20261007/verification.json'
    assert read(preflight)['status']=='passed_actual_six_R90_standalone_root_empty_foundation_and_exact_original_hybrid_and_negative_controls'
    pub=A/'full_universe_HGB_and_R90_root_controls_github_20261007/receipt.json';assert read(pub)['status']=='pushed_and_remote_head_verified'
    prior=A/'service_owned_dependency_queue_v12_local_cache_20261007/activated_jobs/round90'
    assert not owned(read(prior/'launch.json')) and read(prior/'execution.json')['status']=='failed'
    state=read(A/'service_owned_dependency_queue_v4_20261006/state.json')
    assert not any(n.startswith('round') and owned(r) for n,r in state['activated_jobs'].items())
    while psutil.virtual_memory().available<9*2**30:time.sleep(15)
    folder=A/'optimization_20261003_r90';proto=folder/'protocol.json';failed=folder/'provenance_scope_execution.json'
    archive=folder/'provenance_scope_execution_failed_original_20261007.json'
    location_archive=folder/'provenance_scope_execution_failed_location_archive_20261007.json'
    assert failed.resolve().is_relative_to(ROOT) and location_archive.resolve().is_relative_to(ROOT)
    audit=read(A/'R90_failed_scope_canonical_non_pinning_audit_20261007.json')
    assert audit['matched_files']==[] and sha(failed)==sha(archive)==audit['canonical_failed_scope_sha256']
    assert not location_archive.exists() and read(failed)['actual_original138_quality_records']==0
    assert not list(folder.glob('wave*_results.json'))
    prototype=A/'run_classifier_consensus_round90_with_precise_gate_and_parent_cache_20261007.py'
    old_text=prototype.read_text(encoding='utf-8');proto_sha=sha(proto)
    before="    assert not (A / 'optimization_20261003_r90/protocol.json').exists()"
    after="    assert sha(A / 'optimization_20261003_r90/protocol.json') == "+repr(proto_sha)
    assert old_text.count(before)==1
    effective=old_text.replace(before,after);assert effective.replace(after,before)==old_text;ast.parse(effective)
    effective_path=out/'effective_original_R90_bridge.txt'
    with effective_path.open('x',encoding='utf-8') as f:f.write(effective)
    sources=[Path(__file__),A/'classifier_consensus_R90_root_resolution_recovery_admission_20261007.json',A/'classifier_consensus_standalone_root_resolution_runtime_20261007.py',preflight,pub,A/'R90_failed_scope_canonical_non_pinning_audit_20261007.json',archive,prior/'execution.json',prior/'launch.json',proto,effective_path]
    pins={**read(proto)['input_sha256'],**{str(p.resolve()):sha(p) for p in sources}}
    frozen=out/'frozen_before_actual_root_resolution_recovery.json'
    create(frozen,{'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'existing_protocol_sha256':proto_sha,'original_failed_scope_sha256':sha(archive),'original_failed_scope_archive':str(archive),'original_scope_location_archive':str(location_archive),'only_bridge_guard_patch':{'before':before,'after':after,'reverse_original_source_text_exact':True},'canonical_new_scope_written_only_after_actual_execution':True,'no_existing_protocol_or_scientific_source_rewritten':True,'original138_cases_all_required':True,'new_native_fits':0,'test_labels_read':False})
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    import frozen_provenance_execution_scope_20261004 as provenance
    original_factory=provenance.FrozenProvenanceExecutionScope
    original_args=sys.argv;restore_roots=None;restore_children=None
    from hidden_windows_child_creation_20261006 import install as hidden
    restore_children=hidden()
    with LockedReadHashCache({**pins,str(frozen):sha(frozen)}) as extra_scope:
        # Original198-source frozen protocol and its metadata stay byte-identical;
        # the actual new recovery code is separately locked and fully rehashed.
        assert sha(proto)==proto_sha and sha(failed)==sha(archive)
        failed.rename(location_archive)
        assert sha(location_archive)==sha(archive) and not failed.exists()
        create(out/'actual_failed_scope_location_archival.json',{'status':'original_unpinned_failed_record_moved_byte_identical_without_edit','original_path':str(failed),'archive_path':str(location_archive),'sha256':sha(location_archive),'independent_first_archive_sha256':sha(archive),'original_worker_strong_identity_closed_failed':True,'original_score_records':0})
        import optimize_training_round90_v3
        from classifier_consensus_standalone_root_resolution_runtime_20261007 import install
        restore_roots,root_metadata=install()
        def supplement(module,extra_sources,metadata,analysis_root):
            scope=original_factory(module,extra_sources,metadata,analysis_root)
            original_close=scope.close
            def close(failed=False):
                report=original_close(failed=failed)
                assert sha(proto)==proto_sha
                assert sha(location_archive)==sha(archive)==audit['canonical_failed_scope_sha256']
                if not failed:extra_scope.reverify()
                report.update({'actual_root_resolution_recovery':True,'original_failed_scope_byte_identical_archives_preserved':True,'original_failed_scope_sha256':sha(archive),'original_failed_scope_archive_path':str(archive),'original_failed_scope_location_archive_path':str(location_archive),'existing_original_protocol_sha256':proto_sha,'existing_original_protocol_bytes_unchanged':True,'additional_actual_recovery_input_sha256':pins,'additional_raw_Windows_read_only_locks_and_final_full_rehash':not failed,'original138_math_params_and_samples_unchanged':True,'root_read_order_controls':str(preflight),'root_read_order_installation':root_metadata,'new_model_fits':0})
                return report
            scope.close=close
            return scope
        provenance.FrozenProvenanceExecutionScope=supplement
        namespace={'__file__':str(prototype),'__name__':'actual_precise_R90_existing_protocol_guard_recovery'}
        try:
            exec(compile(effective,str(effective_path),'exec'),namespace)
            sys.argv=[str(prototype),str(A/'run_training_round90_v3_pipeline.py'),str(prior/'qualified_run.json')]
            namespace['main']()
            actual=read(folder/'provenance_scope_execution.json')
            assert actual['status']=='passed' and actual['actual_original138_quality_records']==138
            assert actual['additional_raw_Windows_read_only_locks_and_final_full_rehash'] and actual['existing_original_protocol_bytes_unchanged']
            assert sha(proto)==proto_sha;extra_scope.reverify()
            create(out/'verification.json',{'status':'passed_actual_original138_science_candidate_full_QA_root_read_order_recovery','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'original_protocol_sha256':proto_sha,'original_failed_scope_sha256':sha(archive),'actual_closed_scope_sha256':sha(folder/'provenance_scope_execution.json'),'actual_quality_records':138,'new_native_fits':0,'original_sources_and_grid_and_old_failed_archives_byte_identical':True,'main_publication_still_required':True,'test_labels_read':False})
        finally:
            sys.argv=original_args;provenance.FrozenProvenanceExecutionScope=original_factory
            if restore_roots is not None:restore_roots()
            create(out/'actual_hidden_recovery_children.json',{'events':restore_children(),'scientific_workers_not_stopped_or_restarted':True})
if __name__=='__main__':main()
