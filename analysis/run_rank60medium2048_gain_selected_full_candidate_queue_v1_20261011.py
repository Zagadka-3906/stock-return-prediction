from pathlib import Path
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
 storage=importlib.import_module('stock_rank60medium_best33_early_storage_v2_20261011')
 for logical,physical in storage.OUTPUTS.items():
  assert not logical.exists() and not physical.exists();physical.mkdir(parents=True);logical.parent.mkdir(parents=True,exist_ok=True);junction(logical,physical)
 for name,driver in [('actual_stock_rank60medium_best33_native14_v2_20261011', 'verify_stock_rank60medium_best33_native14_v2_20261011.py'), ('actual_StockRank60MediumBest33Early_selected_candidate_preparation_v2_20261011', 'run_StockRank60MediumBest33Early_selected_candidate_feature_cache_v2_20261011.py'), ('actual_StockRank60MediumBest33Early_selected_candidate_sealing_v3_20261011', 'seal_StockRank60MediumBest33Early_selected_candidate_v3_20261011.py')]:
  assert allowed();p=A/driver;r=start_service(name,driver,[],{str(p):sha(p),str(A/'rank60medium2048_best33_full_candidate_sources_admission_v1_20261011.json'):sha(A/'rank60medium2048_best33_full_candidate_sources_admission_v1_20261011.json')})
  create(A/(name+'_activation.json'),r);closed(name)
 print('Actual gaining33 selected candidate sealed; publication/delivery still required.',flush=True)
if __name__=='__main__':main()
