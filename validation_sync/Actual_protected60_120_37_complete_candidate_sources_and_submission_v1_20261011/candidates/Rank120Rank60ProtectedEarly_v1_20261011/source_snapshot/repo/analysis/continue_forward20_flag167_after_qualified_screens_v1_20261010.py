"""Qualify a distinct flag-stock composition only after actual own and priority screen results."""
from pathlib import Path
from datetime import datetime
import sys,time,shutil
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from scheduled_user_pause_20261007 import write
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from build_reused_forward20_neural_frontier_v14_20261010 import build
import run_continuous_fast_reused_frontiers_v15_20261010 as dispatcher
OUT=A/'forward20_flag167_after_priority_screens_queue_v1_20261010'
def wait(name):
    p=A/'service_owned_workflows_20261006'/name
    while allowed():
        if (p/'service_execution.json').exists() and not owned(read(p/'native_launch.json')):
            assert read(p/'service_execution.json')['status']=='passed',read(p/'service_execution.json')
            return True
        time.sleep(15)
    return False
def main():
    assert allowed();OUT.mkdir(exist_ok=False);dispatcher.OUT=OUT;dispatcher.allowed=allowed
    write(OUT/'state.json',{'status':'waiting_own_forward20_full_admission_and_both65_screens_before_new167','at_local':datetime.now().isoformat()})
    for name in ('actual_forward20_qualified_screen_and_main_queue_v1_20261010','actual_Return_after163_65_completion_main_v17_20261010'):
        if not wait(name):return
    for family in ('Return','Forward20'):
        p=Path('E:/赛题五_本机临时')/(family+'_after163_high_impact65_screen_v1_20261010')/'verification.json';proof=read(p)
        assert len(proof['records'])==65
        if proof['best']['score_gain_over_qualified_parent']>0:
            write(OUT/'state.json',{'status':'priority_screen_has_actual_improvement_requires_its_whole_scheme_freeze_before_flag167','family':family,'best':proof['best'],'source':str(p),'goal_remains_active':True,'at_local':datetime.now().isoformat()})
            return
    assert read(A/'optimization_20261003_r166/full_registration_execution.json')['status']=='passed'
    while allowed() and (shutil.disk_usage('D:/').free<1.5*2**30 or shutil.disk_usage('E:/').free<22*2**30):
        write(OUT/'state.json',{'status':'resource_boundary_wait_before_fresh167_requires_audited_scratch_cleanup','at_local':datetime.now().isoformat()});time.sleep(20)
    if not allowed():return
    value=build(167,'forward20huber050','flag_valid',10)
    create(OUT/'actual_generated167_prospective_sources.json',value)
    full=dispatcher.launch_frontier(value)
    write(OUT/'state.json',{'status':'actual167_full17_native14_official19_freeze_candidate_QA78_main_running','full_service':full,'at_local':datetime.now().isoformat()})
    if not wait(full):return
    final=read(A/'optimization_20261003_r167/full_registration_execution.json');receipt=read(A/'github_validation_sync_main_20261005/round167_receipt.json')
    assert final['status']=='passed' and receipt['status']=='pushed_and_remote_head_verified' and receipt['scored_records']==19
    write(OUT/'state.json',{'status':'passed_complete167_with_actual_QA78_main','receipt':receipt,'at_local':datetime.now().isoformat()})
if __name__=='__main__':main()
