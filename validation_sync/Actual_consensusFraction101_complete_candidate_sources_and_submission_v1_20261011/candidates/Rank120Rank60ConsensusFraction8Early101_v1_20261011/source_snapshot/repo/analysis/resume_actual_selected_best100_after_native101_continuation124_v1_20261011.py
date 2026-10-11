from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from start_fast_completed_owned_service_v1_20261011 import start_service
assert allowed()
chosen=A/'actual_final_fraction100_vs_weight108_S_only_best_pipeline110_decision_v1_20261011.json';selection=read(chosen);decision=A/'rank120_rank60_consensusFraction8_gain_decision101_v1_20261011.json';selected=read(decision)
assert selection['choice']==0 and selected['adopt'] and selected['best']['connected_final_score']==max(selection['scores'])
protocol=A/'rank120_rank60_consensusFraction8_early101_sources_admission_v2_20261011.json'
for p,d in read(protocol)['input_sha256'].items():assert sha(p)==d,p
for p,d in selected['input_sha256'].items():assert sha(p)==d,p
closed('actual_rank120_rank60_consensusFraction8_early101_normalization_v1_20261011')
create(A/'actual_best100_original_normalization_and_native101_dispatch_continuation124_admission_v1_20261011.json',{'status':'actual_old110_had_already_dispatched_normalization101_and_native101_before_administrative_retirement_only_verified_existing_jobs_reused_no_rerun_existing_outputs','best_S':selected['best']['connected_final_score'],'input_sha256':{str(p):sha(p) for p in [Path(__file__),chosen,decision,protocol,A/'actual_idle_best_only110_replaced_for_TRAIN_native_prequalification123_v1_20261011.json']},'original_existing_namespace_launch_refusal_preserved':True,'native_scientific_workers_not_interrupted':True,'test_labels_read':False})
closed('actual_rank120_rank60_consensusFraction8_early101_selected_native14_v1_20261011')
import rank120_rank60_consensusFraction8_early101_storage_v1_20261011 as storage
for logical,physical in storage.OUTPUTS.items():assert logical.is_dir() and logical.resolve()==physical.resolve() and not any(logical.iterdir()),logical
stages=[('Rank120Rank60ConsensusFraction8Early101_selected_candidate_preparation_v1_20261011','run_fraction101_same_bytes_TRAIN_link103_candidate_wrapper_v1_20261011.py'),('Rank120Rank60ConsensusFraction8Early101_selected_candidate_sealing_v1_20261011','seal_Rank120Rank60ConsensusFraction8Early101_selected_candidate_v2_20261011.py'),('actual_consensusFraction101_complete_candidate_main_v1_20261011','publish_actual_consensusFraction101_complete_candidate_main_v1_20261011.py'),('actual_verified_consensusFraction101_alternate_submission_delivery_v1_20261011','prepare_verified_consensusFraction101_alternate_submission_delivery_v1_20261011.py')]
for name,driver in stages:
 assert allowed();p=A/driver;pins={str(p):sha(p),str(protocol):sha(protocol),str(Path(__file__)):sha(__file__),str(decision):sha(decision)}
 if 'preparation' in name:
  original=A/'run_Rank120Rank60ConsensusFraction8Early101_selected_candidate_feature_cache_v2_20261011.py';pins[str(original)]=sha(original)
 r=start_service(name,driver,[],pins);create(A/(name+'_actual124_activation.json'),r);closed(name)
closed('actual_completed_consensusFraction8_actual8_early114_main_v1_20261011')
pointer=A/'alternate_verified_consensusFraction101_submission_delivery_v1_20261011.json';actual=read(pointer);assert actual['all_full_native_independent_reload_csv_and_cold80_checks_passed'] and actual['official_TRAIN_internal_score']==selected['best']['connected_final_score']
create(A/'actual_best100_full_candidate_continuation124_complete_v1_20261011.json',{'status':'passed_actual8_TRAIN_records_early114_main_native14_and_full37_native_independent_reload_CSV_cold80_main_and_E_delivery_after_existing_native101_only_continuation','delivery':actual,'input_sha256':{str(p):sha(p) for p in [Path(__file__),protocol,decision,pointer]},'original191_cap_full_connected_board_registration_still_separate':True,'test_labels_read':False,'global_exhaustion_proven':False})
