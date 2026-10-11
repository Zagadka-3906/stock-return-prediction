"""Recover186 after registration, then replace only failed dependent helpers with fresh identities."""
from pathlib import Path
import sys,re,ast,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
def save(p,s):
 assert not p.exists(),p;ast.parse(s);p.write_text(s,encoding='utf8');return p
def main():
 assert allowed();d36=read(A/'unified_completed_parent_shared_publication36_routes_v1_20261011.json');d37=read(A/'actual_latest183_parent196198_routes37_v1_20261011.json')
 factories=list(dict.fromkeys([*d36['source_factories'],*d37['source_factories'],'prepare_Rank60Rank20Mixed199_complete51_pipeline_v1_20261011','prepare_StockRank60Direct200_complete35_pipeline_v6_20261011']))
 catalog={d:n for n,d in [*d36['remaining_tasks'],*d37['tasks']]}
 catalog.update({'normalize_completed_rank60_rank20_mixed51_after198_v1_20261011.py':'actual_rank60_rank20_mixed51_after198_normalization_v1_20261011','qualify_rank60_rank20_mixed51_selected_native14_v1_20261011.py':'actual_rank60_rank20_mixed51_selected_native14_v1_20261011','run_Rank60Rank20Mixed199_complete_family_v4_20261011.py':'Rank60Rank20Mixed199_complete51_family_v4_20261011','normalize_completed_stock_rank60_direct_embedding_complete35_after199_v6_20261011.py':'actual_stock_rank60_direct_embedding35_after199_normalization_queue_v6_20261011','qualify_stock_rank60_direct_embedding35_selected_native14_v6_20261011.py':'StockRank60DirectEmbedding35_selected_native14_v6_20261011','run_StockRank60DirectEmbedding200_complete_family_v6_20261011.py':'StockRank60DirectEmbedding200_complete35_family_v6_20261011'})
 aliases={**d36['service_aliases'],**d37['service_aliases']};overrides=dict(d37['actual_source_overrides']);module_aliases={};tasks=[];files=[Path(__file__),A/'route_verified_canonical_publication_and_failed_chain38_v1_20261011.py'];adopted=[]
 from verify_protected162_full_family_preflight_v1_20261010 import literal_assignments
 for f in factories:
  m=importlib.import_module(f);number=literal_assignments(A/m.NAMES[2])['NUMBER']
  if number<186:continue
  adopted.append(f);files.extend(A/n for n in m.NAMES[2:4])
  for prefix,index in [('optimize_training_round',2),('finalize_training_round',3)]:module_aliases[prefix+str(number)]=Path(m.NAMES[index]).stem
  if number==186:continue
  for index in (0,1,5):
   driver=m.EXTRAS[index];old=catalog[driver];folder=A/'service_owned_workflows_20261006'/old
   assert read(folder/'service_execution.json')['status']=='failed' and not owned(read(folder/'native_launch.json')),old
   new='recovery38_'+re.sub(r'^recovery\d+_','',old);aliases[old]=new;tasks.append((new,driver))
  family=(A/m.EXTRAS[5]).read_text(encoding='utf8')
  launches=re.findall(r"\('([^']+)',\s*'([^']+\.py)'\)",family);assert len(launches)==3,f
  for n,d in launches:aliases[n]='recovery38_'+n
  sealer=m.EXTRAS[4];source=A/overrides.get(sealer,sealer);s=source.read_text(encoding='utf8');line=next(l for l in s.splitlines() if "service=A/'service_owned_workflows_20261006/" in l)
  oldgate=line.split('service_owned_workflows_20261006/')[1].rstrip("'");canonical=re.sub(r'^recovery\d+_','',oldgate)
  p=save(A/(Path(sealer).stem+'_actual_preparation_identity38.py'),s.replace(line,line.replace(oldgate,'recovery38_'+canonical)));overrides[sealer]=p.name;files.extend([source,p])
 # The old186 worker is terminal before publish(), with registration already on disk.
 folder=A/'service_owned_workflows_20261006/recovery15_StockRank20Seed10Embedding186_round186_full_registration_v1_20261010';assert read(folder/'service_execution.json')['failure']=="ModuleNotFoundError: No module named 'optimize_training_round186'" and not owned(read(folder/'native_launch.json'))
 source=A/'run_StockRank20Seed10Embedding186_full_registration_v2_20261011_actual_shared_publication_recovery35.py';s=source.read_text(encoding='utf8')
 needle="    protocol=register();folder=A/'optimization_20261003_r186'";assert s.count(needle)==1
 s=s.replace(needle,"    folder=A/'optimization_20261003_r186';protocol=read(folder/'protocol.json')")
 s=s.replace('frozen_before_actual_full_registration.json','frozen_before_actual_registered_publish_resume38.json').replace('actual_main7_idle_before_and_after_hold.json','actual_main12_idle_before_and_after_hold_resume38.json').replace('safe_full_main_v1_20261010','safe_full_main_resume38_v1_20261011').replace("folder/'full_registration_failure.json'","folder/'full_registration_resume38_failure.json'")
 p=save(A/'run_StockRank20Seed10Embedding186_registered_QA_main_resume38_v1_20261011.py',s);files.extend([source,p]);resume=p.name;tasks.insert(0,('actual186_registered_QA_main_resume38_v1_20261011',resume))
 # Bridge only the actually completed186 full registration; keep failed family36 receipts intact.
 oldbridge=A/'verify_actual184_registered_QA_main_complete_parent_bridge30_v1_20261011.py';s=oldbridge.read_text(encoding='utf8').replace('actual184_registered_QA_main_resume29_v1_20261011','actual186_registered_QA_main_resume38_v1_20261011').replace('StockPairRankEmbedding184','StockRank20Seed10Embedding186').replace('17306','17402').replace('QA95','QA97').replace('184','186').replace('bridge30','bridge38')
 s=s.replace("ready['selected_configuration']['anchor_round']==183","ready['selected_configuration']['anchor_round']==185")
 bridge=save(A/'verify_actual186_registered_QA_main_complete_parent_bridge38_v1_20261011.py',s);files.extend([oldbridge,bridge])
 bridge_name='actual186_complete_parent_bridge38_v1_20261011';aliases['recovery36_StockRank20Seed10Embedding186_complete48_family_v2_20261011']=bridge_name;tasks.insert(1,(bridge_name,bridge.name))
 # Flatten old canonical names to the fresh real successors.
 for k in list(aliases):
  n=aliases[k];seen={k}
  while n in aliases and aliases[n]!=n and n not in seen:seen.add(n);n=aliases[n]
  aliases[k]=n
 drivers={d for n,d in tasks}
 for f in adopted:
  m=importlib.import_module(f);drivers.update(d for d in m.EXTRAS if d.endswith('.py'))
 wrappers={}
 for driver in drivers:
  p=save(A/(Path(driver).stem+'_canonical_publication_chain38_wrapper.py'),"from pathlib import Path\nimport sys\nA=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]\nfrom route_verified_canonical_publication_and_failed_chain38_v1_20261011 import execute\nif __name__=='__main__':execute("+repr(driver)+")\n");wrappers[driver]=p.name;files.append(p)
 proof=A/'verified_canonical_publication_failed_chain38_routes_v1_20261011.json'
 create(proof,{'status':'canonical_dynamic_publication_module_aliases_and_actual_failed_dependency_chain_fresh38','input_sha256':{str(p):sha(p) for p in files},'canonical_publication_module_aliases':module_aliases,'service_aliases':aliases,'actual_source_overrides':overrides,'driver_wrappers':wrappers,'source_factories':adopted,'tasks':tasks,'new_fits':0,'new_scores':0,'failed_logs_preserved':True,'full186_registration_reused_not_rerun':True})
 for name,driver in tasks:
  assert allowed();p=A/wrappers[driver];r=start_service(name,p.name,[],{str(p):sha(p),str(proof):sha(proof)});create(A/(name+'_activation.json'),r)
 print({'actual38_recovery_services_started':len(tasks),'publication_module_aliases':len(module_aliases),'no_scientific_refit_or_rescore':True},flush=True)
if __name__=='__main__':main()
