"""Audit actual full forecast hashes against all prior full-board records with available complete-scheme hashes; never infer unobserved equality."""
from pathlib import Path
import sys,time,json,re,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
OUT=Path('E:/赛题五_本机临时/Pure149_prior_complete_forecast_duplicate_audit_v1_20261008')
def closed(n):
 p=A/'service_owned_workflows_20261006'/n
 while not (p/'service_execution.json').exists():time.sleep(10)
 while owned(read(p/'native_launch.json')):time.sleep(1)
 assert read(p/'service_execution.json')['status']=='passed',n
def signature(case):
 return tuple((stage,case[stage]['group'],case[stage]['share'],case[stage]['amplitude']) for stage in case['order'] if case[stage]['amplitude'])
def main():
 closed('AdaptiveJointCrossHuber242_round148_full_registration_v1_20261008')
 closed('PureRFFHuber124_actual_full_historical_controls_v2_20261008')
 import psutil
 while psutil.virtual_memory().available<3*2**30:time.sleep(15)
 from build_lossless_ranking_display_v2_20261006 import unpack_report
 display=A/'lossless_ranking_display_v2_20261006/round148';proof=read(display/'verification.json');page=display/'complete_rankings_lossless.html'
 assert proof['status']=='passed_all_original_report_values_and_six_views_lossless_roundtrip' and sha(page)==proof['lossless_HTML_sha256']
 match=re.search(r'<script\s+id="data"\s+type="application/json">(.*?)</script>',page.read_text(encoding='utf8'),re.S);assert match
 report=unpack_report(json.loads(match.group(1)));del match
 assert len(report['connected'])==proof['connected_records']
 pointer=A/'actual_PureRFFHuber124_parent134_location_v2_20261008.json';full=Path(read(pointer)['output'])/'verification.json';assert sha(full)==read(pointer)['verification_sha256']
 current=read(full);assert len(current['records'])==124
 plan=A/'PureRFFHuber128_round149_plan_v1_20261008.json';proposal=read(plan)
 inputs=[Path(__file__),display/'verification.json',page,pointer,full,plan,A/'optimization_20261003_r148/full_registration_execution.json',A/'github_validation_sync_main_20261005/round148_receipt.json']
 prior={};unavailable=[];ineligible=[];scanned=0
 for row in report['connected']:
  scanned+=1
  if row.get('known_restriction'):
   ineligible.append(row['id']);continue
  params=row.get('parameters',{});control=params.get('actual_full_conditional_residual_control',{})
  digest=params.get('original_numeric_prediction_sha256',control.get('prediction_numeric_bytes_sha256'))
  complete=bool(control.get('whole_complete_parent_branches_preserved_before_new_stage') or control.get('qualified_anchor_all8_metrics_exact'))
  if not digest or not complete:
   unavailable.append({'id':row['id'],'hash_available':bool(digest),'complete_graph_hash_proof_available':complete});continue
  assert re.fullmatch('[0-9a-f]{64}',digest)
  prior.setdefault(digest,[]).append({'id':row['id'],'source':row['source'],'source_pointer':row['source_pointer'],'score':row['score'],'metrics':row['metrics'],'all8_metrics':control.get('metrics')})
 # Explicitly verify the ten known zero/Cross-absent controls against actual147/148 complete forecasts and official capsules.
 previous={};known=[]
 for number,family,count,ptr in [(147,'JointCrossHuberOrder185',181,'actual_JointCrossHuber181_parent134_location_v2_20261008.json'),(148,'AdaptiveJointCrossHuber242',238,'actual_AdaptiveJointCrossHuber238_parent134_location_v3_20261008.json')]:
  p=A/ptr;v=Path(read(p)['output'])/'verification.json';assert sha(v)==read(p)['verification_sha256'];hist=read(v);assert len(hist['records'])==count
  pilot_path=A/(family+'_official_comparison_v1_20261008/verification.json');pilot=read(pilot_path)
  assert len(pilot['records'])==count+4
  by_case={r['configuration']['joint_control_case']:r for r in pilot['records'] if r['configuration'].get('joint_control_case') is not None}
  for r in hist['records']:
   measured=by_case[r['case']];assert measured['prediction_numeric_bytes_sha256']==r['numeric_sha256']
   previous.setdefault(signature(r['configuration']),[]).append({'round':number,'control_case':r['case'],'official_case':measured['case'],'numeric_sha256':r['numeric_sha256'],'metrics':measured['metrics']})
  inputs.extend([p,v,pilot_path])
 rows=[]
 for row in current['records']:
  digest=row['numeric_sha256'];cfg=row['configuration'];assert cfg==proposal['new_cases'][row['case']]
  semantic=previous.get(signature(cfg),[])
  for match in semantic:assert digest==match['numeric_sha256']
  if not cfg['cross']['amplitude']:
   assert semantic and digest in prior
   known.append({'control_case':row['case'],'actual_previous_complete_forecast_matches':semantic})
  rows.append({'control_case':row['case'],'configuration':cfg,'numeric_sha256':digest,'prior_full_board_matches':prior.get(digest,[]),'explicit147_148_semantic_matches':semantic,'has_prior_observed_forecast_duplicate':digest in prior})
 assert len(known)==10
 OUT.mkdir(exist_ok=False)
 create(OUT/'verification.json',{'status':'passed_actual124_forecast_hash_audit_against_prior_available_complete_scheme_hashes_and10_known_controls','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
  'input_sha256':{str(p):sha(p) for p in dict.fromkeys(inputs)},'actual_prior_full_board_records_scanned':scanned,'eligible_prior_numeric_hashes':len(prior),'prior_rows_without_sufficient_complete_forecast_hash_proof':unavailable,'ineligible_restricted_rows':ineligible,
  'actual_current_cases':124,'known_semantic_control_count':10,'known_controls':known,'records':rows,'remaining_cases_without_observed_prior_duplicate':sum(not r['has_prior_observed_forecast_duplicate'] for r in rows),
  'no_global_semantic_uniqueness_or_exhaustion_claimed':True,'all8_official_metrics_of_explicit_previous_matches_preserved_for_quality_crosscheck':True,'new_quality_scores':0,'new_model_fits':0,'test_labels_read':False})
 create(A/'actual_Pure149_prior_complete_forecast_duplicate_audit_v1_20261008.json',{'output':str(OUT),'verification_sha256':sha(OUT/'verification.json'),'new_quality_scores':0})
 print({'actual_cases':124,'known_controls':10,'board_records':scanned},flush=True)
if __name__=='__main__':main()
