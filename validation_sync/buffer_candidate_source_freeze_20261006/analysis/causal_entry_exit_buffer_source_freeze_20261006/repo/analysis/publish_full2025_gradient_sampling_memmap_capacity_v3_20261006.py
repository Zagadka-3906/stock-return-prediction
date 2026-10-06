"""Wait for all6 actual full native closures, verify their evidence, then publish the complete capacity scope."""
from pathlib import Path
import hashlib
import json
import time

import psutil
import publish_classifier_consensus_workflows_20261006 as helpers
from run_dependency_queue_v3_20261006 import owned
from hidden_windows_child_creation_20261006 import install

ROOT, A, sync = helpers.ROOT, helpers.A, helpers.sync
SOURCE = A / 'gradient_sampling_memmap_capacity_v3_20261006'
OUT = A / 'gradient_sampling_memmap_capacity_v3_github_20261006'
PREFIX = Path('validation_sync/gradient_sampling_memmap_capacity_v3_20261006')


def create(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    service = A / 'service_owned_workflows_20261006/gradient_sampling_memmap_capacity_v3'
    while not (service / 'service_execution.json').exists():
        assert owned(sync.read(service / 'native_launch.json')), 'Native capacity actor disappeared without terminal evidence.'
        time.sleep(10.)
    assert sync.read(service / 'service_execution.json')['status'] == 'passed'
    while owned(sync.read(service / 'native_launch.json')):
        time.sleep(.2)
    assert not OUT.exists()
    OUT.mkdir()
    proof = sync.read(SOURCE / 'verification.json')
    assert proof['status'] == 'passed_all6_actual_largest_full_GOSS_native_fits_and_complete_future_controls'
    assert proof['actual_full_final_fits'] == proof['actual300_iteration_models'] == len(proof['checks']) == 6
    assert proof['actual_bank_annual_fits'] == proof['new_quality_scores'] == 0
    for filename, digest in proof['input_sha256'].items():
        assert sha(filename) == digest
    service = A / 'service_owned_workflows_20261006/gradient_sampling_memmap_capacity_v3'
    launch = sync.read(service / 'native_launch.json')
    assert not owned(launch) and sync.read(service / 'service_execution.json')['status'] == 'passed'
    assert launch['actual_native_console_handle'] == 0 and not launch['independent_launch_root_in_any_job']
    protocol = sync.read(A / 'gradient_sampling_memmap_capacity_v3_20261006/protocol.json')
    assert protocol['expected_actual_full_final_fits'] == 6
    resources = sync.read(SOURCE / 'resource_summary.json')
    assert resources['status'] == 'passed' and not resources['observation_errors']
    assert proof['all_temporary_dependency_dispatch_holds_released']
    holds = list(SOURCE.glob('scheduler_fit_hold_*/released.json'))
    assert len(holds) == 6 and all(sync.read(p)['scientific_workers_touched'] == 0 for p in holds)
    assert all(sync.read(p.parent / 'independent_guard_service/service_execution.json')['status'] == 'passed' for p in holds)
    for check in proof['checks']:
        folder = SOURCE / check['model']
        info = sync.read(folder / 'info_2025.json')
        assert info['actual_native_iterations'] == 300 and info['training_meta']['rows'] == 6754006
        assert sha(folder / 'model_2025.joblib') == info['model_sha256'] == check['model_sha256']
        assert sha(folder / 'future_raw.parquet') == check['future_parquet_sha256']
        assert check['actual_full_future_shape'] == [1599600, 344, 4650]
        assert sync.read(folder / 'future_verification.json')['status'] == 'passed'
        assert check['full_saved_reload_independent_codec_and_cold80_37day_predictions_bit_identical']
        assert check['independent_dumped_leaf_sum131_rows_max_abs_error'] < 1e-10
    actual_completed = sorted(p.parent.name for p in (A / 'gradient_sampling_memmap_capacity_v3_20261006').glob('*/future_verification.json'))
    create(OUT / 'actual_launch_observation.json', {
        'at_local': sync.now(), 'actual_owned_native_launch': launch,
        'actual_complete_largest_native_and_future_models_at_observation': actual_completed,
        'actual_host_available_bytes_at_observation': psutil.virtual_memory().available,
        'largest_full_scope_remains_pending': len(actual_completed) < 6,
        'completed_backend_control_is_not_an_official_quality_result': True,
        'original30_annual_and262_quality_records_still_required': True,
        'new_quality_scores': 0, 'test_labels_read': False})
    sources = [Path(__file__), *[A / name for name in (
        'verify_full2025_gradient_sampling_memmap_capacity_v3_20261006.py',
        'gradient_sampling_exact_memmap_20261006.py', 'owned_scheduler_native_fit_hold_v2_20261006.py',
        'watch_owned_scheduler_fit_lease_20261006.py', 'independent_gradient_sampling_native_codec_20261006.py',
        'train_gradient_sampling_memmap_bank_v3_20261006.py', 'run_gradient_sampling_memmap_full_workflow_v3_20261006.py',
        'verify_gradient_sampling_memmap_full_future_v3_20261006.py')]]
    for folder in (SOURCE, service, OUT):
        for pattern in ('*.json', '*.jsonl', '*.txt', '*.log', '*.py'):
            sources += sorted(folder.rglob(pattern))
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
            'status': 'passed_all6_largest_full_native_fits_and_complete_future_controls',
            'at_local': sync.now(), 'files': files, 'previous_main': previous,
            'entire_actual_control_execution_preserved': True,
            'actual_full_final_native_fits': 6, 'actual_bank_annual_fits': 0,
            'actual_bank_annual_fits': 0, 'original30_annual_and262_quality_records_still_required': True,
            'actual_completed_full_capacity_models': actual_completed, 'terminal_actual_full_scope_verified': True,
            'capacity_native_terminal_and_all6_future_controls_verified': True,
            'new_quality_scores': 0, 'physical_resource_boundary_established': False,
            'test_labels_read': False, 'only_publication_branch': 'main'})
        targets[(PREFIX / 'README.md').as_posix()] = '# 六套GOSS最大窗口拟合及完整未来输入控制全部完成\n\n全部六套原配置实际使用6,754,006行成熟训练样本、63特征，完整训练300轮，无样本缩减或验证早停。原模型参数、原均值尺度、原标准化和目标处理保持不变。每个模型绑定实际拟合时间、原生模型字符串、保存模型SHA256及完整成熟信息。\n\n每套模型实际覆盖1,599,600行、344日、4,650股票的全部未来X。原预测、保存模型重载、独立8192行块解码、真实80日372,000行及37日冷启动逐位一致；另独立重构131行原生叶子加和，误差均小于1e-10。无效价格的-1e6规则在原始预测核验之后恢复。\n\n全部六次调度临时保护已释放，独立守护服务正常结束，实际训练与评分进程未被暂停。失败的首版保护检查及正常、异常恢复控制已另行完整上传；本次实测证明这个环境可以完成六个最大窗口，不证明全局物理资源上限。\n\n六个完整最终模型后续复用，不重复计为新增拟合。原30个年度模型和第75/76轮共262个完整输出方案仍要求完成官方评分、方案冻结、因果检查、候选推理与完整榜更新。这些原生未来输入检查不选择完整方案、不读取TestY，不宣布目标完成。记录、源码及完整成功证明只上传main，模型权重继续保留于D以供待办验证。\n'.encode('utf-8')
        for name, data in targets.items():
            sync.atomic(sync.WORKTREE / name, data)
        selected = sorted(targets)
        for offset in range(0, len(selected), 50):
            sync.git('add', '-f', '--', *selected[offset:offset + 50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(selected)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            '完成GOSS六个最大窗口300轮原生拟合及完整未来输入一致性验证', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        expected = {name: hashlib.sha256(data).hexdigest() for name, data in targets.items()}
        assert helpers.blob_hashes(commit, expected) == expected
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        helpers.verify_main(commit)
        helpers.watcher.advance_source_index(commit)
        create(OUT / 'receipt.json', {'status': 'pushed_actual_controls_main_only', 'at_local': sync.now(),
            'commit': commit, 'raw_git_blobs_verified': len(expected), 'control_status': 'passed', 'new_quality_scores': 0,
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
