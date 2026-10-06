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
    closed('local_only_monitor_v8_actual_handoff')
    closed('CPU_MLP44_round110_full_registration')
    proof = read(A / 'local_only_monitor_v8_actual_handoff_20261007/verification.json')
    assert proof['status'] == 'passed_actual_idle_observer8_complete_single_host_HGB_ElasticNet_and_round113_114_generation'
    out = A / 'local_observer8_actual_single_host_routes_github_20261007'
    assert not out.exists()
    out.mkdir()
    sources = [Path(__file__), *[A / n for n in (
        'monitor_local_only_runtime_v8_20261007.py', 'handoff_local_only_monitor_v8_20261007.py',
        'monitor_local_only_runtime_v7_20261007.py',
        'full_universe_HGB_full113_route_controls_v3_github_20261007/receipt.json',
        'ElasticNet_full114_selected_controls_github_20261007/receipt.json',
        'service_owned_workflows_20261006/local_only_progress_monitor_v7/administrative_supersession_local_v8_20261007.json')]]
    sources += list((A / 'local_only_monitor_v8_actual_handoff_20261007').glob('*.json'))
    folder = A / 'service_owned_workflows_20261006/local_only_monitor_v8_actual_handoff'
    sources += list(folder.glob('*.json')) + list(folder.glob('*.log'))
    folder = A / 'service_owned_workflows_20261006/local_only_progress_monitor_v8'
    sources += [folder / n for n in ('job_definition.json', 'verified_hidden_launch.json', 'native_launch.json')]
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
            prefix = Path('validation_sync/local_observer8_actual_single_host_routes_20261007')
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
            manifest = {'status': 'actual_complete_observer8_single_host_routes_separate_from_scientific_qualification',
                'at_local': sync.now(), 'files': files, 'previous_main': previous, 'only_branch': 'main',
                'observer_verification_status': proof['status'], 'scientific_workers_stopped_or_restarted': 0,
                'new_native_fits_by_this_handoff': 0, 'new_official_scores_by_this_handoff': 0,
                'full113_and114_scientific_qualification_not_claimed': True,
                'remote_workers_dispatched': 0, 'exact_idle_main_before_and_after_hold': idle,
                'test_labels_read': False}
            payload[(prefix / 'manifest.json').as_posix()] = sync.encoded(manifest)
            payload[(prefix / 'README.md').as_posix()] = (
                '# 本机监控八代实际交接\n\n'
                '只在本机运行，远程任务为0。旧监控经过空闲栈、精确身份和无子进程检查后替换，科学训练和评分没有停止或重启。\n\n'
                '增加全股票池HGB及ElasticNet的实际训练计数、评分计数、阶段、依赖服务和第113/114轮的完整资格检查。'
                '未完成的模型、评分或候选推理仍列为待完成；源代码和小样本诊断不作为完整验证成绩。\n\n'
                '第90轮实时记录与完整资格分别展示：须通过138条原验证、完整候选检查、main收据及自然结束状态。'
                '公开材料保存本次首个完整监控快照，持续更新的本地状态不作为固定证据反复哈希。\n').encode('utf-8')
            scope.reverify()
            for name, data in payload.items():
                sync.atomic(sync.WORKTREE / name, data)
            names = sorted(payload)
            for offset in range(0, len(names), 50):
                sync.git('add', '-f', '--', *names[offset:offset+50])
            assert set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines()) <= set(payload)
            sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m', '保存本机监控八代实际交接及HGB和ElasticNet后续验证路径', timeout=180)
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
