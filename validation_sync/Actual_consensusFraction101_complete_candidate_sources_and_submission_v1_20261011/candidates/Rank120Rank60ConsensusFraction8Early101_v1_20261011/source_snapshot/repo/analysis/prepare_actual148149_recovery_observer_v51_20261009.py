"""Show actual recovered service identities instead of failed historical attempts."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def main():
 old=A/'monitor_actual_chronological_optimization_progress_v50_20261009.py'
 new=A/'monitor_actual_chronological_optimization_progress_v51_20261009.py'
 s=old.read_text(encoding='utf8').replace('optimization_live_progress_v50_','optimization_live_progress_v51_')
 needle="        if (folder/'verification.json').exists():"
 assert s.count(needle)==1
 insertion="""        if number==148:
            row['selected_candidate']=status('AdaptiveJointCrossHuber242_selected_candidate_preparation_v2_20261009')
            row['candidate_sealing']=status('AdaptiveJointCrossHuber242_selected_candidate_sealing_v2_20261009')
            row['full_registration']=status('AdaptiveJointCrossHuber242_round148_full_registration_v2_20261009')
            row['original_failed_entry_preserved']=status('AdaptiveJointCrossHuber242_selected_candidate_preparation_v1_20261008')
"""
 s=s.replace(needle,insertion+needle)
 for k,v in {
  'PureRFFHuber80_native_historical_calendar_controls_v3_20261009':'PureRFFHuber80_native_historical_calendar_controls_v4_20261009',
  'PureRFFHuber124_actual_full_historical_controls_v3_20261009':'PureRFFHuber124_actual_full_historical_controls_v4_20261009',
  'Pure149_prior_complete_forecast_duplicate_audit_v2_20261009':'Pure149_prior_complete_forecast_duplicate_audit_v3_20261009',
  'PureRFFHuber149_complete_chronological_dispatch_v5_20261009':'PureRFFHuber149_complete_chronological_dispatch_v6_20261009'}.items():s=s.replace(k,v)
 compile(s,str(new),'exec')
 with new.open('x',encoding='utf8') as f:f.write(s)
 meta=A/'actual148149_recovery_observer_preparation_v51_20261009.json'
 pins={str(p):sha(p) for p in [Path(__file__),old,new,A/'Adaptive148_candidate_entry_recovery_v6_20261009.json',A/'Pure149_actual148_gate_recovery_v7_20261009.json']}
 create(meta,{'status':'prepared_actual_current148_retry2_and149_current_gates_observer',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'no_scientific_changes':True})
 from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
 row=start('actual_chronological_optimization_progress_observer_v51_20261009',new.name,[],{**pins,str(meta):sha(meta)})
 create(A/'actual148149_recovery_observer_hidden_launch_v51_20261009.json',row)
 for _ in range(30):
  if (A/'optimization_live_progress_v51_20261009.json').exists():break
  time.sleep(1)
 else:raise RuntimeError('New51 observer failed to publish actual progress')
 assert owned(row)
 previous=read(A/'service_owned_workflows_20261006/actual_chronological_optimization_progress_observer_v50_20261009/native_launch.json')
 from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle,retire_suspended
 line=next(i for i,l in enumerate(old.read_text(encoding='utf8').splitlines(),1) if l.strip()=='time.sleep(45)')
 parent,worker,idle=suspended_idle(previous,'    main ('+old.name+':'+str(line)+')')
 retire_suspended(previous,row)
 create(A/'actual_old_progress50_retired_after51_v1_20261009.json',{
  'status':'retired_only_owned_childfree_idle_observer_after_current51_output',
  'identity':previous,'idle':idle,'successor':row,'scientific_workers_stopped':0})
 create(A/'latest_actual_optimization_progress_pointer_v51_20261009.json',{
  'status':'actual_current_progress','json':str(A/'optimization_live_progress_v51_20261009.json'),
  'markdown':str(A/'optimization_live_progress_v51_20261009.md'),'actual_observer':row})
 print({'observer':row['owned_worker_pid'],'progress':str(A/'optimization_live_progress_v51_20261009.md')},flush=True)
if __name__=='__main__':main()
