"""Replace only verified idle administrative waiters; preserve scientific work and pins."""
from pathlib import Path
import sys,re,importlib,subprocess,psutil
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from start_fast_completed_owned_service_v1_20261011 import start_service

def save(p,s):
 assert not p.exists(),p;compile(s,str(p),'exec');p.write_text(s,encoding='utf8',newline='\n');return p

def main():
 assert allowed();closed('actual_stock_rank20class10_twelve_parent183_callbacks_CPU_v2_20261011')
 previous=A/'unified_completed_parent_shared_publication36_routes_v1_20261011.json';old=read(previous)
 factories=['prepare_StockRank20Class10Embedding196_complete19_pipeline_v2_20261011','prepare_StockRank20Class25Embedding197_complete48_pipeline_v1_20261011','prepare_StockRank60Embedding198_complete48_pipeline_v1_20261011']
 tasks=[(n,d) for n,d in old['remaining_tasks'] if any(f'Embedding{x}' in n or (f'after{x-1}_' in n and ('class10' if x==196 else 'class25') in n) for x in (196,197))]
 # Select by actual authoritative factory drivers rather than informal names.
 task_catalog={d:n for n,d in old['remaining_tasks']};tasks=[]
 for factory in factories:
  m=importlib.import_module(factory)
  for index in (0,1,5):
   driver=m.EXTRAS[index]
   if driver in task_catalog:name=task_catalog[driver]
   else:
    number=198;name={0:'actual_stock_rank60_embedding48_after197_normalization_queue_v1_20261011',1:'StockRank60Embedding48_selected_native14_v1_20261011',5:'StockRank60Embedding198_complete48_family_v1_20261011'}[index]
   tasks.append((name,driver))
 assert len(tasks)==9 and len({n for n,d in tasks})==9
 retirements=[]
 for name,driver in tasks:
  folder=A/'service_owned_workflows_20261006'/name;r=read(folder/'native_launch.json');assert owned(r) and not (folder/'service_execution.json').exists(),name
  worker=psutil.Process(r['owned_worker_pid']);assert worker.create_time()==r['owned_worker_creation_time'] and not worker.children(recursive=True)
  dump=subprocess.run([str(A.parent/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(worker.pid),'--locals'],capture_output=True,text=True,encoding='utf8')
  assert dump.returncode==0 and '(idle)' in dump.stdout and 'closed (' in dump.stdout,name
  retirements.append({'identity':r,'actual_idle_stack':dump.stdout,'scientific_children':0})
 overrides=dict(old['actual_source_overrides'])
 overrides.update({'normalize_completed_stock_rank20class10_embedding_complete19_after195_v1_20261011.py':'normalize_completed_stock_rank20class10_embedding_complete19_after195_exact_v4_20261011.py','qualify_stock_rank20class10_embedding19_selected_native14_v1_20261011.py':'qualify_stock_rank20class10_embedding19_selected_native14_v2_20261011.py','prepare_StockRank20Class10Embedding196_selected_candidate_v1_20261011.py':'prepare_StockRank20Class10Embedding196_selected_candidate_v2_20261011.py'})
 aliases=dict(old['service_aliases']);names={n:'recovery37_'+re.sub(r'^recovery\d+_','',n) for n,d in tasks};aliases.update(names)
 for k,v in list(aliases.items()):
  if v in names:aliases[k]=names[v]
 files=[Path(__file__),previous,A/'stock_rank20class10_actual_twelve_parent_callbacks_CPU_controls_v2_20261011.json',A/'verify_stock_rank20class10_actual_twelve_parent_callbacks_CPU_v2_20261011.py']
 for filename in overrides.values():
  if filename in ('normalize_completed_stock_rank20class10_embedding_complete19_after195_exact_v4_20261011.py','qualify_stock_rank20class10_embedding19_selected_native14_v2_20261011.py','prepare_StockRank20Class10Embedding196_selected_candidate_v2_20261011.py'):files.append(A/filename)
 module_aliases={'stock_rank20class10_embedding_after_complete_qualified_parent_native_stage_v1_20261011':'stock_rank20class10_embedding_after_complete_qualified_parent_native_stage_v2_20261011','predict_stock_rank20class10_embedding_complete_qualified_parent_scheme_v1_20261011':'predict_stock_rank20class10_embedding_complete_qualified_parent_scheme_v2_20261011'}
 files += [A/(n+'.py') for n in module_aliases.values()]
 drivers={d for n,d in tasks}
 for factory in factories:
  m=importlib.import_module(factory);drivers.update(d for d in m.EXTRAS if d.endswith('.py'))
  family=(A/m.EXTRAS[5]).read_text(encoding='utf8')
  launches=re.findall(r"\('([^']+)',\s*'([^']+\.py)'\)",family)
  assert len(launches)==3,factory
  for n,d in launches:aliases[n]='recovery37_'+n;drivers.add(d)
  sealer=m.EXTRAS[4];source=A/overrides.get(sealer,sealer);s=source.read_text(encoding='utf8');lines=[l for l in s.splitlines() if l.strip().startswith("service=A/'service_owned_workflows_20261006/")];assert len(lines)==1
  line=lines[0];oldname=line.split('service_owned_workflows_20261006/')[1].rstrip("'");canonical=re.sub(r'^recovery\d+_','',oldname);s=s.replace(line,line.replace(oldname,'recovery37_'+canonical));p=save(A/(Path(sealer).stem+'_actual_preparation_identity37.py'),s);overrides[sealer]=p.name;files.extend([source,p])
  if 'Rank60Embedding198' in factory:
   driver=m.EXTRAS[6];source=A/driver;s=source.read_text(encoding='utf8');needle='from late_bound_dynamic_snapshot_encoder_runtime_v1_20261010 import installed';assert needle in s;s=s.replace(needle,'from late_bound_shared_snapshot_encoder_runtime_v1_20261011 import installed');p=save(A/(Path(driver).stem+'_actual_shared_binding37.py'),s);overrides[driver]=p.name;files.extend([source,p])
 wrappers={}
 for driver in drivers:
  p=save(A/(Path(driver).stem+'_latest183_parent37_wrapper.py'),"from pathlib import Path\nimport sys\nA=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]\nfrom route_actual_latest183_parent196198_v37_20261011 import execute\nif __name__=='__main__':execute("+repr(driver)+")\n");wrappers[driver]=p.name;files.append(p)
 proof=A/'actual_latest183_parent196198_routes37_v1_20261011.json';route=A/'route_actual_latest183_parent196198_v37_20261011.py';files.append(route)
 create(proof,{'status':'compiled_actual183_anchor_loop_native_parent_and_topmost_rank20_callback_fixed_before196_future','input_sha256':{str(p):sha(p) for p in files},'service_aliases':aliases,'actual_source_overrides':overrides,'module_aliases':module_aliases,'driver_wrappers':wrappers,'source_factories':factories,'actual_verified_idle_retirements':retirements,'tasks':[(names[n],d) for n,d in tasks],'new_fits':0,'new_scores':0,'all_old_outputs_preserved':True,'actual198_shared_snapshot_binder_prospective':True})
 for row in retirements:
  assert allowed();r=row['identity'];w=psutil.Process(r['owned_worker_pid']);assert owned(r) and not w.children();w.terminate();w.wait(10)
  create(A/'service_owned_workflows_20261006'/r['name']/'verified_idle_administrative_supersession37.json',{'identity':r,'actual_idle_stack':row['actual_idle_stack'],'new_fits':0,'new_scores':0,'reason':'Use true183 anchors and replay its complete topmost Rank20 stage; preserve partial work, stop no scientific child'})
 for name,driver in tasks:
  assert allowed();p=A/wrappers[driver];r=start_service(names[name],p.name,[],{str(p):sha(p),str(proof):sha(proof)});create(A/(names[name]+'_activation.json'),r)
 print({'actual_latest183_routes37_replaced_only_idle_waiters':len(tasks),'original_scientific_fits_or_scores_restarted':0},flush=True)
if __name__=='__main__':main()
