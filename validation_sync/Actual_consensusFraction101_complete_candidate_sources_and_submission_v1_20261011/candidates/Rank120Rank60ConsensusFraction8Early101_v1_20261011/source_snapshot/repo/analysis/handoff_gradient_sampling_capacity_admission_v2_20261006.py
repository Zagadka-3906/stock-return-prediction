"""Retire only zero-fit waiting services and test complete native GOSS scope under a measured admission policy."""
from pathlib import Path
import json
import math
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
OUT = A / 'gradient_sampling_memmap_admission_v2_handoff_20261006'


def main():
    import psutil
    from handoff_distribution_views_progress_monitor_20261006 import read, sha, create
    from run_dependency_queue_v3_20261006 import owned
    from launch_service_owned_workflow_with_pwsh_20261006 import launch
    generation = A / 'gradient_sampling_memmap_admission_v2_source_generation_20261006.json'
    generated = read(generation)
    for path, digest in {**generated['original_sha256'], **generated['generated_sha256']}.items():
        assert sha(path) == digest
    quantile = A / 'quantile_tree_memmap_capacity_20261006/resource_summary.json'
    qproof = A / 'quantile_tree_memmap_capacity_20261006/verification.json'
    memory = read(quantile)
    assert memory['status'] == 'passed' and not memory['observation_errors']
    assert read(qproof)['status'] == 'passed_actual_four_largest_full_native_fits_and_complete_future_controls'
    assert read(qproof)['actual_full_final_fits'] == read(qproof)['actual300_iteration_models'] == 4
    reserve = math.ceil(max(8 * 1024**3, memory['maximum_target_and_descendant_rss_bytes'] + 4 * 1024**3) / 1024**3)
    assert reserve == 8
    assert psutil.virtual_memory().available >= reserve * 1024**3
    assert not OUT.exists()
    OUT.mkdir()
    old = {}
    for name in ('gradient_sampling_memmap_capacity', 'gradient_sampling_memmap_complete_workflow'):
        service = A / f'service_owned_workflows_20261006/{name}'
        row = read(service / 'native_launch.json')
        assert owned(row) and not (service / 'service_execution.json').exists()
        root, worker = psutil.Process(row['pid']), psutil.Process(row['owned_worker_pid'])
        assert root.create_time() == row['owned_parent_creation_time']
        assert root.cmdline()[1:] == worker.cmdline()[1:]
        assert not worker.children(recursive=True)
        old[name] = {'launch': row, 'root': root, 'worker': worker}
    capacity = A / 'gradient_sampling_memmap_capacity_20261006'
    assert not list(capacity.glob('*/model_2025.joblib'))
    assert not list(capacity.glob('scheduler_fit_hold_*'))
    assert not (A / 'gradient_sampling_memmap_complete_bank_20261006').exists()
    actors = {}
    for name in ('neural16384_annual', 'dependency_queue_v5', 'main_publisher_v5', 'progress_monitor_v25'):
        row = read(A / f'service_owned_workflows_20261006/{name}/native_launch.json')
        assert owned(row)
        actors[name] = row
    bases = read(A / 'service_owned_workflows_20261006/gradient_sampling_memmap_capacity/capacity_run.json')['input_sha256']
    sources = [Path(__file__), generation, quantile, qproof,
        A / 'gradient_sampling_all_annual_cache_controls_20261006/verification.json',
        *[Path(p) for p in generated['generated_sha256']],
        A / 'run_service_owned_windows_workflow_20261006.py',
        A / 'launch_service_owned_workflow_with_pwsh_20261006.py']
    pins = dict(bases)
    pins.update({str(p.resolve()): sha(p) for p in sources})
    for path, digest in pins.items():
        assert sha(path) == digest
    create(OUT / 'frozen_before_handoff.json', {'status': 'frozen_before_zero_fit_waiting_service_supersession',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins,
        'old_owned_zero_fit_services': {name: item['launch'] for name, item in old.items()},
        'active_scientific_and_other_service_actors_to_preserve': actors,
        'peer_full_quantile_actual_peak_bytes': memory['maximum_target_and_descendant_rss_bytes'],
        'new_admission_bytes': reserve * 1024**3, 'extra_margin_bytes': 4 * 1024**3,
        'quantile_observation_is_not_a_proven_GOSS_memory_upper_bound': True,
        'actual_GOSS_largest_fit_success_or_failure_required': True,
        'actual_original_GOSS_configs_full_rows_and300_rounds_preserved': True,
        'original_12GiB_waiting_attempt_preserved_without_fabricating_a_passed_execution': True,
        'new_quality_scores': 0, 'test_labels_read': False})
    suspended, new = [], {}
    try:
        for item in old.values():
            for process in (item['worker'], item['root']):
                process.suspend()
                suspended.append(process)
        assert not list(capacity.glob('*/model_2025.joblib')) and not list(capacity.glob('scheduler_fit_hold_*'))
        create(OUT / 'original_waiting_samples_snapshot.json', {
            'status': 'administrative_zero_fit_waiting_snapshot_not_terminal_native_evidence',
            'resource_samples_sha256': sha(capacity / 'actual_resource_samples.jsonl'),
            'actual_annual_fits': 0, 'actual_final_fits': 0,
            'actual_original_12GiB_waiting_protocol_sha256': sha(capacity / 'protocol.json')})
        for name, driver, arguments in (
            ('gradient_sampling_memmap_capacity_v2', 'verify_full2025_gradient_sampling_memmap_capacity_v2_20261006.py', None),
            ('gradient_sampling_memmap_complete_workflow_v2', 'run_gradient_sampling_memmap_full_workflow_v2_20261006.py', [])):
            service = A / f'service_owned_workflows_20261006/{name}'
            assert not service.exists()
            service.mkdir()
            service_pins = dict(pins)
            if arguments is None:
                run = service / 'capacity_run.json'
                create(run, {'status': 'frozen_before_original6_largest_GOSS_capacity_admission_v2_trial',
                    'input_sha256': pins, 'expected_full_final_fits': 6, 'actual_bank_annual_fits': 0,
                    'new_quality_scores': 0, 'original30_annual_and262_quality_records_preserved': True,
                    '8GiB_trial_uses_peer_full_window_measurement_with_extra4GiB_policy_margin': True,
                    'peer_measurement_is_not_a_GOSS_physical_boundary': True, 'test_labels_read': False})
                arguments = [str(run)]
                service_pins[str(run)] = sha(run)
            definition = service / 'job_definition.json'
            create(definition, {'name': name, 'driver': str(A / driver), 'arguments': arguments,
                'scratch': str(ROOT / f'tmp/service_owned_{name}'), 'input_sha256': service_pins,
                'bootstrap_sha256': sha(A / 'run_service_owned_windows_workflow_20261006.py'),
                'command_line': subprocess.list2cmdline([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8',
                    str(A / 'run_service_owned_windows_workflow_20261006.py'), str(definition)])})
            receipt = launch(definition, Path('C:/Users/esesl/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/powershell/pwsh.exe'))
            create(service / 'verified_hidden_launch.json', receipt)
            deadline = time.monotonic() + 90
            while not (service / 'native_launch.json').exists():
                assert time.monotonic() < deadline
                assert psutil.pid_exists(receipt['actual_launch_result']['ProcessId'])
                time.sleep(.2)
            row = read(service / 'native_launch.json')
            assert owned(row) and row['actual_native_console_handle'] == 0
            assert not row['independent_launch_root_in_any_job']
            new[name] = row
        for name, item in old.items():
            item['worker'].terminate()
            item['worker'].wait(timeout=10)
            if item['root'].is_running():
                item['root'].terminate()
                item['root'].wait(timeout=10)
            assert not owned(item['launch'])
            create(A / f'service_owned_workflows_20261006/{name}/administrative_supersession.json', {
                'status': 'deliberately_superseded_zero_fit_waiting_service_admission_policy_only',
                'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'actual_annual_fits': 0, 'actual_final_fits': 0,
                'source_handoff_record': str(OUT / 'frozen_before_handoff.json'),
                'no_passed_original_execution_fabricated': True, 'new_quality_scores': 0})
        suspended.clear()
        assert all(owned(row) for row in actors.values())
        assert all(owned(row) for row in new.values())
        create(OUT / 'verification.json', {'status': 'passed_actual_zero_fit_service_handoff_and_original_full_GOSS_admission_v2_trial_dispatched',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins,
            'new_actual_owned_services': new, 'old_actual_owned_services_retired': {n: v['launch'] for n, v in old.items()},
            'original_active_scientific_and_other_service_actors_preserved': actors,
            'original30_annual6_final300_rounds_and262_quality_records_preserved': True,
            'original_waiting_attempt_and_sources_not_edited': True,
            'new_admission_bytes': reserve * 1024**3,
            'full_native_trial_not_declared_passed_by_handoff': True,
            'scientific_training_or_scoring_workers_suspended': 0,
            'new_quality_scores': 0, 'test_labels_read': False, 'global_resource_boundary_established': False})
        print(json.dumps({'status': 'passed_actual_admission_v2_handoff', 'new_services': new}, ensure_ascii=False), flush=True)
    except BaseException as error:
        create(OUT / 'failure.json', {'status': 'failed_preserved_actual_admission_v2_handoff', 'error': f'{type(error).__name__}: {error}',
            'actual_new_services_started': new})
        raise
    finally:
        for process in reversed(suspended):
            if process.is_running():
                process.resume()


if __name__ == '__main__':
    main()
