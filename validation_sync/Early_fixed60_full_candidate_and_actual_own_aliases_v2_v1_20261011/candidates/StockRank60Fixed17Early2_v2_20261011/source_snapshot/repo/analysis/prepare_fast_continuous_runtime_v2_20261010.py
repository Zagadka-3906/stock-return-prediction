"""Improve future main serialization and observer coverage; retain active scoring and immutable sources."""
from pathlib import Path
import sys,time
A=Path(__file__).resolve().parent;ROOT=A.parent
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from scheduled_user_pause_20261007 import inventory,verified_pair,exact
from shutdown_ready_stop_v2_20261007 import StableJournal
from handoff_ready_goss_full_execution_20261006 import start_service

def retire_idle(name,folder):
    row=next(r for r in inventory(full=True) if r['name']==name)
    pair=verified_pair(row['launch']);assert pair is not None and not pair[0].children()
    journal=StableJournal(folder);journal.suspend_pair(row)
    for e in journal.data['entries']:
        if e['phase'] in ('pending','suspended'):
            p=exact(e['identity'])
            if p:p.terminate();p.wait(timeout=5)
            e['phase']='idle_operational_controller_superseded';journal.flush()
    return row

def main():
    old=A/'build_reused_neural_frontier_v1_20261010.py';s=old.read_text(encoding='utf8')
    needle="        compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\\n');created.append(target)"
    assert s.count(needle)==1
    insert="""        if name.startswith('publish_'):
            text=text.replace("with safe(log),serial(log/'serial_mutex.json'),git_io(log/'file_backed_git'):",
                "with serial(log/'serial_mutex.json') as mutex,safe(log),git_io(log/'file_backed_git'):\\n        mutex.acquire()")
"""
    s=s.replace(needle,insert+needle)
    builder=A/'build_reused_neural_frontier_v2_20261010.py';assert not builder.exists();compile(s,str(builder),'exec');builder.write_text(s,encoding='utf8',newline='\n')
    old=A/'run_continuous_fast_reused_frontiers_v1_20261010.py';s=old.read_text(encoding='utf8')
    s=s.replace('build_reused_neural_frontier_v1_20261010','build_reused_neural_frontier_v2_20261010')
    s=s.replace("OUT=A/'continuous_fast_reused_frontiers_v1_20261010'","OUT=A/'continuous_fast_reused_frontiers_v2_20261010'")
    needle="        rows[name]=start_service(name,wrapper.name,args,pins)"
    assert s.count(needle)==1
    replacement="""        existing=A/'service_owned_workflows_20261006'/name
        if existing.is_dir():
            row=read(existing/'native_launch.json')
            assert owned(row) or read(existing/'service_execution.json')['status']=='passed',(name,'Existing failed workflow requires separate immutable recovery')
            rows[name]=row
        else:
            rows[name]=start_service(name,wrapper.name,args,pins)"""
    s=s.replace(needle,replacement)
    controller=A/'run_continuous_fast_reused_frontiers_v2_20261010.py';assert not controller.exists();compile(s,str(controller),'exec');controller.write_text(s,encoding='utf8',newline='\n')
    # The previous controller is waiting for full158; no scientific workers are retired.
    state=read(A/'continuous_fast_reused_frontiers_v1_20261010/state.json');assert state['round']==158 and state['status']=='actual_chronological_frontier_running'
    folder=A/'continuous_fast_controller_handoff_v2_20261010';folder.mkdir()
    old_row=retire_idle('continuous_fast_reused_frontiers_v1_20261010',folder)
    row=start_service('continuous_fast_reused_frontiers_v2_20261010',controller.name,[],{str(controller):sha(controller),str(builder):sha(builder)})
    create(folder/'verification.json',{'status':'passed_idle_only_controller_handoff_current158_jobs_reused_without_restart',
        'old':old_row,'new':row,'scientific_training_scoring_inference_jobs_stopped':0})
    old=A/'monitor_fast_optimization_v1_20261010.py';s=old.read_text(encoding='utf8')
    s=s.replace('optimization_live_progress_v1_20261010','optimization_live_progress_v2_20261010')
    needle="        write(A/'optimization_live_progress_v2_20261010.json',state)"
    extra="""        loop=A/'continuous_fast_reused_frontiers_v2_20261010/state.json'
        if loop.is_file():
            state['continuous_reused_frontiers']=read(loop)
            number=state['continuous_reused_frontiers'].get('round')
            if number:
                count=23 if number==158 else 19
                quality=A/f'ReusedNN{number}Quality{count}_official_comparison_v1_20261009'
                state['continuous_reused_frontiers']['actual_saved_official_scores']=len(list(quality.glob('case*_official.json')))
                state['continuous_reused_frontiers']['official_score_complete']=(quality/'verification.json').is_file()
"""
    assert s.count(needle)==1;s=s.replace(needle,extra+needle)
    needle="        target=A/'optimization_live_progress_v2_20261010.md';temporary=target.with_suffix('.tmp')"
    s=s.replace(needle,"        if 'continuous_reused_frontiers' in state:text+=f\"\\n连续扩展：{state['continuous_reused_frontiers']}\\n\"\n"+needle)
    observer=A/'monitor_fast_optimization_v2_20261010.py';assert not observer.exists();compile(s,str(observer),'exec');observer.write_text(s,encoding='utf8',newline='\n')
    folder=A/'fast_progress_observer_handoff_v2_20261010';folder.mkdir();retire_idle('actual_fast_optimization_progress_v1_20261010',folder)
    progress=start_service('actual_fast_optimization_progress_v2_20261010',observer.name,[],{str(observer):sha(observer)})
    create(folder/'verification.json',{'status':'passed_observer_only_handoff_scientific_jobs_untouched','new':progress})
    print({'continuous_controller':row['owned_worker_pid'],'observer':progress['owned_worker_pid']},flush=True)
if __name__=='__main__':main()
