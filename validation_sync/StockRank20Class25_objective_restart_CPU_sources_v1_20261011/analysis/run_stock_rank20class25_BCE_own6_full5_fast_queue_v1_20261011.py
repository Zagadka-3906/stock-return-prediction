from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from start_fast_completed_owned_service_v1_20261011 import start_service
def main():
 assert allowed()
 for name,driver in [('actual_stock_rank20class25_balanced_BCE_CPU_v1_20261011','verify_stock_rank20class25_balanced_BCE_actual_CPU_v1_20261011.py'),('StockRank20Class25Embedding_actual_mature_fixture_CPU_v1_20261011','verify_rank20class25_reused_actual_mature_fixture_gate_v1_20261011.py'),('actual_stock_rank20class25_embedding_small512_restart_v1_20261011','verify_stock_rank20class25_embedding_small512_restart_v1_20261011.py'),('StockRank20Class25EmbeddingSmall512_independent_small_CPU_v1_20261011','verify_stock_rank20class25_embedding_small512_small_CPU_v1_20261011.py'),('actual_stock_rank20class25_embedding_small512_bank6_v1_20261011','train_stock_rank20class25_embedding_small512_BF16_bank6_own64_v1_20261011.py'),('StockRank20Class25EmbeddingSmall512_independent_full5_GPU_controls_v1_20261011','verify_stock_rank20class25_embedding_small512_full5_independent_v1_20261011.py')]:
  if 'restart_' in driver:closed('actual_stock_rank20class10_embedding_six_state_native42_v1_20261011')
  assert allowed();p=A/driver;r=start_service(name,driver,[],{str(p):sha(p)});create(A/(name+'_activation.json'),r);closed(name)
if __name__=='__main__':main()
