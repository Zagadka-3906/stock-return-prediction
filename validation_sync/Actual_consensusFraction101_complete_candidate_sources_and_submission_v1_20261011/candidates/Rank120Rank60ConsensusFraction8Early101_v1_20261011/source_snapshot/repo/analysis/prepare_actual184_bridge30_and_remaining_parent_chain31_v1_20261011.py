from pathlib import Path
import sys,importlib
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
def save(p,s):
 assert not p.exists(),p;compile(s,str(p),'exec');p.write_text(s,encoding='utf8',newline='\n');return p
def main():
 assert allowed();old=A/'completed_score_parent_chain_recovery24_routes_v1_20261011.json';data=read(old);tasks=data['remaining_tasks'][1:];names={n:n.replace('recovery24_','recovery31_') for n,d in tasks};aliases=data['service_aliases'].copy();aliases.update(names)
 bridge='actual184_registered_QA_main_complete_parent_bridge30_v1_20261011'
 for k,v in list(aliases.items()):
  if 'StockPairRankEmbedding184_complete48_family' in v:aliases[k]=bridge
  elif v in names:aliases[k]=names[v]
  elif v.startswith('recovery24_') and any(str(n) in k for n in range(185,192)) and any(t in k for t in ('preparation','sealing','full_registration')):aliases[k]=v.replace('recovery24_','recovery31_')
 route=A/'route_completed_score_parent_chain_recovery24_v1_20261011.py';newroute=save(A/route.name.replace('recovery24','recovery31'),route.read_text(encoding='utf8').replace('recovery24','recovery31'));paths=[Path(__file__),old,route,newroute,A/'verify_actual184_registered_QA_main_complete_parent_bridge30_v1_20261011.py',A/'publish_explicit_parent_training_round_external_frozen_v3_20261011.py',A/'actual_external_frozen_publication183184_capsule_controls_v3_20261011.json',A/'owned_idle_publication_wait_reboot_identity_v2_20261011.py'];overrides=data['actual_source_overrides'].copy()
 for factory in data['source_factories']:
  if not any(str(n) in factory for n in range(185,192)):continue
  m=importlib.import_module(factory)
  for filename in m.EXTRAS:
   if not filename.startswith('run_') or '_full_registration_' not in filename or not filename.endswith('.py'):continue
   p=A/filename;s=p.read_text(encoding='utf8')
   assert 'publish_explicit_parent_training_round_v2_20261005' in s,filename
   s=s.replace('main_publisher_v11_20261010/native_launch.json','main_publisher_reboot_v12_20261011/native_launch.json').replace('from owned_idle_publication_wait_runtime_v1_20261010 import hold','from owned_idle_publication_wait_reboot_identity_v2_20261011 import hold').replace('from publish_explicit_parent_training_round_v2_20261005 import publish','from publish_explicit_parent_training_round_external_frozen_v3_20261011 import publish')
   q=save(A/(p.stem+'_actual_reboot12_external_frozen_recovery31.py'),s);overrides[filename]=q.name;paths.extend([p,q])
 wrappers={}
 for d,name in data['driver_wrappers'].items():
  oldp=A/name;q=save(A/name.replace('recovery24','recovery31'),oldp.read_text(encoding='utf8').replace('recovery24','recovery31'));wrappers[d]=q.name;paths.extend([oldp,q])
 for n,d in tasks:
  f=A/'service_owned_workflows_20261006'/n;assert read(f/'service_execution.json')['status']=='failed' and not owned(read(f/'native_launch.json')),n
 data.update(status='compiled_remaining185191_with_actual184_complete_bridge30_reboot12_watcher_and_strict_external_frozen_capsule_checks',service_aliases=aliases,driver_wrappers=wrappers,actual_source_overrides=overrides,remaining_tasks=[(names[n],d) for n,d in tasks],new_fits=0,new_scores=0)
 data['input_sha256'].update({str(p):sha(p) for p in paths});proof=A/'completed_score_parent_chain_recovery31_routes_v1_20261011.json';create(proof,data)
 driver='verify_actual184_registered_QA_main_complete_parent_bridge30_v1_20261011.py';p=A/driver;assert allowed();r=start_service(bridge,driver,[],{str(p):sha(p),str(proof):sha(proof)});create(A/(bridge+'_activation.json'),r)
 for n,d in tasks:
  assert allowed();p=A/wrappers[d];r=start_service(names[n],p.name,[],{str(p):sha(p),str(proof):sha(proof)});create(A/(names[n]+'_activation.json'),r)
 print({'actual184_complete_bridge_and_parent31_workers':len(tasks)+1,'new_fits_or_scores':0},flush=True)
if __name__=='__main__':main()
