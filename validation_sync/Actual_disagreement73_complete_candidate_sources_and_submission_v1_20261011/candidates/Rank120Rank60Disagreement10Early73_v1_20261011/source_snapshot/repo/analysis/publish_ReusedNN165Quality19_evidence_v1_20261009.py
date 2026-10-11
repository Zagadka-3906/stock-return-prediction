"""Publish every actual165 control/score artifact to main, without weights or training data."""
from pathlib import Path
import argparse,gzip,hashlib,sys,os,time
A=Path(__file__).resolve().parent;ROOT=A.parent
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from verify_ReusedNN165Quality19_round165_sources_v1_20261010 import closed

def main(phase):
    closed('ReusedNN165Quality19_round165_source_admission_v1_20261009')
    if phase=='scores':closed('ReusedNN165Quality19_official_comparison_v3_20261009')
    from prepare_ReusedNN165Quality19_round165_sources_v1_20261009 import source_paths
    sources=[Path(__file__),*[p for p in source_paths() if p.is_file() and p.suffix in ('.py','.json')]]
    index=A/'ReusedNN165Quality19_actual_controls_index_v1_20261009.json';proof=read(index)
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    sources.extend(Path(p) for p in proof['original_external_metadata'])
    for pointer in ('actual_ReusedNN165Full17_full_training_location_v1_20261009.json','actual_ReusedNN165Stage_native14_calendar_location_v1_20261009.json'):
        sources.extend(Path(read(A/pointer)['output']).glob('*.json'))
    if phase=='scores':
        folder=A/'ReusedNN165Quality19_official_comparison_v1_20261009';pilot=read(folder/'verification.json');assert len(pilot['records'])==19
        sources.extend(folder.glob('*.json'))
        for row in pilot['records']:
            capsule=Path(row['official_score_cache']['official_metrics_source']);assert sha(capsule)==row['official_metric_capsule_sha256'];sources.append(capsule)
    sources=[p for p in dict.fromkeys(sources) if p.name!='actual_stage.json']
    import publish_classifier_consensus_workflows_20261006 as helpers
    from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
    from lossless_chunked_safe_main_runtime_v1_20261009 import installed as safe
    from serial_main_publication_mutex_v1_20261009 import installed as serial
    from verified_TLS_Git_retry_runtime_v2_20261008 import installed as git_io
    log=Path('E:/赛题五_本机临时/第165轮_20261009')/('safe_'+phase+'_main_v1')
    with serial(log/'serial_mutex.json') as mutex,safe(log),git_io(log/'file_backed_git'):
        mutex.acquire()
        launch=read(A/'service_owned_workflows_20261006/main_publisher_v10_20261009/native_launch.json')
        parent,worker,idle=suspended_idle(launch,'    main (watch_validations_main_v7_20261006.py:71)')
        try:
            sync=helpers.sync;previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous);assert not sync.git('status','--porcelain')
            prefix=Path('validation_sync')/f'ReusedNN165Quality19_{phase}_20261010';payload={};bindings={}
            for p in sources:
                raw=p.read_bytes();assert not sync.SECRET.search(raw),p;digest=hashlib.sha256(raw).hexdigest()
                relative=p.relative_to(ROOT) if p.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+p.name)
                target=(prefix/relative).as_posix();data=raw
                if len(data)>=5*1024**2:data=gzip.compress(data,mtime=0);target+='.gz';assert gzip.decompress(data)==raw
                assert len(data)<95*1024**2;payload[target]=data;bindings[str(p)]={'published_path':target,'raw_sha256':digest}
            payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
            payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'actual165_controls_or_scores_published_before_full_qualification','phase':phase,'files':bindings,
                'actual_full_cases':17,'actual_cold_cases':51,'actual_native_cases':14,'actual_scored_records':19 if phase=='scores' else 0,
                'new_fits':0,'new_scores_by_publication':0,'test_labels_read':False})
            out=A/f'ReusedNN165Quality19_{phase}_github_v1_20261009';out.mkdir(exist_ok=False)
            create(out/'frozen_before_main_publication.json',{'files':bindings,'phase':phase})
            for name,data in payload.items():sync.atomic(sync.WORKTREE/name,data)
            targets=sorted(payload)
            for i in range(0,len(targets),50):sync.git('add','-f','--',*targets[i:i+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(targets)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','同步第165轮完整152涨停神经融合实际验证 '+phase,timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()};assert helpers.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit)
            create(out/'receipt.json',{'status':'pushed_and_remote_head_verified','branch':'main','commit':commit,'phase':phase,
                'official_score_records':19 if phase=='scores' else 0,'raw_git_blobs_verified':len(hashes),
                'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()})
        finally:
            for process in (parent,worker):
                if process.is_running():process.resume()

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=['controls','scores']);phase=parser.parse_args().phase
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(k,v) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=k;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=v
    os.environ['GIT_CONFIG_COUNT']=str(count+2);main(phase)
