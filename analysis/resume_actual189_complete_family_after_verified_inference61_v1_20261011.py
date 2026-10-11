from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from start_fast_completed_owned_service_v1_20261011 import start_service
def main():
 assert allowed();closed('actual189_completed_inference_missing_evidence_sealing_resume61_v1_20261011')
 ready=read(A/'MixedObjectiveWindow189_selected_release_v1_20261010/selected_candidate_ready_for_registration.json');assert ready['sealed_candidate_complete']
 driver='run_MixedObjectiveWindow189_full_registration_v3_20261011.py';name='MixedObjectiveWindow189_round189_full_registration_v1_20261010'
 from prepare_MixedObjectiveWindow189_complete149_pipeline_v3_20261011 import source_paths
 pins={str(p):sha(p) for p in source_paths()};assert allowed();start_service(name,driver,[],pins);closed(name)
 receipt=read(A/'github_validation_sync_main_20261005/round189_receipt.json');assert receipt['status']=='pushed_and_remote_head_verified' and receipt['scored_records']==149
 assert read(A/'optimization_20261003_r189/full_registration_execution.json')['status']=='passed'
 from maintain_best_fully_qualified_submission_delivery_v3_20261010 import update
 assert allowed();update()
 create(A/'actual189_verified_family_resume61_complete_v1_20261011.json',{'status':'passed_actual149_full_candidate_QA100_main_and_delivery_no_inference_rerun','receipt':receipt,'new_quality_scores':0,'new_native_fits':0,'test_labels_read':False})
if __name__=='__main__':main()
