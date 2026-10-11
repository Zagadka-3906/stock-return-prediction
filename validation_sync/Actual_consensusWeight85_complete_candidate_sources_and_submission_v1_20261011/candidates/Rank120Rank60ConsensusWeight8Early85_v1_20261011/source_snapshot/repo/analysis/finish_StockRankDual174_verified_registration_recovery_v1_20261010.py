from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from route_verified_Dual25_recovery_dependencies_v2_20261010 import installed
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed();closed=installed()
    from handoff_ready_goss_full_execution_20261006 import start_service
    name='StockRankDual174_full_registration_recovery_v1_20261010';p=A/'run_StockRankDual174_full_registration_v3_20261010_after_registry_recovery_v2.py'
    row=start_service(name,p.name,[],{str(p):sha(p)});create(A/(name+'_activation.json'),row);closed(name)
    receipt=read(A/'github_validation_sync_main_20261005/round174_receipt.json');assert receipt['status']=='pushed_and_remote_head_verified' and receipt['scored_records']==44
    assert read(A/'optimization_20261003_r174/full_registration_execution.json')['status']=='passed'
    assert allowed()
    from maintain_best_fully_qualified_submission_delivery_v3_20261010 import update
    update()
    create(A/'StockRankDual174_registry_recovery_complete_v1_20261010.json',{'status':'passed_actual44_QA85_main_and_delivery_after_exact_partial_registry_preservation','receipt':receipt,'new_fits':0,'new_quality_scores':0,'new_inference':False})
if __name__=='__main__':main()
