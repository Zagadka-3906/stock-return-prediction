"""Actual six standalone graphs and exact original nonstandalone root-source controls."""
from pathlib import Path
from copy import deepcopy
import sys
import time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def main():
    out=A/'classifier_consensus_R90_root_resolution_preflight_20261007';assert not out.exists();out.mkdir()
    old_service=A/'service_owned_dependency_queue_v12_local_cache_20261007/activated_jobs/round90'
    assert not owned(read(old_service/'launch.json'))
    assert read(old_service/'execution.json')['status']=='failed'
    failed=A/'optimization_20261003_r90/provenance_scope_execution_failed_original_20261007.json'
    scope=read(failed);assert scope['status']=='failed' and scope['actual_original138_quality_records']==0
    assert 'optimization_20261003_r90' in scope['failure'] and 'verification.json' in scope['failure']
    protocol=A/'optimization_20261003_r90/protocol.json'
    sources=[Path(__file__),A/'classifier_consensus_standalone_root_resolution_runtime_20261007.py',A/'optimize_training_round50.py',A/'ready_classifier_consensus_reference_search_engine_v2_20261006.py',protocol,failed,old_service/'execution.json',old_service/'launch.json',A/'github_validation_sync_main_20261005/round89_receipt.json',ROOT/'后续选模标准.md']
    pins={**read(protocol)['input_sha256'],**{str(p.resolve()):sha(p) for p in sources}}
    create(out/'frozen_before_actual_root_controls.json',{'input_sha256':pins,'original138_grid_frozen_before_this_fix':True,'original_scored_records':0,'new_fits':0,'new_quality_scores':0,'test_labels_read':False})
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    import optimize_training_round90_v3 as module
    import optimize_training_round50 as owner
    from classifier_consensus_standalone_root_resolution_runtime_20261007 import install
    with LockedReadHashCache(pins) as held:
        cfg=module.baseline();graph=cfg[module.GRAPH_FIELD];original=owner.root_model_sources
        baseline=original(graph);assert module.root_model_sources(graph)==baseline
        positives=[]
        graphs=[(name,module.standalone_cfg(name)[module.GRAPH_FIELD]) for name in module.MODELS]
        assert len(graphs)==6
        for name,g in graphs:
            assert g['root']['kind']=='standalone' and g['root']['round']==90 and not g['layers']
            assert not (ROOT/'candidates/optimization_20261003_r90/verification.json').exists()
            try:original(g)
            except FileNotFoundError as e:assert 'optimization_20261003_r90' in str(e)
            else:raise AssertionError('Original expected premature self-candidate lookup was not reproduced')
        restore,details=install()
        try:
            assert owner.root_model_sources(graph)==baseline and module.root_model_sources(graph)==baseline
            for name,g in graphs:
                assert owner.root_model_sources(g)=={} and module.root_model_sources(g)=={}
                native=module.future_native_sources(g);assert native
                for key,item in native.items():
                    assert item['sha256']==read(protocol)['future_native_model_sources'][key]['sha256']
                    assert sha(item['path'])==item['sha256']
                positives.append({'model':name,'standalone_foundation_empty':True,'actual_native_sources':native,'premature_self_candidate_lookup_reproduced_before_and_avoided_after':True})
            bad=deepcopy(graph);bad['root']['kind']='complete_r30';bad['root']['round']=999999;bad['root']['configuration']['standalone']=None
            try:owner.root_model_sources(bad)
            except FileNotFoundError as e:assert 'r999999' in str(e)
            else:raise AssertionError('Nonstandalone missing-candidate negative control did not fail')
        finally:restore()
        assert owner.root_model_sources is original and module.root_model_sources is original
        held.reverify();create(out/'verification.json',{'status':'passed_actual_six_R90_standalone_root_empty_foundation_and_exact_original_hybrid_and_negative_controls','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'records':positives,'installation':details,'actual_original_failure_reproduced_for_all6':True,'original_nonstandalone_foundation_info_exact':True,'nonstandalone_missing_candidate_negative_control_preserved':True,'original_function_bindings_restored':True,'original138_scores_not_yet_executed':True,'new_fits':0,'new_quality_scores':0,'test_labels_read':False})
if __name__=='__main__':main()
