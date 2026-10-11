"""Replace only verified idle future gates; retain live board188 and all scientific work."""
from pathlib import Path
import ast,sys,subprocess,psutil
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service

def main():
 assert allowed()
 previous=A/'actual_verified_current58_after_actual187_bridge_admission_v1_20261011.json'
 raw=A/'actual_raw_science_completed183_current59_admission_v1_20261011.json'
 data=read(previous);paths=[Path(__file__),previous,raw,*[Path(p) for p in data['input_sha256']]]
 # Only the final five families depend on raw59 comparisons. Earlier boards keep their live routes.
 wanted=data['tasks'][-15:];evidence=[];aliases=dict(read(raw)['service_alias_updates'])
 for name,driver in wanted:
  f=A/'service_owned_workflows_20261006'/name;launch=read(f/'native_launch.json')
  assert not (f/'service_execution.json').exists() and owned(launch),name
  stack=subprocess.run([str(A.parent/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(launch['owned_worker_pid'])],capture_output=True,text=True,encoding='utf8',check=True).stdout
  assert '(idle)' in stack and 'closed (' in stack,(name,stack)
  w=psutil.Process(launch['owned_worker_pid']);parent=psutil.Process(launch['pid'])
  assert not w.children() and w.create_time()==launch['owned_worker_creation_time'] and parent.create_time()==launch['owned_parent_creation_time']
  evidence.append({'name':name,'identity':launch,'actual_idle_stack':stack})
  aliases[name]=name.replace('recovery58_','recovery60_',1)
 route=A/'route_future202_206_current60_raw59_v1_20261011.py'
 s=(A/'route_verified_current58_after_actual187_bridge_v1_20261011.py').read_text(encoding='utf8')
 s=s.replace("PROOF=A/'actual_verified_current58_after_actual187_bridge_admission_v1_20261011.json'","PROOF=A/'actual_future202_206_current60_raw59_admission_v1_20261011.json'")
 needle="'actual_verified_current55_publication_runtime_admission_v1_20261011.json']:"
 assert s.count(needle)==1
 s=s.replace(needle,"'actual_verified_current55_publication_runtime_admission_v1_20261011.json','actual_verified_current58_after_actual187_bridge_admission_v1_20261011.json']:")
 ast.parse(s);assert not route.exists();route.write_text(s,encoding='utf8');paths.append(route)
 wrappers={}
 for driver in data['driver_wrappers']:
  p=A/(Path(driver).stem+'_future_raw59_current60_wrapper.py')
  t='from route_future202_206_current60_raw59_v1_20261011 import execute\nif __name__=="__main__":execute('+repr(driver)+')\n'
  ast.parse(t);assert not p.exists();p.write_text(t,encoding='utf8');paths.append(p);wrappers[driver]=p.name
 tasks=[(aliases[n],d) for n,d in wanted]
 proof=A/'actual_future202_206_current60_raw59_admission_v1_20261011.json'
 create(proof,{'status':'actual15_idle_future202_206_gates_only_route_to_raw59_completed183_comparisons_no_science_rerun',
  'input_sha256':{str(p):sha(p) for p in dict.fromkeys(paths)},'service_alias_updates':aliases,
  'driver_wrappers':wrappers,'tasks':tasks,'source_factories':data['source_factories'],
  'publication_module_corrections':data['publication_module_corrections'],
  'actual_family_folder_controls':data['actual_family_folder_controls'],
  'idle_retirements':evidence,'science_workers_restarted':0,'new_fits_or_scores':0,'test_labels_read':False})
 for row in evidence:
  launch=row['identity'];assert owned(launch)
  w=psutil.Process(launch['owned_worker_pid']);parent=psutil.Process(launch['pid']);assert not w.children()
  for p in (w,parent):p.terminate();p.wait(timeout=15)
 for name,driver in tasks:
  assert allowed();p=A/wrappers[driver]
  r=start_service(name,p.name,[],{str(p):sha(p),str(proof):sha(proof)})
  create(A/(name+'_activation.json'),r)
 print({'future202_206_idle_gates_corrected':15,'active_scientific_workers_restarted':0},flush=True)

if __name__=='__main__':main()
