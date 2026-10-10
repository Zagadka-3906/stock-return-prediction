"""Display the actual controller17, Huber163 and smoothing73; retire only the idle observer."""
from pathlib import Path
import sys,ast,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A),str(A.parent)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle,retire_suspended
def main():
    source=A/'monitor_fast_optimization_v16_20261010.py';text=source.read_text(encoding='utf8')
    text=text.replace('optimization_live_progress_v16_20261010','optimization_live_progress_v17_20261010').replace('continuous_fast_reused_frontiers_v15_20261010','continuous_fast_reused_frontiers_v17_20261010')
    text=text.replace('count=23 if current_round==158 else 19',"count=loop_state.get('quality_cases',23 if current_round==158 else 19)")
    text=text.replace('count=23 if number==158 else 19',"count=state['continuous_reused_frontiers'].get('quality_cases',23 if number==158 else 19)")
    text=text.replace("if number==162:","if number in (162,163):")
    text=text.replace("pilot=Path('E:/赛题五_本机临时/protected_tail_selected_native14_v1_20261010/pilot76.json')","pilot=Path('E:/赛题五_本机临时/protected_tail_selected_native14_v1_20261010/pilot76.json' if number==162 else 'E:/赛题五_本机临时/protected_Huber_selected_native14_v1_20261010/pilot67.json')")
    needle='        for logical,name in names.items():';assert text.count(needle)==1
    text=text.replace(needle,"        names.update({k:k for k in ['continuous_fast_reused_frontiers_v17_20261010','HuberProtected163_complete67_family_v2_20261010','HuberProtected163_selected_native14_v1_20261010','HuberProtected163_selected_candidate_preparation_v1_20261010','HuberProtected163_selected_candidate_sealing_v1_20261010','HuberProtected163_round163_full_registration_v1_20261010','actual_causal_neural_smoothing73_screen_v1_20261010']})\n"+needle)
    text=text.replace("'budgeted_neural_Top37_screen_v1_20261010'):","'budgeted_neural_Top37_screen_v1_20261010','causal_neural_smoothing73_screen_v1_20261010'):")
    needle='        screen_rows=[]';assert text.count(needle)==1
    text=text.replace(needle,"        temporal=Path('E:/赛题五_本机临时/causal_neural_smoothing73_screen_v1_20261010')\n        state['causal_neural_smoothing73_screen']={'expected_cases':73,'complete':(temporal/'verification.json').is_file(),'new_native_fits':0}\n        for key,file in [('stage','actual_stage.json'),('best_so_far','best_so_far.json')]:\n            if (temporal/file).is_file():state['causal_neural_smoothing73_screen'][key]=read(temporal/file)\n"+needle)
    target=A/'monitor_fast_optimization_v17_20261010.py';assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    old=read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_v16_20261010/native_launch.json')
    sleeps=[n.lineno for n in ast.walk(ast.parse(source.read_text(encoding='utf8'))) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='sleep' and n.args and isinstance(n.args[0],ast.Constant) and n.args[0].value==20];assert len(sleeps)==1
    parent,worker,boundary=suspended_idle(old,f'    main ({source.name}:{sleeps[0]})')
    folder=A/'Huber163_smoothing73_observer_handoff_v17_20261010';folder.mkdir(exist_ok=False)
    try:
        row=start_service('actual_fast_optimization_progress_v17_20261010',target.name,[],{str(target):sha(target)})
        while not (A/'optimization_live_progress_v17_20261010.json').exists():assert owned(row);time.sleep(.5)
        state=read(A/'optimization_live_progress_v17_20261010.json');assert state['continuous_reused_frontiers']['round']==163 and state['causal_neural_smoothing73_screen']['expected_cases']==73
        retire_suspended(old,row)
        create(folder/'verification.json',{'status':'passed_only_idle_observer_retired_actual163_and_smoothing73_visible','new':row,'old':old,'boundary':boundary,'new_quality_scores':0,'scientific_workers_stopped_or_restarted':0})
    finally:
        for p in (parent,worker):
            if p.is_running():p.resume()
if __name__=='__main__':main()
