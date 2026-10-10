"""Queue14 only behind actually passed15 controls and full1366 qualification, with an accurate phase observer."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
    assert read(A/'service_owned_workflows_20261006/pending137to141_complete_prospective_controls_actual_D1_v15_20261008/service_execution.json')['status']=='passed'
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    driver=A/'dispatch_pending137to141_verified_fresh14_after_actual15_controls_20261008.py'
    row=start('pending137to141_dispatch_verified_fresh14_after_actual15_controls_20261008',driver.name,[],{str(driver):sha(driver),str(A/'pending137to141_collector_controls_v14_20261008.json'):sha(A/'pending137to141_collector_controls_v14_20261008.json')})
    create(A/'pending137to141_dispatch_verified_hidden_launch_v14_actual15_20261008.json',row)
    source=A/'monitor_actual_chronological_optimization_progress_v21_20261008.py'
    text=source.read_text(encoding='utf8').replace('v21','v22').replace(',13)',',14)')
    text=text.replace('pending137to141_complete_prospective_controls_v13_20261008','pending137to141_complete_prospective_controls_actual_D1_v15_20261008')
    text=text.replace('pending137to141_dispatch_verified_fresh13_20261008','pending137to141_dispatch_verified_fresh14_after_actual15_controls_20261008')
    before="'full_registration':status(f'{prefix}_round{number}_full_registration_v{version}_20261008')"
    after="'full_registration':status(f'{prefix}_round{number}_full_registration_v{6 if number==136 else version}_20261008')"
    assert text.count(before)==1;text=text.replace(before,after)
    target=A/'monitor_actual_chronological_optimization_progress_v22_20261008.py';assert not target.exists()
    compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    observer=start('actual_chronological_optimization_progress_observer_v22_20261008',target.name,[],{str(target):sha(target)})
    create(A/'actual_chronological_optimization_progress_observer_v22_hidden_launch_20261008.json',observer)
    print(json.dumps({'dispatch_worker':row['owned_worker_pid'],'observer_worker':observer['owned_worker_pid']}),flush=True)
if __name__=='__main__':main()
