"""Move only immutable Git object bytes to E while owned report bookkeeping is held; retain all working files and refs."""
from pathlib import Path
import hashlib,json,os,subprocess,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
SOURCE=ROOT/'.git/objects';BACKUP=ROOT/'.git/objects_已核验E迁移备份_20261008'
TARGET=Path('E:/赛题五_Git对象库_20261008/root_objects');OUT=Path('E:/赛题五_本机临时/ROOT_Git_objects_E_relocation_v2_20261008')
def git(*args):
    result=subprocess.run(['git','-C',str(ROOT),*args],capture_output=True,text=True,encoding='utf8',errors='replace',creationflags=subprocess.CREATE_NO_WINDOW,timeout=60)
    assert result.returncode==0,(args,result.stderr[:1000]);return result.stdout.strip()
def snapshot(path):
    rows={}
    for directory,dirs,files in os.walk(path,followlinks=False):
        for name in dirs:assert not (Path(directory)/name).is_junction()
        for name in files:
            source=Path(directory)/name;rows[source.relative_to(path).as_posix()]={'bytes':source.stat().st_size,'sha256':sha(source)}
    return rows
def ps(body,name):
    prefix=f"""$ErrorActionPreference='Stop'
$taskSource=[IO.Path]::GetFullPath('{SOURCE.as_posix()}')
$taskBackup=[IO.Path]::GetFullPath('{BACKUP.as_posix()}')
$taskTarget=[IO.Path]::GetFullPath('{TARGET.as_posix()}')
$taskGitParent=[IO.Path]::GetFullPath('{(ROOT/'.git').as_posix()}')
"""
    assert all(ord(c)>=32 or c in '\r\n\t' for c in prefix+body)
    path=OUT/(name+'.ps1');path.write_text(prefix+body,encoding='utf-8-sig',newline='\n')
    result=subprocess.run(['pwsh','-NoProfile','-NonInteractive','-File',str(path)],capture_output=True,text=True,encoding='utf8',errors='replace',creationflags=subprocess.CREATE_NO_WINDOW)
    (OUT/(name+'.stdout')).write_text(result.stdout,encoding='utf8');(OUT/(name+'.stderr')).write_text(result.stderr,encoding='utf8')
    assert result.returncode==0,(name,result.stderr[:1500])
def main():
    gate=A/'service_owned_workflows_20261006/Huber52_round137_full_registration_v14_20261008'
    while not (gate/'native_launch.json').exists() or owned(read(gate/'native_launch.json')):time.sleep(5)
    assert read(gate/'service_execution.json')['status']=='passed'
    assert read(A/'optimization_20261003_r137/full_registration_execution.json')['status']=='passed'
    import psutil
    from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle,stack,pair
    assert ROOT==Path('D:/3.Study/数据分析/赛题五')
    assert SOURCE.resolve()==SOURCE and SOURCE.parent.resolve()==ROOT/'.git' and not SOURCE.is_junction()
    assert BACKUP.parent.resolve()==SOURCE.parent.resolve() and not BACKUP.exists() and not TARGET.exists()
    assert not OUT.exists();OUT.mkdir(parents=True);held=[];switched=False;deleted=False
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v8_20261008/native_launch.json')
        parent,worker,proof=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent));create(OUT/'actual_idle_main_publication_hold.json',proof)
        row=read(A/'service_owned_workflows_20261006/BF16reverse40_controls_main_publication_v14_20261008/native_launch.json');assert owned(row)
        parent,worker,proof=suspended_idle(row,'    closed (publish_BF16reverse40_evidence_v14_20261008.py:')
        held.extend((worker,parent));create(OUT/'actual_idle138_publication_hold.json',{'identity':row,'actual_idle_stack':proof,
            'model_fit_scoring_or_candidate_inference_workers_held':0})
        original_head=git('rev-parse','HEAD');original_refs=git('for-each-ref','--format=%(refname) %(objectname)','refs/heads');index_digest=sha(ROOT/'.git/index')
        original_commit=git('cat-file','-p',original_head)
        disk_before={d:psutil.disk_usage(d+':/').free for d in ('D','E')};rows=snapshot(SOURCE);total=sum(row['bytes'] for row in rows.values())
        assert len(rows)>4000 and total>3*2**30
        create(OUT/'frozen_before_copy.json',{'status':'frozen_complete_Git_object_database_at_held_bookkeeping_boundary','input_files':rows,
            'source':str(SOURCE),'target':str(TARGET),'backup':str(BACKUP),'root_HEAD':original_head,'root_refs':original_refs,'root_index_sha256':index_digest,'bytes':total})
        ps("""if ((Get-Item -LiteralPath $taskSource -Force).FullName -ne $taskSource) { throw 'Wrong source path' }
if ((Get-Item -LiteralPath $taskSource -Force).Parent.FullName -ne $taskGitParent) { throw 'Source is outside the exact workspace Git directory' }
if ((Get-Item -LiteralPath $taskSource -Force).Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Source is already a junction' }
if (Test-Path -LiteralPath $taskTarget) { throw 'Target already exists' }
New-Item -ItemType Directory -Path (Split-Path -Parent $taskTarget) -Force | Out-Null
Copy-Item -LiteralPath $taskSource -Destination $taskTarget -Recurse -Force
""",'copy_exact_object_database')
        assert snapshot(TARGET)==rows
        create(OUT/'actual_complete_copy_verification.json',{'status':'passed_all_object_database_files_byte_exact_before_any_rename_or_delete','files':len(rows),'bytes':total})
        ps("""if ((Get-Item -LiteralPath $taskSource -Force).FullName -ne $taskSource -or (Get-Item -LiteralPath $taskSource -Force).Parent.FullName -ne $taskGitParent) { throw 'Source path changed' }
if (Test-Path -LiteralPath $taskBackup) { throw 'Backup already exists' }
Rename-Item -LiteralPath $taskSource -NewName 'objects_已核验E迁移备份_20261008'
New-Item -ItemType Junction -Path $taskSource -Target $taskTarget | Out-Null
""",'switch_original_Git_object_access_path')
        switched=True
        assert SOURCE.is_junction() and SOURCE.resolve()==TARGET.resolve()
        assert git('rev-parse','HEAD')==original_head and git('for-each-ref','--format=%(refname) %(objectname)','refs/heads')==original_refs
        assert git('cat-file','-p',original_head)==original_commit and sha(ROOT/'.git/index')==index_digest
        create(OUT/'actual_object_access_refs_and_index_verification.json',{'status':'passed_original_commit_object_access_refs_and_index_bytes_after_E_junction_switch',
            'root_HEAD':original_head,'root_refs':original_refs,'root_index_sha256':index_digest,'root_working_files_untouched':True})
        ps("""$taskItem=Get-Item -LiteralPath $taskBackup -Force
if ($taskItem.FullName -ne $taskBackup -or $taskItem.Parent.FullName -ne $taskGitParent) { throw 'Backup outside exact workspace Git directory' }
if ($taskItem.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Never recursively delete an object junction' }
$taskLink=Get-Item -LiteralPath $taskSource -Force
if (-not ($taskLink.Attributes -band [IO.FileAttributes]::ReparsePoint) -or $taskLink.Target -ne $taskTarget) { throw 'Verified E object database link missing' }
Remove-Item -LiteralPath $taskBackup -Recurse -Force
""",'delete_only_verified_original_object_backup')
        deleted=True;assert not BACKUP.exists() and SOURCE.resolve()==TARGET.resolve()
        after={d:psutil.disk_usage(d+':/').free for d in ('D','E')}
        proof={'status':'passed_complete_ROOT_Git_objects_byte_exact_E_relocation_with_original_refs_index_and_working_files_preserved',
            'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'files':len(rows),'bytes':total,'source_access_path':str(SOURCE),'physical_E_path':str(TARGET),
            'root_HEAD':original_head,'root_refs':original_refs,'root_index_sha256':index_digest,'free_before':disk_before,'free_after':after,
            'actual_D_free_gain_bytes':after['D']-disk_before['D'],'model_fitting_scoring_and_candidate_inference_workers_stopped':0,
            'temporarily_held_report_bookkeeping_workers':0,'private_Git_worktree_not_deleted_or_changed':True,'new_scores':0,'test_labels_read':False}
        create(OUT/'verification.json',proof);create(A/'ROOT_Git_objects_E_relocation_location_v2_20261008.json',{'status':proof['status'],'output':str(OUT),'verification_sha256':sha(OUT/'verification.json'),'actual_D_free_gain_bytes':proof['actual_D_free_gain_bytes']})
        print(json.dumps({'status':'passed','files':len(rows),'D_free_GiB':after['D']/2**30,'D_gain_GiB':proof['actual_D_free_gain_bytes']/2**30}),flush=True)
    except BaseException as error:
        create(OUT/'failure.json',{'status':'failed_preserved_original_or_verified_object_database','error':f'{type(error).__name__}: {error}','switched':switched,'deleted_D_backup':deleted});raise
    finally:
        for process in reversed(held):
            if process.is_running():process.resume()
        create(OUT/'actual_bookkeeping_and_publication_resumed.json',{'resumed_in_finally':True,'held_processes':len(held),'model_fit_scoring_or_inference_workers_held':0})
if __name__=='__main__':main()
