"""Verify the live lightweight queue, frozen scope and recovered R66 gate."""
from copy import deepcopy
from datetime import datetime
from pathlib import Path
import json
import sys

import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
from run_dependency_queue_20261006 import read, sha, create, owned
from run_dependency_queue_v2_20261006 import ready

OUT = A / 'dependency_queue_handoff_audit_20261006'
QUEUE = A / 'idle_dependency_queue_handoff_v2_20261006'


def main():
    assert not OUT.exists()
    OUT.mkdir()
    plan = read(QUEUE / 'plan.json')
    row = read(QUEUE / 'launch.json')
    assert owned(row)
    sources = {**plan['input_sha256'], str(Path(__file__)): sha(__file__)}
    create(OUT / 'frozen_before_audit.json', {'input_sha256': sources,
        'queue_owned_worker': row, 'test_labels_read': False})
    for path, digest in sources.items():
        assert sha(path) == digest, path
    state = read(QUEUE / 'state.json')
    assert not state['activated_jobs']
    jobs = dict(plan['preserved_active_jobs'])
    assert all(owned(job) for job in jobs.values())
    rounds = [job['round'] for job in plan['deferred_jobs'] if 'round' in job]
    assert sorted(rounds + [81]) == list(range(67, 89))
    readiness = {job['name']: ready(job, jobs) for job in plan['deferred_jobs']}
    assert not any(readiness.values()), readiness
    # Exercise the authoritative completed-R66 check without pretending that
    # the still-running wide model or global scoring slot is available.
    probe = deepcopy(next(job for job in plan['deferred_jobs'] if job['name'] == 'round67'))
    probe['gate'] = {'parent': 66}
    assert ready(probe, {})
    import qualified_round_recovery_evidence_v2_20261005 as qualification
    qualification.close()
    for path, digest in sources.items():
        assert sha(path) == digest, path
    assert owned(row) and all(owned(job) for job in jobs.values())
    assert not read(QUEUE / 'state.json')['activated_jobs']
    create(OUT / 'verification.json', {
        'status': 'passed_live_queue_all_frozen_sources_and_original_scope',
        'at_local': datetime.now().isoformat(timespec='seconds'),
        'queue_worker': row['owned_worker_pid'],
        'queue_RSS_bytes': psutil.Process(row['owned_worker_pid']).memory_info().rss,
        'all7_preserved_workers_positively_owned': True,
        'deferred_jobs': len(plan['deferred_jobs']), 'actual_readiness': readiness,
        'strict_authoritative_recovered_R66_gate_passed': True,
        'all_original_required_rounds_retained': list(range(67, 89)),
        'all_input_sha256_reverified': True, 'new_model_fits': 0,
        'new_quality_scores': 0, 'test_labels_read': False,
        'physical_resource_boundary_established': False})
    print(json.dumps(read(OUT / 'verification.json'), ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
