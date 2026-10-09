"""Keep GOSS pilot controls, native fitting and official quality evidence distinct."""
from pathlib import Path
from datetime import datetime
import json

from refresh_optimization_boundary_evidence_20261004 import complete_round_evidence

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def main():
    import refresh_optimization_boundary_evidence_v8_20261005 as previous
    from atomic_optimization_observer_writes_20261005 import operational_writes, write
    with operational_writes('refresh_optimization_boundary_evidence_v8_20261005'):
        previous.main()
    from refresh_optimization_boundary_evidence_20261004 import complete_round_evidence
    import refresh_gradient_sampling_cost_evidence_20261005 as costs
    with operational_writes('refresh_gradient_sampling_cost_evidence_20261005'):
        costs.main()
    plan = read(ROOT / 'analysis/gradient_sampling_complete_search_plan_20261005.json')
    cost = read(ROOT / 'analysis/optimization_fit_cost_evidence_20261004.json')
    bank = Path(read(ROOT / 'analysis/gradient_sampling_storage_20261005.json')['output_directory'])
    completed = {n: complete_round_evidence(n) for n in (75, 76)}
    entry = {'method': 'Matched GOSS gradient sampling rates on original63 features',
        'required_official_rounds': [75, 76],
        'actual_completed_official_rounds': [n for n, evidence in completed.items() if evidence is not None],
        'remaining_required_official_rounds': [n for n, evidence in completed.items() if evidence is None],
        'scored_records_prespecified': plan['planned_records'], 'expected_annual_fits': 30, 'expected_final_fits': 6,
        'actual_annual_fits': cost['gradient_sampling_actual_annual_fits'],
        'actual_fulltraining_artifacts': cost['gradient_sampling_actual_fulltraining_artifacts'],
        'actual_annual_execution_status': read(bank / 'training_execution_scope.json')['status']
            if (bank / 'training_execution_scope.json').exists() else 'pending',
        'actual_native_future_status': read(ROOT / 'analysis/gradient_sampling_future_qa_20261005/verification.json')['status']
            if (ROOT / 'analysis/gradient_sampling_future_qa_20261005/verification.json').exists() else 'pending',
        'actual_pilot_controls': 'analysis/gradient_sampling_preflight_20261005/verification.json',
        'actual_direct6_pilot_and30_inherited_codec_controls': 'analysis/gradient_sampling_direct_router_preflight_20261005/verification.json',
        'actual_generator_controls': 'analysis/gradient_sampling_search_generator_preflight_20261005/verification.json',
        '48round_pilots_not_substituted_for300round_full_fits': True,
        'same_training_matrices_targets_keys_and_parameters_except_sampling_required': True,
        'native_training_device': 'cpu', 'RAM_reserve_is_scheduling_policy': True,
        'finite_grid_not_global_method_or_resource_exhaustion': True, 'test_labels_read': False}
    path = ROOT / 'analysis/optimization_boundary_evidence_20261004.json'
    value = read(path)
    if entry['remaining_required_official_rounds']:
        value['open_feasible_directions'].append(entry)
    else:
        value['completed_declared_method_scopes'].append({'method': entry['method'],
            'rounds': [75, 76], 'evidence': completed, 'finite_scope_only': True})
    value.update(gradient_sampling_coverage_evidence=entry, updated_at_local=datetime.now().isoformat(timespec='seconds'),
        additional_boundary_refresh_source=str(Path(__file__).relative_to(ROOT)), global_resource_exhaustion_established=False)
    write(path, value)
    path = ROOT / 'analysis/next_experiment_directions_20261003.json'
    directions = read(path)
    directions['directions'] = [row for row in directions['directions'] if row.get('priority') != 35] + [
        {'priority': 35, **entry, 'status': 'actual_native_fits_and_complete_quality_pending'
            if entry['remaining_required_official_rounds'] else 'completed_declared_GOSS_scope'}]
    directions['last_completed_round'] = value['latest_completed_round']
    directions['validation_best_completed'] = value['completed_best']
    write(path, directions)
