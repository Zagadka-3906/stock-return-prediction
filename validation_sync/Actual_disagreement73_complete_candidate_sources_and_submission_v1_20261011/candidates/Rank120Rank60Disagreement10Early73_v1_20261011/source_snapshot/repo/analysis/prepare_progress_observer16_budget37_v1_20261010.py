"""Expose actual optional-swap scores and completed training, retiring only the idle observer."""
from pathlib import Path
import sys,ast,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A),str(A.parent)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle,retire_suspended
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def main():
    assert allowed();source=A/'monitor_fast_optimization_v15_20261010.py';text=source.read_text(encoding='utf8')
    text=text.replace('optimization_live_progress_v15_20261010','optimization_live_progress_v16_20261010')
    before="'protected_quantization37_screen_v1_20261010'):";assert text.count(before)==1
    text=text.replace(before,"'protected_quantization37_screen_v1_20261010','budgeted_neural_Top37_screen_v1_20261010'):")
    needle='        screen_rows=[]';assert text.count(needle)==1
    text=text.replace(needle,"""        budgeted=Path('E:/赛题五_本机临时/budgeted_neural_Top37_screen_v1_20261010')
        state['budgeted_neural_Top37_screen']={'expected_cases':37,'complete':(budgeted/'verification.json').is_file(),'new_native_fits':0}
        for key,file in [('stage','actual_stage.json'),('best_so_far','best_so_far.json')]:
            if (budgeted/file).is_file():state['budgeted_neural_Top37_screen'][key]=read(budgeted/file)
        state['actual_Huber_annual_training']['actual_training_bank_completed']=(huber/'verification.json').is_file() and read(huber/'verification.json').get('actual_native_fits')==6
        screen_rows=[]""")
    needle="        target=A/'optimization_live_progress_v16_20261010.md'";assert text.count(needle)==1
    text=text.replace(needle,"        text+=f\"\\n每日主动换股预算37项验证：{state['budgeted_neural_Top37_screen']}\\n\"\n"+needle)
    target=A/'monitor_fast_optimization_v16_20261010.py';assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    out=A/'budget37_progress_observer_handoff_v16_20261010';out.mkdir(exist_ok=False)
    old=read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_v15_20261010/native_launch.json')
    sleep=[n.lineno for n in ast.walk(ast.parse(source.read_text(encoding='utf8'))) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='sleep' and n.args and isinstance(n.args[0],ast.Constant) and n.args[0].value==20];assert len(sleep)==1
    parent,worker,proof=suspended_idle(old,f'    main ({source.name}:{sleep[0]})')
    try:
        create(out/'owned_observer_before_and_after_idle_hold.json',proof)
        row=start_service('actual_fast_optimization_progress_v16_20261010',target.name,[],{str(target):sha(target)})
        while not (A/'optimization_live_progress_v16_20261010.json').exists():assert owned(row);time.sleep(.5)
        assert read(A/'optimization_live_progress_v16_20261010.json')['budgeted_neural_Top37_screen']['expected_cases']==37
        retire_suspended(old,row)
        create(out/'verification.json',{'status':'passed_only_idle_observer_retired_actual_budget37_scores_and_Huber_bank_completion_visible','old':old,'new':row,'source_sha256':sha(target),'new_quality_scores':0,'new_native_fits':0,'scientific_workers_stopped_or_restarted':0})
    finally:
        for process in (parent,worker):
            if process.is_running():process.resume()

if __name__=='__main__':main()
