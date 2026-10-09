"""Publish actual all20 annual replay coverage and151 complete preflight/dependency closure without quality claims."""
from pathlib import Path
import sys,time,hashlib,gzip
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def closed(name):
    folder=A/'service_owned_workflows_20261006'/name
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(10)
    assert read(folder/'service_execution.json')['status']=='passed',name

def main():
    for name in ('RFFSparse151_historical_main_publication_v2_20261009','RFFSparse151_complete_prospective_controls_v1_20261009',
        'HuberSparse18_year2023_native_supplement_v1_20261009','RFFSparse18_year2023_native_supplement_v1_20261009'):closed(name)
    current=read(A/'AdaptiveJointCrossHuber242_official_comparison_v1_20261008/actual_stage.json')
    # Serialize around the next148 phase writer if its science is close to completion.
    if current['actual_completed_cases']>=215:closed('AdaptiveJointCrossHuber242_scores_main_publication_v1_20261008')
    proof_paths=[A/n for n in ('sparse150151_all20_annual_native_coverage_v1_20261009.json','RFFSparse59_prospective_routes_v1_20261009.json',
        'RFFSparse151_project_source_closure_v1_20261009.json','HuberSparse150_all5_annual_receiver_runtime_v1_20261009.json','RFFSparse151_source_closure_receiver_runtime_v1_20261009.json')]
    sources=[Path(__file__),*proof_paths]
    for proof_path in proof_paths:
        proof=read(proof_path)
        for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
        sources.extend(Path(p) for p in proof['input_sha256'] if Path(p).suffix in ('.py','.json','.md','.log'))
    for pattern in ('*RFFSparse*','*sparse150151*','*HuberSparse150*','*HuberSparse18*'):
        sources.extend(p for p in A.glob(pattern) if p.is_file() and p.suffix in ('.py','.json'))
    for pointer in ('actual_HuberSparse18_year2023_native_supplement_location_v1_20261009.json','actual_RFFSparse18_year2023_native_supplement_location_v1_20261009.json'):
        p=A/pointer;folder=Path(read(p)['output']);assert sha(folder/'verification.json')==read(p)['verification_sha256'];sources.extend([p,*folder.glob('*.json')])
    for name in ('HuberSparse18_year2023_native_supplement_v1_20261009','RFFSparse18_year2023_native_supplement_v1_20261009',
        'HuberSparse150_complete_chronological_dispatch_v3_20261009','RFFSparse151_complete_chronological_dispatch_v1_20261009',
        'RFFSparse151_complete_chronological_dispatch_v2_20261009','RFFSparse151_complete_prospective_controls_v1_20261009','RFFSparse151_prior_complete_forecast_duplicate_audit_v1_20261009'):
        folder=A/'service_owned_workflows_20261006'/name;sources.extend(p for p in folder.iterdir() if p.is_file() and p.suffix in ('.json','.log'))
    sources.extend([A/'actual_HuberSparse150_all5_native_dispatch_recovery_v3_20261009.json',A/'actual_RFFSparse151_source_closure_dispatch_recovery_v2_20261009.json'])
    sources=list(dict.fromkeys(sources));assert all(p.is_file() and p.suffix in ('.py','.json','.md','.log') for p in sources)
    from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
    from verified_TLS_Git_retry_runtime_v2_20261008 import installed
    import publish_classifier_consensus_workflows_20261006 as helpers
    out=Path('E:/赛题五_本机临时/sparse150151_full_prospective_main_v50_20261009');out.mkdir(exist_ok=False);held=[]
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v9_20261009/native_launch.json');assert owned(row)
        parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        create(out/'main_watcher_idle_hold.json',{'identity':row,'stack':idle,'scientific_workers_held':0})
        sync=helpers.sync;prefix=Path('validation_sync/sparse150151_full_prospective_v50_20261009');payload={};bindings={}
        for source in sources:
            data=source.read_bytes();assert not sync.SECRET.search(data),source
            digest=hashlib.sha256(data).hexdigest();relative=source.relative_to(ROOT) if source.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+source.name)
            target=(prefix/relative).as_posix();size=len(data)
            if size>=5*1024**2:data=gzip.compress(data,mtime=0);target+='.gz';assert hashlib.sha256(gzip.decompress(data)).hexdigest()==digest
            payload[target]=data;bindings[str(source)]={'published_path':target,'raw_sha256':digest,'original_bytes':size}
        payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
        payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'actual150151_all20_annual_native90_cold90_and151_complete32_prospective440_graph_dependency_closure_before_quality',
            'at_local':sync.now(),'files':bindings,'actual20_annual_states_per_scheme_native_replayed':True,'actual90_native90_cold_per_scheme':True,
            'actual151_prospective_sources':32,'actual151_graph_controls':440,'actual151_baseline_controls':12,'actual151_sort_controls':8,'actual151_collector_contracts':4,
            'actual151_project_source_closure_count':read(proof_paths[2])['project_source_count'],'all_first_generator_and_prospective_failures_preserved':True,
            'actual150_official_scores':0,'actual151_official_scores':0,'actual150151_future_inference':0,'actual150_dispatch3_and151_dispatch2_wait_previous_qualified_schemes':True,
            'actual_forecast_duplicate_audits_still_pending_previous_round_completion':True,'new_native_fits':0,'test_labels_read':False,'actual_future_X_read':False,
            'search_exhaustion_claimed':False,'primary_workspace_dirty_index_preserved':True})
        create(out/'frozen_before_main_publication.json',{'files':bindings,'quality_source_admitted':False})
        with installed(out/'file_backed_git'):
            previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous);assert not sync.git('status','--porcelain')
            for name,data in payload.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(payload)
            for left in range(0,len(names),50):sync.git('add','-f','--',*names[left:left+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','同步150与151全五年度90原生及151完整32代码440方案图冻结依赖证据',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()};assert helpers.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit)
            receipt={'status':'pushed_and_remote_head_verified','at_local':sync.now(),'branch':'main','commit':commit,'raw_git_blobs_verified':len(hashes),'actual150151_official_scores':0,'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()}
            create(out/'receipt.json',receipt);create(A/'sparse150151_full_prospective_main_v50_receipt_20261009.json',receipt);print(receipt,flush=True)
    finally:
        for p in reversed(held):
            if p.is_running():p.resume()
        create(out/'idle_publisher_resumed.json',{'held_processes':len(held),'resumed_in_finally':True,'scientific_workers_held':0})
if __name__=='__main__':main()
