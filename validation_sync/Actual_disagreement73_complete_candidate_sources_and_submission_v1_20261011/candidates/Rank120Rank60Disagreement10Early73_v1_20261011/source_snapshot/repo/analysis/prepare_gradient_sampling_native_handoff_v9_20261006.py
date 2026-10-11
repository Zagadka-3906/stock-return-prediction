"""Start pinned consoleless waiting services; no scientific work or promotion before actual closure."""
from pathlib import Path
import json
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]


def main():
    from handoff_distribution_views_progress_monitor_20261006 import read, sha, create
    from run_dependency_queue_v3_20261006 import owned
    from launch_service_owned_workflow_with_pwsh_20261006 import launch
    import publish_classifier_consensus_workflows_20261006 as helpers
    proof_path = A / 'gradient_sampling_native_queue_v6_preflight_20261006/verification.json'
    proof = read(proof_path)
    assert proof['status'] == 'passed_actual23_original_routes_and_unclosed_promotion_dispatch_hold'
    for path, digest in proof['input_sha256'].items():
        assert sha(path) == digest, path
    pins = {**proof['input_sha256'], str(proof_path): sha(proof_path)}
    sources = [A / 'gradient_sampling_native_queue_v9_supersession_20261006.json', A / 'handoff_gradient_sampling_native_to_original_queue_v9_20261006.py', Path(__file__), A / 'publish_gradient_sampling_native_handoff_v9_20261006.py',
        Path(helpers.__file__), Path(helpers.sync.__file__),
        A / 'launch_service_owned_workflow_with_pwsh_20261006.py',
        A / 'launch_service_owned_windows_workflow_20261006.ps1',
        A / 'run_service_owned_windows_workflow_20261006.py']
    pins.update({str(p.resolve()): sha(p) for p in sources})
    for path in sources:
        if path.suffix == '.py':
            compile(path.read_text(encoding='utf-8-sig'), str(path), 'exec')
    results = []
    for name, driver in (
        ('gradient_sampling_native_queue_handoff_v9', 'handoff_gradient_sampling_native_to_original_queue_v9_20261006.py'),
        ('gradient_sampling_native_queue_handoff_v9_publication', 'publish_gradient_sampling_native_handoff_v9_20261006.py')):
        service = A / 'service_owned_workflows_20261006' / name
        assert not service.exists()
        service.mkdir()
        definition = service / 'job_definition.json'
        create(definition, {'name': name, 'driver': str(A / driver), 'arguments': [],
            'scratch': str(ROOT / 'tmp' / ('service_owned_' + name)), 'input_sha256': pins,
            'bootstrap_sha256': sha(A / 'run_service_owned_windows_workflow_20261006.py'),
            'command_line': subprocess.list2cmdline([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8',
                str(A / 'run_service_owned_windows_workflow_20261006.py'), str(definition)])})
        result = launch(definition, Path('C:/Users/esesl/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/powershell/pwsh.exe'))
        create(service / 'verified_hidden_launch.json', result)
        deadline = time.monotonic() + 45
        while not (service / 'native_launch.json').exists():
            assert not (service / 'service_execution.json').exists()
            if time.monotonic() > deadline:
                raise TimeoutError(f'Observe the same launched bootstrap before any retry: {result}')
            time.sleep(.5)
        row = read(service / 'native_launch.json')
        assert owned(row) and row['actual_native_console_handle'] == 0 and not row['independent_launch_root_in_any_job']
        results.append({'service': name, 'actual_ownership': row})
    print(json.dumps({'status': 'passed_actual_two_hidden_waiting_services_for_verified_GOSS_closure', 'services': results}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
