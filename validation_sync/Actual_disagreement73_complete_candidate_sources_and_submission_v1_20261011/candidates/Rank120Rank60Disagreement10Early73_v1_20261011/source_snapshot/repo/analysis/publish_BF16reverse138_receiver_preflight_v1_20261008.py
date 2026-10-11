"""Publish a frozen new direction, actual synthetic controls, native prototypes and honest handoff."""
from pathlib import Path
import hashlib,sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from file_backed_hidden_git_runtime_20261007 import installed
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
import publish_classifier_consensus_workflows_20261006 as helpers


def main():
    plan=A/'BF16reverse40_round138_plan_v1_20261008.json';synthetic=A/'BF16_reverse_rank_CDF_synthetic_preflight_v1_20261008/verification.json'
    proof=read(synthetic);assert (proof['actual_cases'],proof['actual_day_controls'],proof['actual_quality_scores'])==(39,78,0)
    native=A/'BF16_reverse_native_receiver_preparation_v1_20261008.json';assert len(read(native)['controls'])==4
    handoff=A/'actual_optimization_handoff_v9_20261008.json';state=read(handoff)
    assert state['goal_active_not_paused_complete_or_blocked'] and not state['test_labels_read']
    sources=[Path(__file__),plan,synthetic,native,handoff,A/'actual_optimization_handoff_v9_20261008.md',
        A/'record_actual_optimization_handoff_v9_20261008.py',A/'prepare_BF16reverse40_round138_plan_and_controls_v1_20261008.py',
        A/'BF16_reverse_complete_parent_rank_CDF_v1_20261008.py',A/'BF16_reverse_complete_parent_native_stage_v1_20261008.py',
        A/'predict_BF16_reverse_complete_parent_scheme_v1_20261008.py',A/'prepare_BF16_reverse_native_receiver_v1_20261008.py',
        A/'verify_BF16_reverse_rank_CDF_full37_v1_20261008.py',A/'prepare_BF16_reverse_historical_hooks_v1_20261008.py',
        A/'verify_BF16_reverse_complete_parent_native_hook3_v1_20261008.py',A/'actual_BF16reverse40_plan_and_full37_hidden_launch_v1_20261008.json',
        A/'actual_BF16_reverse_historical_native_hook3_hidden_launch_v1_20261008.json',
        A/'monitor_neural135_and_CrossFamily136_v5_20261008.py',A/'actual_optimization135136137_progress_hidden_launch_v5_20261008.json',
        A/'multiyear136137_recovery_main_v2_20261008/receipt.json']
    sources += list(synthetic.parent.glob('*.json'))
    for name in ('BF16_reverse_rank_CDF_actual_full37_controls_v1_20261008','BF16_reverse_complete_parent_actual_historical_native_hook3_v1_20261008'):
        folder=A/'service_owned_workflows_20261006'/name;row=read(folder/'native_launch.json');assert owned(row) and row['actual_native_console_handle']==0
        sources += [folder/'native_launch.json',folder/'job_definition.json']
    from prepare_BF16reverse40_round138_sources_v1_20261008 import source_paths
    routes=A/'BF16reverse40_prospective_routes_v1_20261008.json';route_proof=read(routes)
    assert route_proof['prospective_sources']==24 and len(route_proof['graph_controls'])==444
    assert len(route_proof['baseline_gain_regressions'])==9 and len(route_proof['model_count_sort_controls'])==6
    sources += [p for p in source_paths() if p.is_file()]
    sources += [routes,A/'BF16reverse138_complete_dependency_plan_v1_20261008.json',A/'BF16reverse138_complete_hidden_launches_v1_20261008.json',
        A/'BF16reverse138_junction_requests_v1_20261008.json',A/'verify_BF16reverse40_prospective_routes_v2_20261008.py',
        A/'prepare_BF16reverse138_preflight_v1_20261008.py',A/'BF16reverse138_prospective_scope_reference_recovery_v1_20261008.json',
        A/'verify_BF16reverse138_model_count_contract_v1_20261008.py',A/'BF16reverse138_model_count_contract_v1_20261008.json',
        A/'archive_BF16reverse138_completed_scoring_CSV_v1_20261008.py',A/'actual_BF16reverse138_completed_CSV_archivist_hidden_launch_v1_20261008.json',
        A/'monitor_neural135_CrossFamily136_Huber137_BF16reverse138_v6_20261008.py',A/'actual_optimization135136137138_progress_hidden_launch_v6_20261008.json']
    for p,d in route_proof['input_sha256'].items():assert sha(p)==d,p
    for name,row in read(A/'BF16reverse138_complete_hidden_launches_v1_20261008.json')['launches'].items():
        assert owned(row) and row['actual_native_console_handle']==0,name
        folder=A/'service_owned_workflows_20261006'/name;sources += [folder/'native_launch.json',folder/'job_definition.json']
    sources=list(dict.fromkeys(sources));pins={str(p):sha(p) for p in sources}
    for item in (proof,read(native)):
        for p,d in item['input_sha256'].items():assert sha(p)==d,p
    out=A/'BF16reverse138_receiver_preflight_main_v1_20261008';assert not out.exists();out.mkdir()
    create(out/'frozen_before_main_publication.json',{'input_sha256':pins,'actual39_synthetic78_day_controls':True,
        'four_backend_compilations_not_actual_inference':True,'new_official_scores':0,'new_fits':0,'test_labels_read':False})
    held=[]
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v8_20261008/native_launch.json')
        parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent));create(out/'actual_idle_main_hold.json',idle)
        from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
        with installed(out/'file_backed_git'),LockedReadHashCache(pins) as scope:
            sync=helpers.sync;helpers.verify_main(sync.git('rev-parse','HEAD'));assert not sync.git('status','--porcelain')
            prefix=Path('validation_sync/BF16reverse138_receiver_preflight_v1_20261008');targets={};bindings={}
            for source in sources:
                assert source.is_relative_to(ROOT);data=source.read_bytes();assert not sync.SECRET.search(data),source
                target=(prefix/source.relative_to(ROOT)).as_posix();targets[target]=data
                bindings[source.relative_to(ROOT).as_posix()]={'published_path':target,'raw_sha256':hashlib.sha256(data).hexdigest()}
            targets[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
            targets[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'actual24_138_receivers444_graphs_and39_78_reverse_neural_controls_with_handoff9',
                'at_local':sync.now(),'files':bindings,'planned_round':138,'expected_official_cases':40,
                'actual_prospective_receivers':24,'actual_complete_parent_graphs':444,'actual_baseline_controls':9,'actual_same_S_model_sort_controls':6,'actual_model_SHA_union_controls':8,'actual_original_scope_controls':9,
                'current138_full_quality_pipeline_queued':True,'actual_synthetic_cases':39,'actual_day_prefix_controls':78,'actual_backend_compilations':4,
                'new_official_scores':0,'new_fits':0,'actual_future_feature_X_and_Y_read':False,
                'actual_full37_111cold_historical_native3_and40_quality_candidate_QA49_main_still_required':True,
                'goal_active_and_global_exhaustion_not_claimed':True,'current135136137_queues_owned_live':True,'main_only':True})
            for name,data in targets.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(targets)
            for left in range(0,len(names),50):sync.git('add','-f','--',*names[left:left+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','同步第138轮24接收器444父图及8模型去重检查、完整七阶段队列和交接9',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={name:hashlib.sha256(data).hexdigest() for name,data in targets.items()}
            assert helpers.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit);scope.reverify()
            create(out/'receipt.json',{'status':'pushed_and_remote_head_verified','at_local':sync.now(),'branch':'main','commit':commit,
                'raw_git_blobs_verified':len(hashes),'new_official_scores':0,
                'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()})
            print('Reverse neural actual39/78 controls,40-case plan and current handoff published to main: '+commit,flush=True)
    finally:
        for process in reversed(held):
            if process.is_running():process.resume()


if __name__=='__main__':main()
