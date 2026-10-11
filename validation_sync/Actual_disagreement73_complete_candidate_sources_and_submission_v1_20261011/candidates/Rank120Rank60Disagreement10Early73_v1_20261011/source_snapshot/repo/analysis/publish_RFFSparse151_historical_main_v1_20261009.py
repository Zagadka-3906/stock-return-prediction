"""Publish actual151 synthetic/native/full historical controls; quality admission and future inference remain pending."""
from pathlib import Path
import sys,time,hashlib,gzip
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def closed(name):
    folder=A/'service_owned_workflows_20261006'/name
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(10)
    assert read(folder/'service_execution.json')['status']=='passed',name

def main():
    for name in ('RFFSparse72_native_historical_calendar_controls_v1_20261009','RFFSparse55_full_historical_controls_v1_20261009','HuberSparse150_prospective_main_publication_v2_20261009'):closed(name)
    synthetic_path=A/'RFFSparse59_synthetic55_and_state20_metadata_v1_20261009.json';synthetic=read(synthetic_path)
    assert synthetic['actual_cases']==55 and synthetic['actual_cold_cases']==165 and synthetic['actual_saved_state_metadata_count']==20
    for path,digest in synthetic['input_sha256'].items():assert sha(path)==digest,path
    native_pointer=A/'actual_RFFSparse72_native_calendar_location_v1_20261009.json';full_pointer=A/'actual_RFFSparse55_parent134_location_v1_20261009.json'
    folders=[];proofs=[]
    for pointer in (native_pointer,full_pointer):
        descriptor=read(pointer);folder=Path(descriptor['output']);path=folder/'verification.json';assert sha(path)==descriptor['verification_sha256'];folders.append(folder);proofs.append(read(path))
    native,full=proofs
    assert (native['actual_historical_cases'],native['actual_calendar_cases'],native['actual_cold_cases'])==(54,18,72)
    assert full['actual_full_cases_including_identity']==55 and full['actual_cold_cases_including_identity']==165
    sources=[Path(__file__),synthetic_path,native_pointer,full_pointer,*[Path(p) for p in synthetic['input_sha256'] if Path(p).suffix in ('.py','.json','.md')]]
    sources.extend(p for p in A.glob('*RFFSparse*') if p.is_file() and p.suffix in ('.py','.json'))
    for folder in folders:sources.extend(folder.glob('*.json'))
    for name in ('RFFSparse72_native_historical_calendar_controls_v1_20261009','RFFSparse55_full_historical_controls_v1_20261009'):
        folder=A/'service_owned_workflows_20261006'/name;sources.extend(p for p in folder.iterdir() if p.is_file() and p.suffix in ('.json','.log'))
    sources=list(dict.fromkeys(sources))
    assert all(p.is_file() and p.suffix in ('.py','.json','.md','.log') for p in sources)
    from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
    from verified_TLS_Git_retry_runtime_v2_20261008 import installed
    import publish_classifier_consensus_workflows_20261006 as helpers
    out=Path('E:/赛题五_本机临时/RFFSparse151_historical_main_v1_20261009');out.mkdir(exist_ok=False);held=[]
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v9_20261009/native_launch.json');assert owned(row)
        parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        create(out/'main_watcher_idle_hold.json',{'identity':row,'stack':idle,'scientific_workers_held':0})
        sync=helpers.sync;prefix=Path('validation_sync/RFFSparse151_historical_v1_20261009');payload={};bindings={}
        for source in sources:
            data=source.read_bytes();assert not sync.SECRET.search(data),source
            digest=hashlib.sha256(data).hexdigest();relative=source.relative_to(ROOT) if source.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+source.name)
            target=(prefix/relative).as_posix();size=len(data)
            if size>=5*1024**2:data=gzip.compress(data,mtime=0);target+='.gz';assert hashlib.sha256(gzip.decompress(data)).hexdigest()==digest
            payload[target]=data;bindings[str(source)]={'published_path':target,'raw_sha256':digest,'original_bytes':size}
        payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
        payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'actual151_training_only_synthetic_native_full_controls_completed_before_quality_admission',
            'at_local':sync.now(),'round':151,'files':bindings,'actual_synthetic_cases':55,'actual_synthetic_cold_cases':165,'actual_saved_state_metadata':20,
            'actual_historical_native_cases':54,'actual_final_model_calendar_cases':18,'actual_cold_native_cases':72,'actual_prefit_date_rejections':18,
            'actual_full_training_OOF_cases':55,'actual_full_cold_cases':165,'stage_base_round':134,'teacher_round':106,
            'actual151_official_scores':0,'actual151_future_inference':0,'own32_quality_receivers_and_duplicate_audit_still_required':True,
            'two_first_preparation_failures_retained_before_proposal_or_quality':True,'new_native_fits':0,'test_labels_read':False,'actual_future_X_read':False,
            'search_exhaustion_claimed':False,'primary_workspace_dirty_index_preserved':True})
        create(out/'frozen_before_main_publication.json',{'files':bindings,'quality_source_admitted':False})
        with installed(out/'file_backed_git'):
            previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous);assert not sync.git('status','--porcelain')
            for name,data in payload.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(payload)
            for left in range(0,len(names),50):sync.git('add','-f','--',*names[left:left+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','同步第151轮RFF与稀疏残差55完整165冷检查72原生实际证据',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()};assert helpers.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit)
            receipt={'status':'pushed_and_remote_head_verified','at_local':sync.now(),'branch':'main','commit':commit,'raw_git_blobs_verified':len(hashes),'actual151_official_scores':0,'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()}
            create(out/'receipt.json',receipt);create(A/'RFFSparse151_historical_main_v1_receipt_20261009.json',receipt);print(receipt,flush=True)
    finally:
        for p in reversed(held):
            if p.is_running():p.resume()
        create(out/'idle_publisher_resumed.json',{'held_processes':len(held),'resumed_in_finally':True,'scientific_workers_held':0})
if __name__=='__main__':main()
