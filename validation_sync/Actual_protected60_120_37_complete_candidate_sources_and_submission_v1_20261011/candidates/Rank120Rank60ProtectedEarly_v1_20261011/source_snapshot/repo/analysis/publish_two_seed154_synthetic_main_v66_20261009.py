"""Publish actual150 post-score repairs, prospective151-153 guards, and fixed two-seed154 declaration."""
from pathlib import Path
import sys,os,time,hashlib,gzip
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def main():
    gate=A/'service_owned_workflows_20261006/two_seed154_recovery_main_publication_v65_20261009'
    while not (gate/'native_launch.json').exists() or owned(read(gate/'native_launch.json')):time.sleep(15)
    assert read(gate/'service_execution.json')['status']=='passed'
    import publish_classifier_consensus_workflows_20261006 as helpers
    from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
    from verified_TLS_Git_retry_runtime_v2_20261008 import installed
    out=Path('E:/赛题五_本机临时/two_seed154_synthetic_main_v66_20261009');out.mkdir(exist_ok=False)
    sources=[Path(__file__),A/'lossless_chunked_safe_main_runtime_v1_20261009.py',A/'serial_main_publication_mutex_v1_20261009.py']
    names=['HuberSparse150_import_namespace_v23_20261009.json','future_import_namespaces_v24_20261009.json',
        'HuberSparse150_volume_transfer_v25_20261009.json','future_import_namespaces_v26_20261009.json',
        'HuberSparse150_materialization_v27_20261009.json','future_import_namespaces_v28_20261009.json',
        'HuberSparse150_partial_registry_v29_20261009.json','HuberSparse150_registry_attempt_v30_20261009.json',
        'future_import_namespaces_v31_20261009.json','external_registry_source_paths_runtime_v1_20261009.json',
        'neural_BF16_medium2048_seed10_e64_frontier_v1_20261009.json','BF16TwoSeed79_round154_proposal_v1_20261009.json',
        'BF16TwoSeed154_seed10_independent_controls_preparation_v1_20261009.json',
        'actual_recovered_progress_hidden_launch_v58_20261009.json','latest_actual_optimization_progress_pointer_v58_20261009.json',
        'actual_recovered_progress_handoff_v58_20261009.json','start_actual_recovered_progress_v58_20261009.py','monitor_actual_chronological_optimization_progress_v58_20261009.py']
    for n in names:
        p=A/n;assert p.is_file();sources.append(p)
        if p.suffix=='.json':
            for f,d in read(p).get('input_sha256',{}).items():
                assert sha(f)==d,f
                if Path(f).suffix in ('.py','.json','.log','.md'):sources.append(Path(f))
    for pattern in ('*HuberSparse150*hidden_launch*v2[3579]*20261009.json','*HuberSparse150*hidden_launch*v30*20261009.json',
        'future_import*hidden_launches*20261009.json','*seed10*20261009.json','*seed10*20261009.py','*TwoSeed*20261009.py','*TwoSeed*20261009.json'):
        sources.extend(p for p in A.glob(pattern) if p.is_file())
    for version in range(3,9):
        for stem in ('selected_candidate_preparation','selected_candidate_sealing','round150_full_registration'):
            folder=A/'service_owned_workflows_20261006'/f'HuberSparse59_{stem}_v{version}_20261009'
            if folder.is_dir():sources.extend(p for p in folder.iterdir() if p.suffix in ('.json','.log'))
    for label in ('RFFSparse151','SparseAfter148152','BF16Medium153'):
        for version in range(3,8):
            folder=A/'service_owned_workflows_20261006'/f'{label}_prior_complete_forecast_duplicate_audit_v{version}_20261009'
            if folder.is_dir():sources.extend(p for p in folder.iterdir() if p.suffix in ('.json','.log'))
        for version in (22,31):
            folder=A/'service_owned_workflows_20261006'/f'{label}_complete_chronological_dispatch_serial_v{version}_20261009'
            if folder.is_dir():sources.extend(p for p in folder.iterdir() if p.suffix in ('.json','.log'))
    for name in ('actual_BF16_medium2048_seed10_restart_control_v1_20261009','actual_BF16_medium2048_seed10_e64_bank6_v1_20261009',
        'BF16TwoSeed154_seed10_independent_small_CPU_v1_20261009','BF16TwoSeed154_seed10_independent_full5_GPU_controls_v1_20261009',
        'actual_chronological_optimization_progress_observer_v58_20261009'):
        folder=A/'service_owned_workflows_20261006'/name;sources.extend(p for p in folder.iterdir() if p.suffix in ('.json','.log'))
    for n in ('HuberSparse59_round150_source_preparation_v1_20261008.json','HuberSparse59_actual_source_paths_before_registration_20261008.json',
        'HuberSparse59_actual_source_paths_before_registration_retry30_20261009.json','HuberSparse59_official_comparison_v1_20261008/verification.json',
        'HuberSparse59_scores_github_v1_20261008/receipt.json'):
        sources.append(A/n)
    sources.extend((A/'HuberSparse59_selected_release_v1_20261008').glob('*.json'))
    control=Path('E:/赛题五_本机临时/GPU实测_20261009/BF16_medium2048_seed10_restart_v1')
    sources.extend(control.glob('*/verification.json'))
    bank=Path('E:/赛题五_本机临时/neural_BF16_medium2048_seed10_e64_bank6_v1_20261009')
    if (bank/'protocol.json').exists():sources.append(bank/'protocol.json')
    infos=sorted(bank.glob('*/info.json'));sources.extend(infos);sources.extend(bank.glob('*/frozen_training_inputs.json'))
    pilot=read(A/'HuberSparse59_official_comparison_v1_20261008/verification.json');assert len(pilot['records'])==59
    assert pilot['best']['connected_final_score']==.4511917507998099
    assert len(read(A/'external_registry_source_paths_runtime_v1_20261009.json')['records'])==13
    assert len(read(A/'future_import_namespaces_v31_20261009.json')['checks'])==24
    for n in ('BF16TwoSeed79_synthetic73_cold219_v1_20261009.json','BF16TwoSeed79_round154_math_plan_v1_20261009.json','BF16TwoSeed154_full73_controls_preparation_v1_20261009.json','BF16TwoSeed154_full73_hidden_launch_v1_20261009.json','verify_BF16TwoSeed154_equal_mean_full5_v1_20261009.py','verify_BF16TwoSeed154_full73_training_v1_20261009.py','prepare_BF16TwoSeed154_full73_controls_v1_20261009.py','BF16TwoSeed154_equal_mean_full5_hidden_launch_v1_20261009.json','actual_optimization_checkpoint_v54_20261009.json','two_seed154_recovery_main_v65_receipt_20261009.json'):
        sources.append(A/n)
    assert (read(A/'BF16TwoSeed79_synthetic73_cold219_v1_20261009.json')['actual_cases'],read(A/'BF16TwoSeed79_synthetic73_cold219_v1_20261009.json')['actual_cold_cases'])==(73,219)
    for name in ('BF16TwoSeed154_equal_mean_full5_controls_v1_20261009','BF16TwoSeed154_actual_full73_training_v1_20261009'):
        f=A/'service_owned_workflows_20261006'/name;sources.extend(p for p in f.iterdir() if p.suffix in ('.json','.log'))
    sources.extend(control.glob('*.json'));sources.extend(control.glob('*/*.json'))
    sources=list(dict.fromkeys(sources));assert all(p.is_file() for p in sources)
    held=[]
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v9_20261009/native_launch.json');assert owned(row)
        parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        create(out/'main_watcher_idle_hold.json',{'identity':row,'stack':idle,'scientific_workers_held':0})
        sync=helpers.sync;prefix=Path('validation_sync/two_seed154_synthetic_v66_20261009');payload={};bindings={}
        for source in sources:
            data=source.read_bytes();assert not sync.SECRET.search(data),source
            digest=hashlib.sha256(data).hexdigest();relative=source.relative_to(ROOT) if source.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+source.name)
            target=(prefix/relative).as_posix();size=len(data)
            if size>=5*1024**2:data=gzip.compress(data,mtime=0);target+='.gz';assert hashlib.sha256(gzip.decompress(data)).hexdigest()==digest
            assert len(data)<95*1024**2
            payload[target]=data;bindings[str(source)]={'published_path':target,'raw_sha256':digest,'original_bytes':size}
        payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
        payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'actual150_59_scores_sealed_anchor_and_post_score_recovery_plus_fixed154_declaration',
            'at_local':sync.now(),'files':bindings,'actual150_official_cases':59,'actual150_best_score':pilot['best']['connected_final_score'],
            'actual150_selected_anchor':148,'actual150_new_candidate_inference_claimed':False,'actual_generated150_programs_reconciled':8,
            'actual_future_import_source_checks':24,'actual_future_registry_destination_checks':13,
            'new_seed10_configuration_frozen':True,'actual_seed10_annual_models_at_collection':len(infos),
            'two_seed_equal_weight79_quality_proposal_frozen':True,'actual154_synthetic_cases':73,'actual154_synthetic_cold_cases':219,'actual154_full_mean_and73_training_checks_queued':True,'new154_official_scores':0,'new154_fully_qualified_not_claimed':True,
            'historical_failed_attempts_preserved':True,'primary_workspace_index_preserved':True,'test_labels_read':False,'search_exhaustion_claimed':False})
        create(out/'frozen_before_main_publication.json',{'files':bindings})
        with installed(out/'file_backed_git'):
            previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous);assert not sync.git('status','--porcelain')
            for n,d in payload.items():sync.atomic(sync.WORKTREE/n,d)
            names=sorted(payload)
            for left in range(0,len(names),50):sync.git('add','-f','--',*names[left:left+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','同步154两种子集成73合成219截断和完整历史检查派发及资源实测',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()};assert helpers.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit)
            value={'status':'pushed_and_remote_head_verified','at_local':sync.now(),'branch':'main','commit':commit,'raw_git_blobs_verified':len(hashes),
                'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()}
            create(out/'receipt.json',value);create(A/'two_seed154_synthetic_main_v66_receipt_20261009.json',value);print(value,flush=True)
    finally:
        for p in reversed(held):
            if p.is_running():p.resume()
        create(out/'idle_publisher_resumed.json',{'held_processes':len(held),'resumed_in_finally':True,'scientific_workers_held':0})

if __name__=='__main__':
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for offset,(key,value) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):
        os.environ[f'GIT_CONFIG_KEY_{count+offset}']=key;os.environ[f'GIT_CONFIG_VALUE_{count+offset}']=value
    os.environ['GIT_CONFIG_COUNT']=str(count+2)
    from lossless_chunked_safe_main_runtime_v1_20261009 import installed as safe
    from serial_main_publication_mutex_v1_20261009 import installed as serial
    log=Path('E:/赛题五_本机临时/two_seed154_synthetic_safe_publication_v66_20261009')
    with safe(log),serial(log/'serial_publication_mutex.json'):main()
