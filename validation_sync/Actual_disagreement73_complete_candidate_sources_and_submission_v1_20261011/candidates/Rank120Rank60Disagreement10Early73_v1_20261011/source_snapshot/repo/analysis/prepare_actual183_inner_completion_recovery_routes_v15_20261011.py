from pathlib import Path
import sys,re,subprocess,psutil,os
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from start_fast_completed_owned_service_v1_20261011 import start_service
from handoff_ready_goss_full_execution_20261006 import retire
def main():
 assert allowed();closed('actual183_completed_inner_inference_rehashed_recovery_v1_20261011')
 oldpath=A/'verified4650_recovery_routes_v14_20261011.json';old=read(oldpath);replacements={};tasks=[];inspections=[]
 for name,driver in old['remaining_tasks']:
  folder=A/'service_owned_workflows_20261006'/name
  term=read(folder/'service_execution.json') if (folder/'service_execution.json').exists() else None
  if term and term['status']=='passed':continue
  row=read(folder/'native_launch.json');stack=None
  if owned(row):
   proc=psutil.Process(row['owned_worker_pid']);assert not proc.children(),name
   stack=subprocess.run([str(ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(proc.pid)],capture_output=True,text=True,timeout=30).stdout
   assert ('closed (' in stack or 'wait (' in stack or 'run_service_owned_windows_workflow_20261006.py:93' in stack), (name,stack)
  new=name.replace('recovery14_','recovery15_',1);assert not (A/'service_owned_workflows_20261006'/new/'native_launch.json').exists()
  replacements[name]=new;tasks.append((new,driver));inspections.append({'name':name,'identity':row,'terminal':term,'idle_stack':stack})
 aliases=dict(old['service_aliases']);aliases.update(replacements)
 for key,value in list(aliases.items()):aliases[key]=replacements.get(value,value)
 recovery='actual183_completed_inner_inference_rehashed_recovery_v1_20261011'
 for key in list(aliases):
  if 'StockRank20Embedding183_selected_candidate_preparation' in key:aliases[key]=recovery
 aliases['recovery14_StockRank20Embedding183_selected_candidate_preparation_v1_20261010']=recovery
 for key,value in list(aliases.items()):
  if value.startswith('recovery14_') and any(x in value for x in ('selected_candidate_preparation','selected_candidate_sealing','full_registration')):aliases[key]=value.replace('recovery14_','recovery15_',1);aliases[value]=aliases[key]
 # The inference itself is complete; the failed feature-cache statistics postcondition remains failed.
 filemap={Path(p).name:Path(p).name.replace('_v14_4650','_v15_inner') for p in old['input_sha256'] if Path(p).name.endswith('_v14_4650.py')}
 filemap['route_verified4650_recovery_v14_20261011']='route_actual183_inner_completion_recovery_v15_20261011'
 tokens={**filemap,**aliases};pattern=re.compile('|'.join(re.escape(k) for k in sorted(tokens,key=len,reverse=True)));outputs=[]
 def save(name,text):
  p=A/name;assert not p.exists(),p;compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');outputs.append(p);return p
 for oldname,newname in filemap.items():
  if not oldname.endswith('.py'):continue
  text=pattern.sub(lambda m:tokens[m.group()],(A/oldname).read_text(encoding='utf8'))
  if oldname.startswith('seal_StockRank20Embedding183') and '_registered_services_' in oldname:
   text=text.replace("while not (service/'native_launch.json').exists() or owned(read(service/'native_launch.json')):time.sleep(15)","from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import closed\n    closed('"+recovery+"')")
   text=text.replace('stock_rank20_embedding85_selected_native14_v1_20261010','stock_rank20_embedding85_selected_native14_v2_20261011')
  save(newname,text)
 route=(A/'route_verified4650_recovery_v14_20261011.py').read_text(encoding='utf8').replace("PROOF=A/'verified4650_recovery_routes_v14_20261011.json'","PROOF=A/'actual183_inner_completion_recovery_routes_v15_20261011.json'")
 save('route_actual183_inner_completion_recovery_v15_20261011.py',route)
 family=(A/'run_StockRank20Embedding183_complete_family_v6_20261010.py').read_text(encoding='utf8')
 family=family.replace('    preflight()','    evidence=read(A/\'stock_rank20_embedding183_full_family_preflight_v2_20261010.json\')\n    for p,d in evidence[\'input_sha256\'].items():assert sha(p)==d,p')
 family=family.replace('        assert not logical.exists() and not physical.exists(),logical\n        physical.mkdir(parents=True);logical.parent.mkdir(parents=True,exist_ok=True);junction(logical,physical);empty(logical)','        assert logical.exists() and physical.exists() and os.path.samefile(logical,physical),logical')
 family=family.replace('import sys,time','import sys,time,os').replace('StockRank20Embedding183_complete_family_v1_20261010','StockRank20Embedding183_complete_family_inner_recovery_v2_20261011')
 save('run_StockRank20Embedding183_complete_family_inner_recovery_v2_20261011.py',family)
 wrappers={k:filemap.get(v,v) for k,v in old['driver_wrappers'].items()}
 for _,driver in tasks:
  if driver not in wrappers:
   p=save(Path(driver).stem+'_recovery15_wrapper.py',"from pathlib import Path\nimport sys\nA=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]\nfrom route_actual183_inner_completion_recovery_v15_20261011 import execute\nif __name__=='__main__':execute("+repr(driver)+")\n");wrappers[driver]=p.name
 overrides={**old['actual_source_overrides'],'run_StockRank20Embedding183_complete_family_v6_20261010.py':'run_StockRank20Embedding183_complete_family_inner_recovery_v2_20261011.py'}
 proof=A/'actual183_inner_completion_recovery_routes_v15_20261011.json'
 create(proof,{**old,'status':'compiled_fresh15_after_actual35_model_candidate_rehash_inner_inference_passed_outer_cache_failure_preserved','service_aliases':aliases,'driver_wrappers':wrappers,'actual_source_overrides':overrides,'remaining_tasks':tasks,'input_sha256':{str(p):sha(p) for p in [Path(__file__),oldpath,A/'actual183_completed_inner_inference_rehashed_recovery_v1_20261011.json',*outputs]},'verified_idle_helpers':inspections,'original_failures_preserved':True,'actual_gpu_inference_not_repeated':True})
 for row in inspections:
  if owned(row['identity']):assert allowed();retire(row['identity'],'Fresh15 replaces verified idle dependency helper after ancillary 4660 cache postcondition; actual inner35-model inference independently rehashed, no GPU inference repeated')
 for name,driver in tasks:
  assert allowed();r=start_service(name,wrappers[driver],[],{str(proof):sha(proof)});create(A/(name+'_activation.json'),r)
 print({'fresh15_actual_tasks':len(tasks),'actual183_full_GPU_inference_reused':True},flush=True)
if __name__=='__main__':main()
