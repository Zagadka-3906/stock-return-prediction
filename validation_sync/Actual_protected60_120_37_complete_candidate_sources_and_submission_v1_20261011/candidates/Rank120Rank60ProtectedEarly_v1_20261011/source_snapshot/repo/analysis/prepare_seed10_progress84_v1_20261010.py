"""Replace only the verified idle observer; retain original scientific status records."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service,retire
def main():
    assert allowed(); source=A/'monitor_fast_optimization_v83_20261010.py'
    text=source.read_text(encoding='utf8')
    tasks=['actual_stock_rank20seed10_embedding_own64_controls46_queue_v1_20261010',
        'actual_stock_rank20seed10_embedding_small512_restart_v1_20261010',
        'StockRank20Seed10EmbeddingSmall512_independent_small_CPU_v1_20261009',
        'actual_stock_rank20seed10_embedding_small512_bank6_v1_20261010',
        'StockRank20Seed10EmbeddingSmall512_independent_full5_GPU_controls_v1_20261009',
        'actual_stock_rank20seed10_embedding_six_state_native42_v1_20261010',
        'actual_stock_rank20seed10_embedding_after175_fast17_screen_v1_20261010',
        'actual_stock_rank20seed10_embedding_after175_large_allocation29_screen_v1_20261010',
        'actual_StockRank20Seed10_objective_stages_main_v1_20261010']
    marker='    while True:'; assert text.count(marker)==1
    text=text.replace(marker,'    jobs += '+repr(tasks)+'\n    families += '+repr([
        'StockRank20Seed10EmbeddingSmall512_after175_high_impact17_screen_v1_20261010',
        'StockRank20Seed10EmbeddingSmall512_after175_large_allocation29_screen_v1_20261010'])+'\n'+marker)
    marker="        write(A/'optimization_live_progress_v83_20261010.json',state)"; assert text.count(marker)==1
    insert="""        seedbank=Path('E:/赛题五_本机临时/stock_rank20seed10_embedding_small512_BF16_bank6_v1_20261010')
        seedinfos=[read(seedbank/str(y)/'info.json') for y in range(2020,2026) if (seedbank/str(y)/'info.json').exists()]
        state['independent_rank20_seed10']={'completed_annual_models':seedinfos,'configuration':read(A/'stock_rank20seed10_embedding_own64_controls46_sources_admission_v1_20261010.json')['configuration'],'new_scores_only_from_actual_capsules':True,'submission_qualified':False}
"""
    text=text.replace(marker,insert+marker)
    marker="        p=A/'optimization_live_progress_v83_20261010.md'";assert text.count(marker)==1
    insert="""        lines.append(f"20日排名独立种子20261010：新年度模型{len(seedinfos)}/6；GPU重启{services['actual_stock_rank20seed10_embedding_small512_restart_v1_20261010']['status']}；预声明46项官方比较，尚未完成的不计为分数。")
        for family in ['StockRank20Seed10EmbeddingSmall512_after175_high_impact17_screen_v1_20261010','StockRank20Seed10EmbeddingSmall512_after175_large_allocation29_screen_v1_20261010']:
            s=summaries.get(family,{});lines.append(f"{family}：已评分{s.get('completed_cases',0)}；TRAIN最高S={s.get('best',{}).get('connected_final_score')}；独立新训练，非复制旧权重。")
"""
    text=text.replace(marker,insert+marker).replace('optimization_live_progress_v83','optimization_live_progress_v84').replace('actual_optimization_fast_runtime_handoff_v141','actual_optimization_fast_runtime_handoff_v142').replace('high_impact_additional_validation_rankings_v55','high_impact_additional_validation_rankings_v56')
    driver=A/'monitor_fast_optimization_v84_20261010.py';assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
    old=A/'service_owned_workflows_20261006/actual_fast_optimization_progress_v83_20261010/native_launch.json'
    retire(read(old),'Verified idle main observer replaced with additive seed10 actual statuses; no scientific worker stopped')
    assert allowed(); row=start_service('actual_fast_optimization_progress_v84_20261010',driver.name,[],{str(driver):sha(driver)})
    create(A/'actual_fast_optimization_progress_v84_20261010_activation.json',row)
    print({'observer84':'started','scientific_workers_terminated':0},flush=True)
if __name__=='__main__':main()
