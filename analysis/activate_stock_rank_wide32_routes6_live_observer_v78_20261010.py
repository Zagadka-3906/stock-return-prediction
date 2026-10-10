from pathlib import Path
import sys,subprocess,ast
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service,retire
def main():
    assert allowed()
    original=A/'monitor_fast_optimization_v77_20261010.py';p=A/'monitor_fast_optimization_v78_20261010.py'
    proof=read(A/'Dual25_verified_recovery_exact_dependency_aliases_v6_20261010.json')
    jobs=[*proof['service_aliases'].values(),'actual_stock_top10_embedding_after174_large_allocation29_completion_main_v80_20261010','actual_capacity181_complement182_routes6_sources_main_v67_20261010','actual_stock_rank20_embedding63_after181_normalization_queue_v5_20261010','StockRank20Embedding63_selected_native14_v5_20261010','StockRank20Embedding182_complete63_family_v6_20261010']
    text=original.read_text(encoding='utf8').replace('optimization_live_progress_v77','optimization_live_progress_v78').replace('actual_optimization_fast_runtime_handoff_v128','actual_optimization_fast_runtime_handoff_v129').replace('high_impact_additional_validation_rankings_v49','high_impact_additional_validation_rankings_v50').replace('Dual25_verified_recovery_exact_dependency_aliases_v5','Dual25_verified_recovery_exact_dependency_aliases_v6')
    text=text.replace('    while True:','    jobs += '+repr(jobs)+'\n    while True:',1)
    text=text.replace("'quality_pending':not (capacity_bank/'verification.json').exists()","'quality_pending':not all((Path('E:/赛题五_本机临时')/folder/'verification.json').exists() for folder in ('StockRankWide32Embedding1024_after174_high_impact17_screen_v1_20261010','StockRankWide32Embedding1024_after174_large_allocation29_screen_v1_20261010')),'submission_qualification_pending':not (A/'github_validation_sync_main_20261005/round181_receipt.json').exists()")
    marker="        p=A/'optimization_live_progress_v78_20261010.md'";assert marker in text
    text=text.replace(marker,"        lines.append(f\"容量完整181轮48项/QA92：{services['StockRankWide32Embedding181_complete48_family_v7_20261010']['status']}；互补完整182轮63项/QA93：{services['StockRank20Embedding182_complete63_family_v6_20261010']['status']}。\")\n        lines.append(f\"实际Top29发布v80：{services['actual_stock_top10_embedding_after174_large_allocation29_completion_main_v80_20261010']['status']}；冻结完整流程与111别名/9入口/12父回调源码main：{services['actual_capacity181_complement182_routes6_sources_main_v67_20261010']['status']}。原始失败状态保留。\")\n"+marker)
    assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n')
    row=read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_v77_20261010/native_launch.json');tree=ast.parse(original.read_text(encoding='utf8'));sleeps=[n.lineno for n in ast.walk(tree) if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Attribute) and n.value.func.attr=='sleep'];assert len(sleeps)==1
    dump=subprocess.run([str(ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(row['owned_worker_pid'])],capture_output=True,text=True,check=True).stdout
    assert f'main (monitor_fast_optimization_v77_20261010.py:{sleeps[0]})' in dump and '(idle)' in dump
    retire(row,'Only replace idle progress observer: use actual route6 aliases, 181/182 full qualification, source-main receipts and real capacity/61 score progress; scientific workers untouched.')
    assert allowed();new=start_service('actual_fast_optimization_progress_v78_20261010',p.name,[],{str(p):sha(p)})
    create(A/'actual_fast_optimization_progress_v78_20261010_activation.json',new)
    print(new['name'],flush=True)
if __name__=='__main__':main()
