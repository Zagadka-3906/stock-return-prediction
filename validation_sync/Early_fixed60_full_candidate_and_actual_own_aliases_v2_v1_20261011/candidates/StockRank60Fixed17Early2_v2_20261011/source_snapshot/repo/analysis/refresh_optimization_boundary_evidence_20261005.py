"""Retain established boundaries and add the newly evidenced latest-graph gap."""
from pathlib import Path
from datetime import datetime
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
from refresh_optimization_boundary_evidence_20261004 import complete_round_evidence
from locked_read_hash_cache_20261004 import fresh_sha


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    import refresh_optimization_boundary_evidence_20261004 as original
    original.main()
    analysis = ROOT / 'analysis'
    plan_path = analysis / 'latest_graph_joint_search_plan_20261005.json'
    audit_path = analysis / 'latest_graph_joint_axes_scope_audit_20261005/verification.json'
    plan, audit = read(plan_path), read(audit_path)
    assert audit['status'] == 'passed_actual_graph_routing_audit_only'
    assert fresh_sha(plan_path) == audit['prepared_plan_sha256']
    closed = complete_round_evidence(63)
    target = analysis / 'optimization_boundary_evidence_20261004.json'
    value = read(target)
    direction = {'method': 'Joint reoptimization of the latest complete graph after later accepted model additions',
        'required_official_rounds': [63], 'actual_completed_official_rounds': [63] if closed else [],
        'remaining_required_official_rounds': [] if closed else [63],
        'plan': str(plan_path.relative_to(ROOT)), 'plan_sha256': fresh_sha(plan_path),
        'coverage_audit': str(audit_path.relative_to(ROOT)), 'coverage_audit_sha256': fresh_sha(audit_path),
        'current_reference_active_axes': audit['actual_selected_r59_active_axes'],
        'later_axes_missing_from_original_r50_joint_search': audit['not_covered_in_r50_joint_search'],
        'conditional_reference_scored_records': plan['current_reference_expected_records'],
        'actual_axes_and_arm_count_must_be_refrozen_after_r62': True,
        'reason': 'The original joint grid predates two accepted later branches; its cached axes also retain an inactive old branch. Actual current effective parameters must be jointly reevaluated.',
        'quality_and_fullfuture_evidence_pending': closed is None,
        'prepared_plan_is_not_actual_quality_or_candidate_evidence': True}
    if closed:
        value['completed_declared_method_scopes'].append({'method': direction['method'],
            'rounds': [63], 'evidence': closed, 'finite_scope_only': True})
    else:
        value['open_feasible_directions'].append(direction)
    value['latest_graph_joint_coverage_evidence'] = direction
    value['additional_boundary_refresh_source'] = str(Path(__file__).relative_to(ROOT))
    value['additional_boundary_refresh_source_sha256'] = fresh_sha(Path(__file__))
    value['updated_at_local'] = datetime.now().isoformat(timespec='seconds')
    value['global_resource_exhaustion_established'] = False
    write(target, value)
    directions_path = analysis / 'next_experiment_directions_20261003.json'
    directions = read(directions_path)
    entry = {'priority': 28, **direction,
        'status': 'completed_declared_joint_search' if closed else 'prepared_coverage_verified_full_execution_and_quality_pending',
        'new_model_fits': 0, 'new_quality_scores': 0 if not closed else closed['scored_records'],
        'test_labels_read': False}
    directions['directions'] = [d for d in directions['directions'] if d.get('priority') != 28] + [entry]
    write(directions_path, directions)
    print(json.dumps({'status': value['status'], 'latest_completed_round': value['latest_completed_round'],
        'open_feasible_directions': len(value['open_feasible_directions']), 'latest_graph_joint_actual_quality_complete': closed is not None}), flush=True)


if __name__ == '__main__':
    main()
