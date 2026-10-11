"""Reversibly compress only closed published QA profiles; preserve every original byte."""
from pathlib import Path
import sys,subprocess,psutil,time
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def main():
 assert allowed();out=Path('E:/赛题五_本机临时/new_closed_main_browser_profiles_NTFS_compression_v3_20261011');out.mkdir(exist_ok=False)
 completed=set()
 while allowed():
  commands=[]
  for p in psutil.process_iter(['cmdline']):
   try:commands.append(' '.join(p.info['cmdline'] or []).lower())
   except (psutil.NoSuchProcess,psutil.AccessDenied):pass
  for number in range(184,200):
   receipt=A/f'github_validation_sync_main_20261005/round{number}_receipt.json';terminal=A/f'optimization_20261003_r{number}/full_registration_execution.json'
   if not receipt.exists() or not terminal.exists():continue
   r=read(receipt);t=read(terminal)
   if r.get('status')!='pushed_and_remote_head_verified' or r.get('branch')!='main' or t.get('status')!='passed':continue
   for path in (ROOT/'tmp').glob(f'ranking_display_qa_*/round{number}/codex-model-ranking-qa-*'):
    if str(path) in completed:continue
    resolved=path.resolve(strict=True);assert resolved==path and resolved.is_relative_to((ROOT/'tmp').resolve())
    if any(str(path).lower() in cmd for cmd in commands):continue
    assert allowed();files=list(path.rglob('*'));assert not path.is_symlink() and not path.is_junction() and not any(p.is_symlink() or p.is_junction() for p in files)
    pins={str(p):sha(p) for p in files if p.is_file()};profile=out/f'round{number}_profile{len(completed)}';profile.mkdir(exist_ok=False)
    create(profile/'frozen_before_reversible_compression.json',{'path':str(path),'main_commit':r['commit'],'receipt_sha256':sha(receipt),'full_registration_sha256':sha(terminal),'input_file_sha256':pins,'files_deleted':0,'files_moved':0})
    before=psutil.disk_usage('D:/').free
    result=subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(path),'*'],cwd=path,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
    assert result.returncode==0,result.stderr.decode(errors='replace')
    assert {str(p) for p in path.rglob('*') if p.is_file()}==set(pins)
    for p,d in pins.items():assert sha(p)==d,p
    assert sha(receipt)==read(profile/'frozen_before_reversible_compression.json')['receipt_sha256']
    create(profile/'verification.json',{'status':'passed_reversible_NTFS_closed_published_profile_all_original_bytes_preserved','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'round':number,'path':str(path),'main_commit':r['commit'],'rehashed_files':len(pins),'free_bytes_before':before,'free_bytes_after':psutil.disk_usage('D:/').free,'files_deleted':0,'files_moved':0,'scientific_files_modified':False})
    completed.add(str(path));print({'verified_closed_profile_compressed':str(path),'completed_profiles':len(completed)},flush=True)
  time.sleep(20)
 create(out/'deadline_exit.json',{'status':'stopped_at_actual_user_runtime_control','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'completed_profiles':sorted(completed),'files_deleted':0})
if __name__=='__main__':main()
