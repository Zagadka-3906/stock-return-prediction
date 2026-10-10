"""Observe actual504 normalization/native48 and188 dispatcher routing while preserving the retired source dispatcher."""
from pathlib import Path
import sys,time,subprocess,psutil
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service,retire

def main():
    assert allowed();source=A/'monitor_fast_optimization_v92_20261011.py';text=source.read_text(encoding='utf8')
    jobs=['actual_stock_rank20long_embedding48_after187_normalization_queue_v1_20261011','StockRank20LongEmbedding48_selected_native14_v1_20261011',
        'StockRank20LongEmbedding188_complete48_family_v1_20261011','StockRank20LongEmbedding188_complete48_family_actual_queue_v2_20261011',
        'actual_StockRank20Long188_source_capsules_main_v1_20261011',
        'StockRank20LongEmbedding188_selected_candidate_preparation_v1_20261010','StockRank20LongEmbedding188_selected_candidate_sealing_v1_20261010',
        'StockRank20LongEmbedding188_round188_full_registration_v1_20261010']
    marker='    while True:';assert text.count(marker)==1;text=text.replace(marker,'    jobs += '+repr(jobs)+'\n'+marker)
    marker="        actual_aliases.update(read(A/'PairTop184185_complete_reference_routes_v9_20261010.json')['service_aliases'])";assert text.count(marker)==1
    text=text.replace(marker,marker+"\n        actual_aliases.update(read(A/'long188_actual_scientific_queue_routes_v2_20261011.json')['service_aliases'])")
    marker="        p=A/'optimization_live_progress_v92_20261010.md'";assert text.count(marker)==1
    extra="""        state['long504_complete188']={'normalization':services['actual_stock_rank20long_embedding48_after187_normalization_queue_v1_20261011'],'selected_native14':services['StockRank20LongEmbedding48_selected_native14_v1_20261011'],'actual_family':services['StockRank20LongEmbedding188_complete48_family_actual_queue_v2_20261011'],'sources_main':services['actual_StockRank20Long188_source_capsules_main_v1_20261011'],'actual_callback_CPU_count':11,'expected_records':48,'expected_full_board':17538,'QA':99,'training_calendar_window':504,'fully_qualified':(A/'github_validation_sync_main_20261005/round188_receipt.json').exists()}
        write(A/'optimization_live_progress_v93_20261010.json',state);write(A/'actual_optimization_fast_runtime_handoff_v164_20261011.json',state)
        lines.append(f"504日完整188轮48项/QA99：11项实际CPU父回调通过；归一化{services['actual_stock_rank20long_embedding48_after187_normalization_queue_v1_20261011']['status']}，选中原生14项{services['StockRank20LongEmbedding48_selected_native14_v1_20261011']['status']}，实际候选/登记流程{services['StockRank20LongEmbedding188_complete48_family_actual_queue_v2_20261011']['status']}，源码main{services['actual_StockRank20Long188_source_capsules_main_v1_20261011']['status']}；已核实真实504训练队列，只替换闲置派发助手，训练和评分未重启。")
"""
    text=text.replace(marker,extra+marker).replace('optimization_live_progress_v92','optimization_live_progress_v93').replace('actual_optimization_fast_runtime_handoff_v161','actual_optimization_fast_runtime_handoff_v164').replace('high_impact_additional_validation_rankings_v64','high_impact_additional_validation_rankings_v65')
    driver=A/'monitor_fast_optimization_v93_20261011.py';assert not driver.exists();compile(text,str(driver),'exec')
    row=read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_v92_20261011/native_launch.json')
    spy=A.parent/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'
    for attempt in range(10):
        assert allowed() and owned(row) and not psutil.Process(row['owned_worker_pid']).children()
        stack=subprocess.run([str(spy),'dump','--pid',str(row['owned_worker_pid'])],capture_output=True,text=True,encoding='utf8',check=True).stdout
        if '(idle)' in stack and 'main (monitor_fast_optimization_v92_20261011.py:' in stack:break
        time.sleep(2)
    else:raise RuntimeError('Observer not verified idle; no retirement performed')
    driver.write_text(text,encoding='utf8',newline='\n')
    create(A/'observer92_exact_idle_before93_v1_20261011.json',{'status':'verified_exact_childless_idle_observer','identity':row,'stack':stack})
    retire(row,'Replace only verified idle observer with actual504 complete188 source and dependency evidence; scientific workers untouched')
    assert allowed();name='actual_fast_optimization_progress_v93_20261011';new=start_service(name,driver.name,[],{str(driver):sha(driver)})
    create(A/(name+'_activation.json'),new)
    print({'observer93_started':True,'scientific_workers_terminated':0},flush=True)

if __name__=='__main__':main()
