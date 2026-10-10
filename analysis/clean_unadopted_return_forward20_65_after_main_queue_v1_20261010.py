"""Reclaim scratch space only after complete actual scores and verified main receipts."""
from pathlib import Path
import sys,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,owned,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    for name in ('actual_Return_after163_65_completion_main_v17_20261010','actual_forward20_qualified_screen_and_main_queue_v1_20261010'):
        p=A/'service_owned_workflows_20261006'/name
        while allowed():
            if (p/'service_execution.json').exists() and not owned(read(p/'native_launch.json')):
                assert read(p/'service_execution.json')['status']=='passed',read(p/'service_execution.json');break
            time.sleep(15)
        if not allowed():return
    for family in ('Return','Forward20'):
        p=Path('E:/赛题五_本机临时')/(family+'_after163_high_impact65_screen_v1_20261010')/'verification.json'
        if read(p)['best']['case']!=0:
            create(A/'new65_cleanup_deferred_for_improved_candidate_v1_20261010.json',{'status':'retain_scratch_after_potential_improvement_for_full_qualification','family':family});return
    import cleanup_completed_return_forward20_65_csv_v1_20261010 as cleanup
    cleanup.main()
if __name__=='__main__':main()
