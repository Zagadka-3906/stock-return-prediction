"""Actual owned-controller and original-grid checks; not full198 quality evidence."""
from pathlib import Path
import hashlib
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
OUT = A / 'quantile_tree_memmap_controller_wiring_20261006'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    from run_dependency_queue_v3_20261006 import owned
    assert not OUT.exists()
    OUT.mkdir()
    old = read(A / 'quantile_tree_quality_queue_20261006/plan.json')
    new = read(A / 'quantile_tree_quality_queue_v2_20261006/plan.json')
    assert new['rounds'] == old['rounds'] == [91, 92]
    assert new['expected_full_records'] == old['expected_full_records'] == [100, 98]
    assert new['explicit_parents'] == old['explicit_parents'] == [90, 91]
    for filename, digest in old['input_sha256'].items():
        assert sha(filename) == digest and new['input_sha256'][filename] == digest
    for filename, digest in new['input_sha256'].items():
        assert sha(filename) == digest
    controls = {}
    for name in ('progress_monitor_v22', 'quantile_tree_memmap_complete_workflow',
                 'quantile_tree_quality_queue_v2', 'quantile_tree_memmap_native_promotion',
                 'dependency_queue_v4', 'main_publisher_v5', 'neural16384_annual'):
        row = read(A / f'service_owned_workflows_20261006/{name}/native_launch.json')
        assert owned(row) and row['actual_native_console_handle'] == 0
        assert row['independent_launch_root_in_any_job'] is False
        controls[name] = row
    capacity = read(A / 'quantile_tree_memmap_capacity_20261006/verification.json')
    assert capacity['status'] == 'passed_actual_four_largest_full_native_fits_and_complete_future_controls'
    assert capacity['actual_full_final_fits'] == capacity['actual300_iteration_models'] == 4
    assert capacity['actual_annual_fits'] == capacity['new_quality_scores'] == 0
    assert read(A / 'service_owned_workflows_20261006/quantile_tree_memmap_capacity/service_execution.json')['status'] == 'passed'
    published = read(A / 'quantile_tree_memmap_capacity_github_20261006/receipt.json')
    assert published['status'] == 'pushed_actual_controls_main_only' and published['control_status'] == 'passed'
    protocol = read(A / 'quantile_tree_memmap_complete_bank_20261006/protocol.json')
    assert protocol['expected_annual_fits'] == 20 and protocol['expected_final_fits'] == 4
    assert protocol['expected_complete_validation_rows'] == 5635800
    assert protocol['same_original_full_mature_rows63_features_params_and_native_objectives']
    annual = []
    for path in (A / 'quantile_tree_memmap_complete_bank_20261006').glob('*/info_202[0-4].json'):
        info = read(path)
        assert info['status'] == 'passed' and info['actual_native_boosting_iterations'] == 300
        assert sha(path.parent / f'model_{info["year"]}.joblib') == info['model_sha256']
        assert sha(path.parent / f'raw_{info["year"]}.parquet') == info['prediction_sha256']
        reference = 'rank_ridge_l01' if info['configuration']['target'] == 'y_rank' else 'return_ridge_l01'
        assert info['training_meta'] == read(A / f'linear_bank_20261003/{reference}/info_{info["year"]}.json')['training_meta']
        annual.append({'model': info['model'], 'year': info['year'], 'rows': info['training_meta']['rows'],
                       'model_sha256': info['model_sha256']})
    assert annual, 'Observe at least one actual full annual model before wiring verification.'
    monitor = read(A / 'ongoing_optimization_state.json')
    assert monitor['actual_progress_monitor'].endswith('monitor_actual_optimization_progress_v22_20261006.py')
    assert monitor['quantile_tree_actual_completed_final_fits'] == 4
    assert 0 < monitor['quantile_tree_actual_completed_annual_fits'] <= len(annual)
    assert monitor['native_model_copies_excluded_from_new_fit_totals']
    assert not read(A / 'quantile_tree_quality_queue_v2_20261006/state.json')['actual_native_promotion_verified']
    handoff = read(A / 'progress_monitor_v22_handoff_recovery_20261006.json')
    assert handoff['status'] == 'passed_actual_new_observer_owned_and_old_observer_closed'
    assert not owned(handoff['old_ownership'])
    result = {'status': 'passed_actual_owned_native_and_preserved198_queue_wiring_controls',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'original_scientific_source_hashes_all_preserved': old['input_sha256'],
        'new_full_native_and_promotion_and198_quality_controllers_actual_owned': controls,
        'observed_actual_completed_annual_models': annual, 'actual_four_final_native_and_full_future_controls_passed': True,
        'actual_full_native_main_receipt': published, 'old_monitor_closed_new_monitor_actual_fit_counts_correct': True,
        'full20_annual_closure_and_exposure_and198_quality_not_yet_verified': True,
        'expected_full_quality_rounds': [91, 92], 'expected_quality_records': [100, 98], 'explicit_parents': [90, 91],
        'copies_excluded_from_additional_native_fit_counts': True, 'new_quality_scores': 0,
        'all_original67_through90_required_quality_rounds_retained': True,
        'test_labels_read': False, 'global_resource_boundary_established': False}
    with (OUT / 'verification.json').open('x', encoding='utf-8') as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


if __name__ == '__main__':
    main()
