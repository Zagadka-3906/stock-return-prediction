from pathlib import Path
import sys,subprocess
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from handoff_ready_goss_full_execution_20261006 import start_service,retire
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed()
    source=A/'monitor_fast_optimization_v80_20261010.py';text=source.read_text(encoding='utf8').replace('v80_20261010.json','v81_20261010.json').replace('v80_20261010.md','v81_20261010.md').replace('handoff_v134_','handoff_v136_').replace('rankings_v52_','rankings_v53_')
    jobs=['actual_stock_pairrank_embedding_own32_controls46_queue_v1_20261010','actual_stock_pairrank_embedding_small512_restart_v1_20261010','StockPairRankEmbeddingSmall512_independent_small_CPU_v1_20261009','actual_stock_pairrank_embedding_small512_bank6_v1_20261010','StockPairRankEmbeddingSmall512_independent_full5_GPU_controls_v1_20261009','actual_stock_pairrank_embedding_six_state_native42_v1_20261010','actual_stock_pairrank_embedding_after174_fast17_screen_v1_20261010','actual_stock_pairrank_embedding_after174_large_allocation29_screen_v1_20261010','actual_StockPairRank_objective_stages_main_v1_20261010','actual_PairRank184_frozen_sources_main_v2_20261010','actual_stock_pairrank_embedding48_after183_normalization_queue_v8_20261010','StockPairRankEmbedding48_selected_native14_v8_20261010','StockPairRankEmbedding184_complete48_family_v9_20261010']
    text=text.replace('    while True:\n','    jobs += '+repr(jobs)+'\n    while True:\n',1)
    needle="        write(A/'optimization_live_progress_v81_20261010.json',state);"
    insert="""        pairbank=Path('E:/赛题五_本机临时/stock_pairrank_embedding_small512_BF16_bank6_v1_20261010')
        pairinfos=[read(pairbank/str(y)/'info.json') for y in range(2020,2026) if (pairbank/str(y)/'info.json').exists()]
        state['pairrank_ID16_cross120_own32']={'completed_annual_models':pairinfos,'actual_stage':read(pairbank/'actual_stage.json') if (pairbank/'actual_stage.json').exists() else None,'CPU_loss_controls':read(A/'same_day_ranknet_loss_actual_CPU_controls_v1_20261010.json'),'backend_CPU':read(A/'PairRank184_actual_recipe_backend_schema_CPU_v2_20261010.json'),'full184_expected_records':48,'QA':95,'fully_qualified':False}
"""
    assert text.count(needle)==1;text=text.replace(needle,insert+needle)
    needle="        p=A/'optimization_live_progress_v81_20261010.md';"
    insert="""        lines.append(f"同日成对排序×股票身份16维×120特征：年度模型{len(pairinfos)}/6，固定32轮；阶段{state['pairrank_ID16_cross120_own32']['actual_stage']}。独立损失/双梯度、800次同日配对与GPU重启已实际通过；官方评分以真实回执为准。")
        lines.append(f"成对排序完整184轮48项/QA95：{services['StockPairRankEmbedding184_complete48_family_v9_20261010']['status']}；源码main：{services['actual_PairRank184_frozen_sources_main_v2_20261010']['status']}。原始登记配方键不匹配已在未来推理前通过新版本修复，未重复训练。")
"""
    assert text.count(needle)==1;text=text.replace(needle,insert+needle)
    path=A/'monitor_fast_optimization_v81_20261010.py';assert not path.exists();compile(text,str(path),'exec');path.write_text(text,encoding='utf8',newline='\n')
    row=read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_v80_20261010/native_launch.json')
    result=subprocess.run([str(ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(row['owned_worker_pid'])],capture_output=True,text=True)
    assert result.returncode==0 and '(idle)' in result.stdout and 'main (monitor_fast_optimization_v80_20261010.py:' in result.stdout
    retire(row,'Observer81 adds actual pairrank annual/checkpoint and184 QA95 progress; scientific workers untouched')
    name='actual_fast_optimization_progress_v81_20261010';new=start_service(name,path.name,[],{str(path):sha(path)})
    create(A/(name+'_activation.json'),new);print(new,flush=True)
if __name__=='__main__':main()
