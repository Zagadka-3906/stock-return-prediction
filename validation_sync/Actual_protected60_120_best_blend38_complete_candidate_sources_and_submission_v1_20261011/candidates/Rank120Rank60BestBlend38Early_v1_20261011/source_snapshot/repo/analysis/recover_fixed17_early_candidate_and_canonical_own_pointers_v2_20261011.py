"""Verify real own panels before adding canonical aliases; preserve failed early outputs."""
from pathlib import Path
import sys,ast,importlib
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def main():
 assert allowed()
 old=A/'service_owned_workflows_20261006/actual_StockRank60Fixed17Early_selected_candidate_preparation_v1_20261011'
 assert read(old/'service_execution.json')['status']=='failed' and not owned(read(old/'native_launch.json'))
 aliases=[];aliaspins={}
 for horizon in [60,120]:
  source=A/f'actual_StockRank{horizon}EmbeddingSmall512_full5_independent_location_v1_20261011.json'
  target=A/f'actual_StockRank{horizon}DirectEmbeddingSmall512_full5_independent_location_v1_20261011.json'
  location=read(source);assert location['status']=='actual_complete_wide_annual_independent_controls_passed_on_E'
  folder=Path(location['output']);vpath=folder/'verification.json';v=read(vpath)
  assert sha(vpath)==location['verification_sha256']
  assert v['status']=='passed_actual_full5_5635800_medium2048_BF16_native_and_independent_GPU_forecasts_and10_cold_prefixes'
  assert v['rows_days_stocks']==[5635800,1212,4650] and v['actual_complete_bank_fits']==6 and len(v['records'])==5
  forecast=folder/'combined_raw.parquet';assert sha(forecast)==v['combined_forecast_sha256']
  backend=importlib.import_module(f'stock_rank{horizon}_embedding_small512_BF16_native_v1_20261011')
  bank=Path(f'E:/赛题五_本机临时/stock_rank{horizon}_embedding_small512_BF16_bank6_v1_20261011')
  info=read(bank/'2025/info.json');assert info['configuration']==backend.CONFIG
  assert backend.CONFIG['label_horizon_trading_days']==horizon and backend.CONFIG['target']==f'y_rank_{horizon}mean'
  assert read(bank/'verification.json')['actual_native_fits']==6
  assert not target.exists();raw=source.read_bytes()
  with target.open('xb') as stream:stream.write(raw)
  assert sha(source)==sha(target) and read(source)==read(target)
  pins={str(p):sha(p) for p in [source,target,vpath,forecast,Path(backend.__file__),bank/'verification.json',bank/'2025/info.json']}
  aliaspins.update(pins);aliases.append({'horizon':horizon,'source':str(source),'canonical_alias':str(target),'same_raw_panel_bytes':True,'actual_proof_sha256':sha(vpath)})
 aliasproof=A/'actual_rank60_120_direct_own_pointer_aliases_v2_20261011.json'
 create(aliasproof,{'status':'passed_actual_complete_own6_full5_config_and_raw_panel_before_byte_identical_direct_aliases',
  'input_sha256':aliaspins,'aliases':aliases,'new_fits':0,'new_scores':0,'test_labels_read':False})
 mapping={
  'stock_rank60_fixed17_early_storage_v1_20261011':'stock_rank60_fixed17_early_storage_v2_20261011',
  'stock_rank60_fixed17_early_candidate_sources_preparation_v1_20261011':'stock_rank60_fixed17_early_candidate_sources_preparation_v2_20261011',
  'prepare_StockRank60Fixed17Early_selected_candidate_v1_20261011':'prepare_StockRank60Fixed17Early2_selected_candidate_v2_20261011',
  'seal_StockRank60Fixed17Early_selected_candidate_v1_20261011':'seal_StockRank60Fixed17Early2_selected_candidate_v2_20261011',
  'run_StockRank60Fixed17Early_selected_candidate_feature_cache_v1_20261011':'run_StockRank60Fixed17Early2_selected_candidate_feature_cache_v2_20261011',
  'StockRank60Fixed17Early_selected_candidate_preparation_v1_20261011':'StockRank60Fixed17Early2_selected_candidate_preparation_v2_20261011',
  'StockRank60Fixed17Early_selected_release_v1_20261011':'StockRank60Fixed17Early2_selected_release_v2_20261011',
  'StockRank60Fixed17Early_v1_20261011':'StockRank60Fixed17Early2_v2_20261011',
  '股票60日case17提前完整候选_20261011':'股票60日case17提前完整候选_恢复2_20261011'}
 files=[('stock_rank60_fixed17_early_storage_v1_20261011.py','stock_rank60_fixed17_early_storage_v2_20261011.py'),
  ('prepare_StockRank60Fixed17Early_selected_candidate_v1_20261011.py','prepare_StockRank60Fixed17Early2_selected_candidate_v2_20261011.py'),
  ('seal_StockRank60Fixed17Early_selected_candidate_v1_20261011.py','seal_StockRank60Fixed17Early2_selected_candidate_v2_20261011.py'),
  ('run_StockRank60Fixed17Early_selected_candidate_feature_cache_v1_20261011.py','run_StockRank60Fixed17Early2_selected_candidate_feature_cache_v2_20261011.py')]
 pins={str(Path(__file__)):sha(__file__),str(aliasproof):sha(aliasproof),str(old/'service_execution.json'):sha(old/'service_execution.json')}
 for original,new in files:
  source=A/original;text=source.read_text(encoding='utf8')
  # Longest exact identifier first; none of the proven backend names are changed.
  for k in sorted(mapping,key=len,reverse=True):text=text.replace(k,mapping[k])
  ast.parse(text);target=A/new;assert not target.exists();target.write_text(text,encoding='utf8')
  pins[str(source)]=sha(source);pins[str(target)]=sha(target)
 storage=importlib.import_module('stock_rank60_fixed17_early_storage_v2_20261011')
 for p in storage.OUTPUTS:storage.empty(p)
 proof=A/'stock_rank60_fixed17_early_candidate_sources_preparation_v2_20261011.json'
 create(proof,{'status':'compiled_new_exclusive_fixed_case17_early_full_candidate_actual_own_panel_aliases_resolved_before_future',
  'input_sha256':pins,'previous_failed_outputs_preserved':True,'new_fits':0,'new_scores':0,
  'all_native_independent_cold80_CSV_assertions_preserved':True,'search_winner_not_claimed':True,
  'parent':183,'fixed_case':17,'test_labels_read':False})
 from start_fast_completed_owned_service_v1_20261011 import start_service
 assert allowed()
 print(start_service('actual_StockRank60Fixed17Early2_selected_candidate_preparation_v2_20261011',files[-1][1],[],{**pins,str(proof):sha(proof)}),flush=True)
 assert allowed()
 print(start_service('actual_StockRank60Fixed17Early2_selected_candidate_sealing_v2_20261011',files[2][1],[],{**pins,str(proof):sha(proof)}),flush=True)

if __name__=='__main__':main()
