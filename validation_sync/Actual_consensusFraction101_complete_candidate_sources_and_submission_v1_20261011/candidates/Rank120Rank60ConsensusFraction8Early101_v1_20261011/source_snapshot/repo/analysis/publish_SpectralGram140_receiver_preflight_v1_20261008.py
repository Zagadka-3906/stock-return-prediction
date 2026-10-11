"""Publish actual140 preflight, exact recoveries, all eight receivers and handoff11 to main."""
from pathlib import Path
import gzip,hashlib,sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from file_backed_hidden_git_runtime_20261007 import installed
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
import publish_classifier_consensus_workflows_20261006 as helpers

def main():
    import prepare_SpectralGram52_round140_sources_v2_20261008 as generator
    routes=A/'SpectralGram52_prospective_routes_v2_20261008.json';proof=read(routes)
    assert proof['actual_prospective_sources']==24 and proof['actual_graph_controls']==882 and proof['actual_physical_model_count_controls']==8
    handoff=A/'actual_optimization_handoff_v11_20261008.json';assert read(handoff)['goal_active_not_paused_complete_or_blocked']
    sources=[Path(__file__),routes,handoff,A/'actual_optimization_handoff_v11_20261008.md',A/'record_actual_optimization_handoff_v11_20261008.py',
        A/'SpectralGram140_complete_dependency_plan_v3_20261008.json',A/'SpectralGram140_complete_hidden_launches_v4_20261008.json',
        A/'retire_SpectralGram140_idle_metadata_receivers_v1_20261008.py',A/'queue_SpectralGram140_truthful_dispatch_v3_20261008.py',
        A/'recover_SpectralGram140_registration_receiver_v4_20261008.py',A/'SpectralGram140_registration_admin_path_recovery_v4_20261008.json',
        A/'SpectralGram140_exact_idle_metadata_supersession_v1_20261008.json',A/'run_SpectralGram52_round140_full_registration_v3_20261008.py',
        A/'prepare_SpectralGram140_archive_and_observer_v1_20261008.py',A/'recover_optimization140_progress_observer_v9_20261008.py',
        A/'SpectralGram140_archive_and_observer_preparation_v2_20261008.json',A/'archive_SpectralGram140_completed_scoring_CSV_v1_20261008.py',
        A/'actual_SpectralGram140_completed_CSV_archivist_hidden_launch_v1_20261008.json',A/'monitor_actual_optimization135_to140_v8_20261008.py',
        A/'monitor_actual_optimization135_to140_v9_20261008.py',A/'actual_optimization135_to140_progress_hidden_launch_v9_20261008.json',
        *[p for p in generator.source_paths() if p.is_file()]]
    for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
    for name,row in read(A/'SpectralGram140_complete_hidden_launches_v4_20261008.json')['launches'].items():
        assert owned(row) and row['actual_native_console_handle']==0,name
        folder=A/'service_owned_workflows_20261006'/name;sources += [folder/'native_launch.json',folder/'job_definition.json']
    old_launches=A/'SpectralGram140_complete_hidden_launches_v1_20261008.json';sources.append(old_launches)
    for name,row in read(old_launches)['launches'].items():
        assert not owned(row);folder=A/'service_owned_workflows_20261006'/name
        sources += [folder/'native_launch.json',folder/'job_definition.json',folder/'administrative_metadata_supersession_v1_20261008.json']
    for name in ('SpectralGram52_round140_full_registration_v2_20261008','actual_optimization135_to140_live_progress_v8_20261008'):
        folder=A/'service_owned_workflows_20261006'/name
        sources += [folder/n for n in ('native_launch.json','job_definition.json','service_execution.json','stderr.log','stdout.log')]
    sources=list(dict.fromkeys(sources));assert all(p.is_file() and p.resolve().is_relative_to(ROOT) for p in sources)
    pins={str(p):sha(p) for p in sources};output=A/'SpectralGram140_receiver_preflight_main_v1_20261008';assert not output.exists();output.mkdir()
    create(output/'frozen_before_main_publication.json',{'input_sha256':pins,'actual_prospective_sources':24,
        'actual_complete_graph_controls':882,'actual_physical_SHA_count_controls':8,'new_official_scores':0,'test_labels_read':False})
    held=[]
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v8_20261008/native_launch.json')
        parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        create(output/'actual_idle_main_hold.json',idle)
        from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
        with installed(output/'file_backed_git'),LockedReadHashCache(pins) as scope:
            sync=helpers.sync;helpers.verify_main(sync.git('rev-parse','HEAD'));assert not sync.git('status','--porcelain')
            prefix=Path('validation_sync/SpectralGram140_receiver_preflight_v1_20261008');targets={};bindings={}
            for source in sources:
                data=source.read_bytes();assert not sync.SECRET.search(data),source
                digest=hashlib.sha256(data).hexdigest();target=(prefix/source.relative_to(ROOT)).as_posix();raw_size=len(data)
                if len(data)>=5*1024**2:data=gzip.compress(data,mtime=0);target+='.gz';assert hashlib.sha256(gzip.decompress(data)).hexdigest()==digest
                targets[target]=data;bindings[str(source)]={'published_path':target,'raw_sha256':digest,'original_bytes':raw_size}
            targets[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
            targets[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'passed_actual24_sources882_graphs_and_eight_owned140_queue_handoff11',
                'at_local':sync.now(),'round':140,'files':bindings,'expected_official_cases':52,'actual_prospective_sources':24,
                'actual_complete_graph_controls':882,'actual_baseline_controls':9,'actual_same_S_controls':6,'actual_physical_model_SHA_count_controls':8,
                'actual_preliminary_controls':read(handoff)['actual140_controls'],'receiver_versions':read(handoff)['actual140_launch_metadata'],
                'complete52_quality_candidate_QA51_main_still_required':True,'new_official_scores':0,'new_fits':0,'test_labels_read':False,
                'global_exhaustion_not_claimed':True,'main_only':True})
            for name,data in targets.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(targets)
            for left in range(0,len(names),50):sync.git('add','-f','--',*names[left:left+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','同步第140轮24接收器882父图与真实计数修复、八步骤完整队列及交接11',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={name:hashlib.sha256(data).hexdigest() for name,data in targets.items()}
            assert helpers.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit);scope.reverify()
            create(output/'receipt.json',{'status':'pushed_and_remote_head_verified','at_local':sync.now(),'branch':'main','commit':commit,
                'raw_git_blobs_verified':len(hashes),'new_official_scores':0,
                'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()})
            print('Actual140 receiver checks and full queue handoff11 published: '+commit,flush=True)
    finally:
        for process in reversed(held):
            if process.is_running():process.resume()

if __name__=='__main__':main()
