from pathlib import Path
import sys,subprocess
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from handoff_ready_goss_full_execution_20261006 import start_service,retire
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed()
    source=A/'monitor_fast_optimization_v82_20261010.py';text=source.read_text(encoding='utf8').replace('v82_20261010.json','v83_20261010.json').replace('v82_20261010.md','v83_20261010.md').replace('handoff_v138_','handoff_v141_').replace('rankings_v54_','rankings_v55_')
    proof=read(A/'PairTop184185_complete_reference_routes_v9_20261010.json')
    jobs=list(proof['service_aliases'].values())+['actual_PairTop185_complete_references_sources_main_v9_20261010']
    text=text.replace('    while True:\n','    jobs += '+repr(list(dict.fromkeys(jobs)))+'\n    while True:\n',1)
    needle="        for original,actual in actual_aliases.items():"
    assert text.count(needle)==1;text=text.replace(needle,"        actual_aliases.update(read(A/'PairTop184185_complete_reference_routes_v9_20261010.json')['service_aliases'])\n"+needle)
    needle="        p=A/'optimization_live_progress_v83_20261010.md';"
    assert text.count(needle)==1
    text=text.replace(needle,"        lines.append(f\"后续184/185完整登记：实际33处本地导入与9份逐字源码引用检查通过；恢复流程源码main：{services['actual_PairTop185_complete_references_sources_main_v9_20261010']['status']}。仅更换核实闲置的依赖助手，原始代码与失败记录保留。\")\n"+needle)
    p=A/'monitor_fast_optimization_v83_20261010.py';assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n')
    row=read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_v82_20261010/native_launch.json')
    result=subprocess.run([str(ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(row['owned_worker_pid'])],capture_output=True,text=True)
    assert result.returncode==0 and '(idle)' in result.stdout and 'main (monitor_fast_optimization_v82_20261010.py:' in result.stdout
    retire(row,'Observer83 tracks actual complete-reference9 dependency aliases and real source receipts; scientific workers untouched')
    name='actual_fast_optimization_progress_v83_20261010';row=start_service(name,p.name,[],{str(p):sha(p)})
    create(A/(name+'_activation.json'),row);print(row,flush=True)
if __name__=='__main__':main()
