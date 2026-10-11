"""Publish actual native controls, partial saved fits and the complete pending grid."""
from pathlib import Path
import hashlib
import json
import sys

import psutil

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
import watch_validations_main_v2_20261005 as watcher

sync = watcher.sync
PREFIX = Path('validation_sync/linear_leaf_workflow_20261005')


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    receipt_path = sync.OUT / 'linear_leaf_workflow_receipt.json'
    assert not receipt_path.exists()
    directories = ('linear_leaf_preflight_20261005', 'linear_leaf_search_generator_preflight_v2_20261005',
        'linear_leaf_future_codec_preflight_20261005', 'linear_leaf_cost_inventory_qa_20261005',
        'actual_monitor_v6_handoff_20261005')
    proofs = [sync.read(ROOT / 'analysis' / folder / 'verification.json') for folder in directories]
    assert proofs[0]['status'] == 'passed_actual_linear_leaf_maturity_native_reload_and_prefix_controls'
    assert proofs[1]['status'] == proofs[2]['status'] == 'passed'
    assert proofs[3]['status'] == 'passed_actual_saved_artifact_counts_and_idempotent_refresh'
    assert proofs[4]['status'] == 'passed_owned_observer_handoff'
    for proof in proofs:
        for source, value in proof.get('source_sha256', {}).items():
            assert sha(source) == value, source
    for row in proofs[0]['controls']:
        assert sha(ROOT / f"analysis/linear_leaf_preflight_20261005/{row['model']}.joblib") == row['model_sha256']
    storage = sync.read(ROOT / 'analysis/linear_leaf_storage_20261005.json')
    bank = Path(storage['output_directory'])
    infos = sorted(bank.glob('*/info_202[0-4].json'))
    actual = []
    for source in infos:
        info = sync.read(source)
        assert info['status'] == 'passed' and info['new_model_fits'] == 1
        assert info['leaf_summary']['tree_count'] == 300
        assert sha(source.parent / f"model_{info['year']}.joblib") == info['model_sha256']
        assert sha(source.parent / f"raw_{info['year']}.parquet") == info['prediction_sha256']
        actual.append({'model': info['model'], 'year': info['year'], 'rows': info['training_meta']['rows'],
            'fit_seconds': info['fit_seconds'], 'leaf_summary': info['leaf_summary'],
            'info_sha256': sha(source), 'model_sha256': info['model_sha256'],
            'raw_sha256': info['prediction_sha256']})
    jobs = [sync.read(ROOT / 'analysis/linear_leaf_bank_run_20261005.json')]
    receipt = sync.read(ROOT / 'analysis/linear_leaf_followup_launch_receipt_20261005.json')
    jobs += [receipt['future'], receipt['annual_resource_observer'], *receipt['quality_rounds']]
    for job in jobs:
        assert job['script'] in psutil.Process(job['pid']).cmdline(), job['pid']
    observer = psutil.Process(sync.read(sync.OUT / 'owner.lock')['pid'])
    assert str(ROOT / 'analysis/watch_validations_main_v2_20261005.py') in observer.cmdline()
    parent = observer.parent()
    assert parent is not None and parent.cmdline()[1:] == observer.cmdline()[1:]
    suspended = []
    try:
        for process in (observer, parent):
            process.suspend()
            suspended.append(process)
        assert all(p.pid == observer.pid or p.name().lower() == 'conhost.exe' for p in parent.children(recursive=True))
        assert not sync.git('status', '--porcelain')
        head = sync.git('rev-parse', 'HEAD')
        assert sync.git('ls-remote', '--heads', 'origin').splitlines() == [f'{head}\trefs/heads/main']
        sources = set((ROOT / 'analysis').glob('*linear_leaf*20261005.py'))
        sources.update(ROOT / 'analysis' / f'{prefix}{number}{suffix}.py' for number in (69,70)
            for prefix,suffix in (('optimize_training_round',''),('optimize_training_round','_v2'),
                                  ('finalize_training_round',''),('run_training_round','_v2_pipeline')))
        sources.update(ROOT / 'analysis' / name for name in (
            'monitor_actual_optimization_progress_v6_20261005.py', 'handoff_actual_monitor_v6_20261005.py',
            'refresh_optimization_boundary_evidence_v5_20261005.py'))
        evidence = set((ROOT / 'analysis').glob('linear_leaf*20261005.json'))
        evidence.add(ROOT / 'analysis/actual_optimization_monitor_run_v6_20261005.json')
        for folder in directories:
            evidence.update(p for p in (ROOT / 'analysis' / folder).glob('*.json') if p.is_file())
        evidence.update(infos)
        evidence.update(p for p in bank.glob('*.json') if p.is_file())
        snapshots = {ROOT / 'analysis' / name for name in (
            'optimization_fit_cost_evidence_20261004.json', 'optimization_boundary_evidence_20261004.json',
            'next_experiment_directions_20261003.json', 'actual_optimization_monitor_state_20261005.json')}
        paths, bindings = [], {}
        sync.atomic(sync.WORKTREE / PREFIX / '.gitattributes', b'* -text\n')
        paths.append((PREFIX / '.gitattributes').as_posix())
        for source in sorted(sources | evidence | snapshots):
            data = source.read_bytes()
            assert len(data) < 5 * 1024**2 and not sync.SECRET.search(data)
            if source.suffix == '.json':
                json.loads(data.decode('utf-8-sig'))
            relative = source.relative_to(ROOT) if source.is_relative_to(ROOT) else Path('authorized_E_bank') / source.relative_to(bank)
            destination = relative if source in sources else PREFIX / relative
            sync.atomic(sync.WORKTREE / destination, data)
            paths.append(destination.as_posix())
            bindings[str(source)] = {'sha256': hashlib.sha256(data).hexdigest(),
                                     'observational_snapshot': source in snapshots}
        manifest = {'status': 'passed_actual_native_leaf_codec_and_complete_generator_controls',
            'at_local': sync.now(), 'input_files': bindings,
            'actual_preflight_past_rows_each': 4096, 'rounds_each_preflight': 48,
            'all6_saved_native_linear_controls_passed': True,
            'dumped_leaf_formula_and_missing_fallback_independent_reconstruction_passed': True,
            'all6_linear_and10_existing_nystrom_codec_controls_passed': True,
            'real_generator_controls': proofs[1]['controls'],
            'planned_actual_annual_fits': 30, 'planned_actual_final_fits': 6,
            'actual_completed_annual_fit_snapshot': actual,
            'planned_complete_official_records': {'69': 124, '70': 138},
            'full_annual_bank_final_future_and_quality_still_pending': True,
            'annual_future_and_quality_waiters_confirmed_live': True,
            'observer_monitors_through_actual_qualified_round': 70,
            'small_pilots_and_synthetic_ordering_excluded_from_annual_fits_and_quality_scores': True,
            'weights_and_raw_predictions_remain_local_D_or_E': True,
            'RAM14GiB_admission_is_scheduling_policy_not_physical_limit': True,
            'only_publication_branch': 'main', 'global_resource_exhaustion_established': False,
            'new_quality_scores': 0, 'test_labels_read': False}
        sync.atomic(sync.WORKTREE / PREFIX / 'manifest.json', sync.encoded(manifest))
        paths.append((PREFIX / 'manifest.json').as_posix())
        doc = (
            '# 普通树叶与线性树叶的完整方案验证\n\n'
            '排名与收益率各三种配置：普通树叶对照、线性树叶lambda=1、线性树叶lambda=10。'
            '固定300轮、31叶、深度8、最小叶样本128、学习率0.05及同一种子；'
            '63个原始特征的标准化仅使用过去成熟样本，缺失值保留NaN。\n\n'
            '六种配置均在真实过去4096行完成48轮预检：叶节点线性系数确实生效，'
            '实际导出叶节点公式独立复算预测，缺失值回退、模型重载、不同长度前缀及未来标签扰动均通过。'
            '新推理接口也逐位重放了6个线性树模型及10个已有Nyström模型。\n\n'
            '正式流程包含30次年度向前训练、6次成熟最终训练及每模型全部1,599,600条未来X检查。'
            '第69轮比较124条用途融合方案，第70轮比较138条独立完整方案。'
            '生成器实际执行了独立方案胜出和未胜出的分支；合成排序值不是官方评分。\n\n'
            '评分前必须先复现真实前轮完整验证向量、官方八指标及未来CSV，再完成新分支检查。'
            '最终继续方案冻结、训练期收益映射、官方复核、因果检查、候选推理、完整榜更新及main同步。'
            'manifest.json中的实际年度训练列表是提交时快照，其余未完成工作仍明确标为待验证。\n\n'
            '资源采样不替换模型拟合函数。14GiB内存启动条件是调度规则，未宣告方法或资源耗尽。'
            '数据、权重和原始预测留在本地D盘，必要时使用E盘；GitHub仅保留main。\n')
        sync.atomic(sync.WORKTREE / PREFIX / 'README.md', doc.encode('utf-8'))
        paths.append((PREFIX / 'README.md').as_posix())
        for source, item in bindings.items():
            if not item['observational_snapshot']:
                assert sha(source) == item['sha256'], source
        for offset in range(0, len(paths), 50):
            sync.git('add', '--', *paths[offset:offset + 50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(paths)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            '核验六种普通与线性树叶模型，冻结30折训练及262项完整方案验证', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        assert sync.git('ls-remote', '--heads', 'origin').splitlines() == [f'{commit}\trefs/heads/main']
        watcher.advance_source_index(commit)
        result = {'status': 'pushed_verified_only_main', 'at_local': sync.now(), 'commit': commit,
            'files': len(paths), 'actual_completed_annual_fit_snapshot_count': len(actual),
            'new_quality_scores': 0,
            'url': f'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/{PREFIX.as_posix()}'}
        with receipt_path.open('x', encoding='utf-8') as stream:
            json.dump(result, stream, ensure_ascii=False, indent=2)
        print(json.dumps(result, ensure_ascii=False), flush=True)
    finally:
        for process in reversed(suspended):
            if process.is_running():
                process.resume()


if __name__ == '__main__':
    main()
