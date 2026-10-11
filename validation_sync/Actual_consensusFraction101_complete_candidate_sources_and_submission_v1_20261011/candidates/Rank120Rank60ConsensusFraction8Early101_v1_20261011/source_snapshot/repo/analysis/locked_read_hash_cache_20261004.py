"""Scoped Windows read handles for immutable-input SHA reuse; never global."""
from pathlib import Path
import ctypes
from ctypes import wintypes
import hashlib
import msvcrt
import os

REFERENCES=(
    'https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew',
    'https://docs.python.org/3.12/library/msvcrt.html#msvcrt.open_osfhandle',
)

def stream_sha(stream):
    stream.seek(0);h=hashlib.sha256()
    while chunk:=stream.read(8*1024*1024):h.update(chunk)
    return h.hexdigest()

def fresh_sha(path):
    with Path(path).open('rb') as stream:return stream_sha(stream)

def identity(stat):return stat.st_dev,stat.st_ino,stat.st_size

class LockedReadHashCache:
    def __init__(self,expected):
        if os.name!='nt':raise RuntimeError('Windows read sharing semantics required')
        self.expected={str(Path(p).resolve()):d for p,d in expected.items()}
        self.entries={};self.hits=0;self.fresh_calls=0;self.closed=False

    def __enter__(self):
        kernel=ctypes.WinDLL('kernel32',use_last_error=True)
        create=kernel.CreateFileW
        create.argtypes=(wintypes.LPCWSTR,wintypes.DWORD,wintypes.DWORD,ctypes.c_void_p,wintypes.DWORD,wintypes.DWORD,wintypes.HANDLE)
        create.restype=wintypes.HANDLE
        try:
            for path,digest in self.expected.items():
                handle=create(path,0x80000000,1,None,3,0x80,None)
                if handle==ctypes.c_void_p(-1).value:raise ctypes.WinError(ctypes.get_last_error())
                try:fd=msvcrt.open_osfhandle(handle,os.O_RDONLY|os.O_BINARY)
                except BaseException:
                    kernel.CloseHandle.argtypes=(wintypes.HANDLE,);kernel.CloseHandle(handle);raise
                try:stream=os.fdopen(fd,'rb')
                except BaseException:os.close(fd);raise
                self.entries[path]=(stream,identity(os.fstat(stream.fileno())),digest)
                assert identity(os.stat(path))==self.entries[path][1],path
                assert stream_sha(stream)==digest,path
        except BaseException:self.close();raise
        return self

    def sha(self,path):
        if self.closed:raise RuntimeError('Hash scope already closed')
        key=str(Path(path).resolve())
        if key not in self.entries:
            self.fresh_calls+=1;return fresh_sha(path)
        stream,expected_identity,digest=self.entries[key]
        assert identity(os.stat(key))==identity(os.fstat(stream.fileno()))==expected_identity,key
        self.hits+=1;return digest

    def reverify(self):
        for path,(stream,expected_identity,digest) in self.entries.items():
            assert identity(os.stat(path))==identity(os.fstat(stream.fileno()))==expected_identity,path
            assert stream_sha(stream)==digest,path

    def close(self):
        for stream,_,_ in self.entries.values():stream.close()
        self.closed=True

    def __exit__(self,kind,error,tb):
        try:
            if kind is None:self.reverify()
        finally:self.close()
