"""Bind the untouched149 queue to the actual148 recovery, with a correct predictor entry."""
from pathlib import Path
import ast,sys,time
ROOT=Path(__file__).resolve().parents[1]; A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
META=A/'Pure149_actual148_gate_recovery_v7_20261009.json'
GATES={
 'AdaptiveJointCrossHuber242_round148_full_registration_v1_20261008':'AdaptiveJointCrossHuber242_round148_full_registration_v2_20261009',
 'PureRFFHuber80_native_historical_calendar_controls_v2_20261008':'PureRFFHuber80_native_historical_calendar_controls_v4_20261009',
 'PureRFFHuber124_actual_full_historical_controls_v2_20261008':'PureRFFHuber124_actual_full_historical_controls_v4_20261009',
 'Pure149_prior_complete_forecast_duplicate_audit_v1_20261008':'Pure149_prior_complete_forecast_duplicate_audit_v3_20261009',
 'predict_AdaptivePureRFFHuber_complete_parent_scheme_v1_20261008':'predict_PureRFFHuber_complete_parent_scheme_v1_20261008'}
DRIVERS={
 'verify_PureRFFHuber80_native_historical_calendar_v2_20261008.py':'verify_PureRFFHuber80_native_historical_calendar_v4_20261009.py',
 'verify_PureRFFHuber124_full_historical_controls_v2_20261008.py':'verify_PureRFFHuber124_full_historical_controls_v4_20261009.py',
 'verify_Pure149_prior_complete_forecast_duplicate_audit_v1_20261008.py':'verify_Pure149_prior_complete_forecast_duplicate_audit_v3_20261009.py',
 'verify_PureRFFHuber128_round149_sources_v2_20261008.py':'verify_PureRFFHuber128_round149_sources_v6_20261009.py',
 'publish_PureRFFHuber128_evidence_v2_20261008.py':'publish_PureRFFHuber128_evidence_v6_20261009.py',
 'run_PureRFFHuber128_official_comparison_v2_20261008.py':'run_PureRFFHuber128_official_comparison_v4_20261009.py',
 'prepare_PureRFFHuber128_selected_candidate_v1_20261008.py':'prepare_PureRFFHuber128_selected_candidate_v3_20261009.py',
 'seal_PureRFFHuber128_selected_candidate_v1_20261008.py':'seal_PureRFFHuber128_selected_candidate_v3_20261009.py',
 'run_PureRFFHuber128_round149_full_registration_v2_20261008.py':'run_PureRFFHuber128_round149_full_registration_v5_20261009.py',
 'dispatch_PureRFFHuber149_complete_pipeline_v4_20261008.py':'dispatch_PureRFFHuber149_complete_pipeline_v6_20261009.py'}

def execute(original,phase=None):
 for p,d in read(META)['input_sha256'].items():assert sha(p)==d,p
 import prepare_PureRFFHuber128_round149_sources_v2_20261008 as generator
 paths=generator.source_paths
 extras=[Path(__file__),META,*(A/p for p in DRIVERS.values()),A/'predict_PureRFFHuber_complete_parent_scheme_v1_20261008.py']
 generator.source_paths=lambda:list(dict.fromkeys([*paths(),*extras]))
 import resume_pending149_verified_gates_v6_20261009 as prior
 prior.GATES.update(GATES);prior.SCRIPTS.update(DRIVERS)
 for old,key in [('verify_PureRFFHuber128_round149_sources_v4_20261008.py','verify_PureRFFHuber128_round149_sources_v2_20261008.py'),
  ('publish_PureRFFHuber128_evidence_v4_20261008.py','publish_PureRFFHuber128_evidence_v2_20261008.py'),
  ('run_PureRFFHuber128_round149_full_registration_v3_20261008.py','run_PureRFFHuber128_round149_full_registration_v2_20261008.py')]:
  prior.PREVIOUS_DRIVERS[old]=DRIVERS[key]
 old_route=prior.routed
 def route(s,dispatcher=False):
  return old_route(s,dispatcher).replace('complete_hidden_launches_v5_20261009','complete_hidden_launches_v6_20261009')
 prior.routed=route
 prior.execute(original,phase)

def main():
 services=A/'service_owned_workflows_20261006'
 failed=['PureRFFHuber80_native_historical_calendar_controls_v3_20261009',
  'PureRFFHuber124_actual_full_historical_controls_v3_20261009',
  'Pure149_prior_complete_forecast_duplicate_audit_v2_20261009',
  'PureRFFHuber149_complete_chronological_dispatch_v5_20261009']
 for n in failed:
  f=services/n;assert not owned(read(f/'native_launch.json'))
  assert read(f/'service_execution.json')['status']=='failed'
 for p in [Path('E:/赛题五_本机临时/PureRFFHuber80_native_historical_calendar_v2_20261008'),
  Path('E:/赛题五_本机临时/PureRFFHuber124_parent134_historical_v2_20261008'),
  Path('E:/赛题五_本机临时/Pure149_prior_complete_forecast_duplicate_audit_v2_20261009'),
  Path('E:/赛题五_本机临时/Pure149_prior_complete_forecast_duplicate_audit_v3_20261009'),
  A/'actual_PureRFFHuber80_native_calendar_location_v2_20261008.json',
  A/'actual_PureRFFHuber124_parent134_location_v2_20261008.json',
  A/'actual_Pure149_prior_complete_forecast_duplicate_audit_v2_20261009.json',
  A/'Pure149_prior_complete_forecast_duplicate_audit_raw_v2_20261009.json']:
  assert not p.exists(),p
 assert not (services/'PureRFFHuber128_round149_source_admission_v1_20261008').exists()
 import predict_PureRFFHuber_complete_parent_scheme_v1_20261008 as predictor
 abi=[]
 for backend,(filename,module,teacher) in predictor.BACKENDS.items():
  p=A/filename;compile(predictor.prepared_backend(p.read_text(encoding='utf8'),backend),str(p),'exec')
  abi.append({'backend':backend,'source':str(p),'sha256':sha(p)})
 products=[];originals=[];proofs=[]
 for old,new in DRIVERS.items():
  p=A/old;s=p.read_text(encoding='utf8');r=s
  for k,v in GATES.items():r=r.replace(k,v)
  def normalize(s):
   t=ast.parse(s)
   for n in ast.walk(t):
    if isinstance(n,ast.Constant) and isinstance(n.value,str):n.value='<string>'
    if isinstance(n,ast.ImportFrom) and n.module=='predict_AdaptivePureRFFHuber_complete_parent_scheme_v1_20261008':
     n.module='predict_PureRFFHuber_complete_parent_scheme_v1_20261008'
   return ast.dump(t,include_attributes=False)
  assert normalize(s)==normalize(r),old
  proofs.append({'original':str(p),'sha256':sha(p),'only_declared_service_paths_and_predictor_import_changed':True})
  code="from pathlib import Path\nimport sys\nROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]\nfrom recover_Pure149_actual148_gate_v7_20261009 import execute\n"
  if old.startswith('publish_'):
   code+="if __name__=='__main__':\n import argparse\n p=argparse.ArgumentParser();p.add_argument('phase',choices=('controls','scores'));execute("+repr(old)+",p.parse_args().phase)\n"
  else:code+="if __name__=='__main__':execute("+repr(old)+")\n"
  compile(code,str(A/new),'exec')
  with (A/new).open('x',encoding='utf8') as stream:stream.write(code)
  products.append(A/new);originals.append(p)
 prospective=A/'PureRFFHuber128_prospective_routes_v2_20261008.json'
 for p,d in read(prospective)['input_sha256'].items():assert sha(p)==d,p
 inputs=[Path(__file__),*products,*originals,prospective,A/'resume_pending149_verified_gates_v6_20261009.py',
  A/'actual_pending149_manual_resume_preparation_v6_20261009.json',
  A/'predict_PureRFFHuber_complete_parent_scheme_v1_20261008.py',A/'Adaptive148_candidate_entry_recovery_v6_20261009.json',
  *(services/n/'service_execution.json' for n in failed)]
 pins={str(p):sha(p) for p in inputs}
 create(META,{'status':'prepared149_actual_recovered148_gate_before_any_native_quality_or_future_execution',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'receiver_ast_controls':proofs,
  'actual5_parent_predictor_ABI_controls':abi,'all128_scientific_cases_and32_frozen_sources_unchanged':True,
  'failed_original_services_preserved':failed,'new_quality_scores':0,'new_native_fits':0,'test_labels_read':False})
 from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
 specs=[(GATES['PureRFFHuber80_native_historical_calendar_controls_v2_20261008'],products[0]),
  (GATES['PureRFFHuber124_actual_full_historical_controls_v2_20261008'],products[1]),
  (GATES['Pure149_prior_complete_forecast_duplicate_audit_v1_20261008'],products[2]),
  ('PureRFFHuber149_complete_chronological_dispatch_v6_20261009',products[-1])]
 rows={n:start(n,p.name,[],{**pins,str(META):sha(META)}) for n,p in specs}
 create(A/'Pure149_actual148_gate_hidden_launches_v7_20261009.json',rows)
 print({n:r['owned_worker_pid'] for n,r in rows.items()},flush=True)
if __name__=='__main__':main()
