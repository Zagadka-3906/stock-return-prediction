from pathlib import Path
import sys,subprocess,psutil
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
from handoff_ready_goss_full_execution_20261006 import retire

def save(p,s):
 assert not p.exists(),p;compile(s,str(p),'exec');p.write_text(s,encoding='utf8',newline='\n');return p

def main():
 assert allowed();old=A/'new_objectives_exact_source_recovery32_routes_v1_20261011.json';data=read(old);paths=[Path(__file__),old,A/'owned_idle_publication_wait_reboot_identity_v2_20261011.py',A/'publish_explicit_parent_training_round_external_frozen_v3_20261011.py'];overrides=data['source_overrides'].copy()
 for name in data['source_factories']:
  m=__import__(name)
  for filename in m.EXTRAS:
   if not filename.startswith('run_') or '_full_registration_' not in filename or not filename.endswith('.py'):continue
   p=A/filename;s=p.read_text(encoding='utf8')
   assert 'from owned_idle_publication_wait_runtime_v1_20261010 import hold' in s
   assert 'from publish_explicit_parent_training_round_v2_20261005 import publish' in s
   s=s.replace('main_publisher_v11_20261010/native_launch.json','main_publisher_reboot_v12_20261011/native_launch.json').replace('from owned_idle_publication_wait_runtime_v1_20261010 import hold','from owned_idle_publication_wait_reboot_identity_v2_20261011 import hold').replace('from publish_explicit_parent_training_round_v2_20261005 import publish','from publish_explicit_parent_training_round_external_frozen_v3_20261011 import publish')
   q=save(A/(p.stem+'_actual_reboot12_external_frozen_recovery33.py'),s);overrides[filename]=q.name;paths.extend([p,q])
 aliases={k:v.replace('recovery32_','recovery33_') if v.startswith('recovery32_') else v for k,v in data['service_aliases'].items()};wrappers={}
 route=A/'route_new_objectives_exact_source_recovery32_v1_20261011.py';newroute=save(A/route.name.replace('recovery32','recovery33'),route.read_text(encoding='utf8').replace('recovery32','recovery33'));paths.extend([route,newroute])
 for d,name in data['driver_wrappers'].items():
  p=A/name;q=save(A/name.replace('recovery32','recovery33'),p.read_text(encoding='utf8').replace('recovery32','recovery33'));wrappers[d]=q.name;paths.extend([p,q])
 audit=[]
 for n,d in data['remaining_tasks']:
  assert allowed();f=A/'service_owned_workflows_20261006'/data['service_aliases'][n];row=read(f/'native_launch.json');assert owned(row),n
  p=psutil.Process(row['owned_worker_pid']);assert not p.children(),n
  result=subprocess.run([str(ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(p.pid)],capture_output=True,text=True,timeout=30);assert result.returncode==0;stack=result.stdout;assert 'closed (' in stack,n
  retire(row,'Replace only verified childless dependency waiters with corrected actual watcher identity and frozen E-capsule publisher; live scientific jobs preserved')
  audit.append({'identity':row,'actual_idle_stack':stack})
 data.update(status='compiled_new_objectives_actual_reboot12_and_strict_external_frozen_publication33',service_aliases=aliases,driver_wrappers=wrappers,source_overrides=overrides,retired_only_actual_childless_dependency_waiters32=audit,new_fits=0,new_scores=0)
 data['input_sha256'].update({str(p):sha(p) for p in paths});proof=A/'new_objectives_exact_source_recovery33_routes_v1_20261011.json';create(proof,data)
 for n,d in data['remaining_tasks']:
  assert allowed();p=A/wrappers[d];r=start_service(aliases[n],p.name,[],{str(p):sha(p),str(proof):sha(proof)});create(A/(aliases[n]+'_activation.json'),r)
 print({'corrected_actual_publication33_workers':len(data['remaining_tasks']),'live_scoring_and_training_preserved':True},flush=True)
if __name__=='__main__':main()
