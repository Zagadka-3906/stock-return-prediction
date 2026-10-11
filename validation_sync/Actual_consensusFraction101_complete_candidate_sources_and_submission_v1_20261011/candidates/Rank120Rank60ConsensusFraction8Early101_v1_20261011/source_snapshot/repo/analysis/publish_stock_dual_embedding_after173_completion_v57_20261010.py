"""Publish the actual independent Huber restart controls, before any quality claim."""
from pathlib import Path
from datetime import datetime, timezone, timedelta
import sys, os, gzip, hashlib, time
A=Path(__file__).resolve().parent; ROOT=A.parent
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def main():
    read(A/'current_user_runtime_control_20261009.json')
    control=read(A/'current_user_runtime_control_20261010.json')
    assert control['status']=='optimization_active_after_explicit_manual_resume'
    assert datetime.now(timezone(timedelta(hours=8)))<datetime.fromisoformat(control['stop_at_local'])
    assert read(A/'immutable_prepared_rank_panel_cache_actual_full_TRAIN_benchmark_v1_20261010.json')['status'].startswith('passed')
    assert read(A/'dual_target_rank_consensus_actual13950_TRAIN_and_ties_CPU_controls_v1_20261010.json')['status'].startswith('passed')
    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import closed
    closed('actual_stock_dual_embedding_after173_high_impact25_screen_v1_20261010')
    screen=Path('E:/赛题五_本机临时/StockDualEmbedding_after173_high_impact25_screen_v1_20261010')
    proof=read(screen/'verification.json');assert len(proof['records'])==proof['new_quality_score_records']==25
    assert proof['actual_nonidentity_full_controls']==24 and proof['actual_nonidentity_prefix_controls']==72
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    native=Path(read(A/'actual_stock_rank_embedding_six_state_native42_location_v1_20261010.json')['output'])
    assert read(native/'verification.json')['actual_native_cases']==42
    paths=[*native.glob('*.json'),Path(__file__),A/'stock_rank_embedding_native_stage_and_fast17_sources_admission_v1_20261010.json',A/'run_stock_dual_embedding_after173_high_impact25_screen_v1_20261010.py',*screen.glob('*.json')]
    for admission in ('stock_rank_embedding_own_sources_and_actual_centered_target_admission_v1_20261010.json','stock_rank_embedding_actual_priority173_runtime_admission_v2_20261010.json','stock_rank_embedding_native_stage_and_fast17_sources_admission_v1_20261010.json'):
        paths += [A/admission,*[Path(p) for p in read(A/admission)['input_sha256'] if Path(p).suffix=='.py']]
    paths += [A/'stock_dual_embedding_after173_predeclared25_plan_v1_20261010.json',A/'prepare_stock_dual_embedding_after173_25_v1_20261010.py',A/'dual_target_daily_rank_consensus_v1_20261010.py']
    return_bank=Path(read(A/'actual_stock_embedding_small512_bank6_location_v1_20261010.json')['output'])
    paths += [return_bank/'verification.json',*return_bank.glob('*/info.json')]
    for return_pointer in ('actual_stock_embedding_six_state_native42_location_v1_20261010.json','actual_StockEmbeddingSmall512_full5_independent_location_v1_20261009.json'):
        paths += [A/return_pointer,*Path(read(A/return_pointer)['output']).glob('*.json')]
    bank=Path(read(A/'actual_stock_rank_embedding_small512_bank6_location_v1_20261010.json')['output']);assert read(bank/'verification.json')['actual_native_fits']==6
    paths += [bank/'verification.json',*bank.glob('*/info.json')]
    pointer=A/'actual_StockRankEmbeddingSmall512_full5_independent_location_v1_20261009.json'
    paths += [pointer,*Path(read(pointer)['output']).glob('*.json')]
    for row in proof['records']:
        capsule=Path(row['official_score_cache']['official_metrics_source']);assert sha(capsule)==row['official_metric_capsule_sha256'];paths.append(capsule)
    service=A/'service_owned_workflows_20261006/actual_stock_dual_embedding_after173_high_impact25_screen_v1_20261010'
    paths.extend(service/name for name in ('native_launch.json','service_execution.json','job_definition.json'))
    import publish_classifier_consensus_workflows_20261006 as h
    prefix=Path('validation_sync/stock_dual_embedding25_after173_completion_v57_20261010'); payload={}; bindings={}
    for p in dict.fromkeys(paths):
        raw=p.read_bytes();assert not h.sync.SECRET.search(raw),p
        digest=hashlib.sha256(raw).hexdigest()
        rel=p.relative_to(ROOT) if p.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+p.name)
        name=(prefix/rel).as_posix(); data=raw
        if len(data)>=5*1024**2:data=gzip.compress(data,mtime=0);name+='.gz';assert gzip.decompress(data)==raw
        assert len(data)<95*1024**2;payload[name]=data;bindings[str(p)]={'path':name,'raw_sha256':digest}
    payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({'status':'passed25_actual_stock_dual_embedding_TRAIN_official_records24_full72_cold_controls_selected_stage_candidate_freeze_and_full_registration_pending','files':bindings,'submission_qualified':False,'best_actual_training_only_screen':proof['best'],'scored_records':25,'new_native_fits':0,'new_quality_scores_by_publication':0,'test_labels_read':False,'deadline_local':control['stop_at_local']})
    out=Path('E:/赛题五_本机临时/stock_dual_embedding25_after173_completion_main_v57_20261010');out.mkdir(exist_ok=False)
    create(out/'frozen_before_publication.json',{'files':bindings})
    from lossless_chunked_safe_main_runtime_v1_20261009 import installed as safe
    from serial_main_publication_mutex_v1_20261009 import installed as serial
    from verified_TLS_Git_retry_runtime_v3_20261010 import installed as git_io
    from owned_idle_publication_wait_runtime_v1_20261010 import hold as suspended_idle
    with serial(out/'serial_mutex.json') as mutex,safe(out/'safe'),git_io(out/'file_backed_git'):
        mutex.acquire()
        assert datetime.now(timezone(timedelta(hours=8)))<datetime.fromisoformat(read(A/'current_user_runtime_control_20261010.json')['stop_at_local'])
        launch=read(A/'service_owned_workflows_20261006/main_publisher_v11_20261010/native_launch.json')
        parent,worker,idle=suspended_idle(launch,'    main (watch_validations_main_v7_20261006.py:71)')
        try:
            sync=h.sync;h.verify_main(sync.git('rev-parse','HEAD'));assert not sync.git('status','--porcelain')
            for name,data in payload.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(payload)
            for i in range(0,len(names),50):sync.git('add','-f','--',*names[i:i+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','保存股票收益与排名嵌入模型互补集成25项真实TRAIN官方评分、24项完整及72项因果前缀控制',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()}
            assert h.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);h.verify_main(commit);h.watcher.advance_source_index(commit)
            receipt={'status':'pushed_and_remote_head_verified','branch':'main','commit':commit,'raw_git_blobs_verified':len(hashes),'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()}
            create(out/'receipt.json',receipt);create(A/'stock_dual_embedding25_after173_completion_main_receipt_v57_20261010.json',receipt);print(receipt,flush=True)
        finally:
            for p in (parent,worker):
                if p.is_running():p.resume()

if __name__=='__main__':
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(key,value) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=key;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=value
    os.environ['GIT_CONFIG_COUNT']=str(count+2)
    main()
