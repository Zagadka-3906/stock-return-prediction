"""Publish137 completion and all storage outcomes after actual ROOT object relocation; serialize against138 score publication."""
from pathlib import Path
import datetime,gzip,hashlib,json,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def main():
    assert read(A/'optimization_20261003_r137/full_registration_execution.json')['status']=='passed'
    assert read(A/'service_owned_workflows_20261006/ROOT_Git_objects_verified_E_relocation_v2_20261008/service_execution.json')['status']=='passed'
    assert read(A/'service_owned_workflows_20261006/BF16reverse40_controls_main_publication_v14_20261008/service_execution.json')['status']=='passed'
    from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
    from file_backed_hidden_git_runtime_20261007 import installed
    import publish_classifier_consensus_workflows_20261006 as helpers
    sync=helpers.sync;out=Path('E:/赛题五_本机临时/actual137_and_ROOT_objects_storage_main_v24_20261008');assert not out.exists();out.mkdir();held=[]
    try:
        for name,needle in [('BF16reverse40_scores_main_publication_v14_20261008','    closed (publish_BF16reverse40_evidence_v14_20261008.py:'),('main_publisher_v8_20261008','    main (watch_validations_main_v7_20261006.py:71)')]:
            row=read(A/'service_owned_workflows_20261006'/name/'native_launch.json');assert owned(row)
            parent,worker,proof=suspended_idle(row,needle);held.extend((worker,parent));create(out/(name+'_actual_idle_hold.json'),{'identity':row,'actual_idle_stack':proof,'model_fit_scoring_or_inference_workers_held':0})
        since=datetime.datetime(2026,10,8,16,31).timestamp();sources=[Path(__file__),A/'github_validation_sync_main_20261005/round137_receipt.json',A/'optimization_20261003_r137/full_registration_execution.json']
        sources.extend(p for p in A.iterdir() if p.is_file() and p.suffix in ('.py','.json','.md') and p.stat().st_mtime>=since)
        for folder in (A/'service_owned_workflows_20261006').iterdir():
            if (folder/'native_launch.json').is_file() and (folder/'native_launch.json').stat().st_mtime>=since:
                sources.extend(p for p in folder.iterdir() if p.is_file() and p.suffix in ('.json','.log'))
        for prefix,versions in [('Git_publisher_E_relocation',(1,2,3)),('ROOT_Git_objects_E_relocation',(1,2))]:
            for version in versions:
                folder=Path(f'E:/赛题五_本机临时/{prefix}_v{version}_20261008')
                assert folder.is_dir()
                sources.extend(p for p in folder.iterdir() if p.is_file() and p.suffix in ('.json','.ps1','.stdout','.stderr'))
        sources.append(A/'CrossFamily94_round136_actual_registration_v6_20261008/actual_transport_retries.json')
        proof=read(Path(read(A/'ROOT_Git_objects_E_relocation_location_v2_20261008.json')['output'])/'verification.json')
        prefix=Path('validation_sync/actual137_ROOT_Git_objects_storage_v24_20261008');payload={};bindings={}
        for source in dict.fromkeys(sources):
            data=source.read_bytes();assert not sync.SECRET.search(data),source
            raw=hashlib.sha256(data).hexdigest();size=len(data);relative=source.relative_to(ROOT) if source.is_relative_to(ROOT) else Path('external_frozen_metadata')/(raw+'_'+source.name)
            target=(prefix/relative).as_posix()
            if size>=5*1024**2:data=gzip.compress(data,mtime=0);target+='.gz';assert hashlib.sha256(gzip.decompress(data)).hexdigest()==raw
            payload[target]=data;bindings[str(source)]={'published_path':target,'sha256':raw,'original_bytes':size}
        payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
        payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'actual137_full_qualification_and_verified_ROOT_object_storage_relocation_all_failures_distinct',
            'at_local':sync.now(),'files':bindings,'fully_qualified_best_round':136,'best_score':0.4511623376562006,'full_connected_records':14024,
            'actual137_official_cases':52,'actual137_new_inference_claimed':False,'actual13840_quality_running_not_claimed_complete':True,
            'actual_ROOT_object_files_verified':proof['files'],'actual_D_space_freed_bytes':proof['actual_D_free_gain_bytes'],
            'original_ROOT_refs_index_and_working_files_preserved':True,'private_publication_repository_not_moved_or_deleted':True,
            'failed_private_copy_Git_state_verification_preserved':True,'models_and_training_inputs_not_moved':True,'new_official_scores_by_publication':0,'test_labels_read':False})
        create(out/'frozen_before_main_publication.json',{'files':bindings,'new_quality_scores':0,'passed_and_failed_and_running_records_kept_distinct':True})
        with installed(out/'file_backed_git'):
            previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous);assert not sync.git('status','--porcelain')
            for target,data in payload.items():sync.atomic(sync.WORKTREE/target,data)
            names=sorted(payload)
            for left in range(0,len(names),50):sync.git('add','-f','--',*names[left:left+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','同步137轮完整验证、Git对象库核验迁移E和全部存储尝试记录',timeout=180)
            commit=sync.git('rev-parse','HEAD');expected={name:hashlib.sha256(data).hexdigest() for name,data in payload.items()};assert helpers.blob_hashes(commit,expected)==expected
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit)
            receipt={'status':'pushed_and_remote_head_verified','branch':'main','commit':commit,'at_local':sync.now(),'raw_git_blobs_verified':len(expected),
                'actual_D_free_gain_bytes':proof['actual_D_free_gain_bytes'],'new_quality_scores':0,'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()}
            create(out/'receipt.json',receipt);create(A/'actual137_ROOT_object_storage_main_v24_receipt_20261008.json',receipt);print(json.dumps(receipt,ensure_ascii=False),flush=True)
    finally:
        for process in reversed(held):
            if process.is_running():process.resume()
        create(out/'actual_idle_publishers_resumed.json',{'held_processes':len(held),'resumed_in_finally':True,'model_fit_scoring_or_inference_workers_held':0})
if __name__=='__main__':main()
