"""Freeze uncovered horizon disagreement CDF allocations that can change official Top sets."""
from pathlib import Path
import sys,ast
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
def main():
 assert allowed()
 original=A/'run_rank120_rank60_after183_disagreement10_screen_v1_20261011.py';s=original.read_text(encoding='utf8')
 tree=ast.parse(s);node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='cases');original_cases=ast.literal_eval(node.body[0].value)
 cases=original_cases[:2]+[{'kind':'CDF','role':'nonflag_valid','weight':w,'sign':1.,'protect_fraction':None,'disagreement_penalty':k} for k in (-.5,.5) for w in (.032,.128,.512)]
 lines=s.splitlines(keepends=True);lines[node.lineno-1:node.end_lineno]=['def cases():\n    return '+repr(cases)+'\n'];s=''.join(lines)
 s=s.replace('StockRank120Rank60_after183_disagreement10_screen_v1_20261011','StockRank120Rank60_after183_disagreement_CDF8_screen75_v1_20261011')
 s=s.replace("    closed('actual_fraction38_completed_namespace_bridge_v1_20261011')","    closed('actual_completed_disagreement10_pointer_namespace_bridge72_v1_20261011')\n    closed('actual_fraction38_completed_namespace_bridge_v1_20261011')",1)
 s=s.replace("A/'rank120_rank60_disagreement10_predeclared_sources_admission_v1_20261011.json'","A/'rank120_rank60_disagreement_CDF8_predeclared_sources75_v1_20261011.json'")
 for before,after in [("'completed_cases':len(records),'expected_cases':10","'completed_cases':len(records),'expected_cases':8"),("'new_quality_score_records':10","'new_quality_score_records':8"),("'actual_nonidentity_full_controls':9","'actual_nonidentity_full_controls':7"),("'actual_nonidentity_prefix_controls':27","'actual_nonidentity_prefix_controls':21"),('passed10_disagreement','passed8_disagreement_CDF75'),('frozen10_disagreement','frozen8_disagreement_CDF75'),('actual_disagreement_rank120_rank60_10_TRAIN','actual_disagreement_CDF75_rank120_rank60_8_TRAIN'),("A/'actual_StockRank120Rank60_after183_best_blend_fraction38_screen_location_v1_20261011.json'","A/'actual_StockRank120Rank60_after183_disagreement_CDF8_screen75_location_v1_20261011.json'")]:s=s.replace(before,after)
 q=A/'run_rank120_rank60_after183_disagreement_CDF8_screen75_v1_20261011.py';ast.parse(s);assert not q.exists();q.write_text(s,encoding='utf8')
 proof=A/'rank120_rank60_disagreement_CDF8_predeclared_sources75_v1_20261011.json'
 create(proof,{'status':'frozen8_TRAIN_only_cases6_uncovered_disagreement_CDF_nonflag_valid_allocations_can_change_official_Top_membership_before_actual_controls_and_scores','cases':cases,'input_sha256':{str(p):sha(p) for p in [Path(__file__),original,q,A/'rank120_rank60_disagreement_raw_signal_v1_20261011.py',A/'rank120_rank60_disagreement_actual_CPU_controls_v1_20261011.json',A/'BF16Medium153_complete_parent_rank_CDF_v1_20261009.py']},'expected_full_nonidentity_Pandas':7,'expected_prefix_controls':21,'new_model_fits':0,'future_X_read':False,'test_labels_read':False,'hypothesis_not_actual_gain_claim':True})
 queue_original=A/'run_actual191_then_disagreement10_science_priority72_then_original48_v1_20261011.py'
 queue=queue_original.read_text(encoding='utf8');needle=" proof=A/'actual_current_completed_parents71_child_propagation_admission_v1_20261011.json'"
 assert queue.count(needle)==1;queue=queue.replace(needle," closed('actual_rank120_rank60_after183_disagreement_CDF8_screen75_v1_20261011')\n closed('actual_disagreement_CDF8_results_selection_main75_v1_20261011')\n"+needle)
 queuefile=A/'run_actual191_then_disagreement10_and_CDF8_science_priority75_then_original48_v1_20261011.py';ast.parse(queue);assert not queuefile.exists();queuefile.write_text(queue,encoding='utf8')
 admission=A/'actual_disagreement_CDF8_priority75_admission_v1_20261011.json';create(admission,{'status':'frozen_original48_tasks_unchanged_after_current191_and_raw10_and_conditional_complete_candidate_and_additional_actual_CDF8_results_before_heavy_future_reports','input_sha256':{str(p):sha(p) for p in [Path(__file__),queue_original,queuefile,q,proof]},'raw10_current191_scientific_workers_unchanged':True})
 # Retire only the verified idle administrative queue, never a scientific worker.
 folder=A/'service_owned_workflows_20261006/actual191_then_disagreement10_science_priority72_then_original48_v1_20261011';identity=read(folder/'native_launch.json');assert owned(identity)
 import handoff_joint_goss_round97_full_execution_20261006 as h
 parent,worker=h.pair(identity);before=h.stack(worker.pid)
 assert '(idle)' in before and 'closed (prepare_protected_tail_pilot76_and_selected_native14_v1_20261010.py:' in before and not worker.children(),before
 worker.suspend();parent.suspend()
 after=h.stack(worker.pid)
 if not ('(idle)' in after and 'closed (prepare_protected_tail_pilot76_and_selected_native14_v1_20261010.py:' in after and not worker.children()):
  parent.resume();worker.resume();raise AssertionError(after)
 create(A/'actual_idle_administrative_priority72_retirement_for_new_science75_v1_20261011.json',{'status':'actual_verified_idle_only_no_children_before_and_after_hold','identity':identity,'before':before,'after':after,'scientific_workers_not_stopped_or_restarted':True})
 worker.terminate();parent.terminate()
 for name,p in [('actual_rank120_rank60_after183_disagreement_CDF8_screen75_v1_20261011',q),('actual191_then_disagreement10_and_CDF8_science_priority75_then_original48_v1_20261011',queuefile)]:
  assert allowed();r=start_service(name,p.name,[],{str(p):sha(p),str(admission):sha(admission),str(proof):sha(proof)});create(A/(name+'_activation.json'),r)
 print({'additional_uncovered_CDF_cases':6,'total8_including_two_exact_references':True,'original48_tasks_preserved':True,'new_science_pending':True},flush=True)
if __name__=='__main__':main()
