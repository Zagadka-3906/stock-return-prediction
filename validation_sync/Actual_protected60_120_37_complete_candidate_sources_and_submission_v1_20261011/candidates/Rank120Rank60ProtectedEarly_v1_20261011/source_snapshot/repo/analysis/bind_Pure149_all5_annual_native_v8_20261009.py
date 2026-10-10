"""Supplement the missing2023 composite stage and bind all25 states before149 quality."""
from pathlib import Path
import sys,time,hashlib,ast
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
META=A/'Pure149_all5_annual_native_receiver_binding_v8_20261009.json'
PROOF=A/'Pure149_all25_annual_native_coverage_v1_20261009.json'
SUPPLEMENT='PureRFFHuber20_year2023_native_supplement_v1_20261009'
COVERAGE='PureRFFHuber25_all5_annual_native_coverage_v1_20261009'
DRIVERS={
 'verify_PureRFFHuber128_round149_sources_v2_20261008.py':'verify_PureRFFHuber128_round149_sources_v7_20261009.py',
 'publish_PureRFFHuber128_evidence_v2_20261008.py':'publish_PureRFFHuber128_evidence_v7_20261009.py',
 'run_PureRFFHuber128_official_comparison_v2_20261008.py':'run_PureRFFHuber128_official_comparison_v5_20261009.py',
 'prepare_PureRFFHuber128_selected_candidate_v1_20261008.py':'prepare_PureRFFHuber128_selected_candidate_v4_20261009.py',
 'seal_PureRFFHuber128_selected_candidate_v1_20261008.py':'seal_PureRFFHuber128_selected_candidate_v4_20261009.py',
 'run_PureRFFHuber128_round149_full_registration_v2_20261008.py':'run_PureRFFHuber128_round149_full_registration_v6_20261009.py',
 'dispatch_PureRFFHuber149_complete_pipeline_v4_20261008.py':'dispatch_PureRFFHuber149_complete_pipeline_v7_20261009.py'}

def closed(name):
 f=A/'service_owned_workflows_20261006'/name
 while not (f/'service_execution.json').exists():time.sleep(10)
 while owned(read(f/'native_launch.json')):time.sleep(1)
 assert read(f/'service_execution.json')['status']=='passed',name

def verify_coverage():
 closed('PureRFFHuber80_native_historical_calendar_controls_v4_20261009');closed(SUPPLEMENT)
 planpath=A/'PureRFFHuber128_round149_proposal_v1_20261008.json';plan=read(planpath)
 pointers=[A/'actual_PureRFFHuber80_native_calendar_location_v2_20261008.json',
  A/'actual_PureRFFHuber20_year2023_native_supplement_location_v1_20261009.json']
 stages=[];inputs=[Path(__file__),META,planpath];seen={};prior=set();additional=set()
 for p in pointers:
  proof=Path(read(p)['output'])/'verification.json';assert sha(proof)==read(p)['verification_sha256']
  stages.append(read(proof));inputs.extend([p,proof])
 assert (stages[0]['actual_historical_cases'],stages[0]['actual_calendar_cases'],stages[0]['actual_cold_cases'])==(60,20,80)
 assert (stages[1]['actual_historical_cases'],stages[1]['actual_calendar_cases'],stages[1]['actual_cold_cases'])==(20,0,20)
 assert len(stages[0]['records'])==80 and len(stages[1]['records'])==20
 for i,stage in enumerate(stages):
  for record in stage['records']:
   if i==1:assert record['year']==2023 and record['saved_OOF_and_native_bits_exact']
   for mode in ('full','cold'):
    r=record[mode]
    assert r['complete_parent2020_flag1_invalid_bits_preserved'] and r['all_stage_native_reload_independent_and_Pandas_bits_checked']
    assert r['all_nonzero_stages_use_same_original_teacher106'] and r['actual_complete_qualified_base_round']==134
    for step in r['stage_reports']:
     native=step['native_reload_independent_and_Pandas_report']
     assert native['native_reload_independent_arithmetic_and_Pandas_complete_parent_CDF_bits_exact']
     assert native['saved_fit_year_fixed_for_all_prediction_dates']
     for c in native['controls']:
      key=(c['head'],c['year']);assert c['reload_exact'] and c['independent_decoder_exact']
      row=plan['heads'][key[0]];info_path=Path(row['infos'][str(key[1])]);info=read(info_path)
      state=(c['sha256'],c['independent_state_sha256'])
      assert state==(info['native_model_sha256'],info['independent_'+row['state_kind']+'_state_sha256'])
      assert seen.setdefault(key,state)==state
      (prior if i==0 else additional).add(key);inputs.append(info_path)
 expected={(h,y) for h in plan['heads'] for y in range(2021,2026)}
 assert set(seen)==expected and len(prior)==20 and len(additional)==5 and prior.isdisjoint(additional)
 for n in ('PureRFFHuber80_native_historical_calendar_controls_v4_20261009',SUPPLEMENT):
  f=A/'service_owned_workflows_20261006'/n;inputs.extend([f/'native_launch.json',f/'service_execution.json'])
 create(PROOF,{'status':'passed_actual25_own_annual_native_states100_full100_cold_after_missing2023_supplement',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in dict.fromkeys(inputs)},
  'actual_head_year_states':25,'actual_native_cases':100,'actual_cold_cases':100,
  'actual_historical_native_cases':80,'actual_final_calendar_cases':20,'actual_prefit_rejections':20,
  'original_head_year_states':20,'additional_own2023_head_year_states':5,
  'head_year_records':[{'head':h,'year':y,'native_sha256':seen[(h,y)][0],'independent_state_sha256':seen[(h,y)][1]} for h,y in sorted(seen)],
  'original80_proof_immutable_not_overwritten_or_rerun':True,'all5_annual_years_actual_native_replayed':True,
  'new_native_fits':0,'new_official_scores':0,'actual_future_X_read':False,'test_labels_read':False})
 print({'actual_states':25,'native':100,'cold':100},flush=True)

def execute(original,phase=None):
 for p,d in read(META)['input_sha256'].items():assert sha(p)==d,p
 closed(COVERAGE);proof=read(PROOF)
 assert proof['actual_head_year_states']==25 and proof['actual_native_cases']==proof['actual_cold_cases']==100
 for p,d in proof['input_sha256'].items():assert sha(p)==d,p
 import prepare_PureRFFHuber128_round149_sources_v2_20261008 as g
 paths=g.source_paths;extra=[Path(__file__),META,PROOF,*(A/n for n in DRIVERS.values()),
  A/'verify_PureRFFHuber20_year2023_native_supplement_v1_20261009.py',A/'verify_Pure149_all25_annual_native_coverage_v1_20261009.py']
 g.source_paths=lambda:list(dict.fromkeys([*paths(),*extra]))
 import recover_Pure149_actual148_gate_v7_20261009 as prior
 prior.DRIVERS.update(DRIVERS)
 import resume_pending149_verified_gates_v6_20261009 as base
 old_route=base.routed
 base.routed=lambda s,dispatcher=False:old_route(s,dispatcher).replace('complete_hidden_launches_v5_20261009','complete_hidden_launches_v7_20261009')
 import run_dependency_queue_v3_20261006 as io
 old_create=io.create
 def extended(path,value):
  if Path(path).name in ('PureRFFHuber128_actual_controls_index_v1_20261008.json','PureRFFHuber128_round149_source_admission_v1_20261008.json'):
   value={**value,'input_sha256':{**value['input_sha256'],**{str(p):sha(p) for p in extra},**proof['input_sha256']},
    'actual_all5_annual25_native_states_replayed':True,'actual_native_stage_cases':100,'actual_cold_native_stage_cases':100,
    'additional_own2023_native_supplement':str(PROOF),'original80_native_proof_preserved':True}
  return old_create(path,value)
 io.create=extended
 try:prior.execute(original,phase)
 finally:io.create=old_create

def main():
 services=A/'service_owned_workflows_20261006'
 old_service='PureRFFHuber149_complete_chronological_dispatch_v6_20261009'
 old_launch=read(services/old_service/'native_launch.json');assert owned(old_launch)
 assert not (services/'PureRFFHuber128_round149_source_admission_v1_20261008').exists()
 source=A/'verify_PureRFFHuber80_native_historical_calendar_v2_20261008.py'
 s=source.read_text(encoding='utf8')
 start=s.index(' # Actual2024 training features');end=s.index(' assert len(records)==80',start)
 s=s[:start]+s[end:]
 replacements={
  'PureRFFHuber80_native_historical_calendar_v2_20261008':'PureRFFHuber20_year2023_native_supplement_v1_20261009',
  'actual_PureRFFHuber80_native_calendar_location_v2_20261008':'actual_PureRFFHuber20_year2023_native_supplement_location_v1_20261009',
  " closed('AdaptiveJointCrossHuber242_round148_full_registration_v1_20261008')":" closed('AdaptiveJointCrossHuber242_round148_full_registration_v2_20261009')\n closed('PureRFFHuber80_native_historical_calendar_controls_v4_20261009')",
  'for year in (2021,2022,2024,2025):':'for year in (2023,):',
  'for year in (2021,2022,2024):':'for year in (2023,):',
  'frozen_before_actual80_controls':'frozen_before_actual20_year2023_controls',
  "'historical_years':[2021,2022,2024]":"'historical_years':[2023]",
  "'actual_remapped_final_model_calendar_years':[2025,2026]":"'actual_remapped_final_model_calendar_years':[]",
  "'historical_cases':60":"'historical_cases':20","'calendar_cases':20":"'calendar_cases':0",
  "'expected':80":"'expected':20",'assert len(records)==80':'assert len(records)==20',
  'passed_actual60_historical_joint_native_independent_and_OOF_and20_final_multiyear_calendar_controls_with80_cold_prefixes':'passed_actual20_own2023_native_reload_independent_OOF_and20_cold_supplement',
  "'actual_historical_cases':60":"'actual_historical_cases':20","'actual_calendar_cases':20":"'actual_calendar_cases':0",
  "'actual_cold_cases':80":"'actual_cold_cases':20","'actual_prefit_final_model_date_rejections':20":"'actual_prefit_final_model_date_rejections':0"}
 for k,v in replacements.items():assert k in s,k;s=s.replace(k,v)
 supplemental=A/'verify_PureRFFHuber20_year2023_native_supplement_v1_20261009.py'
 compile(s,str(supplemental),'exec')
 with supplemental.open('x',encoding='utf8') as f:f.write(s)
 coverage_driver=A/'verify_Pure149_all25_annual_native_coverage_v1_20261009.py'
 code="from pathlib import Path\nimport sys\nROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]\nfrom bind_Pure149_all5_annual_native_v8_20261009 import verify_coverage\nif __name__=='__main__':verify_coverage()\n"
 with coverage_driver.open('x',encoding='utf8') as f:f.write(code)
 products=[supplemental,coverage_driver]
 for old,new in DRIVERS.items():
  code="from pathlib import Path\nimport sys\nROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]\nfrom bind_Pure149_all5_annual_native_v8_20261009 import execute\n"
  if old.startswith('publish_'):code+="if __name__=='__main__':\n import argparse\n p=argparse.ArgumentParser();p.add_argument('phase',choices=('controls','scores'));execute("+repr(old)+",p.parse_args().phase)\n"
  else:code+="if __name__=='__main__':execute("+repr(old)+")\n"
  compile(code,str(A/new),'exec')
  with (A/new).open('x',encoding='utf8') as f:f.write(code)
  products.append(A/new)
 prospective=A/'PureRFFHuber128_prospective_routes_v2_20261008.json'
 for p,d in read(prospective)['input_sha256'].items():assert sha(p)==d,p
 pins={str(p):sha(p) for p in [Path(__file__),source,*products,prospective,
  A/'recover_Pure149_actual148_gate_v7_20261009.py',A/'Pure149_actual148_gate_recovery_v7_20261009.json']}
 create(META,{'status':'prepared_additional_2023_composite_native20_cold20_and_all25_state_coverage_binding_before149_quality',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'original80_replay_covers20_of25_head_year_states':True,
  'supplement_adds_missing5_states_not_repeated80':True,'all128_cases_and32_frozen_source_hashes_unchanged':True,
  'original_native4_full4_duplicate3_workers_preserved':True,'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
 from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
 specs=[(SUPPLEMENT,supplemental),(COVERAGE,coverage_driver),('PureRFFHuber149_complete_chronological_dispatch_v7_20261009',products[-1])]
 rows={n:start(n,p.name,[],{**pins,str(META):sha(META)}) for n,p in specs}
 create(A/'Pure149_all5_annual_native_hidden_launches_v8_20261009.json',rows)
 from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle,retire_suspended
 parent,worker,idle=suspended_idle(old_launch,'    closed (dispatch_PureRFFHuber149_complete_pipeline_v4_20261008.py:')
 retire_suspended(old_launch,rows[specs[-1][0]])
 create(A/'Pure149_all5_annual_native_old_dispatch6_retired_v8_20261009.json',{
  'status':'retired_only_owned_childfree_idle_dispatch6_after_actual_dispatch7_started',
  'identity':old_launch,'idle':idle,'successor':rows[specs[-1][0]],'scientific_workers_stopped':0})
 print({n:r['owned_worker_pid'] for n,r in rows.items()},flush=True)
if __name__=='__main__':main()
