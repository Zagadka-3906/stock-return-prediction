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
    science = [closed(n) for n in ('direct_rank92_round108_full_registration', 'official_date_index_speed_benchmark', 'classifier_consensus_status_gate_recovery_preflight')]
    assert read(A / 'optimization_20261003_r108/full_registration_execution.json')['status'] == 'passed'
    assert read(A / 'github_validation_sync_main_20261005/round108_receipt.json')['actual_full_QA_version'] == 19
    benchmark = read(A / 'official_date_index_speed_benchmark_20261007/verification.json')
    gate = read(A / 'classifier_consensus_status_gate_recovery_preflight_20261007/verification.json')
    assert benchmark['status'] == 'passed_actual_full_official_date_index_equivalence_and_benchmark'
    assert gate['status'] == 'passed_actual_precise_completed_route_gate_and_negative_controls_original_sources_preserved'
    out = A / 'local_speed_adoption_github_20261007'
    assert not out.exists()
    out.mkdir()
    sources = [Path(__file__), *[A / n for n in (
        'official_date_index_dataframe_adapter_20261007.py', 'benchmark_official_date_index_speed_20261007.py',
        'classifier_consensus_status_gate_recovery_runtime_20261007.py', 'verify_classifier_consensus_status_gate_recovery_20261007.py',
        'prepare_direct_rank_micro74_20261007.py', 'single_host_direct_flag_rank_micro74_plan_20261007.json',
        'run_direct_flag_rank_micro74_official_comparison_20261007.py', 'publish_single_host_rank_micro74_evidence_20261007.py',
        'single_host_rank_micro74_source_admission_20261007.json')]]
    for folder in (A / 'official_date_index_speed_benchmark_20261007', A / 'classifier_consensus_status_gate_recovery_preflight_20261007'):
        sources += list(folder.glob('*.json'))
    for service in science[1:]:
        sources += list(service.glob('*.json')) + list(service.glob('*.log'))
    pins = {**benchmark['input_sha256'], **gate['input_sha256'], **{str(p): sha(p) for p in sources}}
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
            prefix = Path('validation_sync/local_speed_adoption_20261007')
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
            manifest = {'status': 'actual_measured_local_speed_and_strict_repair_evidence', 'at_local': sync.now(),
                'files': files, 'previous_main': previous, 'only_branch': 'main', 'remote_workers_dispatched': 0,
                'CPU_training_diagnostic_speedup': read(A / 'local_flag_tree_thread_benchmark_20261007/verification.json')['measured_speedup_over_2_threads'],
                'official_evaluator_full_phase_median_speedup': benchmark['median_full_official_evaluation_speedup'],
                'all8_metrics_bit_identical_in_full_and_tied_and80day_actual_comparisons': True,
                'whole_pipeline_speedup_not_measured': True, 'new_model_selection_scores_by_this_publication': 0,
                'R89_actual_gate_checks_passed_but_scientific_retry_qualification_not_completed': True,
                'all_original_failed_scopes_and_scientific_sources_preserved': True,
                'next74_grid_predeclared_and_waits_full108_closed_before_execution': True,
                'original_GPU_scientist_not_suspended_stopped_or_restarted': True,
                'exact_idle_main_before_and_after_hold': idle, 'test_labels_read': False}
            payload[(prefix / 'manifest.json').as_posix()] = sync.encoded(manifest)
            payload[(prefix / 'README.md').as_posix()] = ('# 本机实测提速\n\n'
                '用户取消双机协作。小树训练8线程相对2线程约2.41倍；完整官方评分阶段实测中位约1.25倍。两者均是对应阶段的测量，不能相乘当作整体速度。\n\n'
                '官方evaluate.py保持原字节。日期索引适配沿用所有原始过滤、排序、并列及跨年换手逻辑；实际完整5635800行预测、同分预测及80日前缀的全部8项指标逐位一致。短前缀评分未获得加速。\n\n'
                '下一组74项固定小幅CDF融合已提前声明，复用36个已完成模型；等待完整第108轮关闭后执行。\n\n'
                '旧R89门控错误已有精确修复和5项负向检查，原124/138项科学网格保留，但重试、候选和最终资格尚未完成。本提交不把修复预检冒充完成验证。原超宽GPU训练继续运行。\n').encode('utf-8')
            scope.reverify()
            for name, data in payload.items():
                sync.atomic(sync.WORKTREE / name, data)
            names = sorted(payload)
            for offset in range(0, len(names), 50):
                sync.git('add', '-f', '--', *names[offset:offset+50])
            assert set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines()) <= set(payload)
            sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m', '保存本机评分实测提速、74项冻结搜索与旧分类集成严格门控修复证据', timeout=180)
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
