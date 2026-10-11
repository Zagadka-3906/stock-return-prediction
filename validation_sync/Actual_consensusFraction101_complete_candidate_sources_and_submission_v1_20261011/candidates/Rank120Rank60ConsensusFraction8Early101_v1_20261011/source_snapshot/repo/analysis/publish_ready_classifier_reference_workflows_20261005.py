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
PREFIX = Path('validation_sync/ready_classifier_reference_workflows_20261005')
OUT = A / 'ready_classifier_reference_workflows_github_20261005'


def main():
    assert not (OUT / 'receipt.json').exists(), 'Preserve the completed publication.'
    folders = (
        'ready_classifier_reference_generator_preflight_20261005',
        'ready_classifier_reference_execution_preflight_20261005',
        'ready_classifier_reference_quality_followups_20261005',
        'gap_aware_optimization_monitor_handoff_v17_20261005',
        'streaming_classifier_actual_annual_completion_audit_20261005',
        'rejected_artifact_cleanup_recheck_20261005',
    )
    proofs = [A / folder / 'verification.json' for folder in folders]
    for path in proofs:
        proof = sync.read(path)
        assert proof['status'].startswith('passed'), path
        for source, digest in proof.get('source_sha256', {}).items():
            assert sync.sha(Path(source).read_bytes()) == digest, source
    assert [r['generated_records'] for r in sync.read(proofs[0])['controls']] == [100, 98, 98]
    annual = sync.read(proofs[4])
    assert annual['actual_annual_fits'] == 20 and len(annual['configurations']) == 4
    cleanup = sync.read(proofs[5])
    assert cleanup['deleted_artifacts_still_absent'] == 4674
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
    launch = sync.read(A / 'actual_optimization_monitor_launch_v17_20261005.json')
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
        targets[(PREFIX / 'manifest.json').as_posix()] = sync.encoded({
            'status': 'verified_classifier_controls_actual20_annual_fits_owned_jobs_and_cleanup_recheck',
            'at_local': sync.now(), 'previous_main': previous, 'files': captures,
            'explicit_parent_rounds': {'85': 84, '86': 85},
            'full_official_records_prespecified': {'85': 100, '86': 98},
            'generator_controls': [100, 98, 98], 'actual_annual_fits_independently_verified': 20,
            'all_actual_annual_fits_completed_full32_passes': True,
            'actual4_final_fits_and_full_future_QA_required_before_quality': True,
            'current_quality_worker_ownership': owned, 'original_rounds67_through84_retained_and_required': True,
            'actual_quality_selection_causality_candidates_and_ranking_updates_still_pending': True,
            'verified_cleanup': cleanup,
            'models_raw_data_and_large_predictions_remain_local_D_or_E': True,
            'only_publication_branch': 'main', 'historical_branch_heads_retained': old_heads,
            'new_native_configurations_by_controls': 0, 'new_native_fits_by_controls': 0,
            'existing20_annual_fits_not_counted_twice': True, 'new_quality_scores_by_controls': 0,
            'test_labels_read': False, 'global_resource_exhaustion_established': False,
        })
        targets[(PREFIX / 'README.md').as_posix()] = (
            '# 分类模型年度训练审计、后续完整验证与弃用文件清理复核\n\n'
            '原始63维特征上的Top10%二分类、十分位分类，各比较两种L2强度。'
            '四种配置均已完成2020—2024年20次实际年度训练，每次完整32遍；独立检查权重与预测SHA、成熟标签计数、保存的SGD样本计数和真实扫描批次数。'
            '20次年度训练已完成；4次最终训练和全量未来推理、模型重载、真实80日前缀检查仍是完整验证的前提。\n\n'
            '第85轮接实际合格第84轮，固定100条完整方案；第86轮接合格第85轮，固定98条独立模型与后处理方案。'
            '实际驱动、来源复制、封存拒写、四个真实年度模型的分类路由及前缀控制通过；两个任务已实际启动。'
            '合成生成控制不算官方分数，所有原第67—84轮仍保留并必须完成。\n\n'
            '清理已直接删除903个弃用模型权重、3771个预测或派生缓存，实际释放约38.74 GiB。'
            '复核4674个文件仍不存在，全部12217份保留记录及当前交付、R65/R66候选、采用的原始模型依赖与原SHA一致。'
            '当前方案和运行中验证的依赖保留。清理前后的记录与分数不变。\n\n'
            '继续遵循5,635,800行、1,212连续交易日的训练期完整官方综合分和过去拟合的收益率映射。'
            '重复验证的选模偏差未校正；未读取测试标签。仅使用main，未上传权重或大型缓存。\n'
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
                 '保存20次分类模型完整年度训练审计、198条后续完整验证和弃用文件清理复核', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        expected = {name: hashlib.sha256(data).hexdigest() for name, data in targets.items()}
        assert blob_hashes(commit, expected) == expected
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        verify_main(commit)
        watcher.advance_source_index(commit)
        receipt = {'status': 'pushed_verified_classifier_workflows_and_cleanup_recheck_main_only',
            'at_local': sync.now(), 'commit': commit, 'files': len(targets),
            'verified_raw_git_blob_sha256': len(expected), 'actual_annual_fits_verified': 20,
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
