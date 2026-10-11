"""Publish actual quantile controls and deferred full fits to the sole main branch."""
from pathlib import Path
import hashlib
import json
import time

import psutil

import publish_classifier_consensus_workflows_20261006 as helpers
from run_dependency_queue_v3_20261006 import owned
from hidden_windows_child_creation_20261006 import install

ROOT, A, sync = helpers.ROOT, helpers.A, helpers.sync
OUT = A / 'quantile_tree_native_preflight_github_20261006'
PREFIX = Path('validation_sync/quantile_tree_native_preflight_20261006')


def create(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    assert not OUT.exists()
    proof = sync.read(A / 'quantile_tree_preflight_20261006/verification.json')
    assert proof['status'] == 'passed_actual_quantile_native_maturity_reload_and_cold80_controls'
    assert proof['actual_native_control_fits'] == 8 and len(proof['checks']) == 4
    assert proof['actual_annual_fits'] == proof['new_quality_scores'] == 0
    for row in proof['checks']:
        assert row['actual_cold80_training_validation_rows'] == 372000
        assert row['actual_cold80_days'] == 80 and row['actual_codes'] == 4650
        assert row['future_label_poison_retraining_and_preprocessing_bit_identical']
        assert row['actual_cold80_native_reload_bit_identical']
        assert row['actual37_day_cold_prefix_and_later_feature_poison_bit_identical']
        assert row['independent_dumped_leaf_sum_max_abs_error'] < 1e-10
    service = A / 'service_owned_workflows_20261006/quantile_tree_preflight'
    assert sync.read(service / 'service_execution.json')['status'] == 'passed'
    assert not owned(sync.read(service / 'native_launch.json'))
    native_service = A / 'service_owned_workflows_20261006/quantile_tree_full_workflow'
    native = sync.read(native_service / 'native_launch.json')
    assert owned(native)
    state = sync.read(A / 'quantile_tree_native_full_workflow_20261006/state.json')
    assert state['stage'] == 'deferred_until_existing_required_native_and_quality_jobs_are_closed_and14GiB_available'
    assert state['actual_new_full_annual_fits'] == state['actual_new_full_final_fits'] == 0
    controls = {name: sync.read(A / f'service_owned_workflows_20261006/{name}/native_launch.json')
                for name in ('main_publisher_v4', 'dependency_queue_v4', 'neural16384_annual')}
    assert all(owned(row) for row in controls.values())
    sources = [Path(__file__), *[A / name for name in (
        'quantile_tree_candidate_20261006.py', 'verify_quantile_tree_candidate_20261006.py',
        'quantile_tree_candidate_plan_20261006.json', 'train_quantile_tree_bank_20261006.py',
        'verify_quantile_tree_full_future_20261006.py', 'run_quantile_tree_full_workflow_20261006.py',
        'quantile_tree_storage_20261006.json', 'quantile_tree_native_full_workflow_20261006/run.json')]]
    sources += sorted((A / 'quantile_tree_preflight_20261006').glob('*.json'))
    for folder in (service, native_service):
        sources += [folder / name for name in ('job_definition.json', 'native_launch.json')]
    sources.append(service / 'service_execution.json')
    targets, files = {(PREFIX / '.gitattributes').as_posix(): b'* -text\n'}, {}
    for source in sources:
        data = source.read_bytes()
        assert not sync.SECRET.search(data)
        if source.suffix == '.json':
            json.loads(data.decode('utf-8-sig'))
        destination = source.relative_to(ROOT) if source.parent == A and source.suffix == '.py' else PREFIX / source.relative_to(A)
        name = destination.as_posix()
        targets[name] = data
        files[source.relative_to(ROOT).as_posix()] = {'published_path': name, 'raw_sha256': sync.sha(data)}
    targets[(PREFIX / 'full_native_queue_state_snapshot.json').as_posix()] = sync.encoded(state)
    OUT.mkdir()
    restore, suspended = install(), []
    try:
        row = controls['main_publisher_v4']
        parent, worker = helpers.owned_pair(row['pid'], Path(row['script']), row['script_args'])
        assert worker.pid == row['owned_worker_pid'] and worker.create_time() == row['owned_worker_creation_time']
        for attempt in range(30):
            for process in (worker, parent):
                process.suspend()
                suspended.append(process)
            busy = [p for p in parent.children(recursive=True)
                    if p.pid != worker.pid and p.name().lower() != 'conhost.exe']
            if not busy:
                break
            for process in reversed(suspended):
                process.resume()
            suspended.clear()
            time.sleep(.2)
        else:
            raise RuntimeError('Existing main publisher owns an active child; no concurrent Git mutation allowed.')
        previous = sync.git('rev-parse', 'HEAD')
        helpers.verify_main(previous)
        assert not sync.git('status', '--porcelain')
        targets[(PREFIX / 'manifest.json').as_posix()] = sync.encoded({
            'status': 'actual_quantile_native_controls_passed_full_annual_and_scheme_quality_pending',
            'at_local': sync.now(), 'previous_main': previous, 'files': files,
            'actual_native_control_fits': 8, 'control_training_rows': 4096, 'iterations_each_control_fit': 48,
            'four_actual372000_row80_day_native_reload_and_future_poison_controls_passed': True,
            'independent_dumped_native_leaf_sum_max_abs_error': max(x['independent_dumped_leaf_sum_max_abs_error'] for x in proof['checks']),
            'actual_new_full_annual_fits': 0, 'actual_new_full_final_fits': 0,
            'pending_full_annual_fits': 20, 'pending_full_final_fits': 4,
            'native_full_workflow_owned_deferred': native,
            'original_required_rounds_and29_job_queue_unchanged': True,
            'full_scheme_quality_and_scientific_candidate_and_ranking_update_still_pending': True,
            'no_official_score_or_adoption_claim_from_pilots': True,
            'physical_resource_boundary_established': False, 'selection_bias_uncorrected': True,
            'new_quality_scores': 0, 'test_labels_read': False, 'only_publication_branch': 'main'})
        targets[(PREFIX / 'README.md').as_posix()] = (
            '# 分位数树损失：已完成原生预检，完整评分待执行\n\n'
            '检查现有实现后新增固定分位数损失对照：rank中位数，return的0.1、0.5、0.9分位数。'
            '保持原63特征、成熟训练过滤、过去均值和标准差、缺失值处理、树结构和300轮完整训练预算；'
            '仅改变损失目标与分位数alpha。方法参数见[LightGBM官方文档](https://lightgbm.readthedocs.io/en/latest/Parameters.html#objective)。\n\n'
            '实际完成8次4096行、48轮的小模型控制；四配置的37.2万行、80日冷启动推理重载均逐位一致。'
            '未来标签扰动后重训与预处理逐位一致，第37日之后的未来特征扰动不改变前缀；'
            '独立累加原生模型叶节点值与推理结果最大误差为0。小模型未计入年度完整拟合数或官方分数。\n\n'
            '独立无窗口队列已登记20个完整年度拟合与4个最终拟合，等待原67至90轮工作真正关闭及14GiB可用内存。'
            '现有29任务队列继续运行。之后还须完成完整五年向前官方评分、返回映射CSV、'
            '完整方案冻结和因果检查、最终候选推理、完整榜更新及main同步。'
            '本次尚无官方评分改善或采用结论，也未建立全局资源边界。项目输出只存D/E盘。\n'
        ).encode('utf-8')
        for name, data in targets.items():
            sync.atomic(sync.WORKTREE / name, data)
        selected = sorted(targets)
        for offset in range(0, len(selected), 50):
            sync.git('add', '-f', '--', *selected[offset:offset + 50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(selected)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            '验证固定分位数树原生因果和80日重载，登记完整年度拟合待执行', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        expected = {name: hashlib.sha256(data).hexdigest() for name, data in targets.items()}
        assert helpers.blob_hashes(commit, expected) == expected
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        helpers.verify_main(commit)
        helpers.watcher.advance_source_index(commit)
        create(OUT / 'receipt.json', {'status': 'pushed_actual_quantile_native_controls_and_deferred_full_fits_main_only',
            'at_local': sync.now(), 'commit': commit, 'raw_git_blobs_verified': len(expected),
            'new_quality_scores': 0, 'full_quality_and_adoption_still_pending': True,
            'url': 'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/' + PREFIX.as_posix()})
    except BaseException as error:
        create(OUT / 'failure.json', {'status': 'failed_preserved_publication_attempt',
            'at_local': sync.now(), 'error': f'{type(error).__name__}: {error}'})
        raise
    finally:
        for process in reversed(suspended):
            if process.is_running():
                process.resume()
        create(OUT / 'actual_hidden_publication_children.json', {'actual_CreateProcess_calls': restore()})


if __name__ == '__main__':
    main()
