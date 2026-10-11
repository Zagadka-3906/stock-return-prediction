from pathlib import Path
import sys,ast
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
assert allowed()
original=A/'monitor_verified_current_optimization_v148_20261011.py'
s=original.read_text(encoding='utf8').replace('v148','v149').replace('.148.tmp','.149.tmp').replace('actual_optimization_fast_runtime_handoff_v305','actual_optimization_fast_runtime_handoff_v308').replace('actual191_then_disagreement10_science_priority72_then_original48_v1_20261011','actual191_then_disagreement10_and_CDF8_science_priority75_then_original48_v1_20261011')
names=['actual_disagreement10_conditional_full_pipeline73_v1_20261011','actual_rank120_rank60_disagreement10_early73_normalization_v1_20261011','actual_rank120_rank60_disagreement10_early73_selected_native14_v1_20261011','Rank120Rank60Disagreement10Early73_selected_candidate_preparation_v1_20261011','Rank120Rank60Disagreement10Early73_selected_candidate_sealing_v1_20261011','actual_disagreement73_conditional_main_delivery_v1_20261011','actual_disagreement73_complete_candidate_main_v1_20261011','actual_verified_disagreement73_alternate_submission_delivery_v1_20261011','actual_rank120_rank60_after183_disagreement_CDF8_screen75_v1_20261011','actual_disagreement_CDF8_results_selection_main75_v1_20261011','actual_disagreement73_full_native_pipeline_sources_main_v1_20261011','actual_checkpoint_cleanup_and_QA_E_relocation74_main_v1_20261011']
assert s.count(' while True:')==1;s=s.replace(' while True:',' names += '+repr(names)+'\n while True:',1)
needle="  write(A/'optimization_live_progress_v149_20261011.json',state)";assert s.count(needle)==1
injection="""  d=Path('E:/赛题五_本机临时/StockRank120Rank60_after183_disagreement_CDF8_screen75_v1_20261011');rs=[read(p) for p in d.glob('case*_official.json')];science['rank120_rank60_disagreement_CDF8']={'completed':len(rs),'expected':8,'best_S':max((r['connected_final_score'] for r in rs),default=None),'actual_full_scoring_complete':(d/'verification.json').exists(),'native_candidate_complete_not_assumed':True}
  decision=A/'rank120_rank60_disagreement10_gain_decision_v1_20261011.json';science['actual_disagreement10_S_selection']={'actual':read(decision) if decision.exists() else None,'full_new_candidate_complete':(A/'rank120_rank60_disagreement10_selected_full_candidate_complete_v1_20261011.json').exists()}
  state['pending_cached_highest_S']=max([.4514130257498636,*score_values(science)])
  state['pending_cached_highest_submission_qualified']=delivery['official_score']>=state['pending_cached_highest_S']
  state['pending_cached_highest_native_candidate_verified']=bool(best_sealed and best_sealed['delivery']['official_TRAIN_internal_score']>=state['pending_cached_highest_S'])
"""
s=s.replace(needle,injection+needle);p=A/'monitor_verified_current_optimization_v149_20261011.py';ast.parse(s);assert not p.exists();p.write_text(s,encoding='utf8')
r=start_service('actual_fast_optimization_progress_reboot_v149_20261011',p.name,[],{str(p):sha(p)});create(A/'actual_observer149_disagreement_gain_CDF75_activation_v1_20261011.json',r)
import time
for _ in range(12):
 if (A/'optimization_live_progress_v149_20261011.json').is_file():break
 time.sleep(.3)
snapshot=read(A/'optimization_live_progress_v149_20261011.json');assert snapshot['science']['rank120_rank60_disagreement10']['completed']==10 and snapshot['science']['actual_disagreement10_S_selection']['actual']['adopt'] is True and all(n in snapshot['services'] for n in names)
folder=A/'service_owned_workflows_20261006/actual_fast_optimization_progress_reboot_v148_20261011';identity=read(folder/'native_launch.json');assert owned(identity)
import handoff_joint_goss_round97_full_execution_20261006 as h
parent,worker=h.pair(identity);before=h.stack(worker.pid)
assert '(idle)' in before and 'monitor_verified_current_optimization_v148_20261011.py:' in before and not worker.children()
worker.suspend();parent.suspend();after=h.stack(worker.pid)
if not ('(idle)' in after and 'monitor_verified_current_optimization_v148_20261011.py:' in after and not worker.children()):
 parent.resume();worker.resume();raise AssertionError(after)
worker.terminate();parent.terminate()
create(A/'actual_observer149_disagreement10_gain_and_CDF8_snapshot_admission_v1_20261011.json',{'status':'passed_actual_new149_snapshot_all10_complete_gain9_selected_native_pending_and_actual_CDF8_sources_admitted_old148_only_verified_idle_retired','input_sha256':{str(q):sha(q) for q in [Path(__file__),original,p]},'actual_selected_TRAIN_S':snapshot['science']['rank120_rank60_disagreement10']['best_S'],'current_native_candidate_complete_not_claimed':True,'actual_old_idle_before':before,'actual_old_idle_after':after,'scientific_workers_not_modified_or_stopped':True})
print({'actual_observer149_ready':True,'all10_best_S':snapshot['science']['rank120_rank60_disagreement10']['best_S'],'CDF8_real_service_admitted':True},flush=True)
