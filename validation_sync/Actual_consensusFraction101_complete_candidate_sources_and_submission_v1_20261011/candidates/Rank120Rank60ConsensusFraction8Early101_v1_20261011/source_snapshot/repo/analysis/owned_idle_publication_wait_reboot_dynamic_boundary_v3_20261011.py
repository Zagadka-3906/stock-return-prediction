from pathlib import Path
import time
from owned_idle_publication_wait_reboot_identity_v2_20261011 import hold as original_hold
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def hold(identity,needle):
 import handoff_joint_goss_round97_full_execution_20261006 as h
 def flexible(row,requested):
  parent,worker=h.pair(row)
  for _ in range(180):
   assert allowed()
   before=h.stack(worker.pid)
   guarded='guarded (watch_validations_main_safe_v11_20261010.py:24)'
   boundary=guarded if 'acquire (serial_main_publication_mutex_v1_20261009.py:' in before and guarded in before else requested
   if boundary in before:
    worker.suspend();parent.suspend();after=h.stack(worker.pid)
    if boundary in after and not worker.children():return parent,worker,{'before':before,'after':after,'actual_boundary':boundary,'both_boundaries_before_any_Git_mutation':True}
    parent.resume();worker.resume()
   time.sleep(1)
  raise RuntimeError('Actual owned watcher did not reach either verified idle boundary')
 return original_hold(identity,needle,_original=flexible)
