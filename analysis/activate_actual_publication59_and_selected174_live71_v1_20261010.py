from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from handoff_ready_goss_full_execution_20261006 import start_service,retire
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed();source=A/'monitor_fast_optimization_v70_20261010.py'
    text=source.read_text(encoding='utf8').replace('progress_v70','progress_v71').replace('handoff_v121','handoff_v122').replace('rankings_v42','rankings_v43')
    jobs=['actual_Dual25_recovery_dependencies_main_v59_20261010','StockRankDual174_selected_candidate_preparation_v1_20261010','StockRankDual174_selected_candidate_sealing_v1_20261010','StockRankDual174_round174_full_registration_v1_20261010']
    text=text.replace('    while True:\n','    jobs += '+repr(jobs)+'\n    while True:\n')
    p=A/'monitor_fast_optimization_v71_20261010.py';assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n')
    retire(read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_v70_20261010/native_launch.json'),'Replace childless observer70 with71 including actual publication59 and full174 selected stages')
    assert allowed();row=start_service('actual_fast_optimization_progress_v71_20261010',p.name,[],{str(p):sha(p)});create(A/'actual_fast_optimization_progress_v71_20261010_activation.json',row)
    print('live71 started',flush=True)
if __name__=='__main__':main()
