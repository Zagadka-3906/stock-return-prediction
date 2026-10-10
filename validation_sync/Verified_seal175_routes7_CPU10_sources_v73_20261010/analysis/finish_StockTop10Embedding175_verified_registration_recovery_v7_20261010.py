from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from handoff_ready_goss_full_execution_20261006 import start_service
def main():
    from route_verified_Dual25_recovery_dependencies_v7_20261010 import installed
    installed()
    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import closed
    assert allowed();closed('StockTop10Embedding175_selected_candidate_sealing_v1_20261010')
    driver='run_StockTop10Embedding175_full_registration_v3_20261010_after_verified_seal_routes_v7.py'
    name='StockTop10Embedding175_verified_full_registration_recovery_v7_20261010'
    row=start_service(name,driver,[],{str(A/driver):sha(A/driver)});create(A/(name+'_activation.json'),row);closed(name)
    receipt=read(A/'github_validation_sync_main_20261005/round175_receipt.json');assert receipt['status']=='pushed_and_remote_head_verified' and receipt['scored_records']==47
    assert read(A/'optimization_20261003_r175/full_registration_execution.json')['status']=='passed'
    from maintain_best_fully_qualified_submission_delivery_v3_20261010 import update
    update()
    create(A/'StockTop10Embedding175_verified_completion_recovery_v7_20261010.json',{'status':'passed_verified_inference_and_seal_preserved_full47_QA86_main_delivery','receipt':receipt,'new_inference':0,'new_fits':0,'new_scores':0})
if __name__=='__main__':main()
