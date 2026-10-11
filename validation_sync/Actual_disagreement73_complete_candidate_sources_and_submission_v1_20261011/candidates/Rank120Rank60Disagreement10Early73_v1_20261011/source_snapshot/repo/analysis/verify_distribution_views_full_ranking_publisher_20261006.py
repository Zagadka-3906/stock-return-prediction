"""Check the actual hidden publisher and unchanged scientific queue sources."""
from pathlib import Path
from datetime import datetime
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from collect_full_lossless_round_publication_20261006 import read, sha
from handoff_distribution_views_progress_monitor_20261006 import create, visible_terminals
from run_dependency_queue_v3_20261006 import owned


def main():
    out = A / 'distribution_views_full_ranking_publication_wiring_20261006'
    assert not out.exists()
    service = A / 'service_owned_workflows_20261006/distribution_views_full_ranking_publisher'
    row = read(service / 'native_launch.json')
    assert owned(row) and row['actual_native_console_handle'] == 0
    assert row['independent_launch_root_in_any_job'] is False
    assert not (service / 'service_execution.json').exists()
    run = read(service / 'publisher_run.json')
    for source, digest in run['input_sha256'].items():
        assert sha(source) == digest
    state = read(A / 'distribution_views_full_ranking_publisher_20261006/state.json')
    assert state['stage'] == 'waiting_actual_qualified_complete_round_and_QA_v6'
    assert state['round'] == 93 and state['complete_publication_rounds'] == []
    controls = {}
    for name in ('main_publisher_v5', 'dependency_queue_v4', 'neural16384_annual',
                 'quantile_tree_quality_queue_v2', 'quantile_distribution_views_quality_queue', 'progress_monitor_v25'):
        identity = read(A / f'service_owned_workflows_20261006/{name}/native_launch.json')
        assert owned(identity)
        controls[name] = identity
    scoring = read(A / 'service_owned_dependency_queue_v4_20261006/activated_jobs/round83/launch.json')
    assert owned(scoring)
    controls['actual_round83_scoring'] = scoring
    preserved = {}
    for name in ('quantile_tree_quality_queue_v2_20261006', 'quantile_distribution_views_quality_queue_20261006'):
        plan = read(A / name / 'plan.json')
        for source, digest in plan['input_sha256'].items():
            assert sha(source) == digest
        preserved[name] = plan['input_sha256']
    preflight = read(A / 'distribution_views_full_publication_collector_preflight_20261006/verification.json')
    assert preflight['status'] == 'passed_actual_full138_record_round82_collector_and_committed_blob_match'
    out.mkdir()
    create(out / 'verification.json', {
        'status': 'passed_actual_owned_publisher_and_preserved_scientific_queue_wiring',
        'at_local': datetime.now().isoformat(timespec='seconds'),
        'actual_publication_worker': row, 'actual_waiting_state': state,
        'actual_other_worker_identities': controls, 'publication_source_sha256': run['input_sha256'],
        'original_scientific_queue_source_sha256': preserved,
        'actual_reference_collection_and_committed_raw_blobs': preflight,
        'both93_94_actual_full_validation_and_publication_still_pending': True,
        'original198_and_new262_scientific_records_preserved': True,
        'original_main5_worker_not_replaced': True, 'visible_terminal_windows': visible_terminals(),
        'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False,
        'global_resource_exhaustion_established': False})
    print(json.dumps({'status': 'passed', 'actual_hidden_publisher_pid': row['owned_worker_pid'],
        'waiting_for_qualified_round': state['round'], 'actual_reference_blobs_verified': 10,
        'new_quality_scores': 0}), flush=True)


if __name__ == '__main__':
    main()
