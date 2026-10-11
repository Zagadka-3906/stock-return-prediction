from pathlib import Path
import sys,subprocess,psutil
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
from handoff_ready_goss_full_execution_20261006 import retire
def main():
 assert allowed();old=A/'new_objectives_exact_source_recovery18_routes_v1_20261011.json';data=read(old);p19=A/'completed_score_parent_chain_recovery19_routes_v1_20261011.json';r19=read(p19);tasks=data['remaining_tasks'][3:]
 fresh={n:data['service_aliases'][n].replace('recovery18_','recovery20_') for n,d in tasks}
 aliases=data['service_aliases'].copy();aliases.update({k:v for k,v in r19['service_aliases'].items() if k not in aliases});aliases.update(fresh)
 # Future child dispatches of192/193/194 use fresh20 identities, while the live49 score worker is preserved.
 for n,v in list(aliases.items()):
  if v.startswith('recovery18_') and n not in [x[0] for x in data['remaining_tasks'][:3]]:aliases[n]=v.replace('recovery18_','recovery20_')
 route=A/'route_new_objectives_exact_source_recovery18_v1_20261011.py';newroute=A/route.name.replace('recovery18','recovery20');assert not newroute.exists();s=route.read_text(encoding='utf8').replace('recovery18','recovery20');compile(s,str(newroute),'exec');newroute.write_text(s,encoding='utf8',newline='\n')
 paths=[Path(__file__),old,p19,route,newroute];wrappers={}
 for d,name in data['driver_wrappers'].items():
  oldp=A/name;newp=A/name.replace('recovery18','recovery20');assert not newp.exists();s=oldp.read_text(encoding='utf8').replace('recovery18','recovery20');compile(s,str(newp),'exec');newp.write_text(s,encoding='utf8',newline='\n');wrappers[d]=newp.name;paths.extend([oldp,newp])
 audit=[]
 for n,d in tasks:
  oldname=data['service_aliases'][n];f=A/'service_owned_workflows_20261006'/oldname;row=read(f/'native_launch.json');stack=None
  if owned(row):
   p=psutil.Process(row['owned_worker_pid']);assert not p.children(),n;stack=subprocess.run([str(ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(p.pid)],capture_output=True,text=True,timeout=30).stdout;assert 'closed (' in stack,n
   retire(row,'Transfer exact idle new-objective prerequisite to actual refreshed completed-score19 parent chain; live49/train/full5 scoring preserved')
  audit.append({'identity':row,'actual_idle_stack':stack})
 data.update(service_aliases=aliases,driver_wrappers=wrappers,remaining_tasks=tasks,status='compiled_actual19_parent_chain_with_live49_worker_preserved_before_future',preserved_idle18_helpers=audit,new_fits=0,new_scores=0)
 data['input_sha256'].update({str(p):sha(p) for p in paths});proof=A/'new_objectives_exact_source_recovery20_routes_v1_20261011.json';create(proof,data)
 for n,d in tasks:
  assert allowed();p=A/wrappers[d];r=start_service(fresh[n],p.name,[],{str(p):sha(p),str(proof):sha(proof)});create(A/(fresh[n]+'_activation.json'),r)
 print({'actual_new_objectives20_idle_parent_routes':len(tasks),'live_scientific_workers_preserved':True},flush=True)
if __name__=='__main__':main()
