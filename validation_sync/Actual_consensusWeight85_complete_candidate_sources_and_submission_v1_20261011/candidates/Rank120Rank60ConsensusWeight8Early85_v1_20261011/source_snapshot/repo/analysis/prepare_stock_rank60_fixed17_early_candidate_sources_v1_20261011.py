"""Freeze and dispatch one scored leading case independently of unrelated board rounds."""
from pathlib import Path
import sys,ast
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
PROOF=A/'stock_rank60_fixed17_early_candidate_sources_preparation_v1_20261011.json'

def changed(text):
 return text.replace('StockRank60DirectEmbedding200','StockRank60Fixed17Early').replace('第200轮_20261010','股票60日case17提前完整候选_20261011').replace('stock_rank60_direct_embedding200_storage_v6_20261011','stock_rank60_fixed17_early_storage_v1_20261011').replace('stock_rank60_direct_embedding200_candidate_sources_preparation_v6_20261011','stock_rank60_fixed17_early_candidate_sources_preparation_v1_20261011').replace('prepare_StockRank60Fixed17Early_selected_candidate_v6_20261011','prepare_StockRank60Fixed17Early_selected_candidate_v1_20261011').replace('seal_StockRank60Fixed17Early_selected_candidate_v6_20261011','seal_StockRank60Fixed17Early_selected_candidate_v1_20261011')

def save(name,text):
 ast.parse(text);p=A/name
 if p.exists():
  assert not PROOF.exists() and p.read_text(encoding='utf8')==text, 'Only identical pre-admission source may be reused'
 else:p.write_text(text,encoding='utf8')
 return p

def main():
 assert allowed();closed('actual_stock_rank60_fixed_leading_case17_native14_v2_20261011')
 from stock_rank60_fixed17_early_storage_v1_20261011 import OUTPUTS,empty
 for p in OUTPUTS:empty(p)
 native=Path(read(A/'actual_stock_rank60_fixed_leading_case17_native14_location_v2_20261011.json')['output'])
 proof=read(native/'verification.json');assert proof['status']=='passed_fixed_case17_six_states14_native_and14_cold_and7_prefit_rejections'
 assert proof['best']['connected_final_score']==0.4514355480841008
 for p,d in proof['input_sha256'].items():assert sha(p)==d,p
 template=A/'prepare_StockRank60DirectEmbedding200_selected_candidate_v6_20261011.py'
 text=changed(template.read_text(encoding='utf8'))
 text=text.replace('from qualify_stock_rank60_direct_embedding35_selected_native14_v6_20261011 import allowed','from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed')
 text=text.replace("closed('StockRank60DirectEmbedding35_selected_native14_v6_20261011')","closed('actual_stock_rank60_fixed_leading_case17_native14_v2_20261011')")
 text=text.replace('from qualify_stock_rank60_direct_embedding35_selected_native14_v6_20261011 import OUT as native_out','from verify_stock_rank60_fixed_leading_case17_native14_v2_20261011 import OUT as native_out')
 text=text.replace("pilot_path=native_out/'pilot35.json';pilot=read(pilot_path)","pilot_path=native_out/'fixed_case17.json';pilot=read(pilot_path)")
 text=text.replace('passed_normalized35_actual_TRAIN_official_records_selected_stage_and_full_inference_pending','passed_single_fixed_scored_case17_native_checks_pending')
 text=text.replace("assert len(pilot['records'])==35","assert len(pilot['records'])==1 and pilot['search_winner_not_claimed']")
 text=text.replace("return (-r['connected_final_score'],r['expected_unique_native_models'],abs(r['configuration']['weight']),r['case'])","return (-r['connected_final_score'],r['case'])")
 text=text.replace("assert best==pilot['best'];cfg=best['configuration']","assert best==pilot['best'];best={**best,'prediction_numeric_bytes_sha256':best['prediction_numeric_sha256']};cfg=best['configuration']")
 text=text.replace("comparison_parent=pilot['actual_comparison_parent_round']","comparison_parent=183  # Sole actual fully qualified scheme base; no claim about unfinished later rounds.")
 text=text.replace('in (183,199)','in (183,)')
 text=text.replace('selected_by_all35_actual_official_scores','fixed_case17_from_actual_official_score_search_winner_not_claimed')
 text=text.replace('actual_all35_official_controls','actual_fixed_case17_official_controls')
 text=text.replace('expected_scored_records=35','expected_scored_records=1').replace("'scored_records':35","'scored_records':1")
 text=text.replace("'new_native_fits':0,'test_labels_read':False})\n    raw_path=", "'new_native_fits':0,'search_winner_not_claimed':True,'test_labels_read':False})\n    raw_path=")
 prepare=save('prepare_StockRank60Fixed17Early_selected_candidate_v1_20261011.py',text)
 sealer_template=A/'seal_StockRank60DirectEmbedding200_selected_candidate_v6_20261011.py'
 seal=changed(sealer_template.read_text(encoding='utf8'))
 seal=seal.replace('StockRank60Fixed17Early_selected_candidate_preparation_v6_20261011','actual_StockRank60Fixed17Early_selected_candidate_preparation_v1_20261011')
 seal=seal.replace('stock_rank60_direct_embedding35_selected_native14_v1_20261011','stock_rank60_fixed_leading_case17_native14_v2_20261011').replace('/pilot35.json','/fixed_case17.json')
 seal=seal.replace('passed_actual35_selected_candidate_full_graph_and_metrics_and_source_bytes','passed_fixed_case17_candidate_full_graph_and_metrics_and_source_bytes')
 sealer=save('seal_StockRank60Fixed17Early_selected_candidate_v1_20261011.py',seal)
 cache_template=A/'run_StockRank60DirectEmbedding200_selected_candidate_feature_cache_v6_20261011.py'
 cache=changed(cache_template.read_text(encoding='utf8'))
 # GPU training bank must have ended; full inference preserves all native and independent checks.
 needle="    assert allowed();closed('actual_feature120_verified_memoization_TRAIN344_v1_20261010')"
 assert cache.count(needle)==1
 cache=cache.replace(needle,needle+"\n    closed('actual_stock_rank120_embedding_small512_bank6_v1_20261011')")
 runner=save('run_StockRank60Fixed17Early_selected_candidate_feature_cache_v1_20261011.py',cache)
 for p in [prepare,sealer,runner]:
  s=p.read_text(encoding='utf8');assert 'StockRank60DirectEmbedding200' not in s and '第200轮_20261010' not in s
 assert OUTPUTS[ROOT/'analysis/StockRank60Fixed17Early_selected_release_v1_20261011'].resolve().drive.upper()=='E:'
 paths=[Path(__file__),A/'stock_rank60_fixed17_early_storage_v1_20261011.py',template,sealer_template,cache_template,prepare,sealer,runner,native/'verification.json',native/'fixed_case17.json']
 pins={str(p):sha(p) for p in paths}
 create(PROOF,{'status':'compiled_fixed_case17_early_full_candidate_same_all_native_independent_cold80_CSV_checks_before_future',
  'input_sha256':pins,'fixed_case':17,'S':0.4514355480841008,'actual_complete_scheme_parent':183,
  'expected_scored_records':1,'search_winner_not_claimed':True,'no_dependency_on_unfinished_comparison_anchor199':True,
  'new_fits':0,'new_scores':0,'candidate_future_inference_not_yet_started':True,'test_labels_read':False})
 from start_fast_completed_owned_service_v1_20261011 import start_service
 assert allowed()
 print(start_service('actual_StockRank60Fixed17Early_selected_candidate_preparation_v1_20261011',runner.name,[],{**pins,str(PROOF):sha(PROOF)}),flush=True)
 assert allowed()
 print(start_service('actual_StockRank60Fixed17Early_selected_candidate_sealing_v1_20261011',sealer.name,[],{**pins,str(PROOF):sha(PROOF)}),flush=True)

if __name__=='__main__':main()
