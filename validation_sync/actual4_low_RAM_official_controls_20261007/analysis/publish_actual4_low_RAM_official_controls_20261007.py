"""Archive measured full official controls and the user's app constraint, without publishing training data."""
from pathlib import Path
import sys,gzip,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
from hidden_windows_child_creation_20261006 import install
import publish_classifier_consensus_workflows_20261006 as helpers

def main():
    service=A/'service_owned_workflows_20261006/actual4_official_scoring_8_5GiB_start_gate'
    assert not owned(read(service/'native_launch.json')) and read(service/'service_execution.json')['status']=='passed'
    folder=A/'actual4_official_scoring_8_5GiB_gate_preflight_20261007'
    proofpath=folder/'verification.json';proof=read(proofpath)
    assert proof['status']=='passed_actual4_uncached_full_official_calls_at_8_5GiB_start_gate_all8_and_CSV_and_input_bits_exact'
    assert proof['actual_uncached_official_calls']==len(proof['records'])==4
    out=A/'actual4_low_RAM_official_controls_github_20261007';assert not out.exists();out.mkdir()
    decision=out/'actual_user_constraint.json'
    create(decision,{'actual_user_reply':'这些应用必须保持运行','qemu_and_Java_applications_must_remain_running':True,
        'user_applications_stopped':0,'original_GPU_current_unsaved_fit_cancellation_still_not_authorized':True,
        'original_LOW126_11GiB_gate_retained_and_current_scoring_started_after_RAM_recovered':True,
        'actual8_5GiB_gate_controls_are_not_a_changed_LOW126_recipe_or_full_goal_speedup':True})
    sources=[Path(__file__),A/'verify_actual4_official_scoring_under_8_5GiB_gate_20261007.py',decision,
        *folder.glob('*.json'),*service.glob('*.json'),*service.glob('*.log'),
        A/'nonflag_RFF128Low76_recovered6_complete_pipeline_actual_hidden_launches_20261007.json',
        A/'nonflag_RFF128Low126_execution_gate_recovery_admission_20261007.json']
    sources=list(dict.fromkeys(sources));assert all(p.is_file() for p in sources)
    pins={**proof['input_sha256'],**{str(p):sha(p) for p in sources}}
    create(out/'frozen_before_publication.json',{'input_sha256':pins,'actual_uncached_official_calls':4,
        'test_labels_read':False,'new_distinct_quality_scores':0})
    held=[];restore=install();sync=helpers.sync
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v7/native_launch.json')
        parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
        with LockedReadHashCache(pins) as scope:
            prefix=Path('validation_sync/actual4_low_RAM_official_controls_20261007')
            payload={(prefix/'.gitattributes').as_posix():b'* -text\n'};files={}
            for p in [*sources,out/'frozen_before_publication.json']:
                data=p.read_bytes();assert not sync.SECRET.search(data);raw=hashlib.sha256(data).hexdigest()
                target=(prefix/p.relative_to(ROOT)).as_posix()
                if len(data)>=5*1024**2:data=gzip.compress(data,mtime=0);target+='.gz'
                payload[target]=data;files[str(p.relative_to(ROOT))]={'published_path':target,'original_sha256':raw}
            previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous);assert not sync.git('status','--porcelain')
            payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'published_actual4_full_official_low_RAM_controls_all8_CSV_and_prediction_bits_exact',
                'files':files,'branch':'main','previous_main':previous,'actual_uncached_official_calls':4,
                'minimum_sampled_available_RAM_GiB':proof['minimum_sampled_available_RAM_GiB'],
                'peak_sampled_own_RSS_GiB':proof['peak_sampled_own_RSS_GiB'],
                'user_applications_stopped':0,'new_distinct_quality_scores':0,'new_native_fits':0,'test_labels_read':False})
            scope.reverify()
            for name,data in payload.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(payload)
            for left in range(0,len(names),50):sync.git('add','-f','--',*names[left:left+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())<=set(payload)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','保存保留模拟器与Java应用时的4次全量低内存官方评分核对',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={k:hashlib.sha256(v).hexdigest() for k,v in payload.items()}
            assert helpers.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit);scope.reverify()
            create(out/'receipt.json',{'status':'pushed_and_remote_head_verified','branch':'main','commit':commit,
                'raw_git_blobs_verified':len(hashes),'actual_uncached_official_calls':4,'new_distinct_quality_scores':0})
    finally:
        for p in reversed(held):
            if p.is_running():p.resume()
        create(out/'actual_hidden_publication_children.json',{'events':restore()})
if __name__=='__main__':main()
