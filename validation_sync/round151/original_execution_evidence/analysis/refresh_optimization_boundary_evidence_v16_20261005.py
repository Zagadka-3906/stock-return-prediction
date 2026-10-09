"""Retain all required work and account for the complete ready-classifier chain."""
from pathlib import Path
from datetime import datetime
import json
from refresh_optimization_boundary_evidence_20261004 import complete_round_evidence

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def main():
    import refresh_optimization_boundary_evidence_v15_20261005 as previous
    from atomic_optimization_observer_writes_20261005 import operational_writes, write
    with operational_writes('refresh_optimization_boundary_evidence_v15_20261005'):
        previous.main()
    path = A / 'optimization_boundary_evidence_20261004.json'
    boundary = read(path)
    closed = {n: complete_round_evidence(n) for n in (85, 86)}
    entry = {'method': 'Complete mature streamed-classifier schemes after qualified lightweight reference chain',
        'required_official_rounds': [85, 86], 'explicit_parent_rounds': {'85': 84, '86': 85},
        'actual_completed_official_rounds': [n for n, e in closed.items() if e is not None],
        'remaining_required_official_rounds': [n for n, e in closed.items() if e is None],
        'scored_records_prespecified': {'85': 100, '86': 98},
        'new_native_configurations': 0, 'new_native_fits': 0,
        'all_prior_rounds67_through84_retained_and_required': True,
        'existing_actual_annual_fits_required': 20, 'existing_actual_final_fits_required': 4,
        'actual_final_artifacts_present': len(list((A / 'streaming_rank_classification_bank_v3_20261005').glob('*/info_2025.json'))),
        'same5635800_validation_rows_1212_continuous_days_and_original_official_scorer': True,
        'actual_generator_proof': 'analysis/ready_classifier_reference_generator_preflight_20261005/verification.json',
        'actual_execution_source_controls': 'analysis/ready_classifier_reference_execution_preflight_20261005/verification.json',
        'actual20_full_annual_model_audit': 'analysis/streaming_classifier_actual_annual_completion_audit_20261005/verification.json',
        'one_worker_layout_only_all_original_arms_and_forecast_math_preserved': True,
        'actual4_final_fullfuture_QA_and_complete_official_candidates_still_required': True,
        'finite_grid_not_global_method_or_resource_exhaustion': True, 'test_labels_read': False}
    if entry['remaining_required_official_rounds']:
        boundary['open_feasible_directions'].append(entry)
    else:
        boundary['completed_declared_method_scopes'].append({'method': entry['method'],
            'rounds': [85, 86], 'evidence': closed, 'finite_scope_only': True})
    boundary.update(ready_classifier_reference_coverage_evidence=entry,
        updated_at_local=datetime.now().isoformat(timespec='seconds'),
        additional_boundary_refresh_source=str(Path(__file__).relative_to(ROOT)),
        global_resource_exhaustion_established=False)
    write(path, boundary)
    path = A / 'next_experiment_directions_20261003.json'
    directions = read(path)
    directions['directions'] = [row for row in directions['directions'] if row.get('priority') != 40] + [
        {'priority': 40, **entry, 'status': 'actual_complete_reference_quality_pending'
         if entry['remaining_required_official_rounds'] else 'completed_declared_ready_classifier_scope'}]
    write(path, directions)
