"""Recover the idle main watcher without replacing its historical launch records."""
from pathlib import Path
import sys,time
A=Path(__file__).resolve().parent;ROOT=A.parent
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service
from shutdown_ready_stop_v2_20261007 import StableJournal
from scheduled_user_pause_20261007 import inventory,verified_pair,exact

def main():
    original=A/'watch_validations_main_safe_v10_20261009.py'
    source=original.read_text(encoding='utf8').replace('main_watcher_safe_v10_20261009','main_watcher_safe_v11_20261010')
    watcher=A/'watch_validations_main_safe_v11_20261010.py';watcher.write_text(source,encoding='utf8',newline='\n')
    row=start_service('main_publisher_v11_20261010',watcher.name,[],{str(watcher):sha(watcher),str(original):sha(original)})
    original=A/'manual_resume_service_alias_runtime_v2_20261010.py'
    source=original.read_text(encoding='utf8')
    needle="            name=aliases.get(path.parent.name)"
    assert source.count(needle)==1
    source=source.replace(needle,needle+"\n            if path.parent.name=='main_publisher_v10_20261009':name='main_publisher_v11_20261010'")
    wrapper=A/'manual_resume_service_alias_runtime_v3_20261010.py';wrapper.write_text(source,encoding='utf8',newline='\n')
    old='BF16Drop05_156_complete_chronological_dispatch_v3_20261009_manual_resume_v2_20261010'
    target=next(r for r in inventory(full=True) if r['name']==old)
    pair=verified_pair(target['launch']);assert pair is not None and not pair[0].children()
    folder=A/'manual_resume_dispatcher_handoff_v3_20261010';folder.mkdir()
    journal=StableJournal(folder);journal.suspend_pair(target)
    for entry in journal.data['entries']:
        if entry['phase'] in ('pending','suspended'):
            process=exact(entry['identity'])
            if process:process.terminate();process.wait(timeout=5)
            entry['phase']='idle_dispatcher_superseded';journal.flush()
    alias=A/'manual_resume_service_aliases_v2_20261010.json'
    driver=A/'dispatch_BF16Drop05_156_complete_pipeline_v3_20261009.py'
    dispatcher=start_service('BF16Drop05_156_complete_chronological_dispatch_manual_resume_v3_20261010',wrapper.name,
        ['--driver',str(driver),'--aliases',str(alias)],{str(wrapper):sha(wrapper),str(alias):sha(alias),str(driver):sha(driver)})
    observer=A/'monitor_fast_optimization_v1_20261010.py'
    progress=start_service('actual_fast_optimization_progress_v1_20261010',observer.name,[],{str(observer):sha(observer),str(alias):sha(alias)})
    create(A/'actual_resumed_watcher_and_progress_launches_v1_20261010.json',{'publisher':row,'dispatcher':dispatcher,'observer':progress,
           'scientific_training_untouched':True,'previous_watcher_evidence_retained':True})
    print({'publisher':row['owned_worker_pid'],'dispatcher':dispatcher['owned_worker_pid'],'observer':progress['owned_worker_pid']},flush=True)

if __name__=='__main__':main()
