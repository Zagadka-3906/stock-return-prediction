"""Add the exact compiled48 normalization and qualifier helpers to the single live observer."""
from pathlib import Path
import sys,subprocess,psutil
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service,retire
def main():
    assert allowed();source=A/'monitor_fast_optimization_v87_20261011.py';text=source.read_text(encoding='utf8')
    jobs=['actual_stock_rank20seed10_embedding48_after185_normalization_queue_v1_20261011','StockRank20Seed10Embedding48_selected_native14_v1_20261011',
        'actual_Seed10_complete48_sources_main_v1_20261011','actual_Seed10_complete48_source_capsules_main_v2_20261011']
    marker='    while True:';assert text.count(marker)==1;text=text.replace(marker,'    jobs += '+repr(jobs)+'\n'+marker)
    marker="        p=A/'optimization_live_progress_v87_20261010.md'";assert text.count(marker)==1
    extra="""        lines.append(f"新种子48项统一选模：175/185两个完整锚点与17+29官方记录；11项父方案回调CPU检查已通过；归一化{services['actual_stock_rank20seed10_embedding48_after185_normalization_queue_v1_20261011']['status']}、选中原生14项{services['StockRank20Seed10Embedding48_selected_native14_v1_20261011']['status']}；完整186轮未来流程尚未建立，未派发未来推理。")
        lines.append(f"48项源码发布恢复2：{services['actual_Seed10_complete48_source_capsules_main_v2_20261011']['status']}；原Windows大小写文件名冲突失败回执保留，未重启任何训练或评分。")
"""
    text=text.replace(marker,extra+marker).replace('optimization_live_progress_v87','optimization_live_progress_v88').replace('actual_optimization_fast_runtime_handoff_v148','actual_optimization_fast_runtime_handoff_v151').replace('high_impact_additional_validation_rankings_v59','high_impact_additional_validation_rankings_v60')
    driver=A/'monitor_fast_optimization_v88_20261011.py';assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
    row=read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_v87_20261011/native_launch.json');assert not psutil.Process(row['owned_worker_pid']).children()
    spy=A.parent/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'
    stack=subprocess.run([str(spy),'dump','--pid',str(row['owned_worker_pid'])],capture_output=True,text=True,encoding='utf8',check=True).stdout
    assert '(idle)' in stack and 'main (monitor_fast_optimization_v87_20261011.py:' in stack
    create(A/'observer87_exact_idle_before88_v1_20261011.json',{'status':'verified_exact_childless_idle_observer','stack':stack,'identity':row})
    retire(row,'Verified idle observer replaced with exact seed10 normalization/native14/source-publication recovery states; no scientific workers terminated')
    assert allowed();new=start_service('actual_fast_optimization_progress_v88_20261011',driver.name,[],{str(driver):sha(driver)})
    create(A/'actual_fast_optimization_progress_v88_20261011_activation.json',new)
    print({'observer88':'started','scientific_workers_terminated':0},flush=True)
if __name__=='__main__':main()
