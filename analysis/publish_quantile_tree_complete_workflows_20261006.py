"""Publish tested complete quantile workflow wiring and actual controller recovery."""
from pathlib import Path
import hashlib
import json
import time

import psutil
import publish_classifier_consensus_workflows_20261006 as helpers
from run_dependency_queue_v3_20261006 import owned
from hidden_windows_child_creation_20261006 import install

ROOT, A, sync = helpers.ROOT, helpers.A, helpers.sync
OUT = A / 'quantile_tree_complete_workflows_github_20261006'
PREFIX = Path('validation_sync/quantile_tree_complete_workflows_20261006')


def create(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    assert not OUT.exists()
    generator = sync.read(A / 'quantile_tree_quality_generator_preflight_v2_20261006/verification.json')
    codec = sync.read(A / 'quantile_tree_codec_preflight_20261006/verification.json')
    assert generator['status'] == codec['status'] == 'passed'
    assert [row['generated_records'] for row in generator['controls']] == [100, 98, 98]
    assert codec['actual_native_control_fits'] == 4 and len(codec['checks']) == 4
    assert codec['actual_annual_fits'] == codec['new_quality_scores'] == 0
    recovered = sync.read(A / 'quantile_quality_publication_monitor_handoff_recovery_20261006.json')
    assert recovered['status'] == 'passed_actual_current_PowerShell_recovery_and_full_pending_scope_observation'
    services = {name: sync.read(A / f'service_owned_workflows_20261006/{name}/native_launch.json')
        for name in ('main_publisher_v5', 'progress_monitor_v21', 'quantile_tree_quality_queue',
                     'quantile_tree_full_workflow', 'dependency_queue_v4', 'neural16384_annual')}
    assert all(owned(row) for row in services.values())
    state = sync.read(A / 'ongoing_optimization_state.json')
    assert state['actual_progress_monitor'].endswith('monitor_actual_optimization_progress_v21_20261006.py')
    assert state['quantile_tree_pending_official_rounds'] == [91, 92]
    assert state['quantile_tree_actual_completed_annual_fits'] == state['quantile_tree_actual_completed_final_fits'] == 0
    qstate = sync.read(A / 'quantile_tree_quality_queue_20261006/state.json')
    assert qstate['stage'] == 'waiting_closed_full24_native_fits_and_qualified_predecessor'
    probe = sync.read(A / 'pwsh_service_launch_preflight_20261006/verification.json')
    assert probe['status'] == 'passed_actual_current_PowerShell7_Chinese_path_consoleless_service_launch'
    for name in ('quantile_tree_quality_generators', 'quantile_tree_future_codec', 'pwsh_service_launch_preflight'):
        folder = A / f'service_owned_workflows_20261006/{name}'
        assert sync.read(folder / 'service_execution.json')['status'] == 'passed'
        assert not owned(sync.read(folder / 'native_launch.json'))
    sources = [Path(__file__), *A.glob('*quantile_tree*20261006.py'), *A.glob('*quantile_tree*20261006.json')]
    sources += [A / name for name in (
        'run_quantile_quality_qualified_workflow_20261006.py',
        'build_lossless_ranking_display_v3_20261006.py', 'verify_lossless_ranking_display_v5_20261006.py',
        'lossless_ranking_runtime_adapter_v2_20261006.py', 'lossless_round_publication_adapter_v2_20261006.py',
        'watch_validations_main_v5_20261006.py', 'monitor_actual_optimization_progress_v21_20261006.py',
        'handoff_quantile_quality_publication_monitor_20261006.py',
        'quantile_quality_publication_monitor_handoff_recovery_20261006.json',
        'quantile_quality_lossless_source_extension_20261006.json',
        'launch_service_owned_workflow_utf8_20261006.py',
        'launch_service_owned_workflow_utf8_v2_20261006.py',
        'launch_service_owned_workflow_with_pwsh_20261006.py',
        'probe_utf8_service_launch_20261006.py', 'probe_pwsh_service_launch_20261006.py',
        'utf8_service_launch_initial_failure_20261006.json', 'utf8_service_launch_second_failure_20261006.json',
        'pwsh_service_launch_actual_runtime_20261006.json')]
    sources += [A / f'{prefix}{n}{suffix}.py' for n in (91, 92) for prefix, suffix in (
        ('optimize_training_round', '_v3'), ('finalize_training_round', '_v3'), ('run_training_round', '_v3_pipeline'))]
    for folder in ('quantile_tree_quality_generator_preflight_v2_20261006', 'quantile_tree_codec_preflight_20261006',
        'quantile_quality_publication_monitor_handoff_20261006', 'pwsh_service_launch_preflight_20261006',
        'quantile_tree_quality_queue_20261006'):
        sources += sorted((A / folder).glob('*.json'))
    for name in (*services, 'quantile_tree_quality_generators', 'quantile_tree_future_codec',
        'quantile_quality_controller_handoff', 'utf8_service_launch_preflight', 'utf8_service_launch_preflight_v2',
        'pwsh_service_launch_preflight'):
        folder = A / f'service_owned_workflows_20261006/{name}'
        sources += [p for p in folder.glob('*.json')]
    targets, files = {(PREFIX / '.gitattributes').as_posix(): b'* -text\n'}, {}
    for source in dict.fromkeys(sources):
        data = source.read_bytes()
        assert not sync.SECRET.search(data)
        if source.suffix == '.json':
            json.loads(data.decode('utf-8-sig'))
        destination = source.relative_to(ROOT) if source.parent == A and source.suffix == '.py' else PREFIX / source.relative_to(A)
        name = destination.as_posix()
        targets[name] = data
        files[source.relative_to(ROOT).as_posix()] = {'published_path': name, 'raw_sha256': sync.sha(data)}
    OUT.mkdir()
    restore, suspended = install(), []
    try:
        row = services['main_publisher_v5']
        root, worker = helpers.owned_pair(row['pid'], Path(row['script']), row['script_args'])
        assert worker.pid == row['owned_worker_pid'] and worker.create_time() == row['owned_worker_creation_time']
        for attempt in range(30):
            for p in (worker, root):
                p.suspend()
                suspended.append(p)
            busy = [p for p in root.children(recursive=True) if p.pid != worker.pid and p.name().lower() != 'conhost.exe']
            if not busy:
                break
            for p in reversed(suspended):
                p.resume()
            suspended.clear()
            time.sleep(.2)
        else:
            raise RuntimeError('The exact main publisher still owns an active child.')
        previous = sync.git('rev-parse', 'HEAD')
        helpers.verify_main(previous)
        assert not sync.git('status', '--porcelain')
        targets[(PREFIX / 'manifest.json').as_posix()] = sync.encoded({
            'status': 'passed_actual_copied_native_codec_and_full_generator_wiring_controls_quality_pending',
            'at_local': sync.now(), 'previous_main': previous, 'files': files,
            'actual_additional_native_control_fits': 4, 'actual_new_full_annual_fits': 0,
            'actual_new_full_final_fits': 0, 'pending_full_native_fits': 24,
            'full_official_rounds_pending': [91, 92], 'expected_full_official_records': [100, 98],
            'all_three_generator_ordering_branches_tested_not_official_scores': True,
            'all_four_copied_candidate_local_codecs_actual372000_row_cold80_bit_identical': True,
            'actual_independent_native_and_quality_queues_owned_live': services,
            'actual_complete_main_publisher_and_monitor_recovered_and_operational': True,
            'actual_original_Windows_PowerShell_failures_preserved': True,
            'actual_current_PowerShell7_consoleless_service_probe_passed': True,
            'original67_through90_required_workflow_preserved_and_still_incomplete': True,
            'old_historical_XGBoost90_percent_quantile_overlap_disclosed_in_full_plan': True,
            'physical_resource_boundary_established': False, 'selection_bias_uncorrected': True,
            'new_quality_scores': 0, 'test_labels_read': False, 'only_publication_branch': 'main'})
        targets[(PREFIX / 'README.md').as_posix()] = (
            '# 分位数树完整方案流程与已执行控制\n\n'
            '已生成并测试两轮完整搜索：R91在合格R90上增补三种用途，100条；R92以合格R91为比较基准，'
            '独立主模型及完整后处理细搜98条。三种生成器排序分支均通过，排序值仅用于控制测试，不是官方分数。\n\n'
            '四个原生48轮控制模型的独立推理代码、候选目录中的代码及安装后的祖先路由，'
            '均与此前已验证的37.2万行、80日预测逐位一致；37日前缀也逐位一致，路由恢复检查通过。'
            '新增4次控制拟合未计入完整年度拟合或官方评分，未保存新的小模型缓存。\n\n'
            '完整20年度与4最终拟合仍在等待现有工作关闭和14GiB内存余量；之后才执行两轮198条真实官方评分，'
            '方案冻结、因果检查、完整未来候选、全部榜单检查和每轮main同步。'
            '新队列、同步器及观察器的实际PID、出生时间和命令均已核验；原训练及R82评分没有停止。\n\n'
            '切换控制进程时的旧Windows PowerShell脚本编码失败已保留。恢复后明确选择并核验PowerShell7.6.5，'
            '中文路径下实际独立无窗口启动与来源复核通过。编码差异见'
            '[Microsoft官方说明](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_character_encoding)。\n\n'
            '旧榜已记录XGBoost90%分位数目标；本方向是保持原63特征和树参数的LightGBM固定分位数损失对照。'
            '尚无完整分数、采用或全局资源边界结论。此前四个小模型已清理，来源和验证记录保留。\n'
        ).encode('utf-8')
        for name, data in targets.items():
            sync.atomic(sync.WORKTREE / name, data)
        selected = sorted(targets)
        for offset in range(0, len(selected), 50):
            sync.git('add', '-f', '--', *selected[offset:offset + 50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(selected)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            '接通分位数树198方案完整验证队列，核验独立推理并恢复无窗口同步监控', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        expected = {name: hashlib.sha256(data).hexdigest() for name, data in targets.items()}
        assert helpers.blob_hashes(commit, expected) == expected
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        helpers.verify_main(commit)
        helpers.watcher.advance_source_index(commit)
        create(OUT / 'receipt.json', {'status': 'pushed_complete_workflows_actual_controls_and_recovery_main_only',
            'at_local': sync.now(), 'commit': commit, 'raw_git_blobs_verified': len(expected),
            'new_quality_scores': 0, 'full198_official_scores_and_native24_fits_still_pending': True,
            'url': 'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/' + PREFIX.as_posix()})
    except BaseException as error:
        create(OUT / 'failure.json', {'status': 'failed_preserved_publication_attempt',
            'at_local': sync.now(), 'error': f'{type(error).__name__}: {error}'})
        raise
    finally:
        for p in reversed(suspended):
            if p.is_running():
                p.resume()
        create(OUT / 'actual_hidden_publication_children.json', {'actual_CreateProcess_calls': restore()})


if __name__ == '__main__':
    main()
