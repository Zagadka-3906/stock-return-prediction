from pathlib import Path
import sys,re,ast,subprocess,psutil
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
def main():
 assert allowed();p38=A/'verified_canonical_publication_failed_chain38_routes_v1_20261011.json';p39=A/'canonical_publication_resume186_isolated39_admission_v1_20261011.json';d=read(p38);tasks=read(p39)['tasks'][1:]
 resume=A/'service_owned_workflows_20261006/actual186_registered_QA_main_resume39_v1_20261011';r=read(resume/'native_launch.json');assert owned(r) or read(resume/'service_execution.json')['status']=='passed'
 aliases={'actual186_registered_QA_main_resume38_v1_20261011':'actual186_registered_QA_main_resume39_v1_20261011','actual186_complete_parent_bridge38_v1_20261011':'actual186_complete_parent_bridge40_v1_20261011'}
 for name in set(d['service_aliases'].values())|{n for n,_ in tasks}:
  if name.startswith('recovery38_'):aliases[name]=name.replace('recovery38_','recovery40_',1)
 rows=[];newtasks=[]
 for name,driver in tasks:
  new=aliases.get(name,name);assert new!=name,(name,driver);newtasks.append((new,driver));f=A/'service_owned_workflows_20261006'/name
  if (f/'native_launch.json').exists() and owned(read(f/'native_launch.json')):
   row=read(f/'native_launch.json');w=psutil.Process(row['owned_worker_pid']);p=psutil.Process(row['pid']);assert not w.children() and p.create_time()==row['owned_parent_creation_time']
   out=subprocess.run([str(ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(w.pid)],capture_output=True,text=True,encoding='utf8',check=True,creationflags=subprocess.CREATE_NO_WINDOW)
   assert '(idle)' in out.stdout and 'closed (' in out.stdout;rows.append((f,row,w,p,out.stdout))
 wrappers={};files=[Path(__file__),p38,p39,A/'route_actual_failed_chain40_preserving186_resume39_v1_20261011.py']
 for driver in set(d['driver_wrappers'])|{driver for _,driver in newtasks}:
  p=A/(Path(driver).stem+'_actual_failed_chain40_wrapper.py');s="from pathlib import Path\nimport sys\nA=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]\nfrom route_actual_failed_chain40_preserving186_resume39_v1_20261011 import execute\nif __name__=='__main__':execute("+repr(driver)+")\n";ast.parse(s);assert not p.exists();p.write_text(s,encoding='utf8');wrappers[driver]=p.name;files.append(p)
 proof=A/'actual_failed_chain40_preserving186_resume39_admission_v1_20261011.json';create(proof,{'status':'fresh40_only_failed_dependents_existing_live186_resume39_kept','input_sha256':{str(p):sha(p) for p in files},'service_alias_updates':aliases,'driver_wrappers':wrappers,'tasks':newtasks,'verified_idle_retirements':[{'identity':row,'stack':stack} for _,row,_,_,stack in rows],'scientific_workers_terminated':0,'new_fits_or_scores':0})
 for f,row,w,p,stack in rows:
  assert allowed() and owned(row) and not w.children();w.terminate();w.wait(15);p.terminate();p.wait(15);create(f/'administrative_supersession_for_current_failed_chain40.json',{'identity':row,'stack':stack,'scientific_jobs_terminated':0})
 for name,driver in newtasks:
  assert allowed();p=A/wrappers[driver];r=start_service(name,p.name,[],{str(p):sha(p),str(proof):sha(proof)});create(A/(name+'_activation.json'),r)
 print({'current40_dependents_started':len(newtasks),'live186_resume39_not_restarted':True},flush=True)
if __name__=='__main__':main()
