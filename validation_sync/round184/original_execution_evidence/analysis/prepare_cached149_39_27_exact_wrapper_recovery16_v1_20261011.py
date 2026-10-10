from pathlib import Path
import sys,re,subprocess,psutil
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
from handoff_ready_goss_full_execution_20261006 import retire
def main():
 assert allowed();oldpath=A/'actual183_inner_completion_recovery_routes_v15_20261011.json';old=read(oldpath)
 tasks=old['remaining_tasks'][-11:];mapping={n:n.replace('recovery15_','recovery16_',1) for n,d in tasks};inspections=[]
 for n,d in tasks:
  f=A/'service_owned_workflows_20261006'/n
  if not (f/'native_launch.json').exists():continue
  row=read(f/'native_launch.json');stack=None;term=read(f/'service_execution.json') if (f/'service_execution.json').exists() else None
  assert not term or term['status']!='passed',(n,term)
  if owned(row):
   p=psutil.Process(row['owned_worker_pid']);assert not p.children()
   stack=subprocess.run([str(ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(p.pid)],capture_output=True,text=True,timeout=30).stdout
   assert 'closed (' in stack or 'wait (' in stack,(n,stack)
  inspections.append({'identity':row,'terminal':term,'idle_stack':stack})
 aliases={k:mapping.get(v,v) for k,v in old['service_aliases'].items()};aliases.update(mapping)
 for k,v in list(aliases.items()):
  if any(x in v for x in ('MixedObjectiveWindow189','MixedProtected190','MixedRefined191')) and v.startswith('recovery15_'):aliases[k]=v.replace('recovery15_','recovery16_',1);aliases[v]=aliases[k]
 outputs=[]
 def save(name,text):
  p=A/name;assert not p.exists(),p;compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');outputs.append(p);return p
 files={Path(p).name:Path(p).name.replace('_v15_inner','_v16_cached') for p in old['input_sha256'] if Path(p).name.endswith('_v15_inner.py')}
 tokens={**files,**aliases,'route_actual183_inner_completion_recovery_v15_20261011':'route_cached149_39_27_exact_wrapper_recovery_v16_20261011'}
 pat=re.compile('|'.join(re.escape(k) for k in sorted(tokens,key=len,reverse=True)))
 for oldname,newname in files.items():save(newname,pat.sub(lambda m:tokens[m.group()],(A/oldname).read_text(encoding='utf8')))
 route=(A/'route_actual183_inner_completion_recovery_v15_20261011.py').read_text(encoding='utf8').replace("PROOF=A/'actual183_inner_completion_recovery_routes_v15_20261011.json'","PROOF=A/'cached149_39_27_exact_wrapper_recovery_routes_v16_20261011.json'")
 save('route_cached149_39_27_exact_wrapper_recovery_v16_20261011.py',route)
 wrappers={k:files.get(v,v) for k,v in old['driver_wrappers'].items()}
 for n,d in tasks:
  p=save(Path(d).stem+'_cached_recovery16_wrapper.py',"from pathlib import Path\nimport sys\nA=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]\nfrom route_cached149_39_27_exact_wrapper_recovery_v16_20261011 import execute\nif __name__=='__main__':execute("+repr(d)+")\n");wrappers[d]=p.name
 proof=A/'cached149_39_27_exact_wrapper_recovery_routes_v16_20261011.json';newtasks=[(mapping[n],d) for n,d in tasks]
 create(proof,{**old,'status':'compiled_exact_new16_wrappers_for_cached149_39_27_not_old14_wrapper_dispatch','service_aliases':aliases,'driver_wrappers':wrappers,'remaining_tasks':newtasks,'input_sha256':{str(p):sha(p) for p in [Path(__file__),oldpath,*outputs]},'original_failure_and_idle_inspections':inspections,'new_fits':0,'new_scores':0})
 for row in inspections:
  if owned(row['identity']):assert allowed();retire(row['identity'],'Retire exact idle old14-dispatch dependency wrapper; fresh16 routes cached completed209 records; no scientific output overwritten')
 launches=[]
 for name,driver in newtasks:
  assert allowed()
  try:r=start_service(name,wrappers[driver],[],{str(proof):sha(proof)});create(A/(name+'_activation.json'),r);launches.append({'name':name,'launched':True})
  except AssertionError:
   f=A/'service_owned_workflows_20261006'/name/'service_execution.json';assert f.exists();launches.append({'name':name,'actual_terminal':read(f)})
 create(A/'cached149_39_27_exact_wrapper_recovery16_actual_dispatch_v1_20261011.json',{'launches':launches,'new_fits':0,'new_scores':0});print(launches,flush=True)
if __name__=='__main__':main()
