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
    closed('compact_MLP44_round111_source_route_preflight')
    proof_path = A / 'CPU_COMPACT_MLP44_round111_source_route_preflight_20261007.json'
    proof = read(proof_path)
    assert proof['status'] == 'passed_prospective_eight_source_AST_and_original_QA_reverse_routes_only'
    assert len(proof['generated_source_sha256']) == 8
    out = A / 'compact_MLP44_full111_route_evidence_github_20261007'
    assert not out.exists()
    out.mkdir()
    sources = [Path(__file__), proof_path, *[A / n for n in (
        'CPU_COMPACT_MLP44_round111_initial_route_probe_20261007.json',
        'verify_compact_MLP44_round111_sources_20261007.py',
        'CPU_COMPACT_MLP44_selected_candidate_source_admission_20261007.json',
        'CPU_COMPACT_MLP44_round111_full_registration_admission_20261007.json',
        'predict_compact_conditional_CPU_MLP_residual_CDF_scheme_20261007.py',
        'prepare_CPU_COMPACT_MLP_residual44_selected_candidate_20261007.py',
        'seal_CPU_COMPACT_MLP_residual44_selected_candidate_20261007.py',
        'prepare_CPU_COMPACT_MLP44_round111_sources_20261007.py',
        'run_CPU_COMPACT_MLP44_round111_full_registration_20261007.py',
        'compact_MLP_codec_preflight_github_20261007/receipt.json')]]
    service = A / 'service_owned_workflows_20261006/compact_MLP44_round111_source_route_preflight'
    sources += list(service.glob('*.json')) + list(service.glob('*.log'))
    for name in ('CPU_COMPACT_MLP44_selected_candidate_preparation',
        'CPU_COMPACT_MLP44_selected_candidate_sealing', 'CPU_COMPACT_MLP44_round111_full_registration'):
        service = A / 'service_owned_workflows_20261006' / name
        sources += [service / n for n in ('job_definition.json', 'verified_hidden_launch.json', 'native_launch.json')]
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
            prefix = Path('validation_sync/compact_MLP44_full111_route_evidence_20261007')
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
            manifest = {'status': 'actual_eight_compact44_source_AST_and_original_QA_reverse_route_preflight_only',
                'at_local': sync.now(), 'files': files, 'previous_main': previous, 'only_branch': 'main',
                'prospective_round': 111, 'prospective_full_QA_version': 22, 'prospective_scored_records': 44,
                'actual_generated_source_files_written': 0, 'actual_new_selection_model_fits': 0,
                'actual_new_official_quality_scores': 0, 'actual_new_future_inferences': 0,
                'initial_wrong_control_expected_literal_failure_preserved': True,
                'correct_original_collector_assertion111_22_44_actual_checked': True,
                'initial_generator_source_unchanged_between_failed_probe_and_passing_control': True,
                'original_QA_helpers_exact_reverse_bytes_checked': True,
                'selected_candidate_and_full111_hidden_services_waiting_actual20_and44_scores_main': True,
                'scientific_workers_stopped_or_restarted': 0, 'remote_workers_dispatched': 0,
                'exact_idle_main_before_and_after_hold': idle, 'test_labels_read': False}
            payload[(prefix / 'manifest.json').as_posix()] = sync.encoded(manifest)
            payload[(prefix / 'README.md').as_posix()] = (
                '# 紧凑CPU网络完整候选与第111轮源路由预检\n\n'
                '20次正式模型训练及44项官方评分完成后，才选取最高总分方案。相同106锚点复用须核对全验证预测位、8项指标和全部封存文件；'
                '若新网络胜出，先冻结，再保存重载、独立NumPy解码、完整1599600行两次及80日前缀推理，封存后登记第111轮。\n\n'
                '8个待生成源文件的AST、111/110比较关系、394组、QA22/44项计数及原QA反向字节核对实际通过。'
                '初次检查误期待函数调用文本，实际收藏器以111/22/44断言参数；该失败保留，生成器未修改，只修正检查目标。'
                '本记录未生成8个运行源文件、未执行正式训练、官方评分、未来推理或完整榜QA。\n\n'
                '候选准备、封存、完整111服务均已隐藏启动且等待真实科学结果与main回执。所有原六视图、完整参数来源、45秒浏览器检查保留；'
                '正式流程完成后还需验证完整榜与main。不改变官方公式，不使用真实测试标签，只本机D/E及GitHub main。\n').encode('utf-8')
            scope.reverify()
            for name, data in payload.items():
                sync.atomic(sync.WORKTREE / name, data)
            names = sorted(payload)
            for offset in range(0, len(names), 50):
                sync.git('add', '-f', '--', *names[offset:offset+50])
            assert set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines()) <= set(payload)
            sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m', '保存紧凑CPU网络完整111源预检以及初次检查目标错误原记录', timeout=180)
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
