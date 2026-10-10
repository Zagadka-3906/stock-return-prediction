"""Publish actual largest native fits and every full future control on main."""
from pathlib import Path
import hashlib
import json
import time

import publish_classifier_consensus_workflows_20261006 as helpers
from run_dependency_queue_v3_20261006 import owned
from hidden_windows_child_creation_20261006 import install

ROOT, A, sync = helpers.ROOT, helpers.A, helpers.sync
SOURCE = A / 'quantile_tree_memmap_capacity_20261006'
SERVICE = A / 'service_owned_workflows_20261006/quantile_tree_memmap_capacity'
OUT = A / 'quantile_tree_memmap_capacity_github_20261006'
PREFIX = Path('validation_sync/quantile_tree_memmap_capacity_20261006')


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
        assert proof['status'] == 'passed_actual_four_largest_full_native_fits_and_complete_future_controls'
        assert proof['actual_full_final_fits'] == proof['actual300_iteration_models'] == 4
        assert proof['actual_annual_fits'] == proof['new_quality_scores'] == 0
        assert len(proof['checks']) == 4
        for filename, digest in proof['input_sha256'].items():
            assert sha(Path(filename)) == digest
        for check in proof['checks']:
            assert check['actual_full_training_rows'] == 6754006
            assert check['actual_native_iterations'] == 300 and check['actual_full_future_rows'] == 1599600
            assert check['actual_full_reload_cold80_and37day_prefix_bit_identical']
            folder = SOURCE / check['model']
            assert sha(folder / 'model_2025.joblib') == check['model_sha256']
            assert sha(folder / 'future_raw.parquet') == check['raw_parquet_sha256']
    else:
        assert (SOURCE / 'failure.json').exists()
    sources = [Path(__file__), A / 'mature_training_memmap_20261006.py',
        A / 'verify_full2025_quantile_memmap_capacity_20261006.py',
        A / 'verify_mature_training_memmap_20261006.py', A / 'launch_service_owned_workflow_with_pwsh_20261006.py']
    sources += sorted(SOURCE.rglob('*.json')) + sorted(SOURCE.glob('*.jsonl'))
    sources += sorted(SOURCE.glob('*/future_raw.parquet'))
    sources += sorted(SERVICE.glob('*.json')) + sorted(SERVICE.glob('*.log'))
    sources += sorted((A / 'mature_training_memmap_controls_github_20261006').glob('*.json'))
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
            'actual_full2025_native_capacity_status': terminal['status'],
            'all20_annual_fits_and198_official_scores_and_native_bank_promotion_still_pending': True,
            'new_quality_scores': 0, 'physical_resource_boundary_established': False,
            'test_labels_read': False, 'only_publication_branch': 'main'})
        targets[(PREFIX / 'README.md').as_posix()] = (
            '# 实际最大窗口分位数原生拟合与完整未来X检查\n\n'
            '成功或失败以实际service_execution和verification/failure为准。四个固定分位数目标，'
            '分别在原6754006行、63特征、完整标签成熟窗口上训练300轮；不抽样、不减少特征、不提前停止。'
            '磁盘映射的全部原矩阵、目标、键和成熟元数据与历史原生记录逐字节一致；'
            '完整列均值和标准差沿用原算法，完整2020窗口300轮模型字符串与原实现逐字一致。\n\n'
            '每个模型拟合结束后才读取未来X，检查完整1599600行、344日、4650股票，'
            '实际重载、80日和37日前缀逐位一致，并以131行独立树叶求和检查原生预测。'
            '模型和原生未来预测按冻结参数执行，无测试标签读取。完整未来预测及全部来源、分数占位和资源记录保留。\n\n'
            '本批只有四个完整最终原生模型；完整20年度向前拟合、198条官方完整方案评分、'
            '采用与既有全量队列仍待完成。该批没有新增官方分数，未宣称已完成全局资源边界。'
            '原模型实现、14GiB调度规则及原始队列保持原记录；测量用于下一版实际资源调度的依据。\n'
        ).encode('utf-8')
        for name, data in targets.items():
            sync.atomic(sync.WORKTREE / name, data)
        selected = sorted(targets)
        for offset in range(0, len(selected), 50):
            sync.git('add', '-f', '--', *selected[offset:offset + 50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(selected)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            '验证四个完整最大窗口分位数原生模型及全部未来X预测和实际资源', timeout=180)
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
