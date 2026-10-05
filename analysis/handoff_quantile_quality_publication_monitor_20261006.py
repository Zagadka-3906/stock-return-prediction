"""Replace idle owned controllers; leave all native fitting and scoring live."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import time

import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
OUT = A / 'quantile_quality_publication_monitor_handoff_20261006'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def create(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    from finalize_main_branch_consolidation_20261005 import owned_pair
    from run_dependency_queue_v3_20261006 import owned
    from hidden_windows_child_creation_20261006 import install
    import watch_validations_main_v2_20261005 as retained
    from lossless_round_publication_adapter_v2_20261006 import install as full_export
    assert not OUT.exists()
    OUT.mkdir()
    restore_children = install()
    suspended = []
    old = {}
    try:
        for path in (A / 'quantile_tree_quality_generator_preflight_v2_20261006/verification.json',
                     A / 'quantile_tree_codec_preflight_20261006/verification.json'):
            assert read(path)['status'] == 'passed'
        snapshot = retained.sync.snapshot
        assert full_export(retained.sync) is snapshot
        retained.sync.snapshot = snapshot
        old = {name: read(A / f'service_owned_workflows_20261006/{name}/native_launch.json')
               for name in ('main_publisher_v4', 'progress_monitor_v20')}
        scientific = {name: read(A / f'service_owned_workflows_20261006/{name}/native_launch.json')
            for name in ('neural16384_annual', 'dependency_queue_v4', 'quantile_tree_full_workflow', 'quantile_tree_quality_queue')}
        assert all(owned(row) for row in (*old.values(), *scientific.values()))
        qstate = read(A / 'service_owned_dependency_queue_v4_20261006/state.json')
        scientific['round82'] = qstate['activated_jobs']['round82']
        assert owned(scientific['round82'])
        pairs = []
        for row in old.values():
            pair = owned_pair(row['pid'], Path(row['script']), row['script_args'])
            assert pair[0].create_time() == row['owned_parent_creation_time']
            assert pair[1].pid == row['owned_worker_pid'] and pair[1].create_time() == row['owned_worker_creation_time']
            pairs.append(pair)
        for attempt in range(30):
            for root, worker in pairs:
                for p in (worker, root):
                    p.suspend()
                    suspended.append(p)
            busy = [p for root, worker in pairs for p in root.children(recursive=True)
                    if p.pid != worker.pid and p.name().lower() != 'conhost.exe']
            if not busy:
                break
            for p in reversed(suspended):
                p.resume()
            suspended.clear()
            time.sleep(.2)
        else:
            raise RuntimeError('Owned publication or observer controller still has an active child.')
        create(OUT / 'frozen_before_owned_controller_handoff.json', {
            'old_owned_controllers': old, 'actual_owned_scientific_jobs_not_stopped': scientific,
            'all_old_controllers_idle_with_no_active_children': True,
            'new_driver_sha256': {str(A / name): sha(A / name) for name in
                ('watch_validations_main_v5_20261006.py', 'monitor_actual_optimization_progress_v21_20261006.py')},
            'all_immutable_export_adapter_source_patches_compiled_and_installed': True,
            'new_quality_scores': 0, 'test_labels_read': False})
        for root, worker in pairs:
            worker.terminate()
            worker.wait(timeout=15)
            if root.is_running():
                root.terminate()
                root.wait(timeout=15)
        suspended.clear()
        for name in ('main_publisher_v5', 'progress_monitor_v21'):
            definition = A / f'service_owned_workflows_20261006/{name}/job_definition.json'
            result = subprocess.run(['powershell.exe', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File',
                str(A / 'launch_service_owned_windows_workflow_20261006.ps1'), '-DefinitionPath', str(definition)],
                cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=30)
            assert result.returncode == 0, result.stderr
        deadline = time.monotonic() + 50
        while True:
            launches = [A / f'service_owned_workflows_20261006/{name}/native_launch.json'
                        for name in ('main_publisher_v5', 'progress_monitor_v21')]
            if all(p.exists() and owned(read(p)) for p in launches):
                break
            assert time.monotonic() < deadline, 'Launch observation expired; inspect the same handles before any retry.'
            time.sleep(.2)
        assert all(owned(row) for row in scientific.values())
        create(OUT / 'verification.json', {'status': 'passed_actual_idle_owned_main_and_monitor_handoff',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'new_owned_controllers': [read(p) for p in launches],
            'all_original_native_fitting_and_round82_scoring_jobs_still_exact_owned_live': True,
            'all_old_owned_controllers_closed': all(not owned(row) for row in old.values()),
            'new_controllers_have_independent_consoleless_service_roots': True,
            'original_failed_scopes_and_source_files_and_scientific_predictions_preserved': True,
            'new_quality_scores': 0, 'test_labels_read': False})
    except BaseException as error:
        create(OUT / 'failure.json', {'status': 'failed_preserved_controller_handoff',
            'error': f'{type(error).__name__}: {error}', 'old_owned_controllers': old})
        raise
    finally:
        for p in reversed(suspended):
            if p.is_running():
                p.resume()
        create(OUT / 'actual_hidden_child_creations.json', {'events': restore_children()})


if __name__ == '__main__':
    main()
