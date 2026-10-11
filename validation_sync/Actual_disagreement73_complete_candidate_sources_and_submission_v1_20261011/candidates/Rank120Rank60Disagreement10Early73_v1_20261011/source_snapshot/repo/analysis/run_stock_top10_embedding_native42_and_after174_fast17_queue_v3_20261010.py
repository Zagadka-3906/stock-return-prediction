from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from handoff_ready_goss_full_execution_20261006 import start_service
def main():
    assert allowed();closed('actual_stock_top10_embedding_own_training_queue_v3_20261010')
    for p,d in read(A/'stock_top10_embedding_stage_and_after174_fast17_sources_admission_v2_20261010.json')['input_sha256'].items():assert sha(p)==d,p
    for name,driver in [('actual_stock_top10_embedding_six_state_native42_v1_20261010','verify_stock_top10_embedding_six_state_native42_v2_20261010.py'),('actual_stock_top10_embedding_after174_fast17_screen_v1_20261010','run_stock_top10_embedding_after174_fast17_screen_v1_20261010.py')]:
        assert allowed();p=A/driver;row=start_service(name,driver,[],{str(p):sha(p)});create(A/(name+'_activation.json'),row);closed(name)
if __name__=='__main__':main()
