"""Repair exact references to the preserved handoff17 path reconciliation; preserve failed18 source."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
def main():
    source=A/'record_and_publish_actual_optimization_handoff_v18_20261008.py';text=source.read_text(encoding='utf8')
    changes={'reconcile_actual_handoff18_remote_and_long_paths_v2_20261008.py':'reconcile_actual_handoff17_remote_and_long_paths_v2_20261008.py',
             'actual_handoff18_long_paths_reconciliation_v2_20261008.json':'actual_handoff17_long_paths_reconciliation_v2_20261008.json'}
    for before,after in changes.items():assert text.count(before)==1;text=text.replace(before,after)
    needle='    sources=list(dict.fromkeys(sources));assert all(p.is_file() and p.suffix in (\'.py\',\'.json\',\'.log\') for p in sources)'
    assert text.count(needle)==1
    text=text.replace(needle,"    sources += [A/'publish_actual_optimization_path_recovery_handoff_v18_20261008.py',A/'service_owned_workflows_20261006/actual_optimization_path_recovery_handoff_main_v18_20261008/service_execution.json',A/'service_owned_workflows_20261006/actual_optimization_path_recovery_handoff_main_v18_20261008/stderr.log']\n"+needle)
    target=A/'record_and_publish_actual_optimization_handoff_v18_reference2_20261008.py';assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    create(A/'actual_handoff18_reference_recovery_v2_20261008.json',{
        'status':'frozen_two_exact_reference_repairs_before_publication','input_sha256':{str(p):sha(p) for p in (Path(__file__),source,target)},
        'changes':changes,'failed_publication_source_preserved':True,'new_quality_scores':0})
    namespace={'__file__':str(target),'__name__':'actual_handoff18_reference2'};exec(compile(text,str(target),'exec'),namespace);namespace['main']()
if __name__=='__main__':main()
