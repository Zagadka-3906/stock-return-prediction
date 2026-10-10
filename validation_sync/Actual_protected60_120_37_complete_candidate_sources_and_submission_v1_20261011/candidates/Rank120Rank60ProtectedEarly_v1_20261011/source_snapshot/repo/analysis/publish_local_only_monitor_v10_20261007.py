"""Publish measured local acceleration and strict unfinished-grid repair evidence on main."""
from pathlib import Path
import gzip
import hashlib
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from hidden_windows_child_creation_20261006 import install
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
import publish_classifier_consensus_workflows_20261006 as helpers


def closed(name):
    p = A / 'service_owned_workflows_20261006' / name
    while not (p / 'native_launch.json').exists() or owned(read(p / 'native_launch.json')):
        time.sleep(15)
    assert read(p / 'service_execution.json')['status'] == 'passed', name
    return p


def main():
    closed('local_only_monitor_v10_actual_handoff')
    closed('local_cpu_validation_recovery_chain_main_publication_v1')
    closed('CPU_full_bank_resource_observer_attach_main_publication_v2')
    proof = read(A / 'local_only_monitor_v10_actual_handoff_20261007/verification.json')
    assert proof['status'] == 'passed_actual_idle_observer10_complete_current_recovery_routes_and_R90_full_qualification_generation'
    out = A / 'local_only_monitor_v10_github_20261007'
    assert not out.exists()
    out.mkdir()
    sources = [Path(__file__), *[Path(p) for p in proof['input_sha256']],
        A / 'local_cpu_validation_recovery_resource_and_main6_hidden_launches_v1_20261007.json']
    sources += list((A / 'local_only_monitor_v10_actual_handoff_20261007').glob('*.json'))
    for name in ('local_only_monitor_v10_actual_handoff',):
        service = A / 'service_owned_workflows_20261006' / name
        sources += list(service.glob('*.json')) + list(service.glob('*.log'))
    service = A / 'service_owned_workflows_20261006/local_only_progress_monitor_v10'
    sources += [service / 'job_definition.json', service / 'native_launch.json', service / 'verified_hidden_launch.json']
    sources += [A / 'service_owned_workflows_20261006/local_only_progress_monitor_v9/administrative_supersession_local_v10_20261007.json']
    pins = {**proof['input_sha256'], **{str(p): sha(p) for p in sources}}
    create(out / 'frozen_before_main_publication.json', {'input_sha256': pins, 'test_labels_read': False})
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    held, retries = [], []
    restore = install()
    sync = helpers.sync
    old_git = sync.git

    def retry_git(*args, **kwargs):
        for attempt in range(3):
            try:
                return old_git(*args, **kwargs)
            except RuntimeError as error:
                if args[0] not in ('ls-remote', 'push', 'fetch') or not any(t in str(error).lower() for t in ('tls', 'ssl', 'connection', 'timed out', 'unable to access')):
                    raise
                retries.append({'command': args[0], 'attempt': attempt + 1, 'error': str(error)[:1000]})
                if attempt == 2:
                    raise
                time.sleep(2)

    sync.git = retry_git
    try:
        row = read(A / 'service_owned_workflows_20261006/main_publisher_v7/native_launch.json')
        parent, worker, idle = suspended_idle(row, '    main (watch_validations_main_v7_20261006.py:71)')
        held.extend((worker, parent))
        with LockedReadHashCache(pins) as scope:
            prefix = Path('validation_sync/local_only_monitor_v10_20261007')
            payload = {(prefix / '.gitattributes').as_posix(): b'* -text\n'}
            files = {}
            for p in dict.fromkeys([*sources, out / 'frozen_before_main_publication.json']):
                data = p.read_bytes()
                assert not sync.SECRET.search(data), p
                raw_sha = hashlib.sha256(data).hexdigest()
                target = (prefix / p.relative_to(ROOT)).as_posix()
                if len(data) >= 5 * 1024**2:
                    data = gzip.compress(data, mtime=0)
                    assert hashlib.sha256(gzip.decompress(data)).hexdigest() == raw_sha
                    target += '.gz'
                payload[target] = data
                files[p.relative_to(ROOT).as_posix()] = {'published_path': target, 'original_sha256': raw_sha, 'published_sha256': hashlib.sha256(data).hexdigest()}
            previous = sync.git('rev-parse', 'HEAD')
            helpers.verify_main(previous)
            assert not sync.git('status', '--porcelain')
            manifest = {'status': 'published_actual_idle_observer10_complete_local_recovery_routes',
                'at_local': sync.now(), 'files': files, 'previous_main': previous, 'only_branch': 'main',
                'actual_generation': proof['generation'], 'new_native_fits': 0, 'new_official_scores': 0,
                'scientific_workers_stopped_suspended_or_restarted': 0,
                'new_model_completion_or_global_resource_exhaustion_not_claimed': True,
                'no_data_prediction_arrays_or_model_weights_uploaded': True,
                'exact_idle_main_before_and_after_hold': idle, 'test_labels_read': False}
            payload[(prefix / 'manifest.json').as_posix()] = sync.encoded(manifest)
            payload[(prefix / 'README.md').as_posix()] = (
                '# 本机进度观察器10\n\n'
                '沿用原观察逻辑，将18个恢复版本的实际服务与输出路径接入三份本机状态文件的原子完整代次。'
                '旧9仅在身份、无子进程、调用栈精确空闲的前后核验后退役。'
                '新10先实际发布完整代次，并核实原R90的138项完整QA4与main仍合格、真实新HGB进程身份一致。'
                '原GPU、队列12和两个新CPU训练进程保持存活，0科学进程暂停、终止或重启。'
                '新进度代次不代表24个模型拟合或全局资源边界已经完成。\n').encode('utf-8')
            scope.reverify()
            for name, data in payload.items():
                sync.atomic(sync.WORKTREE / name, data)
            names = sorted(payload)
            for offset in range(0, len(names), 50):
                sync.git('add', '-f', '--', *names[offset:offset+50])
            assert set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines()) <= set(payload)
            sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m', '同步本机观察器10实际完整状态与精确空闲交接记录', timeout=180)
            commit = sync.git('rev-parse', 'HEAD')
            hashes = {name: hashlib.sha256(data).hexdigest() for name, data in payload.items()}
            assert helpers.blob_hashes(commit, hashes) == hashes
            sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
            helpers.verify_main(commit)
            helpers.watcher.advance_source_index(commit)
            scope.reverify()
            create(out / 'receipt.json', {'status': 'pushed_and_remote_head_verified', 'commit': commit, 'at_local': sync.now(),
                'branch': 'main', 'raw_git_blobs_verified': len(hashes), 'new_quality_scores': 0,
                'all_source_inputs_initial_and_final_read_locked_full_rehash': True,
                'url': 'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/' + prefix.as_posix()})
            print(json.dumps(read(out / 'receipt.json'), ensure_ascii=False), flush=True)
    finally:
        sync.git = old_git
        for p in reversed(held):
            if p.is_running():
                p.resume()
        create(out / 'actual_hidden_publication_children.json', {'events': restore()})
        create(out / 'transport_retries.json', {'attempts': retries, 'TLS_verification_unchanged': True})


if __name__ == '__main__':
    main()
