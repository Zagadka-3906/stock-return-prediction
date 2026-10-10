"""Track the longer-history alternative and all pending actual two-seed controls in one observer."""
from pathlib import Path
import sys,subprocess,psutil
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service,retire
def main():
    assert allowed();source=A/'monitor_fast_optimization_v86_20261010.py';text=source.read_text(encoding='utf8')
    jobs=['StockRank20LongEmbedding_actual_mature_fixture_CPU_v1_20261010','actual_stock_rank20long_embedding_504_own64_controls46_queue_v1_20261011',
        'actual_stock_rank20long_embedding_small512_restart_v1_20261010','actual_stock_rank20long_embedding_small512_bank6_v1_20261010',
        'StockRank20LongEmbeddingSmall512_independent_full5_GPU_controls_v1_20261009','actual_stock_rank20long_embedding_six_state_native42_v1_20261010',
        'actual_stock_rank20long_embedding_after175_fast17_screen_v1_20261010','actual_stock_rank20long_embedding_after175_large_allocation29_screen_v1_20261010',
        'actual_StockRank20Long_504_objective_stages_main_v1_20261011','actual_rank20_two_seed_native84_v1_20261010',
        'actual_Rank20_two_seed_native84_stages_main_v2_20261010','actual_Rank20_two_seed_actual_weights_CPU_main_v3_20261010']
    families=['StockRank20LongEmbeddingSmall512_after175_high_impact17_screen_v1_20261010','StockRank20LongEmbeddingSmall512_after175_large_allocation29_screen_v1_20261010']
    marker='    while True:';assert text.count(marker)==1
    text=text.replace(marker,'    jobs += '+repr(jobs)+'\n    families += '+repr(families)+'\n'+marker)
    marker="        write(A/'optimization_live_progress_v86_20261010.json',state)";assert text.count(marker)==1
    extra="""        longbank=Path('E:/赛题五_本机临时/stock_rank20long_embedding_small512_BF16_bank6_v1_20261010')
        longinfos=[read(longbank/str(y)/'info.json') for y in range(2020,2026) if (longbank/str(y)/'info.json').exists()]
        state['rank20_long504']={'completed_annual_models':longinfos,'configuration':read(A/'stock_rank20long_embedding_own64_native_sources_preparation_v1_20261010.json')['configuration'],'actual_CPU504_truncation_and_mature_labels_passed':True,'submission_qualified':False}
"""
    text=text.replace(marker,extra+marker)
    marker="        p=A/'optimization_live_progress_v86_20261010.md'";assert text.count(marker)==1
    extra="""        lines.append(f"504日训练历史20日排名模型：实际年度模型{len(longinfos)}/6；840日期独立成熟标签、排名及504日截断CPU检查通过；真实49153样本服务{services['StockRank20LongEmbedding_actual_mature_fixture_CPU_v1_20261010']['status']}；GPU队列等待实际双种子84项原生检查。")
        lines.append(f"双种子原生84项/冷启动84项服务：{services['actual_rank20_two_seed_native84_v1_20261010']['status']}；六年度相同成熟样本与不同实际参数张量CPU证据main：{services['actual_Rank20_two_seed_actual_weights_CPU_main_v3_20261010']['status']}。")
"""
    text=text.replace(marker,extra+marker)
    text=text.replace('；实际阶段{','；历史阶段记录{').replace('；阶段{','；历史阶段记录{')
    text=text.replace('GPU训练优先等待174候选封装。','已完成状态以实际训练、原生及评分回执判定。')
    text=text.replace('分别等待当前61项完成/合格175，不重复训练。','官方完成状态以实际41项回执判定；复用既有年度权重。')
    text=text.replace('optimization_live_progress_v86','optimization_live_progress_v87').replace('actual_optimization_fast_runtime_handoff_v145','actual_optimization_fast_runtime_handoff_v148').replace('high_impact_additional_validation_rankings_v58','high_impact_additional_validation_rankings_v59')
    driver=A/'monitor_fast_optimization_v87_20261011.py';assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
    row=read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_v86_20261010/native_launch.json')
    assert not psutil.Process(row['owned_worker_pid']).children()
    spy=A.parent/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'
    stack=subprocess.run([str(spy),'dump','--pid',str(row['owned_worker_pid'])],capture_output=True,text=True,encoding='utf8',check=True).stdout
    assert '(idle)' in stack and 'main (monitor_fast_optimization_v86_20261010.py:' in stack
    create(A/'observer86_exact_idle_before87_v1_20261011.json',{'status':'verified_exact_childless_idle_observer','stack':stack,'identity':row})
    retire(row,'Verified idle observer replaced with additive long504 actual states and clarified historical captions; no scientific worker terminated')
    assert allowed();new=start_service('actual_fast_optimization_progress_v87_20261011',driver.name,[],{str(driver):sha(driver)})
    create(A/'actual_fast_optimization_progress_v87_20261011_activation.json',new)
    print({'observer87':'started','scientific_workers_terminated':0},flush=True)
if __name__=='__main__':main()
