"""Pin actual controls and launch six original largest-window GOSS tests consolelessly."""
from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from handoff_distribution_views_progress_monitor_20261006 import read, sha, create
from run_dependency_queue_v3_20261006 import owned
from launch_service_owned_workflow_with_pwsh_20261006 import launch


def main():
    control = A / 'gradient_sampling_exact_memmap_preflight_20261006/verification.json'
    proof = read(control)
    assert proof['status'] == 'passed_all6_native_GOSS_parameters_and_full_original_preprocessing_and_full2020_equivalence'
    assert proof['actual_pilot_native_fits'] == 12 and proof['actual_full2020_native_control_fits'] == 2
    service = A / 'service_owned_workflows_20261006/gradient_sampling_memmap_capacity'
    assert not service.exists() and not (A / 'gradient_sampling_memmap_capacity_20261006').exists()
    assert owned(read(A / 'service_owned_workflows_20261006/dependency_queue_v5/native_launch.json'))
    pins = dict(proof['input_sha256'])
    files = [Path(__file__).resolve(), control, *[A / name for name in (
        'verify_full2025_gradient_sampling_memmap_capacity_20261006.py',
        'independent_gradient_sampling_native_codec_20261006.py',
        'owned_scheduler_native_fit_hold_20261006.py', 'watch_owned_scheduler_fit_lease_20261006.py',
        'windows_hidden_process_launch_20261006.py', 'run_dependency_queue_v3_20261006.py',
        'verify_linear_leaf_bank_20261005.py', 'gradient_sampling_storage_20261005.json',
        'service_owned_workflows_20261006/dependency_queue_v5/native_launch.json',
        'gradient_sampling_exact_memmap_preflight_20261006/resource_summary.json')],
        ROOT / 'deliveries/connected_topk0175_20261003/generation_inputs.parquet',
        ROOT / 'deliveries/connected_topk0175_20261003/train_test.json']
    pins.update({str(path.resolve()): sha(path) for path in files})
    for path, digest in pins.items():
        assert sha(path) == digest, path
        if Path(path).suffix == '.py':
            compile(Path(path).read_text(encoding='utf-8-sig'), path, 'exec')
    service.mkdir()
    run_path = service / 'capacity_run.json'
    create(run_path, {'status': 'frozen_before_original6_largest_GOSS_capacity_controls', 'input_sha256': pins,
        'expected_full_final_fits': 6, 'actual_bank_annual_fits': 0, 'new_quality_scores': 0,
        'original30_annual_and262_quality_records_preserved': True, 'test_labels_read': False})
    definition = service / 'job_definition.json'
    create(definition, {'name': 'gradient_sampling_memmap_capacity',
        'driver': str(A / 'verify_full2025_gradient_sampling_memmap_capacity_20261006.py'), 'arguments': [str(run_path)],
        'scratch': str(ROOT / 'tmp/service_owned_gradient_sampling_memmap_capacity'),
        'input_sha256': {**pins, str(run_path): sha(run_path)},
        'bootstrap_sha256': sha(A / 'run_service_owned_windows_workflow_20261006.py'),
        'command_line': subprocess.list2cmdline([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8',
            str(A / 'run_service_owned_windows_workflow_20261006.py'), str(definition)])})
    result = launch(definition, Path('C:/Users/esesl/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/powershell/pwsh.exe'))
    create(service / 'verified_hidden_launch.json', result)
    print(json.dumps(result, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
