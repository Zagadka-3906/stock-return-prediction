"""Observe actual two-seed direct candidate gates and publish their frozen source protocol."""
from pathlib import Path
import ast,sys,time,subprocess,psutil
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service

def main():
 assert allowed()
 oldsource=A/'monitor_verified_current_optimization_v141_20261011.py';newsource=A/'monitor_verified_current_optimization_v142_20261011.py'
 names=['actual_rank60_two_seed_protected_twelve_parent_callbacks_CPU_v1_20261011','actual_rank60_two_seed_protected37_early_gaining_candidate_queue_v1_20261011','actual_rank60_two_seed_protected37_early_normalization_v1_20261011','actual_rank60_two_seed_protected37_early_selected_native14_v1_20261011','Rank60TwoSeedProtected37Early_selected_candidate_preparation_v1_20261011','Rank60TwoSeedProtected37Early_selected_candidate_sealing_v1_20261011','actual_rank60_two_seed_protected37_complete_candidate_main_v1_20261011','actual_verified_rank60_two_seed_protected37_alternate_delivery_v1_20261011','actual_two_seed37_direct_candidate_observer142_sources_main_v1_20261011']
 text=oldsource.read_text(encoding='utf-8');needle=' while True:\n  c=read(';assert text.count(needle)==1
 text=text.replace(needle,' names += '+repr(names)+'\n'+needle).replace('v141_20261011','v142_20261011').replace('v282_20261011','v286_20261011').replace("+'.141.tmp'","+'.142.tmp'")
 ast.parse(text);assert not newsource.exists();newsource.write_text(text,encoding='utf-8',newline='\n')
 old=read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_reboot_v141_20261011/native_launch.json');assert owned(old)
 new=start_service('actual_fast_optimization_progress_reboot_v142_20261011',newsource.name,[],{str(newsource):sha(newsource),str(oldsource):sha(oldsource)})
 snap=A/'optimization_live_progress_v142_20261011.json'
 for _ in range(30):
  if snap.exists():break
  time.sleep(1)
 assert snap.exists();state=read(snap);assert all(n in state['services'] for n in names)
 for _ in range(20):
  assert owned(old);dump=subprocess.run([str(A.parent/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(old['owned_worker_pid'])],capture_output=True,text=True,encoding='utf-8',check=True).stdout
  if '(idle)' in dump and oldsource.name in dump:break
  time.sleep(1)
 else:raise AssertionError('Preserve active old observer')
 p=psutil.Process(old['owned_worker_pid']);assert owned(old) and not p.children(recursive=True);p.terminate()
 admission=A/'actual_observer142_two_seed37_direct_candidate_snapshot_admission_v1_20261011.json'
 create(admission,{'status':'passed_actual142_all_gain_only_two_seed37_full_candidate_gates_observed','new':new,'old':old,'actual_old_idle_stack':dump,'input_sha256':{str(p):sha(p) for p in [Path(__file__),oldsource,newsource]},'scientific_workers_restarted_or_terminated':0,'new_scientific_scores_claimed':0})
 proof=A/'rank60_two_seed_protected37_early_sources_admission_v2_20261011.json'
 files=[Path(p) for p in read(proof)['input_sha256']]+[proof,A/'actual_two_seed37_early_queue_after_completed_short_CPU_launch_race_admission_v1_20261011.json',A/'rank60_two_seed_actual_completed_CPU12_gate_bridge_admission_v1_20261011.json',admission,newsource]
 template=A/'publish_actual_capacity109_CDF49_complete_candidate_sources_main_v1_20261011.py';text=template.read_text(encoding='utf-8');tree=ast.parse(text)
 node=next(n for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='paths' for t in n.targets));lines=text.splitlines(keepends=True)
 lines[node.lineno-1:node.end_lineno]=['    paths=[Path(p) for p in '+repr([str(p) for p in dict.fromkeys(files)])+']\n']
 text=''.join(lines).replace('capacity109_CDF49_gaining_complete_candidate_sources','two_seed37_direct_candidate_observer142_sources').replace('预声明大小网络109项及CDF49项提分后完整候选核验、main同步与交付；12模块实际导入验证通过','预声明双随机种子37项提分后直接完整候选推理及交付；复用已核验CPU证据，完整科学核验保留')
 driver=A/'publish_actual_two_seed37_direct_candidate_observer142_sources_main_v1_20261011.py';ast.parse(text);assert not driver.exists();driver.write_text(text,encoding='utf-8',newline='\n')
 assert allowed();i=start_service(names[-1],driver.name,[],{str(driver):sha(driver),str(proof):sha(proof)});create(A/'actual_two_seed37_direct_candidate_observer142_sources_main_activation_v1_20261011.json',i)
 print('Actual observer142 includes all direct two-seed candidate gates; source publication queued to main',flush=True)

if __name__=='__main__':main()
