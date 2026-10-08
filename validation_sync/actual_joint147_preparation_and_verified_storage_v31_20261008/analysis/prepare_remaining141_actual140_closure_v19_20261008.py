"""Preflight only the unstarted141 receivers against actual140 full19; preserve all original18 prototypes."""
from pathlib import Path
import sys,time,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
import recover_pending137to141_registration_contracts_v18_20261008 as h
h.initialize();CFG=next(c for c in h.CONFIG if c['round']==141)
MAP={h.MAPPING[Path(r['original_driver']).stem]:h.MAPPING[Path(r['original_driver']).stem].replace('_v18_','_v19_') for r in CFG['launches'].values()}
MAP.update({'prepare_KrylovGram52_round141_sources_v18_20261008':'prepare_KrylovGram52_round141_sources_v19_20261008',
 'verify_KrylovGram52_prospective_routes_v18_20261008':'verify_KrylovGram52_prospective_routes_v19_20261008',
 'KrylovGram52_prospective_routes_v18_20261008':'KrylovGram52_prospective_routes_v19_20261008',
 'SpectralGram52_round140_full_registration_v18_20261008':'SpectralGram52_round140_full_registration_v19_20261008',
 'SpectralGram140_truthful_metadata_receiver_preparation_v18_20261008':'SpectralGram140_truthful_metadata_receiver_preparation_v2_20261008'})
def adapt(s):
 for old,new in MAP.items():s=s.replace(old,new)
 return s
def save(p,s):
 compile(s,str(p),'exec')
 with p.open('x',encoding='utf8',newline='') as f:f.write(s)
def closed(n):
 p=A/'service_owned_workflows_20261006'/n
 while not (p/'service_execution.json').exists():time.sleep(10)
 while owned(read(p/'native_launch.json')):time.sleep(1)
 assert read(p/'service_execution.json')['status']=='passed',n
def dispatch():
 closed('KrylovGram141_remaining_complete_prospective_controls_v19_20261008')
 proof=A/'KrylovGram52_prospective_routes_v19_20261008.json'
 for p,d in read(proof)['input_sha256'].items():assert sha(p)==d,p
 closed('SpectralGram52_round140_full_registration_v19_20261008')
 from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
 pins={str(p):sha(p) for p in [Path(__file__),proof,A/'KrylovGram141_actual140_closure_preparation_v19_20261008.json']};rows={}
 for n,r in CFG['launches'].items():
  service=h.MAPPING[n];driver=MAP[h.MAPPING[Path(r['original_driver']).stem]]+'.py'
  assert not (A/'service_owned_workflows_20261006'/service).exists(),service
  rows[service]=start(service,driver,r['original_arguments'],{**pins,str(A/driver):sha(A/driver)})
 create(A/'round141_actual140_closure_hidden_launches_v19_20261008.json',{'status':'started_eight_preflighted_fresh19_drivers_under_original_unused18_service_names',
  'launches':rows,'actual_previous_passed_service':'SpectralGram52_round140_full_registration_v19_20261008','input_sha256':pins,'new_quality_scores_by_dispatch':0,'test_labels_read':False})
 print(json.dumps(list(rows)),flush=True)
def main():
 assert not any((A/CFG['physical_comparison']).iterdir())
 originals=[];products=[]
 for old,new in MAP.items():
  source=A/(old+'.py')
  if not source.is_file() or old.startswith('prepare_KrylovGram52_round141_sources') or old.startswith('SpectralGram'):continue
  text=adapt(source.read_text(encoding='utf-8-sig'))
  if old.startswith('verify_KrylovGram52_prospective'):
   text=text.replace('transfer_probe_v18','transfer_probe_v19').replace('cross_volume_byte_probe_v18','cross_volume_byte_probe_v19')
  if old.startswith('run_KrylovGram52_round141_full'):
   text=text.replace('actual_registration_v18_20261008','actual_registration_v19_20261008').replace('full_registration_v18_file_IO_20261008','full_registration_v19_file_IO_20261008')
  target=A/(new+'.py');save(target,text);originals.append(source);products.append(target)
 source=A/'prepare_KrylovGram52_round141_sources_v18_20261008.py';old=source.read_text(encoding='utf8')
 tail=old[old.index('def main():'):]
 header='''"""Actual141 routes resolve immutable140 metadata2 and freshly preflighted19 drivers."""
from pathlib import Path
import hashlib,time
from run_dependency_queue_v3_20261006 import read,sha,create
import prepare_KrylovGram52_round141_sources_v18_20261008 as original
from prepare_remaining141_actual140_closure_v19_20261008 import adapt
ROOT=original.ROOT;A=original.A;NAMES=original.NAMES
def source_paths():
 out=[A/adapt(p.relative_to(A).as_posix()) for p in original.source_paths()]
 return list(dict.fromkeys([*out,Path(__file__),Path(original.__file__),A/'prepare_remaining141_actual140_closure_v19_20261008.py',A/'KrylovGram141_actual140_closure_preparation_v19_20261008.json']))
def generate(parent):return {n:adapt(s) for n,s in original.generate(parent).items()}
'''
 target=A/'prepare_KrylovGram52_round141_sources_v19_20261008.py';save(target,header+adapt(tail));originals.append(source);products.append(target)
 prep=A/'KrylovGram141_actual140_closure_preparation_v19_20261008.json';pins={str(p):sha(p) for p in [Path(__file__),*originals,*products]}
 create(prep,{'status':'prepared_only_unstarted141_against_actual140_closure19_before_quality',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'eight_original18_service_names_unused_and_preserved_for_waiting145':True,
  'models_grid_native_CDF_official_scoring_and_inference_mathematics_unchanged':True,'new_quality_scores':0,'test_labels_read':False})
 pins[str(prep)]=sha(prep)
 from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
 p=start('KrylovGram141_remaining_complete_prospective_controls_v19_20261008','verify_KrylovGram52_prospective_routes_v19_20261008.py',[],pins)
 d=start('KrylovGram141_remaining_chronological_dispatch_v19_20261008',Path(__file__).name,['dispatch'],pins)
 create(A/'KrylovGram141_actual140_closure_preflight_launches_v19_20261008.json',{'prospective':p,'dispatch':d,'input_sha256':pins})
 print(json.dumps({'prospective':p['owned_worker_pid'],'dispatch':d['owned_worker_pid']}),flush=True)
if __name__=='__main__':
 if sys.argv[1:] == ['dispatch']:dispatch()
 else:main()
