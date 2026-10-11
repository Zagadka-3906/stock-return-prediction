"""Predeclare complete wider-network candidate qualification only after a real TRAIN score gain."""
from pathlib import Path
import sys,ast,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
from run_protected167_complete_family_v1_20261010 import junction
PROOF='rank60medium2048_best33_full_candidate_sources_admission_v1_20261011.json'
def changed(s):
 s=s.replace('stock_rank60_fixed_leading_case17','stock_rank60medium_best33').replace('stock_rank60_fixed17','stock_rank60medium_best33')
 s=s.replace('StockRank60Fixed17Early2','StockRank60MediumBest33Early').replace('StockRank60Fixed17Early','StockRank60MediumBest33Early')
 s=s.replace('股票60日case17提前完整候选_恢复2','股票60日更大容量最佳33项完整候选')
 s=s.replace('stock_rank60_embedding','stock_rank60medium_embedding').replace('stock_rank60_actual','stock_rank60medium_actual')
 s=s.replace('small512','medium2048').replace('Small512','Medium2048')
 s=s.replace('fixed_case17.json','selected_best33.json')
 s=s.replace('passed_single_fixed_scored_case17_native_checks_pending','passed_selected_best_of_actual33_TRAIN_records_native_checks_pending')
 s=s.replace('passed_fixed_case17','passed_selected_best33').replace('fixed_case17_from_actual_official_score_search_winner_not_claimed','selected_best_of_actual33_TRAIN_scores')
 s=s.replace('actual_fixed_case17_official_controls','actual_selected_best33_official_controls')
 s=s.replace('fixed_case_only','selected_case_only')
 s=s.replace('expected_scored_records=1','expected_scored_records=33').replace("'scored_records':1","'scored_records':33")
 s=s.replace("len(pilot['records'])==1 and pilot['search_winner_not_claimed']","len(pilot['records'])==1 and pilot['source_score_records']==33 and not pilot['search_winner_not_claimed']")
 s=s.replace('normalize_completed_stock_rank60_direct_embedding_complete35_after199_v6_20261011','rank60medium2048_early_candidate_recipes_v1_20261011')
 s=s.replace('actual_StockRank60DirectEmbeddingMedium2048_full5_independent_location_v1_20261011.json','actual_StockRank60MediumEmbeddingMedium2048_full5_independent_location_v1_20261011.json')
 return s
def save(p,s):
 ast.parse(s);assert not p.exists(),p;p.write_text(s,encoding='utf8');return p
def main():
 assert allowed()
 names=['verify_stock_rank60_fixed_leading_case17_native14_v2_20261011.py',
        'prepare_StockRank60Fixed17Early2_selected_candidate_v2_20261011.py',
        'run_StockRank60Fixed17Early2_selected_candidate_feature_cache_v2_20261011.py',
        'seal_StockRank60Fixed17Early2_selected_candidate_v3_20261011.py',
        'stock_rank60_fixed17_early_storage_v2_20261011.py']
 outputs=[]
 for name in names:
  s=changed((A/name).read_text(encoding='utf8'))
  if name.startswith('verify_'):
   start=s.index('SCORE_FILE=');end=s.index('\ndef allowed',start)
   s=s[:start]+"PREPARATION_PROOF=str(A/'"+PROOF+"')\n"+s[end:]
   s=s.replace("    original=Path(SCORE_FILE)","    decision=read(A/'rank60medium2048_best33_gain_decision_v1_20261011.json');assert decision['adopt']\n    original=Path(decision['selected_score_record'])")
   s=s.replace("raw=read(original);assert raw['case']==17 and raw['connected_final_score']==0.4514355480841008","raw=read(original);assert raw==decision['best']")
   s=s.replace("'case017_controls.json'","f\"case{raw['case']:03d}_controls.json\"")
   s=s.replace("'search_winner_not_claimed':True","'search_winner_not_claimed':False,'source_score_records':33")
   s=s.replace("    # Fixed already-scored case: complete-family selection is deliberately not claimed.","    # Best of all actual33 independently controlled official TRAIN records.")
   s=s.replace("pins={str(p):sha(p) for p in [original,", "pins={str(p):sha(p) for p in [A/'rank60medium2048_best33_gain_decision_v1_20261011.json',original,")
  if name.startswith('run_'):
   s=s.replace("    closed('actual_stock_rank120_embedding_small512_bank6_v1_20261011')","    closed('actual_stock_rank60medium_embedding_medium2048_bank6_v1_20261011')")
  if name.startswith('prepare_'):
   s=s.replace("A/'stock_rank60medium_best33_early_candidate_sources_preparation_v2_20261011.json'","A/'"+PROOF+"'")
  outputs.append(save(A/changed(name),s))
 recipes=A/'rank60medium2048_early_candidate_recipes_v1_20261011.py'
 save(recipes,"RECIPES={'stock_rank60medium_embedding16_cross120_rank60mean_recent252_medium2048_BF16_e64':('rank_MLP2048_StockRank60Medium_ID16_Cross120_seed20261009_e64','stock_rank60medium_embedding_medium2048_BF16_bank6_v1_20261011')}\n")
 outputs.append(recipes)
 create(A/PROOF,{'status':'predeclared_actual33_best_vs_completed38_official_S_only_before_new_candidate_inference',
  'input_sha256':{str(p):sha(p) for p in [Path(__file__),*[A/n for n in names],*outputs,
   A/'stock_rank60medium2048_own6_full5_native42_direct33_predeclared_sources_v1_20261011.json',
   A/'stock_rank60medium_actual_twelve_parent183_callbacks_CPU_controls_v2_20261011.json']},
  'expected_source_score_records':33,'selected_records':1,'expected_native_cases':14,'expected_cold_cases':14,'expected_prefit_refusals':7,
  'maximum_new_models':1,'complete_parent_native_independent_reload_and_cold80_required':True,
  'candidate_dispatch_only_if_strictly_higher_official_TRAIN_S':True,'test_labels_read':False,'new_fits':0,'new_scores':0})
 queue=A/'run_rank60medium2048_gain_selected_full_candidate_queue_v1_20261011.py'
 jobs=[('actual_stock_rank60medium_best33_native14_v2_20261011',outputs[0].name),
       ('actual_StockRank60MediumBest33Early_selected_candidate_preparation_v2_20261011',outputs[2].name),
       ('actual_StockRank60MediumBest33Early_selected_candidate_sealing_v3_20261011',outputs[3].name)]
 text='''from pathlib import Path
import sys,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from start_fast_completed_owned_service_v1_20261011 import start_service
from run_protected167_complete_family_v1_20261010 import junction
def main():
 assert allowed();closed('actual_stock_rank60medium_embedding_after183_direct_allocation33_v1_20261011')
 folder=Path('E:/赛题五_本机临时/StockRank60MediumEmbeddingMedium2048_after183_direct_allocation33_screen_v1_20261011')
 proof=read(folder/'verification.json');assert proof['new_quality_score_records']==len(proof['records'])==33
 assert (proof['actual_nonidentity_full_controls'],proof['actual_nonidentity_prefix_controls'])==(32,96)
 benchmark=Path('E:/赛题五_本机临时/StockRank120Rank60_after183_best_blend_fraction38_screen_v1_20261011/verification.json')
 other=read(benchmark);assert len(other['records'])==other['new_quality_score_records']==38
 for report in (proof,other):
  for p,d in report['input_sha256'].items():assert sha(p)==d,p
  for row in report['records']:
   cap=Path(row['official_score_cache']['official_metrics_source']);assert sha(cap)==row['official_metric_capsule_sha256'] and read(cap)['metrics']==row['metrics']
 best=min(proof['records'],key=lambda r:(-r['connected_final_score'],abs(r['configuration']['weight']),r['case']))
 incumbent=max(r['connected_final_score'] for r in other['records'])
 adopt=best['connected_final_score']>incumbent
 create(A/'rank60medium2048_best33_gain_decision_v1_20261011.json',{'status':'actual_all33_vs_all38_OFFICIAL_TRAIN_S_only_selection','adopt':adopt,'best':best,'incumbent_S':incumbent,'selected_score_record':str(folder/f"case{best['case']:03d}_official.json"),'input_sha256':{str(folder/'verification.json'):sha(folder/'verification.json'),str(benchmark):sha(benchmark)},'test_labels_read':False})
 if not adopt:
  print('All33 retained; no higher S than completed38 incumbent, so no candidate inference.',flush=True);return
 closed('Rank120Rank60BestBlend38Early_selected_candidate_sealing_v1_20261011')
 storage=importlib.import_module(STORAGE)
 for logical,physical in storage.OUTPUTS.items():
  assert not logical.exists() and not physical.exists();physical.mkdir(parents=True);logical.parent.mkdir(parents=True,exist_ok=True);junction(logical,physical)
 for name,driver in JOBS:
  assert allowed();p=A/driver;r=start_service(name,driver,[],{str(p):sha(p),str(A/PROOF):sha(A/PROOF)})
  create(A/(name+'_activation.json'),r);closed(name)
 print('Actual gaining33 selected candidate sealed; publication/delivery still required.',flush=True)
if __name__=='__main__':main()
'''.replace('STORAGE',repr(outputs[4].stem)).replace('JOBS',repr(jobs)).replace('PROOF',repr(PROOF))
 save(queue,text)
 r=start_service('actual_rank60medium2048_gain_selected_full_candidate_queue_v1_20261011',queue.name,[],{str(queue):sha(queue),str(A/PROOF):sha(A/PROOF)})
 create(A/'actual_rank60medium2048_gain_selected_candidate_queue_activation_v1_20261011.json',r)
 print({'conditional_full_candidate_pipeline':True,'only_official_TRAIN_S_gain_dispatches_inference':True,'new_inference_claimed':False},flush=True)
if __name__=='__main__':main()
