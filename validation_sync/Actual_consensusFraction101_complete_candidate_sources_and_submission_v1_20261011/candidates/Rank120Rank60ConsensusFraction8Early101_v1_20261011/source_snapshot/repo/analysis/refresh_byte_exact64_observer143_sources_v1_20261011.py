"""Observe actual64 routing and freeze proven byte-identical performance sources to main."""
from pathlib import Path
import ast,sys,time,subprocess,psutil
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service

def main():
 assert allowed()
 oldsource=A/'monitor_verified_current_optimization_v142_20261011.py';newsource=A/'monitor_verified_current_optimization_v143_20261011.py'
 proof=A/'verified_future_byte_exact64_admission_v1_20261011.json';data=read(proof)
 names=['actual_verified_future_byte_exact64_v1_20261011','actual_identity_codec_bounded_HTML_exact18_scope_controls_v1_20261011','actual_identity_memoized_lossless_codec_full180_controls_v1_20261011','actual_bounded_original_ranking_HTML_full180_controls_v1_20261011','actual_bounded_original_ranking_HTML_tail_and_scope_controls_v1_20261011','actual_bounded_HTML_exact_future18_shared_scopes_controls_v1_20261011','actual_byte_exact64_observer143_sources_main_v1_20261011']
 text=oldsource.read_text(encoding='utf8');needle=' while True:\n  c=read(';assert text.count(needle)==1
 text=text.replace(needle," latest=read(A/"+repr(proof.name)+");aliases.update(latest['service_alias_updates']);names += [n for n,d in latest['tasks']]\n names += "+repr(names)+'\n'+needle).replace('v142_20261011','v143_20261011').replace('v286_20261011','v291_20261011').replace("+'.142.tmp'","+'.143.tmp'")
 ast.parse(text);assert not newsource.exists();newsource.write_text(text,encoding='utf8',newline='\n')
 old=read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_reboot_v142_20261011/native_launch.json');assert owned(old)
 new=start_service('actual_fast_optimization_progress_reboot_v143_20261011',newsource.name,[],{str(newsource):sha(newsource),str(proof):sha(proof)})
 snap=A/'optimization_live_progress_v143_20261011.json'
 for _ in range(30):
  if snap.exists():break
  time.sleep(1)
 state=read(snap);assert all(n in state['services'] for n in names)
 for _ in range(20):
  assert owned(old);dump=subprocess.run([str(A.parent/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(old['owned_worker_pid'])],capture_output=True,text=True,encoding='utf8',check=True).stdout
  if '(idle)' in dump and oldsource.name in dump:break
  time.sleep(1)
 else:raise AssertionError('Preserve active old observer')
 p=psutil.Process(old['owned_worker_pid']);assert owned(old) and not p.children(recursive=True);p.terminate()
 admission=A/'actual_observer143_byte_exact64_snapshot_admission_v1_20261011.json'
 create(admission,{'status':'passed_actual143_current64_future_and_performance_proofs_observed','new':new,'old':old,'actual_old_idle_stack':dump,'input_sha256':{str(p):sha(p) for p in [Path(__file__),oldsource,newsource]},'scientific_workers_restarted_or_terminated':0,'new_scores':0})
 files=[proof,admission,newsource,*[Path(p) for p in data['input_sha256']]]
 for name in ['identity_codec_and_bounded_HTML_actual18_scope_admission_v1_20261011.json','bounded_original_ranking_HTML_actual_full180_and_scope_admission_v1_20261011.json','bounded_original_HTML_exact_future18_shared_scopes_admission_v1_20261011.json']:
  q=A/name;files.append(q);files.extend(Path(p) for p in read(q)['input_sha256'])
 for name in ['actual_identity_memoized_lossless_codec_full180_location_v1_20261011.json','actual_bounded_original_ranking_HTML_full180_location_v1_20261011.json']:
  q=A/name;v=Path(read(q)['output'])/'verification.json';files += [q,v];files.extend(Path(p) for p in read(v)['input_sha256'])
 template=A/'publish_actual_two_seed37_direct_candidate_observer142_sources_main_v1_20261011.py';text=template.read_text(encoding='utf8');tree=ast.parse(text)
 node=next(n for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='paths' for t in n.targets));lines=text.splitlines(keepends=True)
 lines[node.lineno-1:node.end_lineno]=['    paths=[Path(p) for p in '+repr([str(p) for p in dict.fromkeys(files)])+']\n']
 text=''.join(lines).replace('two_seed37_direct_candidate_observer142_sources','byte_exact64_observer143_sources').replace('预声明双随机种子37项提分后直接完整候选推理及交付；复用已核验CPU证据，完整科学核验保留','完整第180轮报告字节与18组作用域实测通过；仅未来轮次启用有界HTML及共享节点编码复用')
 text=text.replace('actual12_candidate_runtime_imports_capacity109_CDF49_score_gain_only_future_native14_complete37_model_independent_cold80_main_and_delivery_predeclared_no_execution_claim','actual_complete180_every_original_codec_node_and_HTML_bytes_exact_all18_scopes_proven_future64_only_adopted_original_per_round_QA_still_required')
 driver=A/'publish_actual_byte_exact64_observer143_sources_main_v1_20261011.py';ast.parse(text);assert not driver.exists();driver.write_text(text,encoding='utf8',newline='\n')
 assert allowed();i=start_service(names[-1],driver.name,[],{str(driver):sha(driver),str(proof):sha(proof)});create(A/'actual_byte_exact64_observer143_sources_main_activation_v1_20261011.json',i)
 print('Actual143 snapshot verified; old idle observer retired; performance proof/source main publication queued',flush=True)

if __name__=='__main__':main()
