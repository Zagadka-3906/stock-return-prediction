"""Keep live190 intact; defer only unstarted low-gain full-board stages until high-impact science is complete."""
from pathlib import Path
import sys,ast,subprocess,psutil
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service

def main():
 assert allowed()
 oldproof=A/'verified_future_byte_exact64_admission_v1_20261011.json';data=read(oldproof);tasks=data['tasks'];assert len(tasks)==54
 for n,_ in tasks[:2]:assert read(A/'service_owned_workflows_20261006'/n/'service_execution.json')['status']=='passed'
 current=tasks[2][0];assert 'MixedProtected190' in current
 for n,_ in tasks[3:]:assert not (A/'service_owned_workflows_20261006'/n).exists(),n
 service=A/'service_owned_workflows_20261006/actual_verified_future_byte_exact64_v1_20261011';identity=read(service/'native_launch.json')
 def idle():
  assert owned(identity);p=psutil.Process(identity['owned_worker_pid']);assert not p.children(recursive=True)
  dump=subprocess.run([str(A.parent/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(p.pid)],capture_output=True,text=True,encoding='utf8',check=True).stdout
  assert '(idle)' in dump and 'closed (' in dump,dump;return dump
 dump=idle()
 science=['actual_rank60_two_capacity_after183_protected109_screen_v3_20261011','actual_rank60_two_capacity_after183_CDF49_screen_v1_20261011','actual_rank120medium2048_own6_native42_direct33_queue_v1_20261011','actual_rank120medium2048_gain_selected_full_candidate_queue_v1_20261011','actual_rank60_two_capacity_protected109_early_gaining_candidate_queue_v1_20261011','actual_rank60_two_capacity_CDF49_early_gaining_candidate_queue_v2_20261011','actual_rank60_flag17_gain_selected_full_candidate_queue_v1_20261011','actual_rank60_flag17_after_best38_gain_selected_full_candidate_queue_v1_20261011']
 proof=A/'high_gain_science_priority_after_actual190_admission_v1_20261011.json';driver=A/'run_high_gain_science_priority_after_actual190_v1_20261011.py'
 text='''from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from start_fast_completed_owned_service_v1_20261011 import start_service
def main():
 assert allowed();proof=A/PROOF;data=read(proof)
 closed(data['live190_family_preserved'])
 for name in data['high_gain_science_gates']:
  assert allowed();closed(name)
 routing=A/'verified_future_byte_exact64_admission_v1_20261011.json';sources=read(routing)
 for name,original in data['remaining_original_tasks']:
  assert allowed();p=A/sources['driver_wrappers'][original]
  i=start_service(name,p.name,[],{str(p):sha(p),str(routing):sha(routing),str(proof):sha(proof)})
  create(A/(name+'_activation.json'),i);closed(name)
 print('All remaining original51 full-board stages complete after high-gain science; goal audit still required',flush=True)
if __name__=='__main__':main()
'''.replace('PROOF',repr(proof.name))
 ast.parse(text);assert not driver.exists();driver.write_text(text,encoding='utf8',newline='\n')
 create(proof,{'status':'actual_idle_coordinator_only_replacement_high_gain_model_scoring_and_full_native_candidate_priority_unchanged_original51_full_board_tasks_deferred_not_deleted','input_sha256':{str(p):sha(p) for p in [Path(__file__),driver,oldproof]},'live190_family_preserved':current,'high_gain_science_gates':science,'remaining_original_tasks':tasks[3:],'original_idle_identity':identity,'actual_idle_stack':dump,'scientific_workers_restarted_or_terminated':0,'new_scores':0,'deadline':'2026-10-11T13:00:00+08:00','test_labels_read':False})
 idle()
 for n,_ in tasks[3:]:assert not (A/'service_owned_workflows_20261006'/n).exists(),n
 p=psutil.Process(identity['owned_worker_pid']);assert owned(identity);p.terminate();p.wait(timeout=10)
 assert allowed();i=start_service('actual_high_gain_science_priority_after_live190_v1_20261011',driver.name,[],{str(driver):sha(driver),str(proof):sha(proof)})
 create(A/'actual_high_gain_science_priority_after_live190_activation_v1_20261011.json',i)
 print('Live190 and every scientific worker preserved; only idle coordinator replaced; original51 stages retained after high-gain science',flush=True)

if __name__=='__main__':main()
