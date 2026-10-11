from pathlib import Path
import sys,subprocess,ast
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service,retire
def main():
    assert allowed()
    original=A/'monitor_fast_optimization_v78_20261010.py';p=A/'monitor_fast_optimization_v79_20261010.py'
    jobs=['actual_stock_rank20_embedding_after174_tiny_CDF41_screen_v1_20261010','actual_stock_rank20_embedding_after175_tiny_CDF41_screen_v1_20261010','actual_rank20_tinyCDF82_stages_main_v68_20261010','actual_stock_rank20_embedding85_after182_normalization_queue_v5_20261010','StockRank20Embedding85_selected_native14_v5_20261010','StockRank20Embedding183_complete85_family_v6_20261010','actual_tiny183_QA94_sources_main_v71_20261010']
    families=['StockRank20EmbeddingSmall512_after174_tiny_CDF41_screen_v1_20261010','StockRank20EmbeddingSmall512_after175_tiny_CDF41_screen_v1_20261010']
    text=original.read_text(encoding='utf8').replace('optimization_live_progress_v78','optimization_live_progress_v79').replace('actual_optimization_fast_runtime_handoff_v129','actual_optimization_fast_runtime_handoff_v131').replace('high_impact_additional_validation_rankings_v50','high_impact_additional_validation_rankings_v51')
    text=text.replace('    while True:','    jobs += '+repr(jobs)+'\n    families += '+repr(families)+'\n    while True:',1)
    marker="        p=A/'optimization_live_progress_v79_20261010.md'";assert marker in text
    text=text.replace(marker,"        for family in "+repr(families)+":\n            current=summaries.get(family,{});lines.append(f\"{family}：已评分{current.get('completed_cases',0)}/41，TRAIN最高S={current.get('best',{}).get('connected_final_score')}；分别等待当前61项完成/合格175，不重复训练。\")\n        lines.append(f\"微权重完整183轮85项/QA94：{services['StockRank20Embedding183_complete85_family_v6_20261010']['status']}；源码main：{services['actual_tiny183_QA94_sources_main_v71_20261010']['status']}。\")\n"+marker)
    assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n')
    row=read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_v78_20261010/native_launch.json');tree=ast.parse(original.read_text(encoding='utf8'));sleeps=[n.lineno for n in ast.walk(tree) if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Attribute) and n.value.func.attr=='sleep'];assert len(sleeps)==1
    dump=subprocess.run([str(ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(row['owned_worker_pid'])],capture_output=True,text=True,check=True).stdout
    assert f'main (monitor_fast_optimization_v78_20261010.py:{sleeps[0]})' in dump and '(idle)' in dump
    retire(row,'Only replace idle progress observer to display real tight82 and full183/QA94 dispatch; no training, scoring or inference stopped.')
    assert allowed();new=start_service('actual_fast_optimization_progress_v79_20261010',p.name,[],{str(p):sha(p)})
    create(A/'actual_fast_optimization_progress_v79_20261010_activation.json',new)
    print(new['name'],flush=True)
if __name__=='__main__':main()
