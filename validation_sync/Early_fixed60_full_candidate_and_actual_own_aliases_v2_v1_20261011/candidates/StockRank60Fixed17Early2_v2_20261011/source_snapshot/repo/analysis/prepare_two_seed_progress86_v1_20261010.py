"""Add actual ensemble service and scores to the single live progress observer."""
from pathlib import Path
import sys,subprocess,psutil
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service,retire
def main():
    assert allowed();source=A/'monitor_fast_optimization_v85_20261010.py';text=source.read_text(encoding='utf8')
    marker='    while True:';assert text.count(marker)==1
    text=text.replace(marker,"    jobs += ['actual_rank20_two_seed_after175_complement49_screen_v1_20261010','actual_Rank20_two_seed_stages_main_v1_20261010']\n    families += ['StockRank20TwoSeed_after175_complement49_screen_v1_20261010']\n"+marker)
    marker="        p=A/'optimization_live_progress_v85_20261010.md'";assert text.count(marker)==1
    extra="""        ensemble=summaries.get('StockRank20TwoSeed_after175_complement49_screen_v1_20261010',{})
        lines.append(f"20日排名双独立种子集成：已评分{ensemble.get('completed_cases',0)}/49；TRAIN最高S={ensemble.get('best',{}).get('connected_final_score')}；3组独立标量、12前缀、3未来扰动与5错误输入拒绝CPU检查已通过；完整资格仍待实际回执。")
"""
    text=text.replace(marker,extra+marker).replace('optimization_live_progress_v85','optimization_live_progress_v86').replace('actual_optimization_fast_runtime_handoff_v143','actual_optimization_fast_runtime_handoff_v145').replace('high_impact_additional_validation_rankings_v57','high_impact_additional_validation_rankings_v58')
    driver=A/'monitor_fast_optimization_v86_20261010.py';assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
    row=read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_v85_20261010/native_launch.json')
    assert not psutil.Process(row['owned_worker_pid']).children()
    spy=A.parent/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'
    stack=subprocess.run([str(spy),'dump','--pid',str(row['owned_worker_pid'])],capture_output=True,text=True,encoding='utf8',check=True).stdout
    assert 'main (monitor_fast_optimization_v85_20261010.py:' in stack and '(idle)' in stack
    create(A/'observer85_exact_idle_before86_v1_20261010.json',{'status':'verified_exact_childless_idle_observer','stack':stack,'identity':row})
    retire(row,'Verified idle observer replaced with additive independent two-seed ensemble states; no scientific task terminated')
    assert allowed();new=start_service('actual_fast_optimization_progress_v86_20261010',driver.name,[],{str(driver):sha(driver)})
    create(A/'actual_fast_optimization_progress_v86_20261010_activation.json',new)
    print({'observer86':'started','scientific_workers_terminated':0},flush=True)
if __name__=='__main__':main()
