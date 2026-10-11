"""Replace only54 actual idle future gate processes with one sequential dispatcher."""
from pathlib import Path
import sys,ast,subprocess,psutil
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
PROOF='verified_idle_future_single_dispatch63_admission_v1_20261011.json'

def save(p,s):
 ast.parse(s);assert not p.exists();p.write_text(s,encoding='utf-8',newline='\n');return p

def main():
 assert allowed()
 prior=A/'actual189_missing_service_evidence_and_failed_chain61_admission_v1_20261011.json'
 last=A/'actual207_current61_parent_exact62_gates_admission_v1_20261011.json'
 data=read(prior);lastdata=read(last)
 wanted=[*data['tasks'][1:],*lastdata['tasks']]
 assert len(wanted)==54
 evidence=[];aliases=dict(lastdata['service_alias_updates']);tasks=[];before=psutil.virtual_memory().available
 for name,driver in wanted:
  d=A/'service_owned_workflows_20261006'/name;i=read(d/'native_launch.json')
  assert owned(i) and not (d/'service_execution.json').exists(),name
  dump=subprocess.run([str(A.parent/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(i['owned_worker_pid'])],capture_output=True,text=True,encoding='utf-8',check=True).stdout
  assert '(idle)' in dump and 'closed (' in dump,(name,dump)
  p=psutil.Process(i['owned_worker_pid']);assert not p.children(recursive=True)
  new=name.replace('recovery61_','recovery63_',1).replace('recovery62_','recovery63_',1)
  assert new!=name;aliases[name]=new;tasks.append((new,driver))
  evidence.append({'name':name,'identity':i,'actual_idle_dump':dump,'resident_bytes':p.memory_info().rss})
 route=A/'route_verified_idle_future_single_dispatch63_v1_20261011.py'
 text=(A/'route_actual207_current61_parent_exact62_gates_v1_20261011.py').read_text(encoding='utf-8')
 text=text.replace("PROOF=A/'"+last.name+"'","PROOF=A/'"+PROOF+"'")
 needle="'actual189_missing_service_evidence_and_failed_chain61_admission_v1_20261011.json']:";assert text.count(needle)==1
 text=text.replace(needle,"'actual189_missing_service_evidence_and_failed_chain61_admission_v1_20261011.json','"+last.name+"']:")
 save(route,text);paths=[Path(__file__),prior,last,route]
 wrappers={}
 for driver in lastdata['driver_wrappers']:
  p=save(A/(Path(driver).stem+'_single_dispatch63_wrapper.py'),"from route_verified_idle_future_single_dispatch63_v1_20261011 import execute\nif __name__=='__main__':execute("+repr(driver)+")\n")
  wrappers[driver]=p.name;paths.append(p)
 coordinator=save(A/'run_verified_idle_future_single_dispatch63_v1_20261011.py','''from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from handoff_ready_goss_full_execution_20261006 import start_service
def main():
 assert allowed();closed('recovery61_MixedObjectiveWindow189_complete149_family_v3_20261011')
 proof=A/'''+repr(PROOF)+''';data=read(proof)
 for name,driver in data['tasks']:
  assert allowed();p=A/data['driver_wrappers'][driver]
  identity=start_service(name,p.name,[],{str(p):sha(p),str(proof):sha(proof)})
  create(A/(name+'_activation.json'),identity);closed(name)
 print('All actual54 future stages completed; full objective audit still required',flush=True)
if __name__=='__main__':main()
''');paths.append(coordinator)
 create(A/PROOF,{'status':'actual54_owned_idle_future_controllers_single_dispatch_same_temporal_dependencies_original_science_gates_preserved','input_sha256':{str(p):sha(p) for p in paths},'service_alias_updates':aliases,'driver_wrappers':wrappers,'source_factories':lastdata['source_factories'],'publication_module_corrections':lastdata['publication_module_corrections'],'actual_family_folder_controls':lastdata['actual_family_folder_controls'],'tasks':tasks,'actual_idle_retirements':evidence,'aggregate_observed_idle_resident_bytes':sum(r['resident_bytes'] for r in evidence),'available_memory_before_bytes':before,'original189_registration_and_family_preserved':True,'scientific_workers_restarted_or_terminated':0,'new_scientific_scores_claimed':0,'future_dispatch_requires_actual189_full_QA_main_complete':True,'test_labels_read':False})
 for row in evidence:
  i=row['identity'];assert owned(i);p=psutil.Process(i['owned_worker_pid']);assert not p.children(recursive=True);p.terminate();p.wait(timeout=10)
 assert allowed();i=start_service('actual_verified_idle_future_single_dispatch63_v1_20261011',coordinator.name,[],{str(coordinator):sha(coordinator),str(A/PROOF):sha(A/PROOF)})
 create(A/'actual_verified_idle_future_single_dispatch63_activation_v1_20261011.json',{'identity':i,'available_memory_after_bytes':psutil.virtual_memory().available,'retired_actual_idle_controller_count':54,'observed_resident_bytes':sum(r['resident_bytes'] for r in evidence),'scientific_workers_restarted_or_terminated':0})
 print({'actual_idle_controllers_replaced':54,'one_sequential_dispatcher_live':True,'observed_idle_RSS_GiB':sum(r['resident_bytes'] for r in evidence)/2**30,'scientific_workers_terminated':0},flush=True)

if __name__=='__main__':main()
