"""Admit only an existing scratch subtree, never any scientific output."""
from pathlib import Path
from contextlib import contextmanager
@contextmanager
def installed(folder):
 folder=Path(folder);base=Path('E:/赛题五_本机临时').resolve()
 assert folder.resolve().is_relative_to(base)
 original=Path.mkdir;events=[]
 def mkdir(path,*args,**kwargs):
  if Path(path).resolve()==folder.resolve() and folder.exists():
   assert not args and kwargs=={'exist_ok':False}
   entries=list(folder.iterdir())
   assert len(entries)==1 and entries[0].name=='tmp' and entries[0].is_dir(), 'Never admit existing scientific files'
   assert not entries[0].is_symlink() and entries[0].resolve().is_relative_to(folder.resolve())
   events.append({'folder':str(folder),'existing_entries':['tmp'],'scientific_files_before_dispatch':0})
   return None
  return original(path,*args,**kwargs)
 Path.mkdir=mkdir
 try:yield events
 finally:
  assert Path.mkdir is mkdir;Path.mkdir=original
