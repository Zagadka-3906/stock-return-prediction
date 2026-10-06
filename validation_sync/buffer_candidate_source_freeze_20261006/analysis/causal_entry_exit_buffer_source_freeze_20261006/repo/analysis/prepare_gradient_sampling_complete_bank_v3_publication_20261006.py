"""Publish the whole30+6 native scope automatically after its complete actual terminal proof."""
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
    native = A / 'service_owned_workflows_20261006/gradient_sampling_memmap_complete_workflow_v3'
    assert owned(read(native / 'native_launch.json')) or read(native / 'service_execution.json')['status'] == 'passed'
    service = A / 'service_owned_workflows_20261006/gradient_sampling_memmap_complete_bank_v3_publication'
    assert not service.exists()
    script = A / 'publish_gradient_sampling_memmap_complete_bank_v3_20261006.py'
    sources = [Path(__file__), script, Path(helpers.__file__), Path(helpers.sync.__file__),
        native / 'native_launch.json', native / 'job_definition.json',
        A / 'hidden_windows_child_creation_20261006.py', A / 'run_dependency_queue_v3_20261006.py']
    pins = {str(p.resolve()): sha(p) for p in sources}
    compile(script.read_text(encoding='utf-8'), str(script), 'exec')
    service.mkdir()
    definition = service / 'job_definition.json'
    create(definition, {'name': 'gradient_sampling_memmap_complete_bank_v3_publication', 'driver': str(script), 'arguments': [],
        'scratch': str(ROOT / 'tmp/service_owned_gradient_sampling_memmap_complete_bank_v3_publication'),
        'input_sha256': pins, 'bootstrap_sha256': sha(A / 'run_service_owned_windows_workflow_20261006.py'),
        'command_line': subprocess.list2cmdline([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8',
            str(A / 'run_service_owned_windows_workflow_20261006.py'), str(definition)])})
    result = launch(definition, Path('C:/Users/esesl/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/powershell/pwsh.exe'))
    create(service / 'verified_hidden_launch.json', result)
    print(json.dumps(result, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
