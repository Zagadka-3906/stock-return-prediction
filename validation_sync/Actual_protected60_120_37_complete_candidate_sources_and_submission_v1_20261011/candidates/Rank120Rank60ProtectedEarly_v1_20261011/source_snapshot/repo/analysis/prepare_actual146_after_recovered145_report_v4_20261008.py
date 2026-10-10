"""Retarget operational145 completion to actual3 and add an explicit report-parent binding before146 quality."""
from pathlib import Path
import sys,time,json,hashlib,ast
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save
WRAPPERS={
 'verify_HuberCrossFamilyFine125_round146_sources_v3_20261008.py':'verify_HuberCrossFamilyFine125_round146_sources_v4_20261008.py',
 'publish_HuberCrossFamilyFine125_evidence_v3_20261008.py':'publish_HuberCrossFamilyFine125_evidence_v4_20261008.py',
 'run_HuberCrossFamilyFine125_official_comparison_v2_20261008.py':'run_HuberCrossFamilyFine125_official_comparison_v3_20261008.py',
 'run_HuberCrossFamilyFine125_round146_full_registration_v3_20261008.py':'run_HuberCrossFamilyFine125_round146_full_registration_v4_20261008.py'}
META=A/'actual146_recovered145_gate_and_report_preflight_v4_20261008.json'
def actual_paths():
 return [Path(__file__),META,A/'actual_explicit_comparison_parent_binding_v1_20261008.py',*(A/n for n in WRAPPERS.values()),
  A/'benchmark_deferred_full_board_serialization_v3_20261008.py',A/'verify_deferred_full_board_QA_v3_20261008.py',A/'dispatch_HuberCrossFamilyFine146_complete_pipeline_v5_20261008.py']
def install_generator():
 import prepare_HuberCrossFamilyFine125_round146_sources_v3_20261008 as g
 original=g.source_paths
 g.source_paths=lambda:list(dict.fromkeys([*original(),*actual_paths()]))
 return g
def execute(original,phase=None):
 p=A/original;note=read(META)
 for f,d in note['input_sha256'].items():assert sha(f)==d,f
 install_generator()
 ns={'__file__':str(p),'__name__':'actual146_recovered_previous_report_operational_receiver'}
 exec(compile(p.read_text(encoding='utf8'),str(p),'exec'),ns)
 original_closed=ns.get('closed')
 if original_closed:
  def closed(name):return original_closed('CrossFamilyFine125_round145_full_registration_v3_20261008' if name=='CrossFamilyFine125_round145_full_registration_v2_20261008' else name)
  ns['closed']=closed
 if original.startswith('verify_'):
  original_create=ns['create']
  def extended_create(path,value):
   if Path(path).name=='HuberCrossFamilyFine125_round146_source_admission_v2_20261008.json':
    value={**value,'input_sha256':{**value['input_sha256'],**{str(f):sha(f) for f in actual_paths()}},
     'actual_operational145_full_service':'CrossFamilyFine125_round145_full_registration_v3_20261008',
     'report_previous_binding_receiver_preflight':str(META),'frozen_scientific_grid_generated_routes_and_original_prospective3_unchanged':True}
   original_create(path,value)
  ns['create']=extended_create
 if original.startswith('run_HuberCrossFamilyFine125_round146_full'):
  import publish_explicit_parent_training_round_v2_20261005 as report
  original_publish=report.publish
  def publish(number,*args,**kwargs):
   assert number==146
   from actual_explicit_comparison_parent_binding_v1_20261008 import bind
   bind(146,A/'HuberCrossFamilyFine125_selected_release_v1_20261008/actual_report_parent_binding_v4_20261008.json')
   return original_publish(number,*args,**kwargs)
  report.publish=publish
 if phase is None:ns['main']()
 else:ns['main'](phase)
def main():
 assert not (A/'service_owned_workflows_20261006/HuberCrossFamilyFine125_official_comparison_v2_20261008').exists()
 originals=[];products=[]
 for old,new in WRAPPERS.items():
  p=A/old;originals.append(p)
  header='''"""Execute the unchanged146 mathematical receiver with actual recovered145 completion and report metadata binding."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
from prepare_actual146_after_recovered145_report_v4_20261008 import execute
'''
  if old.startswith('publish_'):header+=f"if __name__=='__main__':\n import argparse\n p=argparse.ArgumentParser();p.add_argument('phase',choices=('controls','scores'));execute({old!r},p.parse_args().phase)\n"
  else:header+=f"if __name__=='__main__':execute({old!r})\n"
  products.append(save(new,header))
 for old,new in [('benchmark_deferred_full_board_serialization_v2_20261008.py','benchmark_deferred_full_board_serialization_v3_20261008.py'),('verify_deferred_full_board_QA_v2_20261008.py','verify_deferred_full_board_QA_v3_20261008.py')]:
  p=A/old;originals.append(p);s=p.read_text(encoding='utf8').replace('CrossFamilyFine125_round145_full_registration_v2_20261008','CrossFamilyFine125_round145_full_registration_v3_20261008')
  s=s.replace('serialization_benchmark_v2_20261008','serialization_benchmark_v3_20261008').replace('resource_budget_v2_20261008','resource_budget_v3_20261008').replace('verify_deferred_full_board_QA_v2_20261008','verify_deferred_full_board_QA_v3_20261008').replace('full_board_deferred_QA_v2_20261008','full_board_deferred_QA_v3_20261008')
  products.append(save(new,s))
 p=A/'dispatch_HuberCrossFamilyFine146_complete_pipeline_v4_20261008.py';originals.append(p);s=p.read_text(encoding='utf8')
 s=s.replace('CrossFamilyFine125_round145_full_registration_v2_20261008','CrossFamilyFine125_round145_full_registration_v3_20261008').replace('actual_full_board_deferred_serialization_benchmark_v2_20261008','actual_full_board_deferred_serialization_benchmark_v3_20261008')
 s=s.replace('execution_cost_slot_handoff_v2_20261008','execution_cost_slot_handoff_v3_20261008').replace('complete_hidden_launches_v2_20261008','complete_hidden_launches_v3_20261008')
 for old,new in WRAPPERS.items():s=s.replace(old,new)
 s=s.replace("    recovery=A/'actual_idle_optional_benchmark_handoff_v2_20261008.json'", "    recovery=A/'actual146_recovered145_gate_and_report_preflight_v4_20261008.json'")
 products.append(save('dispatch_HuberCrossFamilyFine146_complete_pipeline_v5_20261008.py',s))
 prospective=A/'HuberCrossFamilyFine125_prospective_routes_v3_20261008.json';proof=read(prospective)
 for f,d in proof['input_sha256'].items():assert sha(f)==d,f
 import prepare_HuberCrossFamilyFine125_round146_sources_v3_20261008 as g
 plan=read(A/'HuberCrossFamilyFine125_round146_plan_v2_20261008.json');controls=[]
 for parent in plan['anchor_rounds']:
  generated=g.generate(parent);assert {n:hashlib.sha256(s.encode()).hexdigest() for n,s in generated.items()}==proof['generated_source_sha256'][str(parent)]
  text=generated['optimize_training_round146.py'];tree=ast.parse(text)
  previous=next(ast.literal_eval(n.value.right) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='PREVIOUS' for t in n.targets))
  declared=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='PREVIOUS_NUMBER' for t in n.targets))
  assert declared==parent
  controls.append({'comparison_parent':parent,'original_legacy_report_previous_path':previous,'actual_binding_uses_frozen_protocol_and_gain_contribution_check':True,
   'eight_generated_canonical_scientific_sources_byte_identical_to_original_prospective3':True})
 failed=[A/'service_owned_workflows_20261006'/n/'service_execution.json' for n in ('CrossFamilyFine125_round145_full_registration_v2_20261008','actual_full_board_deferred_serialization_benchmark_v2_20261008','HuberCrossFamilyFine146_complete_chronological_dispatch_v4_20261008')]
 assert all(read(f)['status']=='failed' for f in failed)
 create(META,{'status':'passed_actual_four_parent_report_bindings_and_recovered145_completion_gate_before_any146_score',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(f):sha(f) for f in [Path(__file__),prospective,*originals,*products,*failed,A/'actual_explicit_comparison_parent_binding_v1_20261008.py']},
  'controls':controls,'original_native_math_grid_official_sources_and_full_prospective3_hashes_unchanged':True,
  'only_actual_closed145_service_and_report_previous_binding_changed':True,'new_quality_scores':0,'new_model_fits':0,'test_labels_read':False})
 from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
 pins={str(f):sha(f) for f in [Path(__file__),META,*products]}
 b=start('actual_full_board_deferred_serialization_benchmark_v3_20261008','benchmark_deferred_full_board_serialization_v3_20261008.py',[],pins)
 d=start('HuberCrossFamilyFine146_complete_chronological_dispatch_v5_20261008','dispatch_HuberCrossFamilyFine146_complete_pipeline_v5_20261008.py',[],pins)
 create(A/'actual146_recovered145_report_hidden_launches_v4_20261008.json',{'benchmark':b,'dispatch':d,'input_sha256':pins})
 print(json.dumps({'benchmark':b['owned_worker_pid'],'dispatch':d['owned_worker_pid']}),flush=True)
if __name__=='__main__':main()
