"""Queue main publication of each complete saved-state and official-score batch."""
from pathlib import Path
import sys,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service,retire
def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed()
    from prepare_stock_rank5_embedding_full5_native42_and_early17_v1_20261010 import route
    source=A/'publish_stock_rank_embedding_six_state_native42_completion_v54_20261010.py'
    native=save('publish_stock_rank5_embedding_six_state_native42_completion_v64_20261010.py',route(source.read_text(encoding='utf8')).replace('v54_20261010','v64_20261010'))
    source=A/'publish_stock_rank_embedding_after170_completion_v55_20261010.py';text=route(source.read_text(encoding='utf8')).replace('170','171').replace('v55_20261010','v63_20261010')
    text=text.replace('stock_rank5_embedding_own_sources_and_actual_centered_target_admission_v1_20261010.json','stock_rank5_embedding_own64_native_sources_preparation_v1_20261010.json').replace('stock_rank5_embedding_actual_priority173_runtime_admission_v2_20261010.json','stock_rank5_embedding_actual_restart_and_own6_sources_admission_v1_20261010.json')
    official=save('publish_stock_rank5_embedding_after171_completion_v63_20261010.py',text)
    for name,p in [('actual_stock_rank5_embedding_six_state_native42_completion_main_v64_20261010',native),('actual_stock_rank5_embedding_after171_completion_main_v63_20261010',official)]:
        row=start_service(name,p.name,[],{str(p):sha(p)});create(A/(name+'_activation.json'),row)
    old=A/'monitor_fast_optimization_v61_20261010.py';text=old.read_text(encoding='utf8').replace('v61_20261010','v62_20261010').replace('v105_20261010','v107_20261010').replace('v33_20261010','v34_20261010')
    needle="    families=['StockTop10EmbeddingSmall512_after171_large_allocation29_screen_v1_20261010'";assert text.count(needle)==1
    jobs=['StockRank5Embedding_actual_mature_fixture_CPU_v1_20261010','actual_stock_rank5_embedding_own_training_queue_v1_20261010','actual_stock_rank5_embedding_small512_restart_v1_20261010','StockRank5EmbeddingSmall512_independent_small_CPU_v1_20261009','actual_stock_rank5_embedding_small512_bank6_v1_20261010','StockRank5EmbeddingSmall512_independent_full5_GPU_controls_v1_20261009','actual_stock_rank5_embedding_six_state_native42_v1_20261010','actual_stock_rank5_embedding_full5_native42_and_early17_queue_v1_20261010','actual_stock_rank5_embedding_after171_fast17_screen_v1_20261010','actual_stock_rank5_embedding_six_state_native42_completion_main_v64_20261010','actual_stock_rank5_embedding_after171_completion_main_v63_20261010']
    text=text.replace(needle,'    jobs += '+repr(jobs)+"\n    families=['StockRank5EmbeddingSmall512_after171_high_impact17_screen_v1_20261010','StockTop10EmbeddingSmall512_after171_large_allocation29_screen_v1_20261010'")
    needle="        state['screen_progress']=summaries;state['supplementary_actual_scored_records']=len(rows)";assert text.count(needle)==1
    text=text.replace(needle,"        bank5=Path('E:/赛题五_本机临时/stock_rank5_embedding_small512_BF16_bank6_v1_20261010');state['stock_rank5_embedding']={'completed_annual_models':[y for y in range(2020,2026) if (bank5/str(y)/'info.json').exists()],'bank_stage':read(bank5/'actual_stage.json') if (bank5/'actual_stage.json').exists() else None,'worker':services.get('actual_stock_rank5_embedding_small512_bank6_v1_20261010')}\n"+needle)
    needle="('StockTop10EmbeddingSmall512_after171_large_allocation29_screen_v1_20261010',29)";text=text.replace(needle,"('StockRank5EmbeddingSmall512_after171_high_impact17_screen_v1_20261010',17),"+needle)
    needle="        for name in ('Frontier233171_complete233_family_v2_20261010'";text=text.replace(needle,"        lines.append(f\"股票身份×五日排名：已完成年度模型{len(state['stock_rank5_embedding']['completed_annual_models'])}/6；实际服务{state['stock_rank5_embedding']['worker']}。成熟样本、GPU重启、五年度独立解码和官方评分分别以真实完成回执为准。\")\n"+needle)
    observer=save('monitor_fast_optimization_v62_20261010.py',text);row=start_service('actual_fast_optimization_progress_v62_20261010',observer.name,[],{str(observer):sha(observer)});create(A/'actual_fast_optimization_progress_v62_activation_20261010.json',row)
    while not(A/'optimization_live_progress_v62_20261010.json').exists():time.sleep(1)
    retire(read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_v61_20261010/native_launch.json'),'Verified observer62 exposes actual rank5 maturity, GPU restart, own64 six-year fit, full5 and native42 plus early17 and batch main63/64. All scientific jobs retained.')
    print({'rank5_actual_batch_main_publishers':[63,64],'actual_observer':62},flush=True)
if __name__=='__main__':main()
