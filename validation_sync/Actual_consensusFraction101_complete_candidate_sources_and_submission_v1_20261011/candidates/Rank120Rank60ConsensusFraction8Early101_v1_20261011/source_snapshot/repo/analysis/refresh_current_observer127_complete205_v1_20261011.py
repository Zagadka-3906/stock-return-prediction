from pathlib import Path
import sys,ast,psutil,subprocess
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
assert allowed()
p=A/'monitor_verified_current_optimization_v127_20261011.py'
s=(A/'monitor_verified_current_optimization_v126_20261011.py').read_text(encoding='utf8').replace('v126_20261011','v127_20261011').replace('v243_20261011','v247_20261011').replace('.126.tmp','.127.tmp').replace('range(185,202)','range(185,206)').replace('range(183,202)','range(183,206)')
names=[]
for folder in (A/'service_owned_workflows_20261006').iterdir():
 if folder.is_dir() and any(t in folder.name for t in ['202_','203_','204_','205_','fraction_embedding40','protected39','seed10_direct_embedding35','completed_main_v1_20261011','complete202_205_prospective_sources']):
  if (folder/'native_launch.json').exists():names.append(folder.name)
s=s.replace(' while True:', ' names += '+repr(names)+'\n while True:',1)
ast.parse(s);assert not p.exists();p.write_text(s,encoding='utf8')
r=start_service('actual_fast_optimization_progress_reboot_v127_20261011',p.name,[],{str(p):sha(p),str(Path(__file__)):sha(__file__)})
assert (A/'optimization_live_progress_v127_20261011.json').exists()
old=read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_reboot_v126_20261011/native_launch.json');assert owned(old)
spy=subprocess.run([str(A.parent/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(old['owned_worker_pid'])],capture_output=True,text=True,encoding='utf8',check=True).stdout
assert 'monitor_verified_current_optimization_v126_20261011.py' in spy and 'MainThread' in spy
parent=psutil.Process(old['pid']);worker=psutil.Process(old['owned_worker_pid']);assert not worker.children()
assert worker.create_time()==old['owned_worker_creation_time'] and parent.create_time()==old['owned_parent_creation_time']
worker.terminate();worker.wait(timeout=15);parent.terminate();parent.wait(timeout=15)
create(A/'actual_observer127_complete205_refresh_admission_v1_20261011.json',{'status':'actual_new_observer_first_snapshot_saved_then_only_verified_previous_observer_replaced','new':r,'previous':old,'previous_stack':spy,'additional_service_names':names,'scientific_workers_terminated':0})
print({'observer':127,'additional_services':len(names),'scientific_workers_stopped':0},flush=True)
