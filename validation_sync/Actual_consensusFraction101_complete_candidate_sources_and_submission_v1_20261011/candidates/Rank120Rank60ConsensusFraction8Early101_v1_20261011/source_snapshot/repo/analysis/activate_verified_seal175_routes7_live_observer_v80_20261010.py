from pathlib import Path
import sys,subprocess,ast
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service,retire
def main():
    assert allowed()
    original=A/'monitor_fast_optimization_v79_20261010.py';p=A/'monitor_fast_optimization_v80_20261010.py';proof=read(A/'Dual25_verified_recovery_exact_dependency_aliases_v7_20261010.json')
    jobs=[*proof['service_aliases'].values(),'StockTop10Embedding175_selected_candidate_sealing_recovery_v2_20261010','StockTop10Embedding175_verified_registration_completion_recovery_v7_20261010','StockTop10Embedding175_verified_full_registration_recovery_v7_20261010','actual_verified_seal175_routes7_CPU10_sources_main_v73_20261010']
    text=original.read_text(encoding='utf8').replace('optimization_live_progress_v79','optimization_live_progress_v80').replace('actual_optimization_fast_runtime_handoff_v131','actual_optimization_fast_runtime_handoff_v134').replace('high_impact_additional_validation_rankings_v51','high_impact_additional_validation_rankings_v52').replace('Dual25_verified_recovery_exact_dependency_aliases_v6','Dual25_verified_recovery_exact_dependency_aliases_v7')
    text=text.replace('    while True:','    jobs += '+repr(jobs)+'\n    while True:',1)
    marker="        p=A/'optimization_live_progress_v80_20261010.md'";assert marker in text
    text=text.replace(marker,"        lines.append(f\"175原推理已通过，封装修复：{services['StockTop10Embedding175_selected_candidate_sealing_recovery_v2_20261010']['status']}；保留已完成推理的完整47项登记：{services['StockTop10Embedding175_verified_full_registration_recovery_v7_20261010']['status']}。跨盘失败与下游失败原始回执保留，实际10项原main入口/跨盘CPU验证通过。\")\n"+marker)
    assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n')
    row=read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_v79_20261010/native_launch.json');tree=ast.parse(original.read_text(encoding='utf8'));sleeps=[n.lineno for n in ast.walk(tree) if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Attribute) and n.value.func.attr=='sleep'];assert len(sleeps)==1
    dump=subprocess.run([str(ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(row['owned_worker_pid'])],capture_output=True,text=True,check=True).stdout
    assert f'main (monitor_fast_optimization_v79_20261010.py:{sleeps[0]})' in dump and '(idle)' in dump
    retire(row,'Only replace idle observer with actual recovered175 seal, route7 downstream statuses, completed61 and live tight82; no scores, model fits or inference stopped.')
    assert allowed();new=start_service('actual_fast_optimization_progress_v80_20261010',p.name,[],{str(p):sha(p)})
    create(A/'actual_fast_optimization_progress_v80_20261010_activation.json',new)
    print(new['name'],flush=True)
if __name__=='__main__':main()
