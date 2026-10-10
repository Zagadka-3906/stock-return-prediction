"""Resolve the CPU replay's restart dependency by replacing only its idle scheduler."""
from pathlib import Path
import sys,ast,subprocess,psutil
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
def main():
 assert allowed();old=A/'run_stock_rank120_own6_full5_native42_and_direct33_queue_v1_20261011.py';s=old.read_text(encoding='utf8');tree=ast.parse(s)
 loop=next(n for n in ast.walk(tree) if isinstance(n,ast.For) and isinstance(n.iter,ast.List));tasks=ast.literal_eval(loop.iter)
 i=next(i for i,r in enumerate(tasks) if 'restart_' in r[1]);restart=tasks.pop(i);tasks.insert(1,restart)
 starts=s.index(' for name,driver in ');end=s.index(':\n',starts);s=s[:starts]+' for name,driver in '+repr(tasks)+s[end:]
 needle='  assert allowed();p=A/driver;r=start_service(name,driver,[],{str(p):sha(p)});create(A/(name+\'_activation.json\'),r);closed(name)';assert s.count(needle)==1
 s=s.replace(needle,"  assert allowed()\n  if (A/'service_owned_workflows_20261006'/name).exists():closed(name);continue\n  p=A/driver;r=start_service(name,driver,[],{str(p):sha(p)});create(A/(name+'_activation.json'),r);closed(name)")
 target=A/'run_stock_rank120_own6_full5_native42_and_direct33_queue_v2_20261011.py';ast.parse(s);assert not target.exists();target.write_text(s,encoding='utf8')
 name='actual_stock_rank120_own6_full5_native42_direct33_queue_v1_20261011';f=A/'service_owned_workflows_20261006'/name;row=read(f/'native_launch.json');assert owned(row)
 w=psutil.Process(row['owned_worker_pid']);p=psutil.Process(row['pid']);assert not w.children() and p.create_time()==row['owned_parent_creation_time'] and p.cmdline()[1:]==w.cmdline()[1:]
 spy=ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe';r=subprocess.run([str(spy),'dump','--pid',str(w.pid),'--locals'],capture_output=True,text=True,encoding='utf8',check=True,creationflags=subprocess.CREATE_NO_WINDOW)
 assert '(idle)' in r.stdout and 'closed (' in r.stdout and 'StockRank120EmbeddingSmall512_independent_small_CPU_v1_20261011' in r.stdout
 proof={'status':'verified_idle_scheduler_reordered_restart_before_smallCPU_replay_of_that_restart_bundle','identity':row,'stack':r.stdout,'input_sha256':{str(q):sha(q) for q in (Path(__file__),old,target)},'scientific_jobs_terminated':0,'existing_CPU_replay_kept_running':True}
 create(A/'rank120_actual_restart_order_recovery_v2_20261011.json',proof)
 assert allowed() and owned(row) and not w.children();w.terminate();w.wait(15);p.terminate();p.wait(15);create(f/'administrative_supersession_for_actual_restart_order_v2_20261011.json',proof)
 assert allowed();n=start_service('actual_stock_rank120_own6_full5_native42_direct33_queue_v2_20261011',target.name,[],proof['input_sha256']);create(A/'actual_rank120_restart_order_v2_activation_20261011.json',n)
 print({'actual120_restart_order_corrected':True,'live_CPU_scientific_worker_preserved':True},flush=True)
if __name__=='__main__':main()
