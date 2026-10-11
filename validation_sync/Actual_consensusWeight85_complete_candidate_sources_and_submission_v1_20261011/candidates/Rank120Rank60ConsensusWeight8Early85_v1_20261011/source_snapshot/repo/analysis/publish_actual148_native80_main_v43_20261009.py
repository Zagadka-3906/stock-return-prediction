"""Publish actual draft regression and retained parse failure; no official150 score is claimed."""
from pathlib import Path
import hashlib,sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def main():
    prior=A/'service_owned_workflows_20261006/actual_manual_resume_runtime_main_publication_v42_20261009'
    assert read(prior/'service_execution.json')['status']=='passed' and not owned(read(prior/'native_launch.json'))
    # The147 writer cannot publish before all185 official records; this short evidence commit precedes it.
    import time
    full=A/'service_owned_workflows_20261006/JointCrossHuberOrder185_round147_full_registration_v2_20261009'
    while not (full/'service_execution.json').exists() or owned(read(full/'native_launch.json')):time.sleep(10)
    assert read(full/'service_execution.json')['status']=='passed'
    assert read(A/'optimization_20261003_r147/full_registration_execution.json')['status']=='passed'
    from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
    from verified_TLS_Git_retry_runtime_v2_20261008 import installed
    import publish_classifier_consensus_workflows_20261006 as helpers
    out=Path('E:/赛题五_本机临时/actual148_native80_main_v43_20261009');out.mkdir(exist_ok=False);held=[]
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v9_20261009/native_launch.json');assert owned(row)
        parent,worker,proof=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        create(out/'main_watcher_idle_hold.json',{'identity':row,'stack':proof,'scientific_workers_held':0})
        preparation=read(A/'HuberSparse150_core_receiver_draft_preparation_v2_20261008.json')
        paths=[Path(__file__),A/'HuberSparse150_core_draft_parse_failure_v1_20261008.json',A/'prepare_HuberSparse150_core_receiver_drafts_v1_20261008.py',A/'prepare_HuberSparse150_core_receiver_drafts_v2_20261008.py',A/'HuberSparse150_core_receiver_draft_preparation_v2_20261008.json',A/'verify_HuberSparse150_draft_control_bindings_v1_20261008.py',A/'HuberSparse150_draft_control_bindings_v1_20261008.json',*[Path(p) for p in preparation['input_sha256']],A/'current_user_runtime_control_20261008.json']
        since=__import__('datetime').datetime(2026,10,9,12,0).timestamp()
        paths.extend(p for p in A.iterdir() if p.is_file() and p.suffix in ('.py','.json') and p.stat().st_mtime>=since)
        for folder in (A/'service_owned_workflows_20261006').iterdir():
            if not folder.is_dir():continue
            entries=[p for p in folder.iterdir() if p.is_file() and p.suffix in ('.json','.log')]
            if any(p.stat().st_mtime>=since for p in entries):paths.extend(entries)
        paths.extend((A/'user_requested_stop2355_until_manual_continue_v2_20261008').glob('*.json'))
        paths.extend([A/'github_validation_sync_main_20261005/round147_receipt.json',A/'optimization_20261003_r147/full_registration_execution.json',A/'optimization_20261003_r147/provenance_scope_execution.json',A/'optimization_20261003_r147/calibrated_csv_official.json',A/'actual148149_manual_resume_AST_preflight_v1_20261009.json'])
        native_pointer=A/'actual_AdaptiveJointCrossHuber80_native_calendar_location_v3_20261008.json'
        native_folder=Path(read(native_pointer)['output']);native_proof=native_folder/'verification.json'
        assert sha(native_proof)==read(native_pointer)['verification_sha256']
        native_check=read(native_proof);assert (native_check['actual_historical_cases'],native_check['actual_calendar_cases'],native_check['actual_cold_cases'])==(60,20,80)
        paths.extend([native_pointer,*native_folder.glob('*.json'),A/'actual_optimization_checkpoint_v47_20261009.json',A/'actual_delivery_checkpoint47_wrong_manifest_name_failure_v1_20261009.json'])
        sync=helpers.sync;prefix=Path('validation_sync/actual148_native80_v43_20261009');payload={};bindings={}
        for source in dict.fromkeys(paths):
            data=source.read_bytes();assert not sync.SECRET.search(data),source
            assert source.is_relative_to(ROOT)
            target=(prefix/source.relative_to(ROOT)).as_posix();payload[target]=data
            bindings[str(source)]={'published_path':target,'raw_sha256':hashlib.sha256(data).hexdigest(),'original_bytes':len(data)}
        payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
        payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'actual148_native60_calendar20_cold80_completed_original35_states_reused_with147_qualified_delivery',
            'at_local':sync.now(),'files':bindings,'actual_bound_full_training_controls':55,'actual_empty_E_outputs_verified':6,
            'first_draft_parse_failure_before_any_output_mutation_preserved':True,'full_source_admission_not_completed':True,
            'actual150_official_scores':0,'actual150_future_inference':0,'new_native_fits':0,'test_labels_read':False,
            'prior_actual72_native_and55_full165_cold_proofs_already_on_main':True,'primary_workspace_dirty_index_preserved':True,
            'previous_actual_stop_at_local':'2026-10-08T23:55:00+08:00','actual_user_continue_received_on':'2026-10-09','expired_stop_schedule_not_restarted':True,'actual147_two_full_native_independent_csv_replays_and_cold80_full_QA58_main_completed':True,'actual147_official_score':0.4511896739186047,'actual147_full_main_commit':read(A/'github_validation_sync_main_20261005/round147_receipt.json')['commit'],'actual148149_twenty_receiver_AST_controls_passed':True,'actual148149_source_math_and_predeclared_case_grids_unchanged':True,'actual148149_results_have_only_their_own_live_statuses_not_blanket_completion_claims':True,'actual148_native_historical60_calendar20_cold80_passed':True,'actual148_full238_and242_quality_and_selected_future_qualification_have_only_actual_live_statuses':True,'automatic_restart_enabled':False,'global_search_exhaustion_claimed':False})
        create(out/'frozen_before_main_publication.json',{'files':bindings,'quality_source_admitted':False})
        with installed(out/'file_backed_git'):
            previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous);assert not sync.git('status','--porcelain')
            for name,data in payload.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(payload)
            for left in range(0,len(names),50):sync.git('add','-f','--',*names[left:left+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','同步148轮60历史20日历80冷原生复现与已合格147轮交付核对',timeout=120)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()};assert helpers.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=120);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit)
            receipt={'status':'pushed_and_remote_head_verified','at_local':sync.now(),'branch':'main','commit':commit,'raw_git_blobs_verified':len(hashes),'new_quality_scores':0,'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()}
            create(out/'receipt.json',receipt);create(A/'actual_manual_resume_runtime_main_v42_receipt_20261008.json',receipt);print(receipt,flush=True)
    finally:
        for p in reversed(held):
            if p.is_running():p.resume()
        create(out/'idle_publisher_resumed.json',{'held_processes':len(held),'resumed_in_finally':True,'scientific_workers_held':0})
if __name__=='__main__':main()
