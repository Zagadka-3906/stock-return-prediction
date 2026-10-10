"""Publish actual138 completion, all retained failures, and new145 historical controls; main only."""
from pathlib import Path
import datetime,gzip,hashlib,json,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def closed(name):
    folder=A/'service_owned_workflows_20261006'/name
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(10)
    assert read(folder/'service_execution.json')['status']=='passed',name
def main():
    for name in ('BF16reverse40_round138_full_registration_v17_20261008','CrossFamilyFine30_actual_native_historical_controls_v1_20261008',
        'CrossFamilyFine121_actual_full_historical_controls_v1_20261008','HuberCrossFamily112_controls_main_publication_v18_20261008'):closed(name)
    from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
    from verified_TLS_Git_retry_runtime_v2_20261008 import installed
    import publish_classifier_consensus_workflows_20261006 as helpers
    out=Path('E:/赛题五_本机临时/actual138_and_fine145_historical_controls_main_v25_20261008');assert not out.exists();out.mkdir();held=[]
    try:
        for name,needle in [('HuberCrossFamily112_scores_main_publication_v18_20261008','    closed (publish_HuberCrossFamily112_evidence_v18_20261008.py:'),('main_publisher_v8_20261008','    main (watch_validations_main_v7_20261006.py:71)')]:
            row=read(A/'service_owned_workflows_20261006'/name/'native_launch.json');assert owned(row),name
            parent,worker,proof=suspended_idle(row,needle);held.extend((worker,parent));create(out/(name+'_idle_hold.json'),{'identity':row,'actual_idle_stack':proof,'model_fit_scoring_or_inference_workers_held':0})
        since=datetime.datetime(2026,10,8,17,11).timestamp()
        sources=[Path(__file__),A/'github_validation_sync_main_20261005/round138_receipt.json',A/'optimization_20261003_r138/full_registration_execution.json']
        sources.extend(p for p in A.iterdir() if p.is_file() and p.suffix in ('.py','.json','.md') and p.stat().st_mtime>=since)
        for folder in (A/'service_owned_workflows_20261006').iterdir():
            if not folder.is_dir():continue
            entries=[p for p in folder.iterdir() if p.is_file() and p.suffix in ('.json','.log')]
            if any(p.stat().st_mtime>=since for p in entries):sources.extend(entries)
        for pointer in ('actual_CrossFamilyFine30_native_hooks_location_v1_20261008.json','actual_CrossFamilyFine121_parent134_location_v1_20261008.json'):
            folder=Path(read(A/pointer)['output']);sources.extend(folder.glob('*.json'))
        api=Path('E:/赛题五_本机临时/exact138_scores_connected_API_v1_20261008')
        sources.extend(api/n for n in ('bundle.json','actual_connected_API_mutation_responses.json','actual_native_remote_and_blob_verification_calls.json','reconciliation_verification_v2.json'))
        payload={};bindings={};sync=helpers.sync;prefix=Path('validation_sync/actual138_and_fine145_historical_controls_v25_20261008')
        for source in dict.fromkeys(sources):
            data=source.read_bytes();assert not sync.SECRET.search(data),source
            raw=hashlib.sha256(data).hexdigest();size=len(data);relative=source.relative_to(ROOT) if source.is_relative_to(ROOT) else Path('external_metadata')/(raw+'_'+source.name)
            target=(prefix/relative).as_posix()
            if size>=5*1024**2:data=gzip.compress(data,mtime=0);target+='.gz';assert hashlib.sha256(gzip.decompress(data)).hexdigest()==raw
            payload[target]=data;bindings[str(source)]={'published_path':target,'raw_sha256':raw,'original_bytes':size,'captured_at_local':sync.now()}
        full=read(A/'optimization_20261003_r138/full_registration_execution.json');assert full['status']=='passed'
        fine=read(Path(read(A/'actual_CrossFamilyFine121_parent134_location_v1_20261008.json')['output'])/'verification.json')
        assert fine['actual_nonzero_full_cases']==120 and fine['actual_nonzero_cold_cases']==360
        payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
        payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'actual138_full_qualification_and_new_signed145_historical_controls_with_all_failures_distinct',
            'at_local':sync.now(),'files':bindings,'actual138_official_cases':40,'actual138_new_inference_claimed':False,
            'actual145_native_historical_hooks':30,'actual145_native_cold_hooks':30,'actual145_nonzero_full_CDF_controls':120,'actual145_nonzero_cold_CDF_controls':360,
            'actual145_synthetic_cases':120,'actual145_synthetic_cold_controls':360,'new145_official_scores':0,'new145_candidate_inference':0,
            'all145_score_candidate_registry_prospective_receivers_still_required':True,'running_logs_are_frozen_snapshots_at_read':True,
            'fully_qualified_best_round':136,'best_score':0.4511623376562006,'new_official_scores_by_publication':0,'test_labels_read':False})
        create(out/'frozen_before_main_publication.json',{'files':bindings,'passed_failed_and_running_states_kept_distinct':True,'new_quality_scores':0})
        with installed(out/'file_backed_git'):
            previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous);assert not sync.git('status','--porcelain')
            for name,data in payload.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(payload)
            for left in range(0,len(names),50):sync.git('add','-f','--',*names[left:left+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','同步138轮完整验证、145轮细权重历史控制和全部恢复记录',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()};assert helpers.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit)
            receipt={'status':'pushed_and_remote_head_verified','at_local':sync.now(),'branch':'main','commit':commit,'raw_git_blobs_verified':len(hashes),
                'new_quality_scores':0,'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()}
            create(out/'receipt.json',receipt);create(A/'actual138_fine145_historical_controls_main_v25_receipt_20261008.json',receipt);print(json.dumps(receipt,ensure_ascii=False),flush=True)
    finally:
        for process in reversed(held):
            if process.is_running():process.resume()
        create(out/'actual_idle_publishers_resumed.json',{'held_processes':len(held),'resumed_in_finally':True,'model_fit_scoring_or_inference_workers_held':0})
if __name__=='__main__':main()
