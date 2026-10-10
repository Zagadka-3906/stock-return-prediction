"""Replace only the observer after a real complete update with verified GOSS counts."""
from pathlib import Path
import json
import subprocess
import sys
import time

import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from handoff_distribution_views_progress_monitor_20261006 import read, sha, create, visible_terminals
from run_dependency_queue_v3_20261006 import owned
from launch_service_owned_workflow_with_pwsh_20261006 import launch


def main():
    import monitor_actual_optimization_progress_v28_20261006 as monitor
    out = A / 'GOSS_progress_monitor_handoff_v28_20261006'
    service = A / 'service_owned_workflows_20261006/progress_monitor_v28'
    assert not out.exists() and not service.exists()
    assert read(A / 'observer_snapshot_transaction_preflight_v2_20261006/verification.json')['status'] == 'passed_actual_disk_isolation_commit_and_failed_update_rollback'
    previous = A / 'service_owned_workflows_20261006/progress_monitor_v25'
    old = read(previous / 'native_launch.json')
    assert owned(old)
    root, worker = psutil.Process(old['pid']), psutil.Process(old['owned_worker_pid'])
    assert root.create_time() == old['owned_parent_creation_time'] and root.cmdline()[1:] == worker.cmdline()[1:]
    assert not worker.children()
    scientific = {}
    for name in ('neural16384_annual', 'dependency_queue_v5', 'main_publisher_v5',
                 'gradient_sampling_memmap_complete_workflow_v3', 'gradient_sampling_memmap_complete_bank_v3_publication',
                 'quantile_tree_quality_queue_v2', 'quantile_distribution_views_quality_queue'):
        row = read(A / f'service_owned_workflows_20261006/{name}/native_launch.json')
        assert owned(row), name
        scientific[name] = row
    queue = read(A / 'service_owned_dependency_queue_v4_20261006/state.json')
    for name, row in queue['activated_jobs'].items():
        if name.startswith('round') and owned(row):
            scientific[name] = row
    definition = read(previous / 'job_definition.json')
    definition.update(name='progress_monitor_v28', driver=str(A / 'monitor_actual_optimization_progress_v28_20261006.py'),
        scratch=str(ROOT / 'tmp/service_owned_progress_monitor_v28'))
    additions = [Path(__file__), Path(monitor.__file__), A / 'verify_GOSS_progress_monitor_v28_20261006.py',
        A / 'gradient_sampling_complete_search_plan_20261005.json',
        A / 'gradient_sampling_storage_20261005.json',
        A / 'complete_observer_snapshot_transaction_v2_20261006.py']
    definition['input_sha256'].update({str(p.resolve()): sha(p) for p in additions})
    for path, digest in definition['input_sha256'].items():
        assert sha(path) == digest, path
        if Path(path).suffix == '.py':
            compile(Path(path).read_text(encoding='utf-8-sig'), path, 'exec')
    out.mkdir()
    suspended, retired, new_row, bootstrap_identity = [], False, None, None
    try:
        for process in (worker, root):
            process.suspend()
            suspended.append(process)
        before = read(A / 'ongoing_optimization_state.json')
        assert before['actual_observer_version'] == 25
        create(out / 'frozen_before_handoff.json', {'old_owned_observer': old,
            'preserved_scientific_ownership': scientific, 'input_sha256': definition['input_sha256'],
            'previous_complete_public_state': before, 'scientific_processes_suspended_or_terminated': 0})
        actual = monitor.goss_snapshot()
        monitor.update()
        after = read(A / 'ongoing_optimization_state.json')
        resume = read(A / 'resume_optimization_20261004.json')
        state = read(A / 'actual_optimization_monitor_state_20261005.json')
        assert after['actual_observer_version'] == resume['actual_observer_version'] == state['actual_observer_version'] == 28
        assert len({v['complete_observer_generation'] for v in (after, resume, state)}) == 1
        assert after['gradient_sampling_actual_annual_fits'] >= actual['gradient_sampling_actual_annual_fits']
        assert after['gradient_sampling_actual_final_fits'] == 6
        assert after['gradient_sampling_duplicate_model_records_excluded'] >= 6
        assert after['gradient_sampling_expected_full_quality_records'] == 262
        queue_path, current_queue = monitor.current_dependency()
        assert after['dependency_queue_registry'] == queue_path.relative_to(ROOT).as_posix()
        assert owned(current_queue)
        assert set((75, 76, 91, 92, 93, 94)) <= set(after['pending_required_rounds'])
        assert after['quantile_tree_actual_completed_annual_fits'] == 20
        assert after['quantile_distribution_views_new_native_fits'] == 0
        create(out / 'actual_full_update_preflight.json', {'status': 'passed_actual_complete_update_current_queue_and_SHA_verified_GOSS_counts',
            'complete_public_generation': after['complete_observer_generation'],
            'actual_annual_models': after['gradient_sampling_actual_annual_fits'], 'actual_final_models': 6,
            'excluded_duplicate_records': after['gradient_sampling_duplicate_model_records_excluded'],
            'actual_current_queue': current_queue, 'expected_complete_quality_records': 262,
            'all_public_files_complete_same_generation': True, 'new_native_fits': 0, 'new_quality_scores': 0})
        create(out / 'actual_complete_public_state_after_preflight.json', after)
        definition['input_sha256'][str(out / 'actual_full_update_preflight.json')] = sha(out / 'actual_full_update_preflight.json')
        service.mkdir()
        path = service / 'job_definition.json'
        definition['command_line'] = subprocess.list2cmdline([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8',
            str(A / 'run_service_owned_windows_workflow_20261006.py'), str(path)])
        create(path, definition)
        result = launch(path, Path('C:/Users/esesl/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/powershell/pwsh.exe'))
        create(service / 'verified_hidden_launch.json', result)
        bootstrap = psutil.Process(result['actual_launch_result']['ProcessId'])
        bootstrap_identity = {'pid': bootstrap.pid, 'creation_time': bootstrap.create_time(), 'command_line': bootstrap.cmdline()}
        last_notice = time.monotonic()
        while True:
            assert not (service / 'service_execution.json').exists(), 'New observer terminated before a complete update.'
            if (service / 'native_launch.json').exists():
                new_row = read(service / 'native_launch.json')
                assert owned(new_row)
                value = read(A / 'actual_optimization_monitor_state_20261005.json')
                if value.get('actual_observer_version') == 28 and value.get('pid') == new_row['owned_worker_pid']:
                    break
            if time.monotonic() - last_notice > 10:
                print(json.dumps({'stage': 'waiting_same_actual_owned_observer28_first_complete_update', 'owned_live': owned(new_row) if new_row else None}), flush=True)
                last_notice = time.monotonic()
            time.sleep(.5)
        assert new_row['actual_native_console_handle'] == 0
        assert all(owned(row) for row in scientific.values())
        worker.terminate()
        worker.wait(timeout=15)
        root.terminate()
        root.wait(timeout=15)
        retired = True
        suspended.clear()
        create(out / 'verification.json', {'status': 'passed_actual_observer28_handoff_with_complete_update_and_science_preserved',
            'actual_new_observer': new_row, 'old_observer': old, 'preserved_scientific_ownership': scientific,
            'old_observer_only_processes_retired': [worker.pid, root.pid],
            'scientific_processes_suspended_or_terminated': 0, 'input_sha256': definition['input_sha256'],
            'actual_original_route_and_full_scope_preserved': True, 'new_native_fits': 0, 'new_quality_scores': 0,
            'test_labels_read': False, 'visible_terminal_windows': visible_terminals()})
        print('passed_actual_observer28_handoff_with_complete_update_and_science_preserved', flush=True)
    except BaseException as error:
        if not retired and bootstrap_identity is not None:
            try:
                bootstrap = psutil.Process(bootstrap_identity['pid'])
                if bootstrap.create_time() == bootstrap_identity['creation_time'] and bootstrap.cmdline() == bootstrap_identity['command_line']:
                    matches = [p for p in bootstrap.children() if p.name().lower() == 'python.exe' and p.cmdline()[1:] == bootstrap.cmdline()[1:]]
                    assert all(not p.children() for p in matches)
                    for process in matches:
                        process.terminate()
                        process.wait(timeout=15)
                    bootstrap.terminate()
                    bootstrap.wait(timeout=15)
            except psutil.NoSuchProcess:
                pass
        create(out / 'failure.json', {'status': 'failed_preserved_observer28_handoff', 'error': f'{type(error).__name__}: {error}',
            'old_observer_retired': retired, 'new_observer': new_row})
        raise
    finally:
        if not retired:
            for process in reversed(suspended):
                if process.is_running():
                    process.resume()


if __name__ == '__main__':
    main()
