"""Replace the exact v23 observer after a complete snapshot; preserve all science."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import subprocess
import sys
import time
import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import owned
from launch_service_owned_workflow_with_pwsh_20261006 import launch
from handoff_distribution_views_progress_monitor_20261006 import read, sha, create, visible_terminals


def main():
    service = A / 'service_owned_workflows_20261006/progress_monitor_v25'
    out = A / 'complete_snapshot_monitor_handoff_v25_20261006'
    assert not service.exists() and not out.exists()
    preflight = read(A / 'observer_snapshot_transaction_preflight_v2_20261006/verification.json')
    assert preflight['status'] == 'passed_actual_disk_isolation_commit_and_failed_update_rollback'
    previous_service = A / 'service_owned_workflows_20261006/progress_monitor_v24'
    old = read(previous_service / 'native_launch.json')
    assert owned(old)
    root, worker = psutil.Process(old['pid']), psutil.Process(old['owned_worker_pid'])
    assert root.create_time() == old['owned_parent_creation_time']
    assert root.cmdline()[-2:] == [old['script'], *old['script_args']]
    assert not worker.children()
    assert [p.pid for p in root.children() if p.name().lower() != 'conhost.exe'] == [worker.pid]
    identities = read(A / 'distribution_views_progress_handoff_20261006/frozen_before_handoff.json')['unchanged_scientific_ownership']
    for row in identities.values():
        assert owned(row)
    definition = read(previous_service / 'job_definition.json')
    definition.update(name='progress_monitor_v25',
        driver=str(A / 'monitor_actual_optimization_progress_v25_20261006.py'),
        scratch=str(ROOT / 'tmp/service_owned_progress_monitor_v25'))
    sources = [Path(__file__).resolve(), A / 'monitor_actual_optimization_progress_v25_20261006.py',
        A / 'complete_observer_snapshot_transaction_v2_20261006.py',
        A / 'verify_observer_snapshot_transaction_v2_20261006.py',
        A / 'observer_snapshot_transaction_preflight_v2_20261006/verification.json']
    definition['input_sha256'].update({str(path): sha(path) for path in sources})
    for filename, digest in definition['input_sha256'].items():
        assert sha(filename) == digest
        if Path(filename).suffix == '.py':
            compile(Path(filename).read_text(encoding='utf-8-sig'), filename, 'exec')
    # Wait for the exact old writer to finish its full update; do not publish a partial predecessor.
    for _ in range(180):
        assert owned(old)
        value = read(A / 'ongoing_optimization_state.json')
        if value.get('actual_progress_monitor', '').endswith('monitor_actual_optimization_progress_v24_20261006.py'):
            root.suspend()
            worker.suspend()
            value = read(A / 'ongoing_optimization_state.json')
            if value.get('actual_progress_monitor', '').endswith('monitor_actual_optimization_progress_v24_20261006.py'):
                break
            worker.resume()
            root.resume()
        time.sleep(1)
    else:
        raise RuntimeError('Old observer still live; complete snapshot not yet observed. No duplicate launch.')
    try:
        for row in identities.values():
            assert owned(row)
        out.mkdir()
        create(out / 'frozen_before_handoff.json', {
            'at_local': datetime.now().isoformat(timespec='seconds'),
            'old_owned_observer': old, 'unchanged_scientific_ownership': identities,
            'observed_complete_public_state': value,
            'visible_terminal_windows': visible_terminals(),
            'input_sha256': definition['input_sha256'], 'new_quality_scores': 0})
        service.mkdir()
        path = service / 'job_definition.json'
        definition['command_line'] = subprocess.list2cmdline([str(ROOT / '.venv/Scripts/python.exe'),
            '-B', '-X', 'utf8', str(A / 'run_service_owned_windows_workflow_20261006.py'), str(path)])
        create(path, definition)
        worker.terminate()
        worker.wait(timeout=15)
        if root.is_running():
            assert root.create_time() == old['owned_parent_creation_time']
            root.terminate()
            root.wait(timeout=15)
    finally:
        for process in (worker, root):
            if process.is_running():
                process.resume()
    assert not owned(old)
    result = launch(path, Path('C:/Users/esesl/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/powershell/pwsh.exe'))
    create(out / 'actual_launch.json', result)
    print(json.dumps({'status': 'actual_v25_consoleless_launch_complete_update_pending',
        'prior_complete_snapshot_retained': True, 'launch': result}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
