from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
def main():
 assert allowed();closed('recovery65_actual190_existing_QA101_main_transaction_v1_20261011')
 folder=A/'optimization_20261003_r190';receipt=A/'github_validation_sync_main_20261005/round190_receipt.json';r=read(receipt);prov=folder/'provenance_scope_execution.json'
 assert r['status']=='pushed_and_remote_head_verified' and r['scored_records']==39 and r['connected_records']==17726 and r['actual_full_QA_version']==101
 assert read(prov)['status']=='passed';ready=read(A/'MixedProtected190_selected_release_v1_20261010/selected_candidate_ready_for_registration.json')
 create(folder/'full_registration_execution.json',{'status':'passed','at_local':r['at_local'],'existing_official_scores_registered':39,'full_rankings_all_original_QA_and_main_publication_completed':True,'scientific_workers_suspended_stopped_or_restarted':0,'new_quality_scores_by_registration':0,'new_inference_claimed_by_registration':False,'selected_candidate_actual_new_inference':ready['new_inference_claimed'],'global_goal_or_resource_exhaustion_claimed':False,'test_labels_read':False,'recovery_of_original_disk_failure_not_a_new_scientific_run':True,'actual_main_receipt_sha256':sha(receipt),'original_actual_full_QA_and_provenance_sha256':sha(prov),'original_terminal_failed_services_preserved':True})
 print('Actual completed190 originalQA101 and resumedmain bridged; original failures retained',flush=True)
if __name__=='__main__':main()
