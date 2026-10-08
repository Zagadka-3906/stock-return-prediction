"""Publish completed native controls or full historical controls, preserving source bytes."""
from pathlib import Path
import argparse,gzip,hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from file_backed_hidden_git_runtime_20261007 import installed
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
import publish_classifier_consensus_workflows_20261006 as helpers


def closed(name):
    folder=A/'service_owned_workflows_20261006'/name
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(10)
    assert read(folder/'service_execution.json')['status']=='passed',name
    return folder


def main(phase):
    assert phase in ('native','historical')
    plan_path=A/'HuberCrossFamily112_round139_plan_v1_20261008.json';plan=read(plan_path)
    assert len(plan['heads'])==5 and len(plan['new_cases'])==108 and len(plan['window_controls'])==5
    for path,digest in plan['input_sha256'].items():assert sha(path)==digest,path
    names=['prepare_HuberCrossFamily112_plan_and_historical_controls_v1_20261008.py',
        'start_HuberCrossFamily112_historical_controls_v2_20261008.py','HuberCrossFamily112_initial_dispatch_failure_v1_20261008.json',
        'actual_HuberCrossFamily112_plan_and_historical_hidden_launches_v2_20261008.json',
        'HuberCrossFamily_complete_parent_CDF_v1_20261008.py','HuberCrossFamily_complete_parent_native_stage_v1_20261008.py',
        'predict_HuberCrossFamily_complete_parent_scheme_v1_20261008.py',
        'prepare_HuberCrossFamily139_native_preflight_v1_20261008.py','HuberCrossFamily139_native_receiver_preflight_v1_20261008.json',
        'start_HuberCrossFamily139_calendar_v2_20261008.py','HuberCrossFamily139_calendar_dispatch_failure_v1_20261008.json',
        'actual_HuberCrossFamily139_calendar_hidden_launch_v2_20261008.json',
        'verify_HuberCrossFamily_multiyear_native_calendar_v1_20261008.py',
        'verify_HuberCrossFamily109_parent134_historical_v1_20261008.py','verify_HuberCrossFamily18_native_historical_hooks_v1_20261008.py']
    sources=[Path(__file__),plan_path,*[A/name for name in names]]
    cases={'calendar':18,'calendar_day':36,'adapter':5,'shared_maturity_windows':5,'saved_native_models_rehashed':25,
        'full5635800_CDF':0,'cold_CDF':0,'historical_native_hooks':0,'historical_cold_hooks':0}
    folder=closed('HuberCrossFamily_multiyear_native_calendar_v1_20261008')
    sources += [p for p in folder.iterdir() if p.suffix in ('.json','.log')]
    pointer=A/'actual_HuberCrossFamily_multiyear_calendar_location_v1_20261008.json'
    out=Path(read(pointer)['output']);proof=read(out/'verification.json')
    assert proof['actual_calendar_cases']==18 and proof['actual_whole_day_controls']==36
    assert proof['actual_future_feature_X_and_Y_read'] is False
    sources += [pointer,*out.glob('*.json')]
    if phase=='historical':
        for name,pointer_name,kind in (
            ('HuberCrossFamily109_parent134_historical_controls_v1_20261008','actual_HuberCrossFamily109_parent134_location_v1_20261008.json','cdf'),
            ('HuberCrossFamily18_native_historical_hooks_v1_20261008','actual_HuberCrossFamily18_native_hooks_location_v1_20261008.json','hooks')):
            folder=closed(name);sources += [p for p in folder.iterdir() if p.suffix in ('.json','.log')]
            pointer=A/pointer_name;out=Path(read(pointer)['output']);proof=read(out/'verification.json')
            for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
            if kind=='cdf':
                assert proof['actual_full_cases']==109 and proof['actual_cold_cases']==327
                cases.update(full5635800_CDF=109,cold_CDF=327)
            else:
                assert proof['actual_hooks']==proof['actual_cold_hooks']==18
                cases.update(historical_native_hooks=18,historical_cold_hooks=18)
            sources += [pointer,*out.glob('*.json')]
    for row in plan['heads'].values():
        for path in row['infos'].values():
            path=Path(path);info=read(path);kind=row['state_kind']
            sources += [path,Path(info['independent_'+kind+'_state_path'])]
        sources.append(Path(row['folder'])/'oof_verification.json')
    sources=list(dict.fromkeys(sources));pins={str(p):sha(p) for p in sources}
    output=A/f'HuberCrossFamily139_preliminary_{phase}_main_v1_20261008';assert not output.exists();output.mkdir()
    create(output/'frozen_before_main_publication.json',{'input_sha256':pins,'actual_completed_controls':cases,
        'new_fits':0,'new_official_scores':0,'actual_future_X_and_Y_read':False,
        'full139_quality_freeze_candidate_QA50_and_main_still_required':True})
    held=[]
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v8_20261008/native_launch.json')
        parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        create(output/'actual_idle_main_hold.json',idle)
        from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
        with installed(output/'file_backed_git'),LockedReadHashCache(pins) as scope:
            sync=helpers.sync;helpers.verify_main(sync.git('rev-parse','HEAD'));assert not sync.git('status','--porcelain')
            prefix=Path('validation_sync')/f'HuberCrossFamily139_preliminary_{phase}_v1_20261008';targets={};bindings={}
            for source in sources:
                data=source.read_bytes();assert not sync.SECRET.search(data),source
                digest=hashlib.sha256(data).hexdigest();relative=source.relative_to(ROOT) if source.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+source.name)
                target=(prefix/relative).as_posix();raw_size=len(data)
                if len(data)>=5*1024**2:data=gzip.compress(data,mtime=0);target+='.gz';assert hashlib.sha256(gzip.decompress(data)).hexdigest()==digest
                targets[target]=data;bindings[str(source)]={'published_path':target,'raw_sha256':digest,'original_bytes':raw_size}
            targets[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
            targets[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'passed_completed_Huber_crossfamily_preliminary_controls_before_quality',
                'at_local':sync.now(),'phase':phase,'files':bindings,'actual_completed_controls':cases,'new_fits':0,'new_official_scores':0,
                'no_new_actual_future_inference_claimed':True,'full139_QA50_and_candidate_pending':True,'test_labels_read':False})
            for name,data in targets.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(targets)
            for left in range(0,len(names),50):sync.git('add','-f','--',*names[left:left+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','同步第139轮Huber跨模型已完成验证 '+phase,timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={name:hashlib.sha256(data).hexdigest() for name,data in targets.items()}
            assert helpers.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit);scope.reverify()
            create(output/'receipt.json',{'status':'pushed_and_remote_head_verified','at_local':sync.now(),'phase':phase,'branch':'main',
                'commit':commit,'raw_git_blobs_verified':len(hashes),'actual_completed_controls':cases,'new_official_scores':0,
                'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()})
            print('Completed139 '+phase+' controls published: '+commit,flush=True)
    finally:
        for process in reversed(held):
            if process.is_running():process.resume()


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=('native','historical'));main(parser.parse_args().phase)
