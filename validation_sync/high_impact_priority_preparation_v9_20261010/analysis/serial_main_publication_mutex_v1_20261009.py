"""Serialize complete publication transactions before suspending the shared watcher."""
from pathlib import Path
from contextlib import contextmanager
import ctypes,time,os
from ctypes import wintypes

class MainPublicationMutex:
    def __init__(self,name='Local\\SaiTi5_verified_main_publication_20261009'):
        self.name=name;self.handle=None;self.acquired=False;self.events=[]
    def acquire(self):
        if self.acquired:return
        k=ctypes.WinDLL('kernel32',use_last_error=True)
        k.CreateMutexW.argtypes=[ctypes.c_void_p,wintypes.BOOL,wintypes.LPCWSTR];k.CreateMutexW.restype=wintypes.HANDLE
        k.WaitForSingleObject.argtypes=[wintypes.HANDLE,wintypes.DWORD];k.WaitForSingleObject.restype=wintypes.DWORD
        self.handle=k.CreateMutexW(None,False,self.name)
        if not self.handle:raise ctypes.WinError(ctypes.get_last_error())
        started=time.monotonic()
        while True:
            result=k.WaitForSingleObject(self.handle,1000)
            if result in (0,0x80):break
            if result!=0x102:raise ctypes.WinError(ctypes.get_last_error())
        self.acquired=True;self.events.append({'pid':os.getpid(),'wait_seconds':time.monotonic()-started,'abandoned_owner_reconciled':result==0x80,'acquired_at':time.time()})
    def close(self):
        if not self.handle:return
        k=ctypes.WinDLL('kernel32',use_last_error=True)
        k.ReleaseMutex.argtypes=[wintypes.HANDLE];k.ReleaseMutex.restype=wintypes.BOOL
        k.CloseHandle.argtypes=[wintypes.HANDLE];k.CloseHandle.restype=wintypes.BOOL
        if self.acquired:
            if not k.ReleaseMutex(self.handle):raise ctypes.WinError(ctypes.get_last_error())
            self.events.append({'pid':os.getpid(),'released_at':time.time()});self.acquired=False
        if not k.CloseHandle(self.handle):raise ctypes.WinError(ctypes.get_last_error())
        self.handle=None

@contextmanager
def installed(logpath):
    import handoff_joint_goss_round97_full_execution_20261006 as handoff
    from run_dependency_queue_v3_20261006 import create
    mutex=MainPublicationMutex();original=handoff.suspended_idle
    def held(*args,**kwargs):
        mutex.acquire()
        return original(*args,**kwargs)
    handoff.suspended_idle=held
    try:yield mutex
    finally:
        handoff.suspended_idle=original;mutex.close()
        create(Path(logpath),{'status':'closed_scoped_serial_main_publication','events':mutex.events,
          'lock_acquired_before_shared_watcher_hold':True,'scientific_jobs_suspended_by_mutex':0,'TLS_verification_disabled':False})
