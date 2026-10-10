from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from handoff_ready_goss_full_execution_20261006 import start_service
def main():
    assert allowed();closed('StockRankDual174_selected_candidate_sealing_v1_20261010')
    proof=read(A/'stock_top10_embedding_own_sources_admission_v2_20261010.json')
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    tasks=[('actual_stock_top10_embedding_small512_restart_v1_20261010','verify_stock_top10_embedding_small512_restart_priority174_v2_20261010.py'),('StockTop10EmbeddingSmall512_independent_small_CPU_v1_20261009','verify_stock_top10_embedding_small512_small_CPU_v2_20261010.py'),('actual_stock_top10_embedding_small512_bank6_v1_20261010','train_stock_top10_embedding_small512_BF16_bank6_checkpoint_yield_priority174_v2_20261010.py'),('StockTop10EmbeddingSmall512_independent_full5_GPU_controls_v1_20261009','verify_stock_top10_embedding_small512_full5_independent_v2_20261010.py')]
    for name,driver in tasks:
        assert allowed();p=A/driver;row=start_service(name,driver,[],{str(p):sha(p)});create(A/(name+'_activation.json'),row);closed(name)
if __name__=='__main__':main()
