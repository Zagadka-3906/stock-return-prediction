"""Append the full artifact and live-window recheck to the same main workflow."""
from pathlib import Path
import hashlib
import json

import psutil
import publish_classifier_consensus_workflows_20261006 as previous

sync, A, ROOT = previous.sync, previous.A, previous.ROOT


def main():
    out = A / 'classifier_consensus_recheck_github_20261006'
    assert not out.exists()
    proof = A / 'classifier_consensus_current_artifact_recheck_20261006/verification.json'
    check = sync.read(proof)
    assert check['status'] == 'passed_current_consensus_artifacts_queue_ownership_and_window_recheck'
    assert not check['visible_project_python_windows'] and check['annual_virtual_outputs_rehashed'] == 30
    plan = sync.read(previous.HANDOFF / 'queue_plan.json')
    assert all(previous.owned(row) for row in plan['preserved_active_jobs'].values())
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
        targets = {'analysis/' + Path(__file__).name: Path(__file__).read_bytes(),
            (previous.PREFIX / 'postpublication_recheck/verification.json').as_posix(): proof.read_bytes()}
        for name, data in targets.items():
            assert not sync.SECRET.search(data)
            sync.atomic(sync.WORKTREE / name, data)
        sync.git('add', '-f', '--', *targets)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
                 '复核36份分类集成产物、原模型散列及后台窗口状态', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        expected = {name: hashlib.sha256(data).hexdigest() for name, data in targets.items()}
        assert previous.blob_hashes(commit, expected) == expected
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        previous.verify_main(commit)
        previous.watcher.advance_source_index(commit)
        receipt = {'status': 'pushed_verified_consensus_recheck_main_only', 'commit': commit,
            'at_local': sync.now(), 'raw_git_blob_sha256_verified': len(expected),
            'url': f'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/{previous.PREFIX.as_posix()}'}
        with (out / 'receipt.json').open('x', encoding='utf-8') as stream:
            json.dump(receipt, stream, ensure_ascii=False, indent=2)
        print(json.dumps(receipt, ensure_ascii=False), flush=True)
    finally:
        for process in reversed(suspended):
            if process.is_running():
                process.resume()


if __name__ == '__main__':
    main()
