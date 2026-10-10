"""After actual164, fit a genuinely different TopWeighted signal before round165 quality."""
from pathlib import Path
import sys,time,itertools
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
import run_continuous_fast_reused_frontiers_v15_20261010 as prior
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from scheduled_user_pause_20261007 import write
from handoff_ready_goss_full_execution_20261006 import start_service
OUT=A/'continuous_fast_reused_frontiers_v18_20261010'
def main():
    assert prior.allowed();OUT.mkdir(exist_ok=False);prior.OUT=OUT
    create(OUT/'frozen_before_genuinely_new_training_dispatch.json',{'expected_first_new_quality_round':165,'recipe':'topweightedhuber010','own6_fits_full5_native42_required_before_quality':True,'await_complete164_before_any_GPU_consumer':True,'deadline':read(A/'current_user_runtime_control_20261010.json')['stop_at_local'],'test_labels_read':False})
    write(OUT/'state.json',{'status':'waiting_actual_complete164_before_new_TopWeighted_training','round':164,'quality_cases':19,'QA':75,'full_service':'ReusedNN164Quality19_round164_full_registration_v1_20261009','at_local':time.strftime('%Y-%m-%dT%H:%M:%S')})
    if not prior.closed('ReusedNN164Quality19_round164_full_registration_v1_20261009'):return
    proof=A/'TopWeightedHuber_own_bank_controls_source_admission_v1_20261010.json'
    for p,d in read(proof)['input_sha256'].items():assert sha(p)==d,p
    tasks=[('actual_BF16_medium2048_topweightedhuber010_seed09_restart_control_v1_20261009','verify_neural_BF16_medium2048_topweightedhuber010_seed09_restart_v1_20261009.py'),('BF16TopWeightedHuber010165_independent_small_CPU_v1_20261009','verify_BF16TopWeightedHuber010165_independent_small_CPU_v1_20261009.py'),('actual_BF16_medium2048_topweightedhuber010_seed09_e64_bank6_v1_20261009','train_neural_BF16_medium2048_topweightedhuber010_seed09_e64_bank6_v1_20261009.py'),('BF16TopWeightedHuber010165_independent_full5_GPU_controls_v1_20261009','verify_BF16TopWeightedHuber010165_full5_independent_GPU_v1_20261009.py'),('BF16TopWeightedHuber010165_actual_native42_calendar_v1_20261009','verify_BF16TopWeightedHuber010165_native42_calendar_v1_20261009.py')]
    for name,driver in tasks:
        if not prior.allowed():return
        p=A/driver
        pins={str(p):sha(p),str(proof):sha(proof),str(A/'neural_BF16_medium2048_topweightedhuber010_seed09_e64_native_v1_20261009.py'):sha(A/'neural_BF16_medium2048_topweightedhuber010_seed09_e64_native_v1_20261009.py')}
        row=start_service(name,driver,[],pins);create(OUT/(name+'_launch.json'),row)
        write(OUT/'state.json',{'status':'actual_new_TopWeighted_training_or_own_controls_running','round':165,'quality_cases':19,'QA':76,'recipe':'topweightedhuber010','actual_service':name,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'new_quality_scores':0,'future_X_read':False})
        if not prior.closed(name):return
    for n in range(165,1001):
        if not prior.allowed():return
        if n==165:
            from build_reused_topweighted_neural_frontier_v10_20261010 import build
            recipe,role,grid='topweightedhuber010','nonflag_valid',10
        else:
            build=prior.build
            if n<=172:
                recipe,role=[('seed10','all_valid'),('drop05','all_valid'),('seed09','nonflag_valid'),('huber010','flag_valid'),('seed09','flag_valid'),('seed10','flag_valid'),('drop05','flag_valid')][n-166];grid=10
            else:
                expanded=list(itertools.product(('nonflag_valid','all_valid','flag_valid'),('huber010','seed09','seed10','drop05')))
                role,recipe=expanded[(n-173)%12];grid=1+(n-173)//12
        import psutil
        while prior.allowed() and (psutil.disk_usage('D:/').free<1.5*2**30 or psutil.disk_usage('E:/').free<22*2**30):
            write(OUT/'state.json',{'status':'waiting_actual_storage_boundary','next_round':n,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S')});time.sleep(30)
        if not prior.allowed():return
        assert prior.closed(f'ReusedNN{n-1}Quality19_round{n-1}_full_registration_v1_20261009')
        value=build(n,recipe,role,grid);create(A/f'ReusedNN{n}_prepared_frontier_v1_20261010.json',value)
        name=prior.launch_frontier(value)
        write(OUT/'state.json',{'status':'actual_chronological_frontier_running','round':n,'recipe':recipe,'role':role,'grid':grid,'quality_cases':value['count'],'QA':value['QA'],'full_service':name,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S')})
        if not prior.closed(name):return
        assert read(A/f'optimization_20261003_r{n}/full_registration_execution.json')['status']=='passed'
        receipt=read(A/f'github_validation_sync_main_20261005/round{n}_receipt.json');assert receipt['status']=='pushed_and_remote_head_verified'
        create(OUT/f'round{n}_fully_qualified.json',{'status':'passed_full_quality_freeze_inference_causal_QA_and_main','receipt':receipt,'test_labels_read':False})
if __name__=='__main__':main()
