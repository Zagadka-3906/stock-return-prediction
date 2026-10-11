"""Make full native scope publication automatic after actual successful closure."""
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
    capacity = A / 'service_owned_workflows_20261006/gradient_sampling_memmap_capacity_v3'
    assert owned(read(capacity / 'native_launch.json')) or read(capacity / 'service_execution.json')['status'] == 'passed'
    service = A / 'service_owned_workflows_20261006/gradient_sampling_memmap_capacity_v3_publication'
    assert not service.exists()
    service.mkdir()
    script = A / 'publish_full2025_gradient_sampling_memmap_capacity_v3_20261006.py'
    sources = [Path(__file__), script, capacity / 'native_launch.json', capacity / 'job_definition.json',
        A / 'publish_classifier_consensus_workflows_20261006.py',
        A / 'github_validation_sync_main_20261005.py', A / 'hidden_windows_child_creation_20261006.py',
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
