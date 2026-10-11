"""Test original32 queue routes and strict R89 refusal without launching any scientist."""
from pathlib import Path
from copy import deepcopy
import ast
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create


def route_expression(source):
    tree = ast.parse(source)
    candidates = [keyword.value for node in ast.walk(tree) if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name)
        and node.func.value.id == 'run' and node.func.attr == 'update'
        for keyword in node.keywords if keyword.arg == 'original_script']
    assert len(candidates) == 1
    return compile(ast.Expression(candidates[0]), '<readonly_original_route_expression>', 'eval')


def main():
    from run_dependency_queue_v12_local_cache_and_R89_qualification_20261007 import source_namespace
    import qualified_round_recovery_evidence_v4_20261007 as qualification
    out = A / 'dependency_queue_v12_local_cache_routes_preflight_20261007'
    assert not out.exists()
    out.mkdir()
    plan_path = A / 'service_owned_dependency_queue_bootstrap_fields_recovery_v2_20261006/queue_plan.json'
    original_plan = read(plan_path)
    assert len(original_plan['deferred_jobs']) == 32
    plan = deepcopy(original_plan)
    marker = A / 'optimization_20261003_r110/full_registration_execution.json'
    assert not marker.exists()
    plan['complete_ranking_registration_serialization_markers'].append(str(marker))
    assert plan['deferred_jobs'] == original_plan['deferred_jobs']
    paths = [Path(__file__), plan_path, A / 'run_dependency_queue_v12_local_cache_and_R89_qualification_20261007.py',
        A / 'run_dependency_queue_v10_20261006.py', A / 'run_dependency_queue_v3_20261006.py',
        A / 'qualified_round_recovery_evidence_v4_20261007.py',
        A / 'run_classifier_consensus_round90_with_precise_gate_and_parent_cache_20261007.py',
        A / 'parent_graph_rank_cache_preflight_v3_20261007/verification.json',
        A / 'optimization_20261003_r89/provenance_scope_execution.json']
    pins = {str(p): sha(p) for p in paths}
    create(out / 'frozen_before_prospective_route_controls.json', {'input_sha256': pins,
        'actual_scientific_processes_to_launch': 0, 'new_model_fits': 0, 'new_official_scores': 0, 'test_labels_read': False})
    namespace, effective, patches = source_namespace(plan)
    source = (A / 'run_dependency_queue_v10_20261006.py').read_text(encoding='utf-8')
    old_expression, new_expression = route_expression(source), route_expression(effective)
    controls = []
    for job in plan['deferred_jobs']:
        if 'round' not in job:
            continue
        values = {'A': A, 'job': job, 'plan': plan, 'str': str}
        old, new = eval(old_expression, values), eval(new_expression, values)
        if job['round'] == 90:
            assert Path(new).name == 'run_classifier_consensus_round90_with_precise_gate_and_parent_cache_20261007.py'
            assert Path(old).name == 'run_recovery_qualified_workflow_with_exact_rank_cache_v2_20261006.py'
        else:
            assert old == new, job['name']
        controls.append({'name': job['name'], 'original_route': old, 'prospective_route': new,
            'only_R90_route_changed': job['round'] == 90})
    # A missing full110 closure prevents new quality writers. This does not
    # fabricate a completed candidate or alter any current queue state.
    for job in plan['deferred_jobs']:
        if job['gate'].get('quality_slot'):
            assert namespace['ready'](job, {}) is False
    direct = dict(namespace)
    exec(compile(effective, str(A / 'run_dependency_queue_v10_20261006.py'), 'exec'), direct)
    job90 = next(j for j in plan['deferred_jobs'] if j['name'] == 'round90')
    calls = []
    old_gate = qualification.complete_round_evidence
    def observed(number):
        calls.append(number)
        return old_gate(number)
    qualification.complete_round_evidence = observed
    try:
        assert direct['ready'](job90, {}) is False
        assert calls == [89]
    finally:
        qualification.complete_round_evidence = old_gate
        qualification.close()
    for path, digest in pins.items():
        assert sha(path) == digest, path
    create(out / 'verification.json', {'status': 'passed_original32_routes_and_R90_only_dispatch_and_strict89_qualification_source_controls',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins, 'literal_runtime_patches': patches,
        'actual_original_route_count': 32, 'original_deferred_jobs': original_plan['deferred_jobs'],
        'route_controls': controls, 'actual_R89_V4_qualification_returned_not_ready': True,
        'actual_failed_R89_scope_bytes_unchanged': True, 'required_actual_full110_marker_before_quality_dispatch': str(marker),
        'all_original_scientific_grids_parents_arguments_and_original_routes_preserved': True,
        'new_source_prospective_only_not_actual138_validation': True,
        'new_scientific_workers_launched': 0, 'new_native_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})


if __name__ == '__main__':
    main()
