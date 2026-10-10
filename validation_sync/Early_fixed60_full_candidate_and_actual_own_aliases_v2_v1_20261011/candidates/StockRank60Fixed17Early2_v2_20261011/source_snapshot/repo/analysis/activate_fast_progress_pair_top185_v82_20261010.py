from pathlib import Path
import sys,subprocess
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import create,sha,read
from handoff_ready_goss_full_execution_20261006 import start_service,retire
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed()
    source=A/'monitor_fast_optimization_v81_20261010.py';text=source.read_text(encoding='utf8').replace('v81_20261010.json','v82_20261010.json').replace('v81_20261010.md','v82_20261010.md').replace('handoff_v136_','handoff_v138_').replace('rankings_v53_','rankings_v54_')
    jobs=['actual_stock_pairrank_embedding_six_state_native42_admission_recovery_v2_20261010','actual_stock_pairrank_embedding_own32_controls46_queue_v2_20261010','actual_stock_toppair_embedding_own32_controls46_queue_v2_20261010','actual_stock_toppair_embedding_small512_restart_v1_20261010','StockTopPairEmbeddingSmall512_independent_small_CPU_v1_20261009','actual_stock_toppair_embedding_small512_bank6_v1_20261010','StockTopPairEmbeddingSmall512_independent_full5_GPU_controls_v1_20261009','actual_stock_toppair_embedding_six_state_native42_v1_20261010','actual_stock_toppair_embedding_after174_fast17_screen_v1_20261010','actual_stock_toppair_embedding_after174_large_allocation29_screen_v1_20261010','actual_PairTop185_native_admission_sources_main_v1_20261010','actual_StockTopPair_objective_stages_main_v1_20261010','actual_StockPairRank_remaining_native46_main_v8_20261010','actual_stock_toppair_embedding48_after184_normalization_import_recovery_v2_20261010','StockTopPairEmbedding48_selected_native14_v8_20261010','StockTopPairEmbedding185_complete48_family_v9_20261010']+list(read(A/'actual_PairRank_native42_admission_routes_v8_20261010.json')['service_aliases'].values())
    text=text.replace('    while True:\n','    jobs += '+repr(jobs)+"\n    families += ['StockPairRankEmbeddingSmall512_after174_high_impact17_screen_v1_20261010','StockPairRankEmbeddingSmall512_after174_large_allocation29_screen_v1_20261010','StockTopPairEmbeddingSmall512_after174_high_impact17_screen_v1_20261010','StockTopPairEmbeddingSmall512_after174_large_allocation29_screen_v1_20261010']\n    while True:\n",1)
    text=text.replace("        for original,actual in alias_proof['service_aliases'].items():", "        actual_aliases={**alias_proof['service_aliases'],**read(A/'actual_PairRank_native42_admission_routes_v8_20261010.json')['service_aliases']}\n        actual_aliases['actual_stock_toppair_embedding48_after184_normalization_queue_v8_20261010']='actual_stock_toppair_embedding48_after184_normalization_import_recovery_v2_20261010'\n        for original,actual in actual_aliases.items():")
    needle="        write(A/'optimization_live_progress_v82_20261010.json',state);"
    insert="""        topbank=Path('E:/赛题五_本机临时/stock_toppair_embedding_small512_BF16_bank6_v1_20261010')
        topinfos=[read(topbank/str(y)/'info.json') for y in range(2020,2026) if (topbank/str(y)/'info.json').exists()]
        state['top_emphasized_pairrank_own32']={'completed_annual_models':topinfos,'actual_stage':read(topbank/'actual_stage.json') if (topbank/'actual_stage.json').exists() else None,'loss_CPU':read(A/'same_day_top_ranknet_loss_actual_CPU_controls_v1_20261010.json'),'full185_records':48,'QA':96,'fully_qualified':False}
"""
    assert text.count(needle)==1;text=text.replace(needle,insert+needle)
    needle="        p=A/'optimization_live_progress_v82_20261010.md';"
    insert="""        lines.append(f"同日排序原生42项实际恢复：{services['actual_stock_pairrank_embedding_six_state_native42_admission_recovery_v2_20261010']['status']}；只补齐源码记录引用，五年度完整独立推理已通过，未重复训练。")
        for family in ['StockPairRankEmbeddingSmall512_after174_high_impact17_screen_v1_20261010','StockPairRankEmbeddingSmall512_after174_large_allocation29_screen_v1_20261010','StockTopPairEmbeddingSmall512_after174_high_impact17_screen_v1_20261010','StockTopPairEmbeddingSmall512_after174_large_allocation29_screen_v1_20261010']:
            s=summaries.get(family,{});lines.append(f"{family}：已评分{s.get('completed_cases',0)}，TRAIN最高S={s.get('best',{}).get('connected_final_score')}；完整资格以交付指针为准。")
        lines.append(f"Top组训练权重十倍成对排序：年度模型{len(topinfos)}/6；GPU重启{services['actual_stock_toppair_embedding_small512_restart_v1_20261010']['status']}；完整185轮48项/QA96：{services['StockTopPairEmbedding185_complete48_family_v9_20261010']['status']}。官方总分及Top股票池规则保持原口径。")
"""
    assert text.count(needle)==1;text=text.replace(needle,insert+needle)
    p=A/'monitor_fast_optimization_v82_20261010.py';assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n')
    row=read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_v81_20261010/native_launch.json')
    result=subprocess.run([str(ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(row['owned_worker_pid'])],capture_output=True,text=True)
    assert result.returncode==0 and '(idle)' in result.stdout and 'main (monitor_fast_optimization_v81_20261010.py:' in result.stdout
    retire(row,'Observer82 shows actual native42 recovery alias, pair/top official scores and185; scientific workers untouched')
    name='actual_fast_optimization_progress_v82_20261010';row=start_service(name,p.name,[],{str(p):sha(p)})
    create(A/(name+'_activation.json'),row);print(row,flush=True)
if __name__=='__main__':main()
