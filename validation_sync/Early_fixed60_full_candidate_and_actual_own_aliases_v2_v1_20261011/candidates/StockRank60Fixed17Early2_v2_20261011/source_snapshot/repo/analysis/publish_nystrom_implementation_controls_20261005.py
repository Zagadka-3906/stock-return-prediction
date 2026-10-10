"""Archive completed Nyström implementation controls before R61 publication."""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
import sync_validated_rounds_github_20261005 as sync


def main():
    assert not (ROOT / 'results/optimization_20261003_r61.json').exists()
    assert not sync.git('status', '--porcelain', '--untracked-files=no')
    assert not sync.git('diff', '--cached', '--name-only')
    gates = [ROOT / 'analysis' / name for name in (
        'nystrom_ridge_bank_20261004/oof_audit.json',
        'nystrom_ridge_bank_20261004/training_execution_scope.json',
        'nystrom_ridge_future_models_qa_20261004/verification.json',
        'nystrom_ridge_complete_scheme_preflight_20261004/verification.json',
        'nystrom_future_codec_recovery_20261005/verification.json',
        'nystrom_evidence_audit_resume_20261005/verification.json',
        'nystrom_count_resume_20261005/verification.json')]
    assert all(sync.read(p)['status'] == 'passed' for p in gates)
    folders = (
        'nystrom_ridge_bank_20261004', 'nystrom_ridge_future_models_qa_20261004',
        'nystrom_ridge_complete_scheme_preflight_20261004', 'nystrom_future_codec_recovery_20261005',
        'nystrom_codec_queue_handoff_20261005', 'nystrom_evidence_audit_resume_20261005',
        'nystrom_count_resume_20261005', 'nystrom_ridge_scheme_count_metadata_audit_20261004')
    originals = {p for folder in folders for p in (ROOT / 'analysis' / folder).rglob('*.json')}
    originals.update(ROOT / 'analysis' / name for name in (
        'nystrom_ridge_resource_scope_audit_20261004.json',
        'nystrom_ridge_future_resource_scope_audit_20261004.json',
        'nystrom_future_codec_recovery_run_20261005.json'))
    originals.update(ROOT / 'analysis/run_logs' / name for name in (
        'nystrom_ridge_complete_scheme_run_restart_20261005.stderr.log',
        'nystrom_future_codec_recovery_20261005.stdout.log',
        'nystrom_future_codec_recovery_20261005.stderr.log'))
    prefix = Path('validation_sync/implementation_controls_nystrom_20261005')
    paths, bindings, assets = [], {}, []
    for original in sorted(originals):
        data = original.read_bytes()
        assert len(data) < 5 * 1024**2 and not sync.SECRET.search(data)
        destination = prefix / original.relative_to(ROOT)
        sync.atomic(sync.WORKTREE / destination, data)
        paths.append(destination.as_posix())
        bindings[str(original)] = sync.sha(data)
    for name in ('nystrom_future_codec_adapter_20261005.py', 'recover_nystrom_future_codec_20261005.py',
                 'run_nystrom_codec_locked_pipeline_20261005.py', 'handoff_nystrom_codec_queue_20261005.py',
                 Path(__file__).name):
        original = ROOT / 'analysis' / name
        destination = Path('analysis') / name
        data = original.read_bytes()
        sync.atomic(sync.WORKTREE / destination, data)
        paths.append(destination.as_posix())
        bindings[str(original)] = sync.sha(data)
    complete = ROOT / 'analysis/nystrom_ridge_complete_scheme_preflight_20261004'
    for label in ('role_baseline', 'standalone_baseline', 'role_changed', 'pure_changed'):
        candidate = complete / label / 'candidate'
        proof = sync.read(candidate / 'verification.json')
        assert sync.sha((candidate / 'submission.csv').read_bytes()) == proof['csv_sha256']
        assets.append({'case': label, 'csv_sha256': proof['csv_sha256'], 'rows': proof['rows'],
                       'days': proof['days'], 'codes': proof['codes'], 'local_path': str(candidate / 'submission.csv')})
    manifest = {'status': 'passed_implementation_controls_archived', 'at_local': sync.now(),
        'actual_annual_fits': 20, 'actual_fulltraining_native_models': 4,
        'actual_role_parameter_cases': 13, 'actual_standalone_parameter_cases': 4,
        'actual_fullfuture_cases': 4, 'new_quality_scores': 0, 'test_labels_read': False,
        'source_sha256': bindings, 'large_csv_assets': assets,
        'scope': 'Native training and complete-scheme implementation controls; R61-R63 actual predecessor quality comparisons remain in progress.'}
    sync.atomic(sync.WORKTREE / prefix / 'manifest.json', sync.encoded(manifest))
    paths.append((prefix / 'manifest.json').as_posix())
    readme = ('# Nyström新模型实现核验\n\n'
        '20次训练内部年度连续向前拟合、4个成熟全训练模型和4个完整未来候选案例均已通过核验。'
        '用途模型参数对照13例，独立主模型参数对照4例；保留原失败日志及两个已通过基线，'
        '通过独立版本适配器修复ridge_nystrom误入神经网络预测器的问题，补跑两项实际未来案例。\n\n'
        '本目录为实现核验，候选质量分仍待第61—63轮训练内部官方评分，未读取测试标签。'
        '大文件CSV与模型权重保留在本地D盘，哈希、参数、成熟训练范围及检查结果见manifest与原始JSON。\n')
    sync.atomic(sync.WORKTREE / prefix / 'README.md', readme.encode('utf-8'))
    paths.append((prefix / 'README.md').as_posix())
    for path, digest in bindings.items():
        assert sync.sha(Path(path).read_bytes()) == digest
    for offset in range(0, len(paths), 60):
        sync.git('add', '--', *paths[offset:offset + 60])
    assert set(sync.git('diff', '--cached', '--name-only').splitlines()) == set(paths)
    sync.git('commit', '-m', '归档Nyström二十次年度拟合、四完整候选核验及推理接口恢复证据')
    commit = sync.git('rev-parse', 'HEAD')
    sync.git('push', 'origin', f'HEAD:refs/heads/{sync.BRANCH}')
    assert sync.git('ls-remote', '--heads', 'origin', f'refs/heads/{sync.BRANCH}').split()[0] == commit
    receipt = {'status': 'pushed_and_remote_head_verified', 'at_local': sync.now(), 'commit': commit,
        'files': len(paths), 'url': f'https://github.com/Zagadka-3906/stock-return-prediction/tree/{sync.BRANCH}/{prefix.as_posix()}'}
    with (sync.OUT / 'nystrom_implementation_receipt.json').open('x', encoding='utf-8') as stream:
        json.dump(receipt, stream, ensure_ascii=False, indent=2)
    print(json.dumps(receipt, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
