"""Publish actual controller wiring and observed complete native scope progress on main."""
from pathlib import Path
import hashlib
import json
import time

import publish_classifier_consensus_workflows_20261006 as helpers
from run_dependency_queue_v3_20261006 import owned
from hidden_windows_child_creation_20261006 import install

ROOT, A, sync = helpers.ROOT, helpers.A, helpers.sync
SOURCE = A / 'distribution_views_progress_handoff_20261006'
OUT = A / 'distribution_views_progress_handoff_github_20261006'
PREFIX = Path('validation_sync/distribution_views_progress_handoff_20261006')


def create(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    assert not OUT.exists()
    OUT.mkdir()
    proof = sync.read(SOURCE / 'verification.json')
    assert proof['status'] == 'passed_actual_v23_update_and_scientific_workers_preserved'
    assert owned(proof['actual_owned_observer'])
    for filename, digest in proof['input_sha256'].items():
        assert sha(Path(filename)) == digest
    for row in proof['unchanged_scientific_workers'].values():
        assert owned(row)
    terminal = {'status': 'passed'}
    sources = [Path(__file__),
        A / 'monitor_actual_optimization_progress_v23_20261006.py',
        A / 'handoff_distribution_views_progress_monitor_20261006.py',
        A / 'recover_distribution_views_progress_monitor_20261006.py',
        A / 'verify_distribution_views_progress_monitor_20261006.py']
    sources += sorted(SOURCE.glob('*.json'))
    for name in ('progress_monitor_v23', 'progress_monitor_v23_recovery'):
        folder = A / 'service_owned_workflows_20261006' / name
        sources += sorted(folder.glob('*.json')) + sorted(folder.glob('*.log'))
    for name in ('quantile_tree_quality_queue_v2_20261006', 'quantile_distribution_views_quality_queue_20261006'):
        sources += sorted((A / name).glob('*.json'))
    targets = {(PREFIX / '.gitattributes').as_posix(): b'* -text\n'}
    files = {}
    for source in dict.fromkeys(sources):
        data = source.read_bytes()
        assert not sync.SECRET.search(data)
        destination = source.relative_to(ROOT) if source.parent == A and source.suffix == '.py' else PREFIX / source.relative_to(A)
        targets[destination.as_posix()] = data
        files[source.relative_to(ROOT).as_posix()] = {'published_path': destination.as_posix(), 'raw_sha256': hashlib.sha256(data).hexdigest()}
    restore, suspended = install(), []
    try:
        pub = sync.read(A / 'service_owned_workflows_20261006/main_publisher_v5/native_launch.json')
        assert owned(pub)
        root, worker = helpers.owned_pair(pub['pid'], Path(pub['script']), pub['script_args'])
        assert worker.pid == pub['owned_worker_pid'] and worker.create_time() == pub['owned_worker_creation_time']
        for attempt in range(50):
            for process in (worker, root):
                process.suspend()
                suspended.append(process)
            busy = [p for p in root.children(recursive=True) if p.pid != worker.pid and p.name().lower() != 'conhost.exe']
            if not busy:
                break
            for process in reversed(suspended):
                process.resume()
            suspended.clear()
            time.sleep(.2)
        else:
            raise RuntimeError('Main publisher still owns an active publication child.')
        previous = sync.git('rev-parse', 'HEAD')
        helpers.verify_main(previous)
        assert not sync.git('status', '--porcelain')
        targets[(PREFIX / 'manifest.json').as_posix()] = sync.encoded({
            'status': terminal['status'], 'at_local': sync.now(), 'files': files, 'previous_main': previous,
            'entire_actual_control_execution_preserved': True,
            'actual_controller_wiring_control_status': terminal['status'],
            'complete_native20_annual4_final_and_virtual30_annual6_final_verified': True,
            'original198_and_additional262_official_quality_still_pending': True,
            'new_quality_scores': 0, 'physical_resource_boundary_established': False,
            'test_labels_read': False, 'only_publication_branch': 'main'})
        targets[(PREFIX / 'README.md').as_posix()] = (
            '# 原生与组合进度的实际汇总核验\n\n'
            '新的汇总程序实际报告20个年度原生拟合及4个最终原生拟合，'
            '另列30份年度组合输出和6个最终组合文件；组合不计作新增原生训练。'
            '原有198条及新增262条完整官方评分方案均保留，83轮正在实际评分。\n\n'
            '切换仅停止旧汇总进程。训练、评分和队列的PID、创建时间、命令身份保持一致。'
            '首次汇总启动因定义缺少command_line返回WMI错误21且没有创建进程；'
            '原定义及失败结果保留，独立新定义修复后无窗口启动成功并产生真实更新。'
            '已核对当前可见终端窗口，记录实际数量；没有关闭用户应用。\n\n'
            '本次属于运行状态与汇总核验，未新增官方评分或采用结论。'
            '所有仍待完成的训练、连续五年评分、冻结、因果、候选与完整榜检查继续保留。'
            '未证明全局优化极限或资源耗尽。\n'
        ).encode('utf-8')
        for name, data in targets.items():
            sync.atomic(sync.WORKTREE / name, data)
        selected = sorted(targets)
        for offset in range(0, len(selected), 50):
            sync.git('add', '-f', '--', *selected[offset:offset + 50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(selected)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            '核验原生20加4及组合30加6进度并保留198与262完整评分队列', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        expected = {name: hashlib.sha256(data).hexdigest() for name, data in targets.items()}
        assert helpers.blob_hashes(commit, expected) == expected
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        helpers.verify_main(commit)
        helpers.watcher.advance_source_index(commit)
        create(OUT / 'receipt.json', {'status': 'pushed_actual_controls_main_only', 'control_status': terminal['status'],
            'at_local': sync.now(), 'commit': commit, 'raw_git_blobs_verified': len(expected), 'new_quality_scores': 0,
            'url': 'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/' + PREFIX.as_posix()})
    except BaseException as error:
        create(OUT / 'failure.json', {'status': 'failed_preserved_publication_attempt', 'error': f'{type(error).__name__}: {error}'})
        raise
    finally:
        for process in reversed(suspended):
            if process.is_running():
                process.resume()
        create(OUT / 'actual_hidden_publication_children.json', {'actual_CreateProcess_calls': restore()})


if __name__ == '__main__':
    main()
