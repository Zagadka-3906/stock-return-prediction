"""Replace only the idle administrative dispatcher; preserve all live science."""
from pathlib import Path
import sys,time
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle,retire_suspended
from handoff_ready_goss_full_execution_20261006 import start_service
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed();folder=A/'superior_Huber_priority_controller_handoff_v16_20261010';folder.mkdir(exist_ok=False)
    old=read(A/'service_owned_workflows_20261006/continuous_fast_reused_frontiers_v15_20261010/native_launch.json')
    assert owned(old) and not (A/'ReusedNN163_prepared_frontier_v1_20261010.json').exists()
    script=A/'run_continuous_fast_reused_frontiers_v16_20261010.py';compile(script.read_text(encoding='utf8'),str(script),'exec')
    proof=read(Path('E:/赛题五_本机临时/Huber010_high_impact65_screen_v1_20261010/verification.json'))
    assert len(proof['records'])==65 and proof['best']['connected_final_score']>0.45120245465782494
    parent,worker,boundary=suspended_idle(old,'    closed (run_continuous_fast_reused_frontiers_v15_20261010.py:')
    retired=False
    try:
        state=read(A/'continuous_fast_reused_frontiers_v15_20261010/state.json');assert state['round']==162
        create(folder/'actual_idle_boundary.json',{'old':old,'stack':boundary,'state':state,'scientific_workers_stopped_or_restarted':0})
        pins={str(p):sha(p) for p in (Path(__file__),script,A/'run_continuous_fast_reused_frontiers_v15_20261010.py')}
        row=start_service('continuous_fast_reused_frontiers_v16_20261010',script.name,[],pins)
        assert owned(row)
        retire_suspended(old,row);retired=True
        create(folder/'verification.json',{'status':'passed_idle_administrative_dispatcher_priority_handoff','new':row,'scientific_workers_stopped_or_restarted':0,'awaits_actual_full162_then_prospective163_admission':True,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S')})
    finally:
        if not retired:
            if parent.is_running():parent.resume()
            if worker.is_running():worker.resume()
if __name__=='__main__':main()
