"""Reconcile every declared round, original prerequisite and actual resource handle."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import sys
import time

import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
from run_dependency_queue_20261006 import owned
OUT = A / 'current_optimization_scope_audit_20261006'

PLANS = (
    'neural16384_full_complete_search_plan_20261005.json',
    'linear_leaf_complete_search_plan_20261005.json',
    'linear_leaf_ensemble_complete_search_plan_20261005.json',
    'factorization_machine_complete_search_plan_20261005.json',
    'gradient_sampling_complete_search_plan_20261005.json',
    'memory_efficient_neural_complete_search_plan_20261005.json',
    'streaming_rank_classifier_complete_search_plan_20261005.json',
    'reference66_linear_leaf_complete_plan_20261005.json',
    'ready_fm_reference_complete_plan_20261005.json',
    'ready_classifier_reference_complete_plan_20261005.json',
    'ready_robust_reference_complete_plan_20261005.json',
    'ready_classifier_consensus_reference_complete_plan_v2_20261006.json')


def read(path):
    for _ in range(30):
        try:
            return json.loads(Path(path).read_text(encoding='utf-8-sig'))
        except json.JSONDecodeError:
            time.sleep(.1)
    raise RuntimeError('A mutable record did not yield a complete JSON snapshot.')


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def create(name, value):
    with (OUT / name).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    assert not OUT.exists()
    OUT.mkdir()
    progress = read(A / 'ongoing_optimization_state.json')
    queue = read(ROOT / progress['dependency_queue_registry'])
    plan_path = Path(queue['script_args'][0])
    queue_plan, queue_state = read(plan_path), read(plan_path.parent / 'state.json')
    registry = read(ROOT / progress['active_run_registry'])
    create('registered_rounds_snapshot.json', registry)
    create('queue_state_snapshot.json', queue_state)
    create('progress_snapshot.json', progress)
    sources = [Path(__file__), *[A / name for name in PLANS], plan_path,
               OUT / 'registered_rounds_snapshot.json', OUT / 'queue_state_snapshot.json',
               OUT / 'progress_snapshot.json', ROOT / '后续选模标准.md']
    bindings = {str(path): sha(path) for path in sources}
    create('frozen_before_audit.json', {'input_sha256': bindings,
        'mutable_records_captured_as_immutable_observation_snapshots': True,
        'new_quality_scores': 0, 'test_labels_read': False})
    expected, origins = {}, {}
    for name in PLANS:
        doc = read(A / name)
        counts = next(doc[key] for key in ('expected_total_records', 'planned_records', 'scored_records_prespecified') if key in doc)
        for number, count in counts.items():
            number = int(number)
            assert number not in expected
            expected[number], origins[number] = count, name
            if 'wave_arm_counts' in doc:
                assert sum(doc['wave_arm_counts'][str(number)]) == count
    assert sorted(expected) == list(range(67, 91))
    assert set(expected) <= {row['round'] for row in registry}
    assert sum(expected.values()) == 2760
    jobs = {**queue_plan['preserved_active_jobs'], **queue_state['activated_jobs']}
    assert owned(queue)
    assert all(owned(row) for row in queue_plan['preserved_active_jobs'].values())
    first = {name: sum(psutil.Process(row['owned_worker_pid']).cpu_times()[:2])
             for name, row in jobs.items() if owned(row)}
    time.sleep(1)
    observations = []
    for name, row in jobs.items():
        if not owned(row):
            observations.append({'job': name, 'owned_live_now': False})
            continue
        p = psutil.Process(row['owned_worker_pid'])
        observations.append({'job': name, 'owned_live_now': True, 'pid': p.pid,
            'creation_time': p.create_time(), 'RSS_bytes': p.memory_info().rss,
            'CPU_seconds': sum(p.cpu_times()[:2]),
            'CPU_seconds_delta_over1s': sum(p.cpu_times()[:2]) - first[name]})
    from qualified_round_recovery_evidence_v2_20261005 import complete_round_evidence, close
    rows = []
    try:
        for number, count in sorted(expected.items()):
            folder = A / f'optimization_20261003_r{number}'
            waves = {path.stem: read(path) for path in folder.glob('wave*_results.json')}
            actual = sum(len(payload['results']) for payload in waves.values())
            assert actual <= count, (number, actual, count)
            qualified = complete_round_evidence(number)
            rows.append({'round': number, 'declared_records': count,
                'records_saved_in_current_attempt': actual, 'records_remaining_to_score': count - actual,
                'scope_qualified_complete': qualified is not None, 'closed_scope_evidence': qualified,
                'declared_plan': origins[number],
                'waves': {name: {'status': value['status'], 'records': len(value['results'])} for name, value in waves.items()}})
    finally:
        close()
    gates = []
    for job in queue_plan['deferred_jobs']:
        markers = []
        for marker in job['gate'].get('markers', []):
            path = Path(marker['path'])
            status = read(path).get('status') if path.exists() else None
            passed = path.exists() and ('statuses' not in marker or status in marker['statuses'])
            markers.append({'path': str(path), 'exists': path.exists(), 'status': status, 'gate_satisfied_now': passed})
        gates.append({'job': job['name'], 'activated': job['name'] in queue_state['activated_jobs'],
            'required_parent_round': job['gate'].get('parent'), 'markers': markers,
            'must_wait_for_live_jobs_to_close': [name for name in job['gate'].get('closed_jobs', []) if name in jobs and owned(jobs[name])],
            'serial_quality_slot_required': job['gate'].get('quality_slot', False)})
    assert all(sha(path) == digest for path, digest in bindings.items())
    evidence = {'status': 'passed_all24_declared_rounds_retained_with_live_resource_evidence',
        'at_local': datetime.now().isoformat(timespec='seconds'), 'rounds': rows,
        'total_declared_records': sum(expected.values()),
        'records_saved': sum(row['records_saved_in_current_attempt'] for row in rows),
        'records_remaining_to_score': sum(row['records_remaining_to_score'] for row in rows),
        'rounds_remaining_to_qualify': [row['round'] for row in rows if not row['scope_qualified_complete']],
        'original67_to80_declared_records': sum(expected[n] for n in range(67, 81)),
        'original67_to88_scopes_preserved': True, 'current_jobs': observations,
        'queue_gates': gates, 'host_available_bytes': psutil.virtual_memory().available,
        'wide14GiB_reserve_satisfied_now': psutil.virtual_memory().available >= 14 * 2**30,
        'wide_reserve_is_admission_policy_not_evidence_of_physical_exhaustion': True,
        'wide_and_robust_fit_workers_owned_live_now': all(owned(jobs[n]) for n in ('neural16384_annual', 'robust_annual')),
        'historical_closed_grids_not_proof_of_unfinished_direction_quality': True,
        'finite_plan_coverage_not_claim_of_all_possible_methods_exhausted': True,
        'global_method_and_resource_boundary_established': False,
        'goal_complete': False, 'new_native_fits_by_audit': 0,
        'new_quality_scores_by_audit': 0, 'test_labels_read': False}
    create('verification.json', evidence)
    print(json.dumps({key: evidence[key] for key in ('status', 'total_declared_records', 'records_saved',
        'records_remaining_to_score', 'rounds_remaining_to_qualify', 'wide14GiB_reserve_satisfied_now')}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
