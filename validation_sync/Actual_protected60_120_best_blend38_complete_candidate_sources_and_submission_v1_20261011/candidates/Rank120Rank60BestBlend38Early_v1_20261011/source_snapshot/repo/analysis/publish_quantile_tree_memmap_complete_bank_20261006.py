"""Publish the complete20 annual and4 final native scope plus repeated full future checks."""
from pathlib import Path
import hashlib
import json
import time

import publish_classifier_consensus_workflows_20261006 as helpers
from run_dependency_queue_v3_20261006 import owned
from hidden_windows_child_creation_20261006 import install

ROOT, A, sync = helpers.ROOT, helpers.A, helpers.sync
SOURCE = A / 'quantile_tree_memmap_complete_bank_20261006'
FUTURE = A / 'quantile_tree_memmap_future_qa_20261006'
SERVICE = A / 'service_owned_workflows_20261006/quantile_tree_memmap_complete_workflow'
OUT = A / 'quantile_tree_memmap_complete_bank_github_20261006'
PREFIX = Path('validation_sync/quantile_tree_memmap_complete_bank_20261006')


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
        proof = sync.read(FUTURE / 'verification.json')
        audit = sync.read(SOURCE / 'oof_audit.json')
        assert proof['status'] == audit['status'] == 'passed'
        assert audit['actual_annual_fits'] == audit['actual300_round_complete_models'] == 20
        assert proof['actual_full_final_fits'] == 4 and proof['new_native_fits_by_this_verifier'] == 0
        assert len(proof['checks']) == 4 and audit['new_quality_scores'] == proof['new_quality_scores'] == 0
        assert sync.read(SOURCE / 'training_execution_scope.json')['status'] == 'passed'
        assert sync.read(FUTURE / 'execution_scope.json')['status'] == 'passed'
        for filename, digest in proof['input_sha256'].items():
            assert sha(Path(filename)) == digest
        for check in proof['checks']:
            assert check['actual_final_training_rows'] == 6754006
            assert check['actual_native_boosting_iterations'] == 300 and check['actual_full_future_rows'] == 1599600
            assert check['actual_full_reload_and_native_cold80_bit_identical']
            assert sha(SOURCE / check['model'] / 'model_2025.joblib') == check['model_sha256']
            assert sha(FUTURE / (check['model'] + '_raw.parquet')) == check['raw_sha256']
    else:
        assert (SOURCE / 'training_execution_scope.json').exists() or terminal.get('failure')
    sources = [Path(__file__), A / 'mature_training_memmap_20261006.py',
        A / 'verify_full2025_quantile_memmap_capacity_20261006.py',
        A / 'train_quantile_tree_memmap_bank_20261006.py',
        A / 'run_quantile_tree_memmap_full_workflow_20261006.py',
        A / 'verify_quantile_tree_memmap_full_future_20261006.py',
        A / 'verify_mature_training_memmap_20261006.py', A / 'launch_service_owned_workflow_with_pwsh_20261006.py']
    sources += sorted(SOURCE.rglob('*.json')) + sorted(SOURCE.glob('*.jsonl'))
    sources += sorted(SOURCE.glob('*/raw_202*.parquet'))
    sources += sorted(FUTURE.glob('*.json')) + sorted(FUTURE.glob('*.jsonl')) + sorted(FUTURE.glob('*.parquet'))
    sources += sorted(SERVICE.glob('*.json')) + sorted(SERVICE.glob('*.log'))
    sources += sorted((A / 'quantile_tree_memmap_capacity_github_20261006').glob('*.json'))
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
            'all198_official_scores_full_scheme_causality_ranking_and_adoption_still_pending': True,
            'new_quality_scores': 0, 'physical_resource_boundary_established': False,
            'test_labels_read': False, 'only_publication_branch': 'main'})
        targets[(PREFIX / 'README.md').as_posix()] = (
            '# 分位数树完整原生范围与资源优化\n\n'
            '实际终态以service_execution和oof_audit、完整future QA及执行来源范围为准。'
            '完整2020–2024向前验证，四个固定分位数目标共20次300轮原生年度拟合，'
            '每个模型完整覆盖5635800行、1212日、4650股票，逐年成熟标签边界检查。'
            '全部原始矩阵、目标、键和成熟元数据与历史原记录逐字节一致。\n\n'
            '四个完整最终模型来自已经真实执行的6754006行300轮训练，来源和模型字节固定，'
            '复制模型文件没有计为新增拟合。年度训练全部结束后，又对四个模型独立重做全部1599600行未来X、'
            '实际重载、80日冷启动及131行树叶独立求和；无测试答案读取。'
            '每秒实际资源记录与完整原生输出保留。\n\n'
            '本批完成原生范围，完整198条方案官方评分、收益映射校准、方案冻结、'
            '完整因果与候选检查、全榜更新及采用仍待完成，零新增官方分数。'
            '没有修改原63特征、300轮、参数或先前被冻结的方案；实际资源测量支持采用磁盘映射的计算调度，'
            '不构成全局方向与资源耗尽结论。\n'
        ).encode('utf-8')
        for name, data in targets.items():
            sync.atomic(sync.WORKTREE / name, data)
        selected = sorted(targets)
        for offset in range(0, len(selected), 50):
            sync.git('add', '-f', '--', *selected[offset:offset + 50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(selected)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            '完成分位数树20年度及4最终原生模型和全部未来X复核并保留资源证据', timeout=180)
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
