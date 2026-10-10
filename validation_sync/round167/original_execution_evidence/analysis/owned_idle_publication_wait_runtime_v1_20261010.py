"""Recognize an owned watcher blocked on our publication mutex before any Git mutation."""
from contextlib import contextmanager
from pathlib import Path
import time
from serial_main_publication_mutex_v1_20261009 import MainPublicationMutex
from run_dependency_queue_v3_20261006 import read,create,owned
A=Path(__file__).resolve().parent

def hold(identity,needle,_original=None):
    import handoff_joint_goss_round97_full_execution_20261006 as handoff
    original=_original or handoff.suspended_idle
    mutex=MainPublicationMutex();mutex.acquire()
    try:
        launcher=read(A/'service_owned_workflows_20261006/main_publisher_v11_20261010/native_launch.json')
        if identity['owned_worker_pid']==launcher['owned_worker_pid']:
            assert identity['owned_worker_creation_time']==launcher['owned_worker_creation_time'] and owned(launcher)
            before=handoff.stack(identity['owned_worker_pid'])
            if 'acquire (serial_main_publication_mutex_v1_20261009.py:' in before and 'guarded (watch_validations_main_safe_v11_20261010.py:24)' in before:
                needle='guarded (watch_validations_main_safe_v11_20261010.py:24)'
        return original(identity,needle)
    finally:mutex.close()

@contextmanager
def installed(log):
    import handoff_joint_goss_round97_full_execution_20261006 as handoff
    original=handoff.suspended_idle;events=[]
    def fixed(identity,needle):
        parent,worker,evidence=hold(identity,needle,original)
        events.append({'worker_pid':worker.pid,'owned_idle_before_and_after':evidence,'at':time.time()})
        return parent,worker,evidence
    handoff.suspended_idle=fixed
    try:yield
    finally:
        handoff.suspended_idle=original
        create(Path(log),{'status':'closed_owned_idle_watcher_boundary_scope','events':events,'scientific_jobs_held':0,'watcher_only_mutex_wait_is_before_mutation':True})
