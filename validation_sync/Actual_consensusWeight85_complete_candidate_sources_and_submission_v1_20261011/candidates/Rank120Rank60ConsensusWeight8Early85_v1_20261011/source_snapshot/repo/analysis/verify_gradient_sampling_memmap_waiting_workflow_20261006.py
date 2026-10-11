"""Check actual consoleless dispatch, all annual proof bindings and unchanged original quality scope."""
from pathlib import Path
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
OUT = A / 'gradient_sampling_memmap_waiting_workflow_controls_20261006'


def main():
    import psutil
    import train_gradient_sampling_memmap_bank_20261006 as bank
    from run_dependency_queue_v3_20261006 import owned
    from handoff_distribution_views_progress_monitor_20261006 import read, sha, create
    from locked_read_hash_cache_20261004 import LockedReadHashCache
    assert not OUT.exists()
    OUT.mkdir()
    service = A / 'service_owned_workflows_20261006/gradient_sampling_memmap_complete_workflow'
    definition = read(service / 'job_definition.json')
    launch = read(service / 'native_launch.json')
    assert owned(launch) and launch['actual_native_console_handle'] == 0
    assert not launch['independent_launch_root_in_any_job']
    assert launch['original_driver'] == str(A / 'run_gradient_sampling_memmap_full_workflow_20261006.py')
    assert launch['original_arguments'] == []
    assert not (service / 'service_execution.json').exists()
    capacity_service = A / 'service_owned_workflows_20261006/gradient_sampling_memmap_capacity'
    capacity = read(capacity_service / 'native_launch.json')
    assert owned(capacity) and capacity['actual_native_console_handle'] == 0
    assert not (capacity_service / 'service_execution.json').exists()
    assert not (bank.CAPACITY / 'verification.json').exists()
    assert not bank.OUT.exists(), 'The full bank must not freeze or train before all6 actual capacity closures.'
    original = read(A / 'gradient_sampling_complete_search_plan_20261005.json')
    assert bank.CONFIGS == original['model_configurations']
    assert original['expected_annual_fits'] == len(bank.CONFIGS) * len(bank.YEARS) == 30
    assert original['expected_complete_final_fits'] == len(bank.CONFIGS) == 6
    assert original['planned_records'] == {'75': 124, '76': 138}
    assert original['actual_previous_selection_required'] == {'75': 74, '76': 75}
    queue = read(A / 'service_owned_dependency_queue_v4_20261006/queue_plan_v5.json')
    jobs = {j['name']: j for j in queue['deferred_jobs']}
    for number, parent in ((75, 74), (76, 75)):
        assert jobs[f'round{number}']['gate']['parent'] == parent
        assert jobs[f'round{number}']['gate']['quality_slot']
        assert any(Path(m['path']) == A / 'gradient_sampling_future_qa_20261005/verification.json'
                   and m['statuses'] == ['passed'] for m in jobs[f'round{number}']['gate']['markers'])
    assert not (A / 'gradient_sampling_future_qa_20261005/verification.json').exists()
    assert not (A / 'gradient_sampling_bank_20261005/oof_audit.json').exists()
    actors = {}
    for name in ('dependency_queue_v5', 'main_publisher_v5', 'neural16384_annual', 'progress_monitor_v25'):
        row = read(A / f'service_owned_workflows_20261006/{name}/native_launch.json')
        assert owned(row)
        actors[name] = row
    proof = read(bank.CACHE_PROOF)
    assert proof['status'] == 'passed_all5_full_original_GOSS_annual_preprocessing_targets_and_maturity'
    assert [x['full_actual_training_shape'][0] for x in proof['checks']] == [1694259, 2594048, 3568878, 4597785, 5659954]
    pins = dict(definition['input_sha256'])
    for path in (Path(__file__), service / 'native_launch.json', service / 'job_definition.json',
                 A / 'gradient_sampling_complete_search_plan_20261005.json',
                 A / 'service_owned_dependency_queue_v4_20261006/queue_plan_v5.json'):
        pins[str(path.resolve())] = sha(path)
    with LockedReadHashCache(pins):
        assert owned(launch) and owned(capacity)
    create(OUT / 'verification.json', {'status': 'passed_actual_full_GOSS_waiting_workflow_and_all5_cache_controls_original_scope_preserved',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins,
        'actual_full_workflow_owned_launch': launch, 'actual_pending_capacity_owned_launch': capacity,
        'original_active_actors_preserved': actors, 'original30_annual_and6_final_required': True,
        'original75_76_parents_and124_plus138_quality_grid_preserved': True,
        'old_native_and_future_dependency_jobs_remain_preserved_for_later_qualified_supersession': True,
        'actual_all5_full_cache_checks': proof['checks'],
        'actual_shared_cache_files_rewritten': 0, 'actual_new_native_fits_by_this_check': 0,
        'actual30_annual_and6_final_and262_quality_not_yet_completed': True,
        'actual_host_available_bytes_at_observation': psutil.virtual_memory().available,
        'largest_capacity_wait_is_specific_verified_live_handle': True,
        'new_quality_scores': 0, 'test_labels_read': False, 'physical_resource_boundary_established': False})


if __name__ == '__main__':
    main()
