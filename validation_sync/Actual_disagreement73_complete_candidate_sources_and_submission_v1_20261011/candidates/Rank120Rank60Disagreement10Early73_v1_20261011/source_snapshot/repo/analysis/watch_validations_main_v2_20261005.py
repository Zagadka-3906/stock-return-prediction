"""Continue qualified round publication on main; the source checkout retains its files."""
from pathlib import Path
import os
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
import sync_validated_rounds_main_20261005 as sync

DELEGATE = Path(sync.__file__)
sync.__file__ = str(Path(__file__))


def advance_source_index(commit):
    assert sync.git('branch', '--show-current', cwd=ROOT) == 'main'
    old = sync.git('rev-parse', 'refs/heads/main', cwd=ROOT)
    if old == commit:
        return
    # A prior-round receipt is historical; never rewind the newer main tip.
    prior = sync.subprocess.run(['git', 'merge-base', '--is-ancestor', commit, old], cwd=ROOT, capture_output=True)
    if prior.returncode == 0:
        return
    assert prior.returncode == 1, prior.stderr.decode('utf-8', errors='replace')
    sync.git('merge-base', '--is-ancestor', old, commit)
    if old != commit:
        sync.git('update-ref', 'refs/heads/main', commit, old, cwd=ROOT)
        sync.git('read-tree', '--reset', commit, cwd=ROOT)
    # Historical exports were intentionally cleaned locally. Keep them remote and
    # in the index, without checking out a second set into the research workspace.
    raw = sync.subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT)
    missing = [name for name in raw.split(b'\0') if name and not (ROOT / name.decode('utf-8')).exists()]
    if missing:
        sync.subprocess.run(['git', 'update-index', '--skip-worktree', '-z', '--stdin'],
            cwd=ROOT, input=b'\0'.join(missing) + b'\0', check=True, capture_output=True)


def main():
    run = sync.read(ROOT / 'analysis/github_validation_sync_main_20261005/run_v2.json')
    bindings = {str(path): sync.sha(path.read_bytes()) for path in (Path(__file__), DELEGATE)}
    assert all(run['input_sha256'][path] == digest for path, digest in bindings.items())
    lock = sync.initialize()
    try:
        while True:
            assert all(sync.sha(Path(path).read_bytes()) == digest for path, digest in bindings.items())
            latest = None
            try:
                rounds = sorted(int(path.stem.rsplit('_r', 1)[1]) for path in
                                (ROOT / 'results').glob('optimization_20261003_r*.json'))
                for number in rounds:
                    if number >= 60 and sync.complete_round_evidence(number) is not None:
                        latest = sync.sync_round(number)
                        advance_source_index(latest['commit'])
                state = {'status': 'monitoring_completed_validations', 'pid': os.getpid(),
                    'at_local': sync.now(), 'branch': 'main', 'latest_synced': latest,
                    'all_history_preserved_by_main_fast_forward': True, 'poll_seconds': 45}
            except Exception as error:
                state = {'status': 'sync_failed_retry_pending', 'pid': os.getpid(), 'at_local': sync.now(),
                    'branch': 'main', 'error': f'{type(error).__name__}: {error}', 'retry_seconds': 45}
                print(sync.json.dumps(state, ensure_ascii=False), flush=True)
            sync.atomic(sync.OUT / 'state.json', sync.encoded(state))
            time.sleep(45)
    finally:
        if lock.exists() and sync.read(lock).get('pid') == os.getpid():
            lock.unlink()


if __name__ == '__main__':
    main()
