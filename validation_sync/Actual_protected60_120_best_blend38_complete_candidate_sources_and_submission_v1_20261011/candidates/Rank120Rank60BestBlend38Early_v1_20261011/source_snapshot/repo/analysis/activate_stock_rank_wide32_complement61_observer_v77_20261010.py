from pathlib import Path
import sys,subprocess,ast
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service,retire
def main():
    assert allowed()
    original=A/'monitor_fast_optimization_v76_20261010.py';p=A/'monitor_fast_optimization_v77_20261010.py'
    text=original.read_text(encoding='utf8').replace('optimization_live_progress_v76','optimization_live_progress_v77').replace('actual_optimization_fast_runtime_handoff_v127','actual_optimization_fast_runtime_handoff_v128').replace('high_impact_additional_validation_rankings_v48','high_impact_additional_validation_rankings_v49')
    text=text.replace('    while True:',"    jobs += ['actual_stock_rank20_embedding_after174_complement61_screen_v1_20261010','actual_Rank20_after174_complement61_stages_main_v1_20261010']\n    families += ['StockRank20EmbeddingSmall512_after174_high_impact61_screen_v1_20261010']\n    while True:",1)
    marker="        p=A/'optimization_live_progress_v77_20261010.md'"
    assert marker in text
    text=text.replace(marker,"        complement=summaries.get('StockRank20EmbeddingSmall512_after174_high_impact61_screen_v1_20261010',{});lines.append(f\"20日排名叠加174：已评分{complement.get('completed_cases',0)}/61，TRAIN最高S={complement.get('best',{}).get('connected_final_score')}；复用已验证年度模型，未完成完整提交资格。\")\n"+marker)
    assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n')
    row=read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_v76_20261010/native_launch.json')
    tree=ast.parse(original.read_text(encoding='utf8'));sleeps=[n.lineno for n in ast.walk(tree) if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Attribute) and n.value.func.attr=='sleep']
    assert len(sleeps)==1
    dump=subprocess.run([str(ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(row['owned_worker_pid'])],capture_output=True,text=True,check=True).stdout
    assert f'main (monitor_fast_optimization_v76_20261010.py:{sleeps[0]})' in dump and '(idle)' in dump
    retire(row,'Only replace idle progress observer to display actual complement61 and capacity own64 phases; no training or scoring terminated.')
    assert allowed();new=start_service('actual_fast_optimization_progress_v77_20261010',p.name,[],{str(p):sha(p)})
    create(A/'actual_fast_optimization_progress_v77_20261010_activation.json',new)
    print(new['name'],flush=True)
if __name__=='__main__':main()
