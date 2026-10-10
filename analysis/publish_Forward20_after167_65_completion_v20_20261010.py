"""Publish frozen priority changes or all completed screen records to main under the shared mutex."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import sys,os,time,gzip,hashlib,argparse
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def allowed():
    c=read(A/'current_user_runtime_control_20261010.json');read(A/'current_user_runtime_control_20261009.json')
    return c['status']=='optimization_active_after_explicit_manual_resume' and datetime.now(timezone(timedelta(hours=8)))<datetime.fromisoformat(c['stop_at_local'])

def main(phase):
    assert allowed()
    screen=Path('E:/赛题五_本机临时')/({'temporal73':'causal_neural_smoothing73_screen_v1_20261010','protected':'protected_official_top_screen_v2_20261010','valid':'protected_upper_tail_screen_v1_20261010','huber65':'Forward20_after167_high_impact65_screen_v1_20261010','quant37':'protected_quantization37_screen_v1_20261010','budget37':'budgeted_neural_Top37_screen_v1_20261010'}.get(phase,'high_impact_cumulative_screen_v2_20261010'))
    sources=[Path(__file__),A/'run_Forward20_after167_high_impact65_screen_v1_20261010.py',A/'prepare_forward20_and_return65_v1_20261010.py',A/'latest_verified_submission_delivery_v2_20261008.json',A/'github_validation_sync_main_20261005/round167_receipt.json',A/'Forward20_after167_synergy65_source_admission_v1_20261010.json',Path('E:/赛题五_本机临时/Forward20_after163_high_impact65_screen_v1_20261010/verification.json'),A/'high_impact_priority_huber65_main_receipt_v18_20261010.json',A/'qualified_Return167_prior_screen_csv_cleanup_v1_20261010/verification.json',A/'cleanup_qualified_Return167_prior_screen_csv_v1_20261010.py']
    if phase in ('scores','protected','valid','huber65','quant37','budget37','temporal73'):
        folder=A/'service_owned_workflows_20261006'/({'temporal73':'actual_causal_neural_smoothing73_screen_v1_20261010','protected':'actual_protected_official_top_screen_v2_20261010','valid':'actual_protected_upper_tail_screen_v1_20261010','huber65':'actual_Forward20_after167_high_impact65_screen_v1_20261010','quant37':'actual_protected_quantization37_screen_v1_20261010','budget37':'actual_budgeted_neural_Top37_screen_v1_20261010'}.get(phase,'actual_high_impact_cumulative_screen_v2_20261010'))
        while not (folder/'service_execution.json').is_file() or owned(read(folder/'native_launch.json')):
            assert allowed();time.sleep(15)
        assert read(folder/'service_execution.json')['status']=='passed'
        proof=read(screen/'verification.json');expected=73 if phase=='temporal73' else 65 if phase=='huber65' else 37 if phase in ('protected','valid','quant37','budget37') else 97
        assert proof['new_quality_score_records']==expected and len(proof['records'])==expected
        assert proof['actual_nonidentity_full_controls']==expected-1 and proof['actual_nonidentity_prefix_controls']==3*(expected-1)
        sources.extend(screen.glob('*.json'))
        if phase!='valid':sources.append(A/('actual_causal_neural_smoothing73_screen_location_v1_20261010.json' if phase=='temporal73' else 'actual_budgeted_neural_Top37_screen_location_v1_20261010.json' if phase=='budget37' else 'actual_protected_quantization37_screen_location_v1_20261010.json' if phase=='quant37' else 'actual_Forward20_after167_high_impact65_screen_location_v1_20261010.json' if phase=='huber65' else 'actual_protected_official_top_screen_location_v2_20261010.json' if phase=='protected' else 'actual_high_impact_cumulative_screen_location_v2_20261010.json'))
        sources.extend(folder/n for n in ('service_execution.json','native_launch.json','job_definition.json'))
        for row in proof['records']:
            p=Path(row['official_score_cache']['official_metrics_source']);assert sha(p)==row['official_metric_capsule_sha256'];sources.append(p)
    else:proof=None
    assert allowed()
    import publish_classifier_consensus_workflows_20261006 as h
    from owned_idle_publication_wait_runtime_v1_20261010 import hold as suspended_idle
    from lossless_chunked_safe_main_runtime_v1_20261009 import installed as safe
    from serial_main_publication_mutex_v1_20261009 import installed as serial
    from verified_TLS_Git_retry_runtime_v3_20261010 import installed as git_io
    out=Path('E:/赛题五_本机临时')/('high_impact_priority_'+phase+'_main_v20_20261010');out.mkdir(exist_ok=False)
    prefix=Path('validation_sync')/('high_impact_priority_'+phase+'_v20_20261010')
    payload={};bindings={}
    for p in dict.fromkeys(sources):
        raw=p.read_bytes();assert not h.sync.SECRET.search(raw),p;digest=hashlib.sha256(raw).hexdigest()
        target=(prefix/(p.relative_to(ROOT) if p.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+p.name))).as_posix()
        blob=raw
        if len(blob)>=5*1024**2:blob=gzip.compress(blob,mtime=0);target+='.gz';assert gzip.decompress(blob)==raw
        assert len(blob)<95*1024**2;payload[target]=blob;bindings[str(p)]={'published_path':target,'raw_sha256':digest}
    payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({'status':'frozen_priority_preparation' if proof is None else 'completed_training_only_official_screen_not_submission_qualified',
        'phase':phase,'files':bindings,'screen_records':0 if proof is None else len(proof['records']),'screen_full_and_prefix_checks':[0,0] if proof is None else [proof['actual_nonidentity_full_controls'],proof['actual_nonidentity_prefix_controls']],
        'best_screen':None if proof is None else proof['best'],'submission_qualified':False,'complete_ranking_registration_still_required_for_new_screen_scheme':True,
        'test_labels_read':False,'new_native_fits_by_publication':0,'deadline_local':read(A/'current_user_runtime_control_20261010.json')['stop_at_local']})
    create(out/'frozen_before_publication.json',{'files':bindings,'phase':phase})
    with serial(out/'serial_mutex.json') as mutex,safe(out/'safe'),git_io(out/'file_backed_git'):
        mutex.acquire();assert allowed()
        launch=read(A/'service_owned_workflows_20261006/main_publisher_v11_20261010/native_launch.json')
        parent,worker,idle=suspended_idle(launch,'    main (watch_validations_main_v7_20261006.py:71)')
        try:
            sync=h.sync;previous=sync.git('rev-parse','HEAD');h.verify_main(previous);assert not sync.git('status','--porcelain')
            for name,data in payload.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(payload)
            for i in range(0,len(names),50):sync.git('add','-f','--',*names[i:i+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','发布20日平均收益率网络在当前最佳完整167方案之后65项实际组合控制和官方评分 '+phase,timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()};assert h.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);h.verify_main(commit);h.watcher.advance_source_index(commit)
            value={'status':'pushed_and_remote_head_verified','phase':phase,'commit':commit,'branch':'main','raw_git_blobs_verified':len(hashes),
                'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix(),'submission_qualified':False}
            create(out/'receipt.json',value);create(A/('high_impact_priority_'+phase+'_main_receipt_v20_20261010.json'),value);print(value,flush=True)
        finally:
            for p in (parent,worker):
                if p.is_running():p.resume()

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=['preparation','scores','protected','valid','huber65','quant37','budget37','temporal73']);args=parser.parse_args()
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(k,v) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=k;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=v
    os.environ['GIT_CONFIG_COUNT']=str(count+2);main(args.phase)
