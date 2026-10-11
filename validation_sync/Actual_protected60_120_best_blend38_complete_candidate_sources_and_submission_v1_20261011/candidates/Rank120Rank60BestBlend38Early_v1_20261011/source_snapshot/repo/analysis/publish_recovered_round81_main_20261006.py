"""Wait for real R81 recovery closure and publish all evidence using hidden children."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import time

import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
import publish_classifier_consensus_workflows_20261006 as helpers
import qualified_round_recovery_evidence_v3_20261006 as qualification
from recovered_round81_publication_adapter_20261006 import install

sync = helpers.sync
OUT = A / 'round81_recovered_publication_github_20261006'


def create(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    assert not OUT.exists()
    own_sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    original_popen, original_snapshot = subprocess.Popen, sync.snapshot
    child_events, lock = [], None

    def hidden_popen(arguments, *args, **kwargs):
        flags = kwargs.pop('creationflags', 0)
        flags &= ~(subprocess.CREATE_NEW_CONSOLE | subprocess.DETACHED_PROCESS)
        flags |= subprocess.CREATE_NO_WINDOW
        startup = kwargs.pop('startupinfo', None) or subprocess.STARTUPINFO()
        startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startup.wShowWindow = subprocess.SW_HIDE
        kwargs.setdefault('stdin', subprocess.DEVNULL)
        child_events.append({'program': str(arguments[0]), 'creationflags': flags, 'SW_HIDE': True})
        return original_popen(arguments, *args, creationflags=flags, startupinfo=startup, **kwargs)

    OUT.mkdir()
    try:
        subprocess.Popen = hidden_popen
        deadline = time.monotonic() + 1200
        evidence = None
        while time.monotonic() < deadline:
            failure = A / 'optimization_20261003_r81/publication_recovery_failure_v2_20261006.json'
            if failure.exists():
                raise RuntimeError('The second actual recovery failed; no completed-round export is permitted.')
            evidence = qualification.complete_round_evidence(81)
            if evidence is not None:
                break
            print(json.dumps({'status': 'waiting_for_actual_recovery_scope_service_completion_and_process_closure',
                'round': 81, 'at_local': sync.now()}), flush=True)
            time.sleep(15)
        assert evidence is not None, 'No fully qualified closed recovery within the bounded wait.'
        # The original publisher is absent; verify this before taking its stale lock.
        old_owner = sync.OUT / 'owner.lock'
        if old_owner.exists():
            owner = sync.read(old_owner)
            try:
                process = psutil.Process(owner['pid'])
                command = ' '.join(process.cmdline())
                assert not ('watch_validations_main' in command or 'sync_validated_rounds_main' in command)
            except psutil.NoSuchProcess:
                pass
        lock = sync.initialize()
        old = sync.git('rev-parse', 'HEAD')
        helpers.verify_main(old)
        assert not sync.git('status', '--porcelain')
        install(sync, qualification)
        manifest, targets = sync.snapshot(81)
        assert manifest['scored_records'] == 124 and manifest['connected_records'] == 9946
        assert manifest['scientific_evidence'] == evidence
        assert hashlib.sha256(Path(__file__).read_bytes()).hexdigest() == own_sha
        for filename, data in targets.items():
            sync.atomic(sync.WORKTREE / filename, data)
        selected = sorted(targets)
        for offset in range(0, len(selected), 50):
            sync.git('add', '-f', '--', *selected[offset:offset + 50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(selected)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            '完成第81轮124方案及完整来源锁恢复核验，保留失败证明和9946条完整榜', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        expected = {filename: hashlib.sha256(data).hexdigest() for filename, data in targets.items()}
        assert helpers.blob_hashes(commit, expected) == expected
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        helpers.verify_main(commit)
        helpers.watcher.advance_source_index(commit)
        receipt = {'status': 'pushed_and_remote_head_verified', 'round': 81, 'at_local': sync.now(),
            'commit': commit, 'branch': 'main', 'remote': sync.REMOTE,
            'official_score': manifest['metrics']['final_score'], 'scored_records': 124,
            'connected_records': 9946, 'raw_git_blobs_verified': len(expected),
            'all_publication_child_processes_explicitly_hidden': True,
            'original_failures_retained_and_closed_full_recovery_passed': True,
            'scheme_url': 'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/validation_sync/round81'}
        create(OUT / 'receipt.json', receipt)
        sync.atomic(sync.OUT / 'round81_receipt.json', sync.encoded(receipt))
        create(OUT / 'hidden_child_launches.json', {'status': 'passed_all_actual_publication_children_hidden',
            'at_local': sync.now(), 'calls': child_events})
        print(json.dumps(receipt, ensure_ascii=False), flush=True)
    except BaseException as error:
        create(OUT / 'failure.json', {'status': 'failed_preserved_publication_attempt',
            'at_local': sync.now(), 'error': f'{type(error).__name__}: {error}', 'child_calls': child_events})
        raise
    finally:
        sync.snapshot = original_snapshot
        try:
            qualification.close()
        finally:
            subprocess.Popen = original_popen
            if lock is not None and lock.exists() and sync.read(lock).get('pid') == os.getpid():
                lock.unlink()


if __name__ == '__main__':
    main()
