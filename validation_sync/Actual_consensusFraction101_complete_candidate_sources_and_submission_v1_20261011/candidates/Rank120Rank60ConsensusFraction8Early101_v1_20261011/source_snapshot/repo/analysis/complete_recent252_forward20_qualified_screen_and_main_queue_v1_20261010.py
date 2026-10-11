"""Wait for own scientific admission, then screen and publish all actual comparisons."""
from pathlib import Path
import sys,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def wait(name):
    folder=A/'service_owned_workflows_20261006'/name
    while not (folder/'service_execution.json').exists() or owned(read(folder/'native_launch.json')):
        if not allowed():return False
        time.sleep(15)
    assert read(folder/'service_execution.json')['status']=='passed',read(folder/'service_execution.json')
    return True
def main():
    assert allowed()
    if not wait('actual_recent252_forward20_own_controls_and_training_queue_v1_20261010'):return
    if not wait('RecentReturn252Protected168_round168_full_registration_v1_20261010'):return
    for name,driver,args in [('actual_Recent252Forward20_after168_high_impact65_screen_v1_20261010','run_Recent252Forward20_after168_high_impact65_screen_v1_20261010.py',[]),('actual_Recent252Forward20_after168_65_completion_main_v21_20261010','publish_Recent252Forward20_after168_65_completion_v21_20261010.py',['huber65'])]:
        if not allowed():return
        row=start_service(name,driver,args,{str(A/driver):sha(A/driver)})
        create(A/(name+'_activation.json'),row)
        if not wait(name):return
    create(A/'Recent252Forward20_qualified65_main_queue_completion_v1_20261010.json',{'status':'passed_own_six_fit_full5_native42_and65_actual_official_comparisons_published','submission_qualified':False,'full_candidate_round_freeze_and_native_controls_still_required_if_winner':True})
if __name__=='__main__':main()
