"""Execute the preflighted joint147 pipeline after actual146, native80 and full181 closure."""
from pathlib import Path
import sys,time,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def closed(name):
 f=A/'service_owned_workflows_20261006'/name
 while not (f/'service_execution.json').exists():time.sleep(10)
 while owned(read(f/'native_launch.json')):time.sleep(1)
 assert read(f/'service_execution.json')['status']=='passed',name
def main():
 closed('PureRFFHuber149_complete_prospective_controls_v2_20261008')
 p=A/'PureRFFHuber128_prospective_routes_v2_20261008.json';proof=read(p)
 for f,d in proof['input_sha256'].items():assert sha(f)==d,f
 for n in ('Pure149_prior_complete_forecast_duplicate_audit_v1_20261008','AdaptiveJointCrossHuber242_round148_full_registration_v1_20261008','PureRFFHuber80_native_historical_calendar_controls_v2_20261008','PureRFFHuber124_actual_full_historical_controls_v2_20261008'):closed(n)
 from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
 specs=[('PureRFFHuber128_round149_source_admission_v1_20261008','verify_PureRFFHuber128_round149_sources_v4_20261008.py',[]),
  ('PureRFFHuber128_controls_main_publication_v1_20261008','publish_PureRFFHuber128_evidence_v4_20261008.py',['controls']),
  ('PureRFFHuber128_official_comparison_v1_20261008','run_PureRFFHuber128_official_comparison_v2_20261008.py',[]),
  ('PureRFFHuber128_scores_main_publication_v1_20261008','publish_PureRFFHuber128_evidence_v4_20261008.py',['scores']),
  ('PureRFFHuber128_selected_candidate_preparation_v1_20261008','prepare_PureRFFHuber128_selected_candidate_v1_20261008.py',[]),
  ('PureRFFHuber128_selected_candidate_sealing_v1_20261008','seal_PureRFFHuber128_selected_candidate_v1_20261008.py',[]),
  ('PureRFFHuber128_round149_full_registration_v1_20261008','run_PureRFFHuber128_round149_full_registration_v3_20261008.py',[])]
 from prepare_pending148_149_phase_isolated_publishers_v1_20261008 import META
 pins={str(Path(__file__)):sha(__file__),str(p):sha(p),str(META):sha(META)};rows={}
 for name,driver,args in specs:rows[name]=start(name,driver,args,{**pins,str(A/driver):sha(A/driver)})
 create(A/'PureRFFHuber149_complete_hidden_launches_v4_20261008.json',{'status':'started_seven_preflighted147_receivers_after_actual146_and80native124full_controls',
  'launches':rows,'input_sha256':pins,'stage_base_round':134,'expected_official_cases':128,'QA_version':60,
  'new_fits':0,'new_quality_scores_by_dispatch':0,'test_labels_read':False})
 print(json.dumps({'started':list(rows)}),flush=True)
if __name__=='__main__':main()
