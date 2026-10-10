"""Publish completed GOSS backend controls and the actual pending full-capacity launch."""
from pathlib import Path
import hashlib
import json
import time

import psutil
import publish_classifier_consensus_workflows_20261006 as helpers
from run_dependency_queue_v3_20261006 import owned
from hidden_windows_child_creation_20261006 import install

ROOT, A, sync = helpers.ROOT, helpers.A, helpers.sync
SOURCE = A / 'gradient_sampling_exact_memmap_preflight_20261006'
OUT = A / 'gradient_sampling_exact_memmap_preflight_github_20261006'
PREFIX = Path('validation_sync/gradient_sampling_exact_memmap_preflight_20261006')


def create(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    assert not OUT.exists()
    OUT.mkdir()
    proof = sync.read(SOURCE / 'verification.json')
    assert proof['status'] == 'passed_all6_native_GOSS_parameters_and_full_original_preprocessing_and_full2020_equivalence'
    assert proof['actual_pilot_native_fits'] == 12 and proof['actual_full2020_native_control_fits'] == 2
    assert proof['control_weights_written'] == proof['actual_bank_annual_fits'] == proof['new_quality_scores'] == 0
    for filename, digest in proof['input_sha256'].items():
        assert sha(filename) == digest
    service = A / 'service_owned_workflows_20261006/gradient_sampling_memmap_capacity'
    launch = sync.read(service / 'native_launch.json')
    assert owned(launch)
    assert launch['actual_native_console_handle'] == 0 and not launch['independent_launch_root_in_any_job']
    protocol = sync.read(A / 'gradient_sampling_memmap_capacity_20261006/protocol.json')
    assert protocol['expected_actual_full_final_fits'] == 6
    resources = sync.read(SOURCE / 'resource_summary.json')
    assert resources['status'] == 'passed' and not resources['observation_errors']
    actual_completed = sorted(p.parent.name for p in (A / 'gradient_sampling_memmap_capacity_20261006').glob('*/future_verification.json'))
    create(OUT / 'actual_launch_observation.json', {
        'at_local': sync.now(), 'actual_owned_native_launch': launch,
        'actual_complete_largest_native_and_future_models_at_observation': actual_completed,
        'actual_host_available_bytes_at_observation': psutil.virtual_memory().available,
        'largest_full_scope_remains_pending': len(actual_completed) < 6,
        'completed_backend_control_is_not_an_official_quality_result': True,
        'original30_annual_and262_quality_records_still_required': True,
        'new_quality_scores': 0, 'test_labels_read': False})
    sources = [Path(__file__), *[A / name for name in (
        'gradient_sampling_exact_memmap_20261006.py', 'verify_gradient_sampling_exact_memmap_20261006.py',
        'independent_gradient_sampling_native_codec_20261006.py', 'watch_owned_scheduler_fit_lease_20261006.py',
        'owned_scheduler_native_fit_hold_20261006.py', 'verify_full2025_gradient_sampling_memmap_capacity_20261006.py',
        'prepare_gradient_sampling_memmap_capacity_20261006.py')]]
    for folder in (SOURCE, service, A / 'gradient_sampling_memmap_capacity_20261006', OUT):
        for pattern in ('*.json', '*.jsonl', '*.txt', '*.log'):
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
            'status': 'passed_backend_equivalence_controls_actual_full_capacity_pending',
            'at_local': sync.now(), 'files': files, 'previous_main': previous,
            'entire_actual_control_execution_preserved': True,
            'actual_control_native_fits': 14, 'control_weights_written': 0,
            'actual_bank_annual_fits': 0, 'original30_annual_and262_quality_records_still_required': True,
            'actual_completed_full_capacity_models_at_observation': actual_completed,
            'capacity_live_logs_are_time_bounded_snapshots_not_terminal_evidence': True,
            'new_quality_scores': 0, 'physical_resource_boundary_established': False,
            'test_labels_read': False, 'only_publication_branch': 'main'})
        targets[(PREFIX / 'README.md').as_posix()] = (
            '# GOSS磁盘映射后端：已完成等价性检查，最大训练窗口待验证\n\n'
            '原6套GOSS参数保持不变。完整6,754,006行、63特征的原均值、尺度及标准化字节与共享磁盘缓存一致。'
            '每套参数在32,768行实样本上训练原数组和磁盘映射各一个300轮模型；6对完整原生模型字符串、参数、目标截尾、预处理和预测均一致。\n\n'
            '另对完整2020成熟训练集1,694,259行进行两个300轮配对控制，核对完整原生模型字符串及2020全部1,129,950行预测。'
            '保存格式的内存重载和80日372,000行冷启动均逐位一致。共14个控制拟合，写入模型权重0，新增正式年模型和质量成绩0。\n\n'
            '113次实际资源观测记录控制进程峰值约1.875 GiB，观测错误0；此值只描述控制实验，不能证明最大窗口的资源上限。'
            '最大窗口工作流已按无窗口方式实际启动并核验身份。六个完整6,754,006行、300轮拟合及完整未来输入检查仍待完成。'
            '启动前12 GiB可用内存要求是保守调度策略，不是物理边界。每次原生拟合只暂缓新任务派发，并有异常退出恢复守护；当前验证和GPU训练继续运行。\n\n'
            '随后仍须完成原30个年模型、第75/76轮共262个完整方案的官方评分、冻结、因果检查、候选推理和完整榜更新。'
            '控制实验不依据未来标签选择方案，不读取TestY。源码、成功证据、资源记录和实际启动快照仅同步main；未宣布优化目标完成。\n'
        ).encode('utf-8')
        for name, data in targets.items():
            sync.atomic(sync.WORKTREE / name, data)
        selected = sorted(targets)
        for offset in range(0, len(selected), 50):
            sync.git('add', '-f', '--', *selected[offset:offset + 50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(selected)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            '核验GOSS全量预处理及14个配对控制并记录最大窗口实际无窗口启动', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        expected = {name: hashlib.sha256(data).hexdigest() for name, data in targets.items()}
        assert helpers.blob_hashes(commit, expected) == expected
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        helpers.verify_main(commit)
        helpers.watcher.advance_source_index(commit)
        create(OUT / 'receipt.json', {'status': 'pushed_actual_controls_main_only', 'at_local': sync.now(),
            'commit': commit, 'raw_git_blobs_verified': len(expected), 'new_quality_scores': 0,
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
