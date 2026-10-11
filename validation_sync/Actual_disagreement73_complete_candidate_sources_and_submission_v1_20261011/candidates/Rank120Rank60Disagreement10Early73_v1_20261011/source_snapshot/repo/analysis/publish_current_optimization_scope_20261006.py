"""Publish the full declared-scope audit with the current main branch invariant."""
from pathlib import Path
import hashlib
import json

import publish_classifier_consensus_workflows_20261006 as previous

sync, ROOT, A = previous.sync, previous.ROOT, previous.A
PREFIX = Path('validation_sync/current_optimization_scope_20261006')


def main():
    out = A / 'current_optimization_scope_github_20261006'
    assert not out.exists()
    audit = A / 'current_optimization_scope_audit_20261006'
    evidence = sync.read(audit / 'verification.json')
    assert evidence['status'] == 'passed_all24_declared_rounds_retained_with_live_resource_evidence'
    assert evidence['total_declared_records'] == 2760
    plan = sync.read(previous.HANDOFF / 'queue_plan.json')
    pairs = [previous.owned_pair(plan['preserved_active_jobs'][name]['pid'],
             Path(plan['preserved_active_jobs'][name]['script']), plan['preserved_active_jobs'][name]['script_args'])
             for name in ('main_publisher', 'progress_monitor')]
    suspended = []
    out.mkdir()
    try:
        for parent, worker in pairs:
            assert not [p for p in parent.children(recursive=True)
                        if p.pid != worker.pid and p.name().lower() != 'conhost.exe']
            for process in (worker, parent):
                process.suspend()
                suspended.append(process)
        old = sync.git('rev-parse', 'HEAD')
        previous.verify_main(old)
        assert not sync.git('status', '--porcelain')
        sources = [Path(__file__), A / 'audit_current_optimization_scope_20261006.py']
        targets = {source.relative_to(ROOT).as_posix(): source.read_bytes() for source in sources}
        targets.update({(PREFIX / path.name).as_posix(): path.read_bytes() for path in audit.glob('*.json')})
        targets[(PREFIX / '.gitattributes').as_posix()] = b'* -text\n'
        targets[(PREFIX / 'README.md').as_posix()] = (
            '# 尚未完成的优化范围与真实资源状态\n\n'
            '根据12份原冻结计划逐轮核对67—90轮，合计2,760条预定官方评分；'
            '其中原67—80轮1,578条全部保留。审计时R81保存120条，剩余2,640条尚待评分。'
            '评分条目保存不代表完整方案资格检查、候选推理和榜单更新已经完成。\n\n'
            '现场核验原七个工作进程的命令、创建时间、内存和一秒CPU变化，'
            '并逐项保存队列前置证明与需要关闭的任务。'
            '宽网络14GiB预留条件未满足是下一次训练的启动条件，当前训练仍在运行，'
            '不能用这一调度条件认定物理资源耗尽。所有未完成范围保留，目标仍未完成。'
            '快照与核验均有独立时间标记；未增加模型训练或质量评分，未读取测试标签。\n'
        ).encode('utf-8')
        for name, data in targets.items():
            assert not sync.SECRET.search(data)
            sync.atomic(sync.WORKTREE / name, data)
        sync.git('add', '-f', '--', *targets)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
                 '核对67至90轮2760个评分配置与实际资源等待条件', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        expected = {name: hashlib.sha256(data).hexdigest() for name, data in targets.items()}
        assert previous.blob_hashes(commit, expected) == expected
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        previous.verify_main(commit)
        previous.watcher.advance_source_index(commit)
        receipt = {'status': 'pushed_verified_all24_round_scope_main_only', 'commit': commit,
            'at_local': sync.now(), 'raw_git_blob_sha256_verified': len(expected),
            'url': f'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/{PREFIX.as_posix()}'}
        with (out / 'receipt.json').open('x', encoding='utf-8') as stream:
            json.dump(receipt, stream, ensure_ascii=False, indent=2)
        print(json.dumps(receipt, ensure_ascii=False), flush=True)
    finally:
        for process in reversed(suspended):
            if process.is_running():
                process.resume()


if __name__ == '__main__':
    main()
