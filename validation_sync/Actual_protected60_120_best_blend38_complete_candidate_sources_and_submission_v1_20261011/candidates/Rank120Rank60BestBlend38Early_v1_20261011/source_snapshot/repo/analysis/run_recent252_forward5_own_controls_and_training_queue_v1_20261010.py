"""Sequential GPU admission and own six fits, reusing no old annual weights."""
from pathlib import Path
from datetime import datetime
import sys,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service
from scheduled_user_pause_20261007 import write
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
OUT=A/'recent252_forward5_own_controls_and_training_queue_v1_20261010'
def main():
    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import closed
    assert allowed()
    closed('actual_recent252_forward20_own_controls_and_training_queue_v1_20261010')
    assert allowed();OUT.mkdir(exist_ok=False)
    proof=A/'Recent252Forward5Huber050_own_bank_controls_source_admission_v1_20261010.json'
    for p,d in read(proof)['input_sha256'].items():assert sha(p)==d,p
    tasks=[('actual_BF16_medium2048_recent252forward5huber050_seed09_restart_control_v1_20261009','verify_neural_BF16_medium2048_recent252forward5huber050_seed09_restart_v1_20261009.py'),('BF16Recent252Forward5Huber050171_independent_small_CPU_v1_20261009','verify_BF16Recent252Forward5Huber050171_independent_small_CPU_v1_20261009.py'),('actual_BF16_medium2048_recent252forward5huber050_seed09_e64_bank6_v1_20261009','train_neural_BF16_medium2048_recent252forward5huber050_seed09_e64_bank6_v1_20261009.py'),('BF16Recent252Forward5Huber050171_independent_full5_GPU_controls_v1_20261009','verify_BF16Recent252Forward5Huber050171_full5_independent_GPU_v1_20261009.py'),('BF16Recent252Forward5Huber050171_actual_native42_calendar_v1_20261009','verify_BF16Recent252Forward5Huber050171_native42_calendar_v1_20261009.py')]
    for name,driver in tasks:
        if not allowed():return
        row=start_service(name,driver,[],{str(p):sha(p) for p in [A/driver,proof,A/'neural_BF16_medium2048_recent252forward5huber050_seed09_e64_native_v1_20261009.py']})
        create(OUT/(name+'_launch.json'),row)
        write(OUT/'state.json',{'status':'actual_forward5_own_training_or_admission_running','actual_service':name,'recipe':'recent252forward5huber050','at_local':datetime.now().isoformat(),'new_quality_scores':0})
        folder=A/'service_owned_workflows_20261006'/name
        while owned(row):
            if not allowed():return
            time.sleep(15)
        assert read(folder/'service_execution.json')['status']=='passed',read(folder/'service_execution.json')
    write(OUT/'state.json',{'status':'own_forward5_six_fits_full5_native42_qualified_official_comparison_pending','at_local':datetime.now().isoformat(),'new_quality_scores':0})
    print('PASS own forward5 GPU controls and six fits; official scoring still required',flush=True)
if __name__=='__main__':main()
