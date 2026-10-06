"""Wait for the actual controller closure, then publish every control record on main."""
from pathlib import Path
import hashlib
import json
import time

import publish_classifier_consensus_workflows_20261006 as helpers
from run_dependency_queue_v3_20261006 import owned
from hidden_windows_child_creation_20261006 import install

ROOT, A, sync = helpers.ROOT, helpers.A, helpers.sync
SOURCE = A / 'mature_training_memmap_controls_20261006'
SERVICE = A / 'service_owned_workflows_20261006/mature_training_memmap_controls'
OUT = A / 'mature_training_memmap_controls_github_20261006'
PREFIX = Path('validation_sync/mature_training_memmap_controls_20261006')


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
    if terminal['status'] == 'passed':
        proof = sync.read(SOURCE / 'verification.json')
        assert proof['status'] == 'passed_actual_full_matrix_preparation_and_native_equivalence'
        assert proof['actual_largest_window_original_rows'] == 6754006
        assert proof['actual_full300_round_control_fits'] == 2
        assert proof['additional_actual48_round_control_fits'] == 8
        assert proof['actual_qualified_bank_annual_fits'] == proof['new_quality_scores'] == 0
        for filename, digest in proof['source_sha256'].items():
            assert sha(Path(filename)) == digest
        full = sync.read(SOURCE / 'full2020_native_equivalence.json')
        assert full['original_native_model_string_parameters_and_preprocessing_bit_identical']
        assert full['full_original2020_native_reload_bit_identical'] and full['actual_cold80_rows'] == 372000
    else:
        assert (SOURCE / 'failure.json').exists()
    sources = [Path(__file__), A / 'mature_training_memmap_20261006.py',
        A / 'verify_mature_training_memmap_20261006.py', A / 'launch_service_owned_workflow_with_pwsh_20261006.py']
    sources += sorted(SOURCE.glob('*.json')) + sorted(SOURCE.glob('*.jsonl'))
    sources += sorted(SERVICE.glob('*.json')) + sorted(SERVICE.glob('*.log'))
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
            'full2025_native300_round_fit_not_yet_measured': True,
            'complete_native24_fits_and198_official_scores_still_pending': True,
            'new_quality_scores': 0, 'physical_resource_boundary_established': False,
            'test_labels_read': False, 'only_publication_branch': 'main'})
        targets[(PREFIX / 'README.md').as_posix()] = (
            '# 完整训练窗口磁盘映射与原生等价控制\n\n'
            '本目录保留实际运行的全部控制记录与终态，成功或失败以service_execution和verification/failure为准。'
            '完整2025训练窗口的6754006行原63特征，按原日期和股票顺序写入D盘映射矩阵；'
            '全部原始矩阵、两种目标、键、标签成熟边界与既有完整训练记录逐字节核对。'
            '均值与标准差继续调用原始完整列算法，逐块标准化保持原始浮点计算顺序。\n\n'
            '四种分位数目标各执行一对65536行48轮原生等价控制；另以完整2020训练窗口执行两次300轮原生拟合，'
            '核对完整模型字符串、全部2020预测、实际重载及80日冷前缀。'
            '这些均为实现及资源控制，没有产生新的官方分数，未冒充已完成的20年度与4最终模型。\n\n'
            '每秒采集实际进程树内存和主机可用内存。最大2025窗口的完整300轮原生拟合尚未测量；'
            '14GiB是既有流程的调度规则，当前控制不修改旧来源、旧队列或既有选模标准，'
            '也不构成全局可行方向与资源边界结论。\n'
        ).encode('utf-8')
        for name, data in targets.items():
            sync.atomic(sync.WORKTREE / name, data)
        selected = sorted(targets)
        for offset in range(0, len(selected), 50):
            sync.git('add', '-f', '--', *selected[offset:offset + 50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(selected)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            '核验完整成熟训练矩阵磁盘映射及实际原生等价控制并保留资源记录', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        expected = {name: hashlib.sha256(data).hexdigest() for name, data in targets.items()}
        assert helpers.blob_hashes(commit, expected) == expected
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        helpers.verify_main(commit)
        helpers.watcher.advance_source_index(commit)
        create(OUT / 'receipt.json', {'status': 'pushed_actual_controls_main_only', 'control_status': terminal['status'],
            'at_local': sync.now(), 'commit': commit, 'raw_git_blobs_verified': len(expected), 'new_quality_scores': 0,
            'url': 'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/' + PREFIX.as_posix()})
        # The reload-only control is not used by any prospective full bank. Keep
        # its exact hash and control records, remove this one verified local file.
        if terminal['status'] == 'passed':
            model = Path(full['model_path']).resolve()
            assert model.parent == SOURCE.resolve() and model.name == 'full2020_memmap_reload_control.joblib'
            assert model.is_file() and sha(model) == full['model_file_sha256']
            size = model.stat().st_size
            model.unlink()
            create(OUT / 'control_model_cleanup.json', {'status': 'deleted_verified_reload_only_model_after_remote_main_verification',
                'path': str(model), 'bytes': size, 'sha256': full['model_file_sha256'],
                'records_retained': True, 'pending_full_matrix_dependencies_retained_on_D': True})
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
