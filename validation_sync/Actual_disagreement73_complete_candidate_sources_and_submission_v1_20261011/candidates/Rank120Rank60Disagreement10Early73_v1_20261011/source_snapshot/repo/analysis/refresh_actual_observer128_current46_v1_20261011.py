from pathlib import Path
import sys,ast,time,psutil,subprocess
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
assert allowed()
s=(A/'monitor_verified_current_optimization_v127_20261011.py').read_text(encoding='utf8').replace('v127_20261011','v128_20261011').replace('v247_20261011','v251_20261011').replace('.127.tmp','.128.tmp').replace('range(185,206)','range(185,207)').replace('range(183,206)','range(183,207)')
s=s.replace(' def current(n):'," p46=read(A/'actual_fraction38_gate_only_routes46_admission_v1_20261011.json');aliases.update(p46['service_alias_updates']);names += [n for n,d in p46['tasks']]\n def current(n):",1)
s=s.replace(' while True:'," names += ['actual_fraction38_completed_namespace_bridge_v1_20261011','actual_rank120_rank60_after183_best_blend_fraction38_screen_v1_20261011','actual_rank120_rank60_best_blend_fraction38_completed_main_v1_20261011','actual_best_blend38_and_prospective_gate46_sources_main_v1_20261011','actual_complete206_prospective_sources_main_v1_20261011']\n while True:",1)
s=s.replace('  def score_values(value):',"  folder=Path('E:/赛题五_本机临时/StockRank120Rank60_after183_best_blend_fraction38_screen_v1_20261011');rows=[read(p) for p in folder.glob('case*_official.json')]\n  science['rank120_rank60_best_blend_fraction38']={'completed':len(rows),'expected':38,'best_S':max((r['connected_final_score'] for r in rows),default=None),'qualification_pending':True}\n  def score_values(value):",1)
p=A/'monitor_verified_current_optimization_v128_20261011.py';ast.parse(s);assert not p.exists();p.write_text(s,encoding='utf8')
r=start_service('actual_fast_optimization_progress_reboot_v128_20261011',p.name,[],{str(p):sha(p),str(Path(__file__)):sha(__file__)})
for _ in range(20):
 if (A/'optimization_live_progress_v128_20261011.json').exists():break
 time.sleep(.5)
snapshot=read(A/'optimization_live_progress_v128_20261011.json');assert '206' in snapshot['rounds'] and 'rank120_rank60_best_blend_fraction38' in snapshot['science']
old=read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_reboot_v127_20261011/native_launch.json');assert owned(old)
spy=subprocess.run([str(A.parent/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(old['owned_worker_pid'])],capture_output=True,text=True,encoding='utf8',check=True).stdout
assert 'monitor_verified_current_optimization_v127_20261011.py' in spy and 'MainThread' in spy
parent=psutil.Process(old['pid']);worker=psutil.Process(old['owned_worker_pid']);assert not worker.children()
assert worker.create_time()==old['owned_worker_creation_time'] and parent.create_time()==old['owned_parent_creation_time']
worker.terminate();worker.wait(timeout=15);parent.terminate();parent.wait(timeout=15)
create(A/'actual_observer128_current46_and206_admission_v1_20261011.json',{'status':'actual128_first_snapshot_verified_old127_idle_monitor_only_replaced','new':r,'previous':old,'previous_stack':spy,'scientific_workers_terminated':0,'user_deadline':'2026-10-11T13:00:00+08:00'})
print({'observer':128,'through_round':206,'scientific_workers_stopped':0},flush=True)
