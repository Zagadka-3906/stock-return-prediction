from pathlib import Path
import sys,subprocess,psutil
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
from handoff_ready_goss_full_execution_20261006 import retire
def main():
 assert allowed();old=A/'monitor_reboot_optimization_v110_20261011.py';new=A/'monitor_reboot_optimization_v111_20261011.py';assert not new.exists()
 text=old.read_text(encoding='utf8').replace('v110','v111').replace('.110.tmp','.111.tmp').replace('handoff_v195','handoff_v200')
 extra=""" current31=read(A/'completed_score_parent_chain_recovery31_routes_v1_20261011.json');current33=read(A/'new_objectives_exact_source_recovery33_routes_v1_20261011.json')
 current_aliases={**current31['service_aliases'],**current33['service_aliases']}
 def current_name(n):
  if n.startswith('recovery24_'):return current_aliases.get(n,n.replace('recovery24_','recovery31_'))
  if n.startswith('recovery25_'):return current_aliases.get(n,n.replace('recovery25_','recovery33_'))
  return current_aliases.get(n,n)
 names=[current_name(n) for n in names]
 names=[n.replace('actual_1300_deadline_Top10BCE_CPU_sources_main_v1_','actual_1300_deadline_Top10BCE_CPU_sources_main_v2_') for n in names]
 names+=['actual184_registered_QA_main_resume29_v1_20261011','actual184_registered_QA_main_complete_parent_bridge30_v1_20261011','actual_parent3133_frozen_publication_runtime_sources_main_v1_20261011','actual_stock_rank20class10_objective_stages_main_v1_20261011']
 names += [n for n,_ in current31['remaining_tasks']]+[current33['service_aliases'][n] for n,_ in current33['remaining_tasks']]
"""
 assert text.count(' while True:\n')==1;text=text.replace(' while True:\n',extra+' while True:\n',1)
 compile(text,str(new),'exec');new.write_text(text,encoding='utf8',newline='\n')
 row=read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_reboot_v110_20261011/native_launch.json');assert owned(row)
 p=psutil.Process(row['owned_worker_pid']);assert not p.children();r=subprocess.run([str(ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(p.pid)],capture_output=True,text=True,timeout=30);assert r.returncode==0 and 'main (monitor_reboot_optimization_v110_20261011.py:' in r.stdout
 retire(row,'Observer111 follows current live parent31 and objective33 and preserves historical failures and scientific work')
 paths=[Path(__file__),old,new,A/'completed_score_parent_chain_recovery31_routes_v1_20261011.json',A/'new_objectives_exact_source_recovery33_routes_v1_20261011.json']
 proof=A/'actual_observer111_parent3133_sources_admission_v1_20261011.json';create(proof,{'status':'compiled_current_actual3133_observer111','input_sha256':{str(p):sha(p) for p in paths},'retired_only_idle_observer':row,'actual_idle_stack':r.stdout,'new_fits':0,'new_scores':0})
 assert allowed();r=start_service('actual_fast_optimization_progress_reboot_v111_20261011',new.name,[],{str(new):sha(new),str(proof):sha(proof)});create(A/'actual_fast_optimization_progress_reboot_v111_20261011_activation.json',r)
 print({'current_observer111_started':True},flush=True)
if __name__=='__main__':main()
