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
    screen=Path('E:/赛题五_本机临时')/({'protected':'protected_official_top_screen_v2_20261010','valid':'protected_upper_tail_screen_v1_20261010','huber65':'Huber010_high_impact65_screen_v1_20261010','quant37':'protected_quantization37_screen_v1_20261010','budget37':'budgeted_neural_Top37_screen_v1_20261010'}.get(phase,'high_impact_cumulative_screen_v2_20261010'))
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
    sources.extend(A/name for name in ('protected_official_top_rank_permutation_v2_20261010.py',
        'protected_official_top_rank_permutation_controls_v2_20261010.json','run_protected_official_top_screen_v2_20261010.py',
        'protected_official_top_screen_plan_v2_20261010.json','protected_official_top_screen_actual_hidden_queue_v2_20261010.json',
        'high_impact_positive_candidate_followthrough_v1_20261010.json'))
    positive=read(A/'high_impact_positive_candidate_followthrough_v1_20261010.json')
    for p,d in positive['input_sha256'].items():
        path=Path(p);assert sha(path)==d; sources.append(path)
    sources.extend(A/name for name in ('monitor_fast_optimization_v12_20261010.py',
        'train_Huber010_overlap_verified_reuse160_v1_20261010.py','Huber010_actual_idle_GPU_overlap160_v1_20261010.json',
        'Huber010_actual_idle_GPU_overlap160_hidden_launch_v1_20261010.json',
        'high_impact_positive_candidate_followthrough_v2_20261010.json','remaining_feasible_optimization_frontier_fast_v7_20261010.json',
        'actual_optimization_fast_runtime_handoff_v10_20261010.json'))
    current_positive=read(A/'high_impact_positive_candidate_followthrough_v2_20261010.json')
    for p,d in current_positive['input_sha256'].items():
        path=Path(p);assert sha(path)==d;sources.append(path)
    sources.extend((A/'high_impact_progress_observer_handoff_v12_20261010').glob('*.json'))
    sources.extend((A/'high_impact_priority_handoff_v1_20261010').glob('*.json'))
    sources.extend((A/'high_impact_progress_observer_handoff_v10_20261010').glob('*.json'))
    sources.extend((A/'continuous_fast_reused_frontiers_v11_20261010').glob('frozen*.json'))
    original=A/'service_owned_workflows_20261006/actual_high_impact_cumulative_screen_v1_20261010'
    sources.extend(original/n for n in ('service_execution.json','stderr.log','native_launch.json','job_definition.json'))
    from prepare_protected162_full_registry_sources_v1_20261010 import source_paths
    sources.extend(source_paths())
    sources.extend(A/n for n in ('monitor_fast_optimization_v13_20261010.py','run_continuous_fast_reused_frontiers_v15_20261010.py','prepare_priority_screen_location_recovery_v2_20261010.py','reconcile_completed_priority_screen_pointer_v1_20261010.py','reconcile_completed_priority_screen_pointer_v2_20261010.py'))
    sources.extend((A/'high_impact_protected162_priority_controller_handoff_v15_20261010').glob('*.json'))
    sources.extend((A/'protected162_progress_observer_handoff_v13_20261010').glob('*.json'))
    sources.extend((A/'service_owned_workflows_20261006/actual_high_impact_priority_protected_main_v2_20261010').glob('*.json'))
    sources.extend((A/'service_owned_workflows_20261006/actual_high_impact_cumulative_screen_v2_20261010_original_pointer_collision_evidence_v1_20261010').glob('*.json'))
    sources.extend((A/'service_owned_workflows_20261006/actual_high_impact_cumulative_screen_v2_20261010_location_reconciliation_v1_20261010').glob('*.json'))
    sources.extend(A/n for n in ('verify_protected162_full_family_preflight_v1_20261010.py','protected162_full_family_preflight_v1_20261010.json','TailProtected162_full76_ready_dispatch_v1_20261010.json','run_Huber010_high_impact65_screen_v1_20261010.py','Huber010_high_impact65_actual_hidden_queue_v1_20261010.json','high_impact_priority_preparation_main_receipt_v6_20261010.json','high_impact_priority_scores_main_receipt_v6_20261010.json','high_impact_priority_valid_main_receipt_v6_20261010.json'))
    sources.extend(A/n for n in ('protected_lower_rank_quantization_v1_20261010.py','protected_lower_rank_quantization_v2_20261010.py','protected_lower_rank_quantization_v3_20261010.py','verify_protected_lower_rank_quantization_v1_20261010.py','protected_lower_rank_quantization_controls_v1_20261010.json','prepare_fast_quantization_controls_v2_20261010.py','prepare_fast_quantization_controls_v3_20261010.py','run_fast_quantization_controls_v3_20261010.py','protected_lower_rank_quantization_controls_v3_20261010.json','run_protected_quantization37_screen_v1_20261010.py','protected_quantization37_actual_hidden_launch_v1_20261010.json','monitor_fast_optimization_v14_20261010.py','prepare_progress_observer14_Huber65_v1_20261010.py','save_high_impact_runtime_handoff_v11_20261010.py','actual_optimization_fast_runtime_handoff_v11_20261010.json','high_impact_priority_protected_main_receipt_v7_20261010.json','protected_official_top_screen_v2_20261010_location_reconciliation_v2_20261010.json'))
    sources.extend((A/'Huber65_progress_observer_handoff_v14_20261010').glob('*.json'))
    sources.extend(A/n for n in ('budgeted_neural_Top_projection37_proposal_v1_20261010.json','budgeted_neural_Top_projection_v1_20261010.py','verify_budgeted_neural_Top_projection_v1_20261010.py','budgeted_neural_Top_projection_controls_v1_20261010.json','run_budgeted_neural_Top37_screen_v1_20261010.py','budgeted_neural_Top37_actual_hidden_launch_v1_20261010.json','monitor_fast_optimization_v15_20261010.py','prepare_progress_observer15_quantization37_v1_20261010.py','save_high_impact_runtime_handoff_v12_20261010.py','actual_optimization_fast_runtime_handoff_v12_20261010.json'))
    sources.extend((A/'quantization37_progress_observer_handoff_v15_20261010').glob('*.json'))
    if phase in ('scores','protected','valid','huber65','quant37','budget37'):
        folder=A/'service_owned_workflows_20261006'/({'protected':'actual_protected_official_top_screen_v2_20261010','valid':'actual_protected_upper_tail_screen_v1_20261010','huber65':'actual_Huber010_high_impact65_screen_v1_20261010','quant37':'actual_protected_quantization37_screen_v1_20261010','budget37':'actual_budgeted_neural_Top37_screen_v1_20261010'}.get(phase,'actual_high_impact_cumulative_screen_v2_20261010'))
        while not (folder/'service_execution.json').is_file() or owned(read(folder/'native_launch.json')):
            assert allowed();time.sleep(15)
        assert read(folder/'service_execution.json')['status']=='passed'
        proof=read(screen/'verification.json');expected=65 if phase=='huber65' else 37 if phase in ('protected','valid','quant37','budget37') else 97
        assert proof['new_quality_score_records']==expected and len(proof['records'])==expected
        assert proof['actual_nonidentity_full_controls']==expected-1 and proof['actual_nonidentity_prefix_controls']==3*(expected-1)
        sources.extend(screen.glob('*.json'))
        if phase!='valid':sources.append(A/('actual_budgeted_neural_Top37_screen_location_v1_20261010.json' if phase=='budget37' else 'actual_protected_quantization37_screen_location_v1_20261010.json' if phase=='quant37' else 'actual_Huber010_high_impact65_screen_location_v1_20261010.json' if phase=='huber65' else 'actual_protected_official_top_screen_location_v2_20261010.json' if phase=='protected' else 'actual_high_impact_cumulative_screen_location_v2_20261010.json'))
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
    out=Path('E:/赛题五_本机临时')/('high_impact_priority_'+phase+'_main_v9_20261010');out.mkdir(exist_ok=False)
    prefix=Path('validation_sync')/('high_impact_priority_'+phase+'_v9_20261010')
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
            create(out/'receipt.json',value);create(A/('high_impact_priority_'+phase+'_main_receipt_v9_20261010.json'),value);print(value,flush=True)
        finally:
            for p in (parent,worker):
                if p.is_running():p.resume()

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=['preparation','scores','protected','valid','huber65','quant37','budget37']);args=parser.parse_args()
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(k,v) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=k;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=v
    os.environ['GIT_CONFIG_COUNT']=str(count+2);main(args.phase)
