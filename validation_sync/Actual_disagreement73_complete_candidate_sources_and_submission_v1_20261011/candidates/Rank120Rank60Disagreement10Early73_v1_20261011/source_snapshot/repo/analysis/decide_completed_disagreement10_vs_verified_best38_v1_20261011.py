from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
def main():
 assert allowed();closed('actual_rank120_rank60_after183_disagreement10_screen_v1_20261011');folder=Path('E:/赛题五_本机临时/StockRank120Rank60_after183_disagreement10_screen_v1_20261011');proof=read(folder/'verification.json')
 assert len(proof['records'])==proof['new_quality_score_records']==10 and (proof['actual_nonidentity_full_controls'],proof['actual_nonidentity_prefix_controls'])==(9,27)
 for p,d in proof['input_sha256'].items():assert sha(p)==d,p
 for r in proof['records']:
  cap=Path(r['official_score_cache']['official_metrics_source']);assert sha(cap)==r['official_metric_capsule_sha256'] and read(cap)['metrics']==r['metrics']
 incumbent=A/'alternate_verified_best_blend38_submission_delivery_v1_20261011.json';best_delivery=read(incumbent);assert best_delivery['all_full_native_independent_reload_csv_and_cold80_checks_passed']
 best=min(proof['records'],key=lambda r:(-r['connected_final_score'],abs(r['configuration'].get('disagreement_penalty') or 0),abs(r['configuration']['weight']),r['case']))
 adopt=best['connected_final_score']>best_delivery['official_TRAIN_internal_score']
 create(A/'rank120_rank60_disagreement10_gain_decision_v1_20261011.json',{'status':'actual10_OFFICIAL_TRAIN_S_only_comparison_vs_fully_verified_best38_complete_candidate','adopt':adopt,'best':best,'incumbent_S':best_delivery['official_TRAIN_internal_score'],'input_sha256':{str(folder/'verification.json'):sha(folder/'verification.json'),str(incumbent):sha(incumbent)},'new_full_candidate_native_qualification_required_if_adopt':adopt,'test_labels_read':False,'future_X_read':False})
 print({'adopt':adopt,'best_S':best['connected_final_score'],'full_native_candidate_qualification_required_if_higher':adopt},flush=True)
if __name__=='__main__':main()
