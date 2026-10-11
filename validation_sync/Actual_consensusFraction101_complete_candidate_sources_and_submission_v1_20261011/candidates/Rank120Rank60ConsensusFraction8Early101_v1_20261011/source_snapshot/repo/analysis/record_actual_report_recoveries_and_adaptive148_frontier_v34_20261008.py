"""Replace stale failed operational pointers with actual recovered services; preserve all failures."""
from pathlib import Path
import sys,time,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
 inputs=[Path(__file__),A/'actual145_report_parent_recovery_preparation_v3_20261008.json',A/'actual145_report_parent_binding_v3_20261008.json',
  A/'actual146_recovered145_gate_and_report_preflight_v4_20261008.json',A/'actual146_full_context_receiver_preparation_v5_20261008.json',
  A/'JointCrossHuberOrder185_prospective_routes_v2_20261008.json',A/'AdaptiveJointCrossHuber242_round148_proposal_v1_20261008.json',
  A/'AdaptiveJointCrossHuber148_historical_hidden_launches_v2_20261008.json',A/'actual_AdaptiveJointCrossHuber238_synthetic_location_v2_20261008.json',
  A/'CrossFamilyFine125_selected_release_v1_20261008/inference_ready.json',A/'CrossFamilyFine125_selected_release_v1_20261008/selected_candidate_ready_for_registration.json']
 ready=read(inputs[-2]);assert ready['actual_saved_native_models']==22 and ready['new_inference_claimed']
 synthetic=Path(read(inputs[-3])['output'])/'verification.json';s=read(synthetic)
 assert s['actual_cases']==238 and s['actual_cold_cases']==714 and s['actual_double_stage_order_pairs']==108
 inputs.append(synthetic)
 create(A/'actual_optimization_checkpoint_v34_20261008.json',{'status':'actual145_native_candidate_sealed_report_recovery_running_and_joint147_prospective2_adaptive148_synthetic238_passed',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'deadline_local':'2026-10-10T23:59:00+08:00','input_sha256':{str(p):sha(p) for p in inputs},
  'actual145_score':ready['best']['connected_final_score'],'actual145_physical_models':22,'actual145_genuine_native_independent_reload_CSV_cold80_and_sealing_passed':True,
  'actual145_original_registration_failure_retained_and_report_previous_binding_recovered':True,
  'actual145_full_QA_and_main_not_yet_claimed':True,'current_actual145_full_service':'CrossFamilyFine125_round145_full_registration_v3_20261008',
  'current_actual146_dispatch':'HuberCrossFamilyFine146_complete_chronological_dispatch_v6_20261008',
  'current_actual_benchmark_service':'actual_full_board_deferred_serialization_benchmark_v3_20261008',
  'actual147_fresh32_prospective_routes_include_all_four_explicit_module_previous_paths':True,
  'actual148_synthetic_cases':238,'actual148_cold_synthetic_cases':714,'actual148_order_pairs':108,
  'actual148_native80_and_full238_only_queued_after147_full':True,'actual148_complete_quality_receivers_not_yet_prepared':True,
  'actual147_and148_official_scores_at_record':0,'new_quality_scores_by_checkpoint':0,'test_labels_read':False,'goal_or_compute_exhaustion_claimed':False})
 old=A/'monitor_actual_chronological_optimization_progress_v33_20261008.py';text=old.read_text(encoding='utf8')
 for before,after in [('optimization_live_progress_v33','optimization_live_progress_v34'),('CrossFamilyFine125_round145_full_registration_v2','CrossFamilyFine125_round145_full_registration_v3'),
  ('HuberCrossFamilyFine146_complete_chronological_dispatch_v4','HuberCrossFamilyFine146_complete_chronological_dispatch_v6'),
  ('actual_full_board_deferred_serialization_benchmark_v2','actual_full_board_deferred_serialization_benchmark_v3'),
  ('JointCrossHuber147_complete_prospective_controls_v1','JointCrossHuber147_complete_prospective_controls_v2'),('JointCrossHuber147_complete_chronological_dispatch_v1','JointCrossHuber147_complete_chronological_dispatch_v2')]:text=text.replace(before,after)
 needle="    write(A/'optimization_live_progress_v34_20261008.json'";assert text.count(needle)==1
 extra="""    adaptive=Path('E:/赛题五_本机临时/AdaptiveJointCrossHuber238_parent134_historical_v1_20261008')
    state['adaptive148_frontier']={'expected_quality_cases':242,'new_configuration_cases':238,
        'synthetic238':status('AdaptiveJointCrossHuber238_actual_synthetic_controls_v2_20261008'),
        'native80':status('AdaptiveJointCrossHuber80_native_historical_calendar_controls_v2_20261008'),
        'full238':status('AdaptiveJointCrossHuber238_actual_full_historical_controls_v2_20261008'),
        'native_and_full_wait_for_actual147_full':True,'actual_full_control_records':len(list(adaptive.glob('case*.json'))),
        'actual148_official_scores':0,'complete_quality_receivers_not_yet_prepared':True,'new_model_fits':0,'actual_future_inference':0}
"""
 # Actual recovered full238 output is version1 by its immutable original receiver; verify the queued source path independently.
 full_source=(A/'verify_AdaptiveJointCrossHuber238_full_historical_controls_v2_20261008.py').read_text(encoding='utf8')
 import ast
 tree=ast.parse(full_source);out=next(n.value.args[0].value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='OUT' for t in n.targets))
 extra=extra.replace('E:/赛题五_本机临时/AdaptiveJointCrossHuber238_parent134_historical_v1_20261008',out)
 text=text.replace(needle,extra+needle)
 needle="    write(A/'optimization_live_progress_v34_20261008.md',text)";assert text.count(needle)==1
 text=text.replace(needle,"    text+='\\n第148轮扩展低比例联合方案：238项合成及714冷检查已通过，80原生和238完整历史控制排在147完成之后；242项正式评分流程仍待准备。\\n'\n"+needle)
 p=A/'monitor_actual_chronological_optimization_progress_v34_20261008.py';compile(text,str(p),'exec')
 with p.open('x',encoding='utf8',newline='') as f:f.write(text)
 from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
 pins={str(p):sha(p),str(Path(__file__)):sha(__file__)};row=start('actual_chronological_optimization_progress_observer_v34_20261008',p.name,[],pins)
 create(A/'latest_actual_optimization_progress_pointer_v34_20261008.json',{'json':str(A/'optimization_live_progress_v34_20261008.json'),
  'markdown':str(A/'optimization_live_progress_v34_20261008.md'),'launch':row,'input_sha256':pins,'new_quality_scores':0})
 print(row['owned_worker_pid'],flush=True)
if __name__=='__main__':main()
