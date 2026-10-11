"""Route raw comparisons to actual completed prerequisites, preserving scientific sources."""
from pathlib import Path
import sys,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed as base_closed
PROOF=A/'actual_raw_science_completed183_current59_admission_v1_20261011.json'
def execute(driver):
 assert allowed();proof=read(PROOF)
 for p,d in proof['input_sha256'].items():assert sha(p)==d,p
 def closed(n):
  seen=set()
  while n in proof['service_alias_updates'] and proof['service_alias_updates'][n]!=n:
   assert n not in seen;seen.add(n);n=proof['service_alias_updates'][n]
  return base_closed(n)
 import owned_idle_publication_wait_reboot_identity_v2_20261011 as old_wait
 from owned_idle_publication_wait_reboot_dynamic_boundary_v3_20261011 import hold
 old_wait.hold=hold
 m=importlib.import_module(Path(driver).stem)
 if hasattr(m,'closed'):m.closed=closed
 # Publishers import this closed function inside main.
 import prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 as checks
 checks.closed=closed
 if hasattr(m,'create'):
  original=m.create
  def create(path,value):
   if isinstance(value,dict) and 'input_sha256' in value:
    value['input_sha256'].update({str(PROOF):sha(PROOF),str(Path(__file__)):sha(__file__)})
   return original(path,value)
  m.create=create
 m.main()
