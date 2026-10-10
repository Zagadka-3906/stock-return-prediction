"""Publish actual historical/calendar controls and source preflights, never large model/data bytes."""
from pathlib import Path
import hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from file_backed_hidden_git_runtime_20261007 import installed
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
import publish_classifier_consensus_workflows_20261006 as helpers


def closed(name):
    folder=A/'service_owned_workflows_20261006'/name
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(10)
    assert read(folder/'service_execution.json')['status']=='passed',name


def main():
    for name in ('CrossFamily15_native_historical_hooks_v2_20261008','HuberIRLS64_18_native_historical_hooks_v3_20261008',
        'multiyear_residual_native_calendar_v1_20261008'):closed(name)
    pointers=['actual_CrossFamily15_native_hooks_location_v2_20261008.json','actual_HuberIRLS64_18_native_hooks_location_v3_20261008.json',
        'actual_multiyear_residual_calendar_location_v1_20261008.json']
    scientific=[Path(read(A/name)['output']) for name in pointers];proofs=[read(folder/'verification.json') for folder in scientific]
    assert proofs[0]['actual_hooks']==proofs[0]['actual_cold_hooks']==15
    assert proofs[1]['actual_hooks']==proofs[1]['actual_cold_hooks']==18
    assert proofs[2]['actual_calendar_cases']==33 and proofs[2]['actual_whole_day_controls']==66
    prospective=[A/'CrossFamily94_prospective_routes_v3_20261008.json',A/'Huber52_prospective_routes_v2_20261008.json']
    assert [len(read(p)['graph_controls']) for p in prospective]==[186,588]
    sources=[Path(__file__),A/'prepare_multiyear_residual_receivers_v1_20261008.py',A/'multiyear_residual_native_preparation_v1_20261008.json',
        A/'recover_multiyear_136137_queues_v1_20261008.py',A/'recover_multiyear_136137_queues_v2_20261008.py',
        A/'multiyear136137_queue_recovery_v1_20261008.json',A/'verify_multiyear_residual_native_calendar_v1_20261008.py',
        A/'start_multiyear_136137_recovered_queues_v1_20261008.py',A/'actual_multiyear136137_recovered_queue_launches_v1_20261008.json',
        A/'actual_multiyear_residual_controls_hidden_launches_v1_20261008.json',*[A/name for name in pointers],*prospective]
    from prepare_CrossFamily94_round136_sources_v3_20261008 import source_paths as cs
    from prepare_Huber52_round137_sources_v2_20261008 import source_paths as hs
    sources += [p for p in [*cs(),*hs()] if p.is_file()]
    recovery=read(A/'multiyear136137_queue_recovery_v1_20261008.json')
    sources += [Path(p) for p in recovery['generated_source_sha256']]
    for folder in scientific:sources += list(folder.glob('*.json'))
    for family,version in (('CrossFamily136',3),('Huber137',2)):
        paths=[A/f'{family}_complete_dependency_plan_v{version}_20261008.json',A/f'{family}_complete_hidden_launches_v{version}_20261008.json']
        sources += paths
        for name,row in read(paths[1])['launches'].items():
            assert row['actual_native_console_handle']==0 and owned(row),name
            folder=A/'service_owned_workflows_20261006'/name;sources += [folder/'job_definition.json',folder/'native_launch.json']
    for name in recovery['audited_retired_jobs']:
        folder=A/'service_owned_workflows_20261006'/name;sources += list(folder.glob('*.json'))+list(folder.glob('*.log'))
    sources=list(dict.fromkeys(sources));pins={str(p):sha(p) for p in sources}
    for proof in [*proofs,*[read(p) for p in prospective]]:
        for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    out=A/'multiyear136137_recovery_main_v1_20261008';assert not out.exists();out.mkdir()
    create(out/'frozen_before_main_publication.json',{'input_sha256':pins,'actual_historical_hooks':33,'actual_calendar_cases':33,
        'actual_calendar_day_controls':66,'actual_prospective_sources':48,'actual_parent_graph_controls':774,
        'new_official_scores':0,'new_fits':0,'actual_future_feature_X_and_Y_read':False})
    held=[]
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v8_20261008/native_launch.json')
        parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        create(out/'actual_idle_main_hold.json',idle)
        from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
        with installed(out/'file_backed_git'),LockedReadHashCache(pins) as scope:
            sync=helpers.sync;helpers.verify_main(sync.git('rev-parse','HEAD'));assert not sync.git('status','--porcelain')
            prefix=Path('validation_sync/multiyear136137_recovery_v1_20261008');targets={};bindings={}
            for source in sources:
                data=source.read_bytes();assert not sync.SECRET.search(data),source
                if source.is_relative_to(ROOT):relative=source.relative_to(ROOT)
                else:
                    assert source.is_relative_to(Path('E:/赛题五_本机临时')) and source.suffix=='.json'
                    relative=Path('external_E_metadata')/source.relative_to(Path('E:/赛题五_本机临时'))
                target=(prefix/relative).as_posix();assert target not in targets;targets[target]=data
                bindings[str(source)]={'published_path':target,'raw_sha256':hashlib.sha256(data).hexdigest()}
            targets[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
            targets[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'actual33_historical_hooks33_calendar_controls66_day_controls_and48_prospective_sources_passed',
                'at_local':sync.now(),'files':bindings,'actual_frozen_final_fit_year':2025,'actual_prediction_calendar_years':[2025,2026],
                'actual_parent_graph_controls':774,'new_fits':0,'new_official_scores':0,'actual_future_feature_X_and_Y_read':False,
                'calendar_controls_used_date_remapped_historical_X_only':True,'actual_future_candidate_qualification_still_required':True,
                'original_scientific_training_and_original_official_math_unchanged':True,'main_only':True})
            for name,data in targets.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(targets)
            for left in range(0,len(names),50):sync.git('add','-f','--',*names[left:left+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','修正136和137轮跨年推理准入并同步33历史、33跨年及774父图复核',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={name:hashlib.sha256(data).hexdigest() for name,data in targets.items()}
            assert helpers.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit);scope.reverify()
            create(out/'receipt.json',{'status':'pushed_and_remote_head_verified','at_local':sync.now(),'branch':'main','commit':commit,
                'raw_git_blobs_verified':len(hashes),'new_official_scores':0,
                'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()})
            print('Actual historical/calendar controls and both recovered queues published to main: '+commit,flush=True)
    finally:
        for process in reversed(held):
            if process.is_running():process.resume()


if __name__=='__main__':main()
