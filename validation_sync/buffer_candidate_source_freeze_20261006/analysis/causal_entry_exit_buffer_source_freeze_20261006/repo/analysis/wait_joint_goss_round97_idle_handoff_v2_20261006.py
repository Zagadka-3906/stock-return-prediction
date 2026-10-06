"""Wait for original queue children to finish naturally before additive adoption."""
from pathlib import Path
import json
import runpy
import sys
import time

import psutil

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from atomic_optimization_observer_writes_20261005 import write
from handoff_joint_goss_round97_full_execution_20261006 import pair,stack

OUT=A/'joint_goss_round97_idle_handoff_waiter_v2_20261006'

def main():
    assert not OUT.exists();OUT.mkdir()
    queue=read(A/'service_owned_workflows_20261006/dependency_queue_v7/native_launch.json')
    source=A/'handoff_joint_goss_round97_full_execution_v2_20261006.py'
    proof=A/'joint_goss_round97_queue_preparation_20261006/verification.json'
    receipt=A/'joint_goss_round97_prospective_github_20261006/receipt.json'
    assert owned(queue)
    pins={str(p):sha(p) for p in (Path(__file__),source,proof,receipt,A/'recover_joint97_handoff_sources_v2_20261006.py',
        A/'interrupted_round95_lossless_snapshot_recovery_20261006/verification.json')}
    create(OUT/'frozen_before_waiting.json',{'status':'frozen_before_original_children_natural_exit_wait',
        'input_sha256':pins,'original_queue_identity':queue,
        'no_live_scientific_process_will_be_terminated_or_restarted':True,
        'wait_requires_actual_empty_child_tree_and_verified_idle_stack':True,
        'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    suspended=[]
    try:
        while True:
            parent,worker=pair(queue)
            children=worker.children(recursive=True)
            if children:
                write(OUT/'state.json',{'status':'waiting_for_owned_original_queue_scientific_children_natural_completion',
                    'pid':psutil.Process().pid,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
                    'owned_original_queue_live':True,'actual_original_child_pids':[p.pid for p in children],
                    'scientific_children_not_suspended_or_stopped':True,'new_quality_scores':0,'test_labels_read':False})
                time.sleep(1)
                continue
            before=stack(worker.pid)
            needle='    main (run_dependency_queue_v3_20261006.py:141)'
            if needle not in before:
                time.sleep(1);continue
            worker.suspend();parent.suspend();suspended=[worker,parent]
            after=stack(worker.pid)
            if worker.children() or needle not in after:
                for p in reversed(suspended):p.resume()
                suspended=[];time.sleep(1);continue
            create(OUT/'actual_empty_children_idle_boundary.json',{'status':'passed_actual_original_queue_child_tree_empty_and_idle_before_and_after_hold',
                'original_queue_identity':queue,'before':before,'after':after,
                'only_original_empty_queue_helper_processes_held':True,'scientific_children_held':0})
            for p,digest in pins.items():assert sha(p)==digest,p
            runpy.run_path(str(source),run_name='__main__')
            assert not owned(queue),'Old controller must have been retired by successful handoff'
            suspended=[]
            import publish_joint_goss_round97_progress_20261006 as publisher
            publisher.main('actual')
            write(OUT/'state.json',{'status':'completed_actual_additive_handoff_and_main_publication',
                'pid':psutil.Process().pid,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
                'actual_handoff':str(A/'joint_goss_round97_actual_handoff_20261006/verification.json'),
                'actual_main_receipt':str(A/'joint_goss_round97_actual_github_20261006/receipt.json'),
                'new_native_fits':0,'new_quality_scores':0,'scientific_workers_stopped_or_restarted':0,'test_labels_read':False})
            return
    finally:
        for p in reversed(suspended):
            try:
                if p.is_running():p.resume()
            except psutil.NoSuchProcess:pass

if __name__=='__main__':
    try:main()
    except BaseException as exc:
        if OUT.exists() and not (OUT/'failure.json').exists():create(OUT/'failure.json',{'status':'failed_preserved_original_children_wait_and_handoff','error':f'{type(exc).__name__}: {exc}'})
        raise
