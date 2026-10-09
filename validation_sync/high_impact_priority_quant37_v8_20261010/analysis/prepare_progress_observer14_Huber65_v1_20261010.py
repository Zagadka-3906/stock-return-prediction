"""Extend actual progress to the independent65 screen; retire only a proven idle observer."""
from pathlib import Path
import sys,ast,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A),str(A.parent)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle,retire_suspended
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def main():
    assert allowed();source=A/'monitor_fast_optimization_v13_20261010.py';text=source.read_text(encoding='utf8')
    text=text.replace('optimization_live_progress_v13_20261010','optimization_live_progress_v14_20261010')
    text=text.replace("'protected_official_top_screen_v2_20261010'):","'protected_official_top_screen_v2_20261010','Huber010_high_impact65_screen_v1_20261010'):")
    needle='        screen_rows=[]';assert text.count(needle)==1
    replacement="""        new_screen=Path('E:/赛题五_本机临时/Huber010_high_impact65_screen_v1_20261010')
        state['new_Huber65_screen']={'expected_cases':65,'complete':(new_screen/'verification.json').is_file(),'queued_after_own_Huber6_full5_native42':True}
        for key,file in [('stage','actual_stage.json'),('best_so_far','best_so_far.json')]:
            if (new_screen/file).is_file():state['new_Huber65_screen'][key]=read(new_screen/file)
        state['protected162_full_chain_descriptor_installed']=(A/'TailProtected162_full76_ready_dispatch_v1_20261010.json').is_file()
        screen_rows=[]"""
    text=text.replace(needle,replacement)
    needle="        target=A/'optimization_live_progress_v14_20261010.md'";assert text.count(needle)==1
    text=text.replace(needle,"        text+=f\"\\n新Huber完整157之后65项组合验证：{state['new_Huber65_screen']}\\n\"\n"+needle)
    target=A/'monitor_fast_optimization_v14_20261010.py';assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    out=A/'Huber65_progress_observer_handoff_v14_20261010';out.mkdir(exist_ok=False)
    old=read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_v13_20261010/native_launch.json')
    sleep=[n.lineno for n in ast.walk(ast.parse(source.read_text(encoding='utf8'))) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='sleep' and n.args and isinstance(n.args[0],ast.Constant) and n.args[0].value==20];assert len(sleep)==1
    parent,worker,proof=suspended_idle(old,f'    main ({source.name}:{sleep[0]})')
    try:
        create(out/'owned_observer_before_and_after_idle_hold.json',proof)
        row=start_service('actual_fast_optimization_progress_v14_20261010',target.name,[],{str(target):sha(target)})
        while not (A/'optimization_live_progress_v14_20261010.json').exists():assert owned(row);time.sleep(.5)
        assert read(A/'optimization_live_progress_v14_20261010.json')['new_Huber65_screen']['expected_cases']==65
        retire_suspended(old,row)
        create(out/'verification.json',{'status':'passed_idle_observer_only_retired_new65_and_full162_actual_progress_visible','old':old,'new':row,'source_sha256':sha(target),'new_quality_scores':0,'new_native_fits':0,'scientific_workers_stopped_or_restarted':0})
    finally:
        for process in (parent,worker):
            if process.is_running():process.resume()

if __name__=='__main__':main()
