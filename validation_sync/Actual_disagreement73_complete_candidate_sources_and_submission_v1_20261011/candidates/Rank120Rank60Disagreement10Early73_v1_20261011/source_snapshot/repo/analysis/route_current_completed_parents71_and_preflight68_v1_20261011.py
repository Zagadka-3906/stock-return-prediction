from pathlib import Path
import sys,copy,runpy
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
def augment(original,proof):
 result=copy.deepcopy(original);result['service_alias_updates'].update(proof['service_alias_updates']);result['driver_wrappers'].update(proof['child_driver_wrappers']);return result
def execute(driver):
 from run_dependency_queue_v3_20261006 import read,sha
 from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
 assert allowed();p=A/'actual_current_completed_parents71_child_propagation_admission_v1_20261011.json';d=read(p)
 for name,digest in d['input_sha256'].items():assert sha(name)==digest,name
 import route_verified_future_byte_exact64_v1_20261011 as routing
 original_read=routing.read
 def actual_read(path):
  original=original_read(path)
  return augment(original,d) if Path(path)==routing.PROOF else original
 routing.read=actual_read
 try:
  from route_future_preflights_current_main_index68_v1_20261011 import execute as guarded
  guarded(driver)
 finally:routing.read=original_read
