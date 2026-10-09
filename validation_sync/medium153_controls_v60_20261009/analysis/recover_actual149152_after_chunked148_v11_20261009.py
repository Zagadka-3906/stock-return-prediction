"""Prepare current bindings and launch only after148 chunked main publication actually passes."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
import os
count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
for offset,(key,value) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):
 os.environ[f'GIT_CONFIG_KEY_{count+offset}']=key;os.environ[f'GIT_CONFIG_VALUE_{count+offset}']=value
os.environ['GIT_CONFIG_COUNT']=str(count+2)
META=A/'actual149152_after_chunked148_recovery_v11_20261009.json'
BASE={
 'verify_PureRFFHuber80_native_historical_calendar_v2_20261008.py':'verify_PureRFFHuber80_native_historical_calendar_v7_20261009.py',
 'verify_PureRFFHuber124_full_historical_controls_v2_20261008.py':'verify_PureRFFHuber124_full_historical_controls_v7_20261009.py',
 'verify_Pure149_prior_complete_forecast_duplicate_audit_v1_20261008.py':'verify_Pure149_prior_complete_forecast_duplicate_audit_v6_20261009.py'}
CORE={
 'verify_PureRFFHuber128_round149_sources_v2_20261008.py':'verify_PureRFFHuber128_round149_sources_v10_20261009.py',
 'publish_PureRFFHuber128_evidence_v2_20261008.py':'publish_PureRFFHuber128_evidence_v10_20261009.py',
 'run_PureRFFHuber128_official_comparison_v2_20261008.py':'run_PureRFFHuber128_official_comparison_v8_20261009.py',
 'prepare_PureRFFHuber128_selected_candidate_v1_20261008.py':'prepare_PureRFFHuber128_selected_candidate_v7_20261009.py',
 'seal_PureRFFHuber128_selected_candidate_v1_20261008.py':'seal_PureRFFHuber128_selected_candidate_v7_20261009.py',
 'run_PureRFFHuber128_round149_full_registration_v2_20261008.py':'run_PureRFFHuber128_round149_full_registration_v9_20261009.py',
 'dispatch_PureRFFHuber149_complete_pipeline_v4_20261008.py':'dispatch_PureRFFHuber149_complete_pipeline_v10_20261009.py'}
def closed(n):
 f=A/'service_owned_workflows_20261006'/n
 while not (f/'service_execution.json').exists():time.sleep(10)
 while owned(read(f/'native_launch.json')):time.sleep(1)
 assert read(f/'service_execution.json')['status']=='passed',n
def execute(original,phase=None):
 for p,d in read(META)['input_sha256'].items():assert sha(p)==d,p
 import recover_actual149152_after_chunked148_v9_20261009 as prior
 prior.GATES.update({
  'AdaptiveJointCrossHuber242_round148_full_registration_v1_20261008':'AdaptiveJointCrossHuber242_round148_full_registration_v6_20261009',
  'PureRFFHuber80_native_historical_calendar_controls_v2_20261008':'PureRFFHuber80_native_historical_calendar_controls_v6_20261009'})
 prior.BASE.update(BASE);prior.CORE.update(CORE)
 import prepare_PureRFFHuber128_round149_sources_v2_20261008 as g
 paths=g.source_paths;extra=[Path(__file__),META,*(A/p for p in [*BASE.values(),*CORE.values()])]
 g.source_paths=lambda:list(dict.fromkeys([*paths(),*extra]))
 if original.startswith('dispatch_'):
  import resume_pending149_verified_gates_v6_20261009 as base
  route=base.routed;base.routed=lambda s,dispatcher=False:route(s,dispatcher).replace('complete_hidden_launches_v5_20261009','complete_hidden_launches_v11_20261009')
 prior.execute(original,phase)
def dispatch():
 for p,d in read(META)['input_sha256'].items():assert sha(p)==d,p
 closed('AdaptiveJointCrossHuber242_round148_full_registration_v6_20261009')
 specs=read(META)['specs']
 from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
 rows={}
 for n,p in specs:rows[n]=start(n,p,[],{str(META):sha(META),str(A/p):sha(A/p),str(Path(__file__)):sha(__file__)})
 create(A/'actual149152_after_chunked148_hidden_launches_v11_20261009.json',rows)
 print({n:r['owned_worker_pid'] for n,r in rows.items()},flush=True)
def main():
 services=A/'service_owned_workflows_20261006'
 failed=services/'PureRFFHuber80_native_historical_calendar_controls_v5_20261009'
 assert read(failed/'service_execution.json')['status']=='failed' and not owned(read(failed/'native_launch.json'))
 products=[]
 for old,new in {**BASE,**CORE}.items():
  s="from pathlib import Path\nimport sys\nROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]\nfrom recover_actual149152_after_chunked148_v10_20261009 import execute\n"
  if old.startswith('publish_'):s+="if __name__=='__main__':\n import argparse\n p=argparse.ArgumentParser();p.add_argument('phase',choices=('controls','scores'));execute("+repr(old)+",p.parse_args().phase)\n"
  else:s+="if __name__=='__main__':execute("+repr(old)+")\n"
  compile(s,str(A/new),'exec')
  with (A/new).open('x',encoding='utf8') as f:f.write(s)
  products.append(A/new)
 raw=[('verify_PureRFFHuber20_year2023_native_supplement_v2_20261009.py','verify_PureRFFHuber20_year2023_native_supplement_v4_20261009.py'),
  ('verify_Pure149_all25_annual_native_coverage_v2_20261009.py','verify_Pure149_all25_annual_native_coverage_v4_20261009.py'),
  ('verify_SparseAfter14860_native_historical_calendar_v2_20261009.py','verify_SparseAfter14860_native_historical_calendar_v4_20261009.py'),
  ('verify_SparseAfter14825_full_historical_controls_v2_20261009.py','verify_SparseAfter14825_full_historical_controls_v4_20261009.py'),
  ('publish_actual149_all5_and152_historical_main_v53_20261009.py','publish_actual149_all5_and152_historical_main_v55_20261009.py')]
 replacements={
  'AdaptiveJointCrossHuber242_round148_full_registration_v4_20261009':'AdaptiveJointCrossHuber242_round148_full_registration_v6_20261009',
  'PureRFFHuber80_native_historical_calendar_controls_v5_20261009':'PureRFFHuber80_native_historical_calendar_controls_v6_20261009',
  'actual149_all5_and152_historical_main_v53':'actual149_all5_and152_historical_main_v55',
  'actual149_all5_and152_historical_v53':'actual149_all5_and152_historical_v55'}
 for old,new in raw:
  s=(A/old).read_text(encoding='utf8')
  for k,v in replacements.items():s=s.replace(k,v)
  if old.startswith('publish_'):
   s=s.replace("sources=[Path(__file__),","sources=[Path(__file__),A/'recover_actual149152_after_chunked148_v11_20261009.py',A/'actual149152_after_chunked148_recovery_v11_20261009.json',",1)
  compile(s,str(A/new),'exec')
  with (A/new).open('x',encoding='utf8') as f:f.write(s)
  products.append(A/new)
 specs=[('PureRFFHuber80_native_historical_calendar_controls_v6_20261009',products[0].name),
  ('PureRFFHuber124_actual_full_historical_controls_v5_20261009',products[1].name),
  ('Pure149_prior_complete_forecast_duplicate_audit_v4_20261009',products[2].name),
  ('PureRFFHuber20_year2023_native_supplement_v2_20261009',products[10].name),
  ('PureRFFHuber25_all5_annual_native_coverage_v2_20261009',products[11].name),
  ('PureRFFHuber149_complete_chronological_dispatch_v11_20261009',A.joinpath(CORE['dispatch_PureRFFHuber149_complete_pipeline_v4_20261008.py']).name),
  ('SparseAfter14860_native_historical_calendar_controls_v2_20261009',products[12].name),
  ('SparseAfter14825_full_historical_controls_v2_20261009',products[13].name),
  ('actual149_all5_and152_historical_main_publication_v55_20261009',products[14].name)]
 assert all(not (services/n).exists() for n,_ in specs)
 inputs=[Path(__file__),*products,A/'recover_actual149152_after_chunked148_v9_20261009.py',
  A/'actual149152_after_chunked148_recovery_v9_20261009.json',failed/'service_execution.json',*(A/p for p,_ in raw)]
 pins={str(p):sha(p) for p in inputs}
 create(META,{'status':'prepared_current149152_recovery_launch_only_after_actual148_chunked_main_PASS',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'specs':specs,
  'all_original_scientific_cases_parameters_and_unused_outputs_unchanged':True,
  'original_failed_native5_preserved_not_marked_passed':True,'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
 from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
 row=start('actual149152_recovery_after_actual148_chunked_main_v11_20261009',Path(__file__).name,['--dispatch'],{**pins,str(META):sha(META)})
 create(A/'actual149152_recovery_waiting_dispatch_launch_v11_20261009.json',row);print(row['owned_worker_pid'],flush=True)
if __name__=='__main__':
 if '--dispatch' in sys.argv:dispatch()
 else:main()
