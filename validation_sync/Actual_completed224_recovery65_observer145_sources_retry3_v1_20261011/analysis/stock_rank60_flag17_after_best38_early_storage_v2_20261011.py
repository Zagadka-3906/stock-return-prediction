"""Only two explicitly admitted E junction outputs; byte-exact cross-volume copies."""
from pathlib import Path
from contextlib import contextmanager
import os,shutil,hashlib,ctypes
ROOT=Path(__file__).resolve().parents[1]
EBASE=Path('E:/赛题五_本机临时/股票60日涨停股叠加best38最佳17项完整候选_20261011')
OUTPUTS={ROOT/'analysis/StockRank60FlagOnlyAfterBest38Early_selected_release_v2_20261011':EBASE/'selected_release',
 ROOT/'candidates/StockRank60FlagOnlyAfterBest38Early_v2_20261011':EBASE/'candidate'}
def sha(path):
 with Path(path).open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()
def empty(path):
 path=Path(path);assert path in OUTPUTS and path.is_dir()
 assert path.resolve()==OUTPUTS[path].resolve() and path.resolve().is_relative_to(EBASE.resolve())
 flags=ctypes.windll.kernel32.GetFileAttributesW(str(path))
 assert flags!=0xFFFFFFFF and flags&0x400 and not any(path.iterdir())
@contextmanager
def installed_transfer():
 original=os.link
 def transfer(source,destination,*args,**kwargs):
  source,destination=Path(source),Path(destination)
  assert source.is_file() and not destination.exists()
  resolved=destination.parent.resolve()
  assert resolved.is_relative_to(ROOT.resolve()) or resolved.is_relative_to(EBASE.resolve()),destination
  digest=sha(source)
  if source.resolve().drive.upper()==resolved.drive.upper():original(source,destination,*args,**kwargs)
  else:
   assert not args and not kwargs
   with source.open('rb') as reader,destination.open('xb') as writer:shutil.copyfileobj(reader,writer,4*1024**2)
  assert sha(source)==sha(destination)==digest
 os.link=transfer
 try:yield
 finally:
  assert os.link is transfer;os.link=original
