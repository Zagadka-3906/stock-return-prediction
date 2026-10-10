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
    science = [closed('parent_graph_rank_cache_preflight_v3')]
    proof = read(A / 'parent_graph_rank_cache_preflight_v3_20261007/verification.json')
    assert proof['status'] == 'passed_actual_R88_parent5635800_and_empty_cache_cold80_260_975_bits'
    out = A / 'parent_graph_rank_cache_evidence_github_20261007'
    assert not out.exists()
    out.mkdir()
    sources = [Path(__file__), *[A / n for n in (
        'exact_daily_rank_memoization_20261006.py', 'verify_parent_graph_rank_cache_20261007.py',
        'verify_parent_graph_rank_cache_v2_20261007.py', 'verify_parent_graph_rank_cache_v3_20261007.py',
        'monitor_local_only_runtime_v3_20261007.py', 'complete_observer_snapshot_transaction_v2_20261006.py',
        'conditional_residual_mlp44_source_admission_20261007.json',
        'github_validation_sync_main_20261005/round109_receipt.json',
        'cpu_conditional_residual_mlp20_bank_github_20261007/receipt.json')]]
    sources += list((A / 'parent_graph_rank_cache_preflight_v3_20261007').glob('*.json'))
    sources += list((A / 'local_only_monitor_v3_actual_handoff_20261007').glob('*.json'))
    for name in ('parent_graph_rank_cache_preflight', 'parent_graph_rank_cache_preflight_v2', 'parent_graph_rank_cache_preflight_v3'):
        service = A / 'service_owned_workflows_20261006' / name
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
            prefix = Path('validation_sync/parent_graph_rank_cache_evidence_20261007')
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
            manifest = {'status': 'actual_parent_graph_rank_cache_full_and_empty_cache_prefix_evidence',
                'at_local': sync.now(), 'files': files, 'previous_main': previous, 'only_branch': 'main',
                'remote_workers_dispatched': 0, 'actual_parent_round': 88, 'timings': proof['timings'],
                'cache_maximum_retained_bytes': 2**30, 'all_full_and80_260_975_prefix_prediction_bits_exact': True,
                'all_date_masks_dtype_shapes_and_values_hashed': True,
                'single_control_timings_not_formal_multi_repeat_benchmark': True,
                'whole_pipeline_speedup_not_measured': True, 'new_model_selection_scores_by_this_publication': 0,
                'original_first_two_path_failures_preserved_and_not_quality_completions': True,
                'latest_full_qualified_round': 109, 'complete_ranking_records': 11770,
                'actual_new_CPU_MLP_models': 20, 'MLP44_official_comparison_still_pending': True,
                'original_GPU_scientist_not_suspended_stopped_or_restarted': True,
                'exact_idle_main_before_and_after_hold': idle, 'test_labels_read': False}
            payload[(prefix / 'manifest.json').as_posix()] = sync.encoded(manifest)
            payload[(prefix / 'README.md').as_posix()] = (
                '# 本机完整父方案排序缓存核验\n\n'
                '合格第88轮5635800行完整重放、清空缓存后80/260/975日前缀均与原始预测逐位一致。'
                '只缓存原同日排序函数，键包含全部预测值、可用掩码、日期、dtype和shape；返回复制，最大1GiB。\n\n'
                '原始完整重放49.680秒，缓存首次30.465秒，同上下文缓存再次10.063秒。'
                '这些是一次顺序诊断，原始首次含内部缓存预热，不是交替多次正式基准，不声明整体速度倍数。'
                'warm阶段11次排序缓存命中、0新miss；冷前缀前清除缓存，不复用完整未来数组。\n\n'
                '两次输入路径错误在真正模型重放前失败，原记录与代码保留。修正版本的全部控制实际通过。'
                '现有科学训练继续，本核验没有新拟合或官方质量分数。仅main，D/E存储。'
                '第109轮11770条完整榜已通过，新20个CPU条件残差MLP已保存核验，44项评分仍在等待。\n').encode('utf-8')
            scope.reverify()
            for name, data in payload.items():
                sync.atomic(sync.WORKTREE / name, data)
            names = sorted(payload)
            for offset in range(0, len(names), 50):
                sync.git('add', '-f', '--', *names[offset:offset+50])
            assert set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines()) <= set(payload)
            sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m', '保存完整父方案同日排序缓存真实全量与空缓存前缀核验及两次路径失败记录', timeout=180)
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
