from pathlib import Path
import sys,time,psutil
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from start_fast_completed_owned_service_v1_20261011 import start_service
def candidate_busy():
 for folder in (A/'service_owned_workflows_20261006').glob('*selected_candidate_preparation*'):
  p=folder/'native_launch.json'
  if p.exists() and owned(read(p)):return True
 return False
def main():
 assert allowed()
 for name,driver in [('StockRank120Embedding_actual_mature_fixture_CPU_v1_20261011', 'verify_stock_rank120_embedding_actual_mature_fixture_v1_20261011.py'), ('StockRank120EmbeddingSmall512_independent_small_CPU_v1_20261011', 'verify_stock_rank120_embedding_small512_small_CPU_v1_20261011.py'), ('actual_stock_rank120_embedding_small512_restart_v1_20261011', 'verify_stock_rank120_embedding_small512_restart_v1_20261011.py'), ('actual_stock_rank120_embedding_small512_bank6_v1_20261011', 'train_stock_rank120_embedding_small512_BF16_bank6_own64_v1_20261011.py'), ('StockRank120EmbeddingSmall512_independent_full5_GPU_controls_v1_20261011', 'verify_stock_rank120_embedding_small512_full5_independent_v1_20261011.py'), ('actual_stock_rank120_embedding_six_state_native42_v1_20261011', 'verify_stock_rank120_embedding_six_state_native42_v1_20261011.py'), ('actual_stock_rank120_embedding_after183_direct_allocation33_v1_20261011', 'run_stock_rank120_embedding_after183_direct_allocation33_v1_20261011.py')]:
  if 'restart_' in driver or driver.startswith('train_'):
   while candidate_busy() or psutil.virtual_memory().available<12*2**30:
    assert allowed();time.sleep(10)
  assert allowed();p=A/driver;r=start_service(name,driver,[],{str(p):sha(p)});create(A/(name+'_activation.json'),r);closed(name)
if __name__=='__main__':main()
