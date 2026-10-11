from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
import handoff_joint_goss_round97_full_execution_20261006 as h
assert allowed();folder=A/'service_owned_workflows_20261006/actual_consensusFraction8_results_selection_main101_v1_20261011';identity=read(folder/'native_launch.json');assert owned(identity) and not (folder/'service_execution.json').exists()
parent,worker=h.pair(identity);before=h.stack(worker.pid)
def idle(stack):return '(idle)' in stack and 'closed (prepare_protected_tail_pilot76_and_selected_native14_v1_20261010.py:' in stack and 'main (run_consensusFraction8_results_selection_main_and_conditional101_v1_20261011.py:' in stack
assert idle(before) and not worker.children(),before
worker.suspend();parent.suspend();after=h.stack(worker.pid)
if not (idle(after) and not worker.children()):parent.resume();worker.resume();raise AssertionError(after)
p=A/'run_fraction101_storage_safe_controller103_v1_20261011.py';proof=A/'actual_idle_fraction101_storage_safe103_controller_admission_v1_20261011.json';create(proof,{'status':'actual_idle_administrative_wait_only_replaced_before_any_fraction101_dispatch_same_bytes_canonical_TRAIN_links_only_all_original_native_scoring_qualification_preserved','identity':identity,'before':before,'after':after,'input_sha256':{str(q):sha(q) for q in [Path(__file__),p,A/'run_fraction101_same_bytes_TRAIN_link103_candidate_wrapper_v1_20261011.py',A/'rank120_rank60_consensusFraction8_early101_sources_admission_v2_20261011.json']},'native_or_scientific_workers_stopped':0,'test_labels_read':False})
worker.terminate();parent.terminate();name='actual_consensusFraction8_storage_safe_results_main103_v1_20261011';assert allowed();r=start_service(name,p.name,[],{str(p):sha(p),str(proof):sha(proof)});create(A/(name+'_activation.json'),r)
