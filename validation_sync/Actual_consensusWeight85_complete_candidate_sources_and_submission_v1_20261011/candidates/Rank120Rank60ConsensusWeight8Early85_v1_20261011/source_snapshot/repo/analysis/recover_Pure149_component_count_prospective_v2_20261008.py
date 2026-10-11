"""Declare2/3/5 native components prospectively; preserve the rejected unscored prototype."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save
MAP={n:n.replace('_v1_20261008','_v2_20261008') for n in ['verify_PureRFFHuber128_prospective_routes_v1_20261008.py','PureRFFHuber128_prospective_routes_v1_20261008.json','verify_PureRFFHuber128_round149_sources_v1_20261008.py','publish_PureRFFHuber128_evidence_v1_20261008.py','run_PureRFFHuber128_round149_full_registration_v1_20261008.py','dispatch_PureRFFHuber149_complete_pipeline_v1_20261008.py']}
def adapt(s):
 for a,b in MAP.items():s=s.replace(a,b)
 return s.replace('prepare_PureRFFHuber128_round149_sources_v1_20261008','prepare_PureRFFHuber128_round149_sources_v2_20261008').replace('PureRFFHuber149_complete_prospective_controls_v1_20261008','PureRFFHuber149_complete_prospective_controls_v2_20261008')
def main():
 failed=A/'service_owned_workflows_20261006/PureRFFHuber149_complete_prospective_controls_v1_20261008/service_execution.json';assert read(failed)['status']=='failed'
 originals=[];products=[]
 for old,new in MAP.items():
  if not old.endswith('.py'):continue
  p=A/old;originals.append(p);s=adapt(p.read_text(encoding='utf8'))
  if old.startswith('run_'):s=s.replace('actual_registration_v1_20261008','actual_registration_v2_20261008').replace('full_registration_v1_file_IO','full_registration_v2_file_IO')
  if old.startswith('dispatch_'):s=s.replace('complete_hidden_launches_v1','complete_hidden_launches_v2')
  products.append(save(new,s))
 header='''from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
import prepare_PureRFFHuber128_round149_sources_v1_20261008 as original
from recover_Pure149_component_count_prospective_v2_20261008 import MAP
NAMES=original.NAMES
ORIGINAL_GENERATE=original.generate
def source_paths():
 result=[A/MAP.get(p.relative_to(A).as_posix(),p.relative_to(A).as_posix()) for p in original.source_paths()]
 result += [Path(__file__),Path(original.__file__),A/'recover_Pure149_component_count_prospective_v2_20261008.py',A/'Pure149_component_count_prospective_recovery_v2_20261008.json']
 return list(dict.fromkeys(result))
def generate(parent):
 result={}
 for name,s in ORIGINAL_GENERATE(parent).items():
  s=s.replace('prepare_PureRFFHuber128_round149_sources_v1_20261008','prepare_PureRFFHuber128_round149_sources_v2_20261008')
  if name.startswith('register_'):
   needle="len(measured['ordered_native_components']) in (3,4,7)";assert s.count(needle)==1
   s=s.replace(needle,"len(measured['ordered_native_components']) in (2,3,5)")
  compile(s,str(A/name),'exec');result[name]=s
 return result
def main():
 original.generate=generate
 original.main()
if __name__=='__main__':main()
'''
 products.append(save('prepare_PureRFFHuber128_round149_sources_v2_20261008.py',header))
 meta=A/'Pure149_component_count_prospective_recovery_v2_20261008.json'
 create(meta,{'status':'prepared_fresh32_routes_with_actual2_3_5_physical_component_guard_before_any149_quality','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in [Path(__file__),failed,*originals,*products]},'original_failed_sources_preserved':True,'new_quality_scores':0,'test_labels_read':False})
 from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
 p=A/'verify_PureRFFHuber128_prospective_routes_v2_20261008.py';row=start('PureRFFHuber149_complete_prospective_controls_v2_20261008',p.name,[],{str(p):sha(p),str(meta):sha(meta),str(Path(__file__)):sha(__file__)})
 create(A/'Pure149_component_count_prospective_hidden_launch_v2_20261008.json',row);print(row['owned_worker_pid'],flush=True)
if __name__=='__main__':main()
