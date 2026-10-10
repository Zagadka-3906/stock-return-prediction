"""Two independent TRAIN score streams; original scientific drivers stay unchanged."""
from pathlib import Path
import sys,time,psutil
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from start_fast_completed_owned_service_v1_20261011 import start_service
def main():
 assert allowed()
 for name in ('StockRank60EmbeddingSmall512_independent_full5_GPU_controls_v1_20261011','actual_stock_rank60_embedding_six_state_native42_v1_20261011'):
  closed(name)
 for name,driver in [('actual_stock_rank60_embedding_after175_fast17_screen_v1_20261011','run_stock_rank60_embedding_after175_fast17_screen_v1_20261011.py'),('actual_stock_rank60_embedding_after175_large_allocation29_screen_v1_20261011','run_stock_rank60_embedding_after175_large_allocation29_screen_v1_20261011.py')]:
  while psutil.virtual_memory().available<16*2**30:
   assert allowed();time.sleep(10)
  assert allowed();p=A/driver
  row=start_service(name,driver,[],{str(p):sha(p),str(Path(__file__)):sha(__file__)})
  create(A/(name+'_activation.json'),row);closed(name)
if __name__=='__main__':main()
