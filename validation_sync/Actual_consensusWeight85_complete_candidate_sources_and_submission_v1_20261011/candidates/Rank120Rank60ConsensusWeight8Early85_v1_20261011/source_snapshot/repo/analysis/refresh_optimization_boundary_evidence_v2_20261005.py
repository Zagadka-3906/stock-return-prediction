"""Add the verified but quality-pending agreement-gate experiment to boundaries."""
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
    import refresh_optimization_boundary_evidence_20261005 as original
    original.main()
    preflight = ROOT / 'analysis/agreement_gate_preflight_v2_20261005/verification.json'
    source_control = ROOT / 'analysis/agreement_gate_round64_source_preflight_20261005/verification.json'
    proof, source = read(preflight), read(source_control)
    assert proof['status'] == 'passed_actual_mature_oof_gate_controls'
    assert source['status'] == 'passed_actual_reference_graph_and_synthetic_generator_checks'
    closed = complete_round_evidence(64)
    entry = {'method': 'Same-day model agreement and diversity gated effective layer weights',
        'required_official_rounds': [64], 'actual_completed_official_rounds': [64] if closed else [],
        'remaining_required_official_rounds': [] if closed else [64],
        'preflight': str(preflight.relative_to(ROOT)), 'preflight_sha256': fresh_sha(preflight),
        'source_preflight': str(source_control.relative_to(ROOT)), 'source_preflight_sha256': fresh_sha(source_control),
        'actual_nonzero_mature_oof_primitive_cases': proof['actual_nonzero_gate_cases'],
        'actual_zero_strength_weight_cases': proof['actual_zero_strength_weight_cases'],
        'conditional_reference_gate_axes': len(source['actual_reference_gate_axes']),
        'conditional_reference_scored_records': source['conditional_reference_scored_records'],
        'actual_r63_axes_and_count_refreeze_required': True,
        'reason': 'Constant and market-regime weights were compared; stock-specific same-day model disagreement gates remain a distinct unscored complete-output direction.',
        'quality_and_fullfuture_evidence_pending': closed is None,
        'new_model_fits': 0, 'test_labels_read': False}
    target = ROOT / 'analysis/optimization_boundary_evidence_20261004.json'
    value = read(target)
    if closed:
        value['completed_declared_method_scopes'].append({'method': entry['method'], 'rounds': [64],
            'evidence': closed, 'finite_scope_only': True})
    else:
        value['open_feasible_directions'].append(entry)
    value['agreement_gate_coverage_evidence'] = entry
    value['additional_boundary_refresh_source'] = str(Path(__file__).relative_to(ROOT))
    value['additional_boundary_refresh_source_sha256'] = fresh_sha(Path(__file__))
    value['updated_at_local'] = datetime.now().isoformat(timespec='seconds')
    value['global_resource_exhaustion_established'] = False
    write(target, value)
    directions_path = ROOT / 'analysis/next_experiment_directions_20261003.json'
    directions = read(directions_path)
    directions['directions'] = [d for d in directions['directions'] if d.get('priority') != 29] + [{
        'priority': 29, **entry, 'status': 'completed_declared_gate_search' if closed else 'primitive_and_source_controls_passed_complete_output_quality_pending',
        'new_quality_scores': closed['scored_records'] if closed else 0}]
    write(directions_path, directions)
    print(json.dumps({'latest_completed_round': value['latest_completed_round'],
        'open_feasible_directions': len(value['open_feasible_directions']),
        'agreement_gate_full_quality_complete': closed is not None}), flush=True)


if __name__ == '__main__':
    main()
