from pathlib import Path
import sys,subprocess,psutil
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
from handoff_ready_goss_full_execution_20261006 import retire
def main():
 assert allowed();old=A/'verify_stock_rank20tail4_embedding_small512_small_CPU_v1_20261011.py';new=A/'verify_stock_rank20tail4_embedding_small512_small_CPU_v2_20261011.py';assert not new.exists()
 text=old.read_text(encoding='utf8').replace('actual_stock_rank20tail4_embedding_small512_restart_v1_20261011','actual_stock_rank20tail4_embedding_small512_restart_v2_20261011')
 compile(text,str(new),'exec');new.write_text(text,encoding='utf8',newline='\n')
 assert not (A/'service_owned_workflows_20261006/StockRank20Tail4EmbeddingSmall512_independent_small_CPU_v1_20261011/native_launch.json').exists()
 oldqueue=A/'run_stock_rank20tail4_own_training_and_full5_queue_v2_20261011.py';queue=A/'run_stock_rank20tail4_own_training_and_full5_queue_v3_20261011.py';assert not queue.exists()
 text=oldqueue.read_text(encoding='utf8').replace("('actual_stock_rank20tail4_embedding_small512_restart_v2_20261011','verify_stock_rank20tail4_embedding_small512_restart_v2_20261011.py'),",'')
 text=text.replace(" for name,driver in ["," closed('actual_stock_rank20tail4_embedding_small512_restart_v2_20261011')\n for name,driver in [")
 text=text.replace(old.name,new.name);compile(text,str(queue),'exec');queue.write_text(text,encoding='utf8',newline='\n')
 row=read(A/'service_owned_workflows_20261006/actual_stock_rank20tail4_own_training_and_full5_queue_v2_20261011/native_launch.json');stack=None
 if owned(row):
  p=psutil.Process(row['owned_worker_pid']);assert not p.children();stack=subprocess.run([str(ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(p.pid)],capture_output=True,text=True,timeout=30).stdout;assert 'closed (' in stack,(row,stack)
  retire(row,'Replace only exact idle queue after restart2 dispatch; new CPU helper references actual restart2, existing live scientific restart2 left running')
 proof=A/'stock_rank20tail4_restart2_CPU_and_own6_queue_sources_admission_v3_20261011.json'
 create(proof,{'status':'compiled_fresh_CPU_helper_and_post_restart2_training_queue_live_restart2_not_restarted','input_sha256':{str(p):sha(p) for p in [Path(__file__),old,new,oldqueue,queue]},'old_queue_identity':row,'idle_stack':stack,'scientific_workers_terminated':0,'new_fits':0,'new_scores':0})
 r=start_service('actual_stock_rank20tail4_own_training_and_full5_queue_v3_20261011',queue.name,[],{str(queue):sha(queue),str(proof):sha(proof)});create(A/'actual_stock_rank20tail4_own_training_and_full5_queue_v3_activation_20261011.json',r)
 print({'live_restart2_retained_CPU2_and_own6_queue3_dispatched':True},flush=True)
if __name__=='__main__':main()
