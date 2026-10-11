from pathlib import Path
import sys,ast,time,psutil,subprocess
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
assert allowed()
s=(A/'monitor_verified_current_optimization_v128_20261011.py').read_text(encoding='utf8').replace('v128_20261011','v129_20261011').replace('v251_20261011','v255_20261011').replace('.128.tmp','.129.tmp')
s=s.replace(' def current(n):'," for filename in ['actual_nested_dispatch_and_complete_aliases48_admission_v1_20261011.json','actual_failed_future202_206_routes49_admission_v1_20261011.json','actual_current_publication_paths_and_prospective50_admission_v1_20261011.json']:\n  latest=read(A/filename);aliases.update(latest['service_alias_updates']);names += [n for n,d in latest['tasks']]\n aliases['actual187_registered_QA_main_resume45_v1_20261011']='actual187_completed_QA_publication_only_resume47_v1_20261011'\n names += ['actual187_completed_QA_publication_only_resume47_v1_20261011','actual_current50_and_publication47_sources_main_v1_20261011']\n def current(n):",1)
p=A/'monitor_verified_current_optimization_v129_20261011.py';ast.parse(s);assert not p.exists();p.write_text(s,encoding='utf8')
r=start_service('actual_fast_optimization_progress_reboot_v129_20261011',p.name,[],{str(p):sha(p),str(Path(__file__)):sha(__file__)})
for _ in range(20):
 if (A/'optimization_live_progress_v129_20261011.json').exists():break
 time.sleep(.5)
snapshot=read(A/'optimization_live_progress_v129_20261011.json');assert '206' in snapshot['rounds']
old=read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_reboot_v128_20261011/native_launch.json');assert owned(old)
spy=subprocess.run([str(A.parent/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(old['owned_worker_pid'])],capture_output=True,text=True,encoding='utf8',check=True).stdout
assert 'monitor_verified_current_optimization_v128_20261011.py' in spy
worker=psutil.Process(old['owned_worker_pid']);parent=psutil.Process(old['pid']);assert not worker.children() and worker.create_time()==old['owned_worker_creation_time'] and parent.create_time()==old['owned_parent_creation_time']
worker.terminate();worker.wait(timeout=15);parent.terminate();parent.wait(timeout=15)
create(A/'actual_observer129_current50_first_snapshot_admission_v1_20261011.json',{'status':'actual129_first_snapshot_current50_future_gates_and187_publication47_verified_only_old128_monitor_replaced','new':r,'previous':old,'scientific_workers_terminated':0})
print({'actual_observer':129,'science_workers_stopped':0},flush=True)
