"""Continue main-only publication with actual recovery gates and hidden child creation."""
from pathlib import Path
import hashlib
import json
import os
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]


def main():
    from hidden_windows_child_creation_20261006 import install as hide_children
    restore_children = hide_children()
    import qualified_round_recovery_evidence_v3_20261006 as qualification
    import watch_validations_main_v2_20261005 as retained
    from finalize_main_branch_consolidation_20261005 import verify_main
    from recovered_round66_publication_adapter_20261005 import install as recover66
    from recovered_round81_publication_adapter_v2_20261006 import install as recover81
    from lossless_round_publication_adapter_v2_20261006 import install as lossless
    from verified_round_main_publication_20261006 import publish
    sync = retained.sync
    own_sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    old_gate, old_snapshot = sync.complete_round_evidence, sync.snapshot
    sync.complete_round_evidence = qualification.complete_round_evidence
    recover66(sync)
    recover81(sync, qualification)
    lossless(sync)
    lock = None
    try:
        verify_main(sync.git('rev-parse', 'HEAD'))
        lock = sync.initialize()
        while True:
            assert hashlib.sha256(Path(__file__).read_bytes()).hexdigest() == own_sha
            latest = None
            try:
                rounds = sorted(int(path.stem.rsplit('_r', 1)[1]) for path in
                    (ROOT / 'results').glob('optimization_20261003_r*.json'))
                for number in rounds:
                    if number < 60:
                        continue
                    receipt = sync.OUT / f'round{number}_receipt.json'
                    if receipt.exists():
                        saved = sync.read(receipt)
                        if saved.get('status') == 'pushed_and_remote_head_verified' and saved.get('branch') == 'main':
                            latest = saved
                            continue
                    try:
                        if qualification.complete_round_evidence(number) is not None:
                            latest = publish(sync, number)
                    finally:
                        qualification.close()
                state = {'status': 'monitoring_completed_validations', 'pid': os.getpid(),
                    'at_local': sync.now(), 'branch': 'main', 'latest_synced': latest,
                    'actual_R81_recovery_required': True, 'all_actual_child_creations_hidden': True,
                    'entire_future_lossless_ranking_and_actual_full_QA_required': True, 'poll_seconds': 45}
            except Exception as error:
                state = {'status': 'sync_failed_retry_pending', 'pid': os.getpid(),
                    'at_local': sync.now(), 'branch': 'main', 'error': f'{type(error).__name__}: {error}',
                    'retry_seconds': 45}
            sync.atomic(sync.OUT / 'state_v5_20261006.json', sync.encoded(state))
            print(json.dumps(state, ensure_ascii=False), flush=True)
            time.sleep(45)
    finally:
        sync.snapshot, sync.complete_round_evidence = old_snapshot, old_gate
        try:
            qualification.close()
        finally:
            if lock is not None and lock.exists() and sync.read(lock).get('pid') == os.getpid():
                lock.unlink()
            restore_children()


if __name__ == '__main__':
    main()
