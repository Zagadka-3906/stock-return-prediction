"""Read only the exact API transport holder's current stack and child command names."""
from pathlib import Path
import sys,psutil,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,owned
from handoff_joint_goss_round97_full_execution_20261006 import stack
row=read(A/'service_owned_workflows_20261006/main_publication_API_tree_recovery_lease/native_launch.json')
assert owned(row)
proc=psutil.Process(row['owned_worker_pid'])
print(json.dumps({'pid':proc.pid,'stack':stack(proc.pid),'children':[{'pid':p.pid,'name':p.name(),'cmdline':p.cmdline()} for p in proc.children(recursive=True)]},ensure_ascii=False,indent=2))
