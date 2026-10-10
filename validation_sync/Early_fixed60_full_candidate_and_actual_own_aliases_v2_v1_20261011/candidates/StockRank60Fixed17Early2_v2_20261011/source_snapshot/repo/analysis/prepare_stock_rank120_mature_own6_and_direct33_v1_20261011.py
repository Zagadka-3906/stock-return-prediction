"""Explore a new120 target, strict maturity controls first, no larger network."""
from pathlib import Path
import sys,re,ast,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
def renamed(s):
 for old,new in [('stock_rank60','stock_rank120'),('StockRank60','StockRank120'),('rank60','rank120'),('Rank60','Rank120'),('forward60','forward120'),('y_rank_60mean','y_rank_120mean'),('y_ret_60mean','y_ret_120mean'),('label_end_60d','label_end_120d'),('_calendar60','_calendar120'),('mean60_tied','mean120_tied')]:s=s.replace(old,new)
 return re.sub(r'(?<!\d)60(?!\d)','120',s)
def save(name,s):
 p=A/name;assert not p.exists(),p;ast.parse(s);p.write_text(s,encoding='utf8');return p
def source_paths():
 proof=read(A/'stock_rank120_new120_pipeline_admission_v1_20261011.json')
 return [Path(__file__),A/'stock_rank120_new120_pipeline_admission_v1_20261011.json',*[Path(p) for p in proof['input_sha256']]]
def main():
 assert allowed();inputs=[];outputs=[]
 files=['forward60_mature_training_labels_v2_20261011.py','recent252_rank60_mature_training_population_v2_20261011.py','verify_recent252_rank60_mature_population_v2_20261011.py','verify_rank60_first_mature_boundary_and_gaps_CPU_v1_20261011.py','stock_rank60_embedding_small512_BF16_native_v1_20261011.py','stock_rank60_embedding_saved_tensor_decoder_v1_20261011.py','verify_stock_rank60_embedding_actual_mature_fixture_v1_20261011.py','verify_stock_rank60_embedding_small512_restart_v1_20261011.py','verify_stock_rank60_embedding_small512_small_CPU_v1_20261011.py','train_stock_rank60_embedding_small512_BF16_bank6_own64_v1_20261011.py','verify_stock_rank60_embedding_small512_full5_independent_v1_20261011.py','stock_rank60_embedding_after_complete_qualified_parent_native_stage_v1_20261011.py','stock_rank60_embedding_after_complete_qualified_parent_native_stage_v2_20261011.py','verify_stock_rank60_embedding_six_state_native42_v1_20261011.py','predict_stock_rank60_embedding_complete_qualified_parent_scheme_v2_20261011.py','verify_stock_rank60_actual_twelve_parent183_callbacks_CPU_v2_20261011.py','run_stock_rank60_embedding_after183_direct_allocation33_v1_20261011.py','run_publish_rank60_after183_completed33_main_v1_20261011.py']
 for n in files:
  p=A/n;inputs.append(p);s=p.read_text(encoding='utf8')
  if n.startswith('verify_recent252_'):s=s.replace('(1,59,60,61,253,301,401)','(1,119,120,121,253,301,401)')
  if n.startswith('verify_rank60_first_'):
   s=s.replace('range(1,91)','range(1,181)').replace('(61,62,63)','(121,122,123)').replace('cutoff==61','cutoff==121').replace('cutoff==62','cutoff==122').replace('=={61}','=={121}').replace('eligible62_strict61','eligible122_strict121')
  s=renamed(s)
  if n.startswith('run_stock_rank60_embedding_after183_'):
   # One new33 stream, after the corresponding original H60 stream; no unused120/175 screen.
   s=s.replace("closed('actual_stock_rank120_embedding_after175_large_allocation29_screen_v1_20261011')","closed('actual_stock_rank60_embedding_after183_direct_allocation33_v1_20261011')")
  outputs.append(save(renamed(n),s))
 native=importlib.import_module('stock_rank120_embedding_small512_BF16_native_v1_20261011')
 labels=importlib.import_module('forward120_mature_training_labels_v2_20261011')
 assert native.CONFIG['target']=='y_rank_120mean' and native.CONFIG['label_horizon_trading_days']==labels.HORIZON==120
 assert native.CONFIG['training_calendar_window']==252 and native.CONFIG['hidden']==[512,256,128] and native.CONFIG['epochs']==64
 cpu=importlib.import_module('verify_recent252_rank120_mature_population_v2_20261011');cpu.main()
 boundary=importlib.import_module('verify_rank120_first_mature_boundary_and_gaps_CPU_v1_20261011');boundary.main()
 callback=importlib.import_module('verify_stock_rank120_actual_twelve_parent183_callbacks_CPU_v2_20261011');callback.main()
 actualproofs=[A/n for n in ['recent252_rank120_mature_population_actual_CPU_controls_v2_20261011.json','rank120_first_mature_boundary_and_gaps_actual_CPU_controls_v1_20261011.json','stock_rank120_actual_twelve_parent183_callbacks_CPU_controls_v2_20261011.json']]
 assert [len(read(p)['records']) for p in actualproofs]==[7,12,12]
 pins={str(p):sha(p) for p in [Path(__file__),*inputs,*outputs,*actualproofs]}
 for n in ['stock_rank120_embedding_own64_native_sources_preparation_v1_20261011.json','stock_rank120_embedding_actual_restart_and_own6_sources_admission_v1_20261011.json','stock_rank120_embedding_native_stage_and_fast17_sources_admission_v1_20261011.json','stock_rank120_after183_direct33_predeclared_sources_v1_20261011.json']:
  create(A/n,{'status':'actual31_CPU_cases_passed_for_new120_before_GPU_fits_or_official_scores','input_sha256':pins,'configuration':native.CONFIG,'actual_CPU_maturity_cases':19,'actual_CPU_parent_callback_cases':12,'new_fits':0,'new_scores':0,'actual_future_X_read':False,'test_labels_read':False})
 tasks=[('StockRank120Embedding_actual_mature_fixture_CPU_v1_20261011','verify_stock_rank120_embedding_actual_mature_fixture_v1_20261011.py'),('StockRank120EmbeddingSmall512_independent_small_CPU_v1_20261011','verify_stock_rank120_embedding_small512_small_CPU_v1_20261011.py'),('actual_stock_rank120_embedding_small512_restart_v1_20261011','verify_stock_rank120_embedding_small512_restart_v1_20261011.py'),('actual_stock_rank120_embedding_small512_bank6_v1_20261011','train_stock_rank120_embedding_small512_BF16_bank6_own64_v1_20261011.py'),('StockRank120EmbeddingSmall512_independent_full5_GPU_controls_v1_20261011','verify_stock_rank120_embedding_small512_full5_independent_v1_20261011.py'),('actual_stock_rank120_embedding_six_state_native42_v1_20261011','verify_stock_rank120_embedding_six_state_native42_v1_20261011.py'),('actual_stock_rank120_embedding_after183_direct_allocation33_v1_20261011','run_stock_rank120_embedding_after183_direct_allocation33_v1_20261011.py')]
 queue='''from pathlib import Path
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
 for name,driver in TASKS:
  if 'restart_' in driver or driver.startswith('train_'):
   while candidate_busy() or psutil.virtual_memory().available<12*2**30:
    assert allowed();time.sleep(10)
  assert allowed();p=A/driver;r=start_service(name,driver,[],{str(p):sha(p)});create(A/(name+'_activation.json'),r);closed(name)
if __name__=='__main__':main()
'''.replace('TASKS',repr(tasks))
 q=save('run_stock_rank120_own6_full5_native42_and_direct33_queue_v1_20261011.py',queue)
 admission=A/'stock_rank120_new120_pipeline_admission_v1_20261011.json'
 create(admission,{'status':'actual31_independent_CPU_controls_passed_new120_own6_full5_native42_direct33_predeclared_before_fits','input_sha256':{**pins,str(q):sha(q)},'fresh_weights_required':True,'actual_CPU_cases':31,'expected_years':[2020,2021,2022,2023,2024,2025],'window_definition':'last252_past_calendar_origins_then_strict120_maturity_filter; not252 mature origins','expected_official_records':33,'new_fits':0,'new_scores':0,'test_labels_read':False})
 for name,p in [('actual_stock_rank120_own6_full5_native42_direct33_queue_v1_20261011',q),('actual_rank120_after183_completed33_main_v1_20261011',A/'run_publish_rank120_after183_completed33_main_v1_20261011.py')]:
  assert allowed();r=start_service(name,p.name,[],{str(p):sha(p),str(admission):sha(admission)});create(A/(name+'_activation.json'),r)
 print({'new120_actual_CPU_checks':31,'new_fits_by_preparation':0,'own6_full5_native42_direct33_queued':True},flush=True)
if __name__=='__main__':main()
