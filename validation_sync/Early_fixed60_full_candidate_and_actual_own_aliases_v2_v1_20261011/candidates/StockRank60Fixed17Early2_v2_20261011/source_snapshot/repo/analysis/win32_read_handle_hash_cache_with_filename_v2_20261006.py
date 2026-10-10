"""Keep all immutable inputs read-only locked without using one CRT fd per file."""
from pathlib import Path
import ctypes
from ctypes import wintypes
import hashlib
import os


class _FileInformation(ctypes.Structure):
    _fields_=[('attributes',wintypes.DWORD),('created',wintypes.FILETIME),
        ('accessed',wintypes.FILETIME),('written',wintypes.FILETIME),
        ('volume',wintypes.DWORD),('size_high',wintypes.DWORD),('size_low',wintypes.DWORD),
        ('links',wintypes.DWORD),('index_high',wintypes.DWORD),('index_low',wintypes.DWORD)]


def _stat_identity(stat):
    return stat.st_dev,stat.st_ino,stat.st_size


class LockedReadHashCache:
    def __init__(self,expected):
        if os.name!='nt':raise RuntimeError('Windows read sharing semantics required')
        self.expected={str(Path(p).resolve()):digest for p,digest in expected.items()}
        self.entries={};self.hits=0;self.fresh_calls=0;self.closed=False
        self.kernel=ctypes.WinDLL('kernel32',use_last_error=True)
        signatures={
            'CreateFileW':((wintypes.LPCWSTR,wintypes.DWORD,wintypes.DWORD,ctypes.c_void_p,wintypes.DWORD,wintypes.DWORD,wintypes.HANDLE),wintypes.HANDLE),
            'CloseHandle':((wintypes.HANDLE,),wintypes.BOOL),
            'ReadFile':((wintypes.HANDLE,ctypes.c_void_p,wintypes.DWORD,ctypes.POINTER(wintypes.DWORD),ctypes.c_void_p),wintypes.BOOL),
            'SetFilePointerEx':((wintypes.HANDLE,ctypes.c_longlong,ctypes.POINTER(ctypes.c_longlong),wintypes.DWORD),wintypes.BOOL),
            'GetFileInformationByHandle':((wintypes.HANDLE,ctypes.POINTER(_FileInformation)),wintypes.BOOL)}
        for name,(args,result) in signatures.items():
            fn=getattr(self.kernel,name);fn.argtypes=args;fn.restype=result
        self.buffer=ctypes.create_string_buffer(8*1024*1024)

    def _handle_identity(self,handle):
        info=_FileInformation()
        if not self.kernel.GetFileInformationByHandle(handle,ctypes.byref(info)):
            raise ctypes.WinError(ctypes.get_last_error())
        return info.volume,(info.index_high<<32)|info.index_low,(info.size_high<<32)|info.size_low

    def _digest(self,handle):
        if not self.kernel.SetFilePointerEx(handle,0,None,0):
            raise ctypes.WinError(ctypes.get_last_error())
        h=hashlib.sha256();count=wintypes.DWORD()
        while True:
            if not self.kernel.ReadFile(handle,self.buffer,len(self.buffer),ctypes.byref(count),None):
                raise ctypes.WinError(ctypes.get_last_error())
            if not count.value:break
            h.update(memoryview(self.buffer).cast('B')[:count.value])
        return h.hexdigest()

    def __enter__(self):
        if self.closed:raise RuntimeError('Hash scope already closed')
        try:
            for path,digest in self.expected.items():
                # GENERIC_READ, FILE_SHARE_READ, OPEN_EXISTING. Concurrent
                # writers and deletion are denied for the entire scope.
                handle=self.kernel.CreateFileW(path,0x80000000,1,None,3,0x80,None)
                if handle==ctypes.c_void_p(-1).value:
                    error=ctypes.WinError(ctypes.get_last_error())
                    error.filename=path
                    raise error
                try:
                    path_id=_stat_identity(os.stat(path));handle_id=self._handle_identity(handle)
                    self.entries[path]=(handle,path_id,handle_id,digest)
                except BaseException:
                    self.kernel.CloseHandle(handle);raise
                assert self._digest(handle)==digest,path
        except BaseException:
            self.close();raise
        return self

    def sha(self,path):
        if self.closed:raise RuntimeError('Hash scope already closed')
        key=str(Path(path).resolve())
        if key not in self.entries:
            self.fresh_calls+=1
            with Path(path).open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()
        handle,path_id,handle_id,digest=self.entries[key]
        assert _stat_identity(os.stat(key))==path_id,key
        assert self._handle_identity(handle)==handle_id,key
        self.hits+=1
        return digest

    def reverify(self):
        if self.closed:raise RuntimeError('Hash scope already closed')
        for path,(handle,path_id,handle_id,digest) in self.entries.items():
            assert _stat_identity(os.stat(path))==path_id,path
            assert self._handle_identity(handle)==handle_id,path
            assert self._digest(handle)==digest,path

    def close(self):
        if self.closed:return
        errors=[]
        for handle,_,_,_ in self.entries.values():
            if not self.kernel.CloseHandle(handle):errors.append(ctypes.get_last_error())
        self.closed=True
        if errors:raise ctypes.WinError(errors[0])

    def __exit__(self,kind,error,tb):
        try:
            if kind is None:self.reverify()
        finally:self.close()
