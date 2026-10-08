"""Correct generated report PREVIOUS paths prospectively before147 quality; preserve all earlier prototypes."""
from pathlib import Path
import sys,time,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save
MAP={
 'verify_JointCrossHuberOrder185_prospective_routes_v1_20261008.py':'verify_JointCrossHuberOrder185_prospective_routes_v2_20261008.py',
 'JointCrossHuberOrder185_prospective_routes_v1_20261008.json':'JointCrossHuberOrder185_prospective_routes_v2_20261008.json',
 'verify_JointCrossHuberOrder185_round147_sources_v1_20261008.py':'verify_JointCrossHuberOrder185_round147_sources_v2_20261008.py',
 'dispatch_JointCrossHuber147_complete_pipeline_v1_20261008.py':'dispatch_JointCrossHuber147_complete_pipeline_v2_20261008.py',
 'publish_JointCrossHuberOrder185_evidence_v3_20261008.py':'publish_JointCrossHuberOrder185_evidence_v4_20261008.py',
 'run_JointCrossHuberOrder185_round147_full_registration_v4_20261008.py':'run_JointCrossHuberOrder185_round147_full_registration_v5_20261008.py'}
def adapt(s):
 for old,new in MAP.items():s=s.replace(old,new)
 return s.replace('prepare_JointCrossHuberOrder185_round147_sources_v3_20261008','prepare_JointCrossHuberOrder185_round147_sources_v4_20261008').replace('JointCrossHuber147_complete_prospective_controls_v1_20261008','JointCrossHuber147_complete_prospective_controls_v2_20261008')
def main():
 originals=[];products=[]
 header='''"""Explicit comparison parent paths are fixed before quality; scientific134 stage graph stays unchanged."""
from pathlib import Path
import sys,ast
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
import prepare_JointCrossHuberOrder185_round147_sources_v3_20261008 as original
from prepare_JointCrossHuber147_explicit_report_paths_v4_20261008 import MAP
NAMES=original.NAMES
ORIGINAL_GENERATE=original.generate
def source_paths():
 out=[A/MAP.get(p.relative_to(A).as_posix(),p.relative_to(A).as_posix()) for p in original.source_paths()]
 out += [Path(__file__),Path(original.__file__),A/'prepare_JointCrossHuber147_explicit_report_paths_v4_20261008.py',A/'JointCrossHuber147_explicit_report_paths_preparation_v4_20261008.json']
 return list(dict.fromkeys(out))
def generate(parent):
 result={}
 for n,s in ORIGINAL_GENERATE(parent).items():
  s=s.replace('prepare_JointCrossHuberOrder185_round147_sources_v3_20261008','prepare_JointCrossHuberOrder185_round147_sources_v4_20261008')
  if n=='optimize_training_round147.py':
   t=ast.parse(s);assignment=next(x for x in t.body if isinstance(x,ast.Assign) and any(isinstance(a,ast.Name) and a.id=='PREVIOUS' for a in x.targets))
   literal=ast.get_source_segment(s,assignment.value.right);assert s.count(literal)==1
   s=s.replace(literal,repr('analysis/optimization_20261003_r'+str(parent)))
  compile(s,str(A/n),'exec');result[n]=s
 return result
def main():
 original.original.generate=generate
 original.original.main()
if __name__=='__main__':main()
'''
 products.append(save('prepare_JointCrossHuberOrder185_round147_sources_v4_20261008.py',header))
 for old,new in MAP.items():
  if not old.endswith('.py'):continue
  p=A/old;originals.append(p);s=adapt(p.read_text(encoding='utf8'))
  if old.startswith('run_'):s=s.replace('actual_registration_v4_20261008','actual_registration_v5_20261008').replace('full_registration_v4_file_IO_20261008','full_registration_v5_file_IO_20261008')
  if old.startswith('verify_JointCrossHuberOrder185_prospective'):
   needle='  generated=generator.generate(parent);assert len(generated)==8\n';assert s.count(needle)==1
   s=s.replace(needle,needle+'''  registry=ast.parse(generated['optimize_training_round147.py'])
  previous=next(ast.literal_eval(x.value.right) for x in registry.body if isinstance(x,ast.Assign) and any(isinstance(a,ast.Name) and a.id=='PREVIOUS' for a in x.targets))
  declared=next(ast.literal_eval(x.value) for x in registry.body if isinstance(x,ast.Assign) and any(isinstance(a,ast.Name) and a.id=='PREVIOUS_NUMBER' for a in x.targets))
  assert previous=='analysis/optimization_20261003_r'+str(parent) and declared==parent
''')
   s=s.replace('cross_volume_byte_probe_v1','cross_volume_byte_probe_v2')
  if old.startswith('dispatch_'):
   s=s.replace('complete_hidden_launches_v1_20261008','complete_hidden_launches_v2_20261008')
  products.append(save(new,s))
 from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
 f=A/'service_owned_workflows_20261006/JointCrossHuber147_complete_chronological_dispatch_v1_20261008';row=read(f/'native_launch.json');assert owned(row)
 parent,worker,idle=suspended_idle(row,'    closed (dispatch_JointCrossHuber147_complete_pipeline_v1_20261008.py:')
 try:
  assert not (A/'service_owned_workflows_20261006/JointCrossHuberOrder185_official_comparison_v1_20261008').exists()
  worker.terminate();parent.terminate()
  import psutil
  _,alive=psutil.wait_procs([worker,parent],timeout=10);assert not alive and not owned(row)
  meta=A/'JointCrossHuber147_explicit_report_paths_preparation_v4_20261008.json'
  create(meta,{'status':'prepared_fresh32_explicit_report_parent_paths_before_any147_quality',
   'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in [Path(__file__),*originals,*products]},
   'cancelled_only_proved_idle_dispatch1':{'launch':row,'idle_stack':idle},'old_prospective1_passed_proof_retained':True,
   'all_old_sources_preserved_and_stage_math_grid_models_unchanged':True,'new_quality_scores':0,'test_labels_read':False})
  from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
  pins={str(p):sha(p) for p in [Path(__file__),meta,*products]}
  p=start('JointCrossHuber147_complete_prospective_controls_v2_20261008','verify_JointCrossHuberOrder185_prospective_routes_v2_20261008.py',[],pins)
  d=start('JointCrossHuber147_complete_chronological_dispatch_v2_20261008','dispatch_JointCrossHuber147_complete_pipeline_v2_20261008.py',[],pins)
  create(A/'JointCrossHuber147_explicit_report_paths_hidden_launches_v4_20261008.json',{'prospective':p,'dispatch':d,'input_sha256':pins})
  print(json.dumps({'prospective':p['owned_worker_pid'],'dispatch':d['owned_worker_pid']}),flush=True)
 finally:
  for p in (worker,parent):
   if p.is_running():p.resume()
if __name__=='__main__':main()
