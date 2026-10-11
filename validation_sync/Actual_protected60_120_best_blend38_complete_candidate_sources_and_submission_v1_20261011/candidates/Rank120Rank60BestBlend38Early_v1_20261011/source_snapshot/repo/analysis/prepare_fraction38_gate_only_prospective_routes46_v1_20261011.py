from pathlib import Path
import sys,ast,importlib,subprocess,psutil,re
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
assert allowed()
factories=['prepare_StockRank60Fraction202_complete40_pipeline_v2_20261011','prepare_Rank120Rank60Protected203_complete39_pipeline_v1_20261011','prepare_StockRank60Seed10Direct204_complete35_pipeline_v1_20261011','prepare_Rank60TwoSeedProtected205_complete39_pipeline_v2_20261011','prepare_StockRank60Window504Direct206_complete35_pipeline_v1_20261011']
drivers=[];top=[];paths=[Path(__file__)]
for name in factories:
 m=importlib.import_module(name);drivers.extend(m.NAMES+m.EXTRAS[:9]);top.extend(m.EXTRAS[i] for i in (0,1,5));paths.extend(m.source_paths())
top += ['run_stock_rank60seed10_embedding_after183_direct_allocation33_v1_20261011.py','run_rank60_two_seed_after183_protected37_screen_v1_20261011.py','run_stock_rank60window504_embedding_after183_direct_allocation33_v1_20261011.py','publish_actual_protected37_fraction38_completed75_main_v1_20261011.py','publish_actual_rank60_seed10_pure33_and_two_seed37_completed70_main_v1_20261011.py','publish_actual_rank60_seed10_pure33_completed_main_v1_20261011.py','publish_actual_rank60_two_seed_protected37_completed_main_v1_20261011.py','publish_actual_rank60_window504_pure33_completed_main_v1_20261011.py']
drivers+=top
proof=A/'actual_fraction38_gate_only_routes46_admission_v1_20261011.json'
route=A/'route_fraction38_gate_only_prospective46_v1_20261011.py'
s=(A/'route_actual_nested_dispatch_and_complete_aliases45_v1_20261011.py').read_text(encoding='utf8')
s=s.replace("PROOF=A/'actual_nested_dispatch_and_complete_aliases45_admission_v1_20261011.json'","PROOF=A/'actual_fraction38_gate_only_routes46_admission_v1_20261011.json'")
s=s.replace("'actual_nested_dispatch_and_complete_aliases44_admission_v1_20261011.json']","'actual_nested_dispatch_and_complete_aliases44_admission_v1_20261011.json','actual_nested_dispatch_and_complete_aliases45_admission_v1_20261011.json']")
s=s.replace(" for f in p41['source_factories']:"," for f in [*p41['source_factories'],*proof['source_factories']]:")
s=s.replace("  if hasattr(m,'closed'):m.closed=closed", "  if hasattr(m,'create'):\n   prior_create=m.create\n   def pinned_create(path,value):\n    if isinstance(value,dict) and 'input_sha256' in value:value['input_sha256'].update({str(PROOF):sha(PROOF),str(Path(__file__)):sha(__file__)})\n    return prior_create(path,value)\n   m.create=pinned_create\n  if hasattr(m,'closed'):m.closed=closed")
ast.parse(s);assert not route.exists();route.write_text(s,encoding='utf8');paths.append(route)
wrappers={}
for driver in dict.fromkeys(drivers):
 if not (A/driver).is_file():continue
 p=A/(Path(driver).stem+'_fraction38_gate46_wrapper.py')
 t="from pathlib import Path\nimport sys\nA=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]\nfrom route_fraction38_gate_only_prospective46_v1_20261011 import execute\nif __name__=='__main__':execute("+repr(driver)+")\n"
 assert not p.exists();ast.parse(t);p.write_text(t,encoding='utf8');wrappers[driver]=p.name;paths.append(p)
aliases={'actual_stock_rank60_after183_protected_fraction38_screen_v1_20261011':'actual_fraction38_completed_namespace_bridge_v1_20261011'};tasks=[];retired=[]
for driver in top:
 matches=[]
 for folder in (A/'service_owned_workflows_20261006').iterdir():
  p=folder/'native_launch.json'
  if p.exists() and Path(read(p)['original_driver']).name==driver:matches.append(folder)
 assert len(matches)==1,(driver,[str(p) for p in matches])
 folder=matches[0];row=read(folder/'native_launch.json');name=folder.name;new='recovery46_'+name
 if (folder/'service_execution.json').exists():
  terminal=read(folder/'service_execution.json');assert terminal['status']=='failed' and not owned(row),(name,terminal)
  retired.append({'name':name,'already_failed':terminal})
 else:
  assert owned(row),name
  spy=subprocess.run([str(A.parent/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(row['owned_worker_pid'])],capture_output=True,text=True,encoding='utf8',check=True).stdout
  assert 'closed (prepare_protected_tail_pilot76_and_selected_native14_v1_20261010.py:' in spy and driver in spy,(name,spy)
  worker=psutil.Process(row['owned_worker_pid']);parent=psutil.Process(row['pid']);assert not worker.children()
  assert worker.create_time()==row['owned_worker_creation_time'] and parent.create_time()==row['owned_parent_creation_time']
  worker.terminate();worker.wait(timeout=15);parent.terminate();parent.wait(timeout=15)
  item={'name':name,'identity':row,'stack':spy,'reason':'verified_idle_before_first_scientific_or_publication_gate_only_recovery','scientific_workers_stopped':0}
  create(folder/'administrative_prospective_gate_only_supersession46.json',item);retired.append(item)
 aliases[name]=new;tasks.append((new,driver))
# Capture all nested fresh service identifiers so families start and wait for the same identities.
for driver in drivers:
 p=A/driver
 if not p.is_file():continue
 for node in ast.walk(ast.parse(p.read_text(encoding='utf8'))):
  if isinstance(node,ast.Tuple) and len(node.elts)>=2 and all(isinstance(n,ast.Constant) and isinstance(n.value,str) for n in node.elts[:2]):
   name,child=(n.value for n in node.elts[:2])
   if child in wrappers:aliases.setdefault(name,'recovery46_'+name)
for k,v in list(aliases.items()):
 if 'two_seed_protected39' in k and '_v2_20261011' in k:aliases[k.replace('_v2_20261011','_v1_20261011')]=v
create(proof,{'status':'only_idle_prospective_helpers_replaced_final_fraction38_namespace_failure_is_independently_bridged_no_scientific_worker_restart','input_sha256':{str(p):sha(p) for p in dict.fromkeys(paths)},'service_alias_updates':aliases,'driver_wrappers':wrappers,'source_factories':factories,'tasks':tasks,'retired_idle_helpers':retired,'new_fits_or_scores':0,'test_labels_read':False})
for name,driver in tasks:
 assert allowed();p=A/wrappers[driver];r=start_service(name,p.name,[],{str(p):sha(p),str(proof):sha(proof)});create(A/(name+'_activation.json'),r)
print({'actual_prospective_helpers_recovered':len(tasks),'scientific_workers_restarted':0},flush=True)
