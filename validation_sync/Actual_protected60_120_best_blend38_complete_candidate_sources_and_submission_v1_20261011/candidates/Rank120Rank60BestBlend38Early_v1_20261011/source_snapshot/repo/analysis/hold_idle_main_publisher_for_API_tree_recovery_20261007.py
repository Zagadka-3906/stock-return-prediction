"""Wait for a leased API ref update; preserve exact file tree while adopting verified new SHA."""
from pathlib import Path
from datetime import datetime
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
from hidden_windows_child_creation_20261006 import install
import publish_classifier_consensus_workflows_20261006 as helpers
OUT=A/'sparse_main_API_transport_recovery_20261007'

def main():
    import psutil
    p=read(OUT/'frozen_exact_API_tree_payload.json');held=[];restore=install();sync=helpers.sync
    try:
        main7=read(A/'service_owned_workflows_20261006/main_publisher_v7/native_launch.json')
        while any(psutil.Process(pid).status()==psutil.STATUS_STOPPED for pid in (main7['pid'],main7['owned_worker_pid'])):time.sleep(2)
        parent,worker,idle=suspended_idle(main7,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        assert sync.git('rev-parse','HEAD')==p['original_local_commit'] and not sync.git('status','--porcelain')
        create(OUT/'actual_idle_main_publisher_held.json',{'status':'held_only_strong_owned_idle_main_publisher_for_exact_tree_API_transport','idle':idle,'new_quality_scores':0})
        release=OUT/'actual_API_ref_update_and_release.json'
        while not release.exists():
            assert time.time()<datetime.fromisoformat('2026-10-07T23:35:00+08:00').timestamp();time.sleep(2)
        result=read(release);assert result['expected_parent']==p['expected_remote_parent'] and result['verified_tree_sha']==p['expected_tree_sha']
        commit=result['actual_API_main_commit'];sync.git('fetch','origin','main',timeout=90)
        assert sync.git('show','-s','--format=%T',commit)==p['expected_tree_sha']
        assert sync.git('rev-parse','HEAD')==p['original_local_commit'] and not sync.git('status','--porcelain')
        # Both trees are identical. Only this isolated publisher HEAD changes; all worktree bytes remain.
        sync.git('reset','--soft',commit);assert not sync.git('status','--porcelain')
        helpers.verify_main(commit);helpers.watcher.advance_source_index(commit)
        create(OUT/'receipt.json',{'status':'pushed_and_remote_head_verified','at_local':sync.now(),'commit':commit,'branch':'main',
          'exact_original_tree_sha':p['expected_tree_sha'],'all_file_bytes_preserved':True,'original_unpublished_commit_retained_in_local_reflog':p['original_local_commit'],
          'API_main_update_used_expected_parent_lease_and_no_force':True,'new_quality_scores':0,'new_native_fits':0})
    finally:
        for process in reversed(held):
            if process.is_running():process.resume()
        create(OUT/'actual_hidden_main_recovery_children.json',{'events':restore()})

if __name__=='__main__':main()
