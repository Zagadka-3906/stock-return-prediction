"""Publish actual draft regression and retained parse failure; no official150 score is claimed."""
from pathlib import Path
import hashlib,sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def main():
    prior=A/'service_owned_workflows_20261006/actual_phase_recovery_and_stop_main_publication_v40_20261008'
    assert read(prior/'service_execution.json')['status']=='passed' and not owned(read(prior/'native_launch.json'))
    # The147 writer cannot publish before all185 official records; this short evidence commit precedes it.
    assert len(list((A/'JointCrossHuberOrder185_official_comparison_v1_20261008').glob('case*_official.json')))<175
    from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
    from verified_TLS_Git_retry_runtime_v2_20261008 import installed
    import publish_classifier_consensus_workflows_20261006 as helpers
    out=Path('E:/赛题五_本机临时/actual150_receiver_drafts_main_v41_20261008');out.mkdir(exist_ok=False);held=[]
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v8_20261008/native_launch.json');assert owned(row)
        parent,worker,proof=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        create(out/'main_watcher_idle_hold.json',{'identity':row,'stack':proof,'scientific_workers_held':0})
        preparation=read(A/'HuberSparse150_core_receiver_draft_preparation_v2_20261008.json')
        paths=[Path(__file__),A/'HuberSparse150_core_draft_parse_failure_v1_20261008.json',A/'prepare_HuberSparse150_core_receiver_drafts_v1_20261008.py',A/'prepare_HuberSparse150_core_receiver_drafts_v2_20261008.py',A/'HuberSparse150_core_receiver_draft_preparation_v2_20261008.json',A/'verify_HuberSparse150_draft_control_bindings_v1_20261008.py',A/'HuberSparse150_draft_control_bindings_v1_20261008.json',*[Path(p) for p in preparation['input_sha256']],A/'current_user_runtime_control_20261008.json']
        sync=helpers.sync;prefix=Path('validation_sync/actual150_receiver_drafts_v41_20261008');payload={};bindings={}
        for source in dict.fromkeys(paths):
            data=source.read_bytes();assert not sync.SECRET.search(data),source
            assert source.is_relative_to(ROOT)
            target=(prefix/source.relative_to(ROOT)).as_posix();payload[target]=data
            bindings[str(source)]={'published_path':target,'raw_sha256':hashlib.sha256(data).hexdigest(),'original_bytes':len(data)}
        payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
        payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'actual55_control_binding_regression_six_prepared_receiver_drafts_and_retained_parse_failure',
            'at_local':sync.now(),'files':bindings,'actual_bound_full_training_controls':55,'actual_empty_E_outputs_verified':6,
            'first_draft_parse_failure_before_any_output_mutation_preserved':True,'full_source_admission_not_completed':True,
            'actual150_official_scores':0,'actual150_future_inference':0,'new_native_fits':0,'test_labels_read':False,
            'prior_actual72_native_and55_full165_cold_proofs_already_on_main':True,'primary_workspace_dirty_index_preserved':True,
            'actual_stop_at_local':'2026-10-08T23:55:00+08:00','automatic_restart_enabled':False,'global_search_exhaustion_claimed':False})
        create(out/'frozen_before_main_publication.json',{'files':bindings,'quality_source_admitted':False})
        with installed(out/'file_backed_git'):
            previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous);assert not sync.git('status','--porcelain')
            for name,data in payload.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(payload)
            for left in range(0,len(names),50):sync.git('add','-f','--',*names[left:left+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','同步150轮55控制绑定回归、六个未准入草稿与保留的解析失败',timeout=120)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()};assert helpers.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=120);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit)
            receipt={'status':'pushed_and_remote_head_verified','at_local':sync.now(),'branch':'main','commit':commit,'raw_git_blobs_verified':len(hashes),'new_quality_scores':0,'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()}
            create(out/'receipt.json',receipt);create(A/'actual150_receiver_drafts_main_v41_receipt_20261008.json',receipt);print(receipt,flush=True)
    finally:
        for p in reversed(held):
            if p.is_running():p.resume()
        create(out/'idle_publisher_resumed.json',{'held_processes':len(held),'resumed_in_finally':True,'scientific_workers_held':0})
if __name__=='__main__':main()
