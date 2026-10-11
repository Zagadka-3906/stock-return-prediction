from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from start_fast_completed_owned_service_v1_20261011 import start_service
def main():
 assert allowed();closed('actual_rank120_rank60_disagreement10_S_only_gain_decision_v2_20261011')
 decision=read(A/'rank120_rank60_disagreement10_gain_decision_v1_20261011.json')
 if not decision['adopt']:
  create(A/'actual_disagreement73_main_delivery_not_needed_v1_20261011.json',{'status':'passed_actual_no_S_gain_no_new_delivery_claimed','decision_sha256':sha(A/'rank120_rank60_disagreement10_gain_decision_v1_20261011.json')});return
 closed('actual_disagreement10_conditional_full_pipeline73_v1_20261011')
 for name,driver in [('actual_disagreement73_complete_candidate_main_v1_20261011','publish_actual_disagreement73_complete_candidate_main_v1_20261011.py'),('actual_verified_disagreement73_alternate_submission_delivery_v1_20261011','prepare_verified_disagreement73_alternate_submission_delivery_v1_20261011.py')]:
  assert allowed();p=A/driver;r=start_service(name,driver,[],{str(p):sha(p)});create(A/(name+'_activation.json'),r);closed(name)
 actual=read(A/'alternate_verified_disagreement73_submission_delivery_v1_20261011.json')
 assert actual['all_full_native_independent_reload_csv_and_cold80_checks_passed'] and actual['official_TRAIN_internal_score']==decision['best']['connected_final_score']
 create(A/'rank120_rank60_disagreement10_selected_full_candidate_complete_v1_20261011.json',actual)
if __name__=='__main__':main()
