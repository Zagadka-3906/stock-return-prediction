from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from start_fast_completed_owned_service_v1_20261011 import start_service
def main():
    assert allowed();closed('StockRank10Embedding_actual_mature_fixture_CPU_v1_20261011')
    closed('actual183_completed_inner_inference_rehashed_recovery_v1_20261011')
    proof=A/'stock_rank10_embedding_actual_restart_and_own6_sources_admission_v1_20261011.json'
    for p,d in read(proof)['input_sha256'].items():assert sha(p)==d,p
    for name,driver in [('actual_stock_rank10_embedding_small512_restart_v1_20261011', 'verify_stock_rank10_embedding_small512_restart_v1_20261011.py'), ('StockRank10EmbeddingSmall512_independent_small_CPU_v1_20261011', 'verify_stock_rank10_embedding_small512_small_CPU_v1_20261011.py'), ('actual_stock_rank10_embedding_small512_bank6_v1_20261011', 'train_stock_rank10_embedding_small512_BF16_bank6_own64_v1_20261011.py'), ('StockRank10EmbeddingSmall512_independent_full5_GPU_controls_v1_20261011', 'verify_stock_rank10_embedding_small512_full5_independent_v1_20261011.py')]:
        assert allowed();p=A/driver;r=start_service(name,driver,[],{str(p):sha(p),str(proof):sha(proof)})
        create(A/(name+'_activation.json'),r);closed(name)
    print({'actual_rank10_own6_and_independentfull5_complete':True},flush=True)
if __name__=='__main__':main()
