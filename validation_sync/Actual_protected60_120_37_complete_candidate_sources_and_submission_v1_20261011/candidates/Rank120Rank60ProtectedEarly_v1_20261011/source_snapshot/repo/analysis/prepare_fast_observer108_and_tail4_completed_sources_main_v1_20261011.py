from pathlib import Path
import sys,subprocess,psutil
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from start_fast_completed_owned_service_v1_20261011 import start_service
from handoff_ready_goss_full_execution_20261006 import retire
def main():
 assert allowed();old=A/'monitor_reboot_optimization_v107_20261011.py';new=A/'monitor_reboot_optimization_v108_20261011.py';assert not new.exists()
 p21=A/'completed_score_parent_chain_recovery21_routes_v1_20261011.json';p22=A/'new_objectives_exact_source_recovery22_routes_v1_20261011.json';r21=read(p21);r22=read(p22)
 text=old.read_text(encoding='utf8').replace('v107','v108').replace('.107.tmp','.108.tmp').replace('handoff_v191','handoff_v192')
 insert=" aliases="+repr({**r21['service_aliases'],**r22['service_aliases']})+"\n names=[aliases.get(n,n) for n in names]\n names+="+repr([n for n,d in r21['remaining_tasks']]+[r22['service_aliases'][n] for n,d in r22['remaining_tasks']]+['actual_Tail4_completed_own6_full5_native42_routes2122_sources_main_v1_20261011'])+"\n"
 text=text.replace(' while True:\n',insert+' while True:\n',1);compile(text,str(new),'exec');new.write_text(text,encoding='utf8',newline='\n')
 row=read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_reboot_v107_20261011/native_launch.json');stack=None
 if owned(row):
  p=psutil.Process(row['owned_worker_pid']);assert not p.children();stack=subprocess.run([str(ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(p.pid)],capture_output=True,text=True,timeout=30).stdout;assert 'main (monitor_reboot_optimization_v107_20261011.py:' in stack
  retire(row,'Observer108 resolves actual completed queue2 parent21 and objective22, and keeps the existing live49 scorer')
 proof=A/'fast_observer108_actual_tail4_completed_sources_admission_v1_20261011.json'
 gates=['actual_stock_rank20tail4_embedding_small512_bank6_v1_20261011','StockRank20Tail4EmbeddingSmall512_independent_full5_GPU_controls_v1_20261011','actual_stock_rank20tail4_embedding_six_state_native42_v1_20261011','actual_stock_rank20tail4_embedding_eleven_parent_callbacks_CPU_v1_20261011']
 for n in gates:closed(n)
 paths=[Path(__file__),old,new,p21,p22,A/'stock_rank20tail4_embedding194_full_execution_sources_admission_v1_20261011.json',ROOT/'后续选模标准.md']
 for name in ['actual_stock_rank20tail4_embedding_small512_bank6_location_v1_20261011.json','actual_StockRank20Tail4EmbeddingSmall512_full5_independent_location_v1_20261011.json','actual_stock_rank20tail4_embedding_six_state_native42_location_v1_20261011.json']:
  p=A/name;v=Path(read(p)['output'])/'verification.json';paths.extend([p,v])
 for p in [A/'stock_rank20tail4_weighted_Huber_actual_CPU_controls_v1_20261011.json',A/'stock_rank20tail4_embedding_actual_eleven_parent_callbacks_CPU_controls_v1_20261011.json']:
  paths.append(p)
  for name,d in read(p).get('input_sha256',{}).items():
   assert sha(name)==d,name
   if Path(name).suffix in ('.py','.json'):paths.append(Path(name))
 for pp in [p21,p22,A/'stock_rank20tail4_embedding194_full_execution_sources_admission_v1_20261011.json']:
  for name,d in read(pp)['input_sha256'].items():
   assert sha(name)==d,name
   if Path(name).suffix in ('.py','.json'):paths.append(Path(name))
 create(proof,{'status':'passed_actual_own_tail4_bank6_full5_native42_cold42_prefit7_and_callback11_sources_with_exact_idle_observer_supersession','input_sha256':{str(p):sha(p) for p in dict.fromkeys(paths)},'retired_exact_observer':row,'actual_idle_stack':stack,'new_fits_by_publication':0,'new_quality_scores_by_publication':0,'tail4_official46_and_full_submission_still_pending':True,'future_X_read_for_model_selection':False,'test_labels_read':False})
 assert allowed();r=start_service('actual_fast_optimization_progress_reboot_v108_20261011',new.name,[],{str(new):sha(new),str(proof):sha(proof)});create(A/'actual_fast_optimization_progress_reboot_v108_20261011_activation.json',r)
 template=A/'publish_Rank10_actual_maturity7_sources_main_v1_20261011.py';paths.extend([template,proof]);text=template.read_text(encoding='utf8').replace('Rank10_actual_maturity7','Tail4_completed_own6_full5_native42_routes2122')
 start=text.index('    paths=');end=text.index('    import publish_classifier',start);text=text[:start]+'    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in dict.fromkeys(paths)])+']]\n'+text[end:]
 start=text.index("    payload[(prefix/'manifest.json').as_posix()]");end=text.index('    out=Path(',start)
 manifest={'status':'actual_tail4_weighted_mature_rank20_own6_full5_native42_completed_before_official46_and_future','actual_own_annual_fits':6,'actual_full5_rows_days_stocks':[5635800,1212,4650],'actual_native_cases':42,'actual_cold_cases':42,'actual_prefit_refusals':7,'actual_eleven_parent_callback_checks':11,'actual_independent_loss_CPU_cases':6,'new_quality_scores_by_publication':0,'old_failed_source_helpers_preserved':True,'full194_and_official46_not_yet_claimed':True,'test_labels_read':False}
 text=text[:start]+"    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({**"+repr(manifest)+",'files':bindings})\n"+text[end:]
 driver=A/'publish_Tail4_completed_own6_full5_native42_routes2122_sources_main_v1_20261011.py';assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
 assert allowed();r=start_service('actual_Tail4_completed_own6_full5_native42_routes2122_sources_main_v1_20261011',driver.name,[],{str(driver):sha(driver),str(proof):sha(proof)});create(A/'actual_Tail4_completed_own6_full5_native42_routes2122_sources_main_v1_20261011_activation.json',r)
 print({'actual_observer108_and_completed_tail4_sources_main_queued':True,'new_scientific_scores':0},flush=True)
if __name__=='__main__':main()
