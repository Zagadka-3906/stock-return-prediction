from pathlib import Path
import sys,ast,time,re
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
assert allowed()
bridge=A/'verify_actual187_complete_QA_main_finally_bridge57_v2_20261011.py';r=start_service('actual187_complete_QA_main_finally_bridge57_v2_20261011',bridge.name,[],{str(bridge):sha(bridge)});create(A/'actual187_complete_bridge57_activation_v1_20261011.json',r)
oldproof=A/'actual_verified_current55_publication_runtime_admission_v1_20261011.json';data=read(oldproof)
paths=[A/'owned_idle_publication_wait_reboot_dynamic_boundary_v3_20261011.py',Path(__file__),oldproof,bridge,*[Path(p) for p in data['input_sha256']]]
route=A/'route_verified_current58_after_actual187_bridge_v1_20261011.py';s=(A/'route_verified_current55_publication_runtime_v1_20261011.py').read_text(encoding='utf8')
s=s.replace("PROOF=A/'actual_verified_current55_publication_runtime_admission_v1_20261011.json'","PROOF=A/'actual_verified_current58_after_actual187_bridge_admission_v1_20261011.json'")
needle="'actual_current_publication_paths_and_prospective53_admission_v1_20261011.json']:";assert s.count(needle)==1
s=s.replace(needle,"'actual_current_publication_paths_and_prospective53_admission_v1_20261011.json','actual_verified_current55_publication_runtime_admission_v1_20261011.json']:")
s=s.replace(" data['service_aliases'].update(proof['service_alias_updates']);data['driver_wrappers'].update(proof['driver_wrappers'])"," data['service_aliases'].update(proof['service_alias_updates']);data['driver_wrappers'].update(proof['driver_wrappers'])\n import owned_idle_publication_wait_reboot_identity_v2_20261011 as wait_module\n from owned_idle_publication_wait_reboot_dynamic_boundary_v3_20261011 import hold as actual_hold\n wait_module.hold=actual_hold")
assert s.count("PROOF=A/'actual_verified_current58_after_actual187_bridge_admission_v1_20261011.json'")==1;ast.parse(s);assert not route.exists();route.write_text(s,encoding='utf8');paths.append(route)
wrappers={}
for driver in data['driver_wrappers']:
 p=A/(Path(driver).stem+'_verified58_wrapper.py');t="from pathlib import Path\nimport sys\nA=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]\nfrom route_verified_current58_after_actual187_bridge_v1_20261011 import execute\nif __name__=='__main__':execute("+repr(driver)+")\n";ast.parse(t);assert not p.exists();p.write_text(t,encoding='utf8');paths.append(p);wrappers[driver]=p.name
aliases={'actual187_completed_QA_publication_only_resume47_v1_20261011':'actual187_complete_QA_main_finally_bridge57_v2_20261011'};tasks=[];failures=[]
for k,v in data['service_alias_updates'].items():
 if v.startswith('recovery55_'):aliases[v]=v.replace('recovery55_','recovery58_',1)
for name,driver in data['tasks']:
 f=A/'service_owned_workflows_20261006'/name
 while not (f/'service_execution.json').exists():assert allowed();time.sleep(2)
 t=read(f/'service_execution.json');assert t['status']=='failed' and not owned(read(f/'native_launch.json')),(name,t)
 new=name.replace('recovery55_','recovery58_',1);aliases[name]=new;tasks.append((new,driver));failures.append({'name':name,'terminal':t});paths.append(f/'service_execution.json')
proof=A/'actual_verified_current58_after_actual187_bridge_admission_v1_20261011.json'
create(proof,{'status':'actual187_completed_main_and_QA_finally_log_collision_bridged_all57_failed_gates_resume_without_science_rerun','input_sha256':{str(p):sha(p) for p in dict.fromkeys(paths)},'service_alias_updates':aliases,'driver_wrappers':wrappers,'source_factories':data['source_factories'],'tasks':tasks,'publication_module_corrections':data['publication_module_corrections'],'actual_family_folder_controls':data['actual_family_folder_controls'],'original_failed_gates':failures,'science_workers_restarted':0,'new_fits_or_scores':0,'test_labels_read':False})
for name,driver in tasks:
 assert allowed();p=A/wrappers[driver];r=start_service(name,p.name,[],{str(p):sha(p),str(proof):sha(proof)});create(A/(name+'_activation.json'),r)
print({'current58_future_helpers':57,'actual187_bridge':56,'scientific_rerun':False},flush=True)
