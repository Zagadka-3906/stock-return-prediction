from pathlib import Path
import sys,importlib
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
def renamed(s):return s.replace('stock_rank20class10','stock_rank20class25').replace('StockRank20Class10','StockRank20Class25').replace('rank20class10','rank20class25').replace('Rank20Class10','Rank20Class25').replace('top10_binary','top25_binary').replace('Top10_positive','Top25_positive')
def main():
 assert allowed();inputs=[];outputs=[]
 files=['stock_rank20class10_embedding_small512_BF16_native_v1_20261011.py','stock_rank20class10_embedding_saved_tensor_decoder_v1_20261011.py','verify_stock_rank20class10_balanced_BCE_actual_CPU_v1_20261011.py','verify_rank20class10_reused_actual_mature_fixture_gate_v1_20261011.py','verify_stock_rank20class10_embedding_small512_restart_v1_20261011.py','verify_stock_rank20class10_embedding_small512_small_CPU_v1_20261011.py','train_stock_rank20class10_embedding_small512_BF16_bank6_own64_v1_20261011.py','verify_stock_rank20class10_embedding_small512_full5_independent_v1_20261011.py','stock_rank20class10_embedding_after_complete_qualified_parent_native_stage_v1_20261011.py','verify_stock_rank20class10_embedding_six_state_native42_v1_20261011.py','run_stock_rank20class10_embedding_after175_fast17_screen_v1_20261011.py','run_stock_rank20class10_embedding_after175_large_allocation29_screen_v1_20261011.py','predict_stock_rank20class10_embedding_complete_qualified_parent_scheme_v1_20261011.py','verify_stock_rank20class10_embedding_actual_eleven_parent_callbacks_CPU_v1_20261011.py']
 for filename in files:
  p=A/filename;q=A/renamed(filename);assert not q.exists();inputs.append(p);s=renamed(p.read_text(encoding='utf8'))
  if filename.startswith('stock_rank20class10_embedding_small512_BF16_native'):
   s=s.replace("'classification_raw_rank_threshold': .9","'classification_raw_rank_threshold': .75").replace("'positive_class_weight': 9.","'positive_class_weight': 3.").replace("cfg['classification_raw_rank_threshold']==.9","cfg['classification_raw_rank_threshold']==.75").replace("cfg['positive_class_weight']==9.","cfg['positive_class_weight']==3.").replace('target.float()>=.4','target.float()>=.25').replace('pred.new_tensor(9.','pred.new_tensor(3.')
   assert 'target.float()>=.25' in s and 'new_tensor(9.' not in s
  if filename.startswith('verify_stock_rank20class10_balanced_BCE_actual_CPU'):
   s=s.replace('.399,.4,.401','.249,.25,.251').replace('np.float32(.4)','np.float32(.25)').replace('labels==1.,9.,1.','labels==1.,3.,1.').replace("'raw_rank_threshold':.9","'raw_rank_threshold':.75").replace("'positive_weight':9.","'positive_weight':3.")
  compile(s,str(q),'exec');q.write_text(s,encoding='utf8',newline='\n');outputs.append(q)
 native=importlib.import_module('stock_rank20class25_embedding_small512_BF16_native_v1_20261011');assert native.CONFIG['classification_raw_rank_threshold']==.75 and native.CONFIG['positive_class_weight']==3. and native.CONFIG['label_horizon_trading_days']==20
 pins={str(p):sha(p) for p in [Path(__file__),*inputs,*outputs]}
 for name in ('stock_rank20class25_own64_native_sources_preparation_v1_20261011.json','stock_rank20class25_embedding_own64_native_sources_preparation_v1_20261011.json'):
  create(A/name,{'status':'compiled_fresh_mature20_top25_binary_objective_before_any_fit','configuration':native.CONFIG,'input_sha256':pins,'new_fits':0,'new_scores':0,'fresh_weights_required':True,'provided_mature_rank20_population_reused_unchanged':True,'test_labels_read':False})
 admission=A/'stock_rank20class25_BCE_own6_sources_admission_v1_20261011.json';create(admission,{'status':'compiled_genuinely_new_top25_objective_before_CPU_and_restart_training_controls','input_sha256':pins,'raw_rank_label_horizon':20,'classification_Top_fraction':.25,'positive_class_weight':3.,'new_fits':0,'new_scores':0,'test_labels_read':False})
 stageproof=A/'stock_rank20class25_embedding_native_stage_and_fast17_sources_admission_v1_20261011.json';create(stageproof,{'status':'compiled_top25_native42_cold42_prefit7_and_official46_before_real_checks','input_sha256':{**pins,str(admission):sha(admission)},'expected_native_and_cold':[42,42],'expected_prefit':7,'expected_scored_records':[17,29],'new_fits':0,'new_scores':0,'test_labels_read':False})
 old=A/'run_stock_rank20class10_BCE_own6_full5_fast_queue_v1_20261011.py';q=A/renamed(old.name);assert not q.exists();s=renamed(old.read_text(encoding='utf8'))
 s=s.replace("assert allowed();closed('actual_stock_rank20tail4_embedding_six_state_native42_v1_20261011')","assert allowed()")
 s=s.replace("  assert allowed();p=A/driver;","  if 'restart_' in driver:closed('actual_stock_rank20class10_embedding_six_state_native42_v1_20261011')\n  assert allowed();p=A/driver;")
 compile(s,str(q),'exec');q.write_text(s,encoding='utf8',newline='\n')
 oldscore=A/'run_stock_rank20class10_native42_and_fast46_queue_v1_20261011.py';scoring=A/renamed(oldscore.name);assert not scoring.exists();s=renamed(oldscore.read_text(encoding='utf8')).replace("closed('actual_stock_rank20tail4_embedding_after175_large_allocation29_screen_v1_20261011')","closed('actual_stock_rank20class10_embedding_after183_exact_latest_anchor17_v1_20261011')");compile(s,str(scoring),'exec');scoring.write_text(s,encoding='utf8',newline='\n')
 for name,p in [('actual_stock_rank20class25_BCE_own6_full5_queue_v1_20261011',q),('actual_stock_rank20class25_native42_and_fast46_queue_v1_20261011',scoring),('actual_stock_rank20class25_embedding_eleven_parent_callbacks_CPU_v1_20261011',A/'verify_stock_rank20class25_embedding_actual_eleven_parent_callbacks_CPU_v1_20261011.py')]:
  assert allowed();row=start_service(name,p.name,[],{str(p):sha(p),str(admission):sha(admission),str(stageproof):sha(stageproof)});create(A/(name+'_activation.json'),row)
 print({'new_top25_BCE_CPU_restart_own6_full5_native42_official46_queued':True,'fresh_weights':True,'actual_scores_pending':True},flush=True)
if __name__=='__main__':main()
