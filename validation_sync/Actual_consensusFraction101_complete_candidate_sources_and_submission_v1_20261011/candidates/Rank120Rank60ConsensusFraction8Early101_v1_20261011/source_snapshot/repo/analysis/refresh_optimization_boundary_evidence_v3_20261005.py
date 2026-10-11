"""Record expanded kernels as an open empirical scope, preserving broad boundaries."""
from pathlib import Path
from datetime import datetime
import json

ROOT = Path(__file__).resolve().parents[1]
from refresh_optimization_boundary_evidence_20261004 import complete_round_evidence
from locked_read_hash_cache_20261004 import fresh_sha


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    import refresh_optimization_boundary_evidence_v2_20261005 as original
    original.main()
    cost = read(ROOT / 'analysis/optimization_fit_cost_evidence_20261004.json')
    proof = ROOT / 'analysis/nystrom_tuning_search_generator_preflight_v2_20261005/verification.json'
    assert read(proof)['status'] == 'passed'
    completed = {number: complete_round_evidence(number) for number in (65, 66)}
    storage = read(ROOT / 'analysis/nystrom_tuning_storage_20261005.json')
    native = ROOT / 'analysis/nystrom_tuning_future_qa_20261005/verification.json'
    entry = {'method': 'Matched Nyström capacity, lengthscale and ridge penalty contrasts',
        'required_official_rounds': [65, 66],
        'actual_completed_official_rounds': [number for number, evidence in completed.items() if evidence],
        'remaining_required_official_rounds': [number for number, evidence in completed.items() if evidence is None],
        'declared_configurations': 10, 'expected_annual_fits': 50, 'expected_fulltraining_artifacts': 10,
        'actual_annual_fits': cost['nystrom_tuning_actual_annual_fits'],
        'actual_fulltraining_artifacts': cost['nystrom_tuning_actual_fulltraining_artifacts'],
        'bank_protocol': str(Path(storage['output_directory']) / 'protocol.json'),
        'generator_proof': str(proof.relative_to(ROOT)), 'generator_proof_sha256': fresh_sha(proof),
        'native_future_status': read(native)['status'] if native.exists() else 'pending',
        'scored_records_prespecified': {'65': 172, '66': 218},
        'broader_kernel_seeds_capacities_and_full16384_neural_fits_remain_uncovered': True,
        'finite_grid_only_not_global_method_exhaustion': True, 'test_labels_read': False}
    path = ROOT / 'analysis/optimization_boundary_evidence_20261004.json'
    value = read(path)
    if entry['remaining_required_official_rounds']:
        value['open_feasible_directions'].append(entry)
    else:
        value['completed_declared_method_scopes'].append({'method': entry['method'], 'rounds': [65, 66],
            'evidence': completed, 'finite_scope_only': True})
    value.update(nystrom_tuning_coverage_evidence=entry,
        additional_boundary_refresh_source=str(Path(__file__).relative_to(ROOT)),
        additional_boundary_refresh_source_sha256=fresh_sha(Path(__file__)),
        updated_at_local=datetime.now().isoformat(timespec='seconds'), global_resource_exhaustion_established=False)
    write(path, value)
    path = ROOT / 'analysis/next_experiment_directions_20261003.json'
    directions = read(path)
    directions['directions'] = [row for row in directions['directions'] if row.get('priority') != 30] + [{
        'priority': 30, **entry, 'status': 'native_training_and_complete_output_quality_pending'
        if entry['remaining_required_official_rounds'] else 'completed_declared_expanded_kernel_search'}]
    write(path, directions)
