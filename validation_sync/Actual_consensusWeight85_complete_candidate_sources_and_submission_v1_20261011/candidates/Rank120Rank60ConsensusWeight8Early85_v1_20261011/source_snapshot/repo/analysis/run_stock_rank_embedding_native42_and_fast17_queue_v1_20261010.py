from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from handoff_ready_goss_full_execution_20261006 import start_service
def main():
    assert allowed();closed('actual_stock_rank_embedding_own_training_queue_v2_20261010')
    proof=read(A/'stock_rank_embedding_native_stage_and_fast17_sources_admission_v1_20261010.json')
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    for name,source in [('actual_stock_rank_embedding_six_state_native42_v1_20261010','verify_stock_rank_embedding_six_state_native42_v1_20261010.py'),('actual_stock_rank_embedding_after170_fast17_screen_v1_20261010','run_stock_rank_embedding_after170_fast17_screen_v1_20261010.py')]:
        assert allowed();p=A/source;row=start_service(name,p.name,[],{str(p):sha(p)})
        create(A/(name+'_activation.json'),row);closed(name)
if __name__=='__main__':main()
