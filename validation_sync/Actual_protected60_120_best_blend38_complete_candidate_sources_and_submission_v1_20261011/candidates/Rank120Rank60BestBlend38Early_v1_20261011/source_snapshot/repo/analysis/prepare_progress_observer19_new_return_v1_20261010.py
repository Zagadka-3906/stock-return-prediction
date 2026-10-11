"""Observe the actual new-signal dispatcher and both new model banks."""
from pathlib import Path
import sys,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle,retire_suspended

def main():
    s=(A/'monitor_fast_optimization_v18_20261010.py').read_text(encoding='utf8').replace('continuous_fast_reused_frontiers_v18_20261010','continuous_fast_reused_frontiers_v19_20261010').replace('optimization_live_progress_v18_20261010','optimization_live_progress_v19_20261010')
    needle='        screen_rows=[]'
    add='''        returnbank=Path('E:/赛题五_本机临时/neural_BF16_medium2048_returnhuber050_seed09_e64_bank6_v1_20261009')
        state['actual_new_ReturnHuber_training']={'completed_annual_models':[y for y in range(2020,2026) if (returnbank/str(y)/'info.json').is_file()],'six_fit_verification_complete':(returnbank/'verification.json').is_file(),'quality_scores_not_claimed_until_own_full5_and_native42':True}
        if (returnbank/'actual_stage.json').is_file():state['actual_new_ReturnHuber_training']['stage']=read(returnbank/'actual_stage.json')
        topscreen=Path('E:/赛题五_本机临时/TopWeighted_after163_high_impact65_screen_v1_20261010')
        state['TopWeighted_after163_screen']={'complete':(topscreen/'verification.json').is_file(),'expected_cases':65}
        for key,file in [('stage','actual_stage.json'),('best_so_far','best_so_far.json')]:
            if (topscreen/file).is_file():state['TopWeighted_after163_screen'][key]=read(topscreen/file)
'''
    assert s.count(needle)==1;s=s.replace(needle,add+needle)
    s=s.replace("'causal_neural_smoothing73_screen_v1_20261010'):","'causal_neural_smoothing73_screen_v1_20261010','TopWeighted_after163_high_impact65_screen_v1_20261010'):")
    needle='        for logical,name in names.items():'
    assert s.count(needle)==1
    s=s.replace(needle,"        names.update({k:k for k in ['actual_TopWeighted_after163_high_impact65_screen_v1_20261010','actual_BF16_medium2048_returnhuber050_seed09_restart_control_v1_20261009','BF16ReturnHuber050166_independent_small_CPU_v1_20261009','actual_BF16_medium2048_returnhuber050_seed09_e64_bank6_v1_20261009','BF16ReturnHuber050166_independent_full5_GPU_controls_v1_20261009','BF16ReturnHuber050166_actual_native42_calendar_v1_20261009']})\n"+needle)
    s=s.replace('各任务状态以同名JSON为准。','各任务状态以同名JSON为准；新Top与直接收益率训练进度见下方。')
    s=s.replace("        target=A/'optimization_live_progress_v19", "        text+=f\"\\n新Top加权训练：{state['actual_new_TopWeighted_training']}\\n\\n当前最佳163之后65项组合：{state['TopWeighted_after163_screen']}\\n\\n新直接收益率训练：{state['actual_new_ReturnHuber_training']}\\n\"\n        target=A/'optimization_live_progress_v19")
    target=A/'monitor_fast_optimization_v19_20261010.py';assert not target.exists();compile(s,str(target),'exec');target.write_text(s,encoding='utf8',newline='\n')
    old=read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_v18_20261010/native_launch.json');assert owned(old)
    parent,worker,boundary=suspended_idle(old,'    main (monitor_fast_optimization_v18_20261010.py:')
    retired=False
    try:
        row=start_service('actual_fast_optimization_progress_v19_20261010',target.name,[],{str(target):sha(target)})
        while not (A/'optimization_live_progress_v19_20261010.json').exists():assert owned(row);time.sleep(.5)
        retire_suspended(old,row);retired=True
        create(A/'actual_fast_optimization_progress_v19_handoff_v1_20261010.json',{'status':'passed_observer_only_handoff','new':row,'old_idle_boundary':boundary,'no_scientific_tasks_stopped':True})
        print(row,flush=True)
    finally:
        if not retired:
            for p in (parent,worker):
                if p.is_running():p.resume()
if __name__=='__main__':main()
