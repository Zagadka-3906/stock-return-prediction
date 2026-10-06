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
    closed('parent_rank_cache_alternating_benchmark')
    proof = read(A / 'parent_rank_cache_alternating_benchmark_20261007/verification.json')
    assert proof['status'] == 'passed_actual_two_alternating_repeats_full5635800_bits_and_original_restoration'
    out = A / 'parent_rank_cache_alternating_benchmark_github_20261007'
    assert not out.exists()
    out.mkdir()
    sources = [Path(__file__), A / 'benchmark_parent_graph_rank_cache_alternating_20261007.py',
        A / 'exact_daily_rank_memoization_20261006.py',
        A / 'parent_graph_rank_cache_preflight_v3_20261007/verification.json',
        A / 'parent_graph_rank_cache_evidence_github_20261007/receipt.json',
        A / 'local_queue12_and_MLP44_routes_github_20261007/receipt.json']
    sources += list((A / 'parent_rank_cache_alternating_benchmark_20261007').glob('*.json'))
    service = A / 'service_owned_workflows_20261006/parent_rank_cache_alternating_benchmark'
    sources += list(service.glob('*.json')) + list(service.glob('*.log'))
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
            prefix = Path('validation_sync/parent_rank_cache_alternating_benchmark_20261007')
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
            manifest = {'status': 'actual_two_alternating_parent_rank_cache_benchmark_repeats',
                'at_local': sync.now(), 'files': files, 'previous_main': previous, 'only_branch': 'main',
                'remote_workers_dispatched': 0, 'actual_parent_round': 88, 'timings': proof['timings'],
                'medians': proof['median_seconds'],
                'median_warm_rank_phase_speedup': proof['median_warm_rank_phase_speedup'],
                'median_cold_rank_phase_speedup': proof['median_cold_rank_phase_speedup'],
                'inherited_actual_empty_cache_prefixes_not_reexecuted_here': [80, 260, 975],
                'whole_pipeline_speedup_not_measured': True, 'new_model_selection_scores_by_this_publication': 0,
                'original_GPU_scientist_not_suspended_stopped_or_restarted': True,
                'exact_idle_main_before_and_after_hold': idle, 'test_labels_read': False}
            payload[(prefix / 'manifest.json').as_posix()] = sync.encoded(manifest)
            payload[(prefix / 'README.md').as_posix()] = (
                '# 本机完整父方案排序缓存交替重复测速\n\n'
                '第88轮5635800行方案，先核验并预热共同Context内部缓存，再进行两个相反顺序的重复：原函数→排序缓存、排序缓存→原函数。'
                '排序缓存首次成本与命中阶段分别计时；所有6个完整预测控制均与原5635800行预测逐位一致，原函数绑定每轮恢复。\n\n'
                '报告两个重复的中位耗时及阶段倍数，不声明整个搜索或完整流水线速度。'
                '80/260/975日清空排序缓存和根缓存的控制沿用已实际通过的独立证据，本轮没有重复执行此前前缀。\n\n'
                '本轮先等待第90轮官方验证与main、第110轮完整榜闭合，并要求无原队列科学评分写者且RAM至少11GiB。'
                '没有新模型拟合或选模分数，没有停止、暂停、重启科学进程；全部隐藏窗口，本机存储，GitHub仅main。\n').encode('utf-8')
            scope.reverify()
            for name, data in payload.items():
                sync.atomic(sync.WORKTREE / name, data)
            names = sorted(payload)
            for offset in range(0, len(names), 50):
                sync.git('add', '-f', '--', *names[offset:offset+50])
            assert set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines()) <= set(payload)
            sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m', '保存本机完整父方案排序缓存两次交替真实测速与全量逐位核验', timeout=180)
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
