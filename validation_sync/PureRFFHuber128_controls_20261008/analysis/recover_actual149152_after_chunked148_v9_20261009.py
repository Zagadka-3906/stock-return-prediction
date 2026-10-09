"""Recover failed waiting controllers; preserve all scientific cases and unused outputs."""
from pathlib import Path
import sys,time,ast
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
META=A/'actual149152_after_chunked148_recovery_v9_20261009.json'
BASE={
 'verify_PureRFFHuber80_native_historical_calendar_v2_20261008.py':'verify_PureRFFHuber80_native_historical_calendar_v5_20261009.py',
 'verify_PureRFFHuber124_full_historical_controls_v2_20261008.py':'verify_PureRFFHuber124_full_historical_controls_v5_20261009.py',
 'verify_Pure149_prior_complete_forecast_duplicate_audit_v1_20261008.py':'verify_Pure149_prior_complete_forecast_duplicate_audit_v4_20261009.py'}
CORE={
 'verify_PureRFFHuber128_round149_sources_v2_20261008.py':'verify_PureRFFHuber128_round149_sources_v8_20261009.py',
 'publish_PureRFFHuber128_evidence_v2_20261008.py':'publish_PureRFFHuber128_evidence_v8_20261009.py',
 'run_PureRFFHuber128_official_comparison_v2_20261008.py':'run_PureRFFHuber128_official_comparison_v6_20261009.py',
 'prepare_PureRFFHuber128_selected_candidate_v1_20261008.py':'prepare_PureRFFHuber128_selected_candidate_v5_20261009.py',
 'seal_PureRFFHuber128_selected_candidate_v1_20261008.py':'seal_PureRFFHuber128_selected_candidate_v5_20261009.py',
 'run_PureRFFHuber128_round149_full_registration_v2_20261008.py':'run_PureRFFHuber128_round149_full_registration_v7_20261009.py',
 'dispatch_PureRFFHuber149_complete_pipeline_v4_20261008.py':'dispatch_PureRFFHuber149_complete_pipeline_v8_20261009.py'}
GATES={
 'AdaptiveJointCrossHuber242_round148_full_registration_v1_20261008':'AdaptiveJointCrossHuber242_round148_full_registration_v4_20261009',
 'PureRFFHuber80_native_historical_calendar_controls_v2_20261008':'PureRFFHuber80_native_historical_calendar_controls_v5_20261009',
 'PureRFFHuber124_actual_full_historical_controls_v2_20261008':'PureRFFHuber124_actual_full_historical_controls_v5_20261009',
 'Pure149_prior_complete_forecast_duplicate_audit_v1_20261008':'Pure149_prior_complete_forecast_duplicate_audit_v4_20261009'}
def execute(original,phase=None):
 for p,d in read(META)['input_sha256'].items():assert sha(p)==d,p
 import prepare_PureRFFHuber128_round149_sources_v2_20261008 as g
 paths=g.source_paths;extra=[Path(__file__),META,*(A/n for n in [*BASE.values(),*CORE.values()])]
 g.source_paths=lambda:list(dict.fromkeys([*paths(),*extra]))
 import recover_Pure149_actual148_gate_v7_20261009 as prior
 prior.GATES.update(GATES);prior.DRIVERS.update({**BASE,**CORE})
 if original in BASE:prior.execute(original,phase);return
 import bind_Pure149_all5_annual_native_v8_20261009 as annual
 annual.COVERAGE='PureRFFHuber25_all5_annual_native_coverage_v2_20261009';annual.DRIVERS.update(CORE)
 import resume_pending149_verified_gates_v6_20261009 as base
 route=base.routed
 base.routed=lambda s,dispatcher=False:route(s,dispatcher).replace('complete_hidden_launches_v5_20261009','complete_hidden_launches_v8_20261009')
 annual.execute(original,phase)

def main():
 services=A/'service_owned_workflows_20261006'
 failed=['PureRFFHuber80_native_historical_calendar_controls_v4_20261009','PureRFFHuber124_actual_full_historical_controls_v4_20261009',
  'Pure149_prior_complete_forecast_duplicate_audit_v3_20261009','PureRFFHuber20_year2023_native_supplement_v1_20261009',
  'PureRFFHuber25_all5_annual_native_coverage_v1_20261009','PureRFFHuber149_complete_chronological_dispatch_v7_20261009',
  'SparseAfter14860_native_historical_calendar_controls_v1_20261009','SparseAfter14825_full_historical_controls_v1_20261009',
  'actual149_all5_and152_historical_main_publication_v52_20261009']
 for n in failed:
  f=services/n;assert not owned(read(f/'native_launch.json')) and read(f/'service_execution.json')['status']=='failed',n
 for p in [Path('E:/赛题五_本机临时/PureRFFHuber80_native_historical_calendar_v2_20261008'),
  Path('E:/赛题五_本机临时/PureRFFHuber124_parent134_historical_v2_20261008'),
  Path('E:/赛题五_本机临时/PureRFFHuber20_year2023_native_supplement_v1_20261009'),
  Path('E:/赛题五_本机临时/SparseAfter14860_native_historical_calendar_v1_20261009'),
  Path('E:/赛题五_本机临时/SparseAfter14825_parent148_historical_v1_20261009'),A/'Pure149_all25_annual_native_coverage_v1_20261009.json']:
  assert not p.exists(),p
 products=[]
 for old,new in {**BASE,**CORE}.items():
  code="from pathlib import Path\nimport sys\nROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]\nfrom recover_actual149152_after_chunked148_v9_20261009 import execute\n"
  if old.startswith('publish_'):code+="if __name__=='__main__':\n import argparse\n p=argparse.ArgumentParser();p.add_argument('phase',choices=('controls','scores'));execute("+repr(old)+",p.parse_args().phase)\n"
  else:code+="if __name__=='__main__':execute("+repr(old)+")\n"
  compile(code,str(A/new),'exec')
  with (A/new).open('x',encoding='utf8') as f:f.write(code)
  products.append(A/new)
 raw=[('verify_PureRFFHuber20_year2023_native_supplement_v1_20261009.py','verify_PureRFFHuber20_year2023_native_supplement_v2_20261009.py',{
  'AdaptiveJointCrossHuber242_round148_full_registration_v2_20261009':'AdaptiveJointCrossHuber242_round148_full_registration_v4_20261009',
  'PureRFFHuber80_native_historical_calendar_controls_v4_20261009':'PureRFFHuber80_native_historical_calendar_controls_v5_20261009'}),
  ('verify_SparseAfter14860_native_historical_calendar_v1_20261009.py','verify_SparseAfter14860_native_historical_calendar_v2_20261009.py',{
   'AdaptiveJointCrossHuber242_round148_full_registration_v2_20261009':'AdaptiveJointCrossHuber242_round148_full_registration_v4_20261009'}),
  ('verify_SparseAfter14825_full_historical_controls_v1_20261009.py','verify_SparseAfter14825_full_historical_controls_v2_20261009.py',{
   'AdaptiveJointCrossHuber242_round148_full_registration_v2_20261009':'AdaptiveJointCrossHuber242_round148_full_registration_v4_20261009',
   'SparseAfter14860_native_historical_calendar_controls_v1_20261009':'SparseAfter14860_native_historical_calendar_controls_v2_20261009'})]
 for old,new,replacements in raw:
  s=(A/old).read_text(encoding='utf8')
  for k,v in replacements.items():s=s.replace(k,v)
  compile(s,str(A/new),'exec')
  with (A/new).open('x',encoding='utf8') as f:f.write(s)
  products.append(A/new)
 coverage=A/'verify_Pure149_all25_annual_native_coverage_v2_20261009.py'
 code="from pathlib import Path\nimport sys\nROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]\ns=(A/'bind_Pure149_all5_annual_native_v8_20261009.py').read_text(encoding='utf8').replace('PureRFFHuber80_native_historical_calendar_controls_v4_20261009','PureRFFHuber80_native_historical_calendar_controls_v5_20261009').replace('PureRFFHuber20_year2023_native_supplement_v1_20261009','PureRFFHuber20_year2023_native_supplement_v2_20261009')\nns={'__file__':str(A/'bind_Pure149_all5_annual_native_v8_20261009.py'),'__name__':'verified_annual_coverage_service_binding'}\nexec(compile(s,str(A/'bind_Pure149_all5_annual_native_v8_20261009.py'),'exec'),ns)\nif __name__=='__main__':ns['verify_coverage']()\n"
 compile(code,str(coverage),'exec')
 with coverage.open('x',encoding='utf8') as f:f.write(code)
 products.append(coverage)
 pubold=A/'publish_actual149_all5_and152_historical_main_v52_20261009.py';s=pubold.read_text(encoding='utf8')
 mapping={**raw[0][2],**raw[1][2],**raw[2][2],
  'PureRFFHuber20_year2023_native_supplement_v1_20261009':'PureRFFHuber20_year2023_native_supplement_v2_20261009',
  'PureRFFHuber25_all5_annual_native_coverage_v1_20261009':'PureRFFHuber25_all5_annual_native_coverage_v2_20261009'}
 for k,v in mapping.items():s=s.replace(k,v)
 s=s.replace('actual149_all5_and152_historical_main_v52','actual149_all5_and152_historical_main_v53').replace('actual149_all5_and152_historical_v52','actual149_all5_and152_historical_v53')
 needle='sources=[Path(__file__),*pointers,*proofs,';assert s.count(needle)==1
 s=s.replace(needle,"sources=[Path(__file__),A/'recover_actual149152_after_chunked148_v9_20261009.py',A/'actual149152_after_chunked148_recovery_v9_20261009.json',*pointers,*proofs,")
 publisher=A/'publish_actual149_all5_and152_historical_main_v53_20261009.py';compile(s,str(publisher),'exec')
 with publisher.open('x',encoding='utf8') as f:f.write(s)
 products.append(publisher)
 inputs=[Path(__file__),*products,*(A/p for p in [*BASE,*CORE]),*(A/old for old,_,_ in raw),pubold,
  A/'Pure149_all5_annual_native_receiver_binding_v8_20261009.json',*(services/n/'service_execution.json' for n in failed)]
 pins={str(p):sha(p) for p in inputs}
 create(META,{'status':'prepared_failed_wait_only149152_controllers_after_actual148_chunked_publication_recovery',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'old_failed_services_preserved':failed,
  'all128_and29_case_parameters_and32_frozen149_sources_unchanged':True,'all5_annual_coverage_before149_quality_retained':True,
  'previously_unused_scientific_outputs_reused_only_after_no_execution_verified':True,'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
 from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
 specs=[(GATES['PureRFFHuber80_native_historical_calendar_controls_v2_20261008'],A/BASE['verify_PureRFFHuber80_native_historical_calendar_v2_20261008.py']),
  (GATES['PureRFFHuber124_actual_full_historical_controls_v2_20261008'],A/BASE['verify_PureRFFHuber124_full_historical_controls_v2_20261008.py']),
  (GATES['Pure149_prior_complete_forecast_duplicate_audit_v1_20261008'],A/BASE['verify_Pure149_prior_complete_forecast_duplicate_audit_v1_20261008.py']),
  ('PureRFFHuber20_year2023_native_supplement_v2_20261009',products[10]),('PureRFFHuber25_all5_annual_native_coverage_v2_20261009',coverage),
  ('PureRFFHuber149_complete_chronological_dispatch_v8_20261009',A/CORE['dispatch_PureRFFHuber149_complete_pipeline_v4_20261008.py']),
  ('SparseAfter14860_native_historical_calendar_controls_v2_20261009',products[11]),
  ('SparseAfter14825_full_historical_controls_v2_20261009',products[12]),
  ('actual149_all5_and152_historical_main_publication_v53_20261009',publisher)]
 rows={n:start(n,p.name,[],{**pins,str(META):sha(META)}) for n,p in specs}
 create(A/'actual149152_after_chunked148_hidden_launches_v9_20261009.json',rows)
 print({n:r['owned_worker_pid'] for n,r in rows.items()},flush=True)
if __name__=='__main__':main()
