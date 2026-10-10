from pathlib import Path
import sys,ast
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
def main():
 assert allowed()
 from native_scratch_only_mkdir_scope_v1_20261011 import installed
 sandbox=Path('E:/赛题五_本机临时/native_scratch_only_mkdir_actual42_controls_v1_20261011');assert not sandbox.exists();sandbox.mkdir()
 good=sandbox/'good';(good/'tmp').mkdir(parents=True)
 original=Path.mkdir
 with installed(good) as events:good.mkdir(exist_ok=False)
 assert Path.mkdir is original and len(events)==1
 bad=sandbox/'bad';bad.mkdir();(bad/'pilot.json').write_text('{}',encoding='utf8')
 try:
  with installed(bad):bad.mkdir(exist_ok=False)
 except AssertionError:pass
 else:raise AssertionError('Existing scientific output admitted')
 assert Path.mkdir is original
 p41=A/'actual_completed186_finally_collision_and_shared_report41_admission_v1_20261011.json';d=read(p41)
 tasks=[];aliases={};preserved=[]
 for name,driver in d['tasks']:
  f=A/'service_owned_workflows_20261006'/name;terminal=read(f/'service_execution.json')
  assert not owned(read(f/'native_launch.json')),name
  if terminal['status']=='passed':preserved.append({'name':name,'terminal':terminal});continue
  assert terminal['status']=='failed';new=name.replace('recovery41_','recovery42_',1);assert new!=name
  aliases[name]=new;tasks.append((new,driver))
 assert len(preserved)==2 and len(tasks)==44
 drivers=set(d['driver_wrappers']);corrections={};paths=[Path(__file__),p41,A/'route_actual_scratch_only_and_sealing_sources42_v1_20261011.py',A/'native_scratch_only_mkdir_scope_v1_20261011.py']
 routes=read(A/'verified_canonical_publication_failed_chain38_routes_v1_20261011.json')
 for driver,horizon in [('seal_StockRank60DirectEmbedding200_selected_candidate_v6_20261011.py',60),('seal_StockRank120DirectEmbedding201_selected_candidate_v7_20261011.py',120)]:
  source=A/routes['actual_source_overrides'].get(driver,driver);text=source.read_text(encoding='utf8')
  replacements={f'stock_rank{horizon}_direct_embedding_complete_parent_native_replay_verification.json':f'stock_rank{horizon}_embedding_complete_parent_native_replay_verification.json',
   f'passed_actual_complete_qualified_parent_stock_rank{horizon}_direct_embedding_two_full_native_independent_replays_and_cold80':f'passed_actual_complete_qualified_parent_stock_rank{horizon}_embedding_two_full_native_independent_replays_and_cold80'}
  for old,new in replacements.items():assert text.count(old)==1,(source,old);text=text.replace(old,new)
  ast.parse(text);corrections[driver]={'source':str(source),'replacements':replacements};paths.append(source)
 wrappers={}
 for driver in sorted(drivers):
  p=A/(Path(driver).stem+'_actual_scratch_and_sealing42_wrapper.py')
  text="from pathlib import Path\nimport sys\nA=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]\nfrom route_actual_scratch_only_and_sealing_sources42_v1_20261011 import execute\nif __name__=='__main__':execute("+repr(driver)+")\n"
  ast.parse(text);assert not p.exists();p.write_text(text,encoding='utf8');wrappers[driver]=p.name;paths.append(p)
 proof=A/'actual_scratch_only_and_sealing_sources42_admission_v1_20261011.json'
 create(proof,{'status':'actual_tmp_only_directory_positive_and_scientific_file_negative_controls_failed41_dependents_new42_completed_stages_preserved',
  'input_sha256':{str(p):sha(p) for p in paths},'service_alias_updates':aliases,'driver_wrappers':wrappers,'tasks':tasks,
  'preserved_completed41_services':preserved,'sealing_corrections':corrections,
  'scratch_admission_only_if_no_scientific_outputs_exist':True,'all_actual_full_NATIVE_independent_cold80_proof_assertions_retained':True,
  'scientific_workers_stopped_or_restarted':0,'new_fits_or_scores':0,'test_labels_read':False})
 for name,driver in tasks:
  assert allowed();p=A/wrappers[driver];r=start_service(name,p.name,[],{str(p):sha(p),str(proof):sha(proof)})
  create(A/(name+'_activation.json'),r)
 print({'actual42_failed_dependents_started':len(tasks),'actual_completed41_bridge_and_normalization_kept':len(preserved)},flush=True)
if __name__=='__main__':main()
