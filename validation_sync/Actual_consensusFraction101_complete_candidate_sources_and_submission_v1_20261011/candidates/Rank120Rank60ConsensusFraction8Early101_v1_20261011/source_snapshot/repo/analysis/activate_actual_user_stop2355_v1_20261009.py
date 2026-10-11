"""Activate the user's October9 stop without pausing current optimization early."""
from pathlib import Path
from datetime import datetime
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from scheduled_user_pause_20261007 import exact,write
def main():
    deadline=datetime.fromisoformat('2026-10-09T23:55:00+08:00');assert datetime.now().astimezone()<deadline
    module=A/'user_requested_stop2355_v1_20261009.py'
    proofs=[A/'shutdown_ready_stop_preflight_current2355_20261009/verification.json',A/'shutdown_ready_stop_preflight_current2355_preheld_20261009/verification.json']
    for p in proofs:
        v=read(p);assert v['only_isolated_probe_terminated'] and v['scientific_workers_terminated']==0
        assert v['module_sha256']==sha(module) and not v['automatic_restart_enabled']
    folder=A/'user_requested_stop2355_until_manual_continue_v1_20261009';folder.mkdir(exist_ok=False)
    create(folder/'schedule.json',{'actual_latest_user_instruction':'23:55停止工作','stop_at_local':deadline.isoformat(),
        'quiesce_at_local':'2026-10-09T23:53:00+08:00','timezone':'Asia/Taipei','output_folder':str(folder),
        'automatic_restart_enabled':False,'execute_Windows_shutdown':False,'resume_policy':'only_after_actual_user_continue',
        'goal_and_current_scientific_work_remain_active_until_actual2355_stop':True,
        'all_completed_scores_candidates_main_receipts_and_submission_deliveries_preserved':True})
    create(folder/'handoff_committed.json',{'status':'explicit_October9_deadline_committed_without_stopping_optimization','at_local':datetime.now().astimezone().isoformat(),'scientific_workers_stopped_now':0})
    pins={str(p):sha(p) for p in [Path(__file__),module,A/'user_requested_stop2355_v2_20261008.py',
        A/'shutdown_ready_stop_v2_20261007.py',A/'scheduled_user_pause_20261007.py',*proofs,folder/'schedule.json',folder/'handoff_committed.json']}
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    row=start('actual_user_stop2355_wait_manual_continue_v1_20261009',module.name,['run','--folder',str(folder)],pins)
    limit=time.monotonic()+20
    while not (folder/'guardian_status.json').is_file():assert owned(row) and time.monotonic()<limit;time.sleep(.1)
    state=read(folder/'guardian_status.json');assert state['status']=='scheduled_shutdown_compatible_stop' and state['suspended_entries']==0
    assert state['guardian']['pid']==row['owned_worker_pid'] and exact(state['guardian']) is not None and row['actual_native_console_handle']==0
    create(folder/'actual_schedule_activation.json',{'status':'passed_actual_hidden_October9_2355_stop_after_two_isolated_tests','guardian_launch':row,'actual_initial_guardian_state':state,'input_sha256':pins,'current_scientific_workers_stopped':0,'goal_not_paused_early':True})
    previous=read(A/'current_user_runtime_control_20261008.json');create(folder/'previous_runtime_control.json',previous)
    control={'status':'optimization_active_until_actual_user_requested2355_stop','at_local':datetime.now().astimezone().isoformat(),
        'actual_user_instruction':'23:55停止工作','stop_at_local':deadline.isoformat(),'schedule':str(folder/'schedule.json'),
        'activation':str(folder/'actual_schedule_activation.json'),'guard_status':str(folder/'guardian_status.json'),
        'previous_stop_guard_status':previous.get('previous_stop_guard_status',str(A/'user_requested_stop2355_until_manual_continue_v2_20261008/guardian_status.json')),
        'disk_recovery_manifest_expected_after_stop':str(folder/'disk_recovery_manifest.json'),
        'resume_only_after_actual_user_continue':True,'pause_goal_only_when_deadline_has_arrived':True,'automatic_restart_enabled':False}
    write(A/'current_user_runtime_control_20261009.json',control);write(A/'current_user_runtime_control_20261008.json',control)
    print({'actual_guard_worker':row['owned_worker_pid'],'stop_at_local':deadline.isoformat(),'current_optimization_remains_active':True},flush=True)
if __name__=='__main__':main()
