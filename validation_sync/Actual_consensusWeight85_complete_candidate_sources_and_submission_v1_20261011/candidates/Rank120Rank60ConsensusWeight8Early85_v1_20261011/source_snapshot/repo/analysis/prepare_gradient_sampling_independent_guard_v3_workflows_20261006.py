"""Preserve the pre-fit guard failure and execute the same native scope with a tested independent recovery guard."""
from pathlib import Path
import json
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
OUT = A / 'gradient_sampling_memmap_independent_guard_v3_wiring_20261006'


def main():
    from handoff_distribution_views_progress_monitor_20261006 import read, sha, create
    from run_dependency_queue_v3_20261006 import owned
    from launch_service_owned_workflow_with_pwsh_20261006 import launch
    control = A / 'scheduler_fit_guard_controls_v2_20261006/verification.json'
    assert read(control)['status'] == 'passed_actual_independent_WMI_guard_normal_and_abrupt_venv_owner_exit'
    generation = A / 'gradient_sampling_memmap_independent_guard_v3_source_generation_20261006.json'
    generated = read(generation)
    old = {}
    for name in ('gradient_sampling_memmap_capacity_v2', 'gradient_sampling_memmap_complete_workflow_v2'):
        folder = A / f'service_owned_workflows_20261006/{name}'
        row = read(folder / 'native_launch.json')
        assert not owned(row)
        assert read(folder / 'service_execution.json')['status'] == 'failed'
        old[name] = {'launch': row, 'terminal': read(folder / 'service_execution.json')}
    failed = A / 'gradient_sampling_memmap_capacity_v2_20261006'
    assert read(failed / 'failure.json')['actual_completed_models'] == []
    assert not list(failed.glob('*/model_2025.joblib'))
    assert not list(failed.glob('scheduler_fit_hold_*/actual_hold.json'))
    assert not list(failed.glob('scheduler_fit_hold_*/lease.json'))
    assert not (A / 'gradient_sampling_memmap_complete_bank_v2_20261006').exists()
    assert not OUT.exists()
    OUT.mkdir()
    pins = dict(read(A / 'service_owned_workflows_20261006/gradient_sampling_memmap_capacity_v2/capacity_run.json')['input_sha256'])
    sources = [Path(__file__), control, generation, A / 'owned_scheduler_native_fit_hold_v2_20261006.py',
        A / 'scheduler_fit_guard_controls_v2_20261006/protocol.json',
        failed / 'failure.json', failed / 'resource_summary.json',
        *[Path(p) for p in generated['generated_sha256']]]
    pins.update({str(p.resolve()): sha(p) for p in sources})
    for path, digest in {**generated['original_sha256'], **generated['generated_sha256'], **pins}.items():
        assert sha(path) == digest
        if Path(path).suffix == '.py':
            compile(Path(path).read_text(encoding='utf-8-sig'), path, 'exec')
    actors = {}
    for name in ('neural16384_annual', 'dependency_queue_v5', 'main_publisher_v5', 'progress_monitor_v25'):
        row = read(A / f'service_owned_workflows_20261006/{name}/native_launch.json')
        assert owned(row)
        actors[name] = row
    create(OUT / 'frozen_before_actual_dispatch.json', {'status': 'frozen_after_actual_guard_controls_before_native_trial',
        'input_sha256': pins, 'failed_actual_attempts': old,
        'failure_was_before_guard_launch_scheduler_suspend_or_any_native_model_fit': True,
        'root_WMI_process_outside_job_does_not_imply_venv_native_child_outside_job': True,
        'new_guard_root_is_independently_WMI_launched_and_both_real_exit_cases_verified': True,
        'actual_8GiB_trial_and_all_original6_full_fits30_annual_and262_quality_preserved': True,
        'new_quality_scores': 0, 'test_labels_read': False})
    launched = {}
    for name, driver, arguments in (
        ('gradient_sampling_memmap_capacity_v3', 'verify_full2025_gradient_sampling_memmap_capacity_v3_20261006.py', None),
        ('gradient_sampling_memmap_complete_workflow_v3', 'run_gradient_sampling_memmap_full_workflow_v3_20261006.py', [])):
        folder = A / f'service_owned_workflows_20261006/{name}'
        assert not folder.exists()
        folder.mkdir()
        bindings = dict(pins)
        if arguments is None:
            run = folder / 'capacity_run.json'
            create(run, {'status': 'frozen_before_original6_actual_full_GOSS_fits_with_tested_independent_guard',
                'input_sha256': pins, 'expected_full_final_fits': 6, 'actual_bank_annual_fits': 0,
                'new_quality_scores': 0, 'original30_annual_and262_quality_records_preserved': True,
                'guard_controls_passed_before_native_fit': True, 'test_labels_read': False})
            arguments = [str(run)]
            bindings[str(run)] = sha(run)
        definition = folder / 'job_definition.json'
        create(definition, {'name': name, 'driver': str(A / driver), 'arguments': arguments,
            'scratch': str(ROOT / f'tmp/service_owned_{name}'), 'input_sha256': bindings,
            'bootstrap_sha256': sha(A / 'run_service_owned_windows_workflow_20261006.py'),
            'command_line': subprocess.list2cmdline([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8',
                str(A / 'run_service_owned_windows_workflow_20261006.py'), str(definition)])})
        result = launch(definition, Path('C:/Users/esesl/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/powershell/pwsh.exe'))
        create(folder / 'verified_hidden_launch.json', result)
        deadline = time.monotonic() + 90
        while not (folder / 'native_launch.json').exists():
            assert time.monotonic() < deadline
            time.sleep(.1)
        row = read(folder / 'native_launch.json')
        assert owned(row) and row['actual_native_console_handle'] == 0 and not row['independent_launch_root_in_any_job']
        launched[name] = row
    assert all(owned(row) for row in actors.values())
    create(OUT / 'verification.json', {'status': 'passed_actual_independent_guard_v3_full_scope_dispatch_after_normal_and_abrupt_exit_controls',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins,
        'new_actual_owned_workflows': launched, 'original_active_actors_preserved': actors,
        'failed_original_guard_attempts_preserved_without_any_native_fit_count': True,
        'native_scientific_model_params_full_samples_and300_iterations_not_changed': True,
        'original30_annual6_final_and262_quality_still_required': True,
        'full_native_scope_not_declared_complete_by_wiring': True,
        'new_quality_scores': 0, 'test_labels_read': False, 'physical_resource_boundary_established': False})
    print(json.dumps({'status': 'passed_actual_guard_v3_dispatch', 'launches': launched}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
