"""Publish completed native and historical checks to main; no round136 score/admission claim."""
from pathlib import Path
import gzip,hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
from file_backed_hidden_git_runtime_20261007 import installed
import publish_classifier_consensus_workflows_20261006 as helpers


def closed(name):
    folder=A/'service_owned_workflows_20261006'/name
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(10)
    assert read(folder/'service_execution.json')['status']=='passed',name
    return folder


def publish(phase):
    bank=closed('CrossFamily30_native_and90_synthetic_controls_v1_20261008')
    audit=Path(read(A/'actual_CrossFamily_bank30_synthetic_location_v1_20261008.json')['output'])
    proof=read(audit/'verification.json')
    assert proof['actual_model_count']==30 and proof['actual_full_OOF_heads']==6 and proof['synthetic_case_count']==90
    plan_path=A/'CrossFamily94_round136_plan_v1_20261008.json';plan=read(plan_path)
    sources=[Path(__file__),plan_path,A/'freeze_CrossFamily94_plan_v1_20261008.py',
        A/'CrossFamily_complete_parent_CDF_v1_20261008.py',A/'CrossFamily_complete_parent_native_stage_v1_20261008.py',
        A/'verify_CrossFamily_bank30_and_synthetic_v1_20261008.py',A/'verify_CrossFamily91_parent134_historical_v1_20261008.py',
        A/'verify_CrossFamily15_native_historical_hooks_v1_20261008.py',A/'actual_CrossFamily30_controls_hidden_launch_v1_20261008.json',
        A/'actual_CrossFamily91_parent134_hidden_launch_v1_20261008.json',A/'actual_CrossFamily15_native_hooks_hidden_launch_v1_20261008.json',
        A/'actual_CrossFamily_bank30_synthetic_location_v1_20261008.json',A/'github_validation_sync_main_20261005/round134_receipt.json',
        *audit.glob('*.json'),*bank.glob('*.json'),*bank.glob('*.log')]
    for row in plan['heads'].values():
        folder=Path(row['folder']);sources += list(folder.glob('*.json'))+[folder.parent/'verification.json']
    actual_full=actual_cold=actual_hooks=0
    if phase=='historical':
        science=closed('CrossFamily15_native_historical_hooks_v1_20261008')
        full_service=closed('CrossFamily91_parent134_historical_full_controls_v1_20261008')
        for pointer in ('actual_CrossFamily91_parent134_location_v1_20261008.json','actual_CrossFamily15_native_hooks_location_v1_20261008.json'):
            path=A/pointer;sources.append(path);sources += list(Path(read(path)['output']).glob('*.json'))
        full=read(Path(read(A/'actual_CrossFamily91_parent134_location_v1_20261008.json')['output'])/'verification.json')
        hooks=read(Path(read(A/'actual_CrossFamily15_native_hooks_location_v1_20261008.json')['output'])/'verification.json')
        actual_full=full['actual_full_cases'];actual_cold=full['actual_cold_cases'];actual_hooks=hooks['actual_hooks']
        assert (actual_full,actual_cold,actual_hooks)==(91,273,15)
        sources += list(science.glob('*.json'))+list(science.glob('*.log'))+list(full_service.glob('*.json'))+list(full_service.glob('*.log'))
    sources=list(dict.fromkeys(sources));assert all(p.suffix in ('.py','.json','.log') for p in sources)
    pins={str(p):sha(p) for p in sources};out=A/'CrossFamily_preliminary_controls_main_v1_20261008'/phase
    assert not out.exists();out.mkdir(parents=True)
    create(out/'frozen_before_main_publication.json',{'input_sha256':pins,'phase':phase,'actual_quality_scores':0,
        'round136_final_parent_source_admission_quality_candidate_and_full_QA_not_claimed':True})
    held=[]
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v8_20261008/native_launch.json')
        parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        create(out/'actual_idle_main_hold.json',idle)
        from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
        with installed(out/'file_backed_git'),LockedReadHashCache(pins) as scope:
            sync=helpers.sync;helpers.verify_main(sync.git('rev-parse','HEAD'));assert not sync.git('status','--porcelain')
            prefix=Path('validation_sync')/f'CrossFamily_preliminary_{phase}_20261008';targets={};bindings={}
            for source in sources:
                data=source.read_bytes();assert not sync.SECRET.search(data),source
                digest=hashlib.sha256(data).hexdigest();size=len(data)
                relative=source.relative_to(ROOT) if source.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+source.name)
                target=(prefix/relative).as_posix()
                if size>=5*1024**2:
                    data=gzip.compress(data,mtime=0);target+='.gz';assert hashlib.sha256(gzip.decompress(data)).hexdigest()==digest
                targets[target]=data;bindings[str(source)]={'published_path':target,'raw_sha256':digest,'original_bytes':size}
            targets[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
            targets[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'actual_passed_preliminary_crossfamily_controls_before136_quality',
                'at_local':sync.now(),'phase':phase,'files':bindings,'actual_native_model_audits':30,'actual_full_OOF_heads':6,
                'synthetic_CDF_cases':90,'synthetic_cold_controls':270,'actual_historical_parent':134 if phase=='historical' else None,
                'actual_full_historical_CDF_cases':actual_full,'actual_historical_cold_CDF_cases':actual_cold,'actual_native_historical_hooks':actual_hooks,
                'new_native_fits':0,'actual_quality_scores':0,'planned_scored_cases':94,'final136_controls_still_required_after135_closes':True,
                'actual_future_X_and_labels_read':False,'global_optimization_exhaustion_not_claimed':True})
            for name,data in targets.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(targets)
            for left in range(0,len(names),50):sync.git('add','-f','--',*names[left:left+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','同步跨模型集成实际原生与历史复现检查 '+phase,timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in targets.items()}
            assert helpers.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit);scope.reverify()
            create(out/'receipt.json',{'status':'pushed_and_remote_head_verified','at_local':sync.now(),'phase':phase,'branch':'main',
                'commit':commit,'raw_git_blobs_verified':len(hashes),'actual_quality_scores':0,
                'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()})
            print('Actual cross-family '+phase+' controls published to main: '+commit,flush=True)
    finally:
        for process in reversed(held):
            if process.is_running():process.resume()


if __name__=='__main__':
    publish('bank');publish('historical')
