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
    closed('HGB44_round112_source_route_preflight')
    proof_path = A / 'CPU_HGB44_round112_source_route_preflight_20261007.json'
    proof = read(proof_path)
    assert proof['status'] == 'passed_prospective_eight_source_AST_and_original_QA_reverse_routes_only'
    assert len(proof['generated_source_sha256']) == 8
    out = A / 'HGB44_full112_route_evidence_github_20261007'
    assert not out.exists()
    out.mkdir()
    sources = [Path(__file__), proof_path, *[A / n for n in (
        'verify_HGB44_round112_sources_20261007.py',
        'CPU_HGB44_selected_candidate_source_admission_20261007.json',
        'CPU_HGB44_round112_full_registration_admission_20261007.json',
        'predict_conditional_CPU_HGB_residual_CDF_scheme_20261007.py',
        'prepare_CPU_HGB_residual44_selected_candidate_20261007.py',
        'seal_CPU_HGB_residual44_selected_candidate_20261007.py',
        'prepare_CPU_HGB44_round112_sources_20261007.py',
        'run_CPU_HGB44_round112_full_registration_20261007.py',
        'cpu_conditional_residual_hgb20_bank_github_20261007/receipt.json')]]
    service = A / 'service_owned_workflows_20261006/HGB44_round112_source_route_preflight'
    sources += list(service.glob('*.json')) + list(service.glob('*.log'))
    for name in ('CPU_HGB44_selected_candidate_preparation',
        'CPU_HGB44_selected_candidate_sealing', 'CPU_HGB44_round112_full_registration'):
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
            prefix = Path('validation_sync/HGB44_full112_route_evidence_20261007')
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
                'prospective_round': 112, 'prospective_full_QA_version': 23, 'prospective_scored_records': 44,
                'actual_generated_source_files_written': 0, 'actual_new_selection_model_fits': 0,
                'actual_new_official_quality_scores': 0, 'actual_new_future_inferences': 0,
                'four_actual_historical_HGB_codec_and20_bank_controls_already_passed': True,
                'correct_original_collector_assertion112_23_44_actual_checked': True,
                'HGB_bank_models_have64_actual_boosting_iterations': True,
                'original_QA_helpers_exact_reverse_bytes_checked': True,
                'selected_candidate_and_full112_hidden_services_waiting_actual20_and44_scores_main': True,
                'scientific_workers_stopped_or_restarted': 0, 'remote_workers_dispatched': 0,
                'exact_idle_main_before_and_after_hold': idle, 'test_labels_read': False}
            payload[(prefix / 'manifest.json').as_posix()] = sync.encoded(manifest)
            payload[(prefix / 'README.md').as_posix()] = (
                '# CPU直方图梯度回归完整候选与第112轮源预检\n\n'
                '平方/绝对误差各7/15叶，20个成熟窗口模型已训练，通过独立数值树NumPy解码、保存重载及日期前缀控制。'
                '本源预检通过8个待生成文件AST、112/111比较关系、395组、QA23/44项计数以及原QA反向逐字节核对。\n\n'
                '44项正式官方评分须等待完整111/main QA22关闭；仅最高完整官方S选优。相同106锚点核对全预测位、8指标、2237封存文件后复用；'
                '若新HGB胜出则冻结并执行完整1599600行两次、80日前缀及独立树解码，随后完整112/main QA23。'
                '所附源预检不代表这些后续科学评分、推理或完整榜QA已执行。\n\n'
                '四个HGB历史诊断及20个正式模型都已实际通过，其bank回执单独附上。全部进程隐藏、本机D/E、GitHub仅main，未读真实测试标签。\n').encode('utf-8')
            scope.reverify()
            for name, data in payload.items():
                sync.atomic(sync.WORKTREE / name, data)
            names = sorted(payload)
            for offset in range(0, len(names), 50):
                sync.git('add', '-f', '--', *names[offset:offset+50])
            assert set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines()) <= set(payload)
            sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m', '保存CPU直方图梯度回归完整112候选与QA23源路由实际预检', timeout=180)
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
