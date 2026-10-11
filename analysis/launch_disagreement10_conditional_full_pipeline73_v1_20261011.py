from pathlib import Path
import sys,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from start_fast_completed_owned_service_v1_20261011 import start_service
def main():
 assert allowed();closed('actual_rank120_rank60_disagreement10_S_only_gain_decision_v2_20261011')
 decision=read(A/'rank120_rank60_disagreement10_gain_decision_v1_20261011.json')
 if not decision['adopt']:
  create(A/'actual_disagreement10_conditional_full_pipeline73_no_gain_v1_20261011.json',{'status':'passed_actual_S_no_gain_no_Test_inference_required','decision_sha256':sha(A/'rank120_rank60_disagreement10_gain_decision_v1_20261011.json'),'future_X_read':False});return
 assert allowed()
 protocol=A/'rank120_rank60_disagreement10_early73_sources_admission_v2_20261011.json'
 for p,d in read(protocol)['input_sha256'].items():assert sha(p)==d,p
 storage=importlib.import_module('rank120_rank60_disagreement10_early73_storage_v1_20261011')
 from run_protected167_complete_family_v1_20261010 import junction
 for logical,physical in storage.OUTPUTS.items():
  assert not logical.exists() and not physical.exists();physical.mkdir(parents=True);logical.parent.mkdir(parents=True,exist_ok=True);junction(logical,physical)
 jobs=[('actual_rank120_rank60_disagreement10_early73_normalization_v1_20261011','normalize_rank120_rank60_disagreement10_early73_v1_20261011.py'),('actual_rank120_rank60_disagreement10_early73_selected_native14_v1_20261011','qualify_rank120_rank60_disagreement10_early73_selected_native14_v2_20261011.py'),('Rank120Rank60Disagreement10Early73_selected_candidate_preparation_v1_20261011','run_Rank120Rank60Disagreement10Early73_selected_candidate_feature_cache_v2_20261011.py'),('Rank120Rank60Disagreement10Early73_selected_candidate_sealing_v1_20261011','seal_Rank120Rank60Disagreement10Early73_selected_candidate_v2_20261011.py')]
 for name,driver in jobs:
  assert allowed();p=A/driver;result=start_service(name,driver,[],{str(p):sha(p),str(protocol):sha(protocol)});create(A/(name+'_activation.json'),result);closed(name)
 create(A/'actual_disagreement10_conditional_full_pipeline73_sealed_v1_20261011.json',{'status':'passed_complete_candidate_sealed_main_publication_and_delivery_still_required','decision_sha256':sha(A/'rank120_rank60_disagreement10_gain_decision_v1_20261011.json'),'sealed_ready_sha256':sha(A/'Rank120Rank60Disagreement10Early73_selected_release_v1_20261011/selected_candidate_ready_for_registration.json'),'official_TRAIN_internal_score':decision['best']['connected_final_score'],'test_labels_read':False})
if __name__=='__main__':main()
