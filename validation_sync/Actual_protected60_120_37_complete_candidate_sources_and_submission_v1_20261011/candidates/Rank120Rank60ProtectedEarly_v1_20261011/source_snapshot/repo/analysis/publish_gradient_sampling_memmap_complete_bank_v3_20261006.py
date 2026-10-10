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
SOURCE = A / 'gradient_sampling_memmap_complete_bank_v3_20261006'
OUT = A / 'gradient_sampling_memmap_complete_bank_v3_github_20261006'
PREFIX = Path('validation_sync/gradient_sampling_memmap_complete_bank_v3_20261006')


def create(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    service = A / 'service_owned_workflows_20261006/gradient_sampling_memmap_complete_workflow_v3'
    while not (service / 'service_execution.json').exists():
        assert owned(sync.read(service / 'native_launch.json')), 'Full native worker disappeared without terminal evidence.'
        time.sleep(10.)
    assert sync.read(service / 'service_execution.json')['status'] == 'passed'
    while owned(sync.read(service / 'native_launch.json')):
        time.sleep(.2)
    assert not OUT.exists()
    OUT.mkdir()
    future = A / 'gradient_sampling_memmap_future_qa_v3_20261006'
    proof, future_proof = sync.read(SOURCE / 'oof_audit.json'), sync.read(future / 'verification.json')
    assert proof['status'] == future_proof['status'] == 'passed'
    assert proof['actual_annual_fits'] == proof['actual300_round_complete_models'] == len(proof['checks']) == 30
    assert future_proof['actual_full_final_fits'] == len(future_proof['checks']) == 6
    assert future_proof['new_native_fits_by_this_verifier'] == 0
    assert sync.read(SOURCE / 'training_execution_scope.json')['status'] == sync.read(future / 'execution_scope.json')['status'] == 'passed'
    holds = list(SOURCE.glob('scheduler_fit_hold_*/released.json'))
    assert len(holds) == 30 and all(sync.read(p)['scientific_workers_touched'] == 0 for p in holds)
    assert all(sync.read(p.parent / 'independent_guard_service/service_execution.json')['status'] == 'passed' for p in holds)
    for model, cfg in proof['configurations'].items():
        assert proof['entire_original_five_year_prediction_coverage'][model]['rows'] == 5635800
        for year in range(2020, 2026):
            info = sync.read(SOURCE / model / f'info_{year}.json')
            assert info['status'] == 'passed' and info['configuration'] == cfg
            assert info['actual_native_boosting_iterations'] == 300
            assert sha(SOURCE / model / f'model_{year}.joblib') == info['model_sha256']
            label = 'rank' if cfg['target'] == 'y_rank' else 'return'
            assert info['training_meta'] == sync.read(A / f'linear_bank_20261003/{label}_ridge_l01/info_{year}.json')['training_meta']
            if year < 2025:
                assert sha(SOURCE / model / f'raw_{year}.parquet') == info['prediction_sha256']
            else:
                assert info['copied_file_is_not_an_additional_native_fit']
    for check in future_proof['checks']:
        assert check['actual_full1599600_row_reload_bit_identical'] and check['actual_cold80_day_prefix_bit_identical']
        assert check['source_capacity_predictions_bit_identical_all1599600_rows']
        assert sha(future / f"{check['model']}_raw.parquet") == check['raw_sha256']
    protocol = sync.read(SOURCE / 'protocol.json')
    for path, digest in protocol['input_sha256'].items():
        assert sha(path) == digest
    resources = sync.read(SOURCE / 'resource_summary.json')
    assert resources['status'] == 'passed' and not resources['observation_errors']
    actual_completed = list(proof['configurations'])
    sources = [Path(__file__), *[A / name for name in (
        'train_gradient_sampling_memmap_bank_v3_20261006.py', 'run_gradient_sampling_memmap_full_workflow_v3_20261006.py',
        'verify_gradient_sampling_memmap_full_future_v3_20261006.py', 'gradient_sampling_exact_memmap_20261006.py',
        'owned_scheduler_native_fit_hold_v2_20261006.py', 'watch_owned_scheduler_fit_lease_20261006.py',
        'independent_gradient_sampling_native_codec_20261006.py', 'gradient_sampling_pilot_cache_cleanup_20261006.json')]]
    for folder in (SOURCE, future, service):
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
            'status': 'passed_original30_annual6_final_native_scope_and_full_future_controls',
            'at_local': sync.now(), 'files': files, 'previous_main': previous,
            'entire_actual_control_execution_preserved': True,
            'actual_complete_annual_native_fits': 30, 'actual_final_native_fits': 6, 'new_native_fits_by_publication': 0,
            'original_full_native_scope_complete': True, 'original262_quality_records_still_required': True,
            'actual_completed_full_capacity_models_at_observation': actual_completed,
            'full_workflow_native_terminal_and_future_execution_scopes_verified': True,
            'new_quality_scores': 0, 'physical_resource_boundary_established': False,
            'test_labels_read': False, 'only_publication_branch': 'main'})
        targets[(PREFIX / 'README.md').as_posix()] = '# GOSS原定30个年度模型、6个最终模型与完整推理验证完成\n\n原六套配置在2020—2024年的全部成熟窗口实际完成30个300轮模型。63特征、原样本、目标、成熟边界与矩阵哈希均保持一致，五年逐配置覆盖5,635,800行、1,212日、4,650股票。逐模型执行原未来标签扰动控制、全年度重载、独立解码、真实80日及37日冷启动检查；小样本控制拟合不计作30个年度模型。\n\n最终6个模型复用此前实际完成的6,754,006行300轮拟合及模型字符串证明，复制不计新拟合。全部1,599,600行、344日、4,650股票未来输入再次核对原预测、重载、独立解码、80日和37日冷启动，且与原最大窗口推理结果全部一致。模型权重保留于D待评分及候选使用，仅上传源码、元数据、完整验证及实际资源记录。\n\n全部30次临时调度保护已释放，独立守护服务正常结束。已完成、主分支已存档的小样本重复缓存按原SHA核验后删除47.25 MiB，共享完整训练缓冲区与待办模型保留。\n\n这次完成的是原生模型和推理范围，第75/76轮124+138共262个完整方案的官方评分、选模冻结、因果检查、候选推理及完整榜仍待执行。后续暴露旧质量路径和接管原待办需另行核验；不读取TestY，不宣布全局优化完成或物理资源上限。所有记录仅上传main。\n'.encode('utf-8')
        for name, data in targets.items():
            sync.atomic(sync.WORKTREE / name, data)
        selected = sorted(targets)
        for offset in range(0, len(selected), 50):
            sync.git('add', '-f', '--', *selected[offset:offset + 50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(selected)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            '完成并核验GOSS全部30个年度模型6个最终模型及完整未来输入控制', timeout=180)
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
