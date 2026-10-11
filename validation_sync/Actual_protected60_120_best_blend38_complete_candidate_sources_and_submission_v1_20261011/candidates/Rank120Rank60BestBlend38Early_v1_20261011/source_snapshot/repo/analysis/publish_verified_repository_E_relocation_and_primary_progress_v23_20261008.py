"""Publish the actually verified storage relocation and every failed attempt; leave science and model selection unchanged."""
from pathlib import Path
import gzip,hashlib,json,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def main():
    service=A/'service_owned_workflows_20261006/Git_publisher_verified_E_relocation_v3_20261008'
    while not (service/'native_launch.json').exists() or owned(read(service/'native_launch.json')):time.sleep(5)
    assert read(service/'service_execution.json')['status']=='passed'
    base=Path('E:/赛题五_本机临时/Git_publisher_E_relocation_v3_20261008');proof=read(base/'verification.json')
    assert proof['status']=='passed_complete_repository_byte_exact_E_relocation_original_D_access_path_and_main_preserved'
    from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
    import publish_classifier_consensus_workflows_20261006 as helpers
    from file_backed_hidden_git_runtime_20261007 import installed
    out=Path('E:/赛题五_本机临时/Git_relocation_primary_progress_main_v23_20261008');assert not out.exists();out.mkdir()
    held=[]
    try:
        for name,needle in [('Huber52_scores_main_publication_v14_20261008','    closed (publish_Huber52_evidence_v14_20261008.py:'),('main_publisher_v8_20261008','    main (watch_validations_main_v7_20261006.py:71)')]:
            row=read(A/'service_owned_workflows_20261006'/name/'native_launch.json');assert owned(row)
            parent,worker,idle=suspended_idle(row,needle);held.extend((worker,parent));create(out/(name+'_actual_idle_hold.json'),{'identity':row,'actual_idle_stack':idle,'scientific_workers_stopped':0})
        sources=[Path(__file__),A/'prepare_actual_progress_observer23_dispatch16_binding_20261008.py',A/'monitor_actual_chronological_optimization_progress_v23_20261008.py',
            A/'actual_chronological_optimization_progress_observer_v23_hidden_launch_20261008.json',A/'latest_actual_optimization_progress_pointer_v23_20261008.json',
            A/'Git_publisher_E_relocation_location_v3_20261008.json',A/'Git_publisher_E_relocation_gate_recovery_v2_20261008.json',A/'Git_publisher_E_relocation_raw_path_preflight_v3_20261008.json',
            A/'prepare_idle_Git_E_relocation_at_scores_wait_v2_20261008.py',A/'prepare_verified_raw_PowerShell_repository_relocation_v3_20261008.py']
        for version in (1,2,3):
            sources.append(A/f'relocate_idle_verified_Git_publisher_to_E_v{version}_20261008.py')
            folder=A/f'service_owned_workflows_20261006/Git_publisher_verified_E_relocation_v{version}_20261008'
            sources.extend(p for p in folder.iterdir() if p.is_file() and p.suffix in ('.json','.log'))
            folder=Path(f'E:/赛题五_本机临时/Git_publisher_E_relocation_v{version}_20261008')
            sources.extend(p for p in folder.iterdir() if p.is_file() and p.suffix in ('.json','.ps1','.stdout','.stderr'))
        registration=A/'CrossFamily94_round136_actual_registration_v6_20261008/actual_transport_retries.json'
        assert registration.is_file();sources.append(registration)
        sync=helpers.sync;prefix=Path('validation_sync/Git_E_relocation_and_primary_progress_v23_20261008');payload={};bindings={}
        for source in dict.fromkeys(sources):
            data=source.read_bytes();assert not sync.SECRET.search(data),source;digest=hashlib.sha256(data).hexdigest();size=len(data)
            relative=source.relative_to(ROOT) if source.is_relative_to(ROOT) else Path('external_frozen_metadata')/(digest+'_'+source.name)
            destination=(prefix/relative).as_posix()
            if size>=5*1024**2:data=gzip.compress(data,mtime=0);destination+='.gz';assert hashlib.sha256(gzip.decompress(data)).hexdigest()==digest
            payload[destination]=data;bindings[str(source)]={'published_path':destination,'original_sha256':digest,'original_bytes':size}
        payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
        payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'actual_verified_byte_exact_repository_E_relocation_and_current_primary_observer',
            'at_local':sync.now(),'files':bindings,'actual_D_free_gain_bytes':proof['actual_D_free_gain_bytes'],'verified_repository_files':proof['files'],
            'verified_repository_bytes':proof['bytes'],'original_D_access_path':proof['original_path'],'physical_E_path':proof['physical_E_path'],
            'failed1_and2_and_passed3_kept_distinct':True,'all_source_weights_and_training_datasets_untouched':True,'scientific_workers_stopped':0,
            'new_scores_or_model_selection_by_storage_change':0,'test_labels_read':False})
        create(out/'frozen_before_main_publication.json',{'files':bindings,'new_quality_scores':0})
        with installed(out/'file_backed_git'):
            previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous);assert not sync.git('status','--porcelain')
            for name,data in payload.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(payload)
            for offset in range(0,len(names),50):sync.git('add','-f','--',*names[offset:offset+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','同步Git发布副本逐文件核验迁移E盘、全部失败记录和真实进度观察器',timeout=180)
            commit=sync.git('rev-parse','HEAD');expected={name:hashlib.sha256(data).hexdigest() for name,data in payload.items()}
            assert helpers.blob_hashes(commit,expected)==expected
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit)
            receipt={'status':'pushed_and_remote_head_verified','branch':'main','at_local':sync.now(),'commit':commit,'raw_git_blobs_verified':len(expected),
                'actual_D_free_gain_bytes':proof['actual_D_free_gain_bytes'],'new_quality_scores':0,'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()}
            create(out/'receipt.json',receipt);create(A/'Git_relocation_primary_progress_main_v23_receipt_20261008.json',receipt);print(json.dumps(receipt,ensure_ascii=False),flush=True)
    finally:
        for process in reversed(held):
            if process.is_running():process.resume()
        create(out/'actual_idle_publication_receivers_resumed.json',{'held_processes':len(held),'resumed_in_finally':True,'scientific_workers_stopped':0})
if __name__=='__main__':main()
