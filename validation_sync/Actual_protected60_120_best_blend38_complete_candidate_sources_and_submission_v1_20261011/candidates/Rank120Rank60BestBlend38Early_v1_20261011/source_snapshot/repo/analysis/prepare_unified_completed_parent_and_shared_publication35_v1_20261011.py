from pathlib import Path
import sys,importlib,re
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from start_fast_completed_owned_service_v1_20261011 import start_service
def save(p,s):
 assert not p.exists(),p;compile(s,str(p),'exec');p.write_text(s,encoding='utf8',newline='\n');return p
def main():
 assert allowed();closed('actual_shared_publication_board_loader_controls_v1_20261011');closed('actual184_registered_QA_main_complete_parent_bridge30_v1_20261011')
 p31=A/'completed_score_parent_chain_recovery31_routes_v1_20261011.json';p34=A/'new_objectives_exact_source_recovery34_routes_v1_20261011.json';p196=A/'stock_rank20class10_latest183_complete196_exact_routes_v3_20261011.json';a=read(p31);b=read(p34);c=read(p196)
 aliases={**a['service_aliases'],**b['service_aliases'],**c['service_aliases']};overrides={**a['actual_source_overrides'],**b['source_overrides'],**c['source_overrides']};factories=list(dict.fromkeys([*a['source_factories'],*b['source_factories'],'prepare_StockRank20Class10Embedding195_complete48_pipeline_v1_20261011','prepare_StockRank20Class10Embedding196_complete19_pipeline_v2_20261011','prepare_StockRank20Class25Embedding197_complete48_pipeline_v1_20261011']))
 tasks=list(a['remaining_tasks'][1:])+[(b['service_aliases'][n],d) for n,d in b['remaining_tasks']]
 class_tasks=[('actual_stock_rank20class10_embedding48_after194_normalization_queue_v1_20261011','qualify',195),('StockRank20Class10Embedding48_selected_native14_v1_20261011','native',195),('StockRank20Class10Embedding195_complete48_family_v1_20261011','family',195),('actual_stock_rank20class10_embedding19_after195_normalization_exact_v3_20261011','qualify',196),('StockRank20Class10Embedding19_selected_native14_v1_20261011','native',196),('StockRank20Class10Embedding196_complete19_family_v1_20261011','family',196),('actual_stock_rank20class25_embedding48_after196_normalization_queue_v1_20261011','qualify',197),('StockRank20Class25Embedding48_selected_native14_v1_20261011','native',197),('StockRank20Class25Embedding197_complete48_family_v1_20261011','family',197)]
 for n,kind,number in class_tasks:
  m=importlib.import_module(next(f for f in factories if f'Embedding{number}_complete' in f));tasks.append((n,m.EXTRAS[{'qualify':0,'native':1,'family':5}[kind]]))
 for n,d in tasks:
  f=A/'service_owned_workflows_20261006'/n;assert read(f/'service_execution.json')['status']=='failed' and not owned(read(f/'native_launch.json')),n
 names={n:'recovery35_'+re.sub(r'^recovery\d+_','',n) for n,d in tasks}
 for k,v in list(aliases.items()):
  if v in names:aliases[k]=names[v]
  elif (v.startswith('recovery31_') or v.startswith('recovery34_')) and any(str(n) in v for n in range(185,195)) and any(t in v for t in ('preparation','sealing','full_registration')):aliases[k]='recovery35_'+re.sub(r'^recovery\d+_','',v)
 aliases.update(names)
 paths=[Path(__file__),p31,p34,p196,A/'verified_shared_publication_board_loader_v1_20261011.py',A/'verified_shared_publication_board_loader_actual_complete180_controls_v1_20261011.json'];drivers={};mods={}
 for f in factories:
  if not any(str(n) in f for n in range(185,198)):continue
  m=importlib.import_module(f)
  for d in m.EXTRAS:
   if not d.endswith('.py'):continue
   drivers[d]=None
   if d.startswith('seal_'):
    old=A/overrides.get(d,d);s=old.read_text(encoding='utf8');lines=[x for x in s.splitlines() if x.strip().startswith("service=A/'service_owned_workflows_20261006/")];assert len(lines)==1,d
    line=lines[0];prior=line.split('service_owned_workflows_20261006/')[1].rstrip("'");canonical=re.sub(r'^recovery\d+_','',prior);actual='recovery35_'+canonical;aliases[canonical]=actual;aliases[prior]=actual
    s=s.replace(line,line.replace(prior,actual));q=save(A/(Path(d).stem+'_actual_sealer_identity_recovery35.py'),s);overrides[d]=q.name;paths.extend([old,q])
   elif d.startswith('run_') and '_full_registration_' in d:
    old=A/overrides.get(d,d);s=old.read_text(encoding='utf8');assert 'from late_bound_dynamic_snapshot_encoder_runtime_v1_20261010 import installed' in s
    s=s.replace('from late_bound_dynamic_snapshot_encoder_runtime_v1_20261010 import installed','from late_bound_shared_snapshot_encoder_runtime_v1_20261011 import installed')
    q=save(A/(Path(d).stem+'_actual_shared_publication_recovery35.py'),s);overrides[d]=q.name;paths.extend([old,q])
  if any(str(n) in f for n in (195,196,197)):
   for d in (m.EXTRAS[3],m.EXTRAS[4],m.EXTRAS[6],m.EXTRAS[8]):
    stem=Path(d).stem
    if '_selected_candidate_feature_cache_' in stem:service=stem.replace('run_','',1).replace('_selected_candidate_feature_cache_','_selected_candidate_preparation_')
    elif stem.startswith('seal_'):service=stem.replace('seal_','',1).replace('_selected_candidate_','_selected_candidate_sealing_')
    elif stem.startswith('run_') and '_full_registration_' in stem:
     number=next(n for n in (195,196,197) if f'Embedding{n}' in stem);service=stem.replace('run_','',1).replace('_full_registration_',f'_round{number}_full_registration_')
    else:continue
    aliases[service]='recovery35_'+service
 for n,d in tasks:drivers[d]=None
 # Build wrappers for all prior routed drivers, including candidate runpy targets.
 for d in [*a['driver_wrappers'],*b['driver_wrappers'],*c['driver_wrappers']]:drivers[d]=None
 wrappers={}
 for d in drivers:
  p=save(A/(Path(d).stem+'_unified_parent_shared_publication35_wrapper.py'),"from pathlib import Path\nimport sys\nA=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]\nfrom route_unified_completed_parent_shared_publication35_v1_20261011 import execute\nif __name__=='__main__':execute("+repr(d)+")\n");wrappers[d]=p.name;paths.append(p)
 route=A/'route_completed_score_parent_chain_recovery31_v1_20261011.py';s=route.read_text(encoding='utf8').replace('completed_score_parent_chain_recovery31_routes_v1_20261011.json','unified_completed_parent_shared_publication35_routes_v1_20261011.json')
 needle="        if level==0 and name=='register_StockRank20Embedding183_round183_artifacts_v3_20261010':"
 toppair=importlib.import_module('prepare_StockTopPairEmbedding185_complete48_pipeline_v1_20261010').EXTRAS[0]
 assert needle in s;s=s.replace(needle,"        if level==0 and name=='normalize_completed_stock_toppair_embedding_complete48_after184_v6_20261010':\n            return previous_import("+repr(Path(toppair).stem)+",globals,locals,fromlist,level)\n"+needle)
 newroute=save(A/'route_unified_completed_parent_shared_publication35_v1_20261011.py',s);paths.extend([route,newroute,A/'late_bound_shared_snapshot_encoder_runtime_v1_20261011.py'])
 pins={**a['input_sha256'],**b['input_sha256'],**c['input_sha256'],**{str(p):sha(p) for p in paths}}
 proof=A/'unified_completed_parent_shared_publication35_routes_v1_20261011.json';create(proof,{'status':'compiled_all185197_failed_administrative_tasks_missing_v6_import_fixed_and_verified_shared_board_publication35','input_sha256':pins,'service_aliases':aliases,'driver_wrappers':wrappers,'actual_source_overrides':overrides,'source_factories':factories,'remaining_tasks':[(names[n],d) for n,d in tasks],'normal185_passed31_reused':True,'actual184_complete_bridge30_reused':True,'new_fits':0,'new_scores':0,'all_original_failures_preserved':True,'live_scientific_jobs_preserved':True})
 for n,d in tasks:
  assert allowed();p=A/wrappers[d];r=start_service(names[n],p.name,[],{str(p):sha(p),str(proof):sha(proof)});create(A/(names[n]+'_activation.json'),r)
 print({'actual_unified35_administrative_workers_dispatched':len(tasks),'new_fits_or_scores':0},flush=True)
if __name__=='__main__':main()
