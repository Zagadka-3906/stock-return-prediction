from pathlib import Path
import sys,subprocess,psutil
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
from handoff_ready_goss_full_execution_20261006 import retire
def main():
 assert allowed();old=A/'new_objectives_exact_source_recovery25_routes_v1_20261011.json';data=read(old);p21=A/'completed_score_parent_chain_recovery31_routes_v1_20261011.json';r21=read(p21);paths=[Path(__file__),old,p21]
 aliases=data['service_aliases'].copy()
 for k,v in list(aliases.items()):
  if v.startswith('recovery24_'):aliases[k]=r21['service_aliases'].get(v,v.replace('recovery24_','recovery31_'))
  elif v.startswith('recovery25_'):aliases[k]=v.replace('recovery25_','recovery32_')
 aliases.update({k:v for k,v in r21['service_aliases'].items() if k not in aliases})
 route=A/'route_new_objectives_exact_source_recovery25_v1_20261011.py';newroute=A/route.name.replace('recovery25','recovery32');assert not newroute.exists();s=route.read_text(encoding='utf8').replace('recovery25','recovery32');compile(s,str(newroute),'exec');newroute.write_text(s,encoding='utf8',newline='\n');paths.extend([route,newroute]);wrappers={}
 for d,name in data['driver_wrappers'].items():
  oldp=A/name;newp=A/name.replace('recovery25','recovery32');assert not newp.exists();s=oldp.read_text(encoding='utf8').replace('recovery25','recovery32');compile(s,str(newp),'exec');newp.write_text(s,encoding='utf8',newline='\n');wrappers[d]=newp.name;paths.extend([oldp,newp])
 audit=[]
 for n,d in data['remaining_tasks']:
  f=A/'service_owned_workflows_20261006'/data['service_aliases'][n];row=read(f/'native_launch.json');stack=None
  if owned(row):
   p=psutil.Process(row['owned_worker_pid']);assert not p.children();stack=subprocess.run([str(ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(p.pid)],capture_output=True,text=True,timeout=30).stdout;assert 'closed (' in stack,n
   retire(row,'Resolve exact idle completed-score parent19 failure to actual queue2 recovery21; original failures retained, live scoring preserved')
  else:assert read(f/'service_execution.json')['status']=='failed'
  audit.append({'identity':row,'actual_idle_stack':stack})
 data.update(status='compiled_new_objectives_against_actual_reboot12_external_frozen_parent31',service_aliases=aliases,driver_wrappers=wrappers,preserved_prior20=audit,new_fits=0,new_scores=0)
 data['input_sha256'].update({str(p):sha(p) for p in paths});proof=A/'new_objectives_exact_source_recovery32_routes_v1_20261011.json';create(proof,data)
 for n,d in data['remaining_tasks']:
  assert allowed();p=A/wrappers[d];r=start_service(aliases[n],p.name,[],{str(p):sha(p),str(proof):sha(proof)});create(A/(aliases[n]+'_activation.json'),r)
 print({'actual_new_objectives32_dispatched':len(data['remaining_tasks']),'live49_and_tail4_scores_preserved':True},flush=True)
if __name__=='__main__':main()
