"""Synchronize completed native robust fits and independent fullfuture controls."""
from pathlib import Path
import hashlib
import json
import time

import publish_classifier_consensus_workflows_20261006 as helpers

sync, ROOT, A = helpers.sync, helpers.ROOT, helpers.A
OUT = A / 'streaming_robust_full_completion_github_20261006'
PREFIX = Path('validation_sync/streaming_robust_full_completion_20261006')


def create(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    assert not OUT.exists()
    audit_folder = A / 'streaming_robust_full_completion_audit_20261006'
    proof = sync.read(audit_folder / 'verification.json')
    assert proof['status'] == 'passed_all24_actual_full32pass_native_fits_and4_independent_fullfuture_oracles'
    assert proof['actual_annual_fits'] == 20 and proof['actual_final_fits'] == 4
    assert proof['independent_future_rows_checked'] == 6398400
    assert proof['native_final_workflow_authoritatively_completed']
    assert proof['complete_official_quality_freeze_causality_candidate_inference_and_board_still_required']
    future = A / 'streaming_robust_regression_future_qa_20261005'
    bank = A / 'streaming_robust_regression_bank_20261005'
    recovered = A / 'system_reboot_workflow_recovery_20261006/robust_future'
    assert sync.read(future / 'verification.json')['status'] == 'passed'
    assert sync.read(recovered / 'execution.json')['status'] == 'passed'
    sources = [Path(__file__), A / 'audit_streaming_robust_final_model_20261006.py',
               A / 'audit_streaming_robust_full_completion_20261006.py',
               A / 'verify_streaming_robust_regression_full_future_20261005.py',
               bank / 'actual_native_fit_measurements.jsonl']
    sources += sorted(audit_folder.glob('*.json'))
    sources += sorted((A / 'streaming_robust_final_native_audit_20261006').rglob('*.json'))
    sources += sorted(future.glob('*.json')) + sorted(future.glob('*.jsonl'))
    sources += sorted(bank.glob('*/info_2025.json'))
    sources += sorted(recovered.rglob('*.json')) + sorted(recovered.rglob('*.jsonl'))
    targets = {(PREFIX / '.gitattributes').as_posix(): b'* -text\n'}
    files = {}
    for source in dict.fromkeys(sources):
        data = source.read_bytes()
        assert not sync.SECRET.search(data)
        if source.suffix == '.json':
            json.loads(data.decode('utf-8-sig'))
        elif source.suffix == '.jsonl':
            for line in data.splitlines():
                if line:
                    json.loads(line)
        destination = source.relative_to(ROOT) if source.parent == A and source.suffix == '.py' else PREFIX / source.relative_to(A)
        name = destination.as_posix()
        targets[name] = data
        files[source.relative_to(ROOT).as_posix()] = {'published_path': name,
            'raw_sha256': hashlib.sha256(data).hexdigest()}
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
        old = sync.git('rev-parse', 'HEAD')
        helpers.verify_main(old)
        assert not sync.git('status', '--porcelain')
        targets[(PREFIX / 'manifest.json').as_posix()] = sync.encoded({
            'status': 'actual20_annual4_final_robust_native_fits_and_full_independent_oracles_published',
            'at_local': sync.now(), 'previous_main': old, 'files': files,
            'actual_annual_fits': 20, 'actual_final_fits': 4, 'full_data_passes_each_fit': 32,
            'future_rows_per_model': 1599600, 'future_days': 344, 'future_codes': 4650,
            'independent_full_future_rows_checked': 6398400,
            'maximum_native_oracle_error': proof['maximum_independent_fullfuture_oracle_error'],
            'all4_full_reload_real_cold80_and_native_prefix_controls_passed': True,
            'full_official_quality_freeze_causality_candidates_and_board_still_required': True,
            'physical_resource_boundary_established': False,
            'new_native_fits_by_publication': 0, 'new_quality_scores_by_publication': 0,
            'only_publication_branch': 'main', 'test_labels_read': False})
        targets[(PREFIX / 'README.md').as_posix()] = (
            '# 四种稳健回归的完整原生训练与预测核验\n\n'
            '排名、收益率目标与平方误差、Huber损失组成4种配置。'
            '20次年度训练和4次最终全量训练全部完成，每次实际完整遍历训练数据32遍。'
            '每份最终模型使用6,754,006条成熟历史记录，估计器样本计数为216,128,193。\n\n'
            '四份最终预测各覆盖1,599,600行、344天和4,650只股票，保存重载、'
            '真实前80天推理和固定行前缀检查均通过。独立逐行调用原生SGDRegressor.predict，'
            '核验全部6,398,400个输出，同时核验无效价格哨兵、目标单位及成熟历史缩放。'
            '全部协议、源码、模型与预测SHA256绑定再次完整复核；原生工作进程已正常完成。\n\n'
            '记录和证据已同步main。后续83—84轮将比较完整集成角色、主模型及后处理，'
            '仍需官方评分、收益率映射、冻结选择、完整因果检查、候选推理和完整榜更新。'
            '此次原生验证没有产生新官方分数，也没有证明全局计算资源边界已经达到。\n'
        ).encode('utf-8')
        for name, data in targets.items():
            assert not sync.SECRET.search(data)
            sync.atomic(sync.WORKTREE / name, data)
        selected = sorted(targets)
        for offset in range(0, len(selected), 50):
            sync.git('add', '-f', '--', *selected[offset:offset + 50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(selected)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
                 '完成稳健回归20次年度与4次最终训练及6398400个原生输出独立核验', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        expected = {name: hashlib.sha256(data).hexdigest() for name, data in targets.items()}
        assert helpers.blob_hashes(commit, expected) == expected
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        helpers.verify_main(commit)
        helpers.watcher.advance_source_index(commit)
        receipt = {'status': 'pushed_verified_all24_robust_native_fits_and_fullfuture_oracles_main_only',
            'at_local': sync.now(), 'commit': commit, 'raw_git_blobs_verified': len(expected),
            'url': 'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/' + PREFIX.as_posix()}
        create(OUT / 'receipt.json', receipt)
        print(json.dumps(receipt, ensure_ascii=False), flush=True)
    except BaseException as error:
        create(OUT / 'failure.json', {'status': 'failed_preserved_publication_attempt',
            'at_local': sync.now(), 'error': f'{type(error).__name__}: {error}'})
        raise
    finally:
        for process in reversed(suspended):
            if process.is_running():
                process.resume()


if __name__ == '__main__':
    main()
