"""Publish actual24/588 preflight and7 new plus1 reused jobs, with zero quality/future inference claims."""
from pathlib import Path
import hashlib,sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from file_backed_hidden_git_runtime_20261007 import installed
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
import publish_classifier_consensus_workflows_20261006 as helpers


def main():
    from prepare_Huber52_round137_sources_v1_20261008 import source_paths
    proof_path=A/'Huber52_prospective_routes_v1_20261008.json';proof=read(proof_path)
    assert proof['prospective_sources']==24 and len(proof['graph_controls'])==588
    assert len(proof['baseline_gain_regressions'])==9 and len(proof['model_count_sort_controls'])==6
    for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
    launch_path=A/'Huber137_complete_hidden_launches_v1_20261008.json';launch=read(launch_path)
    assert len(launch['launches'])==8 and launch['new_service_count']==7 and launch['reused_service_count']==1
    sources=[Path(__file__),proof_path,A/'Huber137_complete_dependency_plan_v1_20261008.json',launch_path,
        A/'record_Huber137_receiver_preparation_v1_20261008.py',A/'Huber137_receiver_preparation_v1_20261008.json',
        A/'Huber137_junction_requests_v1_20261008.json',A/'prepare_Huber137_archive_and_publication_v1_20261008.py',
        A/'archive_Huber137_completed_scoring_CSV_v1_20261008.py',A/'actual_Huber137_completed_CSV_archivist_hidden_launch_v1_20261008.json',
        A/'prepare_Huber52_receiver_contract_v1_20261008.py',*[path for path in source_paths() if path.is_file()]]
    for name,row in launch['launches'].items():
        assert row['actual_native_console_handle']==0 and not row['independent_launch_root_in_any_job']
        assert owned(row),name
        folder=A/'service_owned_workflows_20261006'/name;sources += [folder/'job_definition.json',folder/'native_launch.json']
    sources=list(dict.fromkeys(sources));pins={str(path):sha(path) for path in sources}
    out=A/'Huber137_receiver_preflight_main_v1_20261008';assert not out.exists();out.mkdir()
    create(out/'frozen_before_main_publication.json',{'input_sha256':pins,'actual24_receivers588_graphs_passed':True,
        'new_quality_scores':0,'actual136_qualification_exact137_parent_and52_scores_not_yet_claimed':True,'test_labels_read':False})
    held=[]
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v8_20261008/native_launch.json')
        parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent));create(out/'actual_idle_main_hold.json',idle)
        from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
        with installed(out/'file_backed_git'),LockedReadHashCache(pins) as scope:
            sync=helpers.sync;helpers.verify_main(sync.git('rev-parse','HEAD'));assert not sync.git('status','--porcelain')
            prefix=Path('validation_sync/Huber137_receiver_preflight_v1_20261008');targets={};bindings={}
            for source in sources:
                data=source.read_bytes();assert not sync.SECRET.search(data),source
                target=(prefix/source.relative_to(ROOT)).as_posix();targets[target]=data
                bindings[source.relative_to(ROOT).as_posix()]={'published_path':target,'raw_sha256':hashlib.sha256(data).hexdigest()}
            targets[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
            targets[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'actual24_prospective137_receivers_and588_complete_graph_controls_passed_8_dependency_chain_live',
                'at_local':sync.now(),'round':137,'files':bindings,'actual_graph_controls':588,'actual_baseline_controls':9,'actual_model_count_sort_controls':6,
                'actual_cross_volume_probe_bytes':7936,'new_quality_scores':0,'new_fits_by_dispatch':0,
                'actual52_scoring_freeze_future_candidate_QA48_fullboard_and_main_pending':True,'parent_frozen_only_after136_complete_QA47_main':True,
                'three_future_backend_compilations_not_actual_future_replay':True,'test_labels_read':False})
            for name,data in targets.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(targets)
            for left in range(0,len(names),50):sync.git('add','-f','--',*names[left:left+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','同步第137轮Huber52项完整方案接收器、588项父图保留检查及八步骤队列',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={name:hashlib.sha256(data).hexdigest() for name,data in targets.items()};assert helpers.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit);scope.reverify()
            create(out/'receipt.json',{'status':'pushed_and_remote_head_verified','at_local':sync.now(),'branch':'main','commit':commit,
                'raw_git_blobs_verified':len(hashes),'new_quality_scores':0,
                'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()})
            print('Actual24 prospective137 receivers,588 complete graphs and8 real dependencies published to main: '+commit,flush=True)
    finally:
        for process in reversed(held):
            if process.is_running():process.resume()


if __name__=='__main__':main()
