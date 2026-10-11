"""Replace only the verified idle observer; no scientific handles are changed."""
from pathlib import Path
import sys,ast,time,subprocess
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def main():
 assert allowed()
 source=A/'monitor_verified_current_optimization_v121_20261011.py'
 text=source.read_text(encoding='utf8').replace('v121_20261011','v122_20261011').replace('v230_20261011','v235_20261011').replace("+'.121.tmp'","+'.122.tmp'")
 text=text.replace('range(185,201)','range(185,202)').replace('range(183,201)','range(183,202)')
 needle=' while True:\n  c=read('
 assert text.count(needle)==1
 names=['actual_stock_rank120_direct_embedding35_after200_normalization_queue_v7_20261011','StockRank120DirectEmbedding35_selected_native14_v7_20261011','StockRank120DirectEmbedding201_complete35_family_v7_20261011',
 'actual_StockRank60Fixed17Early2_selected_candidate_preparation_v2_20261011','actual_StockRank60Fixed17Early2_selected_candidate_sealing_v2_20261011','actual_early_fixed60_complete_candidate_and_own_aliases_main_v1_20261011','actual_shared_report_controls_and_fixed60_case17_main_v3_20261011',
 'actual_stock_rank60_fixed_leading_case17_native14_v2_20261011','actual_shared_live_ranking_report180_reader_controls_v1_20261011','actual_shared_live_ranking_report_scope_controls_v1_20261011']
 text=text.replace(needle,' names += '+repr(names)+'\n'+needle)
 marker="  delivery=read(A/'latest_verified_submission_delivery_v2_20261008.json')"
 assert text.count(marker)==1
 block="""  early=A/'StockRank60Fixed17Early2_selected_release_v2_20261011'
  stage={}
  for filename in ['selected_case_before_future_features.json','calibrated_csv_official.json','inference_ready.json','selected_candidate_ready_for_registration.json']:
   p=early/filename
   if p.exists():
    obj=read(p);stage[filename]={'status':obj.get('status'),'S':obj.get('selected_official_score',obj.get('metrics',{}).get('final_score',obj.get('best',{}).get('connected_final_score'))),'new_inference_claimed':obj.get('new_inference_claimed'),'actual_saved_native_models':obj.get('actual_saved_native_models'),'sealed_candidate_complete':obj.get('sealed_candidate_complete')}
  science['rank60_fixed17_early_full_candidate']={'stages':stage,'full_connected_board_and_release_qualification_pending':True}
  def score_values(value):
   if isinstance(value,dict):
    if value.get('best_S') is not None:yield value['best_S']
    for child in value.values():yield from score_values(child)
  pending_highest=max([.4514130257498636,*score_values(science)])
"""
 text=text.replace(marker,block+marker)
 text=text.replace("'pending_cached_highest_S':.4514130257498636","'pending_cached_highest_S':pending_highest").replace("delivery['official_score']>=.4514130257498636","delivery['official_score']>=pending_highest")
 target=A/'monitor_verified_current_optimization_v122_20261011.py';ast.parse(text);assert not target.exists();target.write_text(text,encoding='utf8')
 proof=A/'actual_progress122_early_candidate_and_real_pending_highest_admission_v1_20261011.json'
 create(proof,{'status':'readonly_observer122_includes201_early_fixed_candidate_and_max_actual_scores',
  'input_sha256':{str(p):sha(p) for p in [Path(__file__),source,target]},'science_dispatched':0,'test_labels_read':False})
 from start_fast_completed_owned_service_v1_20261011 import start_service
 assert allowed()
 identity=start_service('actual_fast_optimization_progress_reboot_v122_20261011',target.name,[],{str(proof):sha(proof),str(target):sha(target)})
 for _ in range(60):
  assert allowed() and owned(identity)
  if (A/'optimization_live_progress_v122_20261011.json').exists():break
  time.sleep(1)
 else:raise AssertionError('New observer first snapshot missing; old observer kept')
 old=A/'service_owned_workflows_20261006/actual_fast_optimization_progress_reboot_v121_20261011'
 row=read(old/'native_launch.json');assert owned(row)
 import psutil
 worker=psutil.Process(row['owned_worker_pid']);parent=psutil.Process(row['pid'])
 assert parent.create_time()==row['owned_parent_creation_time'] and not worker.children()
 tool=ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'
 for _ in range(30):
  stack=subprocess.run([str(tool),'dump','--pid',str(worker.pid)],capture_output=True,text=True,encoding='utf8',check=True,creationflags=subprocess.CREATE_NO_WINDOW).stdout
  if '(idle)' in stack and 'main (monitor_verified_current_optimization_v121_20261011.py:' in stack:break
  time.sleep(1)
 else:raise AssertionError('Old observer idle not proven; kept')
 assert allowed() and owned(row) and not worker.children()
 worker.terminate();worker.wait(15);parent.terminate();parent.wait(15)
 create(old/'administrative_supersession_by_observer122.json',{'identity':row,'actual_idle_stack':stack,'new_identity':identity,'scientific_workers_terminated':0})
 create(A/'actual_progress122_activation_v1_20261011.json',{'status':'actual_new_snapshot_verified_old_idle_observer_only_retired','identity':identity,'old_identity':row,'new_fits':0,'new_scores':0})
 print({'actual_readonly_observer122_active':True,'scientific_workers_stopped':0},flush=True)

if __name__=='__main__':main()
