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
    screen=Path('E:/赛题五_本机临时')/('protected_upper_tail_screen_v1_20261010' if phase=='protected' else 'high_impact_cumulative_screen_v2_20261010')
    sources=[Path(__file__),A/'prepare_high_impact_priority_v1_20261010.py',A/'build_reused_neural_frontier_v8_20261010.py',
        A/'run_continuous_fast_reused_frontiers_v11_20261010.py',A/'monitor_fast_optimization_v10_20261010.py',
        A/'run_high_impact_cumulative_screen_v1_20261010.py',A/'run_high_impact_cumulative_screen_v2_20261010.py',
        A/'high_impact_cumulative_screen_plan_v1_20261010.json',A/'high_impact_cumulative_screen_plan_v2_20261010.json',
        A/'high_impact_cumulative_screen_log_writer_recovery_v2_20261010.json']
    sources.extend(A/name for name in ('monitor_fast_optimization_v11_20261010.py','build_reused_neural_frontier_v9_20261010.py',
        'run_continuous_fast_reused_frontiers_v14_20261010.py','owned_idle_publication_wait_runtime_v1_20261010.py',
        'protected_upper_tail_rank_permutation_v1_20261010.py','protected_upper_tail_rank_permutation_controls_v1_20261010.json',
        'run_protected_upper_tail_screen_v1_20261010.py','protected_upper_tail_screen_plan_v1_20261010.json',
        'round159_reconcile_index_exact_restore_v1_20261010.json','round159_existing_main_reconciliation_v3_20261010.json',
        'finalize_round159_reconciled_main_v4_20261010.py','round159_actual_reconciliation_completion_v4_20261010.json',
        'github_validation_sync_main_20261005/round159_receipt.json','optimization_20261003_r159/full_registration_execution.json'))
    for subfolder in ('round159_transport_alias_and_controller_handoff_v14_20261010','high_impact_progress_observer_handoff_v11_20261010','v100_owned_idle_mutex_wait_recovery_v1_20261010'):
        sources.extend((A/subfolder).glob('*.json'))
    sources.extend((A/'high_impact_priority_handoff_v1_20261010').glob('*.json'))
    sources.extend((A/'high_impact_progress_observer_handoff_v10_20261010').glob('*.json'))
    sources.extend((A/'continuous_fast_reused_frontiers_v11_20261010').glob('frozen*.json'))
    original=A/'service_owned_workflows_20261006/actual_high_impact_cumulative_screen_v1_20261010'
    sources.extend(original/n for n in ('service_execution.json','stderr.log','native_launch.json','job_definition.json'))
    if phase in ('scores','protected'):
        folder=A/'service_owned_workflows_20261006'/('actual_protected_upper_tail_screen_v1_20261010' if phase=='protected' else 'actual_high_impact_cumulative_screen_v2_20261010')
        while not (folder/'service_execution.json').is_file() or owned(read(folder/'native_launch.json')):
            assert allowed();time.sleep(15)
        assert read(folder/'service_execution.json')['status']=='passed'
        proof=read(screen/'verification.json');expected=37 if phase=='protected' else 97
        assert proof['new_quality_score_records']==expected and len(proof['records'])==expected
        assert proof['actual_nonidentity_full_controls']==expected-1 and proof['actual_nonidentity_prefix_controls']==3*(expected-1)
        sources.extend(screen.glob('*.json'))
        sources.append(A/('actual_protected_upper_tail_screen_location_v1_20261010.json' if phase=='protected' else 'actual_high_impact_cumulative_screen_location_v2_20261010.json'))
        sources.extend(folder/n for n in ('service_execution.json','native_launch.json','job_definition.json'))
        for row in proof['records']:
            p=Path(row['official_score_cache']['official_metrics_source']);assert sha(p)==row['official_metric_capsule_sha256'];sources.append(p)
    else:proof=None
    assert allowed()
    import publish_classifier_consensus_workflows_20261006 as h
    from owned_idle_publication_wait_runtime_v1_20261010 import hold as suspended_idle
    from lossless_chunked_safe_main_runtime_v1_20261009 import installed as safe
    from serial_main_publication_mutex_v1_20261009 import installed as serial
    from verified_TLS_Git_retry_runtime_v2_20261008 import installed as git_io
    out=Path('E:/赛题五_本机临时')/('high_impact_priority_'+phase+'_main_v2_20261010');out.mkdir(exist_ok=False)
    prefix=Path('validation_sync')/('high_impact_priority_'+phase+'_v2_20261010')
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
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','优先验证更大提分方向：完整157之后96种互补融合与非涨停、大权重和新Huber训练计划 '+phase,timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()};assert h.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);h.verify_main(commit);h.watcher.advance_source_index(commit)
            value={'status':'pushed_and_remote_head_verified','phase':phase,'commit':commit,'branch':'main','raw_git_blobs_verified':len(hashes),
                'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix(),'submission_qualified':False}
            create(out/'receipt.json',value);create(A/('high_impact_priority_'+phase+'_main_receipt_v2_20261010.json'),value);print(value,flush=True)
        finally:
            for p in (parent,worker):
                if p.is_running():p.resume()

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=['preparation','scores','protected']);args=parser.parse_args()
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(k,v) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=k;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=v
    os.environ['GIT_CONFIG_COUNT']=str(count+2);main(args.phase)
