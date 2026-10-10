"""Recover failed waits from actually completed186 stages; retain live scientific work."""
from pathlib import Path
import sys,ast,importlib,re
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service

def main():
 assert allowed()
 controls=A/'shared_live_report_exact15_scope_controls_v2_20261011.json';c=read(controls)
 assert c['status']=='passed_actual_all15_exact_codec_QA_namespace_scope_and_restoration_controls'
 for p,d in c['input_sha256'].items():assert sha(p)==d,p
 old186=A/'service_owned_workflows_20261006/actual186_registered_QA_main_resume39_v1_20261011'
 fail=read(old186/'service_execution.json');assert fail['status']=='failed' and 'actual_hidden_registration_children.json' in fail['failure'] and 'FileExistsError' in fail['failure']
 assert not owned(read(old186/'native_launch.json'))
 assert read(A/'optimization_20261003_r186/full_registration_execution.json')['status']=='passed'
 assert read(A/'github_validation_sync_main_20261005/round186_receipt.json')['status']=='pushed_and_remote_head_verified'
 bridge_template=A/'verify_actual186_registered_QA_main_complete_parent_bridge38_v1_20261011.py'
 bridge=A/'verify_actual186_completed_stages_and_finally_collision_bridge41_v1_20261011.py'
 text=bridge_template.read_text(encoding='utf8')
 before=" assert allowed();closed('actual186_registered_QA_main_resume38_v1_20261011')"
 assert text.count(before)==1
 after=""" assert allowed()
 source=A/'service_owned_workflows_20261006/actual186_registered_QA_main_resume39_v1_20261011'
 from run_dependency_queue_v3_20261006 import owned
 assert not owned(read(source/'native_launch.json'))
 failure=read(source/'service_execution.json')
 assert failure['status']=='failed' and 'FileExistsError' in failure['failure'] and 'actual_hidden_registration_children.json' in failure['failure']
 assert read(A/'lossless_ranking_display_qa_v97_20261010/round186/verification.json')['status']=='passed_all_original_full_ranking_QA_and_lossless_browser_node_checks'
"""
 text=text.replace(before,after).replace('actual186_registered_QA_main_complete_parent_bridge38_v1_20261011.json','actual186_completed_stages_and_finally_collision_bridge41_v1_20261011.json')
 ast.parse(text)
 if bridge.exists():
  assert not (A/'actual_completed186_finally_collision_and_shared_report41_admission_v1_20261011.json').exists() and bridge.read_text(encoding='utf8')==text
 else:bridge.write_text(text,encoding='utf8')
 p40=A/'actual_failed_chain40_preserving186_resume39_admission_v1_20261011.json';d40=read(p40)
 p38=A/'verified_canonical_publication_failed_chain38_routes_v1_20261011.json';d38=read(p38)
 aliases={'actual186_registered_QA_main_resume39_v1_20261011':'actual186_complete_parent_bridge41_v1_20261011',
  'actual186_complete_parent_bridge40_v1_20261011':'actual186_complete_parent_bridge41_v1_20261011'}
 tasks=[];oldrows=[]
 for name,driver in d40['tasks']:
  if name=='actual186_complete_parent_bridge40_v1_20261011':new='actual186_complete_parent_bridge41_v1_20261011';driver=bridge.name
  else:new=name.replace('recovery40_','recovery41_',1)
  assert new!=name
  f=A/'service_owned_workflows_20261006'/name
  assert (f/'service_execution.json').exists() and read(f/'service_execution.json')['status']=='failed' and not owned(read(f/'native_launch.json')),name
  aliases[name]=new;tasks.append((new,driver));oldrows.append({'name':name,'terminal':read(f/'service_execution.json')})
 f201=importlib.import_module('prepare_StockRank120Direct201_complete35_pipeline_v7_20261011')
 added=[('actual_stock_rank120_direct_embedding35_after200_normalization_queue_v7_20261011',f201.EXTRAS[0]),
  ('StockRank120DirectEmbedding35_selected_native14_v7_20261011',f201.EXTRAS[1]),
  ('StockRank120DirectEmbedding201_complete35_family_v7_20261011',f201.EXTRAS[5])]
 assert 'complete_family' in added[-1][1]
 for name,driver in added:
  f=A/'service_owned_workflows_20261006'/name
  assert read(f/'service_execution.json')['status']=='failed' and not owned(read(f/'native_launch.json')),name
  new='recovery41_'+name;aliases[name]=new;tasks.append((new,driver));oldrows.append({'name':name,'terminal':read(f/'service_execution.json')})
 factories=[*d38['source_factories'],'prepare_StockRank120Direct201_complete35_pipeline_v7_20261011']
 drivers=set(d40['driver_wrappers'])|{d for _,d in tasks}|set(f201.NAMES+f201.EXTRAS[:9])
 variants={row['number']:row for row in c['variants']};contracts={};wrappers={}
 paths=[Path(__file__),A/'route_actual_completed186_and_shared_report41_v1_20261011.py',bridge,bridge_template,p40,p38,controls,A/'shared_live_ranking_report_runtime_v2_20261011.py',old186/'service_execution.json',A/'optimization_20261003_r186/full_registration_execution.json',A/'github_validation_sync_main_20261005/round186_receipt.json']
 for driver in sorted(drivers):
  source=A/d38['actual_source_overrides'].get(driver,driver)
  if '_full_registration_' in driver and source.exists():
   imports=[n.module for n in ast.walk(ast.parse(source.read_text(encoding='utf8'))) if isinstance(n,ast.ImportFrom) and n.module and n.module.startswith('lossless_ranking_runtime_adapter_round')]
   if imports:
    assert len(imports)==1;number=int(re.search(r'round(\d+)',imports[0]).group(1))
    if number in variants:
     row=variants[number];adapter=A/(imports[0]+'.py');s=adapter.read_text(encoding='utf8')
     assert f"from {row['codec_name']} import main as encode" in s and f"from {row['verifier_name']} import main as verify" in s
     contracts[driver]={'number':number,'codec_name':row['codec_name'],'verifier_name':row['verifier_name']};paths.append(source)
  wrapper=A/(Path(driver).stem+'_actual_completed186_shared_report41_wrapper.py')
  body="from pathlib import Path\nimport sys\nA=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]\nfrom route_actual_completed186_and_shared_report41_v1_20261011 import execute\nif __name__=='__main__':execute("+repr(driver)+")\n"
  ast.parse(body);assert not wrapper.exists();wrapper.write_text(body,encoding='utf8');wrappers[driver]=wrapper.name;paths.append(wrapper)
 assert {v['number'] for v in contracts.values()}==set(range(187,202)),sorted(contracts)
 proof=A/'actual_completed186_finally_collision_and_shared_report41_admission_v1_20261011.json'
 create(proof,{'status':'failed_administrative_dependents_recovered_from_actual186_full_QA_main_with_exact_version_reader_controls',
  'input_sha256':{str(p):sha(p) for p in paths},'service_alias_updates':aliases,'driver_wrappers':wrappers,
  'source_factories':factories,'full_driver_contracts':contracts,'tasks':tasks,'old_failed_receipts':oldrows,
  'full186_NOT_reexecuted':True,'original_failed_finally_receipt_NOT_rewritten':True,
  'all15_actual_codec_and_QA_scope_controls_passed_before_reader_adoption':True,
  'scientific_workers_stopped_or_restarted':0,'new_fits_or_scores_by_recovery':0,'test_labels_read':False})
 for name,driver in tasks:
  assert allowed();wrapper=A/wrappers[driver]
  row=start_service(name,wrapper.name,[],{str(wrapper):sha(wrapper),str(proof):sha(proof)})
  create(A/(name+'_activation.json'),row)
 print({'actual41_dependents_started':len(tasks),'actual_full186_not_rerun':True,'exact_version_shared_reader_admitted_rounds':15},flush=True)

if __name__=='__main__':main()
