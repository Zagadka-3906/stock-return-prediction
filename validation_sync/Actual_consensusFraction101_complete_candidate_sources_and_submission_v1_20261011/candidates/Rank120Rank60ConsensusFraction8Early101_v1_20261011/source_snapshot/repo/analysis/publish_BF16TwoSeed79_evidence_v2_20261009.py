"""Publish completed GPU/CDF/native controls and then official score evidence to main, with no large weights."""
from pathlib import Path
import argparse,gzip,hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from verified_TLS_Git_retry_runtime_v2_20261008 import installed
import publish_classifier_consensus_workflows_20261006 as helpers


def closed(name):
    folder=A/'service_owned_workflows_20261006'/name
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(15)
    assert read(folder/'service_execution.json')['status']=='passed',name
    return folder


def main(phase):
    assert phase in ('controls','scores')
    closed('BF16Medium78_round153_full_registration_v4_20261009')
    closed('BF16TwoSeed79_round154_source_admission_v1_20261009')
    if phase=='scores':closed('BF16TwoSeed79_controls_main_publication_v1_20261009')
    science=closed('BF16TwoSeed154_actual_full73_training_v1_20261009' if phase=='controls' else 'BF16TwoSeed79_official_comparison_v1_20261009')
    from prepare_BF16TwoSeed79_round154_sources_v1_20261009 import source_paths
    sources=[Path(__file__),*[p for p in source_paths() if p.is_file()]]
    index=read(A/'BF16TwoSeed79_actual_controls_index_v1_20261009.json')
    assert index['status']=='passed_actual12_two_seed154_states42_native73_full219_cold_controls'
    for path,digest in index['input_sha256'].items():assert sha(path)==digest,path
    sources += [Path(path) for path in index['original_external_metadata']]
    for pointer in ('actual_BF16TwoSeed154_full73_training_location_v1_20261009.json','actual_BF16TwoSeed154_native42_calendar_location_v1_20261009.json','actual_BF16TwoSeed154_prior_complete_forecast_duplicate_audit_v1_20261009.json'):
        folder=Path(read(A/pointer)['output']);sources += list(folder.glob('*.json'))
    sources += list(science.glob('*.json'))+list(science.glob('*.log'))
    best=None
    if phase=='scores':
        folder=A/'BF16TwoSeed79_official_comparison_v1_20261009';proof=read(folder/'verification.json')
        assert proof['status']=='passed_actual79_BF16_two_seed09_seed10_equal_mean_complete_parent_rank_CDF_full_official_comparisons' and len(proof['records'])==79
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
    out=A/f'BF16TwoSeed79_{phase}_github_v1_20261009';assert not out.exists();out.mkdir()
    create(out/'frozen_before_main_publication.json',{'input_sha256':pins,'phase':phase,'new_native_fits':0,
        'actual_score_records':79 if phase=='scores' else 0,'full154_qualification_pending':True,'test_labels_read':False})
    from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
    held=[]
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v10_20261009/native_launch.json')
        parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        create(out/'actual_idle_main_hold.json',idle)
        from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
        with installed(out/'file_backed_git'),LockedReadHashCache(pins) as scope:
            sync=helpers.sync;previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous)
            assert not sync.git('status','--porcelain')
            prefix=Path('validation_sync')/f'BF16TwoSeed79_{phase}_20261009';targets={};bindings={}
            for source in sources:
                data=source.read_bytes();assert not sync.SECRET.search(data),source
                raw_sha=hashlib.sha256(data).hexdigest();raw_size=len(data)
                relative=source.relative_to(ROOT) if source.is_relative_to(ROOT) else Path('external_metadata')/(raw_sha+'_'+source.name)
                target=(prefix/relative).as_posix()
                if len(data)>=5*1024**2:data=gzip.compress(data,mtime=0);target+='.gz';assert hashlib.sha256(gzip.decompress(data)).hexdigest()==raw_sha
                targets[target]=data;bindings[str(source)]={'published_path':target,'raw_sha256':raw_sha,'original_bytes':raw_size}
            targets[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
            targets[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'actual_completed_medium153_controls_or_scores_before_full154_qualification',
                'phase':phase,'at_local':sync.now(),'round':154,'files':bindings,'actual_existing_native_head_audits':12,
                'actual_full_native_OOF_heads':2,'actual_full_CDF_controls':73,'actual_cold_CDF_controls':219,'actual_historical_native_hooks':30,'actual_final_calendar_native_hooks':12,'actual_cold_native_hooks':42,
                'actual_score_records':79 if phase=='scores' else 0,'actual_best':best,'new_quality_scores_by_publication':0,
                'future_candidate_and_QA65_and_round154_main_receipt_pending':True,'test_labels_read':False})
            for name,data in targets.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(targets)
            for left in range(0,len(names),50):sync.git('add','-f','--',*names[left:left+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','同步第154轮中型神经排序融合实际证据 '+phase,timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in targets.items()}
            assert helpers.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit)
            scope.reverify()
            create(out/'receipt.json',{'status':'pushed_and_remote_head_verified','at_local':sync.now(),'phase':phase,'branch':'main',
                'commit':commit,'raw_git_blobs_verified':len(hashes),'official_score_records':79 if phase=='scores' else 0,
                'new_quality_scores_by_publication':0,'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()})
    finally:
        for process in reversed(held):
            if process.is_running():process.resume()


if __name__=='__main__':
    import os
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=('controls','scores'));phase=parser.parse_args().phase
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for offset,(key,value) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):
        os.environ[f'GIT_CONFIG_KEY_{count+offset}']=key;os.environ[f'GIT_CONFIG_VALUE_{count+offset}']=value
    os.environ['GIT_CONFIG_COUNT']=str(count+2)
    from lossless_chunked_safe_main_runtime_v1_20261009 import installed as safe
    from serial_main_publication_mutex_v1_20261009 import installed as serial
    log=Path('E:/赛题五_本机临时/第154轮_20261009')/('safe_'+phase+'_main_v2')
    with safe(log),serial(log/'serial_mutex.json'):main(phase)
