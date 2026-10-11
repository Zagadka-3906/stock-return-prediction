"""Copy the exact idle publication repository to E, retain the D access path, verify before deleting its D backup."""
from pathlib import Path
import hashlib,json,os,subprocess,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
SOURCE=Path('D:/3.Study/数据分析/赛题五_GitHub验证同步_20261005')
TARGET=Path('E:/赛题五_GitHub验证同步_20261008/验证发布工作副本')
BACKUP=Path('D:/3.Study/数据分析/赛题五_GitHub验证同步_20261005_已核验迁移备份_20261008')
OUT=Path('E:/赛题五_本机临时/Git_publisher_E_relocation_v1_20261008')
def git(path,*args):
    result=subprocess.run(['git','-C',str(path),*args],capture_output=True,text=True,encoding='utf8',errors='replace',creationflags=subprocess.CREATE_NO_WINDOW,timeout=60)
    assert result.returncode==0,(args,result.stderr[:1000]);return result.stdout.strip()
def manifest(path):
    records={};total=0
    for directory,dirs,files in os.walk(path,followlinks=False):
        for name in dirs:
            item=Path(directory)/name;assert not item.is_symlink() and not item.is_junction(),item
        for name in files:
            item=Path(directory)/name;assert not item.is_symlink(),item
            relative=item.relative_to(path).as_posix();size=item.stat().st_size
            records[relative]={'bytes':size,'sha256':sha(item)};total+=size
        if len(records)//5000!=(len(records)-len(files))//5000:
            print(json.dumps({'phase':'actual_complete_repository_hash','path':str(path),'files':len(records),'bytes':total}),flush=True)
    return records,total
def powershell(script,name):
    path=OUT/(name+'.ps1');assert not path.exists();path.write_text(script,encoding='utf-8-sig',newline='\n')
    result=subprocess.run(['pwsh','-NoLogo','-NoProfile','-NonInteractive','-File',str(path)],capture_output=True,text=True,encoding='utf8',errors='replace',creationflags=subprocess.CREATE_NO_WINDOW)
    (OUT/(name+'.stdout')).write_text(result.stdout,encoding='utf8');(OUT/(name+'.stderr')).write_text(result.stderr,encoding='utf8')
    assert result.returncode==0,(name,result.stderr[:2000])
def main():
    import psutil
    assert SOURCE.is_dir() and SOURCE.resolve()==SOURCE and not SOURCE.is_junction()
    assert str(SOURCE.resolve()).lower()==str(Path('D:/3.Study/数据分析/赛题五_GitHub验证同步_20261005')).lower()
    assert TARGET.drive.upper()=='E:' and not TARGET.exists() and not BACKUP.exists()
    assert BACKUP.parent.resolve()==SOURCE.parent.resolve() and BACKUP.name==SOURCE.name+'_已核验迁移备份_20261008'
    assert not OUT.exists();OUT.mkdir(parents=True)
    held=[];original_head=None;switched=False;deleted=False
    from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
    try:
        for name,needle in [('Huber52_controls_main_publication_v14_20261008','    closed (publish_Huber52_evidence_v14_20261008.py:'),('main_publisher_v8_20261008','    main (watch_validations_main_v7_20261006.py:71)')]:
            row=read(A/'service_owned_workflows_20261006'/name/'native_launch.json');assert owned(row)
            parent,worker,idle=suspended_idle(row,needle);held.extend((worker,parent))
            create(OUT/(name+'_actual_idle_hold.json'),{'identity':row,'actual_idle_stack_before_and_after':idle,'scientific_workers_stopped':0})
        original_head=git(SOURCE,'rev-parse','HEAD');assert not git(SOURCE,'status','--porcelain')
        refs=git(SOURCE,'for-each-ref','--format=%(refname) %(objectname)','refs/heads');assert refs=='refs/heads/main '+original_head,refs
        assert git(SOURCE,'config','--get','http.sslBackend')=='openssl' and git(SOURCE,'config','--get','http.version')=='HTTP/2'
        before={d:psutil.disk_usage(d+':/').free for d in ('D','E')}
        print('Only idle publication receivers held; hashing the complete repository before any move.',flush=True)
        records,total=manifest(SOURCE)
        assert len(records)>40000 and total>6*2**30
        assert before['E']>total+3*2**30
        create(OUT/'frozen_before_copy.json',{'status':'frozen_all_repository_file_bytes_at_verified_idle_clean_main',
            'source':str(SOURCE),'target':str(TARGET),'backup':str(BACKUP),'main_commit':original_head,
            'only_main_refs':refs,'files':records,'file_count':len(records),'bytes':total,'free_before':before})
        # All destructive operations stay within these checked, explicitly named paths in native PowerShell.
        powershell("""$ErrorActionPreference='Stop'
$taskSource='D:\3.Study\数据分析\赛题五_GitHub验证同步_20261005'
$taskTarget='E:\赛题五_GitHub验证同步_20261008\验证发布工作副本'
if ((Get-Item -LiteralPath $taskSource).FullName -ne $taskSource) { throw 'Unexpected source path' }
if ((Get-Item -LiteralPath $taskSource).Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Source must be a physical directory' }
if (Test-Path -LiteralPath $taskTarget) { throw 'Target already exists' }
New-Item -ItemType Directory -Path 'E:\赛题五_GitHub验证同步_20261008' -Force | Out-Null
Copy-Item -LiteralPath $taskSource -Destination $taskTarget -Recurse -Force
""",'native_copy_exact_named_repository_to_E')
        copied,copied_total=manifest(TARGET);assert copied==records and copied_total==total
        assert git(TARGET,'rev-parse','HEAD')==original_head and git(TARGET,'for-each-ref','--format=%(refname) %(objectname)','refs/heads')==refs
        assert not git(TARGET,'status','--porcelain')
        create(OUT/'actual_complete_E_copy_byte_verification.json',{'status':'passed_all_files_exact_and_clean_identical_main_before_any_D_deletion',
            'files':len(records),'bytes':total,'all_sha256_equal':True,'main_commit':original_head,'copied_manifest_sha256':hashlib.sha256(json.dumps(copied,sort_keys=True).encode()).hexdigest()})
        powershell("""$ErrorActionPreference='Stop'
$taskSource='D:\3.Study\数据分析\赛题五_GitHub验证同步_20261005'
$taskBackup='D:\3.Study\数据分析\赛题五_GitHub验证同步_20261005_已核验迁移备份_20261008'
$taskTarget='E:\赛题五_GitHub验证同步_20261008\验证发布工作副本'
if ((Get-Item -LiteralPath $taskSource).FullName -ne $taskSource) { throw 'Unexpected source path' }
if (Test-Path -LiteralPath $taskBackup) { throw 'Backup already exists' }
if ((Get-Item -LiteralPath $taskSource).Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Source is not physical' }
if ((Get-Item -LiteralPath $taskTarget).FullName -ne $taskTarget) { throw 'Unexpected target path' }
Rename-Item -LiteralPath $taskSource -NewName '赛题五_GitHub验证同步_20261005_已核验迁移备份_20261008'
New-Item -ItemType Junction -Path $taskSource -Target $taskTarget | Out-Null
""",'native_atomic_path_switch_to_verified_E_copy')
        switched=True
        assert SOURCE.is_junction() and SOURCE.resolve()==TARGET.resolve() and BACKUP.resolve()==BACKUP
        assert git(SOURCE,'rev-parse','HEAD')==original_head and git(SOURCE,'for-each-ref','--format=%(refname) %(objectname)','refs/heads')==refs
        assert not git(SOURCE,'status','--porcelain') and not git(ROOT,'status','--porcelain','--untracked-files=no').startswith('fatal:')
        create(OUT/'actual_D_access_path_to_E_Git_verification.json',{'status':'passed_D_junction_and_original_Git_access_path_clean_main_before_backup_deletion',
            'original_access_path':str(SOURCE),'resolved_E_path':str(SOURCE.resolve()),'main_commit':original_head,'only_main_refs':refs,
            'root_worktree_files_index_and_refs_not_replaced_or_reset':True})
        powershell("""$ErrorActionPreference='Stop'
$taskBackup='D:\3.Study\数据分析\赛题五_GitHub验证同步_20261005_已核验迁移备份_20261008'
$taskSource='D:\3.Study\数据分析\赛题五_GitHub验证同步_20261005'
$taskTarget='E:\赛题五_GitHub验证同步_20261008\验证发布工作副本'
$taskItem=Get-Item -LiteralPath $taskBackup
if ($taskItem.FullName -ne $taskBackup -or $taskItem.Parent.FullName -ne 'D:\3.Study\数据分析') { throw 'Backup path is outside the explicit repository parent' }
if ($taskItem.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Backup must be physical, never recursively delete a junction' }
$taskLink=Get-Item -LiteralPath $taskSource
if (-not ($taskLink.Attributes -band [IO.FileAttributes]::ReparsePoint) -or $taskLink.Target -ne $taskTarget) { throw 'Verified E access path is missing' }
Remove-Item -LiteralPath $taskBackup -Recurse -Force
""",'native_delete_only_byte_verified_D_repository_backup')
        deleted=True;assert not BACKUP.exists() and SOURCE.resolve()==TARGET.resolve()
        after={d:psutil.disk_usage(d+':/').free for d in ('D','E')}
        create(OUT/'verification.json',{'status':'passed_complete_repository_byte_exact_E_relocation_original_D_access_path_and_main_preserved',
            'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'files':len(records),'bytes':total,'original_path':str(SOURCE),'physical_E_path':str(TARGET),
            'main_commit':original_head,'free_before':before,'free_after':after,'actual_D_free_gain_bytes':after['D']-before['D'],
            'all_repository_bytes_verified_before_D_backup_deletion':True,'original_source_and_training_files_not_moved':True,
            'TLS_verification_enabled_and_HTTP2_proxy_config_unchanged':True,'main_only':True,'scientific_workers_stopped':0,'new_quality_scores':0})
        create(A/'Git_publisher_E_relocation_location_v1_20261008.json',{
            'status':'passed_complete_repository_E_relocation','output':str(OUT),'verification_sha256':sha(OUT/'verification.json'),
            'original_access_path':str(SOURCE),'physical_E_path':str(TARGET),'actual_D_free_gain_bytes':after['D']-before['D']})
        print(json.dumps({'status':'passed','files':len(records),'D_free_GiB':after['D']/2**30,'D_freed_GiB':(after['D']-before['D'])/2**30}),flush=True)
    except BaseException as error:
        create(OUT/'failure.json',{'status':'failed_preserved_repository_copy_or_source','error':f'{type(error).__name__}: {error}',
            'switched_to_verified_E':switched,'D_backup_deleted':deleted,'original_source':str(SOURCE),'E_copy':str(TARGET),'D_backup':str(BACKUP)})
        raise
    finally:
        for process in reversed(held):
            if process.is_running():process.resume()
        create(OUT/'actual_publication_receiver_resume.json',{'status':'resumed_all_still_owned_idle_publication_receivers_in_finally',
            'held_processes':len(held),'scientific_workers_stopped':0,'training_processes_moved_or_stopped':0})
if __name__=='__main__':main()
