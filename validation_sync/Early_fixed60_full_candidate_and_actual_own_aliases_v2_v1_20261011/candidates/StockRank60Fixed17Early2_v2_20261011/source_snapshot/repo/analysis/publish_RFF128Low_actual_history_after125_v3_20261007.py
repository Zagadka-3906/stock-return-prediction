"""Publish real closed local CPU evidence and preserved failed preparation history to main."""
from pathlib import Path
import sys,time,gzip,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
from hidden_windows_child_creation_20261006 import install
import publish_classifier_consensus_workflows_20261006 as helpers

def closed(name):
    folder=A/'service_owned_workflows_20261006'/name
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(10)
    result=read(folder/'service_execution.json');assert result['status']=='passed',name
    return result

def main():
    names=['nonflag_RFF12876_round125_full_registration_v1','local_boundary_audit_v3_after124',
        'RFF128Low_checkpoint_memory_release_exact_idle_handoff',
        'nonflag_residual_RFF128Low_native_bank10_v2','nonflag_RFF128Low_actual_hook6_and_full73_controls_v2']
    terminals={name:closed(name) for name in names}
    bank=A/'nonflag_residual_RFF128Low_bank10_20261007';native=read(bank/'verification.json')
    saved=read(A/'RFF128Low_checkpoint_resume_snapshot_20261007.json')['saved_native_fit_count']
    assert native['actual_native_fits']==10 and native['reused_saved_native_fits']==saved and native['actual_new_native_fits_by_resume']==10-saved
    controls=read(A/'nonflag_residual_RFF128Low73_transform_preflight_20261007/verification.json')
    assert controls['actual_full_cases']==73 and controls['actual_cold_cases']==219
    assert len(read(A/'nonflag_residual_RFF128Low_native_hook6_preflight_20261007/verification.json')['records'])==6
    receipt=read(A/'github_validation_sync_main_20261005/round125_receipt.json')
    assert receipt['status']=='pushed_and_remote_head_verified' and receipt['branch']=='main'
    handoff=read(A/'RFF128Low_checkpoint_memory_release_actual_handoff_20261007/verification.json')
    assert handoff['saved_native_fits_preserved']==saved and handoff['unsaved_fit_progress_lost']==0 and handoff['active_fits_stopped']==0
    sources=[Path(__file__),A/'RFF128Low_checkpoint_resume_snapshot_20261007.json',
        A/'RFF128Low_memory_release_resume_source_preparation_20261007.json',
        A/'local_optimization_boundary_audit_v3_20261007/verification.json',
        A/'local_optimization_boundary_audit_v3_20261007/运行范围说明.md',
        A/'github_validation_sync_main_20261005/round125_receipt.json',
        A/'audit_local_optimization_boundaries_v3_20261007.py',
        A/'handoff_local_only_monitor_v24_20261007.py']
    for pattern in ('*RFF128Low*20261007.py','*RFF128Low*20261007.json','*RFF128125*20261007.py','*RFF128125*20261007.json',
                    '*RFF12876*20261007.py','*RFF12876*20261007.json','*nonflag_residual_RFF128*20261007.py',
                    '*monitor_v24*20261007.py','*audit_v3*20261007.py'):
        sources.extend(A.glob(pattern))
    for folder in [bank,A/'nonflag_residual_RFF128Low_codec2_preflight_20261007',
        A/'nonflag_residual_RFF128Low_native_hook6_preflight_20261007',A/'nonflag_residual_RFF128Low73_transform_preflight_20261007',
        A/'RFF128Low_checkpoint_memory_release_actual_handoff_20261007',
        A/'local_only_monitor_v24_actual_handoff_20261007',
        A/'RFF128125_zero_science_controller_actual_handoff_20261007']:
        sources.extend(folder.glob('*.json'))
    sources.extend(bank.glob('*/info_*.json'));sources.extend(bank.glob('*/oof_verification.json'))
    sources.extend(bank.glob('*/independent_random_fourier_linear_state_*.json'))
    for name in [*names,'nonflag_residual_RFF128Low_native_bank10','nonflag_RFF128Low_actual_hook6_and_full73_controls',
        'nonflag_RFF12876_round125_source_admission_v1','nonflag_RFF12876_continue_after_actual_admission_v2',
        'RFF128Low_actual_history_main_after125','RFF128Low_actual_history_main_after125_v2',
        'nonflag_RFF128Low76_actual_admission_dependency_queue','nonflag_RFF128Low76_actual_admission_dependency_queue_v2']:
        folder=A/'service_owned_workflows_20261006'/name
        sources.extend(folder.glob('*.json'));sources.extend(folder.glob('*.log'))
    assert all(isinstance(p,Path) for p in sources)
    sources=list(dict.fromkeys(p for p in sources if p.is_file()))
    pins={str(p):sha(p) for p in sources}
    out=A/'RFF128Low_actual_history_github_20261007';assert not out.exists();out.mkdir()
    create(out/'frozen_before_publication.json',{'input_sha256':pins,'actual_terminal_services':terminals,
        'actual_native_fits':10,'saved_fits_reused':saved,'new_fits_by_resume':10-saved,'actual_full_controls':73,
        'actual_cold_controls':219,'actual_native_hooks':6,'full125_main_commit':receipt['commit'],
        'elapsed_seconds_scope':native['elapsed_seconds_scope'],'remaining_training_and_controls_seconds':native['elapsed_seconds'],
        'unsaved_fit_progress_lost':0,'remote_tasks_dispatched':0,'new_quality_scores_by_publication':0,
        'global_optimization_boundaries_proven':False,'test_labels_read':False})
    held=[];restore=install();sync=helpers.sync
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v7/native_launch.json')
        parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
        with LockedReadHashCache(pins) as scope:
            prefix=Path('validation_sync/RFF128Low_actual_history_20261007')
            payload={(prefix/'.gitattributes').as_posix():b'* -text\n'};files={}
            for p in [*sources,out/'frozen_before_publication.json']:
                data=p.read_bytes();assert not sync.SECRET.search(data);raw=hashlib.sha256(data).hexdigest()
                target=(prefix/p.relative_to(ROOT)).as_posix()
                if len(data)>=5*1024**2:
                    data=gzip.compress(data,mtime=0);assert hashlib.sha256(gzip.decompress(data)).hexdigest()==raw;target+='.gz'
                payload[target]=data;files[str(p.relative_to(ROOT))]={'published_path':target,'original_sha256':raw}
            previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous);assert not sync.git('status','--porcelain')
            payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'published_actual_local_checkpoint_resume_native_controls_and125_source_history',
                'files':files,'previous_main':previous,'branch':'main','actual_native_fits':10,'saved_fits_reused':saved,
                'new_fits_by_resume':10-saved,'actual_full_controls':73,'actual_cold_controls':219,'actual_native_hooks':6,
                'failed_preparation_history_preserved':True,'new_quality_scores_by_publication':0,'test_labels_read':False})
            scope.reverify()
            for name,data in payload.items():sync.atomic(sync.WORKTREE/name,data)
            sync.git('add','-f','--',*sorted(payload))
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())<=set(payload)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','保存本机内存释放续跑和弱正则RFF128实际验证及125轮检查历史',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={k:hashlib.sha256(v).hexdigest() for k,v in payload.items()}
            assert helpers.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit);scope.reverify()
            create(out/'receipt.json',{'status':'pushed_and_remote_head_verified','branch':'main','commit':commit,
                'raw_git_blobs_verified':len(hashes),'actual_native_fits':10,'new_quality_scores_by_publication':0})
    finally:
        for p in reversed(held):
            if p.is_running():p.resume()
        create(out/'actual_hidden_publication_children.json',{'events':restore()})
if __name__=='__main__':main()
