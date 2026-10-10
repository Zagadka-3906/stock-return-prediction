"""Sequential GPU admission and own six fits, reusing no old annual weights."""
from pathlib import Path
from datetime import datetime
import sys,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service
from scheduled_user_pause_20261007 import write
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
OUT=A/'cross120_recent252_return_own_controls_and_training_queue_v2_20261010'
def main():
    assert allowed();OUT.mkdir(exist_ok=False)
    predecessor=A/'service_owned_workflows_20261006/Cross120170_selected_candidate_sealing_v1_20261010'
    write(OUT/'state.json',{'status':'waiting_actual_Return167_candidate_sealed_to_overlap_new_GPU_training_with_CPU_QA_main','actual_service':'Cross120170_selected_candidate_sealing_v1_20261010','new_quality_scores':0})
    while allowed() and (not (predecessor/'service_execution.json').exists() or owned(read(predecessor/'native_launch.json'))):time.sleep(15)
    if not allowed():return
    assert read(predecessor/'service_execution.json')['status']=='passed',read(predecessor/'service_execution.json')
    proof=A/'Cross120RecentReturn252Huber050_own_bank_controls_source_admission_v1_20261010.json'
    for p,d in read(proof)['input_sha256'].items():assert sha(p)==d,p
    tasks=[('actual_BF16_medium2048_cross120recent252returnhuber050_seed09_restart_control_v1_20261009','verify_neural_BF16_medium2048_cross120recent252returnhuber050_seed09_restart_v1_20261009.py'),('BF16Cross120RecentReturn252Huber050175_independent_small_CPU_v1_20261009','verify_BF16Cross120RecentReturn252Huber050175_independent_small_CPU_v1_20261009.py'),('actual_BF16_medium2048_cross120recent252returnhuber050_seed09_e64_bank6_v1_20261009','train_neural_BF16_medium2048_cross120recent252returnhuber050_seed09_e64_bank6_v1_20261009.py'),('BF16Cross120RecentReturn252Huber050175_independent_full5_GPU_controls_v1_20261009','verify_BF16Cross120RecentReturn252Huber050175_full5_independent_GPU_v1_20261009.py'),('BF16Cross120RecentReturn252Huber050175_actual_native42_calendar_v1_20261009','verify_BF16Cross120RecentReturn252Huber050175_native42_calendar_v1_20261009.py')]
    for name,driver in tasks:
        if not allowed():return
        row=start_service(name,driver,[],{str(p):sha(p) for p in [A/driver,proof,A/'neural_BF16_medium2048_cross120recent252returnhuber050_seed09_e64_native_v1_20261009.py']})
        create(OUT/(name+'_launch.json'),row)
        write(OUT/'state.json',{'status':'actual_cross120_recent252_return_own_training_or_admission_running','actual_service':name,'recipe':'cross120recent252returnhuber050','at_local':datetime.now().isoformat(),'new_quality_scores':0})
        folder=A/'service_owned_workflows_20261006'/name
        while owned(row):
            if not allowed():return
            time.sleep(15)
        assert read(folder/'service_execution.json')['status']=='passed',read(folder/'service_execution.json')
    write(OUT/'state.json',{'status':'own_recent252_return_six_fits_full5_native42_qualified_official_comparison_pending','at_local':datetime.now().isoformat(),'new_quality_scores':0})
    print('PASS own recent252_return GPU controls and six fits; official scoring still required',flush=True)
if __name__=='__main__':main()
