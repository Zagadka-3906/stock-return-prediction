"""Verify the actual persistent idle waiter and unchanged live scientific identities."""
from pathlib import Path
import json
import sys
import time

import psutil

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
OUT=A/'joint_goss_round97_idle_waiter_launch_control_20261006'

def main():
    assert not OUT.exists();OUT.mkdir()
    launch=A/'service_owned_workflows_20261006/joint_goss_round97_idle_handoff_waiter/native_launch.json'
    row=read(launch)
    queue=read(A/'service_owned_workflows_20261006/dependency_queue_v7/native_launch.json')
    scientific=[read(A/'service_owned_dependency_queue_v4_20261006/activated_jobs/round95/launch.json'),
        read(A/'service_owned_workflows_20261006/neural16384_annual/native_launch.json')]
    assert owned(row) and owned(queue) and all(owned(r) for r in scientific)
    assert row['actual_native_console_handle']==0 and not row['independent_launch_root_in_any_job']
    worker=psutil.Process(row['owned_worker_pid'])
    assert str(Path(read(row['script_args'][0])['scratch'])).startswith(str(ROOT/'tmp'))
    state=read(A/'joint_goss_round97_idle_handoff_waiter_20261006/state.json')
    assert state['pid']==worker.pid and state['status']=='waiting_for_owned_original_queue_scientific_children_natural_completion'
    assert scientific[0]['pid'] in state['actual_original_child_pids']
    sources=[Path(__file__),launch,Path(row['script_args'][0]),
        A/'service_owned_workflows_20261006/joint_goss_round97_idle_handoff_waiter/verified_hidden_launch.json',
        A/'joint_goss_round97_idle_handoff_waiter_20261006/frozen_before_waiting.json',
        A/'wait_joint_goss_round97_idle_handoff_20261006.py',
        A/'handoff_joint_goss_round97_full_execution_20261006.py',
        A/'optimization_20261003_r95/protocol.json',
        A/'joint_goss_round97_prospective_github_20261006/receipt.json']
    pins={str(p):sha(p) for p in sources}
    create(OUT/'verification.json',{'status':'passed_actual_owned_consoleless_persistent_waiter_and_preserved_live_R95_and_neural',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,
        'actual_waiter':row,'actual_RSS_bytes':worker.memory_info().rss,
        'actual_original_queue':queue,'original_child_pids':state['actual_original_child_pids'],
        'preserved_live_scientific_workers':scientific,
        'actual_original_children_still_running_not_restarted':True,
        'waiter_requires_empty_original_children_and_twice_verified_idle_stack':True,
        'actual_handoff_not_yet_performed':True,'new_native_fits':0,'new_quality_scores':0,
        'test_labels_read':False,'scientific_workers_stopped_or_restarted':0})
    assert owned(row) and owned(queue) and all(owned(r) for r in scientific)
    print('passed_actual_consoleless_persistent_waiter_original_children_untouched',flush=True)

if __name__=='__main__':main()
