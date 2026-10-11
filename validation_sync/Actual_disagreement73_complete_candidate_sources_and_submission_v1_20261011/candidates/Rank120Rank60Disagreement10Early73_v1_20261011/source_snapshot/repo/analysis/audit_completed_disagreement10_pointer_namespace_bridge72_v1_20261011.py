from pathlib import Path
import sys,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
 assert allowed();service=A/'service_owned_workflows_20261006/actual_rank120_rank60_after183_disagreement10_screen_v1_20261011'
 while allowed():
  if (service/'service_execution.json').exists() and not owned(read(service/'native_launch.json')):break
  time.sleep(10)
 assert allowed();terminal=read(service/'service_execution.json')
 assert terminal['status']=='passed' or (terminal['status']=='failed' and terminal['failure'].startswith('FileExistsError:') and 'actual_StockRank120Rank60_after183_best_blend_fraction38_screen_location_v1_20261011.json' in terminal['failure']),terminal
 folder=Path('E:/赛题五_本机临时/StockRank120Rank60_after183_disagreement10_screen_v1_20261011');proof=read(folder/'verification.json');assert proof['status'].startswith('passed10_')
 assert proof['new_quality_score_records']==len(proof['records'])==10 and (proof['actual_nonidentity_full_controls'],proof['actual_nonidentity_prefix_controls'])==(9,27)
 for p,d in proof['input_sha256'].items():assert sha(p)==d,p
 for r in proof['records']:
  cap=Path(r['official_score_cache']['official_metrics_source']);assert sha(cap)==r['official_metric_capsule_sha256'] and read(cap)['metrics']==r['metrics']
  controls=folder/f"case{r['case']:03d}_controls.json";assert sha(controls)==r['control_sha256'] and read(controls)['numeric_sha256']==r['prediction_numeric_sha256']
 old=A/'actual_StockRank120Rank60_after183_best_blend_fraction38_screen_location_v1_20261011.json';assert 'best_blend_fraction38' in read(old)['output']
 create(A/'actual_StockRank120Rank60_after183_disagreement10_screen_location_v1_20261011.json',{'output':str(folder),'verification_sha256':sha(folder/'verification.json'),'actual_original_service_terminal':terminal,'original_best38_pointer_unchanged_sha256':sha(old),'original_scientific_controls_and_scores_all_passed':True,'new_scores_by_metadata_bridge':0})
 print('Original all10 controls and official capsules verified; new pointer namespace only; original best38 pointer preserved',flush=True)
if __name__=='__main__':main()
