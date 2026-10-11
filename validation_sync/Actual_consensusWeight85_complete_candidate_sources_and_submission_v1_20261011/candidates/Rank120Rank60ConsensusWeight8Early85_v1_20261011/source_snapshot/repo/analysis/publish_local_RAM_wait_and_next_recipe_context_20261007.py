"""Publish actual preparation and resource evidence; all argument batches are bounded."""
from pathlib import Path
import sys,gzip,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
from hidden_windows_child_creation_20261006 import install
import publish_classifier_consensus_workflows_20261006 as helpers

def main():
    proofpath=A/'local_RAM_wait_and_next_native_recipe_context_20261007.json';proof=read(proofpath)
    assert proof['status']=='recorded_actual_single_host_RAM_gates_and2_stronger_L2_diagnostic_fits'
    sources=[Path(__file__),proofpath,*[Path(p) for p in proof['input_sha256']]]
    for pattern in ('*RFF128Hi*20261007.py','*RFF128Hi*20261007.json',
        '*RFF128Low126*20261007.py','*RFF128Low126*20261007.json','*RFF128Low76*20261007.py','*RFF128Low76*20261007.json'):
        sources.extend(A.glob(pattern))
    sources.extend((A/'nonflag_residual_RFF128Hi_codec2_preflight_20261007').glob('*.json'))
    for name in ('nonflag_RFF128Low76_full37_controls_main_publication_v1','nonflag_RFF128Low76_full73_controls_main_publication_v2',
        'nonflag_RFF128Low126_continue_after_recovered_history','nonflag_RFF128Low76_round126_source_admission_v1',
        'RFF128Low_history_batched_main_recovery'):
        folder=A/'service_owned_workflows_20261006'/name;assert not owned(read(folder/'native_launch.json'))
        sources.extend(folder.glob('*.json'));sources.extend(folder.glob('*.log'))
    for folder in (A/'RFF128Low126_after_history_recovery_source_preparation_20261007',):
        sources.extend(p for p in folder.glob('*') if p.is_file())
    sources=list(dict.fromkeys(sources));assert all(isinstance(p,Path) and p.is_file() for p in sources)
    pins={**proof['input_sha256'],**{str(p):sha(p) for p in sources}}
    out=A/'local_RAM_wait_next_recipe_github_20261007';assert not out.exists();out.mkdir()
    create(out/'frozen_before_publication.json',{'input_sha256':pins,'all_counts_are_the_recorded_observation_not_live_progress':True,
        'new_scientific_scores_by_publication':0,'test_labels_read':False})
    held=[];restore=install();sync=helpers.sync
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v7/native_launch.json')
        parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
        with LockedReadHashCache(pins) as scope:
            prefix=Path('validation_sync/local_RAM_wait_next_recipe_20261007')
            payload={(prefix/'.gitattributes').as_posix():b'* -text\n'};files={}
            for p in [*sources,out/'frozen_before_publication.json']:
                data=p.read_bytes();assert not sync.SECRET.search(data);raw=hashlib.sha256(data).hexdigest()
                target=(prefix/p.relative_to(ROOT)).as_posix()
                if len(data)>=5*1024**2:data=gzip.compress(data,mtime=0);target+='.gz'
                payload[target]=data;files[str(p.relative_to(ROOT))]={'published_path':target,'original_sha256':raw}
            previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous);assert not sync.git('status','--porcelain')
            payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'published_actual_RAM_wait_and_stronger_L2_diagnostics_before_selection',
                'files':files,'branch':'main','previous_main':previous,'actual_Hi_diagnostic_fits':2,
                'actual_Hi_native_fits_at_observation':proof['actual_Hi_annual_native_fits'],
                'actual_LOW_official_scores_at_observation':proof['actual_LOW76_completed_official_scores'],
                'real_zero_score_publication_failures_and_successful_recovery_preserved':True,
                'complete126_or127_qualification_not_claimed':True,'new_scientific_scores_by_publication':0,'test_labels_read':False})
            scope.reverify()
            for name,data in payload.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(payload)
            for left in range(0,len(names),50):sync.git('add','-f','--',*names[left:left+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())<=set(payload)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','保存本机内存等待、强正则RFF128解码试验和126轮评分前恢复证据',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={k:hashlib.sha256(v).hexdigest() for k,v in payload.items()}
            assert helpers.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit);scope.reverify()
            create(out/'receipt.json',{'status':'pushed_and_remote_head_verified','branch':'main','commit':commit,
                'raw_git_blobs_verified':len(hashes),'new_scientific_scores_by_publication':0})
    finally:
        for p in reversed(held):
            if p.is_running():p.resume()
        create(out/'actual_hidden_publication_children.json',{'events':restore()})
if __name__=='__main__':main()
