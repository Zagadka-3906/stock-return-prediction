"""Account for the full paired robust-regression direction; retain all older work."""
from pathlib import Path
from datetime import datetime
import json
import psutil
from refresh_optimization_boundary_evidence_20261004 import complete_round_evidence

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def main():
    import refresh_optimization_boundary_evidence_v16_20261005 as previous
    from atomic_optimization_observer_writes_20261005 import operational_writes, write
    with operational_writes('refresh_optimization_boundary_evidence_v16_20261005'):
        previous.main()
    closed = {number: complete_round_evidence(number) for number in (87, 88)}
    native_jobs = read(A / 'streaming_robust_regression_followups_20261005/verification.json')['native_jobs']
    ownership = []
    for job in native_jobs:
        try:
            p = psutil.Process(job['owned_worker_pid'])
            live = p.create_time() == job['owned_worker_creation_time'] and job['script'] in p.cmdline()
        except psutil.Error:
            live = False
        ownership.append({'kind': job['kind'], 'pid': job['owned_worker_pid'], 'owned_live_now': live})
    bank = A / 'streaming_robust_regression_bank_20261005'
    entry = {
        'method': 'Paired full raw63 streamed squared and Huber rank/return regressions',
        'required_official_rounds': [87, 88], 'explicit_parent_rounds': {'87': 86, '88': 87},
        'actual_completed_official_rounds': [n for n, e in closed.items() if e is not None],
        'remaining_required_official_rounds': [n for n, e in closed.items() if e is None],
        'scored_records_prespecified': {'87': 100, '88': 98},
        'new_native_configurations': 4, 'expected_actual_full_annual_fits': 20,
        'expected_actual_full_final_fits': 4,
        'actual_full_annual_infos_present': len(list(bank.glob('*/info_202[0-4].json'))),
        'actual_full_final_infos_present': len(list(bank.glob('*/info_2025.json'))),
        'actual_native_worker_ownership': ownership,
        'all_original67_through86_rounds_retained_and_required': True,
        'feature_and_target_scaling_only_mature_past_no_label_clipping': True,
        'actual16_small_controls_not_replacing_full20_annual4_final_or_quality': True,
        'same5635800_validation_rows_1212_continuous_days_original_official_scorer': True,
        'actual_fullfuture_reload_cold80_return_mapping_freeze_causality_candidates_ranking_required': True,
        'only_main_and_D_or_E_project_data': True,
        'finite_grid_not_global_method_or_resource_exhaustion': True, 'test_labels_read': False,
    }
    path = A / 'optimization_boundary_evidence_20261004.json'
    boundary = read(path)
    if entry['remaining_required_official_rounds']:
        boundary['open_feasible_directions'].append(entry)
    else:
        boundary['completed_declared_method_scopes'].append({
            'method': entry['method'], 'rounds': [87, 88], 'evidence': closed, 'finite_scope_only': True})
    boundary.update(robust_regression_coverage_evidence=entry,
        updated_at_local=datetime.now().isoformat(timespec='seconds'),
        additional_boundary_refresh_source=str(Path(__file__).relative_to(ROOT)),
        global_resource_exhaustion_established=False)
    write(path, boundary)
    path = A / 'next_experiment_directions_20261003.json'
    directions = read(path)
    directions['directions'] = [r for r in directions['directions'] if r.get('priority') != 41] + [
        {'priority': 41, **entry, 'status': 'actual_full_native_and_complete_quality_pending'
         if entry['remaining_required_official_rounds'] else 'completed_declared_robust_scope'}]
    write(path, directions)
