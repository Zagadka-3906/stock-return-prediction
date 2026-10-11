"""Publish actual24 receiver checks and real eight-service dispatch to main;94 scores remain pending."""
from pathlib import Path
import hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from file_backed_hidden_git_runtime_20261007 import installed
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
import publish_classifier_consensus_workflows_20261006 as helpers


def main():
    folder=A/'service_owned_workflows_20261006/CrossFamily136_complete_pipeline_dispatch_v2_20261008'
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(10)
    assert read(folder/'service_execution.json')['status']=='passed'
    proof_path=A/'CrossFamily94_prospective_routes_v2_20261008.json';proof=read(proof_path)
    assert proof['prospective_sources']==24 and len(proof['graph_controls'])==186
    for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
    from prepare_CrossFamily94_round136_sources_v2_20261008 import source_paths
    launch_path=A/'CrossFamily136_complete_hidden_launches_v2_20261008.json';launch=read(launch_path);assert len(launch['launches'])==8
    sources=[Path(__file__),proof_path,A/'CrossFamily136_receiver_preparation_v2_20261008.json',
        A/'CrossFamily136_complete_dependency_plan_v2_20261008.json',launch_path,A/'actual_CrossFamily136_complete_dispatch_v2_20261008.json',
        A/'CrossFamily136_metadata_receiver_preparation_v2_20261008.json',A/'prepare_CrossFamily136_metadata_receivers_v2_20261008.py',
        A/'CrossFamily94_prospective_routes_v1_20261008.json',A/'CrossFamily136_receiver_preparation_v1_20261008.json',
        A/'archive_CrossFamily136_completed_scoring_CSV_v1_20261008.py',A/'actual_CrossFamily136_completed_CSV_archivist_hidden_launch_v1_20261008.json',
        A/'CrossFamily_preliminary_controls_main_v1_20261008/bank/receipt.json',A/'CrossFamily_preliminary_controls_main_v1_20261008/historical/receipt.json',
        *[path for path in source_paths() if path.is_file()],*folder.glob('*.json'),*folder.glob('*.log')]
    for name in launch['launches']:
        service=A/'service_owned_workflows_20261006'/name;sources += [service/'job_definition.json',service/'native_launch.json']
    sources=list(dict.fromkeys(sources));pins={str(path):sha(path) for path in sources}
    out=A/'CrossFamily136_receiver_preflight_main_v2_20261008';assert not out.exists();out.mkdir()
    create(out/'frozen_before_main_publication.json',{'input_sha256':pins,'actual24_prospective_receivers_passed':True,
        'actual135_qualification_current_parent_and94_scores_not_yet_claimed':True,'new_quality_scores':0,'test_labels_read':False})
    held=[]
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v8_20261008/native_launch.json')
        parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        create(out/'actual_idle_main_hold.json',idle)
        from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
        with installed(out/'file_backed_git'),LockedReadHashCache(pins) as scope:
            sync=helpers.sync;helpers.verify_main(sync.git('rev-parse','HEAD'));assert not sync.git('status','--porcelain')
            prefix=Path('validation_sync/CrossFamily136_receiver_preflight_v2_20261008');targets={};bindings={}
            for source in sources:
                data=source.read_bytes();assert not sync.SECRET.search(data),source
                target=(prefix/source.relative_to(ROOT)).as_posix();targets[target]=data
                bindings[source.relative_to(ROOT).as_posix()]={'published_path':target,'raw_sha256':hashlib.sha256(data).hexdigest()}
            targets[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
            targets[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'actual24_prospective136_receivers_passed_and8_lazy_jobs_dispatched',
                'at_local':sync.now(),'round':136,'files':bindings,'actual_graph_controls':186,'actual_baseline_controls':9,'actual_model_count_sort_controls':6,
                'actual_cross_volume_probe_bytes':7936,'new_quality_scores':0,'actual94_scoring_and_selected_future_candidate_QA47_pending':True,
                'final_parent_frozen_only_after135_fully_qualified':True,'test_labels_read':False})
            for name,data in targets.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(targets)
            for left in range(0,len(names),50):sync.git('add','-f','--',*names[left:left+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','同步第136轮94项跨模型集成的24项接收器、D/E路径检查及完整八步骤队列',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={name:hashlib.sha256(data).hexdigest() for name,data in targets.items()}
            assert helpers.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit);scope.reverify()
            create(out/'receipt.json',{'status':'pushed_and_remote_head_verified','at_local':sync.now(),'branch':'main','commit':commit,
                'raw_git_blobs_verified':len(hashes),'new_quality_scores':0,
                'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()})
            print('Actual24 prospective136 receivers and real eight-service dispatch published to main: '+commit,flush=True)
    finally:
        for process in reversed(held):
            if process.is_running():process.resume()


if __name__=='__main__':main()
