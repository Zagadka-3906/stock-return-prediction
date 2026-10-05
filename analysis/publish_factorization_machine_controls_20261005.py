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
PREFIX = Path('validation_sync/factorization_machine_workflow_20261005')


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    receipt_path = sync.OUT / 'factorization_machine_workflow_receipt.json'
    assert not receipt_path.exists()
    directories = ('factorization_machine_preflight_20261005', 'factorization_machine_search_generator_preflight_v3_20261005',
        'factorization_machine_future_codec_preflight_20261005', 'factorization_machine_cost_inventory_qa_20261005',
        'actual_monitor_v8_handoff_20261005')
    proofs = [sync.read(ROOT / 'analysis' / folder / 'verification.json') for folder in directories]
    assert proofs[0]['status'] == 'passed_actual_factorization_formula_gradients_maturity_saved_models_andprefix_controls'
    assert proofs[1]['status'] == proofs[2]['status'] == 'passed'
    assert proofs[3]['status'] == 'passed_actual_saved_artifact_counts_and_idempotent_refresh'
    assert proofs[4]['status'] == 'passed_owned_observer_handoff'
    for proof in proofs:
        for source, value in proof.get('source_sha256', {}).items():
            assert sha(source) == value, source
    for row in proofs[0]['controls']:
        assert sha(ROOT / f"analysis/factorization_machine_preflight_20261005/{row['model']}.joblib") == row['model_sha256']
    storage = sync.read(ROOT / 'analysis/factorization_machine_storage_20261005.json')
    bank = Path(storage['output_directory'])
    infos = sorted(bank.glob('*/info_202[0-4].json'))
    actual = []
    for source in infos:
        info = sync.read(source)
        assert info['status'] == 'passed' and info['new_model_fits'] == 1
        assert info['completed_training_epochs']==32
        assert sha(source.parent / f"model_{info['year']}.joblib") == info['model_sha256']
        assert sha(source.parent / f"raw_{info['year']}.parquet") == info['prediction_sha256']
        actual.append({'model': info['model'], 'year': info['year'], 'rows': info['training_meta']['rows'],
            'fit_seconds': info['fit_seconds'], 'actual_parameter_count':info['actual_parameter_count'],'completed_training_epochs':info['completed_training_epochs'],
            'info_sha256': sha(source), 'model_sha256': info['model_sha256'],
            'raw_sha256': info['prediction_sha256']})
    jobs = [sync.read(ROOT / 'analysis/factorization_machine_bank_run_20261005.json')]
    receipt = sync.read(ROOT / 'analysis/factorization_machine_followup_launch_receipt_20261005.json')
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
        sources = set((ROOT / 'analysis').glob('*factorization_machine*20261005.py'))
        sources.update(ROOT / 'analysis' / f'{prefix}{number}{suffix}.py' for number in (73,74)
            for prefix,suffix in (('optimize_training_round',''),('optimize_training_round','_v3'),
                                  ('finalize_training_round',''),('run_training_round','_v3_pipeline')))
        sources.update(ROOT / 'analysis' / name for name in (
            'monitor_actual_optimization_progress_v8_20261005.py', 'handoff_actual_monitor_v8_20261005.py',
            'refresh_optimization_boundary_evidence_v7_20261005.py'))
        evidence = set((ROOT / 'analysis').glob('factorization_machine*20261005.json'))
        evidence.add(ROOT / 'analysis/actual_optimization_monitor_run_v8_20261005.json')
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
            'actual_preflight_past_rows_each': 4096, 'epochs_each_preflight':4,'epochs_each_complete_training':32,'training_device':'cpu',
            'all6_saved_native_factorization_controls_passed': True,
            'explicit_pair_formula_and_analytic_parameter_gradients_independently_checked':True,
            'all6_factorization_and10_existing_nystrom_codec_controls_passed': True,
            'real_generator_controls': proofs[1]['controls'],
            'planned_actual_annual_fits': 30, 'planned_actual_final_fits': 6,
            'actual_completed_annual_fit_snapshot': actual,
            'planned_complete_official_records': {'73':124,'74':138},
            'full_annual_bank_final_future_and_quality_still_pending': True,
            'annual_future_and_quality_waiters_confirmed_live': True,
            'observer_monitors_through_actual_qualified_round':74,
            'small_pilots_and_synthetic_ordering_excluded_from_annual_fits_and_quality_scores': True,
            'weights_and_raw_predictions_remain_local_D_or_E': True,
            'RAM14GiB_admission_is_scheduling_policy_not_physical_limit': True,
            'only_publication_branch': 'main', 'global_resource_exhaustion_established': False,
            'new_quality_scores': 0, 'test_labels_read': False}
        sync.atomic(sync.WORKTREE / PREFIX / 'manifest.json', sync.encoded(manifest))
        paths.append((PREFIX / 'manifest.json').as_posix())
        doc = ('# 原始63特征的因子分解机完整方案验证\n\n'
            '排名与收益率各三种配置：一阶对照、二阶因子秩8、二阶因子秩32；固定CPU训练32轮、相同AdamW参数及成熟过去样本。参数数分别为64、568、2080，缺失值仅用过去均值填充，收益率截断仅从过去训练窗口学习。\n\n'
            '六种真实4096行、4轮预检均通过显式特征对交互公式、解析参数梯度、保存模型重载、不同长度前缀及未来标签扰动检查。两种目标的三档配置预测确实不同。小样本预检不计入实际完整年度拟合或官方成绩。\n\n'
            '后续包含30次完整年度拟合、6次成熟最终拟合、全部1,599,600条未来X检查及第73/74轮124/138项完整官方评分。独立方案胜出和未胜出分支的生成器检查通过；合成排序值不是官方分数。\n\n'
            '当前正式年度拟合等待14GiB可用主存调度保留量，尚无完整年度拟合。固定CPU避免争用宽网络的GPU显存，资源观察不替换拟合函数；没有宣告方法或物理资源耗尽。既有的全部年序、意见门控、收益映射、因果检查、候选推理及完整榜工作均保留。\n\n'
            '模型选择仍只比较连接五年的完整方案官方S。训练验证年份已反复使用，选模偏差未校正；没有使用实际测试标签。原始生成v2源文件保留，新v3修正旧宽度标签及继承集成在精确同分时的分支数。数据、模型和原始预测留在D/E盘。\n\n'
            '模型公式依据作者资料：https://www.libfm.org/ ，采用项目自写PyTorch拟合与NumPy原生推理实现。\n')
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
            '核验六种因子分解机交互和梯度，登记30折正式训练及262项完整评分', timeout=180)
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
