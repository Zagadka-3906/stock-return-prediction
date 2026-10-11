"""Preserve exact current QA bytes and paths; keep subsequent generated pages off D."""
from pathlib import Path
from datetime import datetime
import sys,shutil,ctypes
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
assert allowed()
folder=A/'all_model_ranking_qa';result=read(folder/'interaction_result.json')
assert result['status']=='passed' and result['connected_records']==17753 and result['new_round_records']==27
targetroot=Path('E:/赛题五_本机临时/当前完整榜QA页面原路径保留_v74_20261011');assert not targetroot.exists();targetroot.mkdir()
rows=[]
for name in ('interaction_check.html','rendered_dom.html'):
 source=folder/name;target=targetroot/name;assert source.is_file() and not source.is_symlink() and source.resolve().parent==folder.resolve()
 digest=sha(source);shutil.copyfile(source,target);assert sha(target)==sha(source)==digest
 rows.append({'source':str(source),'target':str(target),'sha256':digest,'bytes':source.stat().st_size})
create(A/'actual_completed191_QA_page_E_relocation74_plan_v1_20261011.json',{'status':'frozen_exact_current27_QA102_pages_before_path_preserving_transfer','at_local':datetime.now().isoformat(),'files':rows,'QA_result_sha256':sha(folder/'interaction_result.json')})
kernel=ctypes.WinDLL('kernel32',use_last_error=True);link=kernel.CreateSymbolicLinkW;link.argtypes=(ctypes.c_wchar_p,ctypes.c_wchar_p,ctypes.c_uint32);link.restype=ctypes.c_ubyte
for row in rows:
 assert allowed();source=Path(row['source']);target=Path(row['target']);backup=source.with_name(source.name+'.actual74_transfer_backup');assert not backup.exists()
 assert sha(source)==sha(target)==row['sha256'];source.rename(backup)
 try:
  assert link(str(source),str(target),2),'CreateSymbolicLinkW: '+str(ctypes.get_last_error())
  assert source.is_symlink() and source.resolve()==target.resolve() and sha(source)==row['sha256']
 except BaseException:
  if source.is_symlink():source.unlink()
  assert not source.exists();backup.rename(source);raise
 assert sha(backup)==sha(source)==sha(target)==row['sha256'];backup.unlink()
create(A/'actual_completed191_QA_page_E_relocation74_verification_v1_20261011.json',{'status':'passed_current_QA_pages_original_paths_and_all_bytes_preserved_E_storage','at_local':datetime.now().isoformat(),'files':rows,'D_bytes_released':sum(r['bytes'] for r in rows),'original_QA_result_unchanged':read(folder/'interaction_result.json')==result,'new_scientific_scores_or_inference':0})
print({'QA_pages_relocated':2,'D_bytes_released':sum(r['bytes'] for r in rows)},flush=True)
