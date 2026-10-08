"""Publish completed124 synthetic controls and proposed lower-model frontier, with no native/quality claim."""
from pathlib import Path
import sys,time,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save
def main():
 original=A/'publish_actual145_148_and_RAM_main_v33_20261008.py';s=original.read_text(encoding='utf8')
 for before,after in [('actual145_148_and_RAM_main_v33_20261008','actual_PureRFF149_controls_main_v34_20261008'),
  ('actual145_148_and_RAM_main_v33_receipt_20261008','actual_PureRFF149_controls_main_v34_receipt_20261008'),
  ('actual145_joint148_and_RAM_boundary_v33_20261008','actual_PureRFF149_synthetic_and_proposed_lower_models_v34_20261008'),
  ('actual_joint147_preparation_and_storage_main_publication_v31_20261008','actual145_148_and_RAM_main_publication_v33_20261008')]:s=s.replace(before,after)
 s=s.replace('datetime.datetime(2026,10,8,21,32)','datetime.datetime(2026,10,8,21,38)')
 needle='  sources.extend(p for p in A.iterdir()';assert s.count(needle)==1
 s=s.replace(needle,"  sources += [A/'actual_optimization_checkpoint_v36_20261008.json',A/'PureRFFHuber128_round149_proposal_v1_20261008.json',A/'PureRFFHuber149_synthetic_receiver_recovery_v2_20261008.json']\n"+needle)
 s=s.replace("'actual_AdaptiveJointCrossHuber238_synthetic_location_v2_20261008.json'):","'actual_AdaptiveJointCrossHuber238_synthetic_location_v2_20261008.json','actual_PureRFFHuber124_synthetic_location_v2_20261008.json'):")
 s=s.replace("'new_quality_scores_by_publication':0", "'actual149_synthetic_cases':124,'actual149_synthetic_cold_cases':372,'actual149_zero_Ridge_reference_forecast_bits_equal':True,'actual149_native25_subset_audit_and_historical_full_and_quality_receivers_still_pending':True,'actual149_official_scores':0,'actual149_future_inference':0,'new_quality_scores_by_publication':0")
 s=s.replace('同步145轮正式最佳、148轮完整预检及实际内存边界，保留失败记录','同步149轮少模型方向124项合成与372项冷检查，历史评分与推理尚未执行')
 target=save('publish_actual_PureRFF149_controls_main_v34_20261008.py',s)
 meta=A/'actual_PureRFF149_controls_main_preparation_v34_20261008.json'
 create(meta,{'status':'prepared_main_publication_of_actual124_synthetic_controls_and_lower_head_proposal_after_actual33',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in [Path(__file__),original,target]},'new_quality_scores':0,'test_labels_read':False})
 from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
 row=start('actual_PureRFF149_controls_main_publication_v34_20261008',target.name,[],{str(p):sha(p) for p in [Path(__file__),target,meta]})
 create(A/'actual_PureRFF149_controls_main_hidden_launch_v34_20261008.json',row);print(row['owned_worker_pid'],flush=True)
if __name__=='__main__':main()
