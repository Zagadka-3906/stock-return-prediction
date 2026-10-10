from pathlib import Path
import sys,importlib
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
from prepare_stock_rank20class10_BCE_own6_fast46_v1_20261011 import renamed
def main():
 assert allowed();inputs=[];outputs=[]
 for n in ['stock_rank20tail4_embedding_after_complete_qualified_parent_native_stage_v1_20261011.py','verify_stock_rank20tail4_embedding_six_state_native42_v1_20261011.py','run_stock_rank20tail4_embedding_after175_fast17_screen_v1_20261011.py','run_stock_rank20tail4_embedding_after175_large_allocation29_screen_v1_20261011.py','predict_stock_rank20tail4_embedding_complete_qualified_parent_scheme_v1_20261011.py','verify_stock_rank20tail4_embedding_actual_eleven_parent_callbacks_CPU_v1_20261011.py']:
  p=A/n;inputs.append(p);q=A/renamed(n);assert not q.exists();s=renamed(p.read_text(encoding='utf8'));compile(s,str(q),'exec');q.write_text(s,encoding='utf8',newline='\n');outputs.append(q)
 proof=A/'stock_rank20class10_embedding_native_stage_and_fast17_sources_admission_v1_20261011.json'
 create(proof,{'status':'compiled_new_mature20_top10_binary_BCE_native42_cold42_refusal7_and46_scoring_sources_before_training_completion','input_sha256':{str(p):sha(p) for p in [Path(__file__),*inputs,*outputs,A/'stock_rank20class10_BCE_own6_sources_admission_v1_20261011.json',A/'stock_rank20class10_balanced_BCE_actual_CPU_controls_v1_20261011.json']},'new_fits':0,'new_scores':0,'expected_native_and_cold':[42,42],'expected_prefit':7,'expected_scored_records':[17,29],'raw_rank_label_horizon':20,'classification_Top_fraction':.1,'test_labels_read':False,'actual_future_X_read':False})
 p=A/'run_stock_rank20tail4_native42_and_fast46_queue_v1_20261011.py';queue=A/renamed(p.name);assert not queue.exists();s=renamed(p.read_text(encoding='utf8'))
 # Keep native checks ready as soon as the annual bank completes; serialize new CPU scoring behind weighted46.
 s=s.replace("  assert allowed();p=A/driver;", "  if 'screen_' in driver:closed('actual_stock_rank20tail4_embedding_after175_large_allocation29_screen_v1_20261011')\n  assert allowed();p=A/driver;")
 compile(s,str(queue),'exec');queue.write_text(s,encoding='utf8',newline='\n')
 for name,driver in [('actual_stock_rank20class10_native42_and_fast46_queue_v1_20261011',queue.name),('actual_stock_rank20class10_embedding_eleven_parent_callbacks_CPU_v1_20261011','verify_stock_rank20class10_embedding_actual_eleven_parent_callbacks_CPU_v1_20261011.py')]:
  assert allowed();p=A/driver;r=start_service(name,driver,[],{str(p):sha(p),str(proof):sha(proof)});create(A/(name+'_activation.json'),r)
 create(A/'stock_rank20class10_prospective_complete195_direction_plan_v1_20261011.json',{'status':'predeclared_new_mature20_top10_BCE_own6_native42_official46_before_full195_sources','anchors':[175,194],'expected_complete_records':48,'prospective_round':195,'prospective_QA':106,'prospective_full_board':17948,'prospective_wave':478,'official46_and_full195_not_completed':True,'selection_uses_training_only_continuous2020_2024_S':True,'deadline':'2026-10-11T13:00:00+08:00','new_fits_by_plan':0,'new_scores_by_plan':0,'test_labels_read':False})
 print({'classifier_native42_scoring46_and_CPU11_queued':True,'future195_not_created':True},flush=True)
if __name__=='__main__':main()
