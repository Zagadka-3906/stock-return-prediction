"""Publish completed GPU/CDF/native controls and then official score evidence to main, with no large weights."""
from pathlib import Path
import argparse,gzip,hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
from file_backed_hidden_git_runtime_20261007 import installed
import publish_classifier_consensus_workflows_20261006 as helpers


def closed(name):
    folder=A/'service_owned_workflows_20261006'/name
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(15)
    assert read(folder/'service_execution.json')['status']=='passed',name
    return folder


def main(phase):
    assert phase in ('controls','scores')
    closed('ConeRidgeAlpha100_round144_source_admission_v3_20261008')
    assert_already_qualified_parents()
    if phase=='scores':closed('ConeRidgeAlpha100_controls_main_publication_v3_20261008')
    science=closed('ConeRidgeAlpha97_current_parent_controls_v2_20261008' if phase=='controls' else 'ConeRidgeAlpha100_official_comparison_v5_20261008')
    from prepare_ConeRidgeAlpha100_round144_sources_v4_20261008 import source_paths
    sources=[Path(__file__),*[p for p in source_paths() if p.is_file()]]
    index=read(A/'ConeRidgeAlpha100_actual_controls_index_v1_20261008.json')
    assert index['status']=='passed_actual40_heads97_current_CDF291cold48_historical_native_hooks'
    for path,digest in index['input_sha256'].items():assert sha(path)==digest,path
    sources += [Path(path) for path in index['original_external_metadata']]
    for pointer in ('actual_ConeRidgeAlpha97_current_parent_location_v1_20261008.json',
        'actual_ConeRidgeAlpha48_native_hooks_location_v1_20261008.json','actual_ConeRidgeAlpha_multiyear_calendar_location_v1_20261008.json'):
        folder=Path(read(A/pointer)['output']);sources += list(folder.glob('*.json'))
    sources += list(science.glob('*.json'))+list(science.glob('*.log'))
    best=None
    if phase=='scores':
        folder=A/'ConeRidgeAlpha100_official_comparison_v5_20261008';proof=read(folder/'verification.json')
        assert proof['status']=='passed_actual100_ConeRidge_complete_parent_full_official_comparisons' and len(proof['records'])==100
        sources += list(folder.glob('*.json'));best=proof['best']
        for row in proof['records']:
            capsule=Path(row['official_score_cache']['official_metrics_source'])
            assert sha(capsule)==row['official_metric_capsule_sha256'] and read(capsule)['metrics']==row['metrics']
            sources.append(capsule)
    sources=list(dict.fromkeys(sources))
    # Every score freeze is immutable. Mutable actual_stage.json is only an operational observer.
    sources=[p for p in sources if p.name!='actual_stage.json']
    assert all(p.suffix in ('.py','.json','.log') for p in sources)
    pins={str(p):sha(p) for p in sources}
    out=A/f'ConeRidgeAlpha100_{phase}_github_v1_20261008';assert not out.exists();out.mkdir()
    create(out/'frozen_before_main_publication.json',{'input_sha256':pins,'phase':phase,'new_native_fits':0,
        'actual_score_records':100 if phase=='scores' else 0,'full144_qualification_pending':True,'test_labels_read':False})
    held=[]
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v8_20261008/native_launch.json')
        parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        create(out/'actual_idle_main_hold.json',idle)
        from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
        with installed(out/'file_backed_git'),LockedReadHashCache(pins) as scope:
            sync=helpers.sync;previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous)
            assert not sync.git('status','--porcelain')
            prefix=Path('validation_sync')/f'ConeRidgeAlpha100_{phase}_20261008';targets={};bindings={}
            for source in sources:
                data=source.read_bytes();assert not sync.SECRET.search(data),source
                raw_sha=hashlib.sha256(data).hexdigest();raw_size=len(data)
                relative=source.relative_to(ROOT) if source.is_relative_to(ROOT) else Path('external_metadata')/(raw_sha+'_'+source.name)
                target=(prefix/relative).as_posix()
                if len(data)>=5*1024**2:data=gzip.compress(data,mtime=0);target+='.gz';assert hashlib.sha256(gzip.decompress(data)).hexdigest()==raw_sha
                targets[target]=data;bindings[str(source)]={'published_path':target,'raw_sha256':raw_sha,'original_bytes':raw_size}
            targets[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
            targets[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'actual_completed_CrossFamily_controls_or_scores_before_full144_qualification',
                'phase':phase,'at_local':sync.now(),'round':144,'files':bindings,'actual_existing_native_head_audits':40,
                'actual_full_native_OOF_heads':8,'actual_full_CDF_controls':97,'actual_cold_CDF_controls':291,'actual_historical_native_hooks':48,
                'actual_score_records':100 if phase=='scores' else 0,'actual_best':best,'new_quality_scores_by_publication':0,
                'future_candidate_and_QA55_and_round144_main_receipt_pending':True,'test_labels_read':False})
            for name,data in targets.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(targets)
            for left in range(0,len(names),50):sync.git('add','-f','--',*names[left:left+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','同步第144轮跨模型集成实际证据 '+phase,timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in targets.items()}
            assert helpers.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit)
            scope.reverify()
            create(out/'receipt.json',{'status':'pushed_and_remote_head_verified','at_local':sync.now(),'phase':phase,'branch':'main',
                'commit':commit,'raw_git_blobs_verified':len(hashes),'official_score_records':100 if phase=='scores' else 0,
                'new_quality_scores_by_publication':0,'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()})
    finally:
        for process in reversed(held):
            if process.is_running():process.resume()



def assert_already_qualified_parents():
    for number in (132,134,143):
        assert read(A/f'optimization_20261003_r{number}/full_registration_execution.json')['status']=='passed'
        assert read(A/f'github_validation_sync_main_20261005/round{number}_receipt.json')['status']=='pushed_and_remote_head_verified'

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=('controls','scores'));main(parser.parse_args().phase)
