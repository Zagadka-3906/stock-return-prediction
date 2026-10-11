from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from start_fast_completed_owned_service_v1_20261011 import start_service
def main():
 assert allowed();closed('StockRank20Class25EmbeddingSmall512_independent_full5_GPU_controls_v1_20261011')
 for name,driver in [('actual_stock_rank20class25_embedding_six_state_native42_v1_20261011','verify_stock_rank20class25_embedding_six_state_native42_v1_20261011.py'),('actual_stock_rank20class25_embedding_after175_fast17_screen_v1_20261011','run_stock_rank20class25_embedding_after175_fast17_screen_v1_20261011.py'),('actual_stock_rank20class25_embedding_after175_large_allocation29_screen_v1_20261011','run_stock_rank20class25_embedding_after175_large_allocation29_screen_v1_20261011.py')]:
  if 'screen_' in driver:closed('actual_stock_rank20class10_embedding_after183_exact_latest_anchor17_v1_20261011')
  assert allowed();p=A/driver;r=start_service(name,driver,[],{str(p):sha(p)});create(A/(name+'_activation.json'),r);closed(name)
if __name__=='__main__':main()
