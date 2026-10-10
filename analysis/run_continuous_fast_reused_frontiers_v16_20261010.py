"""Prioritize the actually superior Huber protected screen after complete162."""
from pathlib import Path
import sys,time,itertools
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
import run_continuous_fast_reused_frontiers_v15_20261010 as prior
from run_dependency_queue_v3_20261006 import read,sha,create
from scheduled_user_pause_20261007 import write
from handoff_ready_goss_full_execution_20261006 import start_service
OUT=A/'continuous_fast_reused_frontiers_v16_20261010'

def main():
    assert prior.allowed();OUT.mkdir(exist_ok=False);prior.OUT=OUT
    create(OUT/'frozen_before_priority_dispatch.json',{'priority_reason':'Actual completed Huber65 screen beats the selected protected162 score; qualify it before further reused CDF grids','actual_screen_source':'E:/赛题五_本机临时/Huber010_high_impact65_screen_v1_20261010/verification.json','expected_round163_records':67,'deadline':read(A/'current_user_runtime_control_20261010.json')['stop_at_local'],'test_labels_read':False})
    if not prior.closed('TailProtected162_complete76_family_v1_20261010'):return
    descriptor=A/'HuberProtected163_full67_ready_dispatch_v1_20261010.json'
    while prior.allowed() and not descriptor.exists():
        write(OUT/'state.json',{'status':'waiting_superior_Huber163_complete_source_admission','round':163,'quality_cases':67,'QA':74,'waiting_descriptor':str(descriptor),'at_local':time.strftime('%Y-%m-%dT%H:%M:%S')});time.sleep(10)
    if not prior.allowed():return
    declaration=read(descriptor)
    assert (declaration['round'],declaration['quality_cases'],declaration['QA'])==(163,67,74)
    for p,d in declaration['input_sha256'].items():assert sha(p)==d,p
    name=declaration['service_name']
    row=start_service(name,declaration['driver'],declaration.get('arguments',[]),declaration['input_sha256'])
    create(OUT/'Huber163_actual_full_family_launch.json',row)
    write(OUT/'state.json',{'status':'actual_superior_Huber163_native_candidate_full_QA74_main_running','round':163,'quality_cases':67,'QA':74,'full_service':name,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S')})
    if not prior.closed(name):return
    assert read(A/'optimization_20261003_r163/full_registration_execution.json')['status']=='passed'
    for n in range(164,1001):
        if not prior.allowed():return
        if n<=172:
            recipe,role=[('huber010','all_valid'),('seed09','all_valid'),('seed10','all_valid'),('drop05','all_valid'),('seed09','nonflag_valid'),('huber010','flag_valid'),('seed09','flag_valid'),('seed10','flag_valid'),('drop05','flag_valid')][n-164];grid=10
        else:
            expanded=list(itertools.product(('nonflag_valid','all_valid','flag_valid'),('huber010','seed09','seed10','drop05')))
            role,recipe=expanded[(n-173)%12];grid=1+(n-173)//12
        import psutil
        while prior.allowed() and (psutil.disk_usage('D:/').free<1.5*2**30 or psutil.disk_usage('E:/').free<22*2**30):
            write(OUT/'state.json',{'status':'waiting_actual_storage_boundary','next_round':n});time.sleep(30)
        if not prior.allowed():return
        assert prior.closed(f'ReusedNN{n-1}Quality19_round{n-1}_full_registration_v1_20261009')
        value=prior.build(n,recipe,role,grid);create(A/f'ReusedNN{n}_prepared_frontier_v1_20261010.json',value)
        name=prior.launch_frontier(value)
        write(OUT/'state.json',{'status':'actual_chronological_frontier_running','round':n,'recipe':recipe,'role':role,'grid':grid,'quality_cases':value['count'],'QA':value['QA'],'full_service':name,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S')})
        if not prior.closed(name):return
        assert read(A/f'optimization_20261003_r{n}/full_registration_execution.json')['status']=='passed'
        receipt=read(A/f'github_validation_sync_main_20261005/round{n}_receipt.json');assert receipt['status']=='pushed_and_remote_head_verified'
        create(OUT/f'round{n}_fully_qualified.json',{'status':'passed_full_quality_freeze_inference_causal_QA_and_main','receipt':receipt,'test_labels_read':False})

if __name__=='__main__':main()
