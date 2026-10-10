"""Revalidate and finish the existing exact scientific commit without repeating tests."""
from pathlib import Path
from datetime import datetime
import sys,time,json,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
from hidden_windows_child_creation_20261006 import install
import publish_classifier_consensus_workflows_20261006 as helpers
COMMIT='04c65d0c967c206575a5b4b72dd194e1a3eb45c5'
PREFIX='validation_sync/actual_sparse_and_isolated_scoring_controls_20261007'
OUT=A/'actual_sparse_and_isolated_scoring_controls_github_recovery_v5_20261007'

def main():
    import psutil
    assert not OUT.exists();OUT.mkdir();sync=helpers.sync;original_git=sync.git;attempts=[]
    def retry(*args,**kwargs):
        for trial in range(5):
            try:return original_git(*args,**kwargs)
            except RuntimeError as error:
                if args[0] not in ('ls-remote','push','fetch') or not any(word in str(error).lower() for word in ('tls','ssl','unable to access','connection','timed out','internal server error','http 500','http 502','http 503')):raise
                attempts.append({'command':args[0],'attempt':trial+1,'error':str(error)[:1400]})
                if trial==4:raise
                time.sleep([3,8,15,25][trial])
    held=[];restore=install();sync.git=retry
    try:
        main7=read(A/'service_owned_workflows_20261006/main_publisher_v7/native_launch.json')
        while any(psutil.Process(pid).status()==psutil.STATUS_STOPPED for pid in (main7['pid'],main7['owned_worker_pid'])):
            assert time.time()<datetime.fromisoformat('2026-10-07T23:35:00+08:00').timestamp();time.sleep(5)
        parent,worker,idle=suspended_idle(main7,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        assert sync.git('rev-parse','HEAD')==COMMIT and not sync.git('status','--porcelain')
        manifest=json.loads(sync.git('show',COMMIT+':'+PREFIX+'/manifest.json'))
        assert manifest['status']=='published_actual_sparse10_and_isolated_parallel4_serial4_controls'
        expected={}
        for name,entry in manifest['files'].items():
            path=ROOT/name;assert sha(path)==entry['sha256'],path
            expected[entry['published_path']]=entry['sha256']
        expected[PREFIX+'/.gitattributes']=hashlib.sha256(b'* -text\n').hexdigest()
        assert helpers.blob_hashes(COMMIT,expected)==expected
        source=A/'service_owned_workflows_20261006/actual_sparse_and_isolated_scoring_controls_main_publication_v3'
        assert not owned(read(source/'native_launch.json')) and read(source/'service_execution.json')['status']=='failed'
        create(OUT/'frozen_before_actual_committed_main_recovery.json',{'commit':COMMIT,'original_manifest':manifest,
          'input_sha256':{str(p):sha(p) for p in [Path(__file__),*source.glob('*.json'),*source.glob('*.log')]},
          'main7_actual_idle_hold':idle,'original_failed_execution_status_retained':True,'existing_local_commit_and_all_original_source_blobs_reverified':True})
        sync.git('-c','http.version=HTTP/1.1','push','--no-thin','origin','HEAD:refs/heads/main',timeout=90)
        helpers.verify_main(COMMIT);assert helpers.blob_hashes(COMMIT,expected)==expected
        helpers.watcher.advance_source_index(COMMIT)
        create(OUT/'receipt.json',{'status':'pushed_and_remote_head_verified','at_local':sync.now(),'commit':COMMIT,'branch':'main',
          'original_source_git_blobs_reverified':len(expected),'existing_commit_recovered_without_science_reexecution':True,
          'original_failed_service_execution_not_rewritten':True,'new_quality_scores':0,'new_native_fits':0,'TLS_verification_not_disabled':True})
        print('PASS exact sparse/parallel scientific commit recovered on remote main',flush=True)
    finally:
        sync.git=original_git
        for process in reversed(held):
            if process.is_running():process.resume()
        create(OUT/'actual_server_and_TLS_transport_retries.json',{'attempts':attempts,'TLS_verification_not_disabled':True})
        create(OUT/'actual_hidden_recovery_children.json',{'events':restore()})

if __name__=='__main__':main()
