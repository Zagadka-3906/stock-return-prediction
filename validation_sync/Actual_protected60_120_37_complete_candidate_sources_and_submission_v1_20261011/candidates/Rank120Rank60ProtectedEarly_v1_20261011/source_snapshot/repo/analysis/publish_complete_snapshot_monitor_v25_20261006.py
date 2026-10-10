"""Publish actual controller wiring and observed complete native scope progress on main."""
from pathlib import Path
import hashlib
import json
import time

import publish_classifier_consensus_workflows_20261006 as helpers
from run_dependency_queue_v3_20261006 import owned
from hidden_windows_child_creation_20261006 import install

ROOT, A, sync = helpers.ROOT, helpers.A, helpers.sync
SOURCE = A / 'complete_snapshot_monitor_verified_v25_20261006'
OUT = A / 'complete_snapshot_monitor_github_v25_20261006'
PREFIX = Path('validation_sync/complete_snapshot_monitor_verified_v25_20261006')


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
    assert proof['status'] == 'passed_two_actual_complete_updates_no_intermediate_public_states'
    assert owned(proof['actual_owned_observer'])
    for filename, digest in proof['input_sha256'].items():
        assert sha(Path(filename)) == digest
    for row in proof['unchanged_scientific_ownership'].values():
        assert owned(row)
    terminal = {'status': 'passed'}
    sources = [Path(__file__), *[A / name for name in (
        'monitor_actual_optimization_progress_v24_20261006.py',
        'monitor_actual_optimization_progress_v25_20261006.py',
        'complete_observer_snapshot_transaction_20261006.py',
        'complete_observer_snapshot_transaction_v2_20261006.py',
        'verify_observer_snapshot_transaction_20261006.py',
        'verify_observer_snapshot_transaction_v2_20261006.py',
        'handoff_complete_snapshot_monitor_20261006.py',
        'handoff_complete_snapshot_monitor_v25_20261006.py',
        'verify_complete_snapshot_monitor_v25_20261006.py')]]
    sources += sorted(SOURCE.glob('*.json')) + sorted(SOURCE.glob('*.jsonl'))
    for name in ('observer_snapshot_transaction_preflight_20261006',
                 'observer_snapshot_transaction_preflight_v2_20261006',
                 'complete_snapshot_monitor_handoff_20261006',
                 'complete_snapshot_monitor_handoff_v25_20261006'):
        sources += sorted((A / name).glob('*.json'))
    for name in ('progress_monitor_v24', 'progress_monitor_v25'):
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
            '# 完整进度刷新：中间状态隔离与实际连续验证\n\n'
            '旧汇总逐层写入公开文件，先显示67轮等待，再显示实际83轮评分，'
            '导致核验原生模型字节期间公开状态回退。新汇总在当前进程内暂存中间状态，'
            '保留全部科学核验，完成后才分别原子更新三份公开文件，并标记同一generation。'
            '跨文件读者可用generation识别顺序提交之间的短暂差异。\n\n'
            '第一版隔离控制覆盖直接写入；第二版另外覆盖外层预先绑定的refresh写入函数，'
            '避免它绕过暂存。两版源文件和验证均保留。真实运行持续观察两次完整刷新，'
            '每份公开文件保持正确的83轮状态、全部待验证范围和真实计数，没有暴露中间排队状态。\n\n'
            '原生20个年度拟合和4个最终拟合，以及另列的组合30份年度输出和6个最终文件保持准确。'
            '组合不计新增原生训练。原198和新262条评分范围保留，所有训练、评分和队列进程身份保持不变。'
            '公开状态快照和逐次观察样本均保存，本次没有新增官方分数或采用结论。'
            '整体优化与资源边界仍需后续完整科学验证。\n'
        ).encode('utf-8')
        for name, data in targets.items():
            sync.atomic(sync.WORKTREE / name, data)
        selected = sorted(targets)
        for offset in range(0, len(selected), 50):
            sync.git('add', '-f', '--', *selected[offset:offset + 50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(selected)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            '修复进度刷新回退并验证两次完整状态及原生与组合计数', timeout=180)
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
