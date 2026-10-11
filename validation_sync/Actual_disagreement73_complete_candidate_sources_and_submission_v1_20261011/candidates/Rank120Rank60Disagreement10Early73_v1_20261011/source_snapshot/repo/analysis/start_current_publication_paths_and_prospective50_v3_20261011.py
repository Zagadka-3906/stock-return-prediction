from pathlib import Path
from types import ModuleType
import sys,ast,importlib,subprocess,psutil,re
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
assert allowed()
p48=A/'actual_nested_dispatch_and_complete_aliases48_admission_v1_20261011.json';p49=A/'actual_failed_future202_206_routes49_admission_v1_20261011.json';old48=read(p48);old49=read(p49)
pending=[]
for name,driver in old48['tasks']+old49['tasks']:
 f=A/'service_owned_workflows_20261006'/name;row=read(f/'native_launch.json');terminal=read(f/'service_execution.json') if (f/'service_execution.json').exists() else None
 if terminal:assert terminal['status']=='failed' and not owned(row),(name,terminal);spy=None
 else:
  assert owned(row),name
  spy=subprocess.run([str(A.parent/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(row['owned_worker_pid'])],capture_output=True,text=True,encoding='utf8',check=True).stdout
  assert 'closed (' in spy and '(idle)' in spy and Path(driver).stem in spy,(name,spy)
 pending.append((name,driver,row,terminal,spy))
assert len(pending)==57
pubs={};paths=[Path(__file__),p48,p49]
for obj in (old48,old49):
 for p in obj['input_sha256']:
  q=Path(p)
  if q.name.startswith('publish_') and '_full_validation_' in q.name and q.suffix=='.py':pubs[q.stem]=q
for name in old49['source_factories']:
 m=importlib.import_module(name)
 for q in m.source_paths():
  if q.name.startswith('publish_') and '_full_validation_' in q.name and q.suffix=='.py':pubs[q.stem]=q
corrections={};controls=[]
for module,source in pubs.items():
 text=source.read_text(encoding='utf8');lines=text.splitlines();changes=0
 for i,line in enumerate(lines):
  if "for family in tuple(f['name']+'_screen_v1_20261010'" not in line:continue
  expression=line.strip()[len('for family in tuple('):].rsplit('):',1)[0]
  match=re.search(r"for f in (read\(A/'[^']+'\)\['families'\])",expression);assert match,source
  assert lines[i+1].strip()=="folder=Path('E:/赛题五_本机临时')/family",source
  lines[i]='    for family in '+match.group(1)+':'
  lines[i+1]="        choices=[Path(family['output'])] if family.get('output') else [Path('E:/赛题五_本机临时')/(family['name']+'_screen_v1_'+date) for date in ('20261010','20261011')]\n        existing=[p for p in choices if (p/'verification.json').is_file()]\n        assert len(existing)==1,(family,choices)\n        folder=existing[0];assert family.get('records',len(read(folder/'verification.json')['records']))==len(read(folder/'verification.json')['records'])"
  plan=read(A/re.search(r"read\(A/'([^']+)'",match.group(1)).group(1))
  for family in plan['families']:
   choices=[Path(family['output'])] if family.get('output') else [Path('E:/赛题五_本机临时')/(family['name']+'_screen_v1_'+date) for date in ('20261010','20261011')]
   existing=[p for p in choices if (p/'verification.json').exists()]
   if existing:assert len(existing)==1 and len(read(existing[0]/'verification.json')['records'])==family.get('records',len(read(existing[0]/'verification.json')['records'])),(source,family)
   controls.append({'publisher':str(source),'family':family,'actual_existing_folder':str(existing[0]) if existing else None,'pending_raw_validation_explicitly_not_completed':not bool(existing)})
  changes+=1
 if not changes:continue
 assert changes==1,source
 text='\n'.join(lines)+'\n';ast.parse(text);target=A/(source.stem+'_actual_family_paths51.py');assert not target.exists();target.write_text(text,encoding='utf8');corrections[module]=target.name;paths.extend((source,target))
route=A/'route_current_publication_paths_and_prospective50_v1_20261011.py'
s=(A/'route_failed_future202_206_after_completed187_v49_20261011.py').read_text(encoding='utf8').replace("PROOF=A/'actual_failed_future202_206_routes49_admission_v1_20261011.json'","PROOF=A/'actual_current_publication_paths_and_prospective50_admission_v1_20261011.json'")
s=s.replace("'actual_nested_dispatch_and_complete_aliases48_admission_v1_20261011.json']","'actual_nested_dispatch_and_complete_aliases48_admission_v1_20261011.json','actual_failed_future202_206_routes49_admission_v1_20261011.json']")
s=s.replace(" data['service_aliases'].update(proof['service_alias_updates']);data['driver_wrappers'].update(proof['driver_wrappers'])", " data['service_aliases'].update(proof['service_alias_updates']);data['driver_wrappers'].update(proof['driver_wrappers'])\n from types import ModuleType\n for name,filename in proof['publication_module_corrections'].items():\n  q=A/filename;module=ModuleType(name);module.__file__=str(q);exec(compile(q.read_text(encoding='utf8'),str(q),'exec'),module.__dict__);sys.modules[name]=module")
ast.parse(s);assert not route.exists();route.write_text(s,encoding='utf8');paths.append(route)
drivers={**old48['driver_wrappers'],**old49['driver_wrappers']};wrappers={}
for driver in drivers:
 p=A/(Path(driver).stem+'_current50_wrapper.py');t="from pathlib import Path\nimport sys\nA=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]\nfrom route_current_publication_paths_and_prospective50_v1_20261011 import execute\nif __name__=='__main__':execute("+repr(driver)+")\n";ast.parse(t);assert not p.exists();p.write_text(t,encoding='utf8');wrappers[driver]=p.name;paths.append(p)
aliases={};tasks=[];retired=[]
for obj in (old48,old49):
 for k,v in obj['service_alias_updates'].items():
  if re.match(r'^recovery(48|49)_',v):aliases[v]=re.sub(r'^recovery(48|49)_','recovery50_',v)
for name,driver,row,terminal,spy in pending:
 if terminal:retired.append({'name':name,'original_failure':terminal})
 else:
  latest=subprocess.run([str(A.parent/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(row['owned_worker_pid'])],capture_output=True,text=True,encoding='utf8',check=True).stdout
  assert 'closed (' in latest and '(idle)' in latest and Path(driver).stem in latest,(name,latest)
  worker=psutil.Process(row['owned_worker_pid']);parent=psutil.Process(row['pid']);assert not worker.children() and worker.create_time()==row['owned_worker_creation_time'] and parent.create_time()==row['owned_parent_creation_time']
  worker.terminate();worker.wait(timeout=15);parent.terminate();parent.wait(timeout=15)
  item={'name':name,'identity':row,'actual_idle_stack_before_retirement':latest,'scientific_workers_stopped':0};create(A/'service_owned_workflows_20261006'/name/'administrative_idle_publication_path_supersession50.json',item);retired.append(item)
 new=re.sub(r'^recovery(48|49)_','recovery50_',name);aliases[name]=new;tasks.append((new,driver))
proof=A/'actual_current_publication_paths_and_prospective50_admission_v1_20261011.json'
create(proof,{'status':'actual_idle_only57_future_helpers_unified_all_actual_family_output_paths_checked_no_score_or_native_math_changes','input_sha256':{str(p):sha(p) for p in dict.fromkeys(paths)},'service_alias_updates':aliases,'driver_wrappers':wrappers,'source_factories':old49['source_factories'],'tasks':tasks,'publication_module_corrections':corrections,'actual_family_folder_controls':controls,'retired_idle_helpers':retired,'science_workers_restarted':0,'new_fits_or_scores':0,'test_labels_read':False})
for name,driver in tasks:
 assert allowed();p=A/wrappers[driver];r=start_service(name,p.name,[],{str(p):sha(p),str(proof):sha(proof)});create(A/(name+'_activation.json'),r)
print({'actual_current_helpers':len(tasks),'publication_modules_corrected':len(corrections),'science_rerun':False},flush=True)
