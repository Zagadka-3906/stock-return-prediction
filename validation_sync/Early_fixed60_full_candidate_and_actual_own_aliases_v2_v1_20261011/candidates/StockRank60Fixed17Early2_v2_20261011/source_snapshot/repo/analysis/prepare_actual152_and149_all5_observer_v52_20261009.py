"""Expose the actual152 frontier and current149 all5-year dispatcher."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def main():
 old=A/'monitor_actual_chronological_optimization_progress_v51_20261009.py'
 new=A/'monitor_actual_chronological_optimization_progress_v52_20261009.py'
 s=old.read_text(encoding='utf8').replace('optimization_live_progress_v51_','optimization_live_progress_v52_')
 s=s.replace('PureRFFHuber149_complete_chronological_dispatch_v6_20261009','PureRFFHuber149_complete_chronological_dispatch_v7_20261009')
 needle="    write(A/'optimization_live_progress_v52_20261009.json',"
 assert s.count(needle)==1
 extra="""    state['adaptive148_frontier']['actual_future_inference']=int(pipeline['148']['selected_candidate']['status']=='passed')
    state['adaptive148_frontier']['actual_selected_two_full_native_replays_and_sealing_completed']=pipeline['148']['candidate_sealing']['status']=='passed'
    annual=A/'Pure149_all25_annual_native_coverage_v1_20261009.json'
    state['pure149_frontier'].update(additional2023_native=status('PureRFFHuber20_year2023_native_supplement_v1_20261009'),all5_annual_coverage=status('PureRFFHuber25_all5_annual_native_coverage_v1_20261009'))
    if annual.exists():
        actual=read(annual)
        state['pure149_frontier'].update(actual_all5_annual_states=actual['actual_head_year_states'],actual_native_controls=actual['actual_native_cases'],actual_cold_native_controls=actual['actual_cold_cases'])
    native152=Path('E:/赛题五_本机临时/SparseAfter14860_native_historical_calendar_v1_20261009')
    full152=Path('E:/赛题五_本机临时/SparseAfter14825_parent148_historical_v1_20261009')
    state['sparse_after148_152_frontier']={'stage_base_round':148,'expected_quality_cases':29,'actual_official_scores':0,
        'synthetic25_and75_prefixes_and10_saved_state_metadata_passed':True,
        'native60':status('SparseAfter14860_native_historical_calendar_controls_v1_20261009'),
        'actual_native_control_records':len(list(native152.glob('control*.json'))),'expected_native_controls':60,
        'full25':status('SparseAfter14825_full_historical_controls_v1_20261009'),
        'actual_full_control_records':len(list(full152.glob('case*.json'))),'expected_full_control_records':25,
        'actual_complete148_predictor_adapter_ABI_passed':(A/'SparseAfter148152_complete_native_predictor_preparation_v1_20261009.json').is_file(),
        'complete_quality_receivers_and_prior_duplicate_audit_still_required':True,
        'historical_main':status('actual149_all5_and152_historical_main_publication_v52_20261009'),
        'new_native_fits':0,'actual_future_X_read':False,'test_labels_read':False}
"""
 s=s.replace(needle,extra+needle)
 needle="    write(A/'optimization_live_progress_v52_20261009.md',text)"
 assert s.count(needle)==1
 text="""    frontier=state['sparse_after148_152_frontier']
    text+=f"\\n第152轮在完整148后叠加单独稀疏修正：25合成/75前缀及10年度状态元数据已通过；真实原生回放{frontier['actual_native_control_records']}/60（{frontier['native60']['status']}），完整历史控制{frontier['actual_full_control_records']}/25（{frontier['full25']['status']}）；完整148预测器接口检查已通过。仍需完整评分接收预检查及训练期官方29项评分，尚无质量分。\\n"
"""
 s=s.replace(needle,text+needle);compile(s,str(new),'exec')
 with new.open('x',encoding='utf8') as f:f.write(s)
 meta=A/'actual152_and149_all5_observer_preparation_v52_20261009.json'
 pins={str(p):sha(p) for p in [Path(__file__),old,new,A/'Pure149_all5_annual_native_receiver_binding_v8_20261009.json',
  A/'SparseAfter14829_round152_proposal_v1_20261009.json']}
 create(meta,{'status':'prepared_actual152_frontier_and149_all5_current_service_observer',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'no_scientific_changes':True})
 from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
 row=start('actual_chronological_optimization_progress_observer_v52_20261009',new.name,[],{**pins,str(meta):sha(meta)})
 create(A/'actual152_and149_all5_observer_hidden_launch_v52_20261009.json',row)
 for _ in range(30):
  if (A/'optimization_live_progress_v52_20261009.json').exists():break
  time.sleep(1)
 else:raise RuntimeError('New52 observer failed to publish actual progress')
 assert owned(row)
 previous=read(A/'service_owned_workflows_20261006/actual_chronological_optimization_progress_observer_v51_20261009/native_launch.json')
 from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle,retire_suspended
 line=next(i for i,l in enumerate(old.read_text(encoding='utf8').splitlines(),1) if l.strip()=='time.sleep(45)')
 parent,worker,idle=suspended_idle(previous,'    main ('+old.name+':'+str(line)+')')
 retire_suspended(previous,row)
 create(A/'actual_old_progress51_retired_after52_v1_20261009.json',{
  'status':'retired_only_owned_childfree_idle_observer_after_actual52_output',
  'identity':previous,'idle':idle,'successor':row,'scientific_workers_stopped':0})
 create(A/'latest_actual_optimization_progress_pointer_v52_20261009.json',{
  'status':'actual_current_progress','json':str(A/'optimization_live_progress_v52_20261009.json'),
  'markdown':str(A/'optimization_live_progress_v52_20261009.md'),'actual_observer':row})
 print({'observer':row['owned_worker_pid'],'progress':str(A/'optimization_live_progress_v52_20261009.md')},flush=True)
if __name__=='__main__':main()
