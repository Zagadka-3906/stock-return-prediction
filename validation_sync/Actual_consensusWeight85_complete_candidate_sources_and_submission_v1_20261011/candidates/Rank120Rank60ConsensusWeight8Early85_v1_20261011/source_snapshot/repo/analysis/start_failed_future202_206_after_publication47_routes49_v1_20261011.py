from pathlib import Path
import sys,ast,re,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
assert allowed()
oldproof=A/'actual_fraction38_gate_only_routes46_admission_v1_20261011.json';old=read(oldproof);latest=A/'actual_nested_dispatch_and_complete_aliases48_admission_v1_20261011.json';assert latest.exists()
route=A/'route_failed_future202_206_after_completed187_v49_20261011.py'
s=(A/'route_fraction38_gate_only_prospective46_v1_20261011.py').read_text(encoding='utf8').replace("PROOF=A/'actual_fraction38_gate_only_routes46_admission_v1_20261011.json'","PROOF=A/'actual_failed_future202_206_routes49_admission_v1_20261011.json'")
s=s.replace("'actual_nested_dispatch_and_complete_aliases45_admission_v1_20261011.json']","'actual_nested_dispatch_and_complete_aliases45_admission_v1_20261011.json','actual_fraction38_gate_only_routes46_admission_v1_20261011.json','actual_nested_dispatch_and_complete_aliases48_admission_v1_20261011.json']")
ast.parse(s);assert not route.exists();route.write_text(s,encoding='utf8')
future=[];drivers=[];paths=[Path(__file__),route,oldproof,latest]
for name in old['source_factories']:
 m=importlib.import_module(name);future.extend(m.EXTRAS[i] for i in (0,1,5));drivers.extend(m.NAMES+m.EXTRAS[:9]);paths.extend(m.source_paths())
tasks=[];aliases={};evidence=[]
for name,driver in old['tasks']:
 if driver not in future:continue
 f=A/'service_owned_workflows_20261006'/name;t=read(f/'service_execution.json');assert t['status']=='failed' and not owned(read(f/'native_launch.json')),(name,t)
 new=re.sub(r'^recovery46_','recovery49_',name);aliases[name]=new;tasks.append((new,driver));evidence.append({'name':name,'terminal':t});paths.append(f/'service_execution.json')
assert len(tasks)==15
wrappers={}
for driver in dict.fromkeys(drivers):
 p=A/(Path(driver).stem+'_future49_wrapper.py');text="from pathlib import Path\nimport sys\nA=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]\nfrom route_failed_future202_206_after_completed187_v49_20261011 import execute\nif __name__=='__main__':execute("+repr(driver)+")\n"
 assert not p.exists();ast.parse(text);p.write_text(text,encoding='utf8');wrappers[driver]=p.name;paths.append(p)
 for node in ast.walk(ast.parse((A/driver).read_text(encoding='utf8'))):
  if isinstance(node,ast.Tuple) and len(node.elts)>=2 and all(isinstance(n,ast.Constant) and isinstance(n.value,str) for n in node.elts[:2]):
   name,child=(n.value for n in node.elts[:2])
   if child in drivers:
    physical=old['service_alias_updates'].get(name,'recovery46_'+name);aliases[physical]=re.sub(r'^recovery46_','recovery49_',physical)
proof=A/'actual_failed_future202_206_routes49_admission_v1_20261011.json'
create(proof,{'status':'failed_gate_only_future202_to206_resume_actual47_publication_48_parent_chain_no_scientific_output_started_or_rerun','input_sha256':{str(p):sha(p) for p in dict.fromkeys(paths)},'service_alias_updates':aliases,'driver_wrappers':wrappers,'source_factories':old['source_factories'],'tasks':tasks,'original_failed_gates':evidence,'raw_score_and_publisher46_services_preserved':True,'new_fits_or_scores':0,'test_labels_read':False})
for name,driver in tasks:
 assert allowed();p=A/wrappers[driver];r=start_service(name,p.name,[],{str(p):sha(p),str(proof):sha(proof)});create(A/(name+'_activation.json'),r)
print({'actual_failed_future_helpers_resumed':len(tasks),'science_rerun':False},flush=True)
