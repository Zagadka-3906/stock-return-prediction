"""Replace only the exact idle11:00 guardian after the explicit13:00 extension."""
from pathlib import Path
from datetime import datetime
import sys,subprocess,psutil
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from scheduled_user_pause_20261007 import write
from start_fast_completed_owned_service_v1_20261011 import start_service
from handoff_ready_goss_full_execution_20261006 import retire
def main():
 controls={n:read(A/n) for n in ('current_user_runtime_control_20261010.json','current_user_runtime_control_20261009.json','current_user_runtime_control_20261008.json')}
 now=datetime.now().astimezone();deadline='2026-10-11T13:00:00+08:00';assert now<datetime.fromisoformat(deadline)
 oldfolder=A/'user_requested_stop1100_reboot_guard_v2_20261011';oldrow=read(A/'service_owned_workflows_20261006/actual_user_stop1100_reboot_guard_v2_20261011/native_launch.json')
 folder=A/'user_requested_stop1300_until_manual_continue_v1_20261011';assert not folder.exists();folder.mkdir()
 source=A/'user_requested_stop1100_v1_20261011.py';driver=A/'user_requested_stop1300_v1_20261011.py';assert not driver.exists()
 text=source.read_text(encoding='utf8').replace('10月11日上午11点','10月11日13点');compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
 create(folder/'previous_runtime_controls_and_guard.json',{'controls':controls,'old_guard':oldrow,'old_schedule':read(oldfolder/'schedule.json'),'at_local':now.isoformat()})
 create(folder/'schedule.json',{'output_folder':str(folder),'stop_at_local':deadline,'automatic_restart_enabled':False,'execute_Windows_shutdown':False,'actual_user_instruction':'截止时间更改为13点，在这之前最大可能的提分','supersedes_previous_1100_stop':True})
 for n,c in controls.items():
  c.update(at_local=now.isoformat(),actual_user_instruction='截止时间更改为13点，在这之前最大可能的提分',stop_at_local=deadline,optimization_deadline_local=deadline,schedule=str(folder/'schedule.json'),activation=str(folder/'actual_schedule_activation.json'),guard_status=str(folder/'guardian_status.json'),disk_recovery_manifest=str(folder/'disk_recovery_manifest.json'),expired_1100_schedule_superseded=True,immediate_pause=False,goal_pause_required_now=False,status='optimization_active_after_explicit_manual_resume')
  write(A/n,c)
 row=start_service('actual_user_stop1300_guard_v1_20261011',driver.name,['run','--folder',str(folder)],{str(driver):sha(driver),str(folder/'schedule.json'):sha(folder/'schedule.json')})
 create(folder/'actual_schedule_activation.json',{'status':'actual_owned_1300_guard_started_after_explicit_deadline_extension','identity':row,'stop_at_local':deadline,'old_guards_not_restarted':True,'execute_Windows_shutdown':False})
 create(folder/'handoff_committed.json',{'status':'actual_user13_deadline_controls_and_owned_guard_committed','at_local':datetime.now().astimezone().isoformat(),'old_guard_will_be_retired':oldrow,'scientific_workers_not_restarted_or_stopped':True})
 stack=None
 if owned(oldrow):
  p=psutil.Process(oldrow['owned_worker_pid']);assert not p.children();stack=subprocess.run([str(ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(p.pid)],capture_output=True,text=True,timeout=30).stdout
  assert 'run (user_requested_stop2355_v2_20261008.py:' in stack,stack
  retire(oldrow,'User explicitly extended optimization deadline to13:00; replace only the verified idle11:00 guardian, preserve all scientific tasks')
 create(folder/'actual_1100_guard_retirement.json',{'status':'old11_guard_exact_identity_retired_for_explicit13_extension','identity':oldrow,'actual_idle_stack':stack,'scientific_workers_stopped':0,'new_training_runs':0})
 agents=ROOT/'AGENTS.md';history=agents.read_text(encoding='utf8')
 head='# 最新用户指令（2026-10-11，延长至13:00）\n\n用户明确将模型优化截止时间更改为 **2026-10-11 13:00（Asia/Taipei，UTC+08:00）**，在此之前尽最大可能提分。此前11:00与历史23:55停工安排已被取代。每轮及启动训练、评分、推理、发布前读取10、09控制文件及本机时间。实际新守护记录为 `analysis/user_requested_stop1300_until_manual_continue_v1_20261011/actual_schedule_activation.json`；旧11:00守护已按身份替换，禁止重启。保持目标active；13:00停止项目任务、保存恢复清单，再按用户截止请求暂停目标。继续复用年度模型、已完成epoch与评分缓存，未完成训练、评分或提交资格不得记为完成。\n\n# 历史指令记录（后续明确用户指令优先）\n\n'
 agents.write_text(head+history,encoding='utf8',newline='\n')
 create(folder/'deadline_extension_verification.json',{'status':'passed_actual_three_controls13_new_owned_guard_and_old11_retirement','at_local':datetime.now().astimezone().isoformat(),'stop_at_local':deadline,'new_guard_identity':row,'old_guard_still_owned':owned(oldrow),'AGENTS_sha256':sha(agents),'goal_active_not_early_paused':True,'scientific_workers_stopped_or_restarted':0})
 assert not owned(oldrow)
 print({'actual_stop_at_local':deadline,'old_1100_guard_retired':True,'science_preserved':True},flush=True)
if __name__=='__main__':main()
