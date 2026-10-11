"""Publish actual classifier controls and cleanup recheck to main with raw-byte checks."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import time
import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
import watch_validations_main_v2_20261005 as watcher
from finalize_main_branch_consolidation_20261005 import owned_pair, verify_main
from publish_main_closeout_v2_20261005 import names, blob_hashes
sync = watcher.sync
PREFIX = Path('validation_sync/ready_robust_reference_workflows_20261005')
OUT = A / 'ready_robust_reference_workflows_github_20261005'


def file_sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()


def main():
    assert not (OUT / 'receipt.json').exists(), 'Preserve the completed publication.'
    folders = (
        'ready_robust_reference_generator_preflight_20261005',
        'ready_robust_reference_execution_preflight_20261005',
        'ready_robust_reference_quality_followups_20261005',
        'gap_aware_optimization_monitor_handoff_v18_20261005',
        'streaming_robust_regression_preflight_20261005',
        'streaming_robust_regression_followups_20261005',
        'streaming_classifier_actual_final_completion_audit_20261005',
        'streaming_robust_regression_direct_router_preflight_20261005',
    )
    proofs = [A / folder / 'verification.json' for folder in folders]
    for path in proofs:
        proof = sync.read(path)
        assert proof['status'].startswith('passed'), path
        for source, digest in proof.get('source_sha256', {}).items():
            assert file_sha(Path(source)) == digest, source
    assert [r['generated_records'] for r in sync.read(proofs[0])['controls']] == [100, 98, 98]
    pilot = sync.read(proofs[4])
    assert pilot['actual_small32pass_fits'] == 16 and pilot['actual_full_annual_fits'] == 0
    native = sync.read(proofs[5])
    assert native['expected_full_annual_fits'] == 20 and native['expected_full_final_fits'] == 4
    final = sync.read(proofs[6])
    assert final['actual_full_final_fits_independently_inspected'] == 4
    owned = []
    for job in sync.read(proofs[2])['quality_rounds']:
        process = psutil.Process(job['owned_worker_pid'])
        assert process.create_time() == job['owned_worker_creation_time']
        assert process.cmdline()[-2:] == job['script_args']
        assert not Path(job['stderr']).read_bytes()
        owned.append({'round': job['round'], 'pid': process.pid,
                      'creation_time': process.create_time(),
                      'explicit_parent_round': job['explicit_parent_round'], 'owned_live': True})
    launch = sync.read(sync.OUT / 'launch_v3.json')['publisher']
    publisher = owned_pair(launch['pid'], Path(launch['script']), launch['script_args'])
    assert publisher[1].pid == sync.read(sync.OUT / 'owner.lock')['pid']
    launch = sync.read(A / 'actual_optimization_monitor_launch_v18_20261005.json')
    monitor = owned_pair(launch['pid'], Path(launch['script']), launch['script_args'])
    original_git = sync.git

    def bounded_git(*args, **kwargs):
        if args and args[0] == 'ls-remote':
            kwargs['timeout'] = 25
            for attempt in range(3):
                try:
                    return original_git(*args, **kwargs)
                except (subprocess.TimeoutExpired, RuntimeError):
                    if attempt == 2:
                        raise
                    time.sleep(2)
        return original_git(*args, **kwargs)

    sync.git = bounded_git
    suspended = []
    try:
        for attempt in range(12):
            for parent, child in (publisher, monitor):
                for process in (child, parent):
                    process.suspend()
                    suspended.append(process)
            busy = [p for parent, child in (publisher, monitor) for p in parent.children(recursive=True)
                    if p.pid != child.pid and p.name().lower() != 'conhost.exe']
            if not busy:
                break
            for process in reversed(suspended):
                process.resume()
            suspended.clear()
            time.sleep(1)
        else:
            raise RuntimeError('Owned publisher or observer has an active command.')
        previous = sync.git('rev-parse', 'HEAD')
        old_heads = verify_main(previous)
        assert not sync.git('status', '--porcelain')
        selected = names('ls-files', '--modified') | names('ls-files', '--others', '--exclude-standard')
        evidence = set()
        for folder_name in folders:
            evidence.update(p for p in (A / folder_name).rglob('*')
                            if p.is_file() and p.suffix in ('.py', '.json', '.txt'))
        bank = A / 'streaming_rank_classification_bank_v3_20261005'
        evidence.update(bank.glob('*/info_*.json'))
        evidence.update(bank / name for name in ('oof_audit.json', 'training_execution_scope.json'))
        future = A / 'streaming_rank_classifier_future_qa_v3_20261005'
        evidence.update(future / name for name in ('protocol.json', 'verification.json')
                        if (future / name).is_file())
        robust = A / 'streaming_robust_regression_bank_20261005'
        evidence.update(robust.glob('*/info_*.json'))
        evidence.update(robust.glob('prefix_control_*.json'))
        evidence.update(robust / name for name in ('protocol.json', 'oof_audit.json', 'training_execution_scope.json') if (robust/name).is_file())
        evidence.add(future / 'resource_summary.json')
        evidence.update(future.glob('*_frozen_before_future_inference.json'))
        sources = {ROOT / name for name in selected} | evidence
        targets, captures = {}, {}
        for source in sorted(sources):
            assert source.is_file() and source.suffix in ('.py', '.json', '.md', '.yaml', '.yml', '.toml', '.txt'), source
            data = source.read_bytes()
            assert len(data) < 5 * 1024**2 and not sync.SECRET.search(data), source
            if source.suffix == '.json':
                json.loads(data.decode('utf-8-sig'))
            relative = source.relative_to(ROOT)
            destination = PREFIX / relative if source in evidence else relative
            targets[destination.as_posix()] = data
            operational = source.suffix == '.json' and (
                source.name == 'resumed_rounds_nystrom_locked_20261004.json'
                or 'state' in source.stem or 'resume' in source.stem
                or source.stem.startswith(('optimization_boundary', 'optimization_fit_cost', 'next_experiment')))
            captures[relative.as_posix()] = {'published_path': destination.as_posix(),
                'sha256': sync.sha(data), 'bytes': len(data), 'operational_snapshot': operational}
        targets[(PREFIX / '.gitattributes').as_posix()] = b'* -text\n'
        robust_infos = [sync.read(source) for source in sorted(evidence) if source.parent.parent == robust and source.name.startswith('info_')]
        for info in robust_infos:
            assert info['status'] == 'passed' and info['completed_epochs'] == 32
            assert info['actual_native_sample_counter'] == 1 + 32 * info['training_meta']['rows']
        targets[(PREFIX / 'manifest.json').as_posix()] = sync.encoded({
            'status': 'verified_full_robust_workflows_and_closed_classifier_final_native_checks',
            'at_local': sync.now(), 'previous_main': previous, 'files': captures,
            'explicit_parent_rounds': {'87': 86, '88': 87},
            'full_official_records_prespecified': {'87': 100, '88': 98},
            'generator_controls': [100, 98, 98], 'small_robust32pass_controls': 16,
            'expected_actual_robust_full_annual_fits': 20, 'expected_actual_robust_full_final_fits': 4,
            'actual_robust_full_fit_infos_captured': len(robust_infos),
            'actual_robust_full_annual_fits_captured': sum(row['year'] < 2025 for row in robust_infos),
            'classifier20_annual_and4_final_native_fits_closed': True,
            'classifier4_full1599600_row_forecasts_independently_inspected': True,
            'current_quality_worker_ownership': owned,
            'all_original_rounds67_through86_retained_and_required': True,
            'actual_quality_selection_causality_candidates_and_ranking_updates_still_pending': True,
            'only_publication_branch': 'main', 'historical_branch_heads_retained': old_heads,
            'models_raw_data_large_predictions_remain_local_D_or_E': True,
            'new_robust_native_configurations': 4, 'controls_do_not_replace_actual_full_work': True,
            'new_quality_scores_by_controls': 0, 'test_labels_read': False,
            'global_resource_exhaustion_established': False,
        })
        targets[(PREFIX / 'README.md').as_posix()] = (
            '# 原始特征流式鲁棒回归完整验证与分类模型最终训练关闭\n\n'
            '新增原始63维SGD回归：排序/一天收益率目标分别配对平方损失与Huber损失，L2=.0001、完整32遍、固定学习率日程与过去拟合的特征及目标缩放。'
            '标签不截尾，输出逆变换；所有候选继续使用成熟过去标签和相同年度范围。'
            '已有树模型Huber实验不等于覆盖这组配对线性回归。参见[scikit-learn官方文档](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDRegressor.html)。\n\n'
            '16次真实4096行32遍控制通过：未来训练标签和特征污染不影响拟合，流式、数组及独立原生估计器一致，重载与前缀逐位一致。'
            '两种目标的2020年1694259条完整成熟键一致。控制不算完整年度训练或官方分数。'
            '四种模型仍须完成20次全量年度训练、4次最终训练和全量未来推理检查。实际工作已启动，首个完整2020年度训练及预测已完成。\n\n'
            '第87轮接实际合格R86，固定100条完整方案；第88轮接合格R87，固定98条独立主模型与后处理方案。'
            '生成、实际驱动绑定、父工厂、源码复制、封存拒写及类型路由控制通过。所有原第67—86轮保留并必须完成；后续方案仍等待实际前序合格。\n\n'
            '分类模型四个最终模型均完成6754006条成熟记录的32遍训练；四个1599600行、344日、4650代码的实际未来原始预测均经完整重载与真实80日前缀检查。'
            '独立重新检查四份保存模型的样本计数、SHA、全量预测键与有限值，均通过。分类方案的官方评分、采用与完整榜更新仍待实际质量链执行。\n\n'
            '按2020—2024年5635800行、1212连续日最终输出CSV的原官方综合分选模，再冻结、检查因果、生成全量候选并更新完整榜。'
            '验证年份重复使用，选模偏差未校正；未读取测试标签。只提交main，权重及大型缓存保留本地D/E盘。\n'
        ).encode('utf-8')
        for name, record in captures.items():
            if not record['operational_snapshot']:
                assert sync.sha((ROOT / name).read_bytes()) == record['sha256'], name
        for name, data in targets.items():
            sync.atomic(sync.WORKTREE / name, data)
        paths = sorted(targets)
        for offset in range(0, len(paths), 50):
            sync.git('add', '-f', '--', *paths[offset:offset+50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(paths)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
                 '新增流式鲁棒回归20年度4最终训练及198条完整验证，关闭分类模型最终推理检查', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        expected = {name: hashlib.sha256(data).hexdigest() for name, data in targets.items()}
        assert blob_hashes(commit, expected) == expected
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        verify_main(commit)
        watcher.advance_source_index(commit)
        receipt = {'status': 'pushed_verified_robust_workflows_and_classifier_final_native_checks_main_only',
            'at_local': sync.now(), 'commit': commit, 'files': len(targets),
            'verified_raw_git_blob_sha256': len(expected), 'actual_robust_full_annual_infos_captured': sum(row['year'] < 2025 for row in robust_infos),
            'actual_classifier_final_fits_independently_verified': 4,
            'required_actual_official_records': 198, 'new_quality_scores_by_controls': 0,
            'url': f'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/{PREFIX.as_posix()}'}
        sync.atomic(OUT / 'receipt.json', sync.encoded(receipt))
        print(json.dumps(receipt, ensure_ascii=False), flush=True)
    finally:
        sync.git = original_git
        for process in reversed(suspended):
            if process.is_running():
                process.resume()


if __name__ == '__main__':
    main()
