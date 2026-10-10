from pathlib import Path
import sys,re
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
def main():
 assert allowed();inputs=[];outputs=[]
 def renamed(text):
  return text.replace('stock_rank10','stock_rank20tail4').replace('StockRank10','StockRank20Tail4').replace('rank10mean','rank20mean').replace('Rank10Mean','Rank20Tail4Mean')
 for name in ['stock_rank10_embedding_after_complete_qualified_parent_native_stage_v1_20261011.py','verify_stock_rank10_embedding_six_state_native42_v1_20261011.py','run_stock_rank10_embedding_after175_fast17_screen_v1_20261011.py','run_stock_rank10_embedding_after175_large_allocation29_screen_v1_20261011.py']:
  p=A/name;inputs.append(p);q=A/renamed(name);assert not q.exists();text=renamed(p.read_text(encoding='utf8'));compile(text,str(q),'exec');q.write_text(text,encoding='utf8',newline='\n');outputs.append(q)
 proof=A/'stock_rank20tail4_embedding_native_stage_and_fast17_sources_admission_v1_20261011.json'
 create(proof,{'status':'compiled_new_upper15_weighted_rank20_native42_cold42_refusal7_and17_29_official_sources_before_any_own_annual_completion','input_sha256':{str(p):sha(p) for p in [Path(__file__),*inputs,*outputs,A/'stock_rank20tail4_weighted_Huber_actual_CPU_controls_v1_20261011.json',A/'stock_rank20tail4_restart_and_own6_sources_admission_v1_20261011.json']},'expected_native':42,'expected_cold':42,'expected_prefit':7,'new_official_cases':[17,29],'new_fits':0,'new_scores':0,'test_labels_read':False,'actual_future_X_read':False})
 queue=A/'run_stock_rank20tail4_native42_and_fast46_queue_v1_20261011.py';assert not queue.exists()
 text=(A/'run_stock_rank10_native42_and_fast46_queue_v1_20261011.py').read_text(encoding='utf8');text=renamed(text);compile(text,str(queue),'exec');queue.write_text(text,encoding='utf8',newline='\n')
 r=start_service('actual_stock_rank20tail4_native42_and_fast46_queue_v1_20261011',queue.name,[],{str(queue):sha(queue),str(proof):sha(proof)});create(A/'actual_stock_rank20tail4_native42_and_fast46_activation_v1_20261011.json',r)
 print({'new_rank20_upper15_weighted_training_native42_official46_queue_dispatched':True},flush=True)
if __name__=='__main__':main()
