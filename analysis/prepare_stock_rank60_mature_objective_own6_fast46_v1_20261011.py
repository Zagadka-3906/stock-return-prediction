from pathlib import Path
import sys,re,importlib
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
def renamed(s):
 for old,new in [('stock_rank10','stock_rank60'),('StockRank10','StockRank60'),('rank10','rank60'),('Rank10','Rank60'),('forward10','forward60'),('y_rank_10mean','y_rank_60mean'),('y_ret_10mean','y_ret_60mean'),('label_end_10d','label_end_60d'),('_calendar10','_calendar60'),('ten_day','sixty_day'),('mean10_tied','mean60_tied')]:s=s.replace(old,new)
 s=s.replace("'label_horizon_trading_days':10","'label_horizon_trading_days':60").replace("'label_horizon_trading_days': 10","'label_horizon_trading_days': 60").replace("['label_horizon_trading_days']==10","['label_horizon_trading_days']==60").replace("['label_horizon_trading_days'] == 10","['label_horizon_trading_days'] == 60")
 return s
def save(p,s):
 assert not p.exists(),p;compile(s,str(p),'exec');p.write_text(s,encoding='utf8',newline='\n');return p
def main():
 assert allowed();inputs=[];outputs=[]
 files=['forward10_mature_training_labels_v2_20261011.py','recent252_rank10_mature_training_population_v2_20261011.py','verify_recent252_rank10_mature_population_v2_20261011.py','stock_rank10_embedding_small512_BF16_native_v1_20261011.py','stock_rank10_embedding_saved_tensor_decoder_v1_20261011.py','verify_stock_rank10_embedding_actual_mature_fixture_v1_20261011.py','verify_stock_rank10_embedding_small512_restart_v1_20261011.py','verify_stock_rank10_embedding_small512_small_CPU_v1_20261011.py','train_stock_rank10_embedding_small512_BF16_bank6_own64_v1_20261011.py','verify_stock_rank10_embedding_small512_full5_independent_v1_20261011.py','stock_rank10_embedding_after_complete_qualified_parent_native_stage_v1_20261011.py','verify_stock_rank10_embedding_six_state_native42_v1_20261011.py','run_stock_rank10_embedding_after175_fast17_screen_v1_20261011.py','run_stock_rank10_embedding_after175_large_allocation29_screen_v1_20261011.py','predict_stock_rank10_embedding_complete_qualified_parent_scheme_v1_20261011.py','verify_stock_rank10_embedding_actual_eleven_parent_callbacks_CPU_v1_20261011.py']
 for name in files:
  p=A/name;inputs.append(p);s=renamed(p.read_text(encoding='utf8'))
  if name.startswith('forward10_'):s=s.replace('HORIZON=10','HORIZON=60')
  if name.startswith('verify_recent252_'):
   s=s.replace('(1,9,10,11,253,301,401)','(1,59,60,61,253,301,401)');s=re.sub(r'(?<!\d)10(?!\d)','60',s)
  assert 'y_rank_10mean' not in s and 'label_end_10d' not in s and 'stock_rank10' not in s,name
  outputs.append(save(A/renamed(name),s))
 native=importlib.import_module('stock_rank60_embedding_small512_BF16_native_v1_20261011');assert native.CONFIG['target']=='y_rank_60mean' and native.CONFIG['label_horizon_trading_days']==60 and native.CONFIG['training_calendar_window']==252
 labels=importlib.import_module('forward60_mature_training_labels_v2_20261011');assert labels.HORIZON==60 and labels.TARGET=='y_ret_60mean'
 pins={str(p):sha(p) for p in [Path(__file__),*inputs,*outputs]}
 create(A/'stock_rank60_embedding_own64_native_sources_preparation_v1_20261011.json',{'status':'compiled_genuinely_new_mature60_rank_objective_before_CPU_fixture_or_any_fit','configuration':native.CONFIG,'input_sha256':pins,'fresh_weights_required':True,'label_end_exclusive_calendar_horizon':60,'new_fits':0,'new_scores':0,'test_labels_read':False})
 for name in ['stock_rank60_embedding_actual_restart_and_own6_sources_admission_v1_20261011.json','stock_rank60_embedding_native_stage_and_fast17_sources_admission_v1_20261011.json']:
  create(A/name,{'status':'compiled_actual_source_routes_for_mature60_before_real_independent_controls','input_sha256':pins,'new_fits':0,'new_scores':0,'label_horizon_trading_days':60,'expected_bank_years':[2020,2021,2022,2023,2024,2025],'actual_future_X_read':False,'test_labels_read':False})
 tasks=[('actual_recent252_rank60_mature_population_CPU_v2_20261011','verify_recent252_rank60_mature_population_v2_20261011.py'),('StockRank60Embedding_actual_mature_fixture_CPU_v1_20261011','verify_stock_rank60_embedding_actual_mature_fixture_v1_20261011.py'),('actual_stock_rank60_embedding_small512_restart_v1_20261011','verify_stock_rank60_embedding_small512_restart_v1_20261011.py'),('StockRank60EmbeddingSmall512_independent_small_CPU_v1_20261011','verify_stock_rank60_embedding_small512_small_CPU_v1_20261011.py'),('actual_stock_rank60_embedding_small512_bank6_v1_20261011','train_stock_rank60_embedding_small512_BF16_bank6_own64_v1_20261011.py'),('StockRank60EmbeddingSmall512_independent_full5_GPU_controls_v1_20261011','verify_stock_rank60_embedding_small512_full5_independent_v1_20261011.py')]
 q=save(A/'run_stock_rank60_mature_objective_CPU_fixture_own6_full5_queue_v1_20261011.py',"from pathlib import Path\nimport sys\nA=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]\nfrom run_dependency_queue_v3_20261006 import sha,create\nfrom prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed\nfrom start_fast_completed_owned_service_v1_20261011 import start_service\ndef main():\n assert allowed()\n for name,driver in "+repr(tasks)+":\n  if 'restart_' in driver:closed('actual_stock_rank20class25_embedding_six_state_native42_v1_20261011')\n  assert allowed();p=A/driver;r=start_service(name,driver,[],{str(p):sha(p)});create(A/(name+'_activation.json'),r);closed(name)\nif __name__=='__main__':main()\n")
 oldscore=A/'run_stock_rank20class25_native42_and_fast46_queue_v1_20261011.py';s=oldscore.read_text(encoding='utf8').replace('stock_rank20class25','stock_rank60').replace('StockRank20Class25','StockRank60').replace("closed('actual_stock_rank20class10_embedding_after183_exact_latest_anchor17_v1_20261011')","closed('actual_stock_rank20class25_embedding_after175_large_allocation29_screen_v1_20261011')");scoreq=save(A/'run_stock_rank60_native42_and_fast46_queue_v1_20261011.py',s)
 admission=A/'stock_rank60_new60_horizon_source_pipeline_admission_v1_20261011.json';create(admission,{'status':'compiled_true60_strict_calendar_maturity_CPU7_fixture49153_own6_full5_native42_and_official46_before_any_controls','input_sha256':{**pins,str(q):sha(q),str(scoreq):sha(scoreq)},'new_fits':0,'new_scores':0,'test_labels_read':False})
 for name,p in [('actual_stock_rank60_mature_objective_own6_full5_queue_v1_20261011',q),('actual_stock_rank60_native42_and_fast46_queue_v1_20261011',scoreq),('actual_stock_rank60_embedding_eleven_parent_callbacks_CPU_v1_20261011',A/'verify_stock_rank60_embedding_actual_eleven_parent_callbacks_CPU_v1_20261011.py')]:
  assert allowed();r=start_service(name,p.name,[],{str(p):sha(p),str(admission):sha(admission)});create(A/(name+'_activation.json'),r)
 print({'genuinely_new60_horizon_pipeline_queued_before_real_controls':True,'no_future_data_or_answers_used':True},flush=True)
if __name__=='__main__':main()
