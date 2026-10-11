"""Prepare actual all5-year native controls and whole training controls on qualified148."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
 outputs=[];sources=[]
 original=A/'verify_HuberSparse72_native_historical_calendar_v1_20261008.py';sources.append(original)
 s=original.read_text(encoding='utf8')
 changes={
  'HuberSparse72_native_historical_calendar_v1_20261008':'SparseAfter14860_native_historical_calendar_v1_20261009',
  'HuberSparse_complete_parent_CDF_v1_20261008':'SparseAfter148_complete_parent_CDF_v1_20261009',
  'HuberSparse_complete_parent_native_stage_v1_20261008':'SparseAfter148_complete_parent_native_stage_v1_20261009',
  'HuberSparse59_round150_proposal_v1_20261008':'SparseAfter14829_round152_proposal_v1_20261009',
  'HuberSparse59_synthetic55_and_state20_metadata_v1_20261008':'SparseAfter14829_synthetic25_and_state10_metadata_v1_20261009',
  "closed('JointCrossHuberOrder185_controls_main_publication_v1_20261008')":"closed('AdaptiveJointCrossHuber242_round148_full_registration_v2_20261009')",
  "assert proof['actual_cases']==55 and proof['actual_cold_cases']==165 and proof['actual_saved_state_metadata_count']==20":"assert proof['actual_cases']==25 and proof['actual_cold_cases']==75 and len(proof['actual_existing_state_metadata'])==10",
  "assert not proof['new_native_replays_claimed'] and len(plan['heads'])==4":"assert not proof['new_native_fits'] and len(plan['heads'])==2",
  'optimization_20261003_r134/selected_validation.npy':'optimization_20261003_r148/selected_validation.npy',
  "cases=[{'group':g,'share':s,'amplitude':.0025} for g in range(6) for s in (.25,.5,.75)]":"cases=[{'group':g,'share':.5,'amplitude':a} for g in range(6) for a in (.0005,.00325)]",
  'assert len(cases)==18':'assert len(cases)==12','frozen_before_actual72_native_controls':'frozen_before_actual60_native_controls',
  "'historical_years':[2021,2022,2024]":"'historical_years':[2021,2022,2023,2024]",
  "'expected_historical_cases':54":"'expected_historical_cases':48","'expected_calendar_cases':18":"'expected_calendar_cases':12",
  "'expected_cold_cases':72":"'expected_cold_cases':60","'expected_prefit_date_rejections':18":"'expected_prefit_date_rejections':12",
  "'original_complete_parent_round':134":"'original_complete_parent_round':148",
  'for year in (2021,2022,2024,2025):':'for year in (2021,2022,2023,2024,2025):',
  "'expected':72":"'expected':60",'assert len(records)==72':'assert len(records)==60',
  'passed_actual54_HuberSparse_historical_native_and18_final_calendar_with72_cold_and18_prefit_rejections':'passed_actual48_SparseAfter148_all5_annual_native_and12_final_calendar_with60_cold_and12_prefit_rejections',
  "'actual_historical_cases':54":"'actual_historical_cases':48","'actual_calendar_cases':18":"'actual_calendar_cases':12",
  "'actual_cold_cases':72":"'actual_cold_cases':60","'actual_prefit_final_model_date_rejections':18":"'actual_prefit_final_model_date_rejections':12",
  "'actual_existing_annual_states':20":"'actual_existing_annual_states':10",
  'actual_HuberSparse72_native_calendar_location_v1_20261008':'actual_SparseAfter14860_native_calendar_location_v1_20261009'}
 for k,v in changes.items():assert k in s,k;s=s.replace(k,v)
 native=A/'verify_SparseAfter14860_native_historical_calendar_v1_20261009.py';compile(s,str(native),'exec')
 with native.open('x',encoding='utf8') as f:f.write(s)
 outputs.append(native)
 original=A/'verify_HuberSparse55_full_historical_controls_v1_20261008.py';sources.append(original);s=original.read_text(encoding='utf8')
 changes={
  'HuberSparse55_parent134_historical_v1_20261008':'SparseAfter14825_parent148_historical_v1_20261009',
  'HuberSparse72_native_historical_calendar_controls_v1_20261008':'SparseAfter14860_native_historical_calendar_controls_v1_20261009',
  "closed('JointCrossHuberOrder185_controls_main_publication_v1_20261008')":"closed('AdaptiveJointCrossHuber242_round148_full_registration_v2_20261009')",
  'HuberSparse_complete_parent_CDF_v1_20261008':'SparseAfter148_complete_parent_CDF_v1_20261009',
  'HuberSparse59_round150_proposal_v1_20261008':'SparseAfter14829_round152_proposal_v1_20261009',
  'actual_HuberSparse72_native_calendar_location_v1_20261008':'actual_SparseAfter14860_native_calendar_location_v1_20261009',
  "native['actual_historical_cases']==54 and native['actual_calendar_cases']==18":"native['actual_historical_cases']==48 and native['actual_calendar_cases']==12",
  "native['actual_cold_cases']==72 and native['actual_prefit_final_model_date_rejections']==18":"native['actual_cold_cases']==60 and native['actual_prefit_final_model_date_rejections']==12",
  "len(plan['new_cases'])==55 and plan['fixed_scientific_stage_base_round']==134":"len(plan['new_cases'])==25 and plan['fixed_scientific_stage_base_round']==148",
  'optimization_20261003_r134':'optimization_20261003_r148','round134_receipt.json':'round148_receipt.json',
  'frozen_before_actual55_full_controls':'frozen_before_actual25_full_controls',"'actual_stage_base_round':134":"'actual_stage_base_round':148",
  "'expected_full_cases':55":"'expected_full_cases':25","'expected_cold_cases':165":"'expected_cold_cases':75",
  'for g in range(6) for s in (.25,.5,.75)':'for g in range(6) for s in (.5,)',
  "'qualified_anchor_numeric_identity_round':134":"'qualified_anchor_numeric_identity_round':148","'expected':55":"'expected':25",
  'assert len(records)==55 and sum(len(row[\'cold_controls\']) for row in records)==165':'assert len(records)==25 and sum(len(row[\'cold_controls\']) for row in records)==75',
  'passed_actual55_HuberSparse_full_training_CDF_and165_cold_controls_with_exact134_identity':'passed_actual25_SparseAfter148_full_training_CDF_and75_cold_controls_with_exact148_identity',
  "'actual_full_cases_including_identity':55":"'actual_full_cases_including_identity':25","'actual_cold_cases_including_identity':165":"'actual_cold_cases_including_identity':75",
  'existing20_saved_states_reused_not_new_fits':'existing10_saved_states_reused_not_new_fits',
  'all59_quality_receivers_duplicate_audit_freeze_inference_full_board_and_main_still_required':'all29_quality_receivers_duplicate_audit_freeze_inference_full_board_and_main_still_required',
  'actual_HuberSparse55_parent134_location_v1_20261008':'actual_SparseAfter14825_parent148_location_v1_20261009'}
 for k,v in changes.items():assert k in s,k;s=s.replace(k,v)
 full=A/'verify_SparseAfter14825_full_historical_controls_v1_20261009.py';compile(s,str(full),'exec')
 with full.open('x',encoding='utf8') as f:f.write(s)
 outputs.append(full)
 proposal=A/'SparseAfter14829_round152_proposal_v1_20261009.json'
 proof=A/'SparseAfter14829_synthetic25_and_state10_metadata_v1_20261009.json'
 inputs=[Path(__file__),*sources,*outputs,proposal,proof,A/'SparseAfter148_complete_parent_CDF_v1_20261009.py',A/'SparseAfter148_complete_parent_native_stage_v1_20261009.py']
 pins={str(p):sha(p) for p in inputs};meta=A/'SparseAfter148152_historical_receiver_preparation_v1_20261009.json'
 create(meta,{'status':'prepared_all5_annual10_native_states60_controls_and25_full75_prefix_receivers_on_actual148',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'stage_base_round':148,
  'historical_years':[2021,2022,2023,2024],'final_model_year':2025,'new_native_fits':0,'new_official_scores':0,'test_labels_read':False})
 from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
 specs=[('SparseAfter14860_native_historical_calendar_controls_v1_20261009',native),('SparseAfter14825_full_historical_controls_v1_20261009',full)]
 rows={n:start(n,p.name,[],{**pins,str(meta):sha(meta)}) for n,p in specs}
 create(A/'SparseAfter148152_historical_hidden_launches_v1_20261009.json',rows)
 print({n:r['owned_worker_pid'] for n,r in rows.items()},flush=True)
if __name__=='__main__':main()
