"""Checkpoint actual completion separately from unscored proposals and queued speed work."""
from pathlib import Path
import sys
import time
import json
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create
from monitor_actual_chronological_optimization_progress_v29_20261008 import snapshot, status


def main():
    actual = snapshot()
    assert actual['best_fully_qualified']['round'] == 139
    full = A / 'optimization_20261003_r139/full_registration_execution.json'
    receipt = A / 'github_validation_sync_main_20261005/round139_receipt.json'
    delivery_path = A / 'latest_verified_submission_delivery_v2_20261008.json'
    delivery = read(delivery_path)
    assert read(full)['status'] == 'passed' and read(receipt)['status'] == 'pushed_and_remote_head_verified'
    assert delivery['selected_round'] == 139
    csv = Path(delivery['output']) / 'submission.csv'
    manifest = csv.parent / 'submission_manifest.json'
    assert sha(csv) == delivery['csv_sha256'] and sha(manifest) == delivery['manifest_sha256']
    inputs = [Path(__file__), full, receipt, delivery_path, manifest,
              A / 'deferred_full_board_benchmark_preparation_v1_20261008.json',
              A / 'HuberCrossFamilyFine146_historical_receiver_preparation_v1_20261008.json',
              A / 'HuberCrossFamilyFine146_first_factory_failure_v1_20261008.json']
    create(A / 'actual_optimization_checkpoint_v31_20261008.json', {
        'status': 'progress_actual139_fully_qualified_main_delivery_and_further_feasible_directions',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'deadline_local': '2026-10-10T23:59:00+08:00',
        'best_fully_qualified': actual['best_fully_qualified'], 'submission_delivery': delivery,
        'actual_best_gain_over136': actual['best_fully_qualified']['score'] - actual['pipeline']['136']['scoring_winner']['score'],
        'actual_complete_rankings_records_at139': 14176, 'actual139_full_QA_version': 50,
        'actual139_official_scoring_cases': 112, 'actual139_future_rows': 1599600,
        'pipeline': actual['pipeline'], 'fine146_controls': actual['fine146_frontier'],
        'isolated_speed_benchmark': actual['isolated_serialization_benchmark'],
        'storage_relocation_service': status('Git_publisher_original_D_path_verified_E_relocation_v4_20261008'),
        'new_speed_runtime_not_adopted': True, 'fine146_quality_receivers_still_required': True,
        'all_initial_preparation_failures_preserved': True, 'main29_and30_evidence_publications_queued': True,
        'actual_free_storage_GiB': actual['free_storage_GiB'], 'actual_available_RAM_GiB': actual['available_memory_GiB'],
        'input_sha256': {str(p): sha(p) for p in inputs}, 'new_scores_by_checkpoint': 0,
        'competition_platform_upload_performed': False, 'test_labels_read': False,
        'optimization_goal_remains_active': True, 'global_feasible_direction_exhaustion_proven': False,
        'global_compute_resource_exhaustion_proven': False})
    print(json.dumps({'status': 'checkpointed', 'best_round': 139,
                      'score': actual['best_fully_qualified']['score'], 'submission': str(csv)}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
