"""Reuse live return training, then apply proven dynamic-namespace serialization to166."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import sys,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from scheduled_user_pause_20261007 import write
from handoff_ready_goss_full_execution_20261006 import start_service
import run_continuous_fast_reused_frontiers_v15_20261010 as prior
OUT=A/'continuous_fast_reused_frontiers_v21_20261010'

def allowed():
    now=datetime.now(timezone(timedelta(hours=8)))
    return all(c['status']=='optimization_active_after_explicit_manual_resume' and now<datetime.fromisoformat(c['stop_at_local']) for c in (read(A/name) for name in ('current_user_runtime_control_20261009.json','current_user_runtime_control_20261010.json')))
prior.allowed=allowed

def main():
    assert allowed();OUT.mkdir(exist_ok=False);prior.OUT=OUT
    assert prior.closed('ReusedNN165Quality19_round165_full_registration_v1_20261009')
    proof=A/'ReturnHuber050_own_bank_controls_source_admission_v1_20261010.json'
    for p,d in read(proof)['input_sha256'].items():assert sha(p)==d,p
    tasks=[('actual_BF16_medium2048_returnhuber050_seed09_restart_control_v1_20261009','verify_neural_BF16_medium2048_returnhuber050_seed09_restart_v1_20261009.py'),('BF16ReturnHuber050166_independent_small_CPU_v1_20261009','verify_BF16ReturnHuber050166_independent_small_CPU_v1_20261009.py'),('actual_BF16_medium2048_returnhuber050_seed09_e64_bank6_v1_20261009','train_neural_BF16_medium2048_returnhuber050_seed09_e64_bank6_v1_20261009.py'),('BF16ReturnHuber050166_independent_full5_GPU_controls_v1_20261009','verify_BF16ReturnHuber050166_full5_independent_GPU_v1_20261009.py'),('BF16ReturnHuber050166_actual_native42_calendar_v1_20261009','verify_BF16ReturnHuber050166_native42_calendar_v1_20261009.py')]
    for name,driver in tasks:
        if not allowed():return
        p=A/driver;folder=A/'service_owned_workflows_20261006'/name
        if folder.exists():
            row=read(folder/'native_launch.json');assert owned(row) or read(folder/'service_execution.json')['status']=='passed',(name,'immutable own recovery required')
        else:
            row=start_service(name,driver,[],{str(q):sha(q) for q in (p,proof,A/'neural_BF16_medium2048_returnhuber050_seed09_e64_native_v1_20261009.py')})
        create(OUT/(name+'_launch.json'),row)
        write(OUT/'state.json',{'status':'actual_direct_return_own_training_or_controls_running','round':166,'recipe':'returnhuber050','actual_service':name,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'new_quality_scores':0,'live_science_reused_without_restart':True})
        if not prior.closed(name):return
    stock='actual_stock_identity_prior_after163_screen33_v4_20261010'
    write(OUT/'state.json',{'status':'own_return_bank_qualified_waiting_stock33_priority_decision','round':166,'actual_service':stock,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S')})
    if not prior.closed(stock):return
    stockproof=read(Path(read(A/'actual_stock_identity_prior_after163_screen33_location_v4_20261010.json')['output'])/'verification.json')
    current=read(A/'latest_verified_submission_delivery_v2_20261008.json')
    if stockproof['best']['connected_final_score']>current['official_score']:
        write(OUT/'state.json',{'status':'stock_prior33_actual_winner_requires_complete_parent_freeze_and_next_round_assignment','round':166,'best':stockproof['best'],'return_own6_full5_native42_reusable':True,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S')});return
    import psutil
    while allowed() and (psutil.disk_usage('D:/').free<1.5*2**30 or psutil.disk_usage('E:/').free<22*2**30):
        write(OUT/'state.json',{'status':'waiting_actual_storage_boundary','next_round':166,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S')});time.sleep(30)
    if not allowed():return
    assert not (A/'ReusedNN166_prepared_frontier_v1_20261010.json').exists()
    from build_reused_return_neural_frontier_v13_20261010 import build
    value=build(166,'returnhuber050','nonflag_valid',10)
    create(A/'ReusedNN166_prepared_frontier_v1_20261010.json',value)
    name=prior.launch_frontier(value)
    write(OUT/'state.json',{'status':'actual_new_return166_full_qualification_running','round':166,'quality_cases':19,'QA':77,'recipe':'returnhuber050','full_service':name,'dynamic_snapshot_encoder_proven_and_installed':True,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S')})
    if not prior.closed(name):return
    receipt=read(A/'github_validation_sync_main_20261005/round166_receipt.json');assert receipt['status']=='pushed_and_remote_head_verified'
    create(OUT/'round166_fully_qualified.json',{'status':'passed_full_quality_freeze_inference_causal_QA_and_main','receipt':receipt})
    write(OUT/'state.json',{'status':'new_return166_complete_next_direction_requires_evidence_review','round':166,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S')})
if __name__=='__main__':main()
