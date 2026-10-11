"""Pin the full original30+6 native scope and dispatch its consoleless waiting service."""
from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]


def main():
    from handoff_distribution_views_progress_monitor_20261006 import read, sha, create
    from run_dependency_queue_v3_20261006 import owned
    from launch_service_owned_workflow_with_pwsh_20261006 import launch
    proof = A / 'gradient_sampling_all_annual_cache_controls_20261006/verification.json'
    assert read(proof)['status'] == 'passed_all5_full_original_GOSS_annual_preprocessing_targets_and_maturity'
    capacity = A / 'service_owned_workflows_20261006/gradient_sampling_memmap_capacity'
    assert owned(read(capacity / 'native_launch.json')) or read(capacity / 'service_execution.json')['status'] == 'passed'
    service = A / 'service_owned_workflows_20261006/gradient_sampling_memmap_complete_workflow'
    assert not service.exists() and not (A / 'gradient_sampling_memmap_complete_bank_20261006').exists()
    sources = [Path(__file__), proof, A / 'gradient_sampling_all_annual_cache_controls_20261006/resource_summary.json',
        capacity / 'native_launch.json', capacity / 'job_definition.json',
        A / 'gradient_sampling_memmap_capacity_20261006/protocol.json',
        *[A / name for name in ('train_gradient_sampling_memmap_bank_20261006.py',
            'run_gradient_sampling_memmap_full_workflow_20261006.py',
            'verify_gradient_sampling_memmap_full_future_20261006.py',
            'owned_scheduler_native_fit_hold_20261006.py', 'watch_owned_scheduler_fit_lease_20261006.py',
            'independent_gradient_sampling_native_codec_20261006.py', 'gradient_sampling_exact_memmap_20261006.py',
            'windows_hidden_process_launch_20261006.py', 'locked_read_hash_cache_20261004.py',
            'linear_leaf_actual_resource_sampler_20261005.py', 'run_dependency_queue_v3_20261006.py')]]
    bindings = dict(read(proof)['input_sha256'])
    bindings.update({str(path.resolve()): sha(path) for path in sources})
    for name, digest in bindings.items():
        assert sha(name) == digest
        if Path(name).suffix == '.py':
            compile(Path(name).read_text(encoding='utf-8-sig'), name, 'exec')
    service.mkdir()
    definition = service / 'job_definition.json'
    create(definition, {'name': 'gradient_sampling_memmap_complete_workflow',
        'driver': str(A / 'run_gradient_sampling_memmap_full_workflow_20261006.py'), 'arguments': [],
        'scratch': str(ROOT / 'tmp/service_owned_gradient_sampling_memmap_complete_workflow'),
        'input_sha256': bindings,
        'bootstrap_sha256': sha(A / 'run_service_owned_windows_workflow_20261006.py'),
        'command_line': subprocess.list2cmdline([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8',
            str(A / 'run_service_owned_windows_workflow_20261006.py'), str(definition)])})
    result = launch(definition, Path('C:/Users/esesl/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/powershell/pwsh.exe'))
    create(service / 'verified_hidden_launch.json', result)
    print(json.dumps(result, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
