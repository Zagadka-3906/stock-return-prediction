"""Publish tested shutdown-compatible stop and explicit unsaved-fit recovery limits to main."""
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
    folder = A / 'shutdown_ready_stop_until_manual_continue_20261007'
    activation = read(folder / 'actual_schedule_activation.json')
    assert activation['status'] == 'passed_actual_hidden_shutdown_ready_2355_schedule_and_memory_guardian_supersession'
    assert owned(activation['guardian_launch'])
    assert read(folder / 'guardian_status.json')['status'] == 'scheduled_shutdown_compatible_stop'
    old = read(A / 'user_pause_until_manual_continue_20261007/actual_schedule_activation.json')['guardian_launch']
    assert not owned(old)
    module = A / 'shutdown_ready_stop_20261007.py'
    for directory in ('shutdown_ready_stop_preflight_20261007', 'shutdown_ready_stop_preflight_preheld_20261007'):
        proof = read(A / directory / 'verification.json')
        assert proof['module_sha256'] == sha(module)
        assert proof['only_isolated_probe_terminated'] and proof['scientific_workers_terminated'] == 0
    out = A / 'shutdown_ready_stop_github_20261007'
    assert not out.exists()
    out.mkdir()
    sources = [Path(__file__), module, A / 'activate_shutdown_ready_stop_20261007.py',
               A / 'verify_shutdown_ready_stop_20261007.py', A / 'verify_shutdown_preheld_worker_20261007.py',
               A / 'scheduled_user_pause_20261007.py', A / 'current_user_runtime_control_20261007.json',
               A / 'user_requested_qemu_two_Java_cleanup_20261007.json',
               A / 'user_pause_until_manual_continue_20261007/superseded_by_shutdown_plan_20261007.json',
               *[folder / name for name in ('schedule.json','actual_saved_checkpoint_preparation.json',
                                            'handoff_committed.json','actual_schedule_activation.json')]]
    for directory in ('shutdown_ready_stop_preflight_20261007','shutdown_ready_stop_preflight_preheld_20261007'):
        sources.extend((A / directory).rglob('*.json'))
    services = A / 'service_owned_workflows_20261006'
    for name in ('shutdown_stop_probe_v1','shutdown_stop_guardian_preflight_v1',
                 'shutdown_stop_probe_preheld_v1','shutdown_stop_guardian_preheld_preflight_v1'):
        assert not owned(read(services / name / 'native_launch.json'))
        sources.extend((services / name).glob('*.json'))
        sources.extend((services / name).glob('*.log'))
    sources.append(services / old['name'] / 'administrative_supersession_for_shutdown_20261007.json')
    sources.extend((services / activation['guardian_launch']['name']).glob('*.json'))
    sources = list(dict.fromkeys(p.resolve() for p in sources))
    assert all(p.is_file() for p in sources)
    pins = {str(p): sha(p) for p in sources}
    create(out / 'frozen_before_publication.json', {
        'input_sha256': pins, 'actual2_isolated_deadline_stop_tests_passed': True,
        'actual_memory_pause_guardian_retired': True, 'actual_2355_stop_not_yet_claimed': True,
        'completed_GPU2020_native_artifacts_rehashed': True,
        'current_unsaved_GPU_annual_fit_not_claimed_checkpointed': True,
        'scientific_workers_terminated_before_deadline': 0, 'new_native_fits': 0, 'new_quality_scores': 0})
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
            prefix = Path('validation_sync/shutdown_ready_stop_20261007')
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
                'status': 'published_actual_shutdown_compatible_stop_tests_and_2355_schedule',
                'files': files, 'branch': 'main', 'previous_main': previous,
                'stop_at_local': '2026-10-07T23:55:00+08:00',
                'quiesce_at_local': '2026-10-07T23:45:00+08:00',
                'resume_policy': 'only_after_actual_user_continue_after_power_on',
                'automatic_restart_enabled': False, 'Windows_shutdown_executed': False,
                'user_will_shutdown_after_midnight': True, 'memory_pause_plan_superseded': True,
                'actual_2355_stop_not_yet_claimed': True, 'actual2_isolated_stop_tests_passed': True,
                'complete_GPU2020_artifacts_rehashed': True,
                'unsaved_current_GPU_annual_fit_will_need_restart_if_unfinished_at_stop': True,
                'scientific_workers_terminated_before_deadline': 0,
                'new_native_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})
            scope.reverify()
            for name, data in payload.items():
                sync.atomic(sync.WORKTREE / name, data)
            names = sorted(payload)
            for left in range(0, len(names), 50):
                sync.git('add', '-f', '--', *names[left:left + 50])
            assert set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines()) <= set(payload)
            sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit',
                     '-m', '按午夜关机要求替换内存暂停：2355停止、完整落盘模型校验与手动重启清单', timeout=180)
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
