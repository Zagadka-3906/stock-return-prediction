from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
def main():
    for name,driver in [('actual_fast_optimization_progress_reboot_v94_20261011','monitor_reboot_optimization_v94_20261011.py'),('actual_reboot_routes_protected37_capsules_main_v1_20261011','publish_reboot_routes_protected37_capsules_main_v1_20261011.py')]:
        assert allowed();row=start_service(name,driver,[],{str(A/driver):sha(A/driver)});create(A/(name+'_activation.json'),row)
if __name__=='__main__':main()
