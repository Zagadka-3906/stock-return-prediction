"""Publish actual restored-controller and hidden-child controls without stopping science."""
from pathlib import Path
import hashlib
import json
import time

import psutil

import publish_classifier_consensus_workflows_20261006 as helpers
from run_dependency_queue_v3_20261006 import owned
from hidden_windows_child_creation_20261006 import install

ROOT, A, sync = helpers.ROOT, helpers.A, helpers.sync
OUT = A / 'service_owned_workflow_restore_github_20261006'
PREFIX = Path('validation_sync/service_owned_workflow_restore_20261006')


def create(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    assert not OUT.exists()
    child = sync.read(A / 'hidden_windows_child_creation_preflight_20261006/verification.json')
    assert child['status'] == 'passed_actual_subprocess_and_multiprocessing_consoleless_children'
    reconstructed = A / 'lossless_ranking_display_20261006/round81/full_report_publication_snapshot_verification.json'
    proof = sync.read(reconstructed)
    assert proof['status'] == 'passed_exact_original_full_report_bytes_from_immutable_lossless_HTML'
    assert proof['full_original_bytes'] == 634015041 and proof['connected_records'] == 9946
    assert sync.read(A / 'service_owned_workflows_20261006/immutable_ranking_snapshot_preflight/service_execution.json')['status'] == 'passed'
    plan = sync.read(A / 'service_owned_dependency_queue_v4_20261006/queue_plan.json')
    qstate = sync.read(A / 'service_owned_dependency_queue_v4_20261006/state.json')
    controls = {name: sync.read(A / f'service_owned_workflows_20261006/{name}/native_launch.json')
        for name in ('neural16384_annual', 'dependency_queue_v4', 'main_publisher_v4', 'progress_monitor_v20')}
    assert all(owned(row) for row in controls.values())
    round82 = qstate['activated_jobs']['round82']
    assert owned(round82)
    protocol = sync.read(A / 'optimization_20261003_r82/protocol.json')
    assert protocol['expected_scored_records'] == 138
    assert protocol['effective_execution_driver']['all_child_processes_explicitly_hidden_including_multiprocessing']
    sources = [Path(__file__), *[A / name for name in (
        'run_dependency_queue_v4_20261006.py', 'run_recovery_qualified_workflow_v2_20261006.py',
        'qualified_round_recovery_evidence_v3_20261006.py', 'hidden_windows_child_creation_20261006.py',
        'probe_hidden_windows_child_creation_20261006.py', 'lossless_ranking_runtime_adapter_20261006.py',
        'build_lossless_ranking_display_v2_20261006.py', 'verify_lossless_ranking_display_v4_20261006.py',
        'lossless_round_publication_adapter_20261006.py', 'immutable_lossless_ranking_snapshot_20261006.py',
        'probe_immutable_ranking_snapshot_20261006.py', 'verified_round_main_publication_20261006.py',
        'watch_validations_main_v4_20261006.py', 'monitor_actual_optimization_progress_v20_20261006.py',
        'round81_current_lossless_publication_20261006.json')]]
    sources += sorted((A / 'hidden_windows_child_creation_preflight_20261006').glob('*.json'))
    sources += [reconstructed, A / 'service_owned_dependency_queue_v4_20261006/queue_plan.json',
        A / 'service_owned_dependency_queue_v4_20261006/preflight.json',
        A / 'optimization_20261003_r82/protocol.json',
        A / 'resumed_rounds_dependency_queue_v4_20261006.json']
    for name in (*controls, 'immutable_ranking_snapshot_preflight'):
        folder = A / f'service_owned_workflows_20261006/{name}'
        sources += [folder / filename for filename in ('job_definition.json', 'native_launch.json')]
    sources.append(A / 'service_owned_workflows_20261006/immutable_ranking_snapshot_preflight/service_execution.json')
    activated = A / 'service_owned_dependency_queue_v4_20261006/activated_jobs/round82'
    sources += [activated / filename for filename in ('run.json', 'qualified_run.json', 'launch.json')]
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
    restore = install()
    suspended = []
    try:
        row = controls['main_publisher_v4']
        parent, worker = helpers.owned_pair(row['pid'], Path(row['script']), row['script_args'])
        assert worker.pid == row['owned_worker_pid'] and worker.create_time() == row['owned_worker_creation_time']
        for attempt in range(30):
            for process in (worker, parent):
                process.suspend()
                suspended.append(process)
            busy = [p for p in parent.children(recursive=True) if p.pid != worker.pid and p.name().lower() != 'conhost.exe']
            if not busy:
                break
            for process in reversed(suspended):
                process.resume()
            suspended.clear()
            time.sleep(.2)
        else:
            raise RuntimeError('The existing publisher still owns an active child.')
        old = sync.git('rev-parse', 'HEAD')
        helpers.verify_main(old)
        assert not sync.git('status', '--porcelain')
        targets[(PREFIX / 'manifest.json').as_posix()] = sync.encoded({
            'status': 'actual_service_owned_queue_and_hidden_children_and_fullbyte_ranking_reconstruction_validated',
            'at_local': sync.now(), 'previous_main': old, 'files': files,
            'current_exact_owned_controls': controls, 'actual_current_quality_job': round82,
            'all_original_required_rounds': list(range(67, 91)), 'pending_full_quality_rounds': 23,
            'prespecified_scores_still_pending': 2636, 'scheduled_jobs': len(plan['deferred_jobs']),
            'actual_quality_round': 82, 'quality_records_required_for_current_round': 138,
            'all_actual_subprocess_and_multiprocessing_console_handles_zero': True,
            'full9946_record_report634015041_original_bytes_reconstruction_SHA256_identical': True,
            'all_original_full_data_epochs_and_grids_and_independent_future_checks_preserved': True,
            'physical_resource_boundary_established': False, 'new_quality_scores_by_publication': 0,
            'test_labels_read': False, 'only_publication_branch': 'main'})
        targets[(PREFIX / 'README.md').as_posix()] = (
            '# 长任务恢复、窗口检查与完整榜快照\n\n'
            '第81轮124方案的完整来源锁恢复已通过，并已同步main。'
            '新的独立Windows服务启动根进程不依附命令会话；队列、训练、观察器和同步器的'
            '实际PID、出生时间与命令行均已核验。队列保留29个待执行任务和23轮完整评分，'
            '第82轮138方案已实际启动并冻结，超宽模型继续实际32轮年度训练。\n\n'
            '实际普通子进程和multiprocessing.spawn子进程的控制台句柄均为0。'
            '完整9,946条无损页面可以恢复全部634,015,041字节原始JSON，原始字节SHA256一致。'
            '后续每轮保存独立榜单快照与完整浏览器检查；较早轮次可以独立完成，'
            '同时保留全榜真正最高分和当前轮冻结赢家。同步前核验提交中的原始文件字节。\n\n'
            '本次只新增执行和发布证据，没有新增模型分数，没有改变科学模型或官方评分。'
            '尚未证明全局优化或计算资源边界达到。项目输出继续存放于D/E盘，仓库只保留main。\n'
        ).encode('utf-8')
        for name, data in targets.items():
            sync.atomic(sync.WORKTREE / name, data)
        selected = sorted(targets)
        for offset in range(0, len(selected), 50):
            sync.git('add', '-f', '--', *selected[offset:offset + 50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(selected)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            '恢复独立无窗口验证队列及自动同步，核验完整榜634015041字节重建', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        expected = {name: hashlib.sha256(data).hexdigest() for name, data in targets.items()}
        assert helpers.blob_hashes(commit, expected) == expected
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        helpers.verify_main(commit)
        helpers.watcher.advance_source_index(commit)
        create(OUT / 'receipt.json', {'status': 'pushed_all_actual_workflow_and_hidden_child_and_full_report_controls_main_only',
            'at_local': sync.now(), 'commit': commit, 'raw_git_blobs_verified': len(expected),
            'url': 'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/' + PREFIX.as_posix()})
    except BaseException as error:
        create(OUT / 'failure.json', {'status': 'failed_preserved_publication_attempt',
            'at_local': sync.now(), 'error': f'{type(error).__name__}: {error}'})
        raise
    finally:
        for process in reversed(suspended):
            if process.is_running():
                process.resume()
        events = restore()
        create(OUT / 'actual_hidden_publication_children.json', {'actual_CreateProcess_calls': events})


if __name__ == '__main__':
    main()
