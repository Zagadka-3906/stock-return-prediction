"""Retire only the idle dispatcher; complete164 first, then prioritize new own TopWeighted fits."""
from pathlib import Path
import sys,time
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle,retire_suspended
from handoff_ready_goss_full_execution_20261006 import start_service
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed();out=A/'topweighted_training_priority_handoff_v18_20261010';out.mkdir(exist_ok=False)
    proof=A/'TopWeightedHuber_own_bank_controls_source_admission_v1_20261010.json'
    for p,d in read(proof)['input_sha256'].items():assert sha(p)==d,p
    old=read(A/'service_owned_workflows_20261006/continuous_fast_reused_frontiers_v17_20261010/native_launch.json');assert owned(old)
    assert not (A/'ReusedNN165_prepared_frontier_v1_20261010.json').exists()
    parent,worker,boundary=suspended_idle(old,'    closed (run_continuous_fast_reused_frontiers_v15_20261010.py:')
    retired=False
    try:
        state=read(A/'continuous_fast_reused_frontiers_v17_20261010/state.json');assert state['round']==164
        preserved={}
        for folder in (A/'service_owned_workflows_20261006').glob('ReusedNN164*'):
            p=folder/'native_launch.json'
            if p.exists() and owned(read(p)):preserved[folder.name]=read(p)
        create(out/'frozen_before_handoff.json',{'original_state':state,'old':old,'boundary':boundary,'preserved_scientific_workers':preserved,'new_GPU_consumers_only_after_actual164_complete':True})
        source=A/'run_continuous_fast_reused_frontiers_v18_20261010.py';compile(source.read_text(encoding='utf8'),str(source),'exec')
        row=start_service('continuous_fast_reused_frontiers_v18_20261010',source.name,[],{str(source):sha(source),str(proof):sha(proof)})
        while not (A/'continuous_fast_reused_frontiers_v18_20261010/state.json').exists():assert owned(row);time.sleep(.5)
        assert all(owned(v) for v in preserved.values())
        retire_suspended(old,row);retired=True
        create(out/'verification.json',{'status':'passed_idle_dispatcher_handoff_preserving_all_active164_science','new':row,'preserved_scientific_workers':preserved,'scientific_workers_stopped_or_restarted':0,'new_native_fits_by_handoff':0,'new_quality_scores':0,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S')})
    finally:
        if not retired:
            for p in (parent,worker):
                if p.is_running():p.resume()
if __name__=='__main__':main()
