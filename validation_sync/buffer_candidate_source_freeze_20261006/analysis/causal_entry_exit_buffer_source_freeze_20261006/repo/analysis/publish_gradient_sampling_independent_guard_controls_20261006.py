"""Publish actual failed admission guard, both successful independent recovery controls, and the full native trial."""
from pathlib import Path
import hashlib
import json
import time

import psutil
import publish_classifier_consensus_workflows_20261006 as helpers
from run_dependency_queue_v3_20261006 import owned
from hidden_windows_child_creation_20261006 import install

ROOT, A, sync = helpers.ROOT, helpers.A, helpers.sync
SOURCE = A / 'scheduler_fit_guard_controls_v2_20261006'
OUT = A / 'gradient_sampling_independent_guard_controls_github_20261006'
PREFIX = Path('validation_sync/gradient_sampling_independent_guard_controls_20261006')


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
    assert proof['status'] == 'passed_actual_independent_WMI_guard_normal_and_abrupt_venv_owner_exit'
    assert {c['mode'] for c in proof['checks']} == {'normal', 'abrupt_exit'}
    assert proof['actual_scientific_or_dependency_workers_touched'] == proof['new_native_fits'] == proof['new_quality_scores'] == 0
    for filename, digest in proof['input_sha256'].items():
        assert sha(filename) == digest
    service = A / 'service_owned_workflows_20261006/gradient_sampling_memmap_capacity_v3'
    launch = sync.read(service / 'native_launch.json')
    assert owned(launch)
    assert launch['actual_native_console_handle'] == 0 and not launch['independent_launch_root_in_any_job']
    protocol = sync.read(A / 'gradient_sampling_memmap_capacity_v3_20261006/protocol.json')
    assert protocol['expected_actual_full_final_fits'] == 6
    assert sync.read(A / 'gradient_sampling_memmap_independent_guard_v3_wiring_20261006/verification.json')['status'] == 'passed_actual_independent_guard_v3_full_scope_dispatch_after_normal_and_abrupt_exit_controls'
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
        'owned_scheduler_native_fit_hold_20261006.py', 'owned_scheduler_native_fit_hold_v2_20261006.py',
        'watch_owned_scheduler_fit_lease_20261006.py', 'scheduler_hold_dummy_heartbeat_20261006.py',
        'scheduler_hold_synthetic_owner_20261006.py', 'verify_independent_scheduler_fit_guard_v2_20261006.py',
        'handoff_gradient_sampling_capacity_admission_v2_20261006.py',
        'prepare_gradient_sampling_independent_guard_v3_workflows_20261006.py',
        'verify_full2025_gradient_sampling_memmap_capacity_v2_20261006.py',
        'verify_full2025_gradient_sampling_memmap_capacity_v3_20261006.py',
        'train_gradient_sampling_memmap_bank_v2_20261006.py', 'train_gradient_sampling_memmap_bank_v3_20261006.py',
        'run_gradient_sampling_memmap_full_workflow_v2_20261006.py', 'run_gradient_sampling_memmap_full_workflow_v3_20261006.py',
        'verify_gradient_sampling_memmap_full_future_v2_20261006.py', 'verify_gradient_sampling_memmap_full_future_v3_20261006.py')]]
    folders = [SOURCE, OUT, A / 'gradient_sampling_memmap_admission_v2_handoff_20261006',
        A / 'gradient_sampling_memmap_independent_guard_v3_wiring_20261006',
        A / 'gradient_sampling_memmap_capacity_v2_20261006', A / 'gradient_sampling_memmap_capacity_v3_20261006']
    folders += [A / f'service_owned_workflows_20261006/{name}' for name in (
        'gradient_sampling_memmap_capacity', 'gradient_sampling_memmap_complete_workflow',
        'gradient_sampling_memmap_capacity_v2', 'gradient_sampling_memmap_complete_workflow_v2',
        'gradient_sampling_memmap_capacity_v3', 'gradient_sampling_memmap_complete_workflow_v3')]
    sources += [A / 'gradient_sampling_memmap_admission_v2_source_generation_20261006.json',
                A / 'gradient_sampling_memmap_independent_guard_v3_source_generation_20261006.json']
    for folder in folders:
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
            'status': 'passed_independent_guard_controls_actual_full_native_trial_pending',
            'at_local': sync.now(), 'files': files, 'previous_main': previous,
            'entire_actual_control_execution_preserved': True,
            'actual_control_native_fits': 0, 'synthetic_independent_guard_cases_passed': 2,
            'actual_bank_annual_fits': 0, 'original30_annual_and262_quality_records_still_required': True,
            'actual_completed_full_capacity_models_at_observation': actual_completed,
            'capacity_live_logs_are_time_bounded_snapshots_not_terminal_evidence': True,
            'new_quality_scores': 0, 'physical_resource_boundary_established': False,
            'test_labels_read': False, 'only_publication_branch': 'main'})
        targets[(PREFIX / 'README.md').as_posix()] = '# GOSS启动保护失败、独立恢复守护实测及完整模型试运行\n\n原12 GiB条件下的GOSS任务始终处于零拟合等待状态。依据已完成四个最大窗口分位树试验的3.24 GiB进程峰值，并额外预留4 GiB，建立独立的8 GiB入场试验。原六套GOSS参数、6,754,006行、63特征及300轮均保持一致；另一目标的内存观测不是GOSS内存上限。\n\n第一次8 GiB尝试在FitHold保护检查中失败：WMI启动根进程脱离Job，并不代表虚拟环境重定向器的原生子进程也脱离其自身Job。失败发生在守护启动、调度暂停和原生模型拟合之前，模型权重0。下游等待器正确拒绝失败的父任务。失败源码、堆栈、资源及终态全部保留，不作为GOSS硬件边界证据。\n\n修复采用真正独立的WMI守护服务。实际服务控制测试覆盖正常结束与有意os._exit(37)的异常退出；模拟调度器心跳确实暂停并恢复，异常情况下守护只恢复精确PID、创建时间及命令一致的模拟进程。两个控制均通过，实际科学训练及依赖进程触碰0。\n\n原12 GiB零拟合等待任务已明确行政接管，未制造成功执行标记。失败8 GiB尝试已终态，修复后的完整范围工作流实际启动；第一套GOSS已进入最大窗口原生拟合。所有新启动和守护均无可见控制台，原GPU训练、第84轮及发布器继续运行。\n\n实时资源文件及已完成子模型在本次提交中只是带时间边界的快照，六个完整拟合及推理控制是否完成应查看后续终态证明。30个年度模型、第75/76轮262个完整方案评分、冻结、因果检查、候选推理和完整榜仍全部要求完成。未读取TestY，未声明GOSS资源上限或全局目标完成；成功与失败记录仅上传main。\n'.encode('utf-8')
        for name, data in targets.items():
            sync.atomic(sync.WORKTREE / name, data)
        selected = sorted(targets)
        for offset in range(0, len(selected), 50):
            sync.git('add', '-f', '--', *selected[offset:offset + 50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(selected)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            '保留GOSS启动保护失败并核验独立守护正常及异常恢复和实际全量启动', timeout=180)
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
