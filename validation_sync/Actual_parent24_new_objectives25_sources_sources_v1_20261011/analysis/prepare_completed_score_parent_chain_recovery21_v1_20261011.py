from pathlib import Path
import sys,re
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
def main():
 assert allowed();old=A/'completed_score_parent_chain_recovery19_routes_v1_20261011.json';data=read(old);tasks=[];completed=[];paths=[Path(__file__),old]
 for n,d in data['remaining_tasks']:
  f=A/'service_owned_workflows_20261006'/n;t=read(f/'service_execution.json');assert not owned(read(f/'native_launch.json'))
  paths.extend([f/'service_execution.json',f/'native_launch.json'])
  if t['status']=='passed':completed.append(n)
  else:tasks.append((n,d))
 names={n:n.replace('recovery19_','recovery21_') for n,d in tasks};aliases=data['service_aliases'].copy();aliases.update(names)
 for k,v in list(aliases.items()):
  if v in names:aliases[k]=names[v]
 for marker in ('pairrank','toppair'):
  oldname=f'actual_stock_{marker}_embedding_own32_controls46_queue_v1_20261010';actual=oldname.replace('_v1_','_v2_');f=A/'service_owned_workflows_20261006'/actual
  assert read(f/'service_execution.json')['status']=='passed' and not owned(read(f/'native_launch.json'));aliases[oldname]=actual;paths.extend([f/'service_execution.json',f/'native_launch.json'])
 route=A/'route_completed_score_parent_chain_recovery19_v1_20261011.py';newroute=A/route.name.replace('recovery19','recovery21');assert not newroute.exists();s=route.read_text(encoding='utf8').replace('recovery19','recovery21');compile(s,str(newroute),'exec');newroute.write_text(s,encoding='utf8',newline='\n');paths.extend([route,newroute]);wrappers={}
 for d,name in data['driver_wrappers'].items():
  oldp=A/name;newp=A/name.replace('recovery19','recovery21');assert not newp.exists();s=oldp.read_text(encoding='utf8').replace('recovery19','recovery21');compile(s,str(newp),'exec');newp.write_text(s,encoding='utf8',newline='\n');wrappers[d]=newp.name;paths.extend([oldp,newp])
 data.update(service_aliases=aliases,driver_wrappers=wrappers,remaining_tasks=[(names[n],d) for n,d in tasks],status='compiled_actual_completed_own32_queue2_instead_failed_queue1_with_original_failed19_preserved',actual_passed19_reused=completed,new_fits=0,new_scores=0)
 data['input_sha256'].update({str(p):sha(p) for p in paths});proof=A/'completed_score_parent_chain_recovery21_routes_v1_20261011.json';create(proof,data)
 for n,d in tasks:
  assert allowed();p=A/wrappers[d];r=start_service(names[n],p.name,[],{str(p):sha(p),str(proof):sha(proof)});create(A/(names[n]+'_activation.json'),r)
 print({'actual_recovery21_workers':len(tasks),'actual_completed_own32_queue2_proofs_checked':2,'new_scientific_scores_or_fits':0},flush=True)
if __name__=='__main__':main()
