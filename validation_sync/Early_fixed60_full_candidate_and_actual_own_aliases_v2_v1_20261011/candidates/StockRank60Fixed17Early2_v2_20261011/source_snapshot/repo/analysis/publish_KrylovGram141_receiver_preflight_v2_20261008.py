"""Publish actual141 preflight, exact recoveries, all eight receivers and handoff15 to main."""
from pathlib import Path
import gzip,hashlib,sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from file_backed_hidden_git_runtime_20261007 import installed
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
import publish_classifier_consensus_workflows_20261006 as helpers

def main():
    import prepare_KrylovGram52_round141_sources_v3_20261008 as generator
    routes=A/'KrylovGram52_prospective_routes_v3_20261008.json';proof=read(routes)
    assert proof['actual_prospective_sources']==24 and proof['actual_graph_controls']==1029 and proof['actual_physical_model_count_controls']==8
    handoff=A/'actual_optimization_handoff_v15_20261008.json';assert read(handoff)['goal_active_not_paused_complete_or_blocked']
    sources=[Path(__file__),routes,handoff,A/'actual_optimization_handoff_v15_20261008.md',A/'record_actual_optimization_handoff_v15_20261008.py',
        A/'KrylovGram141_complete_dependency_plan_v3_20261008.json',A/'KrylovGram141_complete_hidden_launches_v3_20261008.json',
        A/'prepare_KrylovGram141_parent_set_recovery_v2_20261008.py',A/'KrylovGram141_parent_set_recovery_v2_20261008.json',
        A/'KrylovGram141_prospective_QA_literal_recovery_v2_20261008.json',A/'verify_KrylovGram52_prospective_routes_v1_20261008.py',
        A/'verify_KrylovGram52_prospective_routes_v3_20261008.py',A/'prepare_KrylovGram141_prospective_verifier_v1_20261008.py',
        A/'KrylovGram141_prospective_verifier_preparation_v1_20261008.json',A/'KrylovGram141_receiver_preparation_v3_20261008.json',
        A/'prepare_KrylovGram141_archive_and_observer_v1_20261008.py',A/'KrylovGram141_archive_and_observer_preparation_v1_20261008.json',
        A/'archive_KrylovGram141_completed_scoring_CSV_v1_20261008.py',A/'actual_KrylovGram141_completed_CSV_archivist_hidden_launch_v1_20261008.json',
        A/'monitor_actual_optimization135_to141_v10_20261008.py',A/'actual_optimization135_to141_progress_hidden_launch_v10_20261008.json',
        A/'create_KrylovGram141_output_junctions_native_v1_20261008.ps1',*[p for p in generator.source_paths() if p.is_file()]]
    for stem in ('run_KrylovGram52_official_comparison','prepare_KrylovGram52_selected_candidate','seal_KrylovGram52_selected_candidate',
        'run_KrylovGram52_round141_full_registration','publish_KrylovGram52_evidence','verify_KrylovGram52_round141_sources',
        'verify_KrylovGram49_current_parent','prepare_KrylovGram52_round141_sources'):
        sources.append(A/(stem+'_v1_20261008.py'))
    for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
    for name,row in read(A/'KrylovGram141_complete_hidden_launches_v3_20261008.json')['launches'].items():
        assert owned(row) and row['actual_native_console_handle']==0,name
        folder=A/'service_owned_workflows_20261006'/name;sources += [folder/'native_launch.json',folder/'job_definition.json']
    sources += [A/name for name in ('prepare_KrylovGram141_calendar_evidence_receivers_v3_20261008.py',
        'KrylovGram141_calendar_evidence_receiver_recovery_v3_20261008.json','retire_KrylovGram141_idle_calendar_receivers_v1_20261008.py',
        'KrylovGram141_exact_idle_metadata_supersession_v1_20261008.json','KrylovGram141_exact_idle_calendar_replacement_preparation_v1_20261008.json',
        'prepare_KrylovGram141_corrected_archive_and_observer_v2_20261008.py','KrylovGram141_corrected_archive_and_observer_hidden_launches_v2_20261008.json',
        'archive_KrylovGram141_completed_scoring_CSV_v2_20261008.py','monitor_actual_optimization135_to142_v12_20261008.py')]
    for service in read(A/'KrylovGram141_complete_hidden_launches_v2_20261008.json')['launches']:
        folder=A/'service_owned_workflows_20261006'/service
        sources += [folder/'administrative_metadata_supersession_v1_20261008.json']
    sources=list(dict.fromkeys(sources));assert all(p.is_file() and p.resolve().is_relative_to(ROOT) for p in sources)
    pins={str(p):sha(p) for p in sources};output=A/'KrylovGram141_receiver_preflight_main_v2_20261008';assert not output.exists();output.mkdir()
    create(output/'frozen_before_main_publication.json',{'input_sha256':pins,'actual_prospective_sources':24,
        'actual_complete_graph_controls':1029,'actual_physical_SHA_count_controls':8,'new_official_scores':0,'test_labels_read':False})
    held=[]
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v8_20261008/native_launch.json')
        parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        create(output/'actual_idle_main_hold.json',idle)
        from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
        with installed(output/'file_backed_git'),LockedReadHashCache(pins) as scope:
            sync=helpers.sync;helpers.verify_main(sync.git('rev-parse','HEAD'));assert not sync.git('status','--porcelain')
            prefix=Path('validation_sync/KrylovGram141_receiver_preflight_v2_20261008');targets={};bindings={}
            for source in sources:
                data=source.read_bytes();assert not sync.SECRET.search(data),source
                digest=hashlib.sha256(data).hexdigest();target=(prefix/source.relative_to(ROOT)).as_posix();raw_size=len(data)
                if len(data)>=5*1024**2:data=gzip.compress(data,mtime=0);target+='.gz';assert hashlib.sha256(gzip.decompress(data)).hexdigest()==digest
                targets[target]=data;bindings[str(source)]={'published_path':target,'raw_sha256':digest,'original_bytes':raw_size}
            targets[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
            targets[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'passed_actual24_sources1029_graphs_and_eight_owned140_queue_handoff15',
                'at_local':sync.now(),'round':141,'files':bindings,'expected_official_cases':52,'actual_prospective_sources':24,
                'actual_complete_graph_controls':1029,'actual_baseline_controls':9,'actual_same_S_controls':6,'actual_physical_model_SHA_count_controls':8,
                'actual_preliminary_controls':read(handoff)['actual141_controls'],'receiver_versions':read(handoff)['actual141_launch_metadata'],
                'complete52_quality_candidate_QA52_main_still_required':True,'new_official_scores':0,'new_fits':0,'test_labels_read':False,
                'global_exhaustion_not_claimed':True,'main_only':True})
            for name,data in targets.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(targets)
            for left in range(0,len(names),50):sync.git('add','-f','--',*names[left:left+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','同步第141轮24接收器1029父图与真实计数修复、八步骤完整队列及交接15',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={name:hashlib.sha256(data).hexdigest() for name,data in targets.items()}
            assert helpers.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit);scope.reverify()
            create(output/'receipt.json',{'status':'pushed_and_remote_head_verified','at_local':sync.now(),'branch':'main','commit':commit,
                'raw_git_blobs_verified':len(hashes),'new_official_scores':0,
                'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()})
            print('Actual140 receiver checks and full queue handoff15 published: '+commit,flush=True)
    finally:
        for process in reversed(held):
            if process.is_running():process.resume()

if __name__=='__main__':main()
