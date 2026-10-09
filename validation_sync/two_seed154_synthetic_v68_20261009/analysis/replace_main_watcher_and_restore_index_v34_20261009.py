"""Restore the exact user index only after proving it was replaced by the raw150 publisher's tree."""
from pathlib import Path
import sys,os,time,subprocess,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def main():
    from handoff_joint_goss_round97_full_execution_20261006 import stack,suspended_idle,retire_suspended
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    folder=Path('E:/赛题五_本机临时/main_watcher_safe_handoff_v34_20261009');folder.mkdir(exist_ok=False)
    old=read(A/'service_owned_workflows_20261006/main_publisher_v9_20261009/native_launch.json');assert owned(old)
    line=next(line for line in stack(old['owned_worker_pid']).splitlines() if '    main (watch_validations_main_v7_20261006.py:71)' in line)
    parent,worker,idle=suspended_idle(old,line)
    def git(*args,env=None):return subprocess.check_output(['git',*args],cwd=ROOT,env=env,creationflags=subprocess.CREATE_NO_WINDOW)
    index=Path(git('rev-parse','--git-path','index').decode().strip());index=index if index.is_absolute() else ROOT/index
    assert index.resolve().is_relative_to((ROOT/'.git').resolve())
    backup=Path('E:/赛题五_本机临时/two_seed154_recovery_safe_publication_v65_20261009/research_index_before.bin')
    assert sha(backup)=='ed2fa41598113343f7cf84c4ff16f7685c9ed3e079c16edf869c2c32019d3406'
    receipt=read(A/'github_validation_sync_main_20261005/round150_receipt.json');assert receipt['status']=='pushed_and_remote_head_verified'
    tree=git('ls-tree','-r','-z',receipt['commit'])
    expected=b'\0'.join(x.split(b' ',1)[0]+b' '+x.split(b' ',2)[2].split(b'\t',1)[0]+b' 0\t'+x.split(b'\t',1)[1] for x in tree.rstrip(b'\0').split(b'\0'))+b'\0'
    current=git('ls-files','--stage','-z');assert current==expected,'Do not replace a user-modified index'
    before=sha(index);(folder/'raw_publisher_replaced_index.bin').write_bytes(index.read_bytes())
    saved_entries=git('ls-files','--stage','-z',env=dict(os.environ,GIT_INDEX_FILE=str(backup)))
    new_script=A/'watch_validations_main_safe_v10_20261009.py'
    row=start('main_publisher_v10_20261009',new_script.name,[],{str(new_script):sha(new_script)})
    assert owned(row)
    try:
        retire_suspended(old,row)
        temporary=index.with_name('index.codex_restore_v34');assert not temporary.exists();temporary.write_bytes(backup.read_bytes())
        os.replace(temporary,index)
        assert sha(index)==sha(backup) and git('ls-files','--stage','-z')==saved_entries
        create(A/'main_watcher_safe_handoff_and_index_restore_v34_20261009.json',{'status':'passed_exact_preexisting_index_restored_and_owned_idle_watcher_replaced',
            'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'old':old,'new':row,'old_owned_idle_stack':idle,'index_before_restoration_sha256':before,
            'restored_original_index_sha256':sha(index),'raw_index_entries_exact150_remote_tree_proved':True,
            'original_user_index_entries':saved_entries.count(b'\0'),'raw_replaced_entries':current.count(b'\0'),
            'working_directory_files_rewritten':0,'scientific_jobs_retired':0,'original_replaced_index_backup':str(folder/'raw_publisher_replaced_index.bin')})
        print({'main_safe_worker':row['owned_worker_pid'],'restored_index_sha256':sha(index)},flush=True)
    except BaseException:
        if parent.is_running():parent.resume()
        if worker.is_running():worker.resume()
        raise
if __name__=='__main__':main()
