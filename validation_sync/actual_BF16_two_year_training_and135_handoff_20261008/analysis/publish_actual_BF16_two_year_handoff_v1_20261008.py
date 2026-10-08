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
    closed=A/'service_owned_workflows_20261006/actual_BF16wide135_receiver_preflight_main_publication_v1_20261008'
    assert read(closed/'service_execution.json')['status']=='passed'
    bank=Path('E:/赛题五_本机临时/neural_BF16_micro8192_bank6_v2_20261008')
    sources += [A/'actual_optimization_handoff_v2_20261008.json',A/'record_actual_optimization_handoff_v2_20261008.py',
        A/'monitor_BF16wide135_progress_v1_20261008.py',A/'actual_BF16wide135_live_progress_monitor_launch_v1_20261008.json',
        A/'actual_BF16wide135_receiver_preflight_main_v1_20261008/receipt.json',
        A/'prepare_actual_BF16_two_year_handoff_publisher_v1_20261008.py',bank/'protocol.json',
        *[bank/str(year)/name for year in (2020,2021) for name in ('info.json','frozen_training_inputs.json')]]
    weight_pins={}
    for year in (2020,2021):
        info=read(bank/str(year)/'info.json');model=bank/str(year)/'model.joblib'
        assert info['status']=='passed_actual_complete_mature_BF16_micro_annual_model'
        assert info['actual_full_annual_reload_prediction_bits_exact'] and info['actual_cold80_prefix_bits_exact']
        assert sha(model)==info['model_sha256'];weight_pins[str(model)]=info['model_sha256']
    sources=list(dict.fromkeys(sources));pins={**weight_pins,**{str(p):sha(p) for p in sources}}
    out=A/'actual_BF16_two_year_handoff_main_v1_20261008';assert not out.exists();out.mkdir()
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
            prefix=Path('validation_sync/actual_BF16_two_year_training_and135_handoff_20261008');targets={};bindings={}
            for source in sources:
                data=source.read_bytes();assert not sync.SECRET.search(data),source
                relative=source.relative_to(ROOT) if source.is_relative_to(ROOT) else Path('external_metadata')/(hashlib.sha256(data).hexdigest()+'_'+source.name)
                target=(prefix/relative).as_posix();targets[target]=data
                bindings[str(source)]={'published_path':target,'raw_sha256':hashlib.sha256(data).hexdigest()}
            targets[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
            targets[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'actual24_prospective_receivers_passed_and7_lazy_downstream_jobs_dispatched',
                'at_local':sync.now(),'round':135,'files':bindings,'actual_graph_controls':len(proof['graph_controls']),
                'actual_baseline_controls':len(proof['baseline_gain_regressions']),'actual_cross_volume_probe_bytes':proof['cross_volume_transfer_bytes'],'actual_completed_annual_years':[2020,2021],'completed_model_sha256':weight_pins,'remaining_full_bank_and_quality_pending':True,
                'new_quality_scores':0,'full_annual_bank_GPU_controls_candidate_QA46_pending':True,'test_labels_read':False})
            for name,data in targets.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(targets)
            for left in range(0,len(names),50):sync.git('add','-f','--',*names[left:left+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','同步实际BF16前两年度训练验证与第135轮完整流程交接',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in targets.items()}
            assert helpers.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit)
            scope.reverify()
            create(out/'receipt.json',{'status':'pushed_and_remote_head_verified','at_local':sync.now(),'branch':'main','commit':commit,
                'raw_git_blobs_verified':len(hashes),'new_quality_scores':0,
                'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()})
            print('Actual two complete annual models and full135 handoff published to main: '+commit,flush=True)
    finally:
        for process in reversed(held):
            if process.is_running():process.resume()


if __name__=='__main__':main()
