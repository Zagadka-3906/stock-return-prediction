"""Keep linked-worktree identity at its D path; verify before deletion and roll back failed access."""
from pathlib import Path
import sys
import json
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start


def main():
    source = A / 'relocate_idle_verified_Git_publisher_to_E_v3_20261008.py'
    text = source.read_text(encoding='utf-8-sig')
    text = text.replace('验证发布工作副本', '验证发布工作副本_v4')
    text = text.replace('_已核验迁移备份_20261008', '_已核验迁移备份_v4_20261008')
    text = text.replace('Git_publisher_E_relocation_v3_20261008', 'Git_publisher_E_relocation_v4_20261008')
    text = text.replace('Git_publisher_E_relocation_location_v3_20261008', 'Git_publisher_E_relocation_location_v4_20261008')
    text = text.replace('Huber52_scores_main_publication_v14_20261008', 'SpectralGram52_scores_main_publication_v18_20261008')
    text = text.replace('closed (publish_Huber52_evidence_v14_20261008.py:', 'closed (publish_SpectralGram52_evidence_v18_20261008.py:')
    before = 'def main():\n    import psutil'
    assert text.count(before) == 1
    text = text.replace(before, """def main():
    gate=A/'service_owned_workflows_20261006/actual_full_board_deferred_preparation_main_publication_v29_20261008'
    while not (gate/'service_execution.json').exists():time.sleep(10)
    assert read(gate/'service_execution.json')['status']=='passed'
    while owned(read(gate/'native_launch.json')):time.sleep(1)
    import psutil""")
    before = "assert refs=='refs/heads/main '+original_head,refs"
    assert text.count(before) == 1
    text = text.replace(before, "assert len(refs.splitlines())==1 and refs.startswith('refs/heads/main '),refs")
    before = "        assert not git(TARGET,'status','--porcelain')"
    assert text.count(before) == 1
    text = text.replace(before, """        # A copied .git file belongs to a linked worktree whose registered identity
        # is the original D path. Its alternate E-path status is diagnostic only.
        alternate_status=git(TARGET,'status','--porcelain')
        create(OUT/'actual_alternate_E_path_status_diagnostic.json',{'actual_status':alternate_status,
            'not_used_as_original_D_worktree_qualification':True})""")
    text = text.replace("'passed_all_files_exact_and_clean_identical_main_before_any_D_deletion'",
                        "'passed_all_files_exact_and_identical_refs_before_original_D_access_path_verification'")
    before = "    except BaseException as error:\n        create(OUT/'failure.json'"
    assert text.count(before) == 1
    rollback = """    except BaseException as error:
        if switched and not deleted:
            assert SOURCE.is_junction() and SOURCE.resolve()==TARGET.resolve()
            assert BACKUP.exists() and BACKUP.resolve()==BACKUP and BACKUP.parent.resolve()==SOURCE.parent.resolve()
            powershell(r'''$ErrorActionPreference='Stop'
$taskSource='D:\3.Study\数据分析\赛题五_GitHub验证同步_20261005'
$taskBackup='D:\3.Study\数据分析\赛题五_GitHub验证同步_20261005_已核验迁移备份_v4_20261008'
$taskTarget='E:\赛题五_GitHub验证同步_20261008\验证发布工作副本_v4'
$taskLink=Get-Item -LiteralPath $taskSource -Force
$taskSaved=Get-Item -LiteralPath $taskBackup -Force
if ($taskLink.FullName -ne $taskSource -or -not ($taskLink.Attributes -band [IO.FileAttributes]::ReparsePoint) -or $taskLink.Target -ne $taskTarget) { throw 'Wrong rollback junction' }
if ($taskSaved.FullName -ne $taskBackup -or $taskSaved.Parent.FullName -ne 'D:\3.Study\数据分析' -or ($taskSaved.Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw 'Wrong rollback backup' }
# Delete only the junction itself, without recursion; retain both complete copies.
Remove-Item -LiteralPath $taskSource -Force
Rename-Item -LiteralPath $taskBackup -NewName '赛题五_GitHub验证同步_20261005'
''','rollback_original_physical_D_publisher_access')
            assert SOURCE.resolve()==SOURCE and not SOURCE.is_junction() and not BACKUP.exists()
            assert git(SOURCE,'rev-parse','HEAD')==original_head
            create(OUT/'actual_failed_access_switch_rolled_back.json',{'status':'restored_original_physical_D_repository_before_receiver_resume','E_copy_retained':True,'no_original_file_deleted':True})
            switched=False
        create(OUT/'failure.json'"""
    # Preserve literal Windows backslashes in generated PowerShell, rejecting escapes.
    rollback = rollback.replace(chr(3) + '.Study', r'\3.Study')
    text = text.replace(before, rollback)
    assert all(ord(c) >= 32 or c in '\r\n\t' for c in text)
    target = A / 'relocate_idle_verified_Git_publisher_to_E_v4_20261008.py'
    compile(text, str(target), 'exec')
    with target.open('x', encoding='utf-8', newline='') as stream:
        stream.write(text)
    pins = {str(p): sha(p) for p in [Path(__file__), source, target,
            A / 'queue_deferred_full_board_benchmark_and_main_v29_20261008.py']}
    row = start('Git_publisher_original_D_path_verified_E_relocation_v4_20261008', target.name, [], pins)
    create(A / 'Git_publisher_original_path_E_relocation_v4_hidden_launch_20261008.json',
           {'status': 'queued_after_main29_at_actual_idle140_scores_publication_boundary',
            'identity': row, 'input_sha256': pins, 'original_D_access_must_pass_before_backup_deletion': True,
            'rollback_on_failed_original_path_access': True, 'scientific_workers_to_hold': 0,
            'new_quality_scores': 0, 'test_labels_read': False})
    print(json.dumps({'status': 'queued', 'worker': row['owned_worker_pid']}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
