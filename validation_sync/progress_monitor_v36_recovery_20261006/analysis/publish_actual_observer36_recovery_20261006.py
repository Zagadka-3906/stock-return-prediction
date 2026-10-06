"""Publish actual observer recovery and its first verified complete generation."""
from pathlib import Path
import gzip
import hashlib
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, create, sha, owned
OUT = A / 'progress_monitor_v36_recovery_github_20261006'


def main():
    service = A / 'service_owned_workflows_20261006/progress_monitor_v36'
    identity = read(service / 'native_launch.json')
    public = [A / n for n in ('ongoing_optimization_state.json', 'resume_optimization_20261004.json',
                              'actual_optimization_monitor_state_20261005.json')]
    assert not OUT.exists()
    OUT.mkdir()
    while True:
        assert owned(identity), read(service / 'service_execution.json')
        data = [p.read_bytes() for p in public]
        docs = [json.loads(b.decode('utf-8-sig')) for b in data]
        generations = {d.get('complete_observer_generation') for d in docs}
        if len(generations) == 1 and None not in generations and all(d.get('actual_observer_version') == 36 for d in docs):
            assert docs[-1]['pid'] == identity['owned_worker_pid']
            assert all(d['completed_validation_best'] == 0.45109699933205216 for d in docs)
            break
        time.sleep(30)
    copied = []
    for source, content in zip(public, data):
        destination = OUT / 'first_complete_generation' / source.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(content)
        copied.append(destination)
    create(OUT / 'verification.json', {'status': 'passed_actual_owned_observer36_complete_generation',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'identity': identity,
        'complete_observer_generation': next(iter(generations)),
        'source_snapshot_sha256': {str(p): sha(p) for p in copied},
        'actual_original_failed_observer34_preserved': True,
        'actual_complete_board_records': docs[-1]['completed_board_records'],
        'actual_qualified_best': docs[-1]['completed_validation_best'],
        'scientific_workers_stopped_or_restarted': 0, 'new_quality_scores': 0,
        'global_resource_exhaustion_established': False, 'test_labels_read': False})
    from hidden_windows_child_creation_20261006 import install
    from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
    import publish_classifier_consensus_workflows_20261006 as helpers
    sync = helpers.sync
    restore = install()
    held = []
    try:
        publisher = read(A / 'service_owned_workflows_20261006/main_publisher_v7/native_launch.json')
        parent, worker, idle = suspended_idle(publisher, '    main (watch_validations_main_v7_20261006.py:71)')
        held.extend((worker, parent))
        create(OUT / 'main7_verified_idle_hold.json', idle)
        sources = [Path(__file__), A / 'monitor_completed_worker_safe_v36_20261006.py',
            A / 'monitor_actual_optimization_progress_v34_20261006.py',
            *OUT.glob('*.json'), *copied,
            *(A / 'progress_monitor_v36_recovery_20261006').glob('*.json'),
            *(A / 'service_owned_workflows_20261006/progress_monitor_v34').glob('*.json'),
            A / 'service_owned_workflows_20261006/progress_monitor_v34/stderr.log',
            *service.glob('*.json')]
        prefix = Path('validation_sync/progress_monitor_v36_recovery_20261006')
        payload, files = {}, {}
        for source in dict.fromkeys(sources):
            raw = source.read_bytes()
            assert not sync.SECRET.search(raw), source
            target = (prefix / source.relative_to(ROOT)).as_posix()
            encoded = raw
            if len(raw) >= 5 * 1024**2:
                encoded = gzip.compress(raw, mtime=0)
                assert gzip.decompress(encoded) == raw
                target += '.gz'
            payload[target] = encoded
            files[target] = {'sha256': hashlib.sha256(encoded).hexdigest(),
                'original_sha256': hashlib.sha256(raw).hexdigest(), 'original_bytes': len(raw),
                'lossless_original_bytes_preserved': True}
        payload[(prefix / 'manifest.json').as_posix()] = sync.encoded({
            'status': 'actual_observer36_recovery_and_first_complete_generation', 'files': files,
            'only_publication_branch': 'main', 'new_training_scoring_inference_or_QA': False,
            'test_labels_read': False})
        payload[(prefix / '.gitattributes').as_posix()] = b'* -text\n'
        previous = sync.git('rev-parse', 'HEAD')
        helpers.verify_main(previous)
        assert not sync.git('status', '--porcelain')
        for path, content in payload.items(): sync.atomic(sync.WORKTREE / path, content)
        paths = sorted(payload)
        for offset in range(0, len(paths), 50): sync.git('add', '-f', '--', *paths[offset:offset + 50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(paths)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
                 '修复正常退出进程的进度观察并保存第102轮完整状态证据', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        hashes = {p: hashlib.sha256(b).hexdigest() for p, b in payload.items()}
        assert helpers.blob_hashes(commit, hashes) == hashes
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        helpers.verify_main(commit)
        helpers.watcher.advance_source_index(commit)
        create(OUT / 'receipt.json', {'status': 'pushed_and_remote_head_verified', 'commit': commit,
            'branch': 'main', 'raw_git_blobs_verified': len(hashes), 'at_local': sync.now(),
            'url': 'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/' + prefix.as_posix()})
        print(json.dumps(read(OUT / 'receipt.json'), ensure_ascii=False), flush=True)
    finally:
        for process in reversed(held):
            if process.is_running(): process.resume()
        create(OUT / 'actual_hidden_children.json', {'events': restore()})


if __name__ == '__main__':
    main()
