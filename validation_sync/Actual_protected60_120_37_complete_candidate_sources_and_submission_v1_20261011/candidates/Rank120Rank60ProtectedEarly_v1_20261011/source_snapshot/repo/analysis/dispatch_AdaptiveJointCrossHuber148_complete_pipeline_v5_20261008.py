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
 closed('AdaptiveJointCrossHuber148_complete_prospective_controls_v2_20261008')
 p=A/'AdaptiveJointCrossHuber242_prospective_routes_v2_20261008.json';proof=read(p)
 for f,d in proof['input_sha256'].items():assert sha(f)==d,f
 for n in ('JointCrossHuberOrder185_round147_full_registration_v1_20261008','AdaptiveJointCrossHuber80_native_historical_calendar_controls_v3_20261008','AdaptiveJointCrossHuber238_actual_full_historical_controls_v3_20261008'):closed(n)
 from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
 specs=[('AdaptiveJointCrossHuber242_round148_source_admission_v1_20261008','verify_AdaptiveJointCrossHuber242_round148_sources_v5_20261008.py',[]),
  ('AdaptiveJointCrossHuber242_controls_main_publication_v1_20261008','publish_AdaptiveJointCrossHuber242_evidence_v5_20261008.py',['controls']),
  ('AdaptiveJointCrossHuber242_official_comparison_v1_20261008','run_AdaptiveJointCrossHuber242_official_comparison_v1_20261008.py',[]),
  ('AdaptiveJointCrossHuber242_scores_main_publication_v1_20261008','publish_AdaptiveJointCrossHuber242_evidence_v5_20261008.py',['scores']),
  ('AdaptiveJointCrossHuber242_selected_candidate_preparation_v1_20261008','prepare_AdaptiveJointCrossHuber242_selected_candidate_v2_20261008.py',[]),
  ('AdaptiveJointCrossHuber242_selected_candidate_sealing_v1_20261008','seal_AdaptiveJointCrossHuber242_selected_candidate_v1_20261008.py',[]),
  ('AdaptiveJointCrossHuber242_round148_full_registration_v1_20261008','run_AdaptiveJointCrossHuber242_round148_full_registration_v4_20261008.py',[])]
 from prepare_pending148_149_phase_isolated_publishers_v1_20261008 import META
 pins={str(Path(__file__)):sha(__file__),str(p):sha(p),str(META):sha(META)};rows={}
 for name,driver,args in specs:rows[name]=start(name,driver,args,{**pins,str(A/driver):sha(A/driver)})
 create(A/'AdaptiveJointCrossHuber148_complete_hidden_launches_v5_20261008.json',{'status':'started_seven_preflighted147_receivers_after_actual146_and80native238full_controls',
  'launches':rows,'input_sha256':pins,'stage_base_round':134,'expected_official_cases':242,'QA_version':59,
  'new_fits':0,'new_quality_scores_by_dispatch':0,'test_labels_read':False})
 print(json.dumps({'started':list(rows)}),flush=True)
if __name__=='__main__':main()
