from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle,retire_suspended,stack
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
import Pure149_chunked_publication_receiver_runtime_v15_20261009 as current
old=read(A/'service_owned_workflows_20261006/PureRFFHuber149_complete_chronological_dispatch_v11_20261009/native_launch.json')
assert owned(old)
actual=stack(old['owned_worker_pid']);assert 'closed (' in actual and 'bind_Pure149_all5_annual_native_v8_20261009.py' in actual
line=next(line for line in actual.splitlines() if 'closed (' in line)
parent,worker,proof=suspended_idle(old,line)
try:
    driver=current.CORE['dispatch_PureRFFHuber149_complete_pipeline_v4_20261008.py']
    row=start('PureRFFHuber149_complete_chronological_dispatch_publication_v15_20261009',driver,[],{str(current.META):sha(current.META),str(A/driver):sha(A/driver)})
    assert owned(row)
    create(A/'Pure149_publication_safe_dispatch_handoff_v15_20261009.json',{'old_identity':old,'old_idle_boundary':proof,'new_identity':row,'scientific_workers_stopped_or_restarted':0})
    retire_suspended(old,row);print(row['owned_worker_pid'],flush=True)
except BaseException:
    if parent.is_running():parent.resume()
    if worker.is_running():worker.resume()
    raise
