from pathlib import Path
import sys,ast,re,subprocess,psutil,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
assert allowed()
prior=A/'actual_current_publication_paths_and_prospective53_admission_v1_20261011.json';data=read(prior);assert len(data['publication_module_corrections'])==22 and len(data['tasks'])==57
proof=A/'actual_verified_current55_publication_runtime_admission_v1_20261011.json'
route=A/'route_verified_current55_publication_runtime_v1_20261011.py'
s=(A/'route_current_publication_paths_and_prospective50_v1_20261011.py').read_text(encoding='utf8')
declaration="PROOF=A/'actual_current_publication_paths_and_prospective50_admission_v1_20261011.json'";assert s.count(declaration)==1
s=s.replace(declaration,"PROOF=A/'actual_verified_current55_publication_runtime_admission_v1_20261011.json'")
needle="'actual_failed_future202_206_routes49_admission_v1_20261011.json']:";assert s.count(needle)==1
s=s.replace(needle,"'actual_failed_future202_206_routes49_admission_v1_20261011.json','actual_current_publication_paths_and_prospective50_admission_v1_20261011.json','actual_current_publication_paths_and_prospective53_admission_v1_20261011.json']:")
tree=ast.parse(s);actual=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='PROOF' for t in n.targets));assert actual.value.right.value==proof.name
assert s.count("proof['publication_module_corrections']")==1 and "proof['driver_wrappers']" in s
assert not route.exists();route.write_text(s,encoding='utf8')
paths=[Path(__file__),route,prior,*[Path(p) for p in data['input_sha256']]];wrappers={}
for driver in data['driver_wrappers']:
 p=A/(Path(driver).stem+'_verified55_wrapper.py');text="from pathlib import Path\nimport sys\nA=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]\nfrom route_verified_current55_publication_runtime_v1_20261011 import execute\nif __name__=='__main__':execute("+repr(driver)+")\n";ast.parse(text);assert not p.exists();p.write_text(text,encoding='utf8');paths.append(p);wrappers[driver]=p.name
pending=[]
for name,driver in data['tasks']:
 f=A/'service_owned_workflows_20261006'/name
 while not (f/'native_launch.json').exists():assert allowed();time.sleep(1)
 row=read(f/'native_launch.json');terminal=read(f/'service_execution.json') if (f/'service_execution.json').exists() else None
 if terminal:assert terminal['status']=='failed' and not owned(row),(name,terminal);spy=None
 else:
  assert owned(row),name;spy=subprocess.run([str(A.parent/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(row['owned_worker_pid'])],capture_output=True,text=True,encoding='utf8',check=True).stdout
  assert 'closed (' in spy and '(idle)' in spy and Path(driver).stem in spy,(name,spy)
 pending.append((name,driver,row,terminal))
aliases={};tasks=[];retired=[]
for k,v in data['service_alias_updates'].items():
 if v.startswith('recovery53_'):aliases[v]=v.replace('recovery53_','recovery55_',1)
for name,driver,row,terminal in pending:
 if terminal:retired.append({'name':name,'original_failure':terminal})
 else:
  spy=subprocess.run([str(A.parent/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(row['owned_worker_pid'])],capture_output=True,text=True,encoding='utf8',check=True).stdout
  assert 'closed (' in spy and '(idle)' in spy and Path(driver).stem in spy,(name,spy)
  worker=psutil.Process(row['owned_worker_pid']);parent=psutil.Process(row['pid']);assert not worker.children() and worker.create_time()==row['owned_worker_creation_time'] and parent.create_time()==row['owned_parent_creation_time']
  worker.terminate();worker.wait(timeout=15);parent.terminate();parent.wait(timeout=15)
  item={'name':name,'identity':row,'actual_idle_stack':spy,'scientific_workers_stopped':0};create(A/'service_owned_workflows_20261006'/name/'administrative_verified55_runtime_supersession.json',item);retired.append(item)
 new=name.replace('recovery53_','recovery55_',1);aliases[name]=new;tasks.append((new,driver))
create(proof,{'status':'actual_prospective55_explicit_new_proof_binding_verified_22_corrected_publisher_modules_and_all57_idle_helpers','input_sha256':{str(p):sha(p) for p in dict.fromkeys(paths)},'service_alias_updates':aliases,'driver_wrappers':wrappers,'source_factories':data['source_factories'],'tasks':tasks,'publication_module_corrections':data['publication_module_corrections'],'actual_family_folder_controls':data['actual_family_folder_controls'],'retired_idle_helpers':retired,'original53_wrong_proof_binding_preserved':True,'science_workers_restarted':0,'new_fits_or_scores':0,'test_labels_read':False})
for name,driver in tasks:
 assert allowed();p=A/wrappers[driver];r=start_service(name,p.name,[],{str(p):sha(p),str(proof):sha(proof)});create(A/(name+'_activation.json'),r)
print({'actual_current55_helpers':57,'corrected_publisher_modules':22,'science_rerun':False},flush=True)
