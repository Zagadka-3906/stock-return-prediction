from pathlib import Path
import sys,psutil,subprocess
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
assert allowed()
current=read(A/'optimization_live_progress_v127_20261011.json');assert '205' in current['rounds']
new=read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_reboot_v127_20261011/native_launch.json');assert owned(new)
old=read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_reboot_v126_20261011/native_launch.json');assert owned(old)
spy=subprocess.run([str(A.parent/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(old['owned_worker_pid'])],capture_output=True,text=True,encoding='utf8',check=True).stdout
assert 'monitor_verified_current_optimization_v126_20261011.py' in spy
parent=psutil.Process(old['pid']);worker=psutil.Process(old['owned_worker_pid']);assert not worker.children()
assert worker.create_time()==old['owned_worker_creation_time'] and parent.create_time()==old['owned_parent_creation_time']
worker.terminate();worker.wait(timeout=15);parent.terminate();parent.wait(timeout=15)
create(A/'actual_observer127_complete205_refresh_admission_v2_20261011.json',{'status':'actual_new127_first_snapshot_verified_then_only_old126_observer_replaced','new':new,'previous':old,'previous_stack':spy,'snapshot_at':current['at_local'],'scientific_workers_terminated':0,'prior_administrative_snapshot_race_preserved':True})
print({'observer':127,'scientific_workers_stopped':0},flush=True)
