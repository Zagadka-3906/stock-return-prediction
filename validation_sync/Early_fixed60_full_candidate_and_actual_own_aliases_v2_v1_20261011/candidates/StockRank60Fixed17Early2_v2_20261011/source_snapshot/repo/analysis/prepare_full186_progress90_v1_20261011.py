"""Observe the actually created186 workflow and preserve failed source-only publishers as failed."""
from pathlib import Path
import sys,time,subprocess,psutil
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service,retire

def main():
    assert allowed()
    source=A/'monitor_fast_optimization_v89_20261011.py';text=source.read_text(encoding='utf8')
    jobs=['StockRank20Seed10Embedding186_complete48_family_v2_20261011',
        'actual_Seed10_full186_source_capsules_main_v1_20261011',
        'actual_Seed10_full186_source_capsules_main_v2_20261011',
        'StockRank20Seed10Embedding186_selected_candidate_preparation_v1_20261010',
        'StockRank20Seed10Embedding186_selected_candidate_sealing_v1_20261010',
        'StockRank20Seed10Embedding186_round186_full_registration_v1_20261010']
    marker='    while True:';assert text.count(marker)==1
    text=text.replace(marker,'    jobs += '+repr(jobs)+'\n'+marker)
    marker="        p=A/'optimization_live_progress_v89_20261010.md'";assert text.count(marker)==1
    extra="""        state['independent_seed10_full186']={'actual_service':services['StockRank20Seed10Embedding186_complete48_family_v2_20261011'],'expected_records':48,'QA':97,'expected_full_board':17402,'source_admission_version':2,'source_publication_original_failed':services['actual_Seed10_full186_source_capsules_main_v1_20261011'],'source_publication_actual_v2':services['actual_Seed10_full186_source_capsules_main_v2_20261011'],'fully_qualified':(A/'github_validation_sync_main_20261005/round186_receipt.json').exists()}
        write(A/'optimization_live_progress_v90_20261010.json',state);write(A/'actual_optimization_fast_runtime_handoff_v155_20261011.json',state)
        lines.append(f"第186轮48项完整候选与QA97：流程{services['StockRank20Seed10Embedding186_complete48_family_v2_20261011']['status']}；源码main实际恢复v2{services['actual_Seed10_full186_source_capsules_main_v2_20261011']['status']}；候选推理、完整榜和全部资格以实际回执判定。此前未派发的源码准入断言与源码发布路径失败完整保留。")
"""
    text=text.replace(marker,extra+marker)
    text=text.replace('optimization_live_progress_v89','optimization_live_progress_v90')
    text=text.replace('actual_optimization_fast_runtime_handoff_v153','actual_optimization_fast_runtime_handoff_v155')
    text=text.replace('high_impact_additional_validation_rankings_v61','high_impact_additional_validation_rankings_v62')
    text=text.replace('完整186轮未来流程尚未建立，未派发未来推理。','完整186轮流程已建立；未来推理以实际回执为准。')
    driver=A/'monitor_fast_optimization_v90_20261011.py';assert not driver.exists();compile(text,str(driver),'exec')
    row=read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_v89_20261011/native_launch.json')
    spy=A.parent/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'
    for attempt in range(10):
        assert allowed() and owned(row) and not psutil.Process(row['owned_worker_pid']).children()
        stack=subprocess.run([str(spy),'dump','--pid',str(row['owned_worker_pid'])],capture_output=True,text=True,encoding='utf8',check=True).stdout
        if '(idle)' in stack and 'main (monitor_fast_optimization_v89_20261011.py:' in stack:break
        time.sleep(2)
    else:raise RuntimeError('Observer not verified idle; no retirement performed')
    driver.write_text(text,encoding='utf8',newline='\n')
    create(A/'observer89_exact_idle_before90_v1_20261011.json',{'status':'verified_exact_childless_idle_observer','identity':row,'stack':stack})
    retire(row,'Update only verified idle observer with created186 candidate pipeline and preserved source-publication failure; no scientific workers stopped')
    assert allowed()
    name='actual_fast_optimization_progress_v90_20261011';new=start_service(name,driver.name,[],{str(driver):sha(driver)})
    create(A/(name+'_activation.json'),new)
    print({'observer90_started':True,'scientific_workers_terminated':0},flush=True)

if __name__=='__main__':main()
