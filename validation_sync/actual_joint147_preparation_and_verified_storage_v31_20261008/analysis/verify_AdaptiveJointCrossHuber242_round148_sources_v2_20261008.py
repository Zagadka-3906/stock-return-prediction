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
 for name in ('AdaptiveJointCrossHuber148_complete_prospective_controls_v2_20261008',
  'AdaptiveJointCrossHuber238_actual_synthetic_controls_v2_20261008','AdaptiveJointCrossHuber80_native_historical_calendar_controls_v2_20261008',
  'AdaptiveJointCrossHuber238_actual_full_historical_controls_v2_20261008','JointCrossHuberOrder185_round147_full_registration_v1_20261008',
  'actual_joint147_preparation_and_storage_main_publication_v31_20261008','all_forecast_percentiles_full_scoring_benchmark',
  'cached_official_spearman_full12_benchmark','exact_native_JSON_archive_runtime_full_preflight'):closed(name)
 import prepare_AdaptiveJointCrossHuber242_round148_sources_v2_20261008 as generator
 prospective=A/'AdaptiveJointCrossHuber242_prospective_routes_v2_20261008.json';p=read(prospective)
 assert p['status']=='passed_actual32_prospective148_sources_ordered_joint_graphs_baselines_status_paths_SHA_unions_ties_and_cross_volume_bytes'
 for f,d in p['input_sha256'].items():assert sha(f)==d,f
 pointers=['actual_JointCrossHuber35_existing_native_location_v1_20261008.json','actual_AdaptiveJointCrossHuber238_parent134_location_v2_20261008.json',
  'actual_AdaptiveJointCrossHuber80_native_calendar_location_v2_20261008.json','actual_AdaptiveJointCrossHuber238_synthetic_location_v2_20261008.json']
 metadata=[];proofs=[]
 for n in pointers:
  f=A/n;target=Path(read(f)['output'])/'verification.json';assert sha(target)==read(f)['verification_sha256'];metadata.extend([f,target]);proofs.append(read(target))
 bank,current,native,synthetic=proofs
 assert bank['actual_saved_model_count']==35 and bank['actual_full_OOF_heads']==7 and not bank['new_native_replay_claimed']
 assert current['actual_stage_base_round']==134 and current['actual_full_cases_including_identity']==238 and current['actual_cold_cases_including_identity']==714
 assert {r['actual_qualified_round'] for r in current['known_qualified_numeric_identities']}=={134,136,139,145}
 assert native['actual_historical_cases']==60 and native['actual_calendar_cases']==20 and native['actual_cold_cases']==80 and native['actual_prefit_final_model_date_rejections']==20
 assert synthetic['actual_cases']==238 and synthetic['actual_cold_cases']==714 and synthetic['actual_double_stage_order_pairs']==108
 all_proof_pins={}
 for proof in proofs:
  for f,d in proof['input_sha256'].items():
   assert sha(f)==d,f
   if f in all_proof_pins:assert all_proof_pins[f]==d,f
   all_proof_pins[f]=d
 planpath=A/'AdaptiveJointCrossHuber242_round148_plan_v1_20261008.json';plan=read(planpath)
 assert len(plan['heads'])==7 and len(bank['records'])==35
 for r in plan['heads'].values():
  metadata.append(Path(r['folder'])/'oof_verification.json')
  for path in r['infos'].values():metadata.append(Path(path))
 for n in [134,136,*plan['anchor_rounds']]:
  f=A/f'optimization_20261003_r{n}';candidate=ROOT/f'candidates/optimization_20261003_r{n}';receipt=A/f'github_validation_sync_main_20261005/round{n}_receipt.json'
  assert read(f/'full_registration_execution.json')['status']=='passed' and read(receipt)['status']=='pushed_and_remote_head_verified'
  metadata.extend([f/'full_registration_execution.json',f/'calibrated_csv_official.json',receipt,candidate/'verification.json',candidate/'manifest.json'])
 metadata=list(dict.fromkeys(metadata));index=A/'AdaptiveJointCrossHuber242_actual_controls_index_v1_20261008.json'
 create(index,{'status':'passed_actual35_states238full714cold80native_historical_controls',
  'input_sha256':{str(f):sha(f) for f in metadata},'original_external_metadata':{str(f):read(f) for f in metadata if not f.is_relative_to(ROOT)},
  'existing_bank35_rehashed_records_not_new_native_replays':bank['records'],'fixed_scientific_stage_base_round':134,
  'no_large_weights_copied_into_Git':True,'actual80_new_native_controls_completed':True,'new_quality_scores':0,'test_labels_read':False})
 outputs={str(n):{name:hashlib.sha256(s.encode()).hexdigest() for name,s in generator.generate(n).items()} for n in plan['anchor_rounds']}
 assert outputs==p['generated_source_sha256']
 sources=[Path(__file__),Path(generator.__file__),prospective,planpath,index,*metadata,A/'AdaptiveJointCrossHuber148_complete_receiver_preparation_v1_20261008.json',A/'AdaptiveJointCrossHuber148_D_scoring_scope_v1_20261008.json']
 pins={**all_proof_pins,**p['input_sha256'],**{str(f):sha(f) for f in dict.fromkeys(sources)}}
 create(A/'AdaptiveJointCrossHuber242_round148_source_admission_v1_20261008.json',{'status':'passed_actual35_states238full714cold80native_and32_prospective148_sources',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'generated_source_sha256':outputs,'fixed_scientific_stage_base_round':134,
  'actual_relevant_saved_native_heads':35,'actual_full_OOF_heads':7,'actual_new_native_fits':0,'prospective_sources':32,
  'quality_scoring_admitted_cases':242,'new_quality_scores_by_admission':0,'test_labels_read':False})
 print('Actual35 saved states,80/80 native,181/543 full/cold and32 source routes admit185 original official scores.',flush=True)
if __name__=='__main__':main()
