"""Publish guarded full-control launch or its actual result to main only."""
from pathlib import Path
import hashlib
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from hidden_windows_child_creation_20261006 import install
import publish_classifier_consensus_workflows_20261006 as helpers


def main(phase):
    assert phase in ('launch', 'execution')
    folder = A / 'bounded_root_full_controls_waiter_v2_20261006'
    full = A / 'bounded_root_replay_full_controls_20261006'
    frozen = read(folder / 'frozen_before_actual_wait.json')
    for path, digest in frozen['input_sha256'].items(): assert sha(path) == digest, path
    if phase == 'launch':
        proof = read(folder / 'actual_launch_control.json')
        assert proof['status'] == 'passed_actual_consoleless_waiter_preserving_live_scientific_processes'
        assert owned(proof['actual_waiter'])
    else:
        proof = read(folder / 'actual_full_control_execution.json')
        assert proof['status'] in ('passed', 'failed_preserved')
        assert proof['runtime_adopted'] is False
    out = A / f'bounded_root_full_controls_v2_{phase}_github_20261006'
    assert not out.exists()
    out.mkdir()
    prefix = Path(f'validation_sync/bounded_root_full_controls_v2_{phase}_20261006')
    sources = [Path(__file__), A / 'wait_bounded_root_full_controls_v2_20261006.py',
        A / 'launch_bounded_root_full_controls_waiter_v2_20261006.py',
        *map(Path, frozen['input_sha256']), *folder.glob('*.json'),
        *(A / 'bounded_root_waiter_safe_publication_adoption_20261006').glob('*.json')]
    if phase == 'execution':
        sources += [*full.rglob('*.json'), *folder.glob('*.log')]
    else:
        sources += list((A / 'service_owned_workflows_20261006/bounded_root_full_controls_waiter').glob('*.json'))
    sync = helpers.sync
    targets = {(prefix / '.gitattributes').as_posix(): b'* -text\n'}
    files = {}
    for path in dict.fromkeys(sources):
        data = path.read_bytes()
        assert len(data) < 5 * 1024**2 and not sync.SECRET.search(data), path
        target = path.relative_to(ROOT) if path.parent == A and path.suffix == '.py' else prefix / path.relative_to(ROOT)
        targets[target.as_posix()] = data
        files[path.relative_to(ROOT).as_posix()] = {
            'published_path': target.as_posix(), 'raw_sha256': hashlib.sha256(data).hexdigest()}
    candidates = [read(A / f'service_owned_workflows_20261006/{name}/native_launch.json')
        for name in ('main_publisher_v7', 'main_publisher_v6')
        if (A / f'service_owned_workflows_20261006/{name}/native_launch.json').exists()]
    identity = next(row for row in candidates if owned(row))
    from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
    suspended = []
    restore = install()
    try:
        assert identity['name'] == 'main_publisher_v7'
        root, worker, idle = suspended_idle(identity,
            '    main (watch_validations_main_v7_20261006.py:71)')
        suspended.extend((worker, root))
        create(out / 'actual_publisher_idle_before_and_after_hold.json', idle)
        previous = sync.git('rev-parse', 'HEAD')
        helpers.verify_main(previous)
        assert not sync.git('status', '--porcelain')
        targets[(prefix / 'manifest.json').as_posix()] = sync.encoded({
            'phase': phase, 'status': proof['status'], 'previous_main': previous,
            'at_local': sync.now(), 'files': files, 'runtime_adopted': False,
            'new_quality_scores': 0, 'new_native_fits': 0, 'only_publication_branch': 'main'})
        targets[(prefix / 'README.md').as_posix()] = (
            '# 历史根缓存全量控制的后台执行与结果\n\n'
            '实际无窗口、命令会话外的后台程序等待第97轮队列接入完成。只有实际队列子进程树为空、'
            '没有仍运行的评分轮、暂停前后两次调用栈均在原休眠位置、可用内存至少14GiB时，'
            '才暂时保留空闲调度槽并启动原完整控制程序；不暂停任何科学工作进程。子控制进程'
            '成功或失败后，首先恢复队列，再保存并上传实际结果。14GiB为调度保护而非物理极限。\n\n'
            '完整范围仍为5635800行、1212日、4650股票，五个真实第95轮配置，逐位输出、'
            '八项官方指标、冷80/260日前缀、标签污染、根修改与实测耗时。没有新训练或新选模记录，'
            '不读取测试标签。即使控制通过，也未自动采用该缓存；采用须另行实际验证。'
            'launch发布只证明实际等待程序启动，execution发布才包含实际执行结果，失败记录保留。\n'
        ).encode('utf-8')
        for name, data in targets.items(): sync.atomic(sync.WORKTREE / name, data)
        selected = sorted(targets)
        for offset in range(0, len(selected), 50): sync.git('add', '-f', '--', *selected[offset:offset+50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(selected)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            f'记录历史根缓存完整控制的实际{phase}与科学队列保护', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        hashes = {name: hashlib.sha256(data).hexdigest() for name, data in targets.items()}
        assert helpers.blob_hashes(commit, hashes) == hashes
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        helpers.verify_main(commit)
        helpers.watcher.advance_source_index(commit)
        create(out / 'receipt.json', {
            'status': f'pushed_actual_full_root_controls_{phase}_main_only',
            'at_local': sync.now(), 'commit': commit, 'raw_git_blobs_verified': len(hashes),
            'runtime_adopted': False, 'new_quality_scores': 0,
            'url': 'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/' + prefix.as_posix()})
        print(json.dumps(read(out / 'receipt.json'), ensure_ascii=False), flush=True)
    except BaseException as exc:
        create(out / 'failure.json', {'status': 'failed_preserved_full_root_control_publication',
            'error': f'{type(exc).__name__}: {exc}'})
        raise
    finally:
        for process in reversed(suspended):
            if process.is_running(): process.resume()
        create(out / 'actual_hidden_publication_children.json', {'events': restore()})


if __name__ == '__main__': main(sys.argv[1])
