"""Check the actual reboot watcher by full identity, never a historical reused PID."""
from run_dependency_queue_v3_20261006 import read,owned
from pathlib import Path
from serial_main_publication_mutex_v1_20261009 import MainPublicationMutex
A=Path(__file__).resolve().parent
def hold(identity,needle,_original=None):
 import handoff_joint_goss_round97_full_execution_20261006 as handoff
 original=_original or handoff.suspended_idle
 current=read(A/'service_owned_workflows_20261006/main_publisher_reboot_v12_20261011/native_launch.json')
 assert identity['name']==current['name']
 assert (identity['owned_worker_pid'],identity['owned_worker_creation_time'],identity['owned_parent_creation_time'])==(current['owned_worker_pid'],current['owned_worker_creation_time'],current['owned_parent_creation_time'])
 assert owned(identity) and owned(current)
 mutex=MainPublicationMutex();mutex.acquire()
 try:
  before=handoff.stack(identity['owned_worker_pid'])
  if 'acquire (serial_main_publication_mutex_v1_20261009.py:' in before and 'guarded (watch_validations_main_safe_v11_20261010.py:24)' in before:needle='guarded (watch_validations_main_safe_v11_20261010.py:24)'
  return original(identity,needle)
 finally:mutex.close()
