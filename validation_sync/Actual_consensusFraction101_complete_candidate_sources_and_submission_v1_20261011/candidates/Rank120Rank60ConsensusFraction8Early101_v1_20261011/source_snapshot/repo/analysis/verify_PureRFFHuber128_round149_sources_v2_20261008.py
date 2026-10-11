"""Admit joint185 only after actual80 native,181 full,543 cold and32 prospective controls."""
from pathlib import Path
import sys,time,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def closed(name):
 f=A/'service_owned_workflows_20261006'/name
 while not (f/'service_execution.json').exists():time.sleep(10)
 while owned(read(f/'native_launch.json')):time.sleep(1)
 assert read(f/'service_execution.json')['status']=='passed',name
def main():
 for name in ('Pure149_prior_complete_forecast_duplicate_audit_v1_20261008','PureRFFHuber149_complete_prospective_controls_v2_20261008',
  'PureRFFHuber124_actual_synthetic_controls_v2_20261008','PureRFFHuber80_native_historical_calendar_controls_v2_20261008',
  'PureRFFHuber124_actual_full_historical_controls_v2_20261008','AdaptiveJointCrossHuber242_round148_full_registration_v1_20261008',
  'actual_joint147_preparation_and_storage_main_publication_v31_20261008','all_forecast_percentiles_full_scoring_benchmark',
  'cached_official_spearman_full12_benchmark','exact_native_JSON_archive_runtime_full_preflight'):closed(name)
 import prepare_PureRFFHuber128_round149_sources_v2_20261008 as generator
 prospective=A/'PureRFFHuber128_prospective_routes_v2_20261008.json';p=read(prospective)
 assert p['status']=='passed_actual32_prospective149_sources_ordered_joint_graphs_baselines_status_paths_SHA_unions_ties_and_cross_volume_bytes'
 for f,d in p['input_sha256'].items():assert sha(f)==d,f
 pointers=['actual_PureRFFHuber25_existing_native_location_v1_20261008.json','actual_PureRFFHuber124_parent134_location_v2_20261008.json',
  'actual_PureRFFHuber80_native_calendar_location_v2_20261008.json','actual_PureRFFHuber124_synthetic_location_v2_20261008.json']
 metadata=[];proofs=[]
 for n in pointers:
  f=A/n;target=Path(read(f)['output'])/'verification.json';assert sha(target)==read(f)['verification_sha256'];metadata.extend([f,target]);proofs.append(read(target))
 bank,current,native,synthetic=proofs
 assert bank['actual_saved_model_count']==25 and bank['actual_full_OOF_heads']==5 and not bank['new_native_replay_claimed']
 assert current['actual_stage_base_round']==134 and current['actual_full_cases_including_identity']==124 and current['actual_cold_cases_including_identity']==372
 assert {r['actual_qualified_round'] for r in current['known_qualified_numeric_identities']}=={134}
 assert native['actual_historical_cases']==60 and native['actual_calendar_cases']==20 and native['actual_cold_cases']==80 and native['actual_prefit_final_model_date_rejections']==20
 assert synthetic['actual_cases']==124 and synthetic['actual_cold_cases']==372 and synthetic['actual_double_stage_order_pairs']==54
 all_proof_pins={}
 for proof in proofs:
  for f,d in proof['input_sha256'].items():
   assert sha(f)==d,f
   if f in all_proof_pins:assert all_proof_pins[f]==d,f
   all_proof_pins[f]=d
 planpath=A/'PureRFFHuber128_round149_plan_v1_20261008.json';plan=read(planpath)
 assert len(plan['heads'])==5 and len(bank['records'])==25
 for r in plan['heads'].values():
  metadata.append(Path(r['folder'])/'oof_verification.json')
  for path in r['infos'].values():metadata.append(Path(path))
 for n in [134,136,*plan['anchor_rounds']]:
  f=A/f'optimization_20261003_r{n}';candidate=ROOT/f'candidates/optimization_20261003_r{n}';receipt=A/f'github_validation_sync_main_20261005/round{n}_receipt.json'
  assert read(f/'full_registration_execution.json')['status']=='passed' and read(receipt)['status']=='pushed_and_remote_head_verified'
  metadata.extend([f/'full_registration_execution.json',f/'calibrated_csv_official.json',receipt,candidate/'verification.json',candidate/'manifest.json'])
 metadata=list(dict.fromkeys(metadata));index=A/'PureRFFHuber128_actual_controls_index_v1_20261008.json'
 create(index,{'status':'passed_actual25_states124full372cold80native_historical_controls',
  'input_sha256':{str(f):sha(f) for f in metadata},'original_external_metadata':{str(f):read(f) for f in metadata if not f.is_relative_to(ROOT)},
  'existing_bank35_rehashed_records_not_new_native_replays':bank['records'],'fixed_scientific_stage_base_round':134,
  'no_large_weights_copied_into_Git':True,'actual80_new_native_controls_completed':True,'new_quality_scores':0,'test_labels_read':False})
 outputs={str(n):{name:hashlib.sha256(s.encode()).hexdigest() for name,s in generator.generate(n).items()} for n in plan['anchor_rounds']}
 assert outputs==p['generated_source_sha256']
 sources=[Path(__file__),Path(generator.__file__),prospective,planpath,index,*metadata,A/'Pure149_complete_receiver_preparation_v1_20261008.json',A/'PureRFFHuber149_D_scoring_scope_v1_20261008.json']
 pins={**all_proof_pins,**p['input_sha256'],**{str(f):sha(f) for f in dict.fromkeys(sources)}}
 create(A/'PureRFFHuber128_round149_source_admission_v1_20261008.json',{'status':'passed_actual25_states124full372cold80native_and32_prospective149_sources',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'generated_source_sha256':outputs,'fixed_scientific_stage_base_round':134,
  'actual_relevant_saved_native_heads':25,'actual_full_OOF_heads':7,'actual_new_native_fits':0,'prospective_sources':32,
  'quality_scoring_admitted_cases':128,'new_quality_scores_by_admission':0,'test_labels_read':False})
 print('Actual35 saved states,80/80 native,181/543 full/cold and32 source routes admit185 original official scores.',flush=True)
if __name__=='__main__':main()
