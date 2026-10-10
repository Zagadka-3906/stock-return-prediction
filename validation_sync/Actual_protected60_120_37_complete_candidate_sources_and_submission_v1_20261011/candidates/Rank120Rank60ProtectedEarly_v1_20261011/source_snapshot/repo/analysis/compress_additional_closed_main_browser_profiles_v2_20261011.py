from pathlib import Path
import sys,subprocess,psutil,time
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
 assert allowed();out=Path('E:/赛题五_本机临时/additional_closed_main_browser_profiles_NTFS_compression_v2_20261011');out.mkdir(exist_ok=False);paths=[];commands=[]
 for proc in psutil.process_iter(['cmdline']):
  try:commands.append(' '.join(proc.info['cmdline'] or []).lower())
  except (psutil.NoSuchProcess,psutil.AccessDenied):pass
 for number in [*range(100,154),181,182,183]:
  receipt=A/f'github_validation_sync_main_20261005/round{number}_receipt.json';execution=A/f'optimization_20261003_r{number}/full_registration_execution.json'
  if not receipt.is_file() or not execution.is_file():continue
  r=read(receipt);e=read(execution)
  if r.get('status')!='pushed_and_remote_head_verified' or r.get('branch')!='main' or e.get('status')!='passed':continue
  for p in (ROOT/'tmp').glob(f'ranking_display_qa_*/round{number}/codex-model-ranking-qa-*'):
   resolved=p.resolve(strict=True);assert resolved==p and resolved.is_relative_to((ROOT/'tmp').resolve())
   if any(str(p).lower() in cmd for cmd in commands):continue
   paths.append((number,p,receipt,execution,r['commit']))
 before=psutil.disk_usage('D:/').free;rows=[]
 create(out/'plan.json',{'status':'verified_closed_published_main_profiles_only_reversible_compression','rows':[{'round':n,'path':str(p),'main_commit':commit,'receipt_sha256':sha(r),'full_registration_sha256':sha(e)} for n,p,r,e,commit in paths],'files_deleted':0,'files_moved':0})
 for number,p,receipt,execution,commit in paths:
  assert allowed();files=list(p.rglob('*'));assert not any(q.is_symlink() or q.is_junction() for q in files);pins={str(q):sha(q) for q in files if q.is_file()}
  result=subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(p),'*'],cwd=p,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW);assert result.returncode==0,result.stderr.decode(errors='replace')
  assert {str(q) for q in p.rglob('*') if q.is_file()}==set(pins)
  for q,d in pins.items():assert sha(q)==d,q
  rows.append({'round':number,'path':str(p),'files_rehashed':len(pins),'all_bytes_preserved':True,'main_commit':commit});print({'closed_profile_compressed':len(rows),'expected':len(paths),'round':number},flush=True)
 create(out/'verification.json',{'status':'passed_reversible_NTFS_additional_closed_profiles_all_original_file_bytes_preserved','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'records':rows,'free_bytes_before':before,'free_bytes_after':psutil.disk_usage('D:/').free,'files_deleted':0,'files_moved':0,'scientific_files_modified':False,'test_labels_read':False});create(A/'additional_closed_main_browser_profiles_NTFS_compression_location_v2_20261011.json',{'output':str(out),'verification_sha256':sha(out/'verification.json')})
if __name__=='__main__':main()
