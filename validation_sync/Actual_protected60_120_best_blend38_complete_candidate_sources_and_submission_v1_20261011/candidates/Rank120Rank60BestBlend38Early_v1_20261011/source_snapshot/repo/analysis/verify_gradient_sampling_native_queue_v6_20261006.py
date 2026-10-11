"""Check actual original pending driver routes and dispatch hold without launching scientific jobs."""
from pathlib import Path
from copy import deepcopy
import ast
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]


def main():
    from handoff_distribution_views_progress_monitor_20261006 import read, sha, create
    import run_dependency_queue_v5_20261006 as old
    import run_dependency_queue_v6_20261006 as new
    from run_dependency_queue_v3_20261006 import owned
    output = A / 'gradient_sampling_native_queue_v6_preflight_20261006'
    assert not output.exists()
    plan_path = A / 'service_owned_dependency_queue_v4_20261006/queue_plan_v5.json'
    plan = read(plan_path)
    old_path, new_path = Path(old.__file__), Path(new.__file__)
    old_ast, new_ast = ast.parse(old_path.read_text(encoding='utf-8-sig')), ast.parse(new_path.read_text(encoding='utf-8-sig'))
    for name in ('spawn', 'original_driver_and_bridge'):
        a = next(n for n in old_ast.body if isinstance(n, ast.FunctionDef) and n.name == name)
        b = next(n for n in new_ast.body if isinstance(n, ast.FunctionDef) and n.name == name)
        assert ast.dump(a, include_attributes=False) == ast.dump(b, include_attributes=False), name
    source_record = read(A / 'gradient_sampling_native_queue_v6_source_generation_20261006.json')
    assert sha(old_path) == source_record['original_sha256'] and sha(new_path) == source_record['new_sha256']
    state = read(plan_path.parent / 'state.json')
    jobs = {**plan['preserved_active_jobs'], **state['activated_jobs']}
    assert owned(read(A / 'service_owned_workflows_20261006/dependency_queue_v5/native_launch.json'))
    original_gates = {job['name']: deepcopy(job['gate']) for job in plan['deferred_jobs']}
    new._PROMOTION_PROOF = A / 'gradient_sampling_memmap_native_promotion_20261006/verification.json'
    assert not new._PROMOTION_PROOF.exists()
    assert all(new.ready(job, jobs) is False for job in plan['deferred_jobs'])
    new._PROMOTION_PROOF = None
    checks = []
    for job in plan['deferred_jobs']:
        if 'round' not in job:
            continue
        run = read(job['previous_run'])
        old_route = old.original_driver_and_bridge(job, run)
        new_route = new.original_driver_and_bridge(job, run)
        assert old_route == new_route
        checks.append({'name': job['name'], 'round': job['round'], 'parent': job['gate']['parent'],
            'original_driver': new_route[0], 'original_arguments': new_route[1],
            'original_previous_run_sha256': sha(job['previous_run'])})
    assert len(checks) == 23
    assert original_gates['round75']['parent'] == 74 and original_gates['round76']['parent'] == 75
    required = str(A / 'gradient_sampling_future_qa_20261005/verification.json')
    assert all(original_gates[f'round{number}']['markers'] == [{'path': required, 'statuses': ['passed']}] for number in (75, 76))
    assert all(job['gate'] == original_gates[job['name']] for job in plan['deferred_jobs'])
    output.mkdir()
    paths = [Path(__file__), old_path, new_path, plan_path,
        A / 'gradient_sampling_native_queue_v6_source_generation_20261006.json',
        A / 'promote_gradient_sampling_memmap_native_bank_20261006.py',
        A / 'handoff_gradient_sampling_native_to_original_queue_v6_20261006.py']
    create(output / 'verification.json', {'status': 'passed_actual23_original_routes_and_unclosed_promotion_dispatch_hold',
        'checks': checks, 'input_sha256': {str(p.resolve()): sha(p) for p in paths},
        'old_and_new_spawn_and_original_driver_bridge_AST_identical': True,
        'original_deferred_definitions_gates_and_parents_unchanged': True,
        'all_dispatch_held_until_actual_promotion_proof': True,
        'original30_annual6_final262_quality_scope_preserved': True,
        'full_native_promotion_and_controller_handoff_not_yet_executed': True,
        'new_native_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})
    print('passed_actual23_original_routes_and_unclosed_promotion_dispatch_hold', flush=True)


if __name__ == '__main__':
    main()
