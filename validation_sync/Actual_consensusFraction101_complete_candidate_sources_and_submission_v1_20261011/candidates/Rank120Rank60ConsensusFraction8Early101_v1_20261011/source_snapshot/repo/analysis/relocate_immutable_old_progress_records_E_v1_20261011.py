"""Preserve historical progress bytes at their exact paths while freeing D via proven file links."""
from pathlib import Path
import sys,re,ctypes,psutil
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def main():
 assert allowed()
 base=Path('E:/赛题五_本机临时/不可变旧进度记录原路径保留_v1_20261011');assert not base.exists();base.mkdir()
 probe=A/'current_ranking_file_link_probe_v1_20261008.bin';assert probe.is_symlink() and probe.read_bytes()==b'actual-byte-exact-file-link-probe'
 pattern=re.compile(r'^(?:optimization_live_progress_v|actual_optimization_fast_runtime_handoff_v)(\d+)_202610(?:10|11)\.json$')
 rows=[]
 for p in A.iterdir():
  match=pattern.fullmatch(p.name)
  if match and int(match.group(1))<=90 and p.is_file() and not p.is_symlink() and p.stat().st_size>=500000:
   assert p.resolve().parent==A.resolve();rows.append({'source':str(p),'target':str(base/p.name),'sha256':sha(p),'bytes':p.stat().st_size})
 assert rows
 # These versions predate the current observer143 and are never its output paths.
 for p in psutil.process_iter(['pid','cmdline']):
  text=' '.join(p.info['cmdline'] or [])
  hit=re.search(r'monitor_verified_current_optimization_v(\d+)_20261011\.py',text)
  assert not hit or int(hit.group(1))>90,(p.pid,text)
 plan=A/'immutable_old_progress_records_E_relocation_plan_v1_20261011.json'
 create(plan,{'status':'frozen_historical_versions1_to90_only_original_records_and_paths_preserved','files':rows,'new_scores':0})
 kernel=ctypes.WinDLL('kernel32',use_last_error=True)
 move=kernel.MoveFileExW;move.argtypes=(ctypes.c_wchar_p,ctypes.c_wchar_p,ctypes.c_uint32);move.restype=ctypes.c_int
 link=kernel.CreateSymbolicLinkW;link.argtypes=(ctypes.c_wchar_p,ctypes.c_wchar_p,ctypes.c_uint32);link.restype=ctypes.c_ubyte
 for row in rows:
  source=Path(row['source']);target=Path(row['target'])
  assert source.resolve().parent==A.resolve() and target.parent.resolve()==base.resolve() and target.drive.upper()=='E:'
  assert not target.exists() and sha(source)==row['sha256']
  assert move(str(source),str(target),2),ctypes.get_last_error()
  try:
   assert sha(target)==row['sha256'];assert link(str(source),str(target),2),ctypes.get_last_error()
   assert source.is_symlink() and source.resolve()==target.resolve() and sha(source)==row['sha256']
  except BaseException:
   if not source.exists():assert move(str(target),str(source),2)
   raise
 create(A/'immutable_old_progress_records_E_relocation_verification_v1_20261011.json',{'status':'passed_all_original_paths_and_sha256_preserved_in_E','files':len(rows),'bytes_moved':sum(r['bytes'] for r in rows),'plan_sha256':sha(plan),'scientific_workers_modified':0,'models_deleted':0})
 print({'preserved_historical_records':len(rows),'bytes_moved':sum(r['bytes'] for r in rows)},flush=True)

if __name__=='__main__':main()
