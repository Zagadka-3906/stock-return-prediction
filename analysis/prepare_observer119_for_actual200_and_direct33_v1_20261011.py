from pathlib import Path
import sys,ast,subprocess,psutil,time
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
def main():
 assert allowed()
 old=A/'monitor_verified_current_optimization_v118_20261011.py'
 text=old.read_text(encoding='utf8').replace('v118','v119').replace('v223','v226').replace('.118.tmp','.119.tmp').replace('range(185,200)','range(185,201)').replace('range(183,200)','range(183,201)')
 names=['actual_stock_rank60_embedding_after183_direct_allocation33_v1_20261011','actual_rank60_after183_completed33_main_v1_20261011','actual_rank60_direct33_predeclared_CPU_sources_main_v1_20261011','actual_stock_rank60_direct_embedding35_after199_normalization_queue_v6_20261011','StockRank60DirectEmbedding35_selected_native14_v6_20261011','StockRank60DirectEmbedding200_complete35_family_v6_20261011','actual_complete200_actual_v6_sources_main_v1_20261011']
 assert text.count(' while True:')==1;text=text.replace(' while True:',' names += '+repr(names)+'\n while True:')
 marker="  delivery=read(A/'latest_verified_submission_delivery_v2_20261008.json')";assert text.count(marker)==1
 section="""  direct=Path('E:/赛题五_本机临时/StockRank60EmbeddingSmall512_after183_direct_allocation33_screen_v1_20261011');directrows=[read(p) for p in direct.glob('case*_official.json')]
  science['rank60_pure_after183_direct33']={'completed':len(directrows),'expected':33,'best_S':max((r['connected_final_score'] for r in directrows),default=None),'qualification_pending':True}
"""
 text=text.replace(marker,section+marker);target=A/'monitor_verified_current_optimization_v119_20261011.py';ast.parse(text);assert not target.exists();target.write_text(text,encoding='utf8')
 f=A/'service_owned_workflows_20261006/actual_fast_optimization_progress_reboot_v118_20261011';row=read(f/'native_launch.json');assert owned(row)
 w=psutil.Process(row['owned_worker_pid']);p=psutil.Process(row['pid']);assert not w.children() and p.create_time()==row['owned_parent_creation_time'] and p.cmdline()[1:]==w.cmdline()[1:]
 spy=ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'
 for _ in range(4):
  r=subprocess.run([str(spy),'dump','--pid',str(w.pid)],capture_output=True,text=True,encoding='utf8',check=True,creationflags=subprocess.CREATE_NO_WINDOW)
  if '(idle)' in r.stdout and 'main (monitor_verified_current_optimization_v118_20261011.py:' in r.stdout:break
  time.sleep(1)
 assert '(idle)' in r.stdout and 'main (monitor_verified_current_optimization_v118_20261011.py:' in r.stdout
 proof={'status':'verified_idle_observer_only_replaced_for_actual200_and_direct33','identity':row,'stack':r.stdout,'input_sha256':{str(q):sha(q) for q in (Path(__file__),old,target)},'scientific_workers_terminated':0}
 create(A/'observer119_actual_admission_v1_20261011.json',proof)
 assert allowed() and owned(row) and not w.children();w.terminate();w.wait(15);p.terminate();p.wait(15);create(f/'administrative_supersession_for_actual200_observer119_v1_20261011.json',proof)
 assert allowed();n=start_service('actual_fast_optimization_progress_reboot_v119_20261011',target.name,[],proof['input_sha256']);create(A/'observer119_actual_activation_v1_20261011.json',n)
 print({'actual200_and_direct33_observer119_owned':True},flush=True)
if __name__=='__main__':main()
