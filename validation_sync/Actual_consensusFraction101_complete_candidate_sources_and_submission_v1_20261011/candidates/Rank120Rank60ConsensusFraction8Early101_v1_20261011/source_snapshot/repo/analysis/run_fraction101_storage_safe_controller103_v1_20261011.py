from pathlib import Path
import sys,runpy
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
assert allowed()
import start_fast_completed_owned_service_v1_20261011 as fast
original=fast.start_service
def dispatch(name,driver,args,pins):
 if driver=='run_Rank120Rank60ConsensusFraction8Early101_selected_candidate_feature_cache_v2_20261011.py':
  p=A/'run_fraction101_same_bytes_TRAIN_link103_candidate_wrapper_v1_20261011.py';return original(name,p.name,args,{**pins,str(p):sha(p),str(Path(__file__)):sha(__file__)})
 return original(name,driver,args,pins)
fast.start_service=dispatch
try:runpy.run_path(str(A/'run_consensusFraction8_results_selection_main_and_conditional101_v1_20261011.py'),run_name='__main__')
finally:fast.start_service=original
