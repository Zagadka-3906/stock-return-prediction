"""Read exact live administrative/scientific closing stages without changes."""
from pathlib import Path
import sys,json,psutil,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,owned
from handoff_joint_goss_round97_full_execution_20261006 import stack
rows={}
for name in ['nonflag_RidgeMicro40_selected_candidate_preparation_v2','nonflag_RidgeMicro40_selected_candidate_sealing_v2','nonflag_RidgeMicro40_round131_full_registration_v2']:
    f=A/'service_owned_workflows_20261006'/name;row=read(f/'native_launch.json');live=owned(row)
    rows[name]={'owned_live':live,'execution':read(f/'service_execution.json') if (f/'service_execution.json').exists() else None}
    if live:
        p=psutil.Process(row['owned_worker_pid']);rows[name].update(pid=p.pid,RSS_GiB=p.memory_info().rss/2**30,stack=stack(p.pid).splitlines()[-12:])
print(json.dumps({'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'stages':rows},ensure_ascii=False,indent=2))
