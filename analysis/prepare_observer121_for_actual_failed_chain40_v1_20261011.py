from pathlib import Path
import sys,ast,subprocess,psutil,time
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
def main():
 assert allowed();old=A/'monitor_verified_current_optimization_v120_20261011.py';s=old.read_text(encoding='utf8').replace('v120','v121').replace('v228','v230').replace('.120.tmp','.121.tmp')
 marker=' def current(n):';assert s.count(marker)==1
 addition=""" routes38=read(A/'verified_canonical_publication_failed_chain38_routes_v1_20261011.json');routes40=read(A/'actual_failed_chain40_preserving186_resume39_admission_v1_20261011.json')
 aliases.update(routes38['service_aliases']);aliases.update(routes40['service_alias_updates'])
 aliases['actual_stock_rank120_own6_full5_native42_direct33_queue_v1_20261011']='actual_stock_rank120_own6_full5_native42_direct33_queue_v2_20261011'
 aliases['recovery15_StockRank20Seed10Embedding186_round186_full_registration_v1_20261010']='actual186_registered_QA_main_resume39_v1_20261011'
"""
 s=s.replace(marker,addition+marker)
 names=['actual186_registered_QA_main_resume39_v1_20261011','actual186_complete_parent_bridge40_v1_20261011','actual_stock_rank120_objective_stages_main_v1_20261011']
 assert s.count(' while True:')==1;s=s.replace(' while True:'," names += [n for n,d in routes40['tasks']]\n names += "+repr(names)+'\n while True:')
 target=A/'monitor_verified_current_optimization_v121_20261011.py';ast.parse(s);assert not target.exists();target.write_text(s,encoding='utf8')
 f=A/'service_owned_workflows_20261006/actual_fast_optimization_progress_reboot_v120_20261011';row=read(f/'native_launch.json');assert owned(row)
 w=psutil.Process(row['owned_worker_pid']);p=psutil.Process(row['pid']);assert not w.children() and p.create_time()==row['owned_parent_creation_time'] and p.cmdline()[1:]==w.cmdline()[1:]
 spy=ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'
 for _ in range(4):
  r=subprocess.run([str(spy),'dump','--pid',str(w.pid)],capture_output=True,text=True,encoding='utf8',check=True,creationflags=subprocess.CREATE_NO_WINDOW)
  if '(idle)' in r.stdout and 'main (monitor_verified_current_optimization_v120_20261011.py:' in r.stdout:break
  time.sleep(1)
 assert '(idle)' in r.stdout and 'main (monitor_verified_current_optimization_v120_20261011.py:' in r.stdout
 proof={'status':'verified_idle_observer_only_replaced_for_actual_failed_chain40_and_rank120_queue2','identity':row,'stack':r.stdout,'input_sha256':{str(q):sha(q) for q in (Path(__file__),old,target)},'scientific_workers_terminated':0}
 create(A/'observer121_actual_admission_v1_20261011.json',proof)
 assert allowed() and owned(row) and not w.children();w.terminate();w.wait(15);p.terminate();p.wait(15);create(f/'administrative_supersession_for_actual_failed_chain40_observer_v1_20261011.json',proof)
 assert allowed();n=start_service('actual_fast_optimization_progress_reboot_v121_20261011',target.name,[],proof['input_sha256']);create(A/'observer121_actual_activation_v1_20261011.json',n)
 print({'actual_failed_chain40_and_rank120_queue2_observer121_owned':True},flush=True)
if __name__=='__main__':main()
