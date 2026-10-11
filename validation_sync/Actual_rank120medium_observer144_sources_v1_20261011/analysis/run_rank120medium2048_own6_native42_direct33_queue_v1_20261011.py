from pathlib import Path
import sys,time,psutil
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from start_fast_completed_owned_service_v1_20261011 import start_service
def busy():
 for d in (A/'service_owned_workflows_20261006').glob('*selected_candidate_preparation*'):
  p=d/'native_launch.json'
  if p.exists() and owned(read(p)):return True
 return False
def main():
 assert allowed();closed('actual_rank60medium2048_gain_selected_full_candidate_queue_v1_20261011')
 for name,driver in [('actual_stock_rank120medium_embedding_medium2048_restart_v1_20261011', 'verify_stock_rank120medium_embedding_medium2048_restart_v1_20261011.py'), ('StockRank120MediumEmbeddingMedium2048_independent_small_CPU_v1_20261011', 'verify_stock_rank120medium_embedding_medium2048_small_CPU_v1_20261011.py'), ('actual_stock_rank120medium_embedding_medium2048_bank6_v1_20261011', 'train_stock_rank120medium_embedding_medium2048_BF16_bank6_own64_v1_20261011.py'), ('StockRank120MediumEmbeddingMedium2048_independent_full5_GPU_controls_v1_20261011', 'verify_stock_rank120medium_embedding_medium2048_full5_independent_v1_20261011.py'), ('actual_stock_rank120medium_embedding_six_state_native42_v1_20261011', 'verify_stock_rank120medium_embedding_six_state_native42_v1_20261011.py'), ('actual_stock_rank120medium_embedding_after183_direct_allocation33_v1_20261011', 'run_stock_rank120medium_embedding_after183_direct_allocation33_v1_20261011.py')]:
  if 'restart_' in driver or driver.startswith('train_') or 'full5_' in driver or 'native42_' in driver:
   while busy() or psutil.virtual_memory().available<12*2**30:
    assert allowed();time.sleep(10)
  assert allowed();p=A/driver;i=start_service(name,driver,[],{str(p):sha(p),str(A/'stock_rank120medium2048_own6_full5_native42_direct33_predeclared_sources_v1_20261011.json'):sha(A/'stock_rank120medium2048_own6_full5_native42_direct33_predeclared_sources_v1_20261011.json')});create(A/(name+'_activation.json'),i);closed(name)
if __name__=='__main__':main()
