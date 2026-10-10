"""Observe actual187 dual-seed candidate, registration and source publication without rewriting old failures."""
from pathlib import Path
import sys,time,subprocess,psutil
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service,retire

def main():
    assert allowed();source=A/'monitor_fast_optimization_v91_20261011.py';text=source.read_text(encoding='utf8')
    jobs=['Rank20TwoSeed187_complete88_family_v2_20261011','actual_Rank20TwoSeed187_source_capsules_main_v1_20261011',
        'Rank20TwoSeed187_selected_candidate_preparation_v1_20261010','Rank20TwoSeed187_selected_candidate_sealing_v1_20261010',
        'Rank20TwoSeed187_round187_full_registration_v1_20261010']
    marker='    while True:';assert text.count(marker)==1;text=text.replace(marker,'    jobs += '+repr(jobs)+'\n'+marker)
    text=text.replace("'full187_pipeline_pending':True","'full187_pipeline_created':True,'full187_qualification_pending':True")
    text=text.replace('完整187轮候选与榜单流程待建立，未读取未来X。','完整187轮流程已建立；未来推理与完整资格以实际回执为准。')
    marker="        p=A/'optimization_live_progress_v91_20261010.md'";assert text.count(marker)==1
    extra="""        state['complete187_two_seed88']={'family':services['Rank20TwoSeed187_complete88_family_v2_20261011'],'sources_main':services['actual_Rank20TwoSeed187_source_capsules_main_v1_20261011'],'expected_records':88,'expected_full_board':17490,'QA':98,'physical_signal_models':2,'fully_qualified':(A/'github_validation_sync_main_20261005/round187_receipt.json').exists()}
        write(A/'optimization_live_progress_v92_20261010.json',state);write(A/'actual_optimization_fast_runtime_handoff_v161_20261011.json',state)
        lines.append(f"第187轮双物理种子88项/QA98：完整候选和榜单流程{services['Rank20TwoSeed187_complete88_family_v2_20261011']['status']}，源码main{services['actual_Rank20TwoSeed187_source_capsules_main_v1_20261011']['status']}；原路径替换准入失败保留，新版本只修复确切文件路由，未重跑训练或评分。")
"""
    text=text.replace(marker,extra+marker).replace('optimization_live_progress_v91','optimization_live_progress_v92').replace('actual_optimization_fast_runtime_handoff_v158','actual_optimization_fast_runtime_handoff_v161').replace('high_impact_additional_validation_rankings_v63','high_impact_additional_validation_rankings_v64')
    driver=A/'monitor_fast_optimization_v92_20261011.py';assert not driver.exists();compile(text,str(driver),'exec')
    row=read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_v91_20261011/native_launch.json')
    spy=A.parent/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'
    for attempt in range(10):
        assert allowed() and owned(row) and not psutil.Process(row['owned_worker_pid']).children()
        stack=subprocess.run([str(spy),'dump','--pid',str(row['owned_worker_pid'])],capture_output=True,text=True,encoding='utf8',check=True).stdout
        if '(idle)' in stack and 'main (monitor_fast_optimization_v91_20261011.py:' in stack:break
        time.sleep(2)
    else:raise RuntimeError('Observer not verified idle; no retirement performed')
    driver.write_text(text,encoding='utf8',newline='\n')
    create(A/'observer91_exact_idle_before92_v1_20261011.json',{'status':'verified_exact_childless_idle_observer','identity':row,'stack':stack})
    retire(row,'Replace only verified idle observer with created187 dual-seed candidate/QA98/source-main services; scientific workers untouched')
    assert allowed();name='actual_fast_optimization_progress_v92_20261011'
    new=start_service(name,driver.name,[],{str(driver):sha(driver)});create(A/(name+'_activation.json'),new)
    print({'observer92_started':True,'scientific_workers_terminated':0},flush=True)

if __name__=='__main__':main()
