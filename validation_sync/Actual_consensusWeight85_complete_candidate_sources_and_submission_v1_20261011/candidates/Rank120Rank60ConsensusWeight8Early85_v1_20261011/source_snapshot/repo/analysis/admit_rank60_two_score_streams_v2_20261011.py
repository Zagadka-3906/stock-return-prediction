"""Replace only the exact childless idle scheduler; preserve all score jobs."""
from pathlib import Path
import sys,subprocess,psutil
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
def main():
 assert allowed()
 old='actual_stock_rank60_native42_and_fast46_queue_v1_20261011'
 folder=A/'service_owned_workflows_20261006'/old
 row=read(folder/'native_launch.json');assert owned(row)
 parent=psutil.Process(row['pid']);worker=psutil.Process(row['owned_worker_pid'])
 assert parent.create_time()==row['owned_parent_creation_time'] and not worker.children()
 assert parent.cmdline()[1:]==worker.cmdline()[1:]
 spy=ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'
 r=subprocess.run([str(spy),'dump','--pid',str(worker.pid),'--locals'],capture_output=True,text=True,encoding='utf8',check=True,creationflags=subprocess.CREATE_NO_WINDOW)
 assert '(idle)' in r.stdout and 'closed (prepare_protected_tail_pilot76_and_selected_native14_v1_20261010.py:19)' in r.stdout
 assert 'name: "actual_stock_rank20class25_embedding_after175_large_allocation29_screen_v1_20261011"' in r.stdout
 closed('actual_stock_rank60_embedding_six_state_native42_v1_20261011')
 assert psutil.virtual_memory().available>=16*2**30
 for name in ('actual_stock_rank60_embedding_after175_fast17_screen_v1_20261011','actual_stock_rank60_embedding_after175_large_allocation29_screen_v1_20261011'):
  assert not (A/'service_owned_workflows_20261006'/name).exists(),name
 proof={'status':'verified_childless_idle_scheduler_before_two_independent_TRAIN_score_streams','identity':row,'actual_readonly_stack':r.stdout,'available_memory_before':psutil.virtual_memory().available,'scientific_workers_terminated':0,'scientific_drivers_changed':False,'new_fits':0}
 create(A/'rank60_two_score_streams_pre_retirement_v2_20261011.json',proof)
 assert allowed() and owned(row) and not worker.children()
 worker.terminate();worker.wait(15);parent.terminate();parent.wait(15)
 create(folder/'administrative_supersession_for_two_score_streams_v2_20261011.json',proof)
 from start_fast_completed_owned_service_v1_20261011 import start_service
 p=A/'run_stock_rank60_native42_and_fast46_queue_v2_20261011.py';assert allowed()
 n=start_service('actual_stock_rank60_native42_and_fast46_queue_v2_20261011',p.name,[],{str(p):sha(p),str(Path(__file__)):sha(__file__),str(A/'rank60_two_score_streams_pre_retirement_v2_20261011.json'):sha(A/'rank60_two_score_streams_pre_retirement_v2_20261011.json')})
 create(A/'actual_rank60_two_score_streams_v2_20261011_activation.json',n)
 print({'old_idle_scheduler_retired':True,'new_two_stream_scheduler_owned':True,'scientific_drivers_unchanged':True},flush=True)
if __name__=='__main__':main()
