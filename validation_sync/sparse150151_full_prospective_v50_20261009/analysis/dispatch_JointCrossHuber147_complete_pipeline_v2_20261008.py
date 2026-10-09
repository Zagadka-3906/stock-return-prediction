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
 closed('JointCrossHuber147_complete_prospective_controls_v2_20261008')
 p=A/'JointCrossHuberOrder185_prospective_routes_v2_20261008.json';proof=read(p)
 for f,d in proof['input_sha256'].items():assert sha(f)==d,f
 for n in ('HuberCrossFamilyFine125_round146_full_registration_v2_20261008','JointCrossHuber80_native_historical_calendar_controls_v2_20261008','JointCrossHuber181_actual_full_historical_controls_v1_20261008'):closed(n)
 from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
 specs=[('JointCrossHuberOrder185_round147_source_admission_v1_20261008','verify_JointCrossHuberOrder185_round147_sources_v2_20261008.py',[]),
  ('JointCrossHuberOrder185_controls_main_publication_v1_20261008','publish_JointCrossHuberOrder185_evidence_v4_20261008.py',['controls']),
  ('JointCrossHuberOrder185_official_comparison_v1_20261008','run_JointCrossHuberOrder185_official_comparison_v1_20261008.py',[]),
  ('JointCrossHuberOrder185_scores_main_publication_v1_20261008','publish_JointCrossHuberOrder185_evidence_v4_20261008.py',['scores']),
  ('JointCrossHuberOrder185_selected_candidate_preparation_v1_20261008','prepare_JointCrossHuberOrder185_selected_candidate_v3_20261008.py',[]),
  ('JointCrossHuberOrder185_selected_candidate_sealing_v1_20261008','seal_JointCrossHuberOrder185_selected_candidate_v1_20261008.py',[]),
  ('JointCrossHuberOrder185_round147_full_registration_v1_20261008','run_JointCrossHuberOrder185_round147_full_registration_v5_20261008.py',[])]
 pins={str(Path(__file__)):sha(__file__),str(p):sha(p)};rows={}
 for name,driver,args in specs:rows[name]=start(name,driver,args,{**pins,str(A/driver):sha(A/driver)})
 create(A/'JointCrossHuber147_complete_hidden_launches_v2_20261008.json',{'status':'started_seven_preflighted147_receivers_after_actual146_and80native181full_controls',
  'launches':rows,'input_sha256':pins,'stage_base_round':134,'expected_official_cases':185,'QA_version':58,
  'new_fits':0,'new_quality_scores_by_dispatch':0,'test_labels_read':False})
 print(json.dumps({'started':list(rows)}),flush=True)
if __name__=='__main__':main()
