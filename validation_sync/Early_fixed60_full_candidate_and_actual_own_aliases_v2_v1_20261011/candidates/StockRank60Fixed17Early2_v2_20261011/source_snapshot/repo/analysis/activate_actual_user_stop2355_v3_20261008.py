"""Schedule tonight's explicit stop while optimization remains active until the deadline."""
from pathlib import Path
from datetime import datetime
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from scheduled_user_pause_20261007 import identity,exact,write
def main():
 deadline=datetime.fromisoformat('2026-10-08T23:55:00+08:00');assert datetime.now().astimezone()<deadline
 module=A/'user_requested_stop2355_v2_20261008.py'
 proofs=[A/'shutdown_ready_stop_preflight_late_quiesce2355_20261008/verification.json',A/'shutdown_ready_stop_preflight_late_quiesce2355_preheld_20261008/verification.json']
 for p in proofs:
  v=read(p);assert v['status'] in ('passed_actual_hidden_deadline_stop_exact_probe_identities_and_durable_recovery_record','passed_actual_hidden_deadline_stop_preheld_probe_and_durable_recovery_record')
  assert v['module_sha256']==sha(module) and v['scientific_workers_terminated']==0 and not v['automatic_restart_enabled']
 folder=A/'user_requested_stop2355_until_manual_continue_v2_20261008';assert not folder.exists();folder.mkdir()
 create(folder/'schedule.json',{'actual_latest_user_instruction':'23:55停止工作','stop_at_local':deadline.isoformat(),'quiesce_at_local':'2026-10-08T23:53:00+08:00','timezone':'Asia/Taipei','output_folder':str(folder),'automatic_restart_enabled':False,'execute_Windows_shutdown':False,'resume_policy':'only_after_actual_user_continue','goal_and_current_scientific_work_remain_active_until_actual2355_stop':True,'all_completed_scores_candidates_main_receipts_and_previous_submission_deliveries_preserved':True,'interrupted_steps_require_checked_new_attempts_not_false_completion':True})
 create(folder/'handoff_committed.json',{'status':'actual_user2355_stop_schedule_committed_without_stopping_current_optimization','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'scientific_workers_stopped_now':0})
 pins={str(p):sha(p) for p in [Path(__file__),module,A/'shutdown_ready_stop_v2_20261007.py',A/'scheduled_user_pause_20261007.py',*proofs,folder/'schedule.json',folder/'handoff_committed.json']}
 from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
 row=start('actual_user_stop2355_wait_manual_continue_v3_20261008',module.name,['run','--folder',str(folder)],pins)
 until=time.monotonic()+20
 while not (folder/'guardian_status.json').is_file():
  assert owned(row) and time.monotonic()<until;time.sleep(.1)
 state=read(folder/'guardian_status.json');assert state['status']=='scheduled_shutdown_compatible_stop' and state['suspended_entries']==0
 assert state['guardian']['pid']==row['owned_worker_pid'] and exact(state['guardian']) is not None
 assert row['actual_native_console_handle']==0
 create(folder/'actual_schedule_activation.json',{'status':'passed_actual_hidden2355_stop_guardian_running_after_two_isolated_deadline_tests','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'guardian_launch':row,'actual_initial_guardian_state':state,'input_sha256':pins,'real2355_stop_not_yet_executed':True,'goal_not_paused_early':True,'current_scientific_workers_stopped':0,'automatic_restart_enabled':False,'test_labels_read':False})
 write(A/'current_user_runtime_control_20261008.json',{'status':'optimization_active_until_actual_user_requested2355_stop','actual_user_instruction':'23:55停止工作','stop_at_local':deadline.isoformat(),'schedule':str(folder/'schedule.json'),'activation':str(folder/'actual_schedule_activation.json'),'guard_status':str(folder/'guardian_status.json'),'disk_recovery_manifest_expected_after_stop':str(folder/'disk_recovery_manifest.json'),'resume_only_after_actual_user_continue':True,'pause_goal_only_when_deadline_has_arrived':True,'automatic_restart_enabled':False})
 old_folder=A/'user_requested_stop2355_until_manual_continue_20261008'
 old_state=read(old_folder/'guardian_status.json');assert old_state['suspended_entries']==0
 old=read(A/'service_owned_workflows_20261006/actual_user_stop2355_wait_manual_continue_v2_20261008/native_launch.json')
 assert owned(old) and state['stop_at_local']==old_state['stop_at_local']
 from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
 parent,worker,idle=suspended_idle(old,'    run (user_requested_stop2355_v1_20261008.py:')
 assert not worker.children() and owned(row)
 worker.terminate();worker.wait(timeout=10);parent.terminate();parent.wait(timeout=10)
 create(folder/'old_guard_retired_after_new_live_verified.json',{'status':'retired_only_old_idle_stop_guard_after_live_same_deadline_replacement','old_launch':old,'idle_stack':idle,'new_guard':row,'old_suspended_entries':0,'current_scientific_workers_stopped':0,'stop_at_local_preserved':'2026-10-08T23:55:00+08:00','quiet_publisher_quiesce_at_local':'2026-10-08T23:53:00+08:00'})
 print({'actual_guard_worker':row['owned_worker_pid'],'stop_at_local':deadline.isoformat(),'current_optimization_remains_active':True},flush=True)
if __name__=='__main__':main()
