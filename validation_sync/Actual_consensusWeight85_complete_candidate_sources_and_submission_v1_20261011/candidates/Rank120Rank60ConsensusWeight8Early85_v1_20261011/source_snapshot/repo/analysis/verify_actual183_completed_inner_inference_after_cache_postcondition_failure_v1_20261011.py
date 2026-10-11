from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
 assert allowed()
 release=A/'StockRank20Embedding183_selected_release_v1_20261010';ready=read(release/'inference_ready.json');v=read(release/'verification.json')
 assert ready['status']=='passed_actual_selected_new_StockRank20Embedding183_candidate_inference'
 assert v['status']=='passed_frozen_StockRank20Embedding183_complete_parent_native_independent_and_cold80'
 for p,d in v['input_sha256'].items():assert sha(p)==d,p
 folder=Path(ready['source_candidate']);pred=read(folder/'verification.json')
 assert pred['status']=='passed' and (pred['rows'],pred['days'],pred['codes'])==(1599600,344,4650)
 for k in ('model_reload_bit_identical','pipeline_replay_bit_identical','csv_replay_byte_identical','cold80_day_prefix_bit_identical'):assert pred[k],k
 assert sha(folder/'submission.csv')==pred['csv_sha256']==v['csv_sha256']
 assert len(pred['models'])==v['actual_saved_model_count']==35
 for m in pred['models'].values():assert sha(m['path'])==m['sha256']
 create(A/'actual183_completed_inner_inference_rehashed_recovery_v1_20261011.json',{'status':'passed_rehashed_actual_inner_full_candidate_inference_after_outer_4660_cache_postcondition_failure','input_sha256':{str(p):sha(p) for p in [Path(__file__),release/'inference_ready.json',release/'verification.json',folder/'verification.json',folder/'submission.csv']},'actual_saved_models':35,'rows_days_stocks':[1599600,344,4650],'new_inference_performed':False,'outer_cache_statistics_not_recovered_or_claimed':True,'original_failed_service_preserved':True,'test_labels_read':False})
if __name__=='__main__':main()
