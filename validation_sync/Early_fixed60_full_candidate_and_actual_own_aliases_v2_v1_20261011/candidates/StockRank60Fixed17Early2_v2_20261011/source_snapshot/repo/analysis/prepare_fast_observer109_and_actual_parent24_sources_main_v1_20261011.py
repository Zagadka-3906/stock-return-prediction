from pathlib import Path
import sys,subprocess,psutil
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
from handoff_ready_goss_full_execution_20261006 import retire
def main():
 assert allowed();p24=A/'completed_score_parent_chain_recovery24_routes_v1_20261011.json';p25=A/'new_objectives_exact_source_recovery25_routes_v1_20261011.json';r24=read(p24);r25=read(p25)
 old=A/'monitor_reboot_optimization_v108_20261011.py';new=A/'monitor_reboot_optimization_v109_20261011.py';assert not new.exists();text=old.read_text(encoding='utf8').replace('v108','v109').replace('.108.tmp','.109.tmp').replace('handoff_v192','handoff_v193')
 insert=" aliases.update("+repr({**r24['service_aliases'],**r25['service_aliases']})+")\n names=[aliases.get(n,n) for n in names]\n names+="+repr([n for n,d in r24['remaining_tasks']]+[r25['service_aliases'][n] for n,d in r25['remaining_tasks']]+['actual_parent24_and_new_objectives25_verified_sources_main_v1_20261011'])+"\n"
 text=text.replace(' while True:\n',insert+' while True:\n',1);compile(text,str(new),'exec');new.write_text(text,encoding='utf8',newline='\n')
 row=read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_reboot_v108_20261011/native_launch.json');stack=None
 if owned(row):
  p=psutil.Process(row['owned_worker_pid']);assert not p.children();stack=subprocess.run([str(ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(p.pid)],capture_output=True,text=True,timeout=30).stdout;assert 'main (monitor_reboot_optimization_v108_20261011.py:' in stack
  retire(row,'Observer109 follows actual alias aware24 sealers and25 parent route, preserving live49 and weighted46 scoring')
 paths=[Path(__file__),old,new,p24,p25]
 for pp in [p24,p25]:
  for name,d in read(pp)['input_sha256'].items():
   assert sha(name)==d,name
   if Path(name).suffix in ('.py','.json'):paths.append(Path(name))
 proof=A/'actual_parent24_objectives25_observer109_source_controls_v1_20261011.json';create(proof,{'status':'compiled_actual24_terminal_sealers_184_preparation_reuse_and25_parent_alias_routes','input_sha256':{str(p):sha(p) for p in dict.fromkeys(paths)},'retired_exact_idle_observer_identity':row,'actual_idle_stack':stack,'actual_completed_tail4_model_states':6,'actual_completed_tail4_full5':True,'actual_completed_tail4_native_and_cold':[42,42],'new_quality_scores_by_source_preparation':0,'new_fits':0,'full184_through194_main_not_yet_claimed':True,'test_labels_read':False})
 assert allowed();r=start_service('actual_fast_optimization_progress_reboot_v109_20261011',new.name,[],{str(new):sha(new),str(proof):sha(proof)});create(A/'actual_fast_optimization_progress_reboot_v109_20261011_activation.json',r)
 template=A/'publish_Rank10_actual_maturity7_sources_main_v1_20261011.py';paths.extend([template,proof]);text=template.read_text(encoding='utf8').replace('Rank10_actual_maturity7','Actual_parent24_new_objectives25_sources')
 start=text.index('    paths=');end=text.index('    import publish_classifier',start);text=text[:start]+'    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in dict.fromkeys(paths)])+']]\n'+text[end:]
 start=text.index("    payload[(prefix/'manifest.json').as_posix()]");end=text.index('    out=Path(',start)
 manifest={'status':'actual_verified_source_corrections_and_own6_full5_native42_training_evidence_before_final194_registration','live_rank10_rank20_49_and_weighted_rank20_46_preserved':True,'completed_rank10_46_scores':46,'new_scores_by_publication':0,'original_failed_helper_evidence_preserved':True,'new_model_fits_by_publication':0,'full184_through194_registration_pending':True,'test_labels_read':False}
 text=text[:start]+"    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({**"+repr(manifest)+",'files':bindings})\n"+text[end:]
 driver=A/'publish_actual_parent24_and_new_objectives25_verified_sources_main_v1_20261011.py';assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
 assert allowed();r=start_service('actual_parent24_and_new_objectives25_verified_sources_main_v1_20261011',driver.name,[],{str(driver):sha(driver),str(proof):sha(proof)});create(A/'actual_parent24_and_new_objectives25_verified_sources_main_v1_20261011_activation.json',r)
 print({'actual_observer109_and_current24_25_sources_main_queued':True},flush=True)
if __name__=='__main__':main()
