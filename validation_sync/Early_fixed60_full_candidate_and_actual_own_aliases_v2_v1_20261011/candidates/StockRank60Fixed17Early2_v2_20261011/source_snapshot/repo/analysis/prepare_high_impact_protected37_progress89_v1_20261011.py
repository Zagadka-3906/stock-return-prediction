"""Extend the single live observer with the new protected-tail experiment and actual long-window worker."""
from pathlib import Path
import sys,subprocess,time,psutil
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service,retire

def main():
    assert allowed()
    source=A/'monitor_fast_optimization_v88_20261011.py';text=source.read_text(encoding='utf8')
    jobs=['actual_rank20_two_seed_after175_protected_tail37_screen_v1_20261011',
        'actual_Rank20_two_seed_protected37_stages_main_v1_20261011',
        'actual_rank20_two_seed_protected_selected_native14_v1_20261011',
        'actual_Rank20_two_seed_protected_native14_stages_main_v1_20261011',
        'actual_stock_rank20long_embedding_small512_restart_v1_20261010',
        'actual_stock_rank20long_embedding_small512_bank6_v1_20261010']
    family='StockRank20TwoSeed_after175_protected_tail37_screen_v1_20261011'
    marker='    while True:';assert text.count(marker)==1
    text=text.replace(marker,'    jobs += '+repr(jobs)+'\n    families += ['+repr(family)+']\n'+marker)
    marker="        p=A/'optimization_live_progress_v88_20261010.md'";assert text.count(marker)==1
    extra="""        protected=summaries.get('StockRank20TwoSeed_after175_protected_tail37_screen_v1_20261011',{})
        state['two_seed_protected_tail37']={'progress':protected,'planned_cases':37,'new_training_by_screen':0,'selected_native14_status':services['actual_rank20_two_seed_protected_selected_native14_v1_20261011']['status'],'submission_qualified':False}
        lines.append(f"双种子大权重及头部保护37项：实际评分{protected.get('completed_cases',0)}/37，TRAIN最高S={protected.get('best',{}).get('connected_final_score')}；仅复用已有独立年度模型，选中方案原生14项{services['actual_rank20_two_seed_protected_selected_native14_v1_20261011']['status']}，完整未来提交资格待完成。")
        lines.append(f"504日模型实际GPU重启{services['actual_stock_rank20long_embedding_small512_restart_v1_20261010']['status']}，年度训练服务{services['actual_stock_rank20long_embedding_small512_bank6_v1_20261010']['status']}；新分数尚未生成，资源等待不计为训练完成。")
        write(A/'optimization_live_progress_v89_20261010.json',state);write(A/'actual_optimization_fast_runtime_handoff_v153_20261011.json',state)
"""
    text=text.replace(marker,extra+marker)
    text=text.replace('optimization_live_progress_v88','optimization_live_progress_v89')
    text=text.replace('actual_optimization_fast_runtime_handoff_v151','actual_optimization_fast_runtime_handoff_v153')
    text=text.replace('high_impact_additional_validation_rankings_v60','high_impact_additional_validation_rankings_v61')
    text=text.replace('；GPU队列等待实际双种子84项原生检查。','；实际GPU阶段见下方服务状态。')
    driver=A/'monitor_fast_optimization_v89_20261011.py'
    assert not driver.exists();compile(text,str(driver),'exec')
    row=read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_v88_20261011/native_launch.json')
    spy=A.parent/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'
    for attempt in range(10):
        assert allowed() and owned(row) and not psutil.Process(row['owned_worker_pid']).children()
        stack=subprocess.run([str(spy),'dump','--pid',str(row['owned_worker_pid'])],capture_output=True,text=True,encoding='utf8',check=True).stdout
        if '(idle)' in stack and 'main (monitor_fast_optimization_v88_20261011.py:' in stack:break
        time.sleep(2)
    else:raise RuntimeError('Observer not verified idle; no mutation or retirement performed')
    driver.write_text(text,encoding='utf8',newline='\n')
    create(A/'observer88_exact_idle_before89_v1_20261011.json',{'status':'verified_exact_childless_idle_observer','stack':stack,'identity':row})
    retire(row,'Replace only verified idle observer with protected37 and actual long504 worker states; no scientific worker terminated')
    assert allowed()
    name='actual_fast_optimization_progress_v89_20261011'
    new=start_service(name,driver.name,[],{str(driver):sha(driver)})
    create(A/(name+'_activation.json'),new)
    print({'observer89_started':True,'scientific_workers_terminated':0},flush=True)

if __name__=='__main__':main()
