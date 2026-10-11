from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def main():
    old=A/'monitor_actual_chronological_optimization_progress_v55_20261009.py';new=A/'monitor_actual_chronological_optimization_progress_v56_20261009.py'
    s=old.read_text(encoding='utf8').replace('optimization_live_progress_v55_20261009','optimization_live_progress_v56_20261009')
    needle="    write(A/'optimization_live_progress_v56_20261009.json',";assert s.count(needle)==1
    addition="""    medium_full=Path('E:/赛题五_本机临时/BF16Medium153_full73_training_v1_20261009')
    medium_native=Path('E:/赛题五_本机临时/BF16Medium153_native42_calendar_v1_20261009')
    state['medium153_frontier']={'actual_stage_base_round':148,'quality_anchor_rounds':[148,149,150,151,152],
      'expected_quality_cases':78,'synthetic_cases':73,'synthetic_cold_cases':219,
      'actual_small_independent':status('BF16Medium153_independent_small_CPU_v1_20261009'),
      'actual_full5_independent':status('BF16Medium153_independent_full5_GPU_controls_v1_20261009'),
      'actual_full73':status('BF16Medium153_actual_full73_training_v1_20261009'),
      'actual_native42':status('BF16Medium153_actual_native42_calendar_v1_20261009'),
      'actual_full_case_records':len(list(medium_full.glob('case*.json'))),'actual_native_case_records':len(list(medium_native.glob('case*.json'))),
      'official_scores':0,'actual_future_X_read':False,'test_labels_read':False,
      'complete_quality_receivers_and_prospective_and_duplicate_checks_still_required':True}
"""
    s=s.replace(needle,addition+needle)
    needle="    write(A/'optimization_live_progress_v56_20261009.md',text)";assert s.count(needle)==1
    s=s.replace(needle,"    medium=state['medium153_frontier']\n    text+=f\"\\n第153轮：新中型神经网络叠加完整148方案，正负信号、3种群体、12种权重与零权重，共73个训练组合、5个父方案锚点；73合成/219前缀通过。完整历史控制{medium['actual_full_case_records']}/73，六状态原生控制{medium['actual_native_case_records']}/42。尚无正式质量分；完整接收流程、去重与前置轮次准入仍须完成。\\n\"\n"+needle)
    compile(s,str(new),'exec')
    with new.open('x',encoding='utf8') as f:f.write(s)
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    row=start('actual_chronological_optimization_progress_observer_v56_20261009',new.name,[],{str(new):sha(new)})
    create(A/'actual_medium153_progress_hidden_launch_v56_20261009.json',row)
    for _ in range(30):
        if (A/'optimization_live_progress_v56_20261009.json').exists():break
        time.sleep(1)
    else:raise AssertionError('No complete first snapshot')
    assert owned(row)
    create(A/'latest_actual_optimization_progress_pointer_v56_20261009.json',{'status':'actual_current_progress','json':str(A/'optimization_live_progress_v56_20261009.json'),'markdown':str(A/'optimization_live_progress_v56_20261009.md'),'actual_observer':row})
    from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle,retire_suspended,stack
    before=read(A/'service_owned_workflows_20261006/actual_chronological_optimization_progress_observer_v55_20261009/native_launch.json')
    if owned(before):
        line=next(line for line in stack(before['owned_worker_pid']).splitlines() if '    main (' in line)
        parent,worker,idle=suspended_idle(before,line)
        try:retire_suspended(before,row)
        except BaseException:
            if parent.is_running():parent.resume()
            if worker.is_running():worker.resume()
            raise
        create(A/'actual_medium153_progress_observer_handoff_v56_20261009.json',{'old':before,'new':row,'old_idle_stack':idle,'scientific_jobs_retired':0})
    print(row['owned_worker_pid'],flush=True)

if __name__=='__main__':main()
