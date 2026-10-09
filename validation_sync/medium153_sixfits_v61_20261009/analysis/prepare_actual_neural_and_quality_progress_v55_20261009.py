from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
old=A/'monitor_actual_chronological_optimization_progress_v54_20261009.py';new=A/'monitor_actual_chronological_optimization_progress_v55_20261009.py'
s=old.read_text(encoding='utf8').replace('optimization_live_progress_v54_20261009','optimization_live_progress_v55_20261009')
needle="    write(A/'optimization_live_progress_v55_20261009.json',";assert needle in s
addition="""    bank=Path('E:/赛题五_本机临时/neural_BF16_medium2048_seed09_e64_bank6_v1_20261009')
    completed=[int(p.parent.name) for p in bank.glob('*/info.json') if p.parent.name.isdecimal()]
    stage=read(bank/'actual_stage.json') if (bank/'actual_stage.json').exists() else None
    state['neural_medium_new_recipe_frontier']={'configuration':read(A/'neural_BF16_medium2048_seed09_e64_frontier_v1_20261009.json')['configuration'],
      'actual_restart_control':status('actual_BF16_medium2048_seed09_restart_control_v1_20261009'),
      'actual_annual_training':status('actual_BF16_medium2048_seed09_e64_bank6_v1_20261009'),
      'completed_mature_annual_model_years':sorted(completed),'completed_annual_models':len(completed),'expected_annual_models':6,
      'actual_training_stage':stage,'restart_controls_main_publication':status('neural_medium_restart_main_publication_v58_20261009'),
      'actual_new_quality_scores':0,'actual_future_X_read':False,'fully_qualified_not_claimed':True}
"""
s=s.replace(needle,addition+needle)
needle="    write(A/'optimization_live_progress_v55_20261009.md',text)";assert needle in s
s=s.replace(needle,"    neural=state['neural_medium_new_recipe_frontier']\n    text+=f\"\\n新中型神经网络：2048/1024/512、BF16、seed20261009、64轮固定训练；重启与权重/预测逐位核验{neural['actual_restart_control']['status']}，年度模型{neural['completed_annual_models']}/6，训练{neural['actual_annual_training']['status']}，尚无正式质量分。\\n\"\n"+needle)
compile(s,str(new),'exec')
with new.open('x',encoding='utf8') as f:f.write(s)
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
row=start('actual_chronological_optimization_progress_observer_v55_20261009',new.name,[],{str(new):sha(new)})
create(A/'actual_neural_and_quality_progress_hidden_launch_v55_20261009.json',row)
for _ in range(60):
 if (A/'optimization_live_progress_v55_20261009.json').exists():break
 time.sleep(1)
else:raise AssertionError('No first complete progress snapshot')
assert owned(row)
create(A/'latest_actual_optimization_progress_pointer_v55_20261009.json',{'status':'actual_current_progress','json':str(A/'optimization_live_progress_v55_20261009.json'),'markdown':str(A/'optimization_live_progress_v55_20261009.md'),'actual_observer':row})
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle,retire_suspended,stack
oldrow=read(A/'service_owned_workflows_20261006/actual_chronological_optimization_progress_observer_v54_20261009/native_launch.json')
if owned(oldrow):
 line=next(line for line in stack(oldrow['owned_worker_pid']).splitlines() if '    main (' in line)
 parent,worker,idle=suspended_idle(oldrow,line)
 try:retire_suspended(oldrow,row)
 except BaseException:
  if parent.is_running():parent.resume()
  if worker.is_running():worker.resume()
  raise
print(row['owned_worker_pid'],flush=True)
