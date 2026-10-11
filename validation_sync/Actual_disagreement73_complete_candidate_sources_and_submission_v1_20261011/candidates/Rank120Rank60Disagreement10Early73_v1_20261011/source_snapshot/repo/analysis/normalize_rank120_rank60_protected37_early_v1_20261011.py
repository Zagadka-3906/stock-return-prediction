"""Normalize only the actual completed 37 TRAIN comparisons; no future data or fits."""
from pathlib import Path
import sys,hashlib,numpy as np
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
OUT=Path('E:/赛题五_本机临时/rank120_rank60_protected37_early_normalized_v1_20261011')
def best_key(r):return (-r['connected_final_score'],r['expected_unique_native_models'],abs(r['configuration']['weight']),r['case'])
def main():
 assert allowed();closed('actual_rank120_rank60_after183_protected37_screen_v2_20261011')
 folder=Path('E:/赛题五_本机临时/StockRank120Rank60_after183_protected37_screen_v1_20261011');proof=read(folder/'verification.json')
 assert len(proof['records'])==proof['new_quality_score_records']==37
 assert (proof['actual_nonidentity_full_controls'],proof['actual_nonidentity_prefix_controls'])==(36,108)
 pins={**proof['input_sha256'],str(folder/'verification.json'):sha(folder/'verification.json'),str(Path(__file__)):sha(__file__)}
 parent=ROOT/'candidates/optimization_20261003_r183';release=A/'optimization_20261003_r183'
 assert read(release/'full_registration_execution.json')['status']=='passed'
 parent_hashes={r['sha256'] for r in read(parent/'verification.json')['models'].values()}
 leaves=[]
 for horizon in (60,120):
  bank=Path(f'E:/赛题五_本机临时/stock_rank{horizon}_embedding_small512_BF16_bank6_v1_20261011');info=read(bank/'2025/info.json')
  assert read(bank/'verification.json')['actual_native_fits']==6 and info['configuration']['seed']==20261009
  assert info['configuration']['label_horizon_trading_days']==horizon
  leaves.append({'name':f'rank_MLP512_StockEmbedding16_Cross120Recent252Rank{horizon}Mean_seed09_e64','bank':str(bank),'sha256':info['model_sha256'],'label_horizon_trading_days':horizon,'training_calendar_window':252})
  for year in range(2020,2026):
   for n in ('info.json','model.joblib'):p=bank/str(year)/n;pins[str(p)]=sha(p)
 records=[]
 for original in proof['records']:
  identity=original['case']==0;cfg=dict(original['configuration'])
  cfg.update(stage_kind='anchor' if identity else 'rank120_rank60_protected_raw_average',anchor_round=183,model=None if identity else 'rank120_rank60_protected_pair',recipe=None if identity else 'stock_rank120_rank60_protected_label_horizon_ID16_cross120_recent252_e64',codec=None if identity else cfg['kind'],decay=None,first2020_active=not identity)
  capsule=Path(original['official_score_cache']['official_metrics_source']);record=folder/f"case{original['case']:03d}_official.json";control=folder/f"case{original['case']:03d}_controls.json"
  assert read(record)==original and sha(control)==original['control_sha256']
  assert sha(capsule)==original['official_metric_capsule_sha256'] and read(capsule)['metrics']==original['metrics']
  if identity:
   assert original['metrics']==read(release/'calibrated_csv_official.json')['metrics']
   raw=np.load(release/'selected_validation.npy',mmap_mode='r');assert hashlib.sha256(memoryview(np.ascontiguousarray(raw)).cast('B')).hexdigest()==original['prediction_numeric_sha256']
  records.append({**original,'configuration':cfg,'prediction_numeric_bytes_sha256':original['prediction_numeric_sha256'],'expected_unique_native_models':len(parent_hashes|({r['sha256'] for r in leaves} if not identity else set())),'native_bank_components':leaves if not identity else [],'ordered_native_components':[r['name'] for r in leaves] if not identity else [],'native_stage_module':'rank120_rank60_protected_after_qualified183_native_stage_v1_20261011','original_screen_case':original['case'],'original_screen_record':str(record),'submission_qualified':identity})
  for p in (capsule,record,control):pins[str(p)]=sha(p)
 for p,d in pins.items():assert sha(p)==d,p
 best=min(records,key=best_key);assert best['connected_final_score']>=records[0]['connected_final_score']
 OUT.mkdir(exist_ok=False)
 create(OUT/'pilot37.json',{'status':'passed_normalized37_actual_TRAIN_official_records_selected_native_and_full_future_pending','records':records,'best':best,'input_sha256':pins,'expected_scored_records':37,'actual_nonidentity_full_controls':36,'actual_nonidentity_prefix_controls':108,'actual_comparison_parent_round':183,'actual_scheme_base_round':183,'new_quality_scores_by_normalization':0,'new_native_fits':0,'actual_future_X_read':False,'test_labels_read':False})
 create(OUT/'verification.json',{'status':'passed_actual37_capsules_and_controls_before_selected_native_or_future','best':best,'input_sha256':pins,'full_board_pending':True,'test_labels_read':False})
 create(A/'actual_rank120_rank60_protected37_early_normalized_location_v1_20261011.json',{'output':str(OUT),'pilot_sha256':sha(OUT/'pilot37.json')})
if __name__=='__main__':main()
