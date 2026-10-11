from pathlib import Path
import sys,ast,subprocess,psutil,time
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
def main():
 assert allowed();old=A/'monitor_verified_current_optimization_v119_20261011.py'
 s=old.read_text(encoding='utf8').replace('v119','v120').replace('v226','v228').replace('.119.tmp','.120.tmp')
 names=['actual_stock_rank120_own6_full5_native42_direct33_queue_v1_20261011','StockRank120Embedding_actual_mature_fixture_CPU_v1_20261011','StockRank120EmbeddingSmall512_independent_small_CPU_v1_20261011','actual_stock_rank120_embedding_small512_restart_v1_20261011','actual_stock_rank120_embedding_small512_bank6_v1_20261011','StockRank120EmbeddingSmall512_independent_full5_GPU_controls_v1_20261011','actual_stock_rank120_embedding_six_state_native42_v1_20261011','actual_stock_rank120_embedding_after183_direct_allocation33_v1_20261011','actual_rank120_after183_completed33_main_v1_20261011','actual_rank120_actual31_CPU_sources_main_v1_20261011']
 assert s.count(' while True:')==1;s=s.replace(' while True:',' names += '+repr(names)+'\n while True:')
 marker="  delivery=read(A/'latest_verified_submission_delivery_v2_20261008.json')";assert s.count(marker)==1
 section="""  b120=Path('E:/赛题五_本机临时/stock_rank120_embedding_small512_BF16_bank6_v1_20261011');y120=[]
  for y in range(2020,2026):
   p=b120/str(y)/'info.json'
   if p.exists() and read(p)['status']=='passed_actual_complete_mature_BF16_micro_annual_model':y120.append(y)
  f120=Path('E:/赛题五_本机临时/StockRank120EmbeddingSmall512_after183_direct_allocation33_screen_v1_20261011');r120=[read(p) for p in f120.glob('case*_official.json')]
  science['rank120_pure_after183_direct33']={'completed_annual_years':y120,'completed':len(r120),'expected':33,'best_S':max((r['connected_final_score'] for r in r120),default=None),'qualification_pending':True}
"""
 s=s.replace(marker,section+marker);target=A/'monitor_verified_current_optimization_v120_20261011.py';ast.parse(s);assert not target.exists();target.write_text(s,encoding='utf8')
 f=A/'service_owned_workflows_20261006/actual_fast_optimization_progress_reboot_v119_20261011';row=read(f/'native_launch.json');assert owned(row)
 w=psutil.Process(row['owned_worker_pid']);p=psutil.Process(row['pid']);assert not w.children() and p.create_time()==row['owned_parent_creation_time'] and p.cmdline()[1:]==w.cmdline()[1:]
 spy=ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'
 for _ in range(4):
  r=subprocess.run([str(spy),'dump','--pid',str(w.pid)],capture_output=True,text=True,encoding='utf8',check=True,creationflags=subprocess.CREATE_NO_WINDOW)
  if '(idle)' in r.stdout and 'main (monitor_verified_current_optimization_v119_20261011.py:' in r.stdout:break
  time.sleep(1)
 assert '(idle)' in r.stdout and 'main (monitor_verified_current_optimization_v119_20261011.py:' in r.stdout
 proof={'status':'verified_idle_observer_only_replaced_for_actual_new120_pipeline','identity':row,'stack':r.stdout,'input_sha256':{str(q):sha(q) for q in (Path(__file__),old,target)},'scientific_workers_terminated':0}
 create(A/'observer120_actual_admission_v1_20261011.json',proof)
 assert allowed() and owned(row) and not w.children();w.terminate();w.wait(15);p.terminate();p.wait(15);create(f/'administrative_supersession_for_actual_rank120_observer_v1_20261011.json',proof)
 assert allowed();n=start_service('actual_fast_optimization_progress_reboot_v120_20261011',target.name,[],proof['input_sha256']);create(A/'observer120_actual_activation_v1_20261011.json',n)
 print({'actual_rank120_observer120_owned':True},flush=True)
if __name__=='__main__':main()
