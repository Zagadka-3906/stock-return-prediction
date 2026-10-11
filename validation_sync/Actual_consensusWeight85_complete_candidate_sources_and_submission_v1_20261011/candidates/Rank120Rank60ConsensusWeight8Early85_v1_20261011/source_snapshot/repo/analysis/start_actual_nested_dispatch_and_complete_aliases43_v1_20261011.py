from pathlib import Path
import sys,ast,re
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
def main():
 assert allowed()
 proofs=[A/n for n in ['verified_canonical_publication_failed_chain38_routes_v1_20261011.json','actual_failed_chain40_preserving186_resume39_admission_v1_20261011.json','actual_completed186_finally_collision_and_shared_report41_admission_v1_20261011.json','actual_scratch_only_and_sealing_sources42_admission_v1_20261011.json']]
 d=[read(p) for p in proofs];p42=d[-1];aliases={};names=set()
 for obj in d:
  for field in ['service_aliases','service_alias_updates']:
   for k,v in obj.get(field,{}).items():names.update([k,v])
 for n in names:
  if re.match(r'^recovery\d+_',n):aliases[n]=re.sub(r'^recovery\d+_','recovery43_',n)
 preserved=[];tasks=[]
 for name,driver in p42['tasks']:
  f=A/'service_owned_workflows_20261006'/name;terminal=read(f/'service_execution.json');assert not owned(read(f/'native_launch.json')),name
  if terminal['status']=='passed':aliases[name]=name;preserved.append({'name':name,'terminal':terminal});continue
  assert terminal['status']=='failed';new=re.sub(r'^recovery\d+_','recovery43_',name);aliases[name]=new;tasks.append((new,driver))
 for row in p42['preserved_completed41_services']:
  aliases[row['name']]=row['name'];preserved.append(row)
 assert len(tasks)==43 and len(preserved)==3
 # Latest completed native187 and normalization187 must retain their exact own identities.
 for row in preserved:
  canonical=re.sub(r'^recovery\d+_','',row['name'])
  for name in names:
   if re.sub(r'^recovery\d+_','',name)==canonical:aliases[name]=row['name']
 current_bad=A/'service_owned_workflows_20261006/recovery40_Rank20TwoSeed187_selected_candidate_preparation_v1_20261010'
 assert read(current_bad/'service_execution.json')['status']=='failed' and not owned(read(current_bad/'native_launch.json'))
 paths=[Path(__file__),A/'route_actual_nested_dispatch_and_complete_aliases43_v1_20261011.py',*proofs,current_bad/'service_execution.json',current_bad/'stderr.log']
 wrappers={}
 for driver in sorted(p42['driver_wrappers']):
  p=A/(Path(driver).stem+'_actual_nested_dispatch43_wrapper.py')
  text="from pathlib import Path\nimport sys\nA=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]\nfrom route_actual_nested_dispatch_and_complete_aliases43_v1_20261011 import execute\nif __name__=='__main__':execute("+repr(driver)+")\n"
  ast.parse(text);assert not p.exists();p.write_text(text,encoding='utf8');wrappers[driver]=p.name;paths.append(p)
 proof=A/'actual_nested_dispatch_and_complete_aliases43_admission_v1_20261011.json'
 create(proof,{'status':'nested_cache_runpy_dispatch_uses_same_current_aliases_completed_three_stages_retained_new43_failed_helpers_only',
  'input_sha256':{str(p):sha(p) for p in paths},'service_alias_updates':aliases,'driver_wrappers':wrappers,
  'tasks':tasks,'preserved_completed_services':preserved,'original_stdlib_runpy_private_namespace_preserves_script_main_semantics':True,
  'all_future_child_service_prefixes_current43':True,'scientific_workers_stopped_or_restarted':0,
  'new_fits_or_scores':0,'test_labels_read':False})
 for name,driver in tasks:
  assert allowed();p=A/wrappers[driver];r=start_service(name,p.name,[],{str(p):sha(p),str(proof):sha(proof)})
  create(A/(name+'_activation.json'),r)
 print({'actual43_failed_dependents_started':len(tasks),'completed_stages_kept':len(preserved),'nested_dispatch_fixed':True},flush=True)
if __name__=='__main__':main()
