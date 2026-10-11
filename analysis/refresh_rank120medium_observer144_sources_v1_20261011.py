"""Track the genuinely new H120 capacity hypothesis and publish frozen code/control evidence."""
from pathlib import Path
import sys,ast,time,subprocess,psutil
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service

def main():
 assert allowed()
 oldsource=A/'monitor_verified_current_optimization_v143_20261011.py';newsource=A/'monitor_verified_current_optimization_v144_20261011.py'
 names=['actual_rank120medium_twelve_parent183_callbacks_CPU_v2_20261011','actual_rank120medium2048_own6_native42_direct33_queue_v1_20261011','actual_stock_rank120medium_embedding_medium2048_restart_v1_20261011','StockRank120MediumEmbeddingMedium2048_independent_small_CPU_v1_20261011','actual_stock_rank120medium_embedding_medium2048_bank6_v1_20261011','StockRank120MediumEmbeddingMedium2048_independent_full5_GPU_controls_v1_20261011','actual_stock_rank120medium_embedding_six_state_native42_v1_20261011','actual_stock_rank120medium_embedding_after183_direct_allocation33_v1_20261011','actual_rank120medium_after183_completed33_main_v1_20261011','actual_rank120medium2048_gain_selected_full_candidate_queue_v1_20261011','actual_stock_rank120medium_best33_native14_v2_20261011','actual_StockRank120MediumBest33Early_selected_candidate_preparation_v2_20261011','actual_StockRank120MediumBest33Early_selected_candidate_sealing_v3_20261011','actual_rank120medium2048_best33_complete_candidate_main_v1_20261011','actual_verified_rank120medium2048_best33_alternate_delivery_v1_20261011','actual_rank120medium_observer144_sources_main_v1_20261011']
 text=oldsource.read_text(encoding='utf8');needle=' while True:\n  c=read(';assert text.count(needle)==1
 text=text.replace(needle," aliases['actual_byte_exact64_observer143_sources_main_v1_20261011']='actual_byte_exact64_observer143_small_sources_retry2_main_v1_20261011'\n names += "+repr(names)+'\n'+needle)
 text=text.replace('v143_20261011','v144_20261011').replace('v291_20261011','v294_20261011').replace("+'.143.tmp'","+'.144.tmp'")
 # Restore the historical publisher alias after replacing observer version strings.
 text=text.replace('actual_byte_exact64_observer144','actual_byte_exact64_observer143')
 start=text.index("  mb=Path('E:/赛题五_本机临时/stock_rank60medium")
 end=text.index('\n',text.index("  science['rank60medium2048_own6_and_pure33']",start))+1
 block=text[start:end]
 extra=block.replace('stock_rank60medium','stock_rank120medium').replace('StockRank60Medium','StockRank120Medium').replace('rank60medium2048','rank120medium2048')
 text=text[:end]+extra+text[end:]
 ast.parse(text);assert not newsource.exists();newsource.write_text(text,encoding='utf8',newline='\n')
 old=read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_reboot_v143_20261011/native_launch.json');assert owned(old)
 new=start_service('actual_fast_optimization_progress_reboot_v144_20261011',newsource.name,[],{str(newsource):sha(newsource)})
 snap=A/'optimization_live_progress_v144_20261011.json'
 for _ in range(30):
  if snap.exists():break
  time.sleep(1)
 state=read(snap);assert all(n in state['services'] for n in names);assert 'rank120medium2048_own6_and_pure33' in state['science']
 for _ in range(20):
  assert owned(old);dump=subprocess.run([str(A.parent/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(old['owned_worker_pid'])],capture_output=True,text=True,encoding='utf8',check=True).stdout
  if '(idle)' in dump and oldsource.name in dump:break
  time.sleep(1)
 else:raise AssertionError('Preserve active old observer')
 p=psutil.Process(old['owned_worker_pid']);assert owned(old) and not p.children(recursive=True);p.terminate()
 admission=A/'actual_observer144_rank120medium_snapshot_admission_v1_20261011.json';create(admission,{'status':'passed_actual144_H120_capacity_bank_score_and_complete_candidate_gates_observed','new':new,'old':old,'actual_old_idle_stack':dump,'scientific_workers_restarted_or_terminated':0,'new_scores':0})
 files=[Path(__file__),admission,newsource,A/'recover_rank120medium_factory_source_name_v2_20261011.py',A/'actual_byte_exact64_existing180_large_inputs_reference_v1_20261011.json',A/'publish_actual_byte_exact64_observer143_small_sources_retry2_main_v1_20261011.py']
 for name in ['stock_rank120medium2048_own6_full5_native42_direct33_predeclared_sources_v1_20261011.json','rank120medium2048_runtime_sources_import_admission_v1_20261011.json','rank120medium2048_best33_full_candidate_sources_admission_v1_20261011.json','rank120medium2048_full_candidate_runtime_import_admission_v1_20261011.json']:
  q=A/name;files.append(q);files.extend(Path(p) for p in read(q)['input_sha256'])
 template=A/'publish_actual_two_seed37_direct_candidate_observer142_sources_main_v1_20261011.py';s=template.read_text(encoding='utf8');tree=ast.parse(s)
 node=next(n for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='paths' for t in n.targets));lines=s.splitlines(keepends=True);lines[node.lineno-1:node.end_lineno]=['    paths=[Path(p) for p in '+repr([str(p) for p in dict.fromkeys(files)])+']\n']
 s=''.join(lines).replace('two_seed37_direct_candidate_observer142_sources','rank120medium_observer144_sources').replace('预声明双随机种子37项提分后直接完整候选推理及交付；复用已核验CPU证据，完整科学核验保留','冻结120日目标大容量新网络、连续评分及仅提分后完整候选核验；CPU回调通过，尚无训练评分完成声明')
 s=s.replace('actual12_candidate_runtime_imports_capacity109_CDF49_score_gain_only_future_native14_complete37_model_independent_cold80_main_and_delivery_predeclared_no_execution_claim','actual_H120_medium2048_modules_imported_CPU12_parent_callbacks_passed_original_H120_maturity_evidence_reused_new6_fits_full5_native42_score33_and_gain_only_full36_candidate_predeclared_not_executed')
 driver=A/'publish_actual_rank120medium_observer144_sources_main_v1_20261011.py';ast.parse(s);assert not driver.exists();driver.write_text(s,encoding='utf8',newline='\n')
 assert allowed();i=start_service(names[-1],driver.name,[],{str(driver):sha(driver),str(admission):sha(admission)});create(A/'actual_rank120medium_observer144_sources_main_activation_v1_20261011.json',i)
 print('Observer144 actual H120 bank/score/candidate state included; all code and CPU evidence queued to main',flush=True)

if __name__=='__main__':main()
