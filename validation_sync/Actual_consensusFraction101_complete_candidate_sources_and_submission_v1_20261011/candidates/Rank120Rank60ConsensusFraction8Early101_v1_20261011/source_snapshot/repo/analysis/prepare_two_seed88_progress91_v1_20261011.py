"""Extend the single observer with88 normalization, selected controls and actual11 callback source publication."""
from pathlib import Path
import sys,time,subprocess,psutil
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service,retire

def main():
    assert allowed();source=A/'monitor_fast_optimization_v90_20261011.py';text=source.read_text(encoding='utf8')
    jobs=['actual_rank20_two_seed88_after186_normalization_v1_20261011','actual_rank20_two_seed88_selected_native14_v1_20261011',
        'actual_Rank20_two_seed88_sources_controls_stages_main_v1_20261011','actual_Rank20_two_seed88_actual_parent_callbacks11_main_v1_20261011']
    marker='    while True:';assert text.count(marker)==1;text=text.replace(marker,'    jobs += '+repr(jobs)+'\n'+marker)
    marker="        p=A/'optimization_live_progress_v90_20261010.md'";assert text.count(marker)==1
    extra="""        state['two_seed_complete88']={'normalization':services['actual_rank20_two_seed88_after186_normalization_v1_20261011'],'selected_native14':services['actual_rank20_two_seed88_selected_native14_v1_20261011'],'source_main':services['actual_Rank20_two_seed88_sources_controls_stages_main_v1_20261011'],'callback_CPU_count':11,'callback_main':services['actual_Rank20_two_seed88_actual_parent_callbacks11_main_v1_20261011'],'expected_records':88,'full187_pipeline_pending':True}
        write(A/'optimization_live_progress_v91_20261010.json',state);write(A/'actual_optimization_fast_runtime_handoff_v158_20261011.json',state)
        lines.append(f"双种子88项统一比较：49项CDF、37项头部保护与175/186锚点；归一化{services['actual_rank20_two_seed88_after186_normalization_v1_20261011']['status']}，选中原生14项{services['actual_rank20_two_seed88_selected_native14_v1_20261011']['status']}；11项实际父回调CPU验证已通过，完整187轮候选与榜单流程待建立，未读取未来X。")
"""
    text=text.replace(marker,extra+marker).replace('optimization_live_progress_v90','optimization_live_progress_v91').replace('actual_optimization_fast_runtime_handoff_v155','actual_optimization_fast_runtime_handoff_v158').replace('high_impact_additional_validation_rankings_v62','high_impact_additional_validation_rankings_v63')
    driver=A/'monitor_fast_optimization_v91_20261011.py';assert not driver.exists();compile(text,str(driver),'exec')
    row=read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_v90_20261011/native_launch.json')
    spy=A.parent/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'
    for attempt in range(10):
        assert allowed() and owned(row) and not psutil.Process(row['owned_worker_pid']).children()
        stack=subprocess.run([str(spy),'dump','--pid',str(row['owned_worker_pid'])],capture_output=True,text=True,encoding='utf8',check=True).stdout
        if '(idle)' in stack and 'main (monitor_fast_optimization_v90_20261011.py:' in stack:break
        time.sleep(2)
    else:raise RuntimeError('Observer not verified idle; no retirement performed')
    driver.write_text(text,encoding='utf8',newline='\n')
    create(A/'observer90_exact_idle_before91_v1_20261011.json',{'status':'verified_exact_childless_idle_observer','identity':row,'stack':stack})
    retire(row,'Replace only verified idle observer with actual two-seed88 services and CPU11 evidence; scientific workers untouched')
    assert allowed();name='actual_fast_optimization_progress_v91_20261011'
    new=start_service(name,driver.name,[],{str(driver):sha(driver)})
    create(A/(name+'_activation.json'),new)
    print({'observer91_started':True,'scientific_workers_terminated':0},flush=True)

if __name__=='__main__':main()
