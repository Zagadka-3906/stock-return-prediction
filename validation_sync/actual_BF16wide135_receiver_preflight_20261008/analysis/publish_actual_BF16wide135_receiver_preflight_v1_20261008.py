"""Publish the actually passed24 receiver checks and complete lazy dispatch now; full GPU and quality remain pending."""
from pathlib import Path
import hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from file_backed_hidden_git_runtime_20261007 import installed
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
import publish_classifier_consensus_workflows_20261006 as helpers


def main():
    folder=A/'service_owned_workflows_20261006/BF16wide135_complete_pipeline_dispatch_v1_20261008'
    while not (folder/'service_execution.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(10)
    assert read(folder/'service_execution.json')['status']=='passed'
    proof_path=A/'BF16wide40_prospective_routes_v1_20261008.json';proof=read(proof_path)
    assert proof['status']=='passed_actual24_prospective135_sources_schema_graphs_baselines_status_paths_and_cross_volume_bytes'
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    from prepare_BF16wide40_round135_sources_v1_20261008 import source_paths
    launch_path=A/'BF16wide135_complete_hidden_launches_v1_20261008.json';launch=read(launch_path)
    assert len(launch['launches'])==7
    sources=[Path(__file__),proof_path,A/'record_BF16wide135_receiver_preparation_v1_20261008.py',
        A/'BF16wide135_receiver_preparation_v1_20261008.json',A/'BF16wide135_complete_dependency_plan_v1_20261008.json',
        launch_path,A/'actual_BF16wide135_complete_pipeline_dispatch_v1_20261008.json',
        A/'github_validation_sync_main_20261005/round134_receipt.json',*[p for p in source_paths() if p.is_file()],
        *folder.glob('*.json'),*folder.glob('*.log')]
    for name in launch['launches']:
        service=A/'service_owned_workflows_20261006'/name
        sources += [service/'job_definition.json',service/'native_launch.json']
    sources=list(dict.fromkeys(sources));pins={str(p):sha(p) for p in sources}
    out=A/'actual_BF16wide135_receiver_preflight_main_v1_20261008';assert not out.exists();out.mkdir()
    create(out/'frozen_before_main_publication.json',{'input_sha256':pins,'actual24_prospective_receivers_passed':True,
        'full_GPU_controls_and_quality_not_yet_claimed':True,'new_quality_scores':0,'test_labels_read':False})
    held=[]
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v8_20261008/native_launch.json')
        parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        create(out/'actual_idle_main_hold.json',idle)
        from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
        with installed(out/'file_backed_git'),LockedReadHashCache(pins) as scope:
            sync=helpers.sync;previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous)
            assert not sync.git('status','--porcelain')
            prefix=Path('validation_sync/actual_BF16wide135_receiver_preflight_20261008');targets={};bindings={}
            for source in sources:
                data=source.read_bytes();assert not sync.SECRET.search(data),source
                target=(prefix/source.relative_to(ROOT)).as_posix();targets[target]=data
                bindings[source.relative_to(ROOT).as_posix()]={'published_path':target,'raw_sha256':hashlib.sha256(data).hexdigest()}
            targets[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
            targets[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'actual24_prospective_receivers_passed_and7_lazy_downstream_jobs_dispatched',
                'at_local':sync.now(),'round':135,'files':bindings,'actual_graph_controls':len(proof['graph_controls']),
                'actual_baseline_controls':len(proof['baseline_gain_regressions']),'actual_cross_volume_probe_bytes':proof['cross_volume_transfer_bytes'],
                'new_quality_scores':0,'full_annual_bank_GPU_controls_candidate_QA46_pending':True,'test_labels_read':False})
            for name,data in targets.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(targets)
            for left in range(0,len(names),50):sync.git('add','-f','--',*names[left:left+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','同步第135轮实际24项方案接收器检查与完整排队流程',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in targets.items()}
            assert helpers.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit)
            scope.reverify()
            create(out/'receipt.json',{'status':'pushed_and_remote_head_verified','at_local':sync.now(),'branch':'main','commit':commit,
                'raw_git_blobs_verified':len(hashes),'new_quality_scores':0,
                'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()})
            print('Actual24 receiver checks and lazy135 dispatch published to main: '+commit,flush=True)
    finally:
        for process in reversed(held):
            if process.is_running():process.resume()


if __name__=='__main__':main()
