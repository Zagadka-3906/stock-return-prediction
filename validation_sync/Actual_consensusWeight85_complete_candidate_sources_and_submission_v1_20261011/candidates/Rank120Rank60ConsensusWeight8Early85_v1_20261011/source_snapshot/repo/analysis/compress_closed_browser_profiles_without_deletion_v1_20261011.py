"""Use reversible NTFS compression on closed published browser profiles; preserve every file."""
from pathlib import Path
import subprocess, sys, psutil
A=Path(__file__).resolve().parent; ROOT=A.parent
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def main():
    assert allowed()
    plan=read(A/'closed_main_154180_browser_profile_cleanup_plan_v1_20261011.json')
    out=Path('E:/赛题五_本机临时/closed_browser_profiles_NTFS_compression_v1_20261011');out.mkdir(exist_ok=False)
    commands=[]
    for proc in psutil.process_iter(['cmdline']):
        try: commands.append(' '.join(proc.info['cmdline'] or []))
        except (psutil.AccessDenied,psutil.NoSuchProcess):pass
    before=psutil.disk_usage('D:/').free;records=[]
    for row in plan['rows']:
        assert allowed()
        p=Path(row['path']);resolved=p.resolve(strict=True)
        assert resolved==p and resolved.is_relative_to((ROOT/'tmp').resolve())
        assert p.name.startswith('codex-model-ranking-qa-') and 154<=row['round']<=180
        assert not any(str(p).lower() in c.lower() for c in commands)
        receipt=A/f"github_validation_sync_main_20261005/round{row['round']}_receipt.json"
        execution=A/f"optimization_20261003_r{row['round']}/full_registration_execution.json"
        assert sha(receipt)==row['receipt_sha256'] and sha(execution)==row['full_registration_sha256']
        assert read(receipt)['commit']==row['main_commit'] and read(execution)['status']=='passed'
        files=list(p.rglob('*'));assert not any(q.is_symlink() or q.is_junction() for q in files)
        pins={str(q):sha(q) for q in files if q.is_file()}
        result=subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(p),'*'],cwd=p,
                              capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
        assert result.returncode==0,(str(p),result.stderr.decode(errors='replace'))
        assert {str(q) for q in p.rglob('*') if q.is_file()}==set(pins)
        for q,d in pins.items():assert sha(q)==d,q
        records.append({'path':str(p),'files_rehashed':len(pins),'all_file_bytes_preserved':True})
    after=psutil.disk_usage('D:/').free
    create(out/'verification.json',{'status':'passed_reversible_NTFS_compression_all_closed_profile_bytes_preserved',
           'records':records,'free_bytes_before':before,'free_bytes_after':after,'net_free_bytes_change':after-before,
           'files_deleted':0,'files_moved':0,'scientific_files_modified':False,'test_labels_read':False})
    create(A/'closed_browser_profiles_NTFS_compression_location_v1_20261011.json',{'output':str(out),'verification_sha256':sha(out/'verification.json')})
    print({'closed_profiles':len(records),'net_free_GiB_change':(after-before)/2**30,'files_deleted':0},flush=True)

if __name__=='__main__':main()
