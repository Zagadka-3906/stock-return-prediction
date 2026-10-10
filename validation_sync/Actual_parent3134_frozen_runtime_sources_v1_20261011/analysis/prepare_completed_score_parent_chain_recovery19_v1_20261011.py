"""Resolve old v6 helper names to fresh real v8 execution; retain all existing science."""
from pathlib import Path
import sys,importlib,subprocess,psutil,re
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
from handoff_ready_goss_full_execution_20261006 import retire
def main():
 assert allowed();p15=A/'actual183_inner_completion_recovery_routes_v15_20261011.json';p16=A/'cached149_39_27_exact_wrapper_recovery_routes_v16_20261011.json';r15=read(p15);data=read(p16)
 tasks=r15['remaining_tasks'][2:-11]+data['remaining_tasks']
 tasks=[(n,d) for n,d in tasks if not ((A/'service_owned_workflows_20261006'/n/'service_execution.json').exists() and read(A/'service_owned_workflows_20261006'/n/'service_execution.json')['status']=='passed')]
 names={n:'recovery19_'+re.sub(r'^recovery(?:15|16)_','',n) for n,d in tasks}
 aliases=data['service_aliases'].copy();aliases.update(r15['service_aliases'])
 # Cached16 mappings must supersede15 fallback mappings.
 aliases.update(data['service_aliases']);aliases.update(names)
 for k,v in list(aliases.items()):
  if v in names:aliases[k]=names[v]
 for marker in ('pairrank','toppair'):
  n=f'actual_stock_{marker}_embedding48_after{183 if marker=="pairrank" else 184}_normalization_queue_v6_20261010'
  n8=n.replace('_v6_','_v8_');aliases[n]=names.get('recovery15_'+n8,'recovery15_'+n8)
  qual=f'Stock{"PairRank" if marker=="pairrank" else "TopPair"}Embedding48_selected_native14_v6_20261010'
  aliases[qual]=names['recovery15_'+qual.replace('_v6_','_v8_')]
 route=A/'route_cached149_39_27_exact_wrapper_recovery_v16_20261011.py';newroute=A/'route_completed_score_parent_chain_recovery19_v1_20261011.py';text=route.read_text(encoding='utf8').replace("cached149_39_27_exact_wrapper_recovery_routes_v16_20261011.json","completed_score_parent_chain_recovery19_routes_v1_20261011.json");compile(text,str(newroute),'exec')
 if newroute.exists():assert newroute.read_text(encoding='utf8')==text
 else:newroute.write_text(text,encoding='utf8',newline='\n')
 drivers=set(data['driver_wrappers'])|{d for n,d in tasks};wrappers={};paths=[Path(__file__),p15,p16,route,newroute]
 for d in drivers:
  assert (A/d).is_file(),d
  p=A/(Path(d).stem+'_actual_parent_chain_recovery19_wrapper.py')
  s="from pathlib import Path\nimport sys\nA=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]\nfrom route_completed_score_parent_chain_recovery19_v1_20261011 import execute\nif __name__=='__main__':execute("+repr(d)+")\n";compile(s,str(p),'exec')
  if p.exists():assert p.read_text(encoding='utf8')==s
  else:p.write_text(s,encoding='utf8',newline='\n')
  wrappers[d]=p.name;paths.extend([A/d,p])
 audit=[]
 for n,d in tasks:
  f=A/'service_owned_workflows_20261006'/n;row=read(f/'native_launch.json');stack=None
  if owned(row):
   p=psutil.Process(row['owned_worker_pid']);assert not p.children(),n
   stack=subprocess.run([str(ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(p.pid)],capture_output=True,text=True,timeout=30).stdout;assert 'closed (' in stack,n
   retire(row,'Resolve actual stale v6 prerequisite to completed v8 or fresh19 task; no model/score/future execution begun in this idle helper')
  else:assert not (f/'service_execution.json').exists() or read(f/'service_execution.json')['status']!='passed',n
  audit.append({'prior_name':n,'identity':row,'actual_idle_stack':stack})
 data.update(status='compiled_exact_v6_to_actual_v8_parent_chain_recovery_before_new_future',service_aliases=aliases,driver_wrappers=wrappers,remaining_tasks=[(names[n],d) for n,d in tasks],preserved_previous_idle_helpers=audit,new_fits=0,new_scores=0)
 data['input_sha256'].update({str(p):sha(p) for p in paths});proof=A/'completed_score_parent_chain_recovery19_routes_v1_20261011.json';create(proof,data)
 for n,d in tasks:
  assert allowed();p=A/wrappers[d];r=start_service(names[n],p.name,[],{str(p):sha(p),str(proof):sha(proof)});create(A/(names[n]+'_activation.json'),r)
 print({'actual_recovery19_workers':len(tasks),'all_model_and_score_caches_preserved':True},flush=True)
if __name__=='__main__':main()
