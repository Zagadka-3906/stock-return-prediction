from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A),str(A.parent)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def main():
    assert allowed()
    source=A/'reconcile_completed_priority_screen_pointer_v1_20261010.py'
    text=source.read_text(encoding='utf8').replace('location_reconciliation_v1_20261010','location_reconciliation_v2_20261010')
    before='    collision="FileExistsError: [Errno 17] File exists: \'+str(A/\'actual_high_impact_cumulative_screen_location_v1_20261010.json\')+"\'"'
    lines=text.splitlines()
    indexes=[i for i,line in enumerate(lines) if line.lstrip().startswith('collision=')];assert len(indexes)==1
    lines[indexes[0]]='    collision="FileExistsError: [Errno 17] File exists: "+repr(str(A/"actual_high_impact_cumulative_screen_location_v1_20261010.json"))'
    text='\n'.join(lines)+'\n';target=A/'reconcile_completed_priority_screen_pointer_v2_20261010.py'
    assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    pins={str(target):sha(target),str(A/'run_protected162_complete_family_v1_20261010.py'):sha(A/'run_protected162_complete_family_v1_20261010.py')}
    for family,tag in [('cumulative','high_impact_cumulative_screen_v2_20261010'),('official_top','protected_official_top_screen_v2_20261010')]:
        name='actual_'+tag+'_location_reconciliation_v2_20261010'
        try:row=start_service(name,target.name,[family],pins)
        except AssertionError:
            folder=A/'service_owned_workflows_20261006'/name;row=read(folder/'native_launch.json')
            assert not owned(row) and read(folder/'service_execution.json')['status']=='passed'
        create(A/(tag+'_location_reconciliation_hidden_launch_v2_20261010.json'),row)
        print(family,row['owned_worker_pid'],flush=True)

if __name__=='__main__':main()
