"""Recover a failed path-only entry without changing any of the 242 scored schemes."""
from pathlib import Path
import ast, sys, time, subprocess
ROOT=Path(__file__).resolve().parents[1]; A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
META=A/'Adaptive148_candidate_entry_recovery_v6_20261009.json'
OLD_RELEASE='AdaptiveJointCrossHuber242_selected_release_v1_20261008'
NEW_RELEASE='AdaptiveJointCrossHuber242_selected_release_v2_20261009'
OLD_CANDIDATE='AdaptiveJointCrossHuber242_v1_20261008'
NEW_CANDIDATE='AdaptiveJointCrossHuber242_v2_20261009'
MAP={
 'predict_AdaptiveAdaptiveJointCrossHuber_complete_parent_scheme_v1_20261008':'predict_AdaptiveJointCrossHuber_complete_parent_scheme_v1_20261008',
 OLD_RELEASE:NEW_RELEASE, OLD_CANDIDATE:NEW_CANDIDATE,
 'pre_inference_source_freeze_v1':'pre_inference_source_freeze_v2_20261009',
 'AdaptiveJointCrossHuber148_D_scoring_v1_20261008/selected/':'AdaptiveJointCrossHuber148_D_scoring_v1_20261008/selected_v2_20261009/',
 'AdaptiveJointCrossHuber242_selected_candidate_preparation_v1_20261008':'AdaptiveJointCrossHuber242_selected_candidate_preparation_v2_20261009',
 'AdaptiveJointCrossHuber242_selected_candidate_sealing_v1_20261008':'AdaptiveJointCrossHuber242_selected_candidate_sealing_v2_20261009',
 'seal_AdaptiveJointCrossHuber242_selected_candidate_v1_20261008.py':'seal_AdaptiveJointCrossHuber242_selected_candidate_v3_20261009.py',
 'AdaptiveJointCrossHuber242_round148_actual_registration_v2_20261008':'AdaptiveJointCrossHuber242_round148_actual_registration_v3_20261009'}
DRIVERS={
 'prepare_AdaptiveJointCrossHuber242_selected_candidate_v1_20261008.py':'prepare_AdaptiveJointCrossHuber242_selected_candidate_v4_20261009.py',
 'seal_AdaptiveJointCrossHuber242_selected_candidate_v1_20261008.py':'seal_AdaptiveJointCrossHuber242_selected_candidate_v3_20261009.py',
 'run_AdaptiveJointCrossHuber242_round148_full_registration_v2_20261008.py':'run_AdaptiveJointCrossHuber242_round148_full_registration_v6_20261009.py'}

def closed(name):
 f=A/'service_owned_workflows_20261006'/name
 while not (f/'service_execution.json').exists(): time.sleep(10)
 while owned(read(f/'native_launch.json')): time.sleep(1)
 assert read(f/'service_execution.json')['status']=='passed',name

def execute(original):
 for p,d in read(META)['input_sha256'].items(): assert sha(p)==d,p
 import AdaptiveJointCrossHuber148_storage_v1_20261008 as storage
 for p,t in read(META)['new_E_outputs'].items(): storage.OUTPUTS[Path(p)]=Path(t)
 import prepare_AdaptiveJointCrossHuber242_round148_sources_v2_20261008 as g
 paths=g.source_paths
 extras=[Path(__file__),META,*(A/n for n in DRIVERS.values()),A/'predict_AdaptiveJointCrossHuber_complete_parent_scheme_v1_20261008.py']
 g.source_paths=lambda:list(dict.fromkeys([*paths(),*extras]))
 import resume_pending148_verified_gates_v5_20261009 as prior
 prior.GATES.update(MAP); prior.SCRIPTS.update(DRIVERS)
 if original.startswith('run_'):
  closed(MAP['AdaptiveJointCrossHuber242_selected_candidate_sealing_v1_20261008'])
  new=A/NEW_RELEASE/'selected_candidate_ready_for_registration.json'
  old=A/OLD_RELEASE/'selected_candidate_ready_for_registration.json'
  value=read(new)
  assert value['sealed_candidate_complete'] and value['source_release']==str(new.parent)
  assert not old.exists()
  with old.open('xb') as stream: stream.write(new.read_bytes())
  create(A/'Adaptive148_actual_sealed_retry2_pointer_bridge_v1_20261009.json',{
   'status':'previously_absent_ready_pointer_names_actual_sealed_retry2',
   'source':str(new),'alias':str(old),'sha256':sha(new),
   'old_failed_services_not_marked_passed':True,'canonical32_source_bytes_unchanged':True})
 prior.execute(original)

def junction(access,target):
 assert access.is_relative_to(ROOT) and target.is_relative_to(Path('E:/赛题五_本机临时/第148轮_20261008'))
 assert not access.exists() and not target.exists()
 target.mkdir(parents=True); access.parent.mkdir(parents=True,exist_ok=True)
 q=lambda p:"'"+str(p).replace("'","''")+"'"
 r=subprocess.run(['pwsh','-NoProfile','-NonInteractive','-Command',
  "New-Item -ItemType Junction -Path "+q(access)+' -Target '+q(target)+' | Out-Null'],
  capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
 assert r.returncode==0,r.stderr
 assert access.is_junction() and access.resolve()==target.resolve() and not any(target.iterdir())

def main():
 services=A/'service_owned_workflows_20261006'
 failed=['AdaptiveJointCrossHuber242_selected_candidate_preparation_v1_20261008',
  'AdaptiveJointCrossHuber242_selected_candidate_sealing_v1_20261008',
  'AdaptiveJointCrossHuber242_round148_full_registration_v1_20261008']
 for n in failed:
  f=services/n; assert not owned(read(f/'native_launch.json'))
  assert read(f/'service_execution.json')['status']=='failed'
 assert [p.name for p in (A/OLD_RELEASE).iterdir()]==['scientific_protocol_resolution_before_future_features.json']
 assert not any((ROOT/'candidates'/OLD_CANDIDATE).iterdir())
 pilot=A/'AdaptiveJointCrossHuber242_official_comparison_v1_20261008/verification.json'
 assert len(read(pilot)['records'])==242 and read(pilot)['best']['case']==175
 import predict_AdaptiveJointCrossHuber_complete_parent_scheme_v1_20261008 as predictor
 abi=[]
 for backend,(filename,module,teacher) in predictor.BACKENDS.items():
  p=A/filename; prepared=predictor.prepared_backend(p.read_text(encoding='utf8'),backend)
  compile(prepared,str(p),'exec'); abi.append({'backend':backend,'source':str(p),'sha256':sha(p)})
 originals=[];products=[];ast_proofs=[]
 for old,new in DRIVERS.items():
  p=A/old; before=p.read_text(encoding='utf8'); after=before
  for k,v in MAP.items(): after=after.replace(k,v)
  def normalized(s):
   t=ast.parse(s)
   for node in ast.walk(t):
    if isinstance(node,ast.Constant) and isinstance(node.value,str): node.value='<string>'
    if isinstance(node,ast.ImportFrom) and node.module=='predict_AdaptiveAdaptiveJointCrossHuber_complete_parent_scheme_v1_20261008':
     node.module='predict_AdaptiveJointCrossHuber_complete_parent_scheme_v1_20261008'
   return ast.dump(t,include_attributes=False)
  assert normalized(before)==normalized(after),old
  ast_proofs.append({'original':str(p),'original_sha256':sha(p),'only_declared_path_strings_and_predictor_import_changed':True})
  code="from pathlib import Path\nimport sys\nROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]\nfrom recover_Adaptive148_candidate_entry_v6_20261009 import execute\nif __name__=='__main__':execute("+repr(old)+")\n"
  compile(code,str(A/new),'exec')
  with (A/new).open('x',encoding='utf8') as stream:stream.write(code)
  originals.append(p);products.append(A/new)
 outputs={str(A/NEW_RELEASE):str(Path('E:/赛题五_本机临时/第148轮_20261008/selected_release_retry2_20261009')),
  str(ROOT/'candidates'/NEW_CANDIDATE):str(Path('E:/赛题五_本机临时/第148轮_20261008/candidate_retry2_20261009'))}
 for p,t in outputs.items():junction(Path(p),Path(t))
 inputs=[Path(__file__),*originals,*products,pilot,A/'AdaptiveJointCrossHuber242_scores_github_v1_20261008/receipt.json',
  A/'predict_AdaptiveJointCrossHuber_complete_parent_scheme_v1_20261008.py',
  A/'resume_pending148_verified_gates_v5_20261009.py',A/'actual_pending148_manual_resume_preparation_v5_20261009.json',
  *(services/n/'service_execution.json' for n in failed)]
 pins={str(p):sha(p) for p in inputs}
 create(META,{'status':'prepared_failed148_entry_recovery_before_any_new_future_features',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'new_E_outputs':outputs,
  'receiver_ast_controls':ast_proofs,'actual5_parent_predictor_ABI_controls':abi,
  'all242_scored_configurations_and32_canonical_source_hashes_unchanged':True,
  'failed_original_services_preserved':failed,'new_native_fits':0,'new_official_scores':0,'test_labels_read':False})
 from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
 specs=[('AdaptiveJointCrossHuber242_selected_candidate_preparation_v2_20261009',products[0]),
  ('AdaptiveJointCrossHuber242_selected_candidate_sealing_v2_20261009',products[1]),
  ('AdaptiveJointCrossHuber242_round148_full_registration_v2_20261009',products[2])]
 rows={n:start(n,p.name,[],{**pins,str(META):sha(META)}) for n,p in specs}
 create(A/'Adaptive148_candidate_entry_hidden_launches_v6_20261009.json',rows)
 print({n:r['owned_worker_pid'] for n,r in rows.items()},flush=True)
if __name__=='__main__':main()
