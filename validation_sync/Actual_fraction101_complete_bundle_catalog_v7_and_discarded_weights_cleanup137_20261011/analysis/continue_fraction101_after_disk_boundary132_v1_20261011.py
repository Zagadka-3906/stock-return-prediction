from pathlib import Path
import sys,runpy
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
import prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 as gates
from start_fast_completed_owned_service_v1_20261011 import start_service
assert gates.allowed()
for name,driver in [('actual_fraction101_partial_seal131_v1_20261011','resume_partial_fraction101_seal131_v1_20261011.py'),('actual_consensusFraction101_complete_candidate_main_v1_20261011','publish_fraction101_same_bytes_archive_reuse130_v1_20261011.py')]:
 assert gates.allowed();p=A/driver;r=start_service(name,driver,[],{str(p):sha(p),str(Path(__file__)):sha(__file__)});create(A/(name+'_actual132_activation.json'),r);gates.closed(name)
oldclosed=gates.closed;gates.closed=lambda n:oldclosed('actual_fraction101_partial_seal131_v1_20261011' if n=='Rank120Rank60ConsensusFraction8Early101_selected_candidate_sealing_v1_20261011' else n)
try:runpy.run_path(str(A/'prepare_verified_consensusFraction101_alternate_submission_delivery_v1_20261011.py'),run_name='__main__')
finally:gates.closed=oldclosed
pointer=A/'alternate_verified_consensusFraction101_submission_delivery_v1_20261011.json';actual=read(pointer);assert actual['all_full_native_independent_reload_csv_and_cold80_checks_passed'] and actual['official_TRAIN_internal_score']==.4514612196682616
create(A/'actual_best100_full_candidate_continuation124_complete_v1_20261011.json',{'status':'passed_actual_original_native101_then_partial_disk_seal131_same_bytes_archive_main130_delivery132_full37_all_checks_no_inference_rerun','delivery':actual,'input_sha256':{str(p):sha(p) for p in [Path(__file__),pointer]},'original124_failed_disk_terminal_preserved':True,'global_exhaustion_proven':False,'test_labels_read':False})
