"""Preserve failed unscored prototype; correct remaining quoted collector literals to actual148/59/242."""
from pathlib import Path
import sys,time,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save
MAP={n:n.replace('_v1_20261008','_v2_20261008') for n in [
 'verify_AdaptiveJointCrossHuber242_prospective_routes_v1_20261008.py','AdaptiveJointCrossHuber242_prospective_routes_v1_20261008.json',
 'verify_AdaptiveJointCrossHuber242_round148_sources_v1_20261008.py','publish_AdaptiveJointCrossHuber242_evidence_v1_20261008.py',
 'run_AdaptiveJointCrossHuber242_round148_full_registration_v1_20261008.py','dispatch_AdaptiveJointCrossHuber148_complete_pipeline_v1_20261008.py']}
def adapt(s):
 for old,new in MAP.items():s=s.replace(old,new)
 return s.replace('prepare_AdaptiveJointCrossHuber242_round148_sources_v1_20261008','prepare_AdaptiveJointCrossHuber242_round148_sources_v2_20261008').replace('AdaptiveJointCrossHuber148_complete_prospective_controls_v1_20261008','AdaptiveJointCrossHuber148_complete_prospective_controls_v2_20261008')
def main():
 failed=A/'service_owned_workflows_20261006/AdaptiveJointCrossHuber148_complete_prospective_controls_v1_20261008/service_execution.json';assert read(failed)['status']=='failed'
 originals=[];products=[]
 for old,new in MAP.items():
  if not old.endswith('.py'):continue
  p=A/old;originals.append(p);s=adapt(p.read_text(encoding='utf8'))
  if 'prospective_routes' in old:
   for before,after in [("'collect(147, 58, 185)'","'collect(148, 59, 242)'"),("namespace['snapshot'](147)","namespace['snapshot'](148)"),("== full['scored_records'] == 185","== full['scored_records'] == 242")]:s=s.replace(before,after)
   s=s.replace('cross_volume_byte_probe_v1','cross_volume_byte_probe_v2')
  if old.startswith('run_'):s=s.replace('actual_registration_v1_20261008','actual_registration_v2_20261008').replace('full_registration_v1_file_IO_20261008','full_registration_v2_file_IO_20261008')
  if old.startswith('dispatch_'):s=s.replace('complete_hidden_launches_v1_20261008','complete_hidden_launches_v2_20261008')
  products.append(save(new,s))
 header='''"""Bind actual148 prospective2 and preserve all242 mathematical configurations."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
import prepare_AdaptiveJointCrossHuber242_round148_sources_v1_20261008 as original
from recover_AdaptiveJointCrossHuber148_prospective_literals_v2_20261008 import MAP
NAMES=original.NAMES
ORIGINAL_GENERATE=original.generate
def source_paths():
 out=[A/MAP.get(p.relative_to(A).as_posix(),p.relative_to(A).as_posix()) for p in original.source_paths()]
 out += [Path(__file__),Path(original.__file__),A/'recover_AdaptiveJointCrossHuber148_prospective_literals_v2_20261008.py',A/'AdaptiveJointCrossHuber148_prospective_literal_recovery_v2_20261008.json']
 return list(dict.fromkeys(out))
def generate(parent):
 result={}
 for n,s in ORIGINAL_GENERATE(parent).items():
  s=s.replace('prepare_AdaptiveJointCrossHuber242_round148_sources_v1_20261008','prepare_AdaptiveJointCrossHuber242_round148_sources_v2_20261008')
  compile(s,str(A/n),'exec');result[n]=s
 return result
def main():
 original.generate=generate
 original.main()
if __name__=='__main__':main()
'''
 products.append(save('prepare_AdaptiveJointCrossHuber242_round148_sources_v2_20261008.py',header))
 meta=A/'AdaptiveJointCrossHuber148_prospective_literal_recovery_v2_20261008.json'
 create(meta,{'status':'prepared_fresh_actual148_QA59_242_quoted_collector_contract_checks_before_quality',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in [Path(__file__),failed,*originals,*products]},
  'all_failed_sources_preserved_and_new_scientific_grid_models_math_unchanged':True,'new_quality_scores':0,'new_inference':0,'test_labels_read':False})
 from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
 pins={str(p):sha(p) for p in [Path(__file__),meta,*products]}
 p=start('AdaptiveJointCrossHuber148_complete_prospective_controls_v2_20261008','verify_AdaptiveJointCrossHuber242_prospective_routes_v2_20261008.py',[],pins)
 d=start('AdaptiveJointCrossHuber148_complete_chronological_dispatch_v2_20261008','dispatch_AdaptiveJointCrossHuber148_complete_pipeline_v2_20261008.py',[],pins)
 create(A/'AdaptiveJointCrossHuber148_complete_hidden_preflight_launches_v2_20261008.json',{'prospective':p,'dispatch':d,'input_sha256':pins})
 print(json.dumps({'prospective':p['owned_worker_pid'],'dispatch':d['owned_worker_pid']}),flush=True)
if __name__=='__main__':main()
