"""Prepare the complete134-parent two-replay/cold80 adapter for the explicit joint stage; no future X read."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
def main():
 old=A/'predict_HuberCrossFamilyFine_complete_parent_scheme_v1_20261008.py';target=A/'predict_JointCrossHuber_complete_parent_scheme_v1_20261008.py'
 s=old.read_text(encoding='utf8').replace('HuberCrossFamily','JointCrossHuber')
 s=s.replace('from JointCrossHuberFine_complete_parent_native_stage_v1_20261008 import after_parent,GRAPH_KEY',
  'from JointCrossHuber_ordered_native_stage_v1_20261008 import after_parent,GRAPH_KEY')
 before="assert all(row['native_reload_independent_arithmetic_and_Pandas_complete_parent_CDF_bits_exact'] for row in calls)"
 after="assert all(row['all_stage_native_reload_independent_and_Pandas_bits_checked'] for row in calls)"
 assert s.count(before)==1;s=s.replace(before,after)
 before="next(row for row in source_report['controls'] if row['head']==component['head'])"
 after="next(row for stage in source_report['stage_reports'] for row in stage['native_reload_independent_and_Pandas_report']['controls'] if row['head']==component['head'])"
 assert s.count(before)==1;s=s.replace(before,after)
 assert "assert len(full)>=2 and len(cold)>=1" in s
 assert "assert len({value['sha256'] for value in result['models'].values()})==len(result['models'])" in s
 compile(s,str(target),'exec')
 with target.open('x',encoding='utf8',newline='') as f:f.write(s)
 create(A/'JointCrossHuber_complete_native_predictor_preparation_v1_20261008.json',{
  'status':'prepared_complete134_backend_joint_native_predictor_two_full_replays_and_cold80_not_executed',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in [Path(__file__),old,target,A/'JointCrossHuber_ordered_native_stage_v1_20261008.py']},
  'all_original_parent_backend_routes_preserved':True,'new_joint_report_accessors_preserve_every_original_stage_native_control':True,
  'physical_models_deduplicated_by_actual_native_SHA':True,'new_quality_scores':0,'new_future_inference':0,'test_labels_read':False})
 print('Complete native joint adapter compiled; no future inference executed.',flush=True)
if __name__=='__main__':main()
