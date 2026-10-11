"""Wait for actual whole-scheme qualification, then preserve the best verified E submission."""
from pathlib import Path
from datetime import datetime
import sys,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,owned,create
from scheduled_user_pause_20261007 import write
from prepare_Return_protected_pilot67_and_selected_native14_v1_20261010 import allowed
OUT=A/'Return167_qualification_and_delivery_queue_v1_20261010'
def main():
    assert allowed();OUT.mkdir(exist_ok=False)
    name='ReturnProtected167_complete67_family_admitted_v2_20261010';folder=A/'service_owned_workflows_20261006'/name
    write(OUT/'state.json',{'status':'waiting_own_forward20_GPU_admission_then_Return167_selected_native14_full_candidate_QA78_main','actual_service':name,'at_local':datetime.now().isoformat(),'submission_qualified':False})
    while allowed():
        if (folder/'service_execution.json').exists() and not owned(read(folder/'native_launch.json')):
            assert read(folder/'service_execution.json')['status']=='passed',read(folder/'service_execution.json');break
        time.sleep(15)
    if not allowed():return
    final=read(A/'optimization_20261003_r167/full_registration_execution.json');receipt=read(A/'github_validation_sync_main_20261005/round167_receipt.json')
    assert final['status']=='passed' and final['existing_official_scores_registered']==67 and receipt['status']=='pushed_and_remote_head_verified' and receipt['scored_records']==67
    import maintain_best_fully_qualified_submission_delivery_v3_20261010 as delivery
    delivery.update()
    create(OUT/'verification.json',{'status':'passed_actual_Return167_full_native_candidate_QA78_main_and_best_delivery_update','receipt':receipt,'current_best_delivery':read(A/'latest_verified_submission_delivery_v2_20261008.json'),'new_quality_scores_by_this_queue':0,'competition_upload_performed':False,'optimization_continues':True})
    write(OUT/'state.json',{'status':'passed_actual_Return167_and_best_verified_submission_updated','receipt':receipt,'at_local':datetime.now().isoformat()})
if __name__=='__main__':main()
