"""Record reduced-head124 synthetic controls without claiming historical replay or quality."""
from pathlib import Path
import sys,time,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
 pointer=A/'actual_PureRFFHuber124_synthetic_location_v2_20261008.json';proof=Path(read(pointer)['output'])/'verification.json';v=read(proof)
 assert v['actual_cases']==124 and v['actual_cold_cases']==372 and v['actual_double_stage_order_pairs']==54 and v['actual_zero_Ridge_reference_full_forecast_bits_equal_for_all124_cases']
 inputs=[Path(__file__),pointer,proof,A/'PureRFFHuber128_round149_proposal_v1_20261008.json',A/'PureRFFHuber149_synthetic_receiver_recovery_v2_20261008.json',
  A/'actual145_148_and_RAM_main_v33_receipt_20261008.json']
 create(A/'actual_optimization_checkpoint_v36_20261008.json',{'status':'actual149_reduced_physical_head_synthetic124_and372cold_passed_with_zero_Ridge_forecast_equivalence',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(f):sha(f) for f in inputs},'best_fully_qualified_round':145,
  'best_fully_qualified_score':0.4511766535314416,'actual149_synthetic_cases':124,'actual149_cold_synthetic_cases':372,
  'actual149_order_pairs_distinct_numeric_bits':v['actual_order_pairs_with_distinct_numeric_bits'],'synthetic_reference_zero_Ridge_weight_forecasts_exact':True,
  'actual149_historical_full_native_calendar_replays_not_yet_prepared':True,'actual149_quality_receivers_not_yet_prepared':True,
  '149_saved25_state_subset_rehash_and_historical_duplicate_graph_audit_required':True,'actual149_official_scores':0,'actual149_future_inference':0,
  'new_quality_scores_by_checkpoint':0,'test_labels_read':False,'global_feasible_direction_or_compute_exhaustion_claimed':False})
 old=A/'monitor_actual_chronological_optimization_progress_v35_20261008.py';s=old.read_text(encoding='utf8').replace('optimization_live_progress_v35','optimization_live_progress_v36')
 needle="    write(A/'optimization_live_progress_v36_20261008.json'";assert s.count(needle)==1
 s=s.replace(needle,"    state['pure149_frontier']={'expected_quality_cases':128,'synthetic124':status('PureRFFHuber124_actual_synthetic_controls_v2_20261008'),'actual_native_historical_full_and_quality_receivers_not_yet_prepared':True,'actual_official_scores':0,'actual_future_inference':0,'reduced_required_heads_cross_huber_both':[2,3,5]}\n"+needle)
 needle="    write(A/'optimization_live_progress_v36_20261008.md',text)";assert s.count(needle)==1
 s=s.replace(needle,"    text+='\\n第149轮少模型方向：两个RFF均值与Huber组合，124合成/372冷检查及零Ridge权重参考预测相等已通过；25个年度状态的子集核验、完整历史回放和128项评分接收流程仍待准备，尚无质量分。\\n'\n"+needle)
 p=A/'monitor_actual_chronological_optimization_progress_v36_20261008.py';compile(s,str(p),'exec')
 with p.open('x',encoding='utf8',newline='') as f:f.write(s)
 from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
 pins={str(p):sha(p),str(Path(__file__)):sha(__file__)};row=start('actual_chronological_optimization_progress_observer_v36_20261008',p.name,[],pins)
 create(A/'latest_actual_optimization_progress_pointer_v36_20261008.json',{'json':str(A/'optimization_live_progress_v36_20261008.json'),
  'markdown':str(A/'optimization_live_progress_v36_20261008.md'),'launch':row,'input_sha256':pins,'new_quality_scores':0});print(row['owned_worker_pid'],flush=True)
if __name__=='__main__':main()
