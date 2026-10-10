"""Publish actual parent-metadata repair, immutable failure archives and fresh local compute routes."""
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
    closed('CPU_HGB44_round112_full_registration_v2')
    assert read(A / 'github_validation_sync_main_20261005/round112_receipt.json')['actual_full_QA_version'] == 23
    proof = read(A / 'local_cpu_validation_recovery_chain_v1_20261007.json')
    assert proof['status'] == 'passed_actual_prefit_failed_dependency_history_and18_fresh_source_AST_and_corrected_parent_metadata_routes'
    out = A / 'local_cpu_validation_recovery_chain_v1_github_20261007'
    assert not out.exists()
    out.mkdir()
    sources = [Path(__file__), A / 'local_cpu_validation_recovery_chain_v1_20261007.json',
        A / 'local_cpu_validation_recovery_future_registry_preflight_v1_20261007.json',
        A / 'local_cpu_recovery_actual_publication_receipt_routes_v1_20261007.json',
        A / 'local_cpu_validation_recovery_actual16_hidden_launches_v1_20261007.json',
        A / 'CPU_HGB44_round112_registration_baseline_v2_preflight_20261007.json',
        A / 'memory_bounded_numeric_preparation_20261007.py',
        A / 'memory_bounded_numeric_preparation_preflight_20261007/verification.json',
        A / 'github_validation_sync_main_20261005/round112_receipt.json',
        A / 'publish_cpu_full_universe_HGB24_evidence_v3_20261007.py',
        A / 'publish_cpu_full_universe_ElasticNet24_evidence_v4_20261007.py']
    sources += [Path(p) for p in [*proof['original_sources_sha256'], *proof['new_sources_sha256']]]
    for paths in ('original_sources_sha256', 'new_sources_sha256'):
        for p, digest in proof[paths].items():
            assert sha(Path(p)) == digest, p
    for name in proof['actual_original_failed_terminals']:
        service = A / 'service_owned_workflows_20261006' / name
        assert not owned(read(service / 'native_launch.json'))
        assert read(service / 'service_execution.json') == proof['actual_original_failed_terminals'][name]
        sources += list(service.glob('*.json')) + list(service.glob('*.log'))
    launched = read(A / 'local_cpu_validation_recovery_actual16_hidden_launches_v1_20261007.json')
    for name in launched['identities']:
        service = A / 'service_owned_workflows_20261006' / name
        sources += [service / 'job_definition.json', service / 'native_launch.json', service / 'verified_hidden_launch.json']
    archive = A / 'CPU_HGB44_round112_failed_registration_archive_v1_20261007'
    sources += list(archive.glob('*.json')) + list((archive / 'registry').glob('*.json'))
    sources += list((A / 'CPU_HGB44_round112_actual_registration_v2_20261007').glob('*.json'))
    service = A / 'service_owned_workflows_20261006/CPU_HGB44_round112_full_registration_v2'
    sources += list(service.glob('*.json')) + list(service.glob('*.log'))
    pins = {str(p): sha(p) for p in sources}
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
            prefix = Path('validation_sync/local_cpu_validation_recovery_chain_v1_20261007')
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
            manifest = {'status': 'published_actual_round112_parent_metadata_repair_and_prefit_failure_recovery_routes',
                'at_local': sync.now(), 'files': files, 'previous_main': previous, 'only_branch': 'main',
                'actual_round112_main_full_QA_version': 23,
                'original_failed_canonical_registry_and_alias_files_preserved': 2501,
                'actual_original_prefit_failed_services': len(proof['actual_original_failed_terminals']),
                'fresh_source_variants': len(proof['new_sources_sha256']),
                'actual_new_consoleless_birth_verified_jobs': len(launched['identities']),
                'new_HGB_preparation_implementation': 'same_elementwise_ops_with8192_rows_float64_C',
                'original_HGB24_features_labels_targets_mature_windows_and_native_model_parameters_unchanged': True,
                'scientific_workers_stopped_suspended_or_restarted': 0,
                'new_official_scores_by_this_recovery': 0, 'successful44_scores_and1599600_inference_not_rerun': True,
                'new24_banks_or_full113_114_not_claimed_complete_by_route_admission': True,
                'no_data_prediction_arrays_or_model_weights_uploaded': True,
                'exact_idle_main_before_and_after_hold': idle, 'test_labels_read': False}
            payload[(prefix / 'manifest.json').as_posix()] = sync.encoded(manifest)
            payload[(prefix / 'README.md').as_posix()] = (
                '# 本机登记基准修复与前置失败后的新任务\n\n'
                '第112轮44项官方评分及冻结候选1599600行原生16模型重载、独立解码、两次重放、CSV和冷80日验证已成功。'
                '原登记模板却把获胜分数作为自身基准，记录提升0，导致与第111轮指标贡献加总断言失败。'
                '原失败登记和候选别名2501文件保留原字节归档；新登记使用实际111基准，提升3.7630824289980325e-8。'
                '不改变原44分数、选中的模型、参数、原冻结时间或预测，不重新训练、评分或推理这些成功结果。\n\n'
                '后续全股票池HGB24与ElasticNet24在前置断言退出，均尚未开始拟合；失败原生身份、定义、终态和日志均保留。'
                '新服务以修复后的112完整QA23和main终态为起点，仍须实际完成24拟合、44评分、冻结、推理、全榜和官方QA。'
                '新HGB训练仅采用已实测372000行63特征位值一致的8192行分块预处理，以降低大窗口临时矩阵内存。'
                '统计量、训练行、标签、特征与原生模型参数保持原计划；后续全量原生与独立重载验证必须真实执行。\n\n'
                '113、114未来登记生成器对正、零、负增益做了6个实际元数据回归控制，并编译16个完整源文件、核对评分字段。'
                '这些源码与任务启动检查不能冒充完整科学验证或资源穷尽。原GPU训练保持存活，未暂停、终止或重启。\n').encode('utf-8')
            scope.reverify()
            for name, data in payload.items():
                sync.atomic(sync.WORKTREE / name, data)
            names = sorted(payload)
            for offset in range(0, len(names), 50):
                sync.git('add', '-f', '--', *names[offset:offset+50])
            assert set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines()) <= set(payload)
            sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m', '修复112实际比较基准并保留全部前置失败及本机新训练路径', timeout=180)
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
