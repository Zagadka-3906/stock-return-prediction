from pathlib import Path
import sys,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
def main():
 assert allowed();closed('recovery70_MixedRefined191_round191_full_registration_v1_20261011')
 folder=A/'optimization_20261003_r191';r=read(A/'github_validation_sync_main_20261005/round191_receipt.json');assert r['status']=='pushed_and_remote_head_verified' and r['scored_records']==27 and r['connected_records']==17753 and r['actual_full_QA_version']==102
 assert read(folder/'full_registration_execution.json')['status']=='passed'
 for name in ['recovery58_MixedRefined191_selected_candidate_preparation_v1_20261010','recovery58_MixedRefined191_selected_candidate_sealing_v1_20261010']:closed(name)
 from maintain_best_fully_qualified_submission_delivery_v3_20261010 import update
 update()
 out=A/'MixedRefined191_complete_family_v1_20261010';assert out.is_dir() and not (out/'passed.json').exists()
 create(out/'passed.json',{'status':'passed_actual27_selected_stage_full_native_candidate_or_exact_anchor_QA102_main_and_delivery','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'receipt':r,'actual_scored_records':27,'new_quality_scores_by_registration':0,'test_labels_read':False,'original_failed_parent_closure_and_metadata_attempts_retained':True,'actual_registration_service':'recovery70_MixedRefined191_round191_full_registration_v1_20261011'})
 print('Actual191 original QA102/main/candidate preparation/sealing and delivery all verified; no scientific rerun',flush=True)
if __name__=='__main__':main()
