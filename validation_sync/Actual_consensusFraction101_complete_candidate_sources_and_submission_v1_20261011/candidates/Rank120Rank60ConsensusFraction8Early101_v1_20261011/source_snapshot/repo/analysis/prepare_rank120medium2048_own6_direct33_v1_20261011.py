"""Freeze a fresh wider120-day objective using verified120 maturity, no reused weights."""
from pathlib import Path
import sys,ast,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service

def changed(s):
 s=s.replace('stock_rank120','stock_rank120medium').replace('StockRank120','StockRank120Medium').replace('small512','medium2048').replace('Small512','Medium2048').replace('[512, 256, 128]','[2048, 1024, 512]')
 s=s.replace('recent252_rank120medium','recent252_rank120')
 s=s.replace('actual_stock_rank120medium_embedding_mature_fixture_location','actual_stock_rank120_embedding_mature_fixture_location')
 s=s.replace('StockRank120MediumEmbedding_actual_mature_fixture_CPU','StockRank120Embedding_actual_mature_fixture_CPU')
 return s

def main():
 assert allowed()
 files=['stock_rank120_embedding_small512_BF16_native_v1_20261011.py','stock_rank120_embedding_saved_tensor_decoder_v1_20261011.py','verify_stock_rank120_embedding_small512_restart_v1_20261011.py','verify_stock_rank120_embedding_small512_small_CPU_v1_20261011.py','train_stock_rank120_embedding_small512_BF16_bank6_own64_v1_20261011.py','verify_stock_rank120_embedding_small512_full5_independent_v1_20261011.py','stock_rank120_embedding_after_complete_qualified_parent_native_stage_v1_20261011.py','stock_rank120_embedding_after_complete_qualified_parent_native_stage_v2_20261011.py','verify_stock_rank120_embedding_six_state_native42_v1_20261011.py','predict_stock_rank120_embedding_complete_qualified_parent_scheme_v2_20261011.py','verify_stock_rank120_actual_twelve_parent183_callbacks_CPU_v2_20261011.py','run_stock_rank120_embedding_after183_direct_allocation33_v1_20261011.py','run_publish_rank120_after183_completed33_main_v1_20261011.py']
 outputs=[]
 for name in files:
  p=A/name;q=A/changed(name);s=changed(p.read_text(encoding='utf8'));ast.parse(s);assert not q.exists();q.write_text(s,encoding='utf8',newline='\n');outputs.append(q)
 native=importlib.import_module(changed(Path(files[0]).stem))
 assert native.CONFIG['hidden']==[2048,1024,512] and native.CONFIG['target']=='y_rank_120mean'
 assert native.CONFIG['label_horizon_trading_days']==120 and native.CONFIG['epochs']==64 and native.CONFIG['training_calendar_window']==252
 # The native maturity and boundary cases are target-specific; they are reused, not recounted as new tests.
 actual=[A/'recent252_rank120_mature_population_actual_CPU_controls_v2_20261011.json',A/'rank120_first_mature_boundary_and_gaps_actual_CPU_controls_v1_20261011.json',A/'actual_stock_rank120_embedding_mature_fixture_location_v1_20261011.json']
 assert [len(read(p)['records']) for p in actual[:2]]==[7,12]
 fixture=Path(read(actual[2])['output']);assert read(fixture/'verification.json')['last_label_end']<20191231
 pins={str(p):sha(p) for p in [Path(__file__),*[A/n for n in files],*outputs,*actual,A/'forward120_mature_training_labels_v2_20261011.py',A/'recent252_rank120_mature_training_population_v2_20261011.py',fixture/'verification.json']}
 protocol=A/'stock_rank120medium2048_own6_full5_native42_direct33_predeclared_sources_v1_20261011.json'
 record={'status':'predeclared_fresh_H120_medium2048_hypothesis_before_ANY_fits_or_scores','input_sha256':pins,'configuration':native.CONFIG,'reuse_small512_weights':False,'reuse_H60_weights':False,'actual_existing_maturity_and_boundary_CPU_cases_referenced':19,'new_CPU_tests_claimed_by_preparation':0,'expected_annual_fits':6,'expected_full_independent_years':5,'expected_native_and_cold_states':42,'expected_official_scores':33,'expected_full_controls':32,'expected_prefix_controls':96,'test_labels_read':False,'new_fits':0,'new_scores':0}
 create(protocol,record)
 for name in ['stock_rank120_embedding_own64_native_sources_preparation_v1_20261011.json','stock_rank120_embedding_actual_restart_and_own6_sources_admission_v1_20261011.json','stock_rank120_embedding_native_stage_and_fast17_sources_admission_v1_20261011.json','stock_rank120_after183_direct33_predeclared_sources_v1_20261011.json']:
  create(A/changed(name),record)
 jobs=[('actual_stock_rank120medium_embedding_medium2048_restart_v1_20261011',outputs[2].name),('StockRank120MediumEmbeddingMedium2048_independent_small_CPU_v1_20261011',outputs[3].name),('actual_stock_rank120medium_embedding_medium2048_bank6_v1_20261011',outputs[4].name),('StockRank120MediumEmbeddingMedium2048_independent_full5_GPU_controls_v1_20261011',outputs[5].name),('actual_stock_rank120medium_embedding_six_state_native42_v1_20261011',outputs[8].name),('actual_stock_rank120medium_embedding_after183_direct_allocation33_v1_20261011',outputs[11].name)]
 queue=A/'run_rank120medium2048_own6_native42_direct33_queue_v1_20261011.py'
 text='''from pathlib import Path
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
 for name,driver in JOBS:
  if 'restart_' in driver or driver.startswith('train_') or 'full5_' in driver or 'native42_' in driver:
   while busy() or psutil.virtual_memory().available<12*2**30:
    assert allowed();time.sleep(10)
  assert allowed();p=A/driver;i=start_service(name,driver,[],{str(p):sha(p),str(A/PROTOCOL):sha(A/PROTOCOL)});create(A/(name+'_activation.json'),i);closed(name)
if __name__=='__main__':main()
'''.replace('JOBS',repr(jobs)).replace('PROTOCOL',repr(protocol.name))
 ast.parse(text);assert not queue.exists();queue.write_text(text,encoding='utf8',newline='\n')
 # Import actual modules before dispatch, without invoking model fits or official scores.
 imported=[]
 for q in outputs:
  if q.name.startswith(('stock_','verify_','predict_')):importlib.import_module(q.stem);imported.append(q.name)
 create(A/'rank120medium2048_runtime_sources_import_admission_v1_20261011.json',{'status':'passed_actual_fresh120_medium_runtime_imports_predeclared_no_science_claim','modules':imported,'input_sha256':{**pins,str(queue):sha(queue),str(protocol):sha(protocol)},'new_fits':0,'new_scores':0,'test_labels_read':False})
 for name,p in [('actual_rank120medium_twelve_parent183_callbacks_CPU_v2_20261011',outputs[10]),('actual_rank120medium2048_own6_native42_direct33_queue_v1_20261011',queue),('actual_rank120medium_after183_completed33_main_v1_20261011',outputs[12])]:
  assert allowed();i=start_service(name,p.name,[],{str(p):sha(p),str(protocol):sha(protocol)});create(A/(name+'_activation.json'),i)
 print('New H120 capacity hypothesis frozen; native modules imported; independent CPU callbacks live; GPU queue waits completed H60 gain handling',flush=True)

if __name__=='__main__':main()
