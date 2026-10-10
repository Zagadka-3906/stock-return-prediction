"""Retain all original bytes on E; reconcile only nine exact CRLF/LF legacy worktree copies."""
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle

SOURCE = Path('D:/3.Study/数据分析/赛题五_GitHub验证同步_20261005')
TARGET = Path('E:/赛题五_GitHub验证同步_20261008/验证发布工作副本_v4')
BACKUP = SOURCE.with_name(SOURCE.name + '_已核验迁移备份_v9_20261008')
OUT = Path('E:/赛题五_本机临时/Git_publisher_E_relocation_v9_20261008')


def git_bytes(path, *args):
    result = subprocess.run(['git', '-C', str(path), *args], capture_output=True,
                            creationflags=subprocess.CREATE_NO_WINDOW, timeout=120)
    assert result.returncode == 0, (args, result.stderr.decode('utf-8', errors='replace')[:1500])
    return result.stdout


def git(path, *args):
    return git_bytes(path, *args).decode('utf-8').rstrip('\r\n')


def manifest(path):
    rows = {}
    for directory, dirs, files in os.walk(path, followlinks=False):
        for name in dirs:
            assert not (Path(directory) / name).is_junction()
        for name in files:
            file = Path(directory) / name
            assert not file.is_symlink()
            rows[file.relative_to(path).as_posix()] = {'bytes': file.stat().st_size, 'sha256': sha(file)}
    return rows


def ps(body, name):
    prefix = f"""$ErrorActionPreference='Stop'
$taskSource=[IO.Path]::GetFullPath('{SOURCE.as_posix()}')
$taskBackup=[IO.Path]::GetFullPath('{BACKUP.as_posix()}')
$taskTarget=[IO.Path]::GetFullPath('{TARGET.as_posix()}')
$taskParent=[IO.Path]::GetFullPath('{SOURCE.parent.as_posix()}')
"""
    assert all(ord(c) >= 32 or c in '\r\n\t' for c in prefix + body)
    file = OUT / (name + '.ps1')
    file.write_text(prefix + body, encoding='utf-8-sig', newline='\n')
    result = subprocess.run(['pwsh', '-NoProfile', '-NonInteractive', '-File', str(file)],
                            capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
    (OUT / (name + '.stdout')).write_bytes(result.stdout)
    (OUT / (name + '.stderr')).write_bytes(result.stderr)
    assert result.returncode == 0, result.stderr.decode('utf-8', errors='replace')[:1500]


def semantic(data, name):
    text = data.decode('utf-8-sig')
    return [json.loads(line) for line in text.splitlines() if line.strip()] if name.endswith('.jsonl') else json.loads(text)


def main():
    import psutil
    failure = A / 'service_owned_workflows_20261006/Git_publisher_private_stat_refresh_verified_E_relocation_v8_20261008/service_execution.json'
    assert read(failure)['status'] == 'failed'
    previous = Path('E:/赛题五_本机临时/Git_publisher_E_relocation_v4_20261008')
    assert read(previous / 'actual_failed_access_switch_rolled_back.json')['status'] == 'restored_original_physical_D_repository_before_receiver_resume'
    assert SOURCE.resolve() == SOURCE and not SOURCE.is_junction() and TARGET.is_dir()
    assert not BACKUP.exists() and not OUT.exists()
    OUT.mkdir()
    gate=A/'service_owned_workflows_20261006/KrylovGram52_controls_main_publication_v18_20261008'
    while not (gate/'service_execution.json').exists():time.sleep(10)
    while owned(read(gate/'native_launch.json')):time.sleep(1)
    assert read(gate/'service_execution.json')['status']=='passed'
    held, switched, deleted = [], False, False
    private_index=private_original=root_index_sha=None
    try:
        for name, needle in [('KrylovGram52_scores_main_publication_v18_20261008', '    closed (publish_KrylovGram52_evidence_v19_20261008.py:'),
                             ('main_publisher_v9_20261008', '    main (watch_validations_main_v7_20261006.py:71)')]:
            row = read(A / 'service_owned_workflows_20261006' / name / 'native_launch.json')
            assert owned(row)
            parent, worker, proof = suspended_idle(row, needle)
            held.extend((worker, parent))
            create(OUT / (name + '_actual_idle_hold.json'), {'identity': row, 'stack': proof, 'scientific_workers_held': 0})
        head = git(SOURCE, 'rev-parse', 'HEAD')
        refs = git(SOURCE, 'for-each-ref', '--format=%(refname) %(objectname)', 'refs/heads')
        assert refs.startswith('refs/heads/main ') and len(refs.splitlines()) == 1
        assert not git(SOURCE, 'status', '--porcelain')
        private_path=Path(git(SOURCE,'rev-parse','--git-path','index'))
        private_index=(private_path if private_path.is_absolute() else SOURCE/private_path).resolve()
        assert private_index.is_relative_to((ROOT/'.git/worktrees').resolve()) and private_index!=(ROOT/'.git/index').resolve()
        private_original=private_index.read_bytes();(OUT/'original_private_publisher_index.bin').write_bytes(private_original)
        root_index_sha=sha(ROOT/'.git/index')
        assert git(TARGET, 'rev-parse', 'HEAD') == head
        before = {d: psutil.disk_usage(d + ':/').free for d in ('D', 'E')}
        original = manifest(SOURCE)
        assert len(original) > 40000 and sum(r['bytes'] for r in original.values()) > 6 * 2**30
        names = [
            'validation_sync/authorized_cleanup_20261005/deletions.jsonl',
            'validation_sync/authorized_cleanup_20261005/plan.json',
            'validation_sync/authorized_cleanup_20261005/verification.json',
            'validation_sync/compute_storage_controls_20261005/capability.json',
            'validation_sync/compute_storage_controls_20261005/frozen_before_actual_control.json',
            'validation_sync/compute_storage_controls_20261005/placement_frozen_before_creation.json',
            'validation_sync/compute_storage_controls_20261005/placement_verification.json',
            'validation_sync/compute_storage_controls_20261005/placement_withdrawal_20261005.json',
            'validation_sync/compute_storage_controls_20261005/verification.json']
        stale = manifest(TARGET)
        assert set(stale)<=set(original), 'Unexpected E files require investigation, not deletion.'
        refreshed=[]
        for name,record in original.items():
            if name in names:continue
            if stale.get(name)!=record:
                target=TARGET/name;target.parent.mkdir(parents=True,exist_ok=True)
                shutil.copy2(SOURCE/name,target)
                assert sha(target)==record['sha256'] and target.stat().st_size==record['bytes'],name
                refreshed.append(name)
        create(OUT/'actual_current_main_E_copy_refresh.json',{'current_main_HEAD':head,'refreshed_files':refreshed,'new_commits_created':0})
        corrections = {}
        for name in names:
            raw = (SOURCE / name).read_bytes()
            canonical = git_bytes(SOURCE, 'cat-file', 'blob', head + ':' + name)
            assert raw != canonical and raw.replace(b'\r\n', b'\n') == canonical, name
            assert semantic(raw, name) == semantic(canonical, name), name
            preserved = OUT / 'original_raw_legacy_records' / name
            preserved.parent.mkdir(parents=True, exist_ok=True)
            prior_raw=Path('E:/赛题五_本机临时/Git_publisher_E_relocation_v6_20261008/original_raw_legacy_records')/name
            assert prior_raw.read_bytes()==raw,name
            preserved.write_bytes(raw)
            assert sha(preserved) == original[name]['sha256']
            (TARGET / name).write_bytes(canonical)
            assert sha(TARGET / name) == hashlib.sha256(canonical).hexdigest()
            corrections[name] = {'original_raw_sha256': sha(preserved),
                                 'canonical_committed_SHA256': sha(TARGET / name),
                                 'original_raw_preserved_on_E': str(preserved),
                                 'exact_difference_is_CRLF_to_LF_only': True,
                                 'all_JSON_or_JSONL_values_equal': True}
        actual = manifest(TARGET)
        assert set(actual) == set(original)
        for name, record in original.items():
            if name in corrections:
                assert actual[name]['sha256'] == corrections[name]['canonical_committed_SHA256']
            else:
                assert actual[name] == record, name
        for name in names:assert not git(TARGET,'diff','--raw','--',name),name
        before_objects=git_bytes(TARGET,'ls-files','--stage','-z')
        for name in names:
            actual_blob=git(TARGET,'hash-object','--path='+name,name)
            expected_blob=git(TARGET,'rev-parse',head+':'+name)
            assert actual_blob==expected_blob,name
        # Git refresh may reject a size mismatch without content hashing; add refreshes exactly these same objects and stat entries.
        git(TARGET,'add','-f','--',*names)

        after_objects=git_bytes(TARGET,'ls-files','--stage','-z')
        assert before_objects==after_objects, 'Only stat-cache metadata may change, never staged content.'
        assert sha(ROOT/'.git/index')==root_index_sha, 'Primary workspace dirty index must stay unchanged.'
        create(OUT/'actual_private_index_stat_refresh.json',{'private_index':str(private_index),
            'original_index_sha256':hashlib.sha256(private_original).hexdigest(),'refreshed_index_sha256':sha(private_index),
            'all_staged_modes_objects_and_paths_identical':True,'primary_workspace_index_unchanged':True,
            'primary_index_sha256':root_index_sha,'new_commits_created':0})
        status=git(TARGET,'status','--porcelain')
        create(OUT/'actual_refreshed_E_status_before_access_switch.json',{'status_porcelain':status,'HEAD':head})
        assert not status, 'Every refreshed E worktree file must now match its committed tree.'
        create(OUT / 'frozen_before_original_D_access_switch.json', {'input_files': original,
            'original_raw_bytes': sum(r['bytes'] for r in original.values()), 'main_HEAD': head, 'only_main_refs': refs,
            'nine_exact_line_ending_corrections': corrections, 'all_other_original_bytes_exact_on_E': True,
            'all_original_raw_bytes_present_on_E_before_any_D_deletion': True})
        ps("""$taskItem=Get-Item -LiteralPath $taskSource -Force
if ($taskItem.FullName -ne $taskSource -or $taskItem.Parent.FullName -ne $taskParent -or ($taskItem.Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw 'Wrong physical publisher source' }
if (Test-Path -LiteralPath $taskBackup) { throw 'Backup already exists' }
if ((Get-Item -LiteralPath $taskTarget).FullName -ne $taskTarget) { throw 'Wrong E target' }
Rename-Item -LiteralPath $taskSource -NewName '赛题五_GitHub验证同步_20261005_已核验迁移备份_v9_20261008'
New-Item -ItemType Junction -Path $taskSource -Target $taskTarget | Out-Null
""", 'switch_original_registered_D_publisher_path')
        switched = True
        assert SOURCE.is_junction() and SOURCE.resolve() == TARGET.resolve()
        assert git(SOURCE, 'rev-parse', 'HEAD') == head
        assert git(SOURCE, 'for-each-ref', '--format=%(refname) %(objectname)', 'refs/heads') == refs
        assert not git(SOURCE, 'status', '--porcelain')
        assert manifest(BACKUP) == original
        create(OUT / 'verified_original_D_access_and_all_E_raw_records_before_deletion.json',
               {'status': 'passed_original_D_access_clean_identical_HEAD_and_refs_with_all_original_raw_records_preserved_on_E',
                'main_HEAD': head, 'only_main_refs': refs, 'all_original_raw_files_verified': len(original)})
        ps("""$taskItem=Get-Item -LiteralPath $taskBackup -Force
if ($taskItem.FullName -ne $taskBackup -or $taskItem.Parent.FullName -ne $taskParent -or ($taskItem.Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw 'Backup outside exact publisher directory' }
$taskLink=Get-Item -LiteralPath $taskSource -Force
if (-not ($taskLink.Attributes -band [IO.FileAttributes]::ReparsePoint) -or $taskLink.Target -ne $taskTarget) { throw 'Verified E publisher link missing' }
Remove-Item -LiteralPath $taskBackup -Recurse -Force
""", 'delete_only_fully_verified_duplicate_D_publisher_backup')
        deleted = True
        assert not BACKUP.exists()
        after = {d: psutil.disk_usage(d + ':/').free for d in ('D', 'E')}
        proof = {'status': 'passed_E_publisher_relocation_original_D_identity_all_raw_records_main_and_scores_preserved',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'original_access_path': str(SOURCE), 'physical_E_path': str(TARGET),
            'original_raw_legacy_records': corrections, 'files': len(original), 'main_HEAD': head, 'only_main_refs': refs,
            'free_before': before, 'free_after': after, 'D_freed_bytes': after['D'] - before['D'],
            'original_ROOT_working_files_not_moved': True, 'all_original_raw_records_retained_on_E': True,
            'new_commits_created': 0, 'new_scores': 0, 'scientific_workers_held': 0, 'test_labels_read': False}
        create(OUT / 'verification.json', proof)
        create(A / 'Git_publisher_E_relocation_location_v9_20261008.json',
               {'status': proof['status'], 'output': str(OUT), 'verification_sha256': sha(OUT / 'verification.json'),
                'original_access_path': str(SOURCE), 'physical_E_path': str(TARGET), 'D_freed_bytes': proof['D_freed_bytes']})
        print(json.dumps({'status': 'passed', 'D_free_GiB': after['D'] / 2**30,
                          'D_freed_GiB': proof['D_freed_bytes'] / 2**30}), flush=True)
    except BaseException as error:
        if switched and not deleted:
            assert SOURCE.is_junction() and SOURCE.resolve() == TARGET.resolve()
            assert BACKUP.resolve() == BACKUP and BACKUP.parent.resolve() == SOURCE.parent.resolve()
            ps("""$taskLink=Get-Item -LiteralPath $taskSource -Force
$taskItem=Get-Item -LiteralPath $taskBackup -Force
if ($taskLink.FullName -ne $taskSource -or -not ($taskLink.Attributes -band [IO.FileAttributes]::ReparsePoint) -or $taskLink.Target -ne $taskTarget) { throw 'Wrong rollback junction' }
if ($taskItem.FullName -ne $taskBackup -or $taskItem.Parent.FullName -ne $taskParent -or ($taskItem.Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw 'Wrong rollback backup' }
Remove-Item -LiteralPath $taskSource -Force
Rename-Item -LiteralPath $taskBackup -NewName '赛题五_GitHub验证同步_20261005'
""", 'rollback_original_physical_D_access')
            assert SOURCE.resolve() == SOURCE and not SOURCE.is_junction()
        if not deleted and private_index is not None and private_original is not None:
            assert not SOURCE.is_junction() and private_index.is_relative_to((ROOT/'.git/worktrees').resolve())
            private_index.write_bytes(private_original)
            assert sha(private_index)==hashlib.sha256(private_original).hexdigest()
            assert sha(ROOT/'.git/index')==root_index_sha
            create(OUT/'restored_original_private_index_stat_cache.json',{'original_private_index_restored':True,'primary_workspace_index_unchanged':True})
        create(OUT / 'failure.json', {'status': 'failed_preserved_original_D_or_verified_E_publisher',
            'error': f'{type(error).__name__}: {error}', 'original_D_backup_deleted': deleted})
        raise
    finally:
        for process in reversed(held):
            if process.is_running():
                process.resume()
        create(OUT / 'actual_idle_publishers_resumed.json', {'resumed_in_finally': True,
               'held_processes': len(held), 'scientific_workers_held': 0})


if __name__ == '__main__':
    main()
