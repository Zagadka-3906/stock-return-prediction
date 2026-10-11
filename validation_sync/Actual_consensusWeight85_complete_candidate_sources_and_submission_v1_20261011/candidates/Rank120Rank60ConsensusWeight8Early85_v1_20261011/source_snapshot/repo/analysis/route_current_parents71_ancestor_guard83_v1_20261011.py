from pathlib import Path
import sys,types
A=Path(__file__).resolve().parent
def execute(driver):
 from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
 from run_dependency_queue_v3_20261006 import read,sha
 assert allowed();proof=read(A/'actual_ancestor_guard83_future_scope_admission_v1_20261011.json')
 for p,d in proof['input_sha256'].items():assert sha(p)==d,p
 import verified_ancestor_only_current_main_index_guard83_v1_20261011 as guard
 import verified_current_main_source_index_guard_v68_20261011 as original
 name='verified_current_main_source_index_guard_v68_20261011';proxy=types.ModuleType(name);proxy.__dict__.update(vars(original));proxy.audit=guard.audit
 sys.modules[name]=proxy
 import route_current_completed_parents71_and_preflight68_v1_20261011 as current
 previous=current.augment
 def augmented(original,prior):
  result=previous(original,prior);result['service_alias_updates'].update(proof['service_alias_updates']);result['driver_wrappers'].update(proof['child_driver_wrappers']);return result
 current.augment=augmented
 try:
  current.execute(driver)
 finally:
  current.augment=previous;sys.modules[name]=original
