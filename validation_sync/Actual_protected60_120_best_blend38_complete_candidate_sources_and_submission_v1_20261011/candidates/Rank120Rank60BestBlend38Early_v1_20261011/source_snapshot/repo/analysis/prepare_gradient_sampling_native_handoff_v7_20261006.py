"""Supersede only two zero-work waiting wrappers to bind the actual replacement observer."""
from pathlib import Path
import json
import subprocess
import sys
import time

import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]


def main():
    from handoff_distribution_views_progress_monitor_20261006 import read, sha, create
    from run_dependency_queue_v3_20261006 import owned
    from launch_service_owned_workflow_with_pwsh_20261006 import launch
    import publish_classifier_consensus_workflows_20261006 as helpers
    record_path = A / 'gradient_sampling_native_queue_v7_supersession_20261006.json'
    assert not record_path.exists()
    assert not (A / 'gradient_sampling_memmap_native_promotion_20261006').exists()
    assert not (A / 'gradient_sampling_native_queue_handoff_v6_20261006').exists()
    assert not (A / 'service_owned_workflows_20261006/dependency_queue_v6').exists()
    proof_path = A / 'gradient_sampling_native_queue_v6_preflight_20261006/verification.json'
    proof = read(proof_path)
    assert proof['status'] == 'passed_actual23_original_routes_and_unclosed_promotion_dispatch_hold'
    for path, digest in proof['input_sha256'].items():
        assert sha(path) == digest, path
    retired = {}
    # Publication first: avoid interpreting deliberate administrative retirement as a scientific failure.
    for name in ('gradient_sampling_native_queue_handoff_v6_publication', 'gradient_sampling_native_queue_handoff_v6'):
        folder = A / f'service_owned_workflows_20261006/{name}'
        row = read(folder / 'native_launch.json')
        assert owned(row) and not (folder / 'service_execution.json').exists()
        root, worker = psutil.Process(row['pid']), psutil.Process(row['owned_worker_pid'])
        assert root.create_time() == row['owned_parent_creation_time'] and root.cmdline()[1:] == worker.cmdline()[1:]
        assert not worker.children()
        worker.terminate()
        worker.wait(timeout=15)
        root.terminate()
        root.wait(timeout=15)
        assert not owned(row)
        item = {'status': 'deliberately_superseded_zero_work_waiting_wrapper_to_bind_current_observer27',
            'actual_previous_ownership': row, 'actual_models_promoted': 0, 'actual_controllers_retired_by_wrapper': 0,
            'no_passed_original_execution_fabricated': True, 'scientific_workers_touched': 0}
        create(folder / 'administrative_supersession.json', item)
        retired[name] = item
    create(record_path, {'status': 'verified_exact_retirement_of_two_zero_work_waiting_wrappers',
        'retired_wrappers': retired, 'reason': 'The original frozen wrapper referenced observer25; version7 waits for verified observer27.',
        'original_wrapper_sources_and_frozen_definitions_preserved': True,
        'original_controller6_model_promotion_and_all262_quality_routes_unchanged': True,
        'actual_new_model_fits': 0, 'actual_new_quality_scores': 0,
        'scientific_workers_touched': 0, 'test_labels_read': False})
    pins = {**proof['input_sha256'], str(proof_path): sha(proof_path), str(record_path): sha(record_path)}
    additions = [Path(__file__), A / 'handoff_gradient_sampling_native_to_original_queue_v7_20261006.py',
        A / 'publish_gradient_sampling_native_handoff_v7_20261006.py',
        A / 'monitor_actual_optimization_progress_v27_20261006.py',
        A / 'handoff_GOSS_progress_monitor_v27_20261006.py',
        Path(helpers.__file__), Path(helpers.sync.__file__)]
    pins.update({str(p.resolve()): sha(p) for p in additions})
    for path in additions:
        if path.suffix == '.py':
            compile(path.read_text(encoding='utf-8-sig'), str(path), 'exec')
    results = []
    for name, driver in (
        ('gradient_sampling_native_queue_handoff_v7', 'handoff_gradient_sampling_native_to_original_queue_v7_20261006.py'),
        ('gradient_sampling_native_queue_handoff_v7_publication', 'publish_gradient_sampling_native_handoff_v7_20261006.py')):
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
        while not (service / 'native_launch.json').exists():
            assert not (service / 'service_execution.json').exists()
            time.sleep(.5)
        row = read(service / 'native_launch.json')
        assert owned(row) and row['actual_native_console_handle'] == 0
        results.append({'service': name, 'actual_ownership': row})
    print(json.dumps({'status': 'passed_actual_two_hidden_version7_waiting_wrappers_with_original_routes_preserved', 'services': results}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
