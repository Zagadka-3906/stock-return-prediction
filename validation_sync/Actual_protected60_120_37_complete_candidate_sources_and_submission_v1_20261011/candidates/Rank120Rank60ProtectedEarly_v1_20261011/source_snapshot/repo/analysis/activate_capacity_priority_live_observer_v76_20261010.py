from pathlib import Path
import sys,subprocess
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service,retire
def main():
    assert allowed()
    original=A/'monitor_fast_optimization_v75_20261010.py';p=A/'monitor_fast_optimization_v76_20261010.py'
    tasks=[
      'actual_stock_rank_wide32_embedding1024_ID32_own64_controls46_queue_v1_20261010','actual_stock_rank_wide32_embedding_wide1024_restart_v1_20261010','StockRankWide32Embedding1024_independent_small_CPU_v1_20261009','actual_stock_rank_wide32_embedding_wide1024_bank6_v1_20261010','StockRankWide32Embedding1024_independent_full5_GPU_controls_v1_20261009','actual_stock_rank_wide32_embedding_six_state_native42_v1_20261010','actual_stock_rank_wide32_embedding_after174_fast17_screen_v1_20261010','actual_stock_rank_wide32_embedding_after174_large_allocation29_screen_v1_20261010','actual_StockRankWide32_capacity_stages_main_v2_20261010','actual_nested_candidate_path_CPU8_main_v65_20261010','actual_StockRank20_own6_full5_main_v66_20261010']
    families=['StockRankWide32Embedding1024_after174_high_impact17_screen_v1_20261010','StockRankWide32Embedding1024_after174_large_allocation29_screen_v1_20261010']
    text=original.read_text(encoding='utf8').replace('optimization_live_progress_v75','optimization_live_progress_v76').replace('actual_optimization_fast_runtime_handoff_v126','actual_optimization_fast_runtime_handoff_v127').replace('high_impact_additional_validation_rankings_v47','high_impact_additional_validation_rankings_v48')
    text=text.replace('    while True:', '    jobs += '+repr(tasks)+'\n    families += '+repr(families)+'\n    while True:',1)
    line="        state['original_service_states_before_explicit_aliases']=original_services"
    text=text.replace(line,line+"\n        capacity_bank=Path('E:/赛题五_本机临时/stock_rank_wide32_embedding_wide1024_BF16_bank6_v1_20261010')\n        state['rank1d_capacity_ID32_1024_own64']={'completed_annual_models':[y for y in range(2020,2026) if (capacity_bank/str(y)/'info.json').exists()],'actual_stage':read(capacity_bank/'actual_stage.json') if (capacity_bank/'actual_stage.json').exists() else None,'configuration_source':'stock_rank_wide32_embedding_wide1024_BF16_native_v1_20261010.py','quality_pending':not (capacity_bank/'verification.json').exists()}")
    line='        p=A/\'optimization_live_progress_v76_20261010.md\''
    assert line in text
    text=text.replace(line,"        lines.append(f\"一日排名容量方案：身份32维、1024–512–256、固定64轮；年度模型{len(state['rank1d_capacity_ID32_1024_own64']['completed_annual_models'])}/6；实际阶段{state['rank1d_capacity_ID32_1024_own64']['actual_stage']}。\")\n        for family in "+repr(families)+":\n            summary=summaries.get(family,{});lines.append(f\"{family}：已评分{summary.get('completed_cases',0)}，TRAIN最高S={summary.get('best',{}).get('connected_final_score')}；完整提交资格以交付指针为准。\")\n"+line)
    assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n')
    row=read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_v75_20261010/native_launch.json')
    dump=subprocess.run([str(ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(row['owned_worker_pid'])],capture_output=True,text=True,check=True).stdout
    assert 'main (monitor_fast_optimization_v75_20261010.py:95)' in dump and '(idle)' in dump
    retire(row,'Replace only idle observer with exact ID32-capacity, own6/full5 and official46 actual progress; no scientific tasks stopped.')
    assert allowed();new=start_service('actual_fast_optimization_progress_v76_20261010',p.name,[],{str(p):sha(p)})
    create(A/'actual_fast_optimization_progress_v76_20261010_activation.json',new)
    print(new['name'],flush=True)
if __name__=='__main__':main()
