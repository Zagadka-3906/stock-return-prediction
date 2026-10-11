"""Dispatch only missing unique helpers; never rerun an existing native handle."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
def main():
    assert allowed();path=A/'Dual25_verified_recovery_exact_dependency_aliases_v4_20261010.json';proof=read(path)
    inverse={v:k for vnum in (1,2) for k,v in read(A/f'Dual25_verified_recovery_exact_dependency_aliases_v{vnum}_20261010.json')['driver_wrappers'].items()}
    tasks={}
    for original in proof['selected_helpers']:
        name=proof['service_aliases'][original];definition=read(A/'service_owned_workflows_20261006'/original/'job_definition.json');driver=Path(definition['driver']).name;driver=inverse.get(driver,driver);wrapper=proof['driver_wrappers'][driver]
        assert name not in tasks or tasks[name]==wrapper,(name,wrapper,tasks.get(name));tasks[name]=wrapper
    started=[];retained=[]
    for name,driver in tasks.items():
        assert allowed();folder=A/'service_owned_workflows_20261006'/name
        if folder.exists():
            row=read(folder/'native_launch.json');terminal=read(folder/'service_execution.json') if (folder/'service_execution.json').exists() else {}
            assert owned(row) or terminal.get('status')=='passed',(name,terminal)
            retained.append({'name':name,'live_verified':owned(row),'terminal':terminal.get('status')});continue
        row=start_service(name,driver,[],{str(A/driver):sha(A/driver),str(path):sha(path)});create(A/(name+'_activation.json'),row);started.append(name)
    create(A/'actual_registration_recovery_v4_remaining_dependency_dispatch_v1_20261010.json',{'status':'dispatched_only_missing_unique_dependency_helpers_existing_handles_retained','new_helpers':started,'retained_actual_handles':retained,'unique_helper_tasks':len(tasks),'new_quality_scores':0,'test_labels_read':False})
    print({'remaining_helpers_started':len(started),'existing_handles_retained':len(retained)},flush=True)
if __name__=='__main__':main()
