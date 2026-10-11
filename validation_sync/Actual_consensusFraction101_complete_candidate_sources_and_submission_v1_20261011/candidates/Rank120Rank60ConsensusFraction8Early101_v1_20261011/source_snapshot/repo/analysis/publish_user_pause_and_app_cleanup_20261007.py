"""Publish the actual pause tests, hidden schedule and latest app cleanup to main."""
from pathlib import Path
import sys
import gzip
import hashlib
import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
from scheduled_user_pause_20261007 import read
from run_dependency_queue_v3_20261006 import sha, create, owned
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
from hidden_windows_child_creation_20261006 import install
import publish_classifier_consensus_workflows_20261006 as helpers


def main():
    folder = A / 'user_pause_until_manual_continue_20261007'
    activation = read(folder / 'actual_schedule_activation.json')
    assert activation['status'] == 'passed_actual_independent_hidden_pause_guardian_running_for_2355_manual_resume_only'
    assert owned(activation['guardian_launch'])
    proof = read(A / 'scheduled_user_pause_integration_preflight_v3_20261007/verification.json')
    assert proof['status'] == 'passed_actual_hidden_timer_deadline_pause_no_auto_resume_and_manual_same_identity_resume'
    assert proof['module_sha256'] == sha(A / 'scheduled_user_pause_20261007.py')
    cleanup = read(A / 'user_requested_qemu_two_Java_cleanup_20261007.json')
    assert not cleanup['remaining_qemu_Java_processes'] and cleanup['training_processes_terminated'] == 0
    out = A / 'user_pause_and_app_cleanup_github_20261007'
    assert not out.exists()
    out.mkdir()
    sources = [Path(__file__), A / 'scheduled_user_pause_20261007.py',
               A / 'activate_user_pause_2355_20261007.py',
               A / 'verify_scheduled_user_pause_integration_20261007.py',
               A / 'verify_scheduled_user_pause_integration_v2_20261007.py',
               A / 'verify_scheduled_user_pause_integration_v3_20261007.py',
               A / 'user_requested_qemu_two_Java_cleanup_20261007.json',
               *A.glob('scheduled_user_pause_*snapshot.py'),
               *A.glob('verify_scheduled_user_pause_*snapshot.py'),
               folder / 'schedule.json', folder / 'actual_schedule_activation.json',
               folder / 'actual_owned_scientific_workers_before_scheduling.json']
    for name in ('scheduled_user_pause_preflight_20261007',
                 'scheduled_user_pause_integration_preflight_20261007',
                 'scheduled_user_pause_integration_preflight_v2_20261007',
                 'scheduled_user_pause_integration_preflight_v3_20261007'):
        sources.extend((A / name).rglob('*.json'))
    services = A / 'service_owned_workflows_20261006'
    for name in ('isolated_preflight_probe', 'isolated_user_pause_timer_preflight',
                 'isolated_preflight_probe_v2', 'isolated_user_pause_timer_preflight_v2',
                 'isolated_preflight_probe_v3', 'isolated_user_pause_timer_preflight_v3'):
        assert not owned(read(services / name / 'native_launch.json'))
        sources.extend((services / name).glob('*.json'))
        sources.extend((services / name).glob('*.log'))
    sources.extend((services / activation['guardian_launch']['name']).glob('*.json'))
    sources = list(dict.fromkeys(p.resolve() for p in sources))
    assert all(p.is_file() for p in sources)
    pins = {str(p): sha(p) for p in sources}
    create(out / 'frozen_before_publication.json', {
        'input_sha256': pins, 'actual_failed_preflight_reader_races_retained': 2,
        'actual_final_integration_preflight_passed': True,
        'actual_2355_deadline_execution_not_yet_claimed': True,
        'actual_latest_user_cleanup_supersedes_previous_keep_apps_running': True,
        'new_native_fits': 0, 'new_quality_scores': 0})
    held = []
    restore = install()
    sync = helpers.sync
    try:
        row = read(services / 'main_publisher_v7/native_launch.json')
        assert psutil.Process(row['owned_worker_pid']).status() == psutil.STATUS_RUNNING
        assert psutil.Process(row['pid']).status() == psutil.STATUS_RUNNING
        parent, worker, idle = suspended_idle(row, '    main (watch_validations_main_v7_20261006.py:71)')
        held.extend((worker, parent))
        from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
        with LockedReadHashCache(pins) as scope:
            prefix = Path('validation_sync/user_pause_and_app_cleanup_20261007')
            payload = {(prefix / '.gitattributes').as_posix(): b'* -text\n'}
            files = {}
            for path in [*sources, out / 'frozen_before_publication.json']:
                data = path.read_bytes()
                assert not sync.SECRET.search(data)
                raw = hashlib.sha256(data).hexdigest()
                target = (prefix / path.relative_to(ROOT)).as_posix()
                if len(data) >= 5 * 1024**2:
                    data = gzip.compress(data, mtime=0)
                    target += '.gz'
                payload[target] = data
                files[str(path.relative_to(ROOT))] = {'published_path': target, 'original_sha256': raw}
            previous = sync.git('rev-parse', 'HEAD')
            helpers.verify_main(previous)
            assert not sync.git('status', '--porcelain')
            payload[(prefix / 'manifest.json').as_posix()] = sync.encoded({
                'status': 'published_actual_pause_tests_hidden_2355_schedule_and_user_requested_app_cleanup',
                'files': files, 'branch': 'main', 'previous_main': previous,
                'pause_at_local': '2026-10-07T23:55:00+08:00',
                'resume_policy': 'only_after_actual_user_continue',
                'automatic_resume_enabled': False,
                'actual_deadline_execution_not_yet_claimed': True,
                'actual_Java_processes_terminated': 2, 'qemu_already_exited_before_action': True,
                'actual_failed_preflight_reader_races_retained': 2,
                'scientific_jobs_terminated': 0, 'new_native_fits': 0,
                'new_quality_scores': 0, 'test_labels_read': False})
            scope.reverify()
            for name, data in payload.items():
                sync.atomic(sync.WORKTREE / name, data)
            names = sorted(payload)
            for left in range(0, len(names), 50):
                sync.git('add', '-f', '--', *names[left:left + 50])
            assert set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines()) <= set(payload)
            sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit',
                     '-m', '保存今晚2355手动续跑暂停安排、实际测试与模拟器Java清理记录', timeout=180)
            commit = sync.git('rev-parse', 'HEAD')
            hashes = {key: hashlib.sha256(value).hexdigest() for key, value in payload.items()}
            assert helpers.blob_hashes(commit, hashes) == hashes
            sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
            helpers.verify_main(commit)
            helpers.watcher.advance_source_index(commit)
            scope.reverify()
            create(out / 'receipt.json', {
                'status': 'pushed_and_remote_head_verified', 'branch': 'main', 'commit': commit,
                'raw_git_blobs_verified': len(hashes), 'scientific_jobs_terminated': 0,
                'new_native_fits': 0, 'new_quality_scores': 0})
    finally:
        for process in reversed(held):
            if process.is_running():
                process.resume()
        create(out / 'actual_hidden_publication_children.json', {'events': restore()})


if __name__ == '__main__':
    main()
