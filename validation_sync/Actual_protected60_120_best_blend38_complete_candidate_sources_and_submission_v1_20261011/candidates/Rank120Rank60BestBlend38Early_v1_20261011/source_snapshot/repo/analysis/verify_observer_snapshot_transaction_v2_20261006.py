"""Exercise real disk isolation, complete commit, and failed-update rollback."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
import complete_observer_snapshot_transaction_v2_20261006 as tx
import atomic_optimization_observer_writes_20261005 as atomic
import refresh_continuous_progress_v2_20261005 as bound_producer


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    out = A / 'observer_snapshot_transaction_preflight_v2_20261006'
    assert not out.exists()
    out.mkdir()
    sources = {str(path): sha(path) for path in (Path(__file__).resolve(),
        A / 'complete_observer_snapshot_transaction_v2_20261006.py',
        A / 'monitor_actual_optimization_progress_v25_20261006.py')}
    public = {out / name for name in ('ongoing.json', 'resume.json', 'monitor.json')}
    for path in public:
        atomic.write(path, {'generation': 'prior', 'active_round': 83})
    real_public, tx.PUBLIC = tx.PUBLIC, public
    ordinary_read = Path.read_text
    original_producer_write = bound_producer.write
    bound_producer.write = atomic.write
    prior_bound_write = bound_producer.write
    try:
        prior = {path: path.read_bytes() for path in public}
        with tx.transaction() as (pending, commit):
            for path in public:
                bound_producer.write(path, {'active_round': 67, 'layer': 'intermediate'})
                assert json.loads(path.read_text())['active_round'] == 67
                assert path.read_bytes() == prior[path]
                path.write_text(json.dumps({'active_round': 83, 'layer': 'final'}), encoding='utf-8')
                assert json.loads(path.read_text())['active_round'] == 83
                assert path.read_bytes() == prior[path]
            commit('actual_preflight_complete_generation')
        assert bound_producer.write is prior_bound_write
        assert Path.read_text is ordinary_read
        for path in public:
            value = json.loads(path.read_text())
            assert value['active_round'] == 83
            assert value['complete_observer_generation'] == 'actual_preflight_complete_generation'
        before_failure = {path: path.read_bytes() for path in public}
        try:
            with tx.transaction():
                for path in public:
                    atomic.write(path, {'active_round': 67, 'unverified': True})
                raise RuntimeError('actual controlled failure before commit')
        except RuntimeError as error:
            assert str(error) == 'actual controlled failure before commit'
        assert all(path.read_bytes() == before_failure[path] for path in public)
        assert bound_producer.write is prior_bound_write
        assert Path.read_text is ordinary_read
        for path, digest in sources.items():
            assert sha(path) == digest
        atomic.write(out / 'verification.json', {
            'status': 'passed_actual_disk_isolation_commit_and_failed_update_rollback',
            'at_local': datetime.now().isoformat(timespec='seconds'), 'input_sha256': sources,
            'all3_intermediate_files_kept_off_public_disk': True,
            'actual_prebound_refresh_producer_alias_intercepted': True,
            'staged_reads_observed_current_intermediate_values': True,
            'all3_complete_files_commit_matching_generation': True,
            'failed_update_preserved_all3_prior_public_bytes': True,
            'scientific_sources_and_quality_gates_changed': False,
            'new_model_fits': 0, 'new_quality_scores': 0})
    finally:
        tx.PUBLIC = real_public
        bound_producer.write = original_producer_write
    print('Passed actual snapshot transaction controls.', flush=True)


if __name__ == '__main__':
    main()
