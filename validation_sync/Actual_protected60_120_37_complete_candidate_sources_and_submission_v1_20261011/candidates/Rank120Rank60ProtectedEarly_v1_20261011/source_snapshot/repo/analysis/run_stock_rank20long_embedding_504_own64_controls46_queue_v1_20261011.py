from pathlib import Path
import sys,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from handoff_ready_goss_full_execution_20261006 import start_service
def main():
    assert allowed();closed('StockRank20LongEmbedding_actual_mature_fixture_CPU_v1_20261010')
    closed('actual_rank20_two_seed_native84_v1_20261010')
    proof=A/'stock_rank20long_embedding_own64_native_sources_preparation_v1_20261010.json'
    for p,d in read(proof)['input_sha256'].items():assert sha(p)==d,p
    for name,driver in [('actual_stock_rank20long_embedding_small512_restart_v1_20261010', 'verify_stock_rank20long_embedding_small512_restart_v1_20261010.py'), ('StockRank20LongEmbeddingSmall512_independent_small_CPU_v1_20261009', 'verify_stock_rank20long_embedding_small512_small_CPU_v1_20261010.py'), ('actual_stock_rank20long_embedding_small512_bank6_v1_20261010', 'train_stock_rank20long_embedding_small512_BF16_bank6_own64_v1_20261010.py'), ('StockRank20LongEmbeddingSmall512_independent_full5_GPU_controls_v1_20261009', 'verify_stock_rank20long_embedding_small512_full5_independent_v1_20261010.py'), ('actual_stock_rank20long_embedding_six_state_native42_v1_20261010', 'verify_stock_rank20long_embedding_six_state_native42_v1_20261010.py'), ('actual_stock_rank20long_embedding_after175_fast17_screen_v1_20261010', 'run_stock_rank20long_embedding_after175_fast17_screen_v1_20261010.py'), ('actual_stock_rank20long_embedding_after175_large_allocation29_screen_v1_20261010', 'run_stock_rank20long_embedding_after175_large_allocation29_screen_v1_20261010.py')]:
        assert allowed();p=A/driver;row=start_service(name,driver,[],{str(p):sha(p),str(proof):sha(proof)})
        create(A/(name+'_activation.json'),row)
        while owned(row):assert allowed();time.sleep(15)
        assert read(A/'service_owned_workflows_20261006'/name/'service_execution.json')['status']=='passed',name
if __name__=='__main__':main()
