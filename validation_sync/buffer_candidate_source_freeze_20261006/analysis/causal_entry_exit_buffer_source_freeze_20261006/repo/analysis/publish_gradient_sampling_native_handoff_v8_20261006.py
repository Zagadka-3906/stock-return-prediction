"""Publish actual route preparation or the completed native promotion, retaining main only."""
from pathlib import Path
import hashlib
import json
import sys
import time
import psutil
import publish_classifier_consensus_workflows_20261006 as helpers
from run_dependency_queue_v3_20261006 import owned
from hidden_windows_child_creation_20261006 import install

ROOT, A, sync = helpers.ROOT, helpers.A, helpers.sync


def create(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    checkpoint = sys.argv[1:] == ['--checkpoint']
    assert sys.argv[1:] in ([], ['--checkpoint'])
    scope = 'gradient_sampling_native_queue_v8_wiring_20261006' if checkpoint else 'gradient_sampling_native_queue_handoff_v6_20261006'
    OUT, PREFIX = A / (scope + '_github'), Path('validation_sync') / scope
    service = A / 'service_owned_workflows_20261006/gradient_sampling_native_queue_handoff_v8'
    preflight = A / 'gradient_sampling_native_queue_v6_preflight_20261006/verification.json'
    proof = sync.read(preflight)
    assert proof['status'] == 'passed_actual23_original_routes_and_unclosed_promotion_dispatch_hold'
    for path, digest in proof['input_sha256'].items():
        assert hashlib.sha256(Path(path).read_bytes()).hexdigest() == digest, path
    if checkpoint:
        assert owned(sync.read(service / 'native_launch.json'))
        snapshot = {'status': 'passed_actual_original_route_preflight_and_hidden_waiting_service',
            'actual_annual_models_at_observation': len(list((A / 'gradient_sampling_memmap_complete_bank_v3_20261006').glob('*/info_202[0-4].json'))),
            'actual_handoff_service_owned_live': True,
            'native_promotion_and_original262_quality_records_not_claimed_complete': True}
        folders = [service, A / 'gradient_sampling_native_queue_v6_preflight_20261006']
    else:
        while not (service / 'service_execution.json').exists():
            assert owned(sync.read(service / 'native_launch.json')), 'Handoff service missing without terminal evidence.'
            time.sleep(10)
        assert sync.read(service / 'service_execution.json')['status'] == 'passed'
        while owned(sync.read(service / 'native_launch.json')):
            time.sleep(.2)
        promotion = A / 'gradient_sampling_memmap_native_promotion_20261006'
        handoff = A / 'gradient_sampling_native_queue_handoff_v6_20261006'
        assert sync.read(promotion / 'verification.json')['status'] == 'passed'
        check = sync.read(handoff / 'verification.json')
        assert check['status'] == 'passed_actual_queue6_handoff_and_all36_original_GOSS_routes_exposed'
        assert owned(check['actual_new_controller'])
        assert check['scientific_processes_terminated_or_suspended'] == 0
        snapshot = {'status': check['status'], 'actual_annual_native_fits': 30, 'actual_final_native_fits': 6,
            'original262_GOSS_quality_records_and_parent_gates_preserved': True,
            'actual_all36_original_model_routes_and_all6_final_runtime_routes_passed': True}
        folders = [service, promotion, handoff, A / 'gradient_sampling_native_queue_v6_preflight_20261006',
            A / 'service_owned_workflows_20261006/dependency_queue_v6']
    observer_verified = A / 'GOSS_progress_monitor_verified_v28_20261006/verification.json'
    if not checkpoint:
        while not observer_verified.exists():
            assert not (observer_verified.parent / 'failure.json').exists(), 'Actual observer controls failed; preserve publication evidence.'
            time.sleep(5)
        assert sync.read(observer_verified)['status'] == 'passed_two_actual_observer28_complete_generations_GOSS_counts_and_original_scope'
    assert not OUT.exists()
    OUT.mkdir()
    create(OUT / 'actual_observation.json', {'at_local': sync.now(), **snapshot,
        'new_native_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})
    sources = [Path(__file__), preflight, OUT / 'actual_observation.json',
        A / 'gradient_sampling_native_queue_v8_supersession_20261006.json',
        *[A / name for name in (
        'promote_gradient_sampling_memmap_native_bank_20261006.py',
        'handoff_gradient_sampling_native_to_original_queue_v8_20261006.py',
        'verify_gradient_sampling_native_queue_v6_20261006.py', 'run_dependency_queue_v6_20261006.py',
        'gradient_sampling_native_queue_v6_source_generation_20261006.json',
        'prepare_gradient_sampling_native_handoff_v8_20261006.py')]]
    for folder in folders:
        # Staged/canonical model weights and raw arrays are excluded from publication.
        sources += sorted(folder.glob('*.json'))
        if folder == service:
            sources += sorted(folder.glob('*.log'))
    if not checkpoint:
        sources += [A / 'service_owned_dependency_queue_v4_20261006/queue_plan_v6.json']
    sources += [A / 'monitor_actual_optimization_progress_v28_20261006.py', A / 'handoff_GOSS_progress_monitor_v28_20261006.py', A / 'verify_GOSS_progress_monitor_v28_20261006.py', A / 'GOSS_progress_monitor28_source_generation_20261006.json', A / 'GOSS_monitor28_unfrozen_preparation_correction_20261006.json']
    for name in ('GOSS_progress_monitor_handoff_v26_20261006', 'GOSS_progress_monitor_handoff_v27_20261006', 'GOSS_progress_monitor_handoff_v28_20261006', 'GOSS_progress_monitor_verified_v28_20261006', 'service_owned_workflows_20261006/progress_monitor_v26', 'service_owned_workflows_20261006/progress_monitor_v28', 'service_owned_workflows_20261006/gradient_sampling_native_queue_handoff_v6', 'service_owned_workflows_20261006/gradient_sampling_native_queue_handoff_v6_publication', 'service_owned_workflows_20261006/gradient_sampling_native_queue_handoff_v7'):
        folder = A / name
        if folder.exists():
            sources += sorted(folder.glob('*.json'))
            if not checkpoint:
                sources += sorted(folder.glob('*.jsonl'))
    sources += [A / 'monitor_actual_optimization_progress_v26_20261006.py', A / 'monitor_actual_optimization_progress_v27_20261006.py', A / 'handoff_GOSS_progress_monitor_v26_20261006.py', A / 'handoff_GOSS_progress_monitor_v27_20261006.py', A / 'GOSS_progress_monitor27_source_generation_20261006.json', A / 'handoff_gradient_sampling_native_to_original_queue_v7_20261006.py', A / 'prepare_gradient_sampling_native_handoff_v7_20261006.py']
    targets = {(PREFIX / '.gitattributes').as_posix(): b'* -text\n'}
    files = {}
    for source in dict.fromkeys(sources):
        data = source.read_bytes()
        assert not sync.SECRET.search(data)
        destination = source.relative_to(ROOT) if source.parent == A and source.suffix == '.py' else PREFIX / source.relative_to(ROOT)
        targets[destination.as_posix()] = data
        files[source.relative_to(ROOT).as_posix()] = {
            'published_path': destination.as_posix(), 'raw_sha256': hashlib.sha256(data).hexdigest()}
    restore, suspended = install(), []
    try:
        pub = sync.read(A / 'service_owned_workflows_20261006/main_publisher_v5/native_launch.json')
        assert owned(pub)
        root, worker = helpers.owned_pair(pub['pid'], Path(pub['script']), pub['script_args'])
        assert worker.pid == pub['owned_worker_pid'] and worker.create_time() == pub['owned_worker_creation_time']
        for attempt in range(300):
            for process in (worker, root):
                process.suspend()
                suspended.append(process)
            busy = [p for p in root.children(recursive=True) if p.pid != worker.pid and p.name().lower() != 'conhost.exe']
            if not busy:
                break
            for process in reversed(suspended):
                process.resume()
            suspended.clear()
            time.sleep(1.)
        else:
            raise RuntimeError('Main publisher still owns an active publication child.')
        previous = sync.git('rev-parse', 'HEAD')
        helpers.verify_main(previous)
        assert not sync.git('status', '--porcelain')
        targets[(PREFIX / 'manifest.json').as_posix()] = sync.encoded({
            'status': snapshot['status'], 'at_local': sync.now(), 'files': files,
            'previous_main': previous, 'actual_evidence': snapshot,
            'new_native_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False,
            'only_publication_branch': 'main'})
        targets[(PREFIX / 'README.md').as_posix()] = (
            '# GOSS完整模型接入原定评分队列\n\n'
            + ('准备检查及实际隐藏等待服务已核验；等待全部30个年度模型、6个最终模型、完整未来推理与main回执。原23个待办评分任务驱动参数和父方案保持不变，完整证明生成前全部派发被拦住。此记录不声称接入或评分已完成。\n' if checkpoint else
               '完整30个年度300轮模型、6个最终模型及全部未来推理控制通过并已发布main后，逐文件SHA核验并接入原路径。核对全部36个模型路径及6个原始完整方案最终推理路径。仅接管旧调度器，已完成原生任务以实际服务终态和主分支回执替代，复制及完成记录不计为新拟合。原23个待办评分任务、原67—94范围、第75/76轮262个方案及其父方案保持不变。\n')
            + '\n保持当前科学进程。只上传记录、源代码和分数，模型及数据留在D。官方完整评分、冻结、因果检查、候选推理与完整榜仍沿原定流程推进。不读取TestY，不宣称全局优化或计算边界已经完成。\n').encode('utf-8')
        for name, data in targets.items():
            sync.atomic(sync.WORKTREE / name, data)
        selected = sorted(targets)
        for offset in range(0, len(selected), 50):
            sync.git('add', '-f', '--', *selected[offset:offset + 50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(selected)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            '同步GOSS原始评分路由准备与隐藏等待服务' if checkpoint else '完成GOSS36模型原路径接入及调度接管且保持全部原始评分范围', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        expected = {name: hashlib.sha256(data).hexdigest() for name, data in targets.items()}
        assert helpers.blob_hashes(commit, expected) == expected
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        helpers.verify_main(commit)
        helpers.watcher.advance_source_index(commit)
        create(OUT / 'receipt.json', {'status': 'pushed_actual_controls_main_only', 'at_local': sync.now(),
            'commit': commit, 'raw_git_blobs_verified': len(expected), 'control_status': 'passed', 'scope': snapshot['status'], 'new_quality_scores': 0,
            'url': 'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/' + PREFIX.as_posix()})
    except BaseException as error:
        create(OUT / 'failure.json', {'status': 'failed_preserved_publication_attempt', 'error': f'{type(error).__name__}: {error}'})
        raise
    finally:
        for process in reversed(suspended):
            if process.is_running():
                process.resume()
        create(OUT / 'actual_hidden_publication_children.json', {'actual_CreateProcess_calls': restore()})


if __name__ == '__main__':
    main()
