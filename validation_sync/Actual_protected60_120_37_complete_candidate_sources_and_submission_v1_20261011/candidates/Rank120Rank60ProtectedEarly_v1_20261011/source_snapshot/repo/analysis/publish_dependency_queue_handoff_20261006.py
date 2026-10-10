"""Publish the verified idle-only handoff while leaving scientific work live."""
from pathlib import Path
import hashlib
import json
import sys
import time

import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
import watch_validations_main_v2_20261005 as watcher
from finalize_main_branch_consolidation_20261005 import owned_pair, verify_main
from publish_main_closeout_v2_20261005 import blob_hashes
from run_dependency_queue_20261006 import owned

sync = watcher.sync
OUT = A / 'dependency_queue_handoff_github_20261006'
PREFIX = Path('validation_sync/dependency_queue_handoff_20261006')
QUEUE = A / 'idle_dependency_queue_handoff_v2_20261006'


def main():
    assert not (OUT / 'receipt.json').exists()
    audit = sync.read(A / 'dependency_queue_handoff_audit_20261006/verification.json')
    assert audit['status'] == 'passed_live_queue_all_frozen_sources_and_original_scope'
    plan = sync.read(QUEUE / 'plan.json')
    jobs = {**plan['preserved_active_jobs'], 'dependency_queue': sync.read(QUEUE / 'launch.json')}
    assert all(owned(row) for row in jobs.values())
    pairs = [owned_pair(jobs[name]['pid'], Path(jobs[name]['script']), jobs[name]['script_args'])
             for name in ('main_publisher', 'progress_monitor')]
    suspended = []
    OUT.mkdir(exist_ok=True)
    try:
        for _ in range(30):
            for parent, child in pairs:
                for process in (child, parent):
                    process.suspend()
                    suspended.append(process)
            busy = [p for parent, child in pairs for p in parent.children(recursive=True)
                    if p.pid != child.pid and p.name().lower() != 'conhost.exe']
            if not busy:
                break
            for process in reversed(suspended):
                process.resume()
            suspended.clear()
            time.sleep(.2)
        else:
            raise RuntimeError('An existing publication or observer child is still active.')
        previous = sync.git('rev-parse', 'HEAD')
        verify_main(previous)
        assert not sync.git('status', '--porcelain')
        sources = [Path(__file__), *(A / name for name in (
            'run_dependency_queue_20261006.py', 'run_dependency_queue_v2_20261006.py',
            'handoff_idle_dependencies_20261006.py', 'handoff_dependency_queue_v2_20261006.py',
            'audit_dependency_queue_handoff_20261006.py', 'windows_hidden_process_launch_20261006.py',
            'resumed_rounds_dependency_queue_20261006.json', 'resumed_rounds_dependency_queue_v2_20261006.json'))]
        for folder in ('idle_dependency_queue_handoff_20261006',
                       'idle_dependency_queue_handoff_v2_20261006', 'dependency_queue_handoff_audit_20261006'):
            sources.extend((A / folder).rglob('*.json'))
        targets, files = {}, {}
        for source in dict.fromkeys(sources):
            data = source.read_bytes()
            assert not sync.SECRET.search(data)
            if source.suffix == '.json':
                json.loads(data.decode('utf-8-sig'))
            destination = source.relative_to(ROOT) if source.parent == A and source.suffix == '.py' else PREFIX / source.relative_to(A)
            targets[destination.as_posix()] = data
            files[source.relative_to(ROOT).as_posix()] = {
                'published_path': destination.as_posix(), 'raw_sha256': sync.sha(data)}
        handoff = sync.read(A / 'idle_dependency_queue_handoff_20261006/verification.json')
        targets[(PREFIX / '.gitattributes').as_posix()] = b'* -text\n'
        targets[(PREFIX / 'manifest.json').as_posix()] = sync.encoded({
            'status': 'verified_idle26_handoff_current_lightweight_queue_preserved7_active_jobs',
            'at_local': sync.now(), 'previous_main': previous, 'files': files,
            'current_owned_jobs': {name: {'pid': row['owned_worker_pid'], 'creation_time': row['owned_worker_creation_time']}
                                   for name, row in jobs.items()},
            'required_rounds_retained': list(range(67, 89)), 'handoff': handoff, 'audit': audit,
            'original_scientific_sources_protocols_and_parameters_unchanged': True,
            'only_publication_branch': 'main', 'test_labels_read': False, 'new_quality_scores': 0})
        targets[(PREFIX / 'README.md').as_posix()] = (
            '# 等待任务的内存释放与原验证范围保留\n\n'
            '26个任务尚未进入训练或评分，却因导入计算库合计占用约4.92GiB工作进程内存。'
            '逐一核对进程命令、创建时间、等待状态、CPU活动和原前置条件后，'
            '仅关闭这些等待进程，替换为约24MiB的无窗口依赖队列。'
            '现场可用内存实际增加约4.18GiB；正在执行的训练、R81评分和两个观测进程均保留。\n\n'
            '原67—88轮、全部模型参数、完整评分网格、训练成熟边界、原资源门槛及冻结源码保持。'
            '条件满足后启动原科学程序，其内部仍执行全部严格资格检查。'
            '初版队列尚未启动任何科学任务时，发现R66应使用原独立恢复证明，'
            '已保留初版并以v2调用与原驱动相同的严格资格检查；实际R66探测通过。\n\n'
            '本同步保存两次交接证明、当前队列及所有输入散列复核。'
            '既有弹窗修复已在前一main提交保存；新队列沿用经实际检验的无窗口启动函数。'
            '本次没有新模型评分，也没有据此认定优化目标或计算边界已完成。\n'
        ).encode('utf-8')
        for name, data in targets.items():
            sync.atomic(sync.WORKTREE / name, data)
        paths = sorted(targets)
        for offset in range(0, len(paths), 50):
            sync.git('add', '-f', '--', *paths[offset:offset+50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(paths)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
                 '将26个等待任务移交轻量队列并保留67至88轮完整验证', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        expected = {name: hashlib.sha256(data).hexdigest() for name, data in targets.items()}
        assert blob_hashes(commit, expected) == expected
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        verify_main(commit)
        watcher.advance_source_index(commit)
        assert all(owned(row) for row in jobs.values())
        receipt = {'status': 'pushed_verified_idle_handoff_main_only', 'at_local': sync.now(),
            'commit': commit, 'raw_git_blob_sha256_verified': len(expected),
            'original_required_rounds_retained': list(range(67, 89)),
            'url': f'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/{PREFIX.as_posix()}'}
        with (OUT / 'receipt.json').open('x', encoding='utf-8') as stream:
            json.dump(receipt, stream, ensure_ascii=False, indent=2)
            stream.write('\n')
        print(json.dumps(receipt, ensure_ascii=False), flush=True)
    finally:
        for process in reversed(suspended):
            if process.is_running():
                process.resume()


if __name__ == '__main__':
    main()
