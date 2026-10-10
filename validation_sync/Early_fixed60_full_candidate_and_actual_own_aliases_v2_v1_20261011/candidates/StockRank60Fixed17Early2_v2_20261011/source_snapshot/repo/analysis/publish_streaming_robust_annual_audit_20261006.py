"""Publish actual annual fits and independent inspection without releasing quality."""
from pathlib import Path
import hashlib
import json
import time

import publish_classifier_consensus_workflows_20261006 as helpers

sync, ROOT, A = helpers.sync, helpers.ROOT, helpers.A
OUT = A / 'streaming_robust_annual_github_20261006'
PREFIX = Path('validation_sync/streaming_robust_annual_audit_20261006')
BANK = A / 'streaming_robust_regression_bank_20261005'
AUDIT = A / 'streaming_robust_actual_annual_completion_audit_20261006'
RECOVERY = A / 'system_reboot_workflow_recovery_20261006/robust_annual'


def create(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    assert not OUT.exists()
    inspection = sync.read(AUDIT / 'verification.json')
    assert inspection['status'] == 'passed_actual20_full32pass_robust_annual_models_independently_inspected'
    assert inspection['actual_full_annual_fits'] == 20
    assert sync.read(BANK / 'oof_audit.json')['status'] == 'passed'
    assert sync.read(BANK / 'training_execution_scope.json')['status'] == 'passed'
    assert sync.read(RECOVERY / 'execution.json')['status'] == 'passed'
    measurements_path = BANK / 'actual_native_fit_measurements.jsonl'
    measurements_data = measurements_path.read_bytes()
    measurements = [json.loads(line) for line in measurements_data.splitlines() if line]
    annual_measurements = [row for row in measurements if row['year'] in range(2020, 2025)]
    assert len(annual_measurements) == 20
    actual = {(row['model'], row['year']): row for row in annual_measurements}
    assert len(actual) == 20
    for check in inspection['checks']:
        row = actual[(check['model'], check['year'])]
        assert row['status'] == 'completed_full_original32passes'
        assert row['actual_completed_epochs'] == 32
        assert row['actual_training_rows'] == check['mature_training_rows']
        assert row['actual_native_sample_counter'] == check['actual32pass_counter']
        assert row['actual_partial_fit_calls'] == check['actual_partial_fit_calls']
        assert row['actual_rows_in_each_epoch'] == [check['mature_training_rows']] * 32

    paths = [Path(__file__), A / 'audit_streaming_robust_annual_completion_20261006.py',
             A / 'streaming_robust_regression_20261005.py',
             A / 'train_streaming_robust_regression_bank_20261005.py',
             A / 'run_streaming_robust_regression_bank_20261005.py',
             A / 'verify_streaming_robust_regression_full_future_20261005.py',
             A / 'streaming_robust_regression_bank_run_20261005.json']
    paths += sorted(BANK.rglob('*.json'))
    paths += sorted(AUDIT.glob('*.json'))
    paths += sorted(RECOVERY.glob('*.json'))
    paths += sorted((RECOVERY / 'resources').glob('*.json'))
    paths += sorted((RECOVERY / 'resources').glob('*.jsonl'))
    window_path = A / 'terminal_window_status_20261006_012126.json'
    window = sync.read(window_path)
    assert window['remaining_visible_project_windows'] == 0
    assert window['processes_stopped_or_restarted'] == 0
    paths.append(window_path)
    targets = {(PREFIX / '.gitattributes').as_posix(): b'* -text\n'}
    bindings = {}
    for path in dict.fromkeys(paths):
        data = path.read_bytes()
        assert not sync.SECRET.search(data)
        if path.suffix == '.json':
            json.loads(data.decode('utf-8-sig'))
        if path.suffix == '.jsonl':
            for line in data.splitlines():
                if line:
                    json.loads(line)
        destination = path.relative_to(ROOT) if path.parent == A and path.suffix == '.py' else PREFIX / path.relative_to(A)
        name = destination.as_posix()
        targets[name] = data
        bindings[path.relative_to(ROOT).as_posix()] = {'published_path': name,
            'raw_sha256': hashlib.sha256(data).hexdigest()}
    targets[(PREFIX / 'actual20_annual_fit_measurements.json').as_posix()] = sync.encoded({
        'status': 'all20_actual_completed_full32pass_annual_fits',
        'journal_snapshot_sha256': hashlib.sha256(measurements_data).hexdigest(),
        'records': annual_measurements,
        'ongoing_final_fits_excluded_from_annual_count': True})

    plan = sync.read(helpers.HANDOFF / 'queue_plan.json')
    pairs = [helpers.owned_pair(plan['preserved_active_jobs'][name]['pid'],
             Path(plan['preserved_active_jobs'][name]['script']),
             plan['preserved_active_jobs'][name]['script_args'])
             for name in ('main_publisher', 'progress_monitor')]
    OUT.mkdir()
    suspended = []
    try:
        for _ in range(30):
            for parent, worker in pairs:
                for process in (worker, parent):
                    process.suspend()
                    suspended.append(process)
            busy = [process for parent, worker in pairs for process in parent.children(recursive=True)
                    if process.pid != worker.pid and process.name().lower() != 'conhost.exe']
            if not busy:
                break
            for process in reversed(suspended):
                process.resume()
            suspended.clear()
            time.sleep(.2)
        else:
            raise RuntimeError('Existing publication child still active.')
        previous = sync.git('rev-parse', 'HEAD')
        helpers.verify_main(previous)
        assert not sync.git('status', '--porcelain')
        targets[(PREFIX / 'manifest.json').as_posix()] = sync.encoded({
            'status': 'actual20_annual_fits_and_independent_native_audit_completed',
            'at_local': sync.now(), 'previous_main': previous, 'files': bindings,
            'actual_completed_annual_fits': 20, 'epochs_each': 32,
            'same_validation_rows_each_configuration': 5635800,
            'same_validation_days_each_configuration': 1212,
            'maximum_independent_native_oracle_error': max(
                row['independent_SGDRegressor_predict_max_abs_error'] for row in inspection['checks']),
            'actual_full_rehash_model_counters_scaling_and_validation_keys_verified': True,
            'final4_fits_fullfuture_and_official_quality_still_required': True,
            'no_promotion_to_qualified_quality_board': True,
            'visible_project_terminal_windows_at_recheck': 0,
            'only_publication_branch': 'main', 'test_labels_read': False,
            'new_native_fits_by_publication': 0, 'new_quality_scores_by_publication': 0})
        targets[(PREFIX / 'README.md').as_posix()] = (
            '# 四种稳健回归的完整年度训练与独立复核\n\n'
            '排名和收益率目标分别训练平方误差、Huber损失，共4种模型、'
            '20次实际年度训练，每次完整遍历成熟历史训练数据32遍。'
            '独立检查了实际估计器样本计数、物理批次数、63个特征、'
            '成熟标签截止日期及目标均值标准差的逆变换。\n\n'
            '每种模型均覆盖同一5,635,800行、1,212天年度验证数据。'
            '全部20份年度预测的键、有限值、保存重载及真实前80天检查通过。'
            '独立调用SGDRegressor.predict核验，最大绝对误差为1.32e-16。'
            '源码、协议、模型和年度预测SHA256记录、资源记录及复核证据均保留。\n\n'
            '4次最终全量训练正在执行，后续还需要完整未来推理、官方评分、'
            '冻结选择、因果检查与完整榜更新。此次同步没有产生新官方分数或替换最佳方案。'
            '后台弹窗启动方式已修正；01:21复查可见项目终端为0，未停止训练。\n'
        ).encode('utf-8')
        for name, data in targets.items():
            assert not sync.SECRET.search(data)
            sync.atomic(sync.WORKTREE / name, data)
        paths_to_stage = sorted(targets)
        for offset in range(0, len(paths_to_stage), 50):
            sync.git('add', '-f', '--', *paths_to_stage[offset:offset + 50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(paths_to_stage)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
                 '完成四种稳健回归20次年度训练并独立核验实际32遍计数与预测', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        expected = {name: hashlib.sha256(data).hexdigest() for name, data in targets.items()}
        assert helpers.blob_hashes(commit, expected) == expected
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        helpers.verify_main(commit)
        helpers.watcher.advance_source_index(commit)
        receipt = {'status': 'pushed_verified_actual20_robust_annual_fits_and_native_audit_main_only',
            'at_local': sync.now(), 'commit': commit, 'raw_git_blobs_verified': len(expected),
            'url': 'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/' + PREFIX.as_posix()}
        create(OUT / 'receipt.json', receipt)
        print(json.dumps(receipt, ensure_ascii=False), flush=True)
    except BaseException as error:
        create(OUT / 'failure.json', {'status': 'failed_publication_attempt',
            'at_local': sync.now(), 'error': f'{type(error).__name__}: {error}'})
        raise
    finally:
        for process in reversed(suspended):
            if process.is_running():
                process.resume()


if __name__ == '__main__':
    main()
