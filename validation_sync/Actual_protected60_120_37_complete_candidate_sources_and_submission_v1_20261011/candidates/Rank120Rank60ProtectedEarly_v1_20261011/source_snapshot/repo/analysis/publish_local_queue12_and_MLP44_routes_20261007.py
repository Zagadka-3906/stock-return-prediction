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
    closed('dependency_queue_v12_local_cache_routes_preflight')
    closed('dependency_queue_v12_local_cache_handoff')
    closed('local_only_monitor_v4_actual_handoff')
    proof = read(A / 'dependency_queue_v12_local_cache_actual_handoff_20261007/verification.json')
    assert proof['status'] == 'passed_actual_all32_local_queue12_handoff_preserved_live89_and_GPU'
    observer = read(A / 'local_only_monitor_v4_actual_handoff_20261007/verification.json')
    assert observer['status'] == 'passed_actual_idle_observer4_complete_queue12_and_R89_and_MLP44_generation'
    out = A / 'local_queue12_and_MLP44_routes_github_20261007'
    assert not out.exists()
    out.mkdir()
    sources = [Path(__file__), *[A / n for n in (
        'run_dependency_queue_v12_local_cache_and_R89_qualification_20261007.py',
        'verify_dependency_queue_v12_local_cache_routes_20261007.py',
        'handoff_dependency_queue_v12_local_cache_20261007.py',
        'run_classifier_consensus_round90_with_precise_gate_and_parent_cache_20261007.py',
        'qualified_round_recovery_evidence_v4_20261007.py',
        'predict_conditional_CPU_MLP_residual_CDF_scheme_20261007.py',
        'prepare_CPU_MLP_residual44_selected_candidate_20261007.py',
        'seal_CPU_MLP_residual44_selected_candidate_20261007.py',
        'CPU_MLP44_selected_candidate_source_admission_20261007.json',
        'prepare_CPU_MLP44_round110_sources_20261007.py',
        'run_CPU_MLP44_round110_full_registration_20261007.py',
        'CPU_MLP44_round110_full_registration_admission_20261007.json',
        'CPU_MLP44_round110_source_route_preflight_20261007.json',
        'monitor_local_only_runtime_v4_20261007.py', 'handoff_local_only_monitor_v4_20261007.py',
        'parent_graph_rank_cache_evidence_github_20261007/receipt.json',
        'cpu_conditional_residual_mlp20_bank_github_20261007/receipt.json',
        'service_owned_dependency_queue_v12_local_cache_20261007/queue_plan.json',
        'service_owned_workflows_20261006/dependency_queue_bootstrap_fields_recovery_v2/administrative_supersession_local_v12_20261007.json',
        'service_owned_workflows_20261006/local_only_progress_monitor_v3/administrative_supersession_local_v4_20261007.json')]]
    for folder in ('dependency_queue_v12_local_cache_routes_preflight_20261007',
                   'dependency_queue_v12_local_cache_actual_handoff_20261007',
                   'local_only_monitor_v4_actual_handoff_20261007'):
        sources += list((A / folder).glob('*.json'))
    for name in ('dependency_queue_v12_local_cache_routes_preflight', 'dependency_queue_v12_local_cache_handoff',
                 'local_only_monitor_v4_actual_handoff'):
        folder = A / 'service_owned_workflows_20261006' / name
        sources += list(folder.glob('*.json')) + list(folder.glob('*.log'))
    for name in ('dependency_queue_v12_local_cache', 'local_only_progress_monitor_v4',
                 'CPU_MLP44_selected_candidate_preparation', 'CPU_MLP44_selected_candidate_sealing',
                 'CPU_MLP44_round110_full_registration'):
        folder = A / 'service_owned_workflows_20261006' / name
        sources += [folder / n for n in ('job_definition.json', 'verified_hidden_launch.json', 'native_launch.json')]
    assert all(p.is_file() for p in sources), [str(p) for p in sources if not p.is_file()]
    pins = {**proof['input_sha256'], **observer['input_sha256'], **{str(p): sha(p) for p in sources}}
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
            prefix = Path('validation_sync/local_queue12_and_MLP44_routes_20261007')
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
            manifest = {'status': 'actual_original32_local_queue_and_exact_idle_observer_adoption_with_prospective_MLP44_routes',
                'at_local': sync.now(), 'files': files, 'previous_main': previous, 'only_branch': 'main',
                'original_deferred_routes_preserved': 32, 'scientific_workers_stopped_or_restarted': 0,
                'remote_workers_dispatched': 0, 'R90_only_unstarted_dispatch_adds_verified_parent_rank_cache': True,
                'R89_alternate_full_science_and_QA4_main_receipt_required_before_R90': True,
                'MLP44_full110_QA21_main_receipt_required_before_R90': True,
                'MLP44_eight_generated_source_AST_and_original_QA_reverse_route_preflight_only': True,
                'MLP44_and_R90_actual_scores_or_new_inference_not_claimed_by_this_evidence': True,
                'new_model_selection_scores_by_this_publication': 0,
                'queue_handoff_verification_status': proof['status'], 'observer_verification_status': observer['status'],
                'exact_idle_main_before_and_after_hold': idle, 'test_labels_read': False}
            payload[(prefix / 'manifest.json').as_posix()] = sync.encoded(manifest)
            payload[(prefix / 'README.md').as_posix()] = (
                '# 本机队列与后续条件残差MLP完整流程准备记录\n\n'
                '原32条任务路径与参数保留。第89轮改绑定到实际仍存活的恢复实例，原失败作用域与原失败身份留存。'
                '只为尚未启动的第90轮增加已实际通过5635800行及空缓存80/260/975日前缀逐位核验的父方案排序缓存。\n\n'
                '第90轮严格等待第89轮完整科学验证、QA4、main回执，以及CPU MLP44的完整第110轮QA21和main回执。'
                '第110轮8个待生成源文件的AST和原QA反向替换核验已通过；这不是实际44项评分、候选推理或第110轮完整榜QA。\n\n'
                '新队列实际接管、进度监控第四版完整代际写入均已通过。只替换有身份、空闲栈和无子进程证明的管理辅助进程；'
                '科学训练、评分与GPU进程没有暂停、停止或重启。全部进程隐藏窗口，本机D/E存储，仅GitHub main。\n').encode('utf-8')
            scope.reverify()
            for name, data in payload.items():
                sync.atomic(sync.WORKTREE / name, data)
            names = sorted(payload)
            for offset in range(0, len(names), 50):
                sync.git('add', '-f', '--', *names[offset:offset+50])
            assert set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines()) <= set(payload)
            sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m', '保存本机32路径队列真实接管与MLP44完整候选及QA21流程源预检证据', timeout=180)
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
