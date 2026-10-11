"""Publish actual controller wiring and observed complete native scope progress on main."""
from pathlib import Path
import hashlib
import json
import time

import publish_classifier_consensus_workflows_20261006 as helpers
from run_dependency_queue_v3_20261006 import owned
from hidden_windows_child_creation_20261006 import install

ROOT, A, sync = helpers.ROOT, helpers.A, helpers.sync
SOURCE = A / 'quantile_tree_memmap_controller_wiring_20261006'
SERVICE = A / 'service_owned_workflows_20261006/quantile_tree_memmap_controller_wiring'
OUT = A / 'quantile_tree_memmap_controller_wiring_github_20261006'
PREFIX = Path('validation_sync/quantile_tree_memmap_controller_wiring_20261006')


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
    while not (SERVICE / 'service_execution.json').exists():
        if (SERVICE / 'native_launch.json').exists():
            assert owned(sync.read(SERVICE / 'native_launch.json')), 'Actual controls are missing without a terminal record.'
        time.sleep(10)
    terminal = sync.read(SERVICE / 'service_execution.json')
    row = sync.read(SERVICE / 'native_launch.json')
    while owned(row):
        time.sleep(.2)
    assert terminal['status'] == 'passed'
    proof = sync.read(SOURCE / 'verification.json')
    assert proof['status'] == 'passed_actual_owned_native_and_preserved198_queue_wiring_controls'
    assert proof['observed_actual_completed_annual_models'] and proof['new_quality_scores'] == 0
    for filename, digest in proof['original_scientific_source_hashes_all_preserved'].items():
        assert sha(Path(filename)) == digest
    for row in proof['new_full_native_and_promotion_and198_quality_controllers_actual_owned'].values():
        assert owned(row)
    sources = [Path(__file__), A / 'verify_quantile_memmap_controller_wiring_20261006.py',
        A / 'run_quantile_tree_quality_queue_v2_20261006.py', A / 'promote_quantile_memmap_native_bank_20261006.py',
        A / 'monitor_actual_optimization_progress_v22_20261006.py',
        A / 'train_quantile_tree_memmap_bank_20261006.py', A / 'run_quantile_tree_memmap_full_workflow_20261006.py',
        A / 'verify_quantile_tree_memmap_full_future_20261006.py', A / 'mature_training_memmap_20261006.py',
        A / 'publish_quantile_tree_memmap_complete_bank_20261006.py', A / 'progress_monitor_v22_handoff_recovery_20261006.json',
        A / 'quantile_tree_quality_queue_v2_20261006/plan.json', A / 'quantile_tree_quality_queue_v2_20261006/state.json']
    sources += sorted(SOURCE.glob('*.json'))
    sources += sorted((A / 'quantile_tree_memmap_complete_bank_20261006').glob('*.json'))
    sources += sorted((A / 'quantile_tree_memmap_complete_bank_20261006').glob('*/info_*.json'))
    sources += sorted((A / 'quantile_tree_memmap_capacity_github_20261006').glob('*.json'))
    for name in ('quantile_tree_memmap_controller_wiring', 'quantile_tree_memmap_complete_workflow',
                 'quantile_tree_memmap_complete_publication', 'quantile_tree_quality_queue_v2',
                 'quantile_tree_memmap_native_promotion', 'progress_monitor_v22'):
        folder = A / 'service_owned_workflows_20261006' / name
        sources += sorted(folder.glob('*.json'))
    targets = {(PREFIX / '.gitattributes').as_posix(): b'* -text\n'}
    files = {}
    for source in dict.fromkeys(sources):
        data = source.read_bytes()
        assert not sync.SECRET.search(data)
        destination = source.relative_to(ROOT) if source.parent == A and source.suffix == '.py' else PREFIX / source.relative_to(A)
        targets[destination.as_posix()] = data
        files[source.relative_to(ROOT).as_posix()] = {'published_path': destination.as_posix(), 'raw_sha256': hashlib.sha256(data).hexdigest()}
    restore, suspended = install(), []
    try:
        pub = sync.read(A / 'service_owned_workflows_20261006/main_publisher_v5/native_launch.json')
        assert owned(pub)
        root, worker = helpers.owned_pair(pub['pid'], Path(pub['script']), pub['script_args'])
        assert worker.pid == pub['owned_worker_pid'] and worker.create_time() == pub['owned_worker_creation_time']
        for attempt in range(50):
            for process in (worker, root):
                process.suspend()
                suspended.append(process)
            busy = [p for p in root.children(recursive=True) if p.pid != worker.pid and p.name().lower() != 'conhost.exe']
            if not busy:
                break
            for process in reversed(suspended):
                process.resume()
            suspended.clear()
            time.sleep(.2)
        else:
            raise RuntimeError('Main publisher still owns an active publication child.')
        previous = sync.git('rev-parse', 'HEAD')
        helpers.verify_main(previous)
        assert not sync.git('status', '--porcelain')
        targets[(PREFIX / 'manifest.json').as_posix()] = sync.encoded({
            'status': terminal['status'], 'at_local': sync.now(), 'files': files, 'previous_main': previous,
            'entire_actual_control_execution_preserved': True,
            'actual_controller_wiring_control_status': terminal['status'],
            'complete20_annual_closure_native_promotion_and198_quality_still_pending': True,
            'new_quality_scores': 0, 'physical_resource_boundary_established': False,
            'test_labels_read': False, 'only_publication_branch': 'main'})
        targets[(PREFIX / 'README.md').as_posix()] = (
            '# 完整原生范围接入既定198方案评分队列\n\n'
            '四个最大6754006行窗口的300轮原生模型及全部未来X检查已真实通过，'
            '完整20次年度向前拟合正在进行，本目录快照只报告已经保存且通过原数据哈希和模型重载检查的年度模型。'
            '全量完成后，接入程序要求实际服务关闭、20年度和4最终原生范围、完整未来复核及main回执，'
            '才允许暴露与既有科学代码匹配的模型字节。复制模型不计为新增拟合。\n\n'
            'R91/R92仍是原定100/98条，比较基准仍是合格R90/R91。全部原科学代码SHA保持一致，'
            '全量冻结、官方评分、因果、候选和全部榜单检查保留；与原队列共享单个实际评分窗口。'
            '接入程序只替换尚未执行任何拟合或评分的等待控制器，原记录保留，不伪造旧控制器通过。\n\n'
            '新队列、接入器和观察器的实际PID、出生时间、命令与无窗口启动已检查。'
            '监控按模型、年份和字节去重，反映正在执行的磁盘映射范围。切换时误要求已经正常结束的控制器仍存活的'
            '断言已如实保留并纠正，原训练和评分没有停止。完整20年度、接入和198评分尚未完成，'
            '没有新增官方分数或全局资源耗尽结论。\n'
        ).encode('utf-8')
        for name, data in targets.items():
            sync.atomic(sync.WORKTREE / name, data)
        selected = sorted(targets)
        for offset in range(0, len(selected), 50):
            sync.git('add', '-f', '--', *selected[offset:offset + 50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(selected)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            '核验完整原生范围接入198方案队列及实际训练进度与去重监控', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        expected = {name: hashlib.sha256(data).hexdigest() for name, data in targets.items()}
        assert helpers.blob_hashes(commit, expected) == expected
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        helpers.verify_main(commit)
        helpers.watcher.advance_source_index(commit)
        create(OUT / 'receipt.json', {'status': 'pushed_actual_controls_main_only', 'control_status': terminal['status'],
            'at_local': sync.now(), 'commit': commit, 'raw_git_blobs_verified': len(expected), 'new_quality_scores': 0,
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
