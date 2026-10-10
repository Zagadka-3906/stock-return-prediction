"""Expose the new training queue and actual six-state progress; no progress inferred from plans."""
from pathlib import Path
import sys,ast,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A),str(A.parent)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle,retire_suspended
def main():
    source=A/'monitor_fast_optimization_v17_20261010.py';text=source.read_text(encoding='utf8')
    text=text.replace('optimization_live_progress_v17_20261010','optimization_live_progress_v18_20261010').replace('continuous_fast_reused_frontiers_v17_20261010','continuous_fast_reused_frontiers_v18_20261010')
    needle='        for logical,name in names.items():';assert text.count(needle)==1
    text=text.replace(needle,"        names.update({k:k for k in ['actual_BF16_medium2048_topweightedhuber010_seed09_restart_control_v1_20261009','BF16TopWeightedHuber010165_independent_small_CPU_v1_20261009','actual_BF16_medium2048_topweightedhuber010_seed09_e64_bank6_v1_20261009','BF16TopWeightedHuber010165_independent_full5_GPU_controls_v1_20261009','BF16TopWeightedHuber010165_actual_native42_calendar_v1_20261009']})\n"+needle)
    needle='        screen_rows=[]';assert text.count(needle)==1
    text=text.replace(needle,"        topbank=Path('E:/赛题五_本机临时/neural_BF16_medium2048_topweightedhuber010_seed09_e64_bank6_v1_20261009')\n        state['actual_new_TopWeighted_training']={'completed_annual_models':[y for y in range(2020,2026) if (topbank/str(y)/'info.json').is_file()],'six_fit_verification_complete':(topbank/'verification.json').is_file(),'quality_scores_not_claimed_until_own_full5_and_native42':True}\n        if (topbank/'actual_stage.json').is_file():state['actual_new_TopWeighted_training']['stage']=read(topbank/'actual_stage.json')\n"+needle)
    target=A/'monitor_fast_optimization_v18_20261010.py';assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    old=read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_v17_20261010/native_launch.json')
    sleeps=[n.lineno for n in ast.walk(ast.parse(source.read_text(encoding='utf8'))) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='sleep' and n.args and isinstance(n.args[0],ast.Constant) and n.args[0].value==20];assert len(sleeps)==1
    parent,worker,boundary=suspended_idle(old,f'    main ({source.name}:{sleeps[0]})')
    out=A/'TopWeighted_training_observer_handoff_v18_20261010';out.mkdir(exist_ok=False)
    try:
        row=start_service('actual_fast_optimization_progress_v18_20261010',target.name,[],{str(target):sha(target)})
        while not (A/'optimization_live_progress_v18_20261010.json').exists():assert owned(row);time.sleep(.5)
        state=read(A/'optimization_live_progress_v18_20261010.json');assert 'actual_new_TopWeighted_training' in state
        retire_suspended(old,row)
        create(out/'verification.json',{'status':'passed_only_idle_observer_retired_actual_TopWeighted_training_counts_and_controller18_visible','old':old,'new':row,'boundary':boundary,'scientific_workers_stopped_or_restarted':0,'new_quality_scores':0})
    finally:
        for p in (parent,worker):
            if p.is_running():p.resume()
if __name__=='__main__':main()
