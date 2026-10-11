"""Publish measured32/440 prospective150 controls and retained verifier failure after148 controls writer."""
from pathlib import Path
import sys,time,hashlib,gzip
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def closed(name):
    folder=A/'service_owned_workflows_20261006'/name
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(10)
    assert read(folder/'service_execution.json')['status']=='passed',name

def main():
    closed('HuberSparse150_prospective_main_publication_v1_20261009')
    closed('HuberSparse150_complete_prospective_controls_v1_20261009')
    closed('AdaptiveJointCrossHuber242_controls_main_publication_v1_20261008')
    proof_path=A/'HuberSparse59_prospective_routes_v1_20261009.json';proof=read(proof_path)
    assert proof['actual_prospective_sources']==32 and proof['actual_graph_controls']==440
    for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
    import prepare_HuberSparse59_round150_sources_v2_20261009 as generator
    sources=[Path(__file__),proof_path,*[p for p in generator.source_paths() if p.is_file()],*[Path(p) for p in proof['input_sha256']],
        A/'HuberSparse150_D_scoring_scope_v1_20261008.json',A/'HuberSparse150_prospective_v1_collector_invocation_failure_v1_20261009.json',
        A/'verify_HuberSparse59_prospective_routes_v2_20261009.py',A/'HuberSparse150_foreground_prospective_receipt_v1_20261009.json',
        A/'verify_HuberSparse150_foreground_prospective_receipt_v1_20261009.py',A/'dispatch_HuberSparse150_complete_pipeline_v1_20261009.py',
        A/'actual_HuberSparse150_verified_pipeline_hidden_launches_v1_20261009.json',A/'prepare_HuberSparse150_prospective_verifier_v1_20261009.py',
        A/'prepare_HuberSparse150_evidence_publisher_v1_20261009.py']
    for name in ('HuberSparse150_complete_prospective_controls_v1_20261009','HuberSparse150_prior_complete_forecast_duplicate_audit_v1_20261009','HuberSparse150_complete_chronological_dispatch_v1_20261009'):
        folder=A/'service_owned_workflows_20261006'/name;sources.extend(p for p in folder.iterdir() if p.is_file() and p.suffix in ('.json','.log'))
    for pointer in ('actual_HuberSparse55_parent134_location_v1_20261008.json','actual_HuberSparse72_native_calendar_location_v1_20261008.json'):
        p=A/pointer;folder=Path(read(p)['output']);verification=folder/'verification.json';assert sha(verification)==read(p)['verification_sha256'];sources.extend([p,*folder.glob('*.json')])
    from HuberSparse150_import_dependency_closure_v1_20261009 import EXTRAS,META,PROOF
    closure=read(META)
    for path,digest in closure['input_sha256'].items():assert sha(path)==digest,path
    sources.extend([*(A/n for n in EXTRAS),META,PROOF,A/'actual_HuberSparse150_dispatch_import_closure_recovery_v2_20261009.json',
        A/'prepare_actual_progress47_for150_v1_20261009.py',A/'monitor_actual_chronological_optimization_progress_v47_20261009.py',
        A/'monitor_actual_chronological_optimization_progress_v48_20261009.py',A/'prepare_actual_progress48_and150_closure_publication_v1_20261009.py',
        A/'actual_old_progress46_retired_after47_v1_20261009.json'])
    folder=A/'service_owned_workflows_20261006/HuberSparse150_complete_chronological_dispatch_v2_20261009'
    sources.extend(p for p in folder.iterdir() if p.is_file() and p.suffix in ('.json','.log'))
    sources=list(dict.fromkeys(sources));assert all(p.suffix in ('.py','.json','.log','.md','.bin') for p in sources)
    from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
    from verified_TLS_Git_retry_runtime_v2_20261008 import installed
    import publish_classifier_consensus_workflows_20261006 as helpers
    out=Path('E:/赛题五_本机临时/HuberSparse150_prospective_main_v2_20261009');out.mkdir(exist_ok=False);held=[]
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v9_20261009/native_launch.json');assert owned(row)
        parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        create(out/'main_watcher_idle_hold.json',{'identity':row,'stack':idle,'scientific_workers_held':0})
        sync=helpers.sync;prefix=Path('validation_sync/HuberSparse150_prospective_v2_20261009');payload={};bindings={}
        for source in sources:
            data=source.read_bytes();assert not sync.SECRET.search(data),source
            digest=hashlib.sha256(data).hexdigest();relative=source.relative_to(ROOT) if source.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+source.name)
            target=(prefix/relative).as_posix();size=len(data)
            if size>=5*1024**2:data=gzip.compress(data,mtime=0);target+='.gz';assert hashlib.sha256(gzip.decompress(data)).hexdigest()==digest
            payload[target]=data;bindings[str(source)]={'published_path':target,'raw_sha256':digest,'original_bytes':size}
        payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
        payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'actual_completed32_source440_graph150_prospective_checks_before59_quality_admission',
            'at_local':sync.now(),'round':150,'files':bindings,'actual_prospective_sources':32,'actual_graph_controls':440,'actual_baseline_controls':12,
            'actual_sort_controls':8,'actual_collectors':4,'actual_native72_and_full55_cold165_prior_controls_preserved':True,
            'first_verifier_wrong_collector_invocation_failure_and_corrected_wrapper_preserved':True,'actual150_official_scores':0,'actual150_future_inference':0,
            'own_actual149_dependent_duplicate_audit_and_chronological_dispatch_started':True,'actual_inherited_best_key_import_AST_identity_and_raw_source_frozen':True,'current_live_dispatcher_version':2,'retired_child_free_dispatcher1_preserved':True,'new_native_fits':0,'test_labels_read':False,'search_exhaustion_claimed':False,'primary_workspace_dirty_index_preserved':True})
        create(out/'frozen_before_main_publication.json',{'files':bindings,'quality_source_admitted':False})
        with installed(out/'file_backed_git'):
            previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous);assert not sync.git('status','--porcelain')
            for name,data in payload.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(payload)
            for left in range(0,len(names),50):sync.git('add','-f','--',*names[left:left+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','同步第150轮继承排序函数字节冻结及实际连续派发更新',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()};assert helpers.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit)
            receipt={'status':'pushed_and_remote_head_verified','at_local':sync.now(),'branch':'main','commit':commit,'raw_git_blobs_verified':len(hashes),'actual_new_quality_scores':0,'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()}
            create(out/'receipt.json',receipt);create(A/'HuberSparse150_prospective_main_v2_receipt_20261009.json',receipt);print(receipt,flush=True)
    finally:
        for p in reversed(held):
            if p.is_running():p.resume()
        create(out/'idle_publisher_resumed.json',{'held_processes':len(held),'resumed_in_finally':True,'scientific_workers_held':0})
if __name__=='__main__':main()
