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
    closed('exact_numpy_daily_ranks_operator_benchmark')
    closed('CPU_MLP44_round110_full_registration')
    proof = read(A / 'exact_numpy_daily_ranks_benchmark_20261007/verification.json')
    assert proof['status'] == 'passed_actual_three_full5635800_heads_two_opposite_orders_daily_rank_and_cold_prefix_controls'
    out = A / 'exact_numpy_daily_rank_controls_github_20261007'
    assert not out.exists()
    out.mkdir()
    sources = [Path(__file__), *[Path(p) for p in proof['input_sha256'] if Path(p).suffix.lower() in ('.py','.json','.md','.txt')]]
    sources += list((A / 'exact_numpy_daily_ranks_benchmark_20261007').glob('*.json'))
    service=A/'service_owned_workflows_20261006/exact_numpy_daily_ranks_operator_benchmark'
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
            prefix = Path('validation_sync/exact_numpy_daily_rank_controls_20261007')
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
            manifest = {'status': 'published_actual_full_OOF_numpy_daily_rank_operator_controls',
                'at_local': sync.now(), 'files': files, 'previous_main': previous, 'only_branch': 'main',
                'verification_status':proof['status'],'median_operator_phase_speedup':proof['median_operator_phase_speedup'],
                'actual_heads':3,'full_rows_per_head':5635800,'opposite_orders_actual_timed_calls':12,'whole_day_prefix_controls':9,
                'new_native_fits':0,'new_official_scores':0,'scientific_workers_stopped_or_restarted':0,
                'full_graph_official_metrics_future_candidate_and_whole_goal_speedup_not_claimed':True,
                'operator_not_adopted_in_frozen_or_live_scientific_workflows':True,
                'no_data_prediction_arrays_or_model_weights_uploaded':True,
                'exact_idle_main_before_and_after_hold':idle,'test_labels_read':False}
            payload[(prefix / 'manifest.json').as_posix()] = sync.encoded(manifest)
            payload[(prefix / 'README.md').as_posix()] = (
                '# NumPy按日平均排名实际完整样本检查与测速\n\n'
                '三个真实OOF预测向量分别覆盖5635800行、1212个交易日。两种顺序实测共12次排名计算，'
                '结果全部与原Pandas函数的float64位值完全相同；每个向量另验80、260、975天冷前缀。\n\n'
                f"原实现各次中位数{proof['median_seconds']['original']:.6f}秒，NumPy实现{proof['median_seconds']['numpy']:.6f}秒，"
                f"该操作阶段约快{proof['median_operator_phase_speedup']:.6f}倍。\n\n"
                '并列平均排名、无效价格、NaN、无穷、负九阈值、空输入、乱序日期回退和大整数回退均实测。'
                '使用NumPy稳定排序，参考 https://numpy.org/doc/stable/reference/generated/numpy.argsort.html 。\n\n'
                '本记录只证明排名操作和这些前缀的等价及阶段测速；未证明完整模型图、官方评分、1599600行候选推理或全任务提速。'
                '当前运行与已封存的科学方案没有修改；不上传数据、预测数组或模型权重。\n').encode('utf-8')
            scope.reverify()
            for name, data in payload.items():
                sync.atomic(sync.WORKTREE / name, data)
            names = sorted(payload)
            for offset in range(0, len(names), 50):
                sync.git('add', '-f', '--', *names[offset:offset+50])
            assert set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines()) <= set(payload)
            sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m', '保存NumPy每日排名完整5635800样本位值等价和实测5倍操作提速证据', timeout=180)
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
