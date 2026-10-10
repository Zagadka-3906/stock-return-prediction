"""Retire verified idle orchestration only; keep all scientific workers running."""
from pathlib import Path
import sys,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle,retire_suspended
from handoff_ready_goss_full_execution_20261006 import start_service
import run_continuous_fast_reused_frontiers_v15_20261010 as prior

def main():
    assert prior.allowed();read(A/'current_user_runtime_control_20261009.json')
    out=A/'new_return_priority_handoff_v19_20261010';out.mkdir(exist_ok=False)
    assert not (A/'ReusedNN165_prepared_frontier_v1_20261010.json').exists()
    old=read(A/'service_owned_workflows_20261006/continuous_fast_reused_frontiers_v18_20261010/native_launch.json');assert owned(old)
    parent,worker,boundary=suspended_idle(old,'    closed (run_continuous_fast_reused_frontiers_v15_20261010.py:')
    retired=False
    try:
        state=read(A/'continuous_fast_reused_frontiers_v18_20261010/state.json');assert state['round']==165
        preserved={}
        for folder in (A/'service_owned_workflows_20261006').iterdir():
            if not (folder.name.startswith(('actual_BF16_medium2048_topweighted','BF16TopWeighted','actual_TopWeighted_after163'))):continue
            p=folder/'native_launch.json'
            if p.exists() and owned(read(p)):preserved[folder.name]=read(p)
        assert 'actual_BF16_medium2048_topweightedhuber010_seed09_e64_bank6_v1_20261009' in preserved
        create(out/'frozen_before_handoff.json',{'original_state':state,'old':old,'boundary':boundary,'preserved_scientific_workers':preserved})
        source=A/'run_continuous_fast_reused_frontiers_v19_20261010.py'
        row=start_service('continuous_fast_reused_frontiers_v19_20261010',source.name,[],{str(source):sha(source)})
        while not (A/'continuous_fast_reused_frontiers_v19_20261010/state.json').exists():assert owned(row);time.sleep(.5)
        assert all(owned(v) for v in preserved.values())
        retire_suspended(old,row);retired=True
        create(out/'verification.json',{'status':'passed_idle_controller_handoff_all_scientific_workers_preserved','new':row,'preserved_scientific_workers':preserved,'science_stopped_or_restarted':0,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S')})
        print({'status':'passed','new':row,'preserved':list(preserved)},flush=True)
    finally:
        if not retired:
            for p in (parent,worker):
                if p.is_running():p.resume()
if __name__=='__main__':main()
