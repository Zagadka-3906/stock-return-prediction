"""Publish completed byte-exact storage relocation proof only; no mutable ranking payload or scientific reexecution."""
from pathlib import Path
import sys,time,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
    proof=A/'current_ranking_JSON_E_relocation_verification_v1_20261008.json';q=read(proof)
    assert q['status']=='passed_actual_single_current_ranking_output_moved_byte_exact_to_E_with_original_path_link'
    assert Path(q['original_path']).is_symlink() and Path(q['original_path']).resolve()==Path(q['physical_path']).resolve()
    assert sha(q['original_path'])==q['original_sha256']==q['linked_sha256']
    sources=[Path(__file__),proof,A/'current_ranking_JSON_E_relocation_plan_v1_20261008.json',
        A/'relocate_current_ranking_JSON_byte_exact_to_E_v1_20261008.py',
        A/'actual_optimization_handoff_main_v18_20261008/receipt.json',
        A/'publish_actual_handoff18_reference_recovery_v2_20261008.py',A/'actual_handoff18_reference_recovery_v2_20261008.json']
    sources += [A/'publish_actual_storage_relocation_evidence_v19_20261008.py',A/'retry_storage_relocation_main_v19_transport_v2_20261008.py',A/'service_owned_workflows_20261006/actual_storage_relocation_main_publication_v19_20261008/service_execution.json',A/'service_owned_workflows_20261006/actual_storage_relocation_main_publication_v19_20261008/stderr.log']
    pins={str(p):sha(p) for p in sources};out=A/'actual_storage_relocation_main_v19_retry2_20261008';assert not out.exists();out.mkdir()
    create(out/'frozen_before_main_publication.json',{'input_sha256':pins,'new_quality_scores':0})
    from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
    from file_backed_hidden_git_runtime_20261007 import installed
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    import publish_classifier_consensus_workflows_20261006 as helpers
    held=[]
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v8_20261008/native_launch.json')
        parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent));create(out/'actual_idle_main_hold.json',idle)
        with installed(out/'file_backed_git'),LockedReadHashCache(pins) as scope:
            sync=helpers.sync;previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous);assert not sync.git('status','--porcelain')
            prefix=Path('validation_sync/actual_storage_relocation_v19_20261008');payload={};bindings={}
            for source in sources:
                data=source.read_bytes();assert not sync.SECRET.search(data)
                target=(prefix/source.relative_to(ROOT)).as_posix();payload[target]=data;bindings[str(source)]={'published_path':target,'sha256':sha(source)}
            payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
            payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'passed_actual_byte_exact_2_729GiB_D_to_E_current_ranking_relocation',
                'at_local':sync.now(),'files':bindings,'bytes_freed_on_D':q['bytes_freed_on_D'],'original_path_kept_by_file_link':True,
                'all_models_scientific_inputs_scores_candidates_and_per_round_archives_untouched':True,'new_quality_scores':0,'main_only':True})
            for name,data in payload.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(payload);sync.git('add','-f','--',*names)
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','记录当前完整榜2.729GiB逐字节移至E并保留原路径，保护继续评分存储空间',timeout=180)
            commit=sync.git('rev-parse','HEAD');expected={name:hashlib.sha256(data).hexdigest() for name,data in payload.items()};assert helpers.blob_hashes(commit,expected)==expected
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit);scope.reverify()
            create(out/'receipt.json',{'status':'pushed_and_remote_head_verified','at_local':sync.now(),'branch':'main','commit':commit,
                'raw_git_blobs_verified':len(expected),'new_quality_scores':0,'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()})
            print('Completed storage relocation evidence published: '+commit,flush=True)
    finally:
        for process in reversed(held):
            if process.is_running():process.resume()
if __name__=='__main__':main()
