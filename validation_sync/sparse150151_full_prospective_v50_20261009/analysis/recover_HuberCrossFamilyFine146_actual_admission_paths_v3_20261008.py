"""Preserve both failed preflights; bind real admission2 and fresh prospective3 before146 scoring."""
from pathlib import Path
import sys,time,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
MAP={n:n.replace('_v2_20261008','_v3_20261008') for n in [
 'prepare_HuberCrossFamilyFine125_round146_sources_v2_20261008.py',
 'verify_HuberCrossFamilyFine125_round146_sources_v2_20261008.py',
 'publish_HuberCrossFamilyFine125_evidence_v2_20261008.py',
 'run_HuberCrossFamilyFine125_round146_full_registration_v2_20261008.py',
 'dispatch_HuberCrossFamilyFine146_complete_pipeline_v2_20261008.py']}
MAP.update({'verify_HuberCrossFamilyFine125_prospective_routes_v3_20261008.py':'verify_HuberCrossFamilyFine125_prospective_routes_v4_20261008.py',
 'HuberCrossFamilyFine125_prospective_routes_v2_20261008.json':'HuberCrossFamilyFine125_prospective_routes_v3_20261008.json',
 'HuberCrossFamilyFine125_round146_source_admission_v1_20261008.json':'HuberCrossFamilyFine125_round146_source_admission_v2_20261008.json'})
def adapt(s):
 for old,new in MAP.items():s=s.replace(old.removesuffix('.py'),new.removesuffix('.py'))
 return s.replace('HuberCrossFamilyFine146_complete_prospective_controls_v2_20261008','HuberCrossFamilyFine146_complete_prospective_controls_v3_20261008')
def save(n,s):
 p=A/n;compile(s,str(p),'exec')
 with p.open('x',encoding='utf8',newline='') as f:f.write(s)
 return p
def main():
 failure=A/'service_owned_workflows_20261006/HuberCrossFamilyFine146_complete_prospective_controls_v2_20261008/service_execution.json'
 assert read(failure)['status']=='failed'
 products=[];originals=[]
 for old,new in MAP.items():
  if not old.endswith('.py') or old.startswith('prepare_HuberCrossFamilyFine125_round146_sources'):continue
  p=A/old;s=adapt(p.read_text(encoding='utf-8-sig'));originals.append(p)
  if new.startswith('verify_HuberCrossFamilyFine125_prospective_routes'):
   s=s.replace("'collect(145, 56, 125)'", "'collect(146, 57, 125)'").replace('"namespace[\'snapshot\'](145)"','"namespace[\'snapshot\'](146)"')
   s=s.replace('cross_volume_byte_probe_v1','cross_volume_byte_probe_v3')
  if new.startswith('run_HuberCrossFamilyFine125_round146_full'):
   s=s.replace('actual_registration_v2_20261008','actual_registration_v3_20261008').replace('full_registration_v2_file_IO_20261008','full_registration_v3_file_IO_20261008')
  products.append(save(new,s))
 header='''"""Generate identical146 mathematics with actual admission2 and declared three-head registry."""
from pathlib import Path
import hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
import prepare_HuberCrossFamilyFine125_round146_sources_v2_20261008 as original
from recover_HuberCrossFamilyFine146_actual_admission_paths_v3_20261008 import MAP,adapt
NAMES=original.NAMES
def source_paths():
 out=[A/MAP.get(p.relative_to(A).as_posix(),p.relative_to(A).as_posix()) for p in original.source_paths()]
 out += [Path(__file__),Path(original.__file__),A/'recover_HuberCrossFamilyFine146_actual_admission_paths_v3_20261008.py',A/'HuberCrossFamilyFine146_actual_admission_paths_recovery_v3_20261008.json']
 return list(dict.fromkeys(out))
def generate(parent):
 outputs={n:adapt(s) for n,s in original.generate(parent).items()}
 for n,s in outputs.items():compile(s,str(A/n),'exec')
 return outputs
'''
 first=A/'prepare_HuberCrossFamilyFine125_round146_sources_v1_20261008.py';s=first.read_text(encoding='utf8')
 maintext=s[s.index('def main():'):s.index("if __name__=='__main__':")]
 products.append(save('prepare_HuberCrossFamilyFine125_round146_sources_v3_20261008.py',header+adapt(maintext)+"if __name__=='__main__':main()\n"))
 meta=A/'HuberCrossFamilyFine146_actual_admission_paths_recovery_v3_20261008.json'
 pins={str(p):sha(p) for p in [Path(__file__),failure,first,*originals,*products]}
 create(meta,{'status':'prepared_fresh_prospective3_and_actual_admission2_paths_before_any146_quality',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,
  'all_prior_failures_and_sources_preserved':True,'mathematics_models_grid_and_selection_rules_unchanged':True,
  'declared_native_components':3,'actual_official146_scores':0,'test_labels_read':False})
 pins[str(meta)]=sha(meta)
 from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
 row=start('HuberCrossFamilyFine146_complete_prospective_controls_v3_20261008','verify_HuberCrossFamilyFine125_prospective_routes_v4_20261008.py',[],pins)
 dispatch=start('HuberCrossFamilyFine146_complete_chronological_dispatch_v3_20261008','dispatch_HuberCrossFamilyFine146_complete_pipeline_v3_20261008.py',[],pins)
 create(A/'HuberCrossFamilyFine146_actual_admission_paths_hidden_launches_v3_20261008.json',{'prospective':row,'dispatch':dispatch,'input_sha256':pins})
 print(json.dumps({'prospective':row['owned_worker_pid'],'dispatch':dispatch['owned_worker_pid']}),flush=True)
if __name__=='__main__':main()
