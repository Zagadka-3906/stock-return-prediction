"""Dispatch full capacity publication using the actual imported sync source, preserving preparation failure."""
from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]


def main():
    import publish_classifier_consensus_workflows_20261006 as helpers
    from handoff_distribution_views_progress_monitor_20261006 import read, sha, create
    from run_dependency_queue_v3_20261006 import owned
    from launch_service_owned_workflow_with_pwsh_20261006 import launch
    capacity = A / 'service_owned_workflows_20261006/gradient_sampling_memmap_capacity_v3'
    assert owned(read(capacity / 'native_launch.json')) or read(capacity / 'service_execution.json')['status'] == 'passed'
    service = A / 'service_owned_workflows_20261006/gradient_sampling_memmap_capacity_v3_publication'
    assert service.exists() and not list(service.iterdir()), 'Only reuse the unsubmitted empty preparation folder.'
    original = A / 'prepare_gradient_sampling_capacity_v3_publication_20261006.py'
    create(service / 'preserved_first_preparation_failure.json', {
        'status': 'failed_before_definition_or_process_creation', 'actual_new_processes': 0,
        'failed_preparation_source': str(original), 'failed_preparation_source_sha256': sha(original),
        'error': 'FileNotFoundError: assumed github_validation_sync_main_20261005.py does not exist',
        'correction': 'Pin the actual imported helper sync module path.'})
    script = A / 'publish_full2025_gradient_sampling_memmap_capacity_v3_20261006.py'
    sources = [Path(__file__), original, script, Path(helpers.__file__), Path(helpers.sync.__file__),
        capacity / 'native_launch.json', capacity / 'job_definition.json',
        service / 'preserved_first_preparation_failure.json', A / 'hidden_windows_child_creation_20261006.py',
        A / 'run_dependency_queue_v3_20261006.py']
    pins = {str(p.resolve()): sha(p) for p in sources}
    definition = service / 'job_definition.json'
    create(definition, {'name': 'gradient_sampling_memmap_capacity_v3_publication', 'driver': str(script), 'arguments': [],
        'scratch': str(ROOT / 'tmp/service_owned_gradient_sampling_memmap_capacity_v3_publication'),
        'input_sha256': pins, 'bootstrap_sha256': sha(A / 'run_service_owned_windows_workflow_20261006.py'),
        'command_line': subprocess.list2cmdline([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8',
            str(A / 'run_service_owned_windows_workflow_20261006.py'), str(definition)])})
    receipt = launch(definition, Path('C:/Users/esesl/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/powershell/pwsh.exe'))
    create(service / 'verified_hidden_launch.json', receipt)
    print(json.dumps(receipt, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
