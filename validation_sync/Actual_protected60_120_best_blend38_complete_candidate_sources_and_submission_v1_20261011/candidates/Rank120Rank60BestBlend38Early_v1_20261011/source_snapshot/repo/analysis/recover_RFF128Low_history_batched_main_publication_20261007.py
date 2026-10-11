"""Resume the actual failed pre-commit payload with bounded git arguments and byte verification."""
from pathlib import Path
import sys,time,gzip,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
from hidden_windows_child_creation_20261006 import install
import publish_classifier_consensus_workflows_20261006 as helpers

def main():
    sync=helpers.sync;prefix=Path('validation_sync/RFF128Low_actual_history_20261007')
    out=A/'RFF128Low_actual_history_github_20261007';frozen=read(out/'frozen_before_publication.json')
    assert not (out/'receipt.json').exists()
    original_manifest_path=sync.WORKTREE/prefix/'manifest.json';original_manifest=original_manifest_path.read_bytes()
    manifest=read(original_manifest_path);assert manifest['previous_main']==sync.git('rev-parse','HEAD')
    extras=[Path(__file__),A/'local_only_monitor_v25_source_preparation_20261007.json',
        A/'prepare_local_only_monitor_v25_20261007.py',A/'monitor_local_only_runtime_v25_20261007.py',
        A/'handoff_local_only_monitor_v25_20261007.py']
    for folder in [A/'local_only_monitor_v25_actual_handoff_20261007',
        A/'RFF128Low126_unadmitted_publication_source_correction_20261007',
        A/'RFF128Low126_unadmitted_publication_path_correction_20261007']:
        extras.extend(p for p in folder.glob('*') if p.is_file())
    for name in ('RFF128Low_actual_history_main_after125','RFF128Low_actual_history_main_after125_v2',
        'RFF128Low_actual_history_main_after125_v3','nonflag_RFF128Low76_actual_admission_dependency_queue',
        'nonflag_RFF128Low76_actual_admission_dependency_queue_v2','nonflag_RFF128Low76_actual_admission_dependency_queue_v3',
        'local_only_monitor_v25_exact_idle_handoff'):
        folder=A/'service_owned_workflows_20261006'/name
        assert not owned(read(folder/'native_launch.json'))
        extras.extend(folder.glob('*.json'));extras.extend(folder.glob('*.log'))
    pins={**frozen['input_sha256'],**{str(p):sha(p) for p in extras}}
    payload={};files=dict(manifest['files'])
    for item in manifest['files'].values():
        p=sync.WORKTREE/item['published_path'];data=p.read_bytes()
        raw=gzip.decompress(data) if p.name.endswith('.gz') else data
        assert hashlib.sha256(raw).hexdigest()==item['original_sha256'],p
        payload[item['published_path']]=data
    payload[(prefix/'.gitattributes').as_posix()]=(sync.WORKTREE/prefix/'.gitattributes').read_bytes()
    payload[(prefix/'original_manifest_from_failed_precommit.json').as_posix()]=original_manifest
    for p in extras:
        data=p.read_bytes();assert not sync.SECRET.search(data);raw=hashlib.sha256(data).hexdigest()
        target=(prefix/p.relative_to(ROOT)).as_posix()
        if len(data)>=5*1024**2:data=gzip.compress(data,mtime=0);target+='.gz'
        payload[target]=data;files[str(p.relative_to(ROOT))]={'published_path':target,'original_sha256':raw}
    manifest.update(files=files,publication_recovery='actual_existing_payload_batched50_paths_with_all_raw_bytes_verified',
        real_failed_precommit_status_preserved=True,new_native_fits_by_recovery=0,new_quality_scores_by_recovery=0)
    payload[(prefix/'manifest.json').as_posix()]=sync.encoded(manifest)
    held=[];restore=install()
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v7/native_launch.json')
        parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
        with LockedReadHashCache(pins) as scope:
            previous=sync.git('rev-parse','HEAD');assert previous==manifest['previous_main'];helpers.verify_main(previous)
            # This actual failed attempt wrote only the declared prefix and staged nothing.
            assert not sync.git('diff','--cached','--name-only')
            for line in sync.git('-c','core.quotepath=false','status','--porcelain','--untracked-files=all').splitlines():
                assert line.startswith('?? '+prefix.as_posix()+'/'),line
            for name,data in payload.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(payload)
            for left in range(0,len(names),50):sync.git('add','-f','--',*names[left:left+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())<=set(payload)
            scope.reverify()
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m',
                '保存本机内存释放续跑与弱正则RFF128验证，分批恢复历史记录及125轮完整榜',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={k:hashlib.sha256(v).hexdigest() for k,v in payload.items()}
            assert helpers.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit);scope.reverify()
            create(out/'receipt.json',{'status':'pushed_and_remote_head_verified','branch':'main','commit':commit,
                'raw_git_blobs_verified':len(hashes),'actual_native_fits':10,'saved_fits_reused':frozen['saved_fits_reused'],
                'actual_new_native_fits_by_resume':frozen['new_fits_by_resume'],'new_quality_scores_by_publication':0,
                'actual_recovery_service':'RFF128Low_history_batched_main_recovery'})
    finally:
        for p in reversed(held):
            if p.is_running():p.resume()
        create(out/'actual_batched_recovery_hidden_children.json',{'events':restore()})
if __name__=='__main__':main()
