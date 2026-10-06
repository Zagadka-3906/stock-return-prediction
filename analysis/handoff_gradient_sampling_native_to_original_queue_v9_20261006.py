"""After real36-fit publication, retire only queue5 and satisfy its two old GOSS jobs by provenance."""
from pathlib import Path
from copy import deepcopy
import json
import subprocess
import sys
import time

import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
import promote_gradient_sampling_memmap_native_bank_20261006 as promotion
from handoff_distribution_views_progress_monitor_20261006 import read, sha, create, visible_terminals
from run_dependency_queue_v3_20261006 import owned
from launch_service_owned_workflow_with_pwsh_20261006 import launch

OUT = A / 'gradient_sampling_native_queue_handoff_v6_20261006'
SERVICE = A / 'service_owned_workflows_20261006/dependency_queue_v6'
QUEUE = A / 'service_owned_dependency_queue_v4_20261006'


def main():
    observer_proof = A / 'GOSS_progress_monitor_handoff_v28_20261006/verification.json'
    while not observer_proof.exists():
        failure = observer_proof.parent / 'failure.json'
        assert not failure.exists(), 'Observer handoff has an actual failed record; preserve the old queue.'
        time.sleep(5)
    assert read(observer_proof)['status'] == 'passed_actual_observer28_handoff_with_complete_update_and_science_preserved'
    receipt = promotion.wait_for_closure()
    assert not OUT.exists() and not SERVICE.exists() and not (QUEUE / 'queue_plan_v6.json').exists()
    destination, target_future = promotion.stage()
    original_plan_path = QUEUE / 'queue_plan_v5.json'
    original_plan = read(original_plan_path)
    old = read(A / 'service_owned_workflows_20261006/dependency_queue_v5/native_launch.json')
    assert owned(old)
    root, worker = psutil.Process(old['pid']), psutil.Process(old['owned_worker_pid'])
    assert root.create_time() == old['owned_parent_creation_time'] and root.cmdline()[1:] == worker.cmdline()[1:]
    assert old['script'] in worker.cmdline()
    # All annual FitHold leases refer to queue5. Retirement is permitted only after full closure.
    holds = list(promotion.SOURCE.glob('scheduler_fit_hold_*/released.json'))
    assert len(holds) == 30 and all(read(p)['scientific_workers_touched'] == 0 for p in holds)
    assert all(read(p.parent / 'independent_guard_service/service_execution.json')['status'] == 'passed' for p in holds)
    scientific = {}
    for name in ('neural16384_annual', 'main_publisher_v5', 'progress_monitor_v28',
                 'quantile_tree_quality_queue_v2', 'quantile_distribution_views_quality_queue',
                 'distribution_views_full_ranking_publisher'):
        folder = A / f'service_owned_workflows_20261006/{name}'
        row = read(folder / 'native_launch.json')
        assert owned(row) or read(folder / 'service_execution.json')['status'] == 'passed', name
        scientific[name] = row
    pins = dict(original_plan['input_sha256'])
    additions = [Path(__file__), Path(promotion.__file__), original_plan_path, promotion.RECEIPT,
        promotion.OUT / 'staging_verification.json', promotion.SERVICE / 'native_launch.json',
        promotion.SERVICE / 'service_execution.json',
        A / 'gradient_sampling_native_queue_v6_source_generation_20261006.json',
        A / 'run_dependency_queue_v6_20261006.py', observer_proof,
        A / 'run_dependency_queue_v5_20261006.py',
        A / 'service_owned_workflows_20261006/dependency_queue_v5/job_definition.json',
        A / 'service_owned_workflows_20261006/dependency_queue_v5/native_launch.json',
        A / 'launch_service_owned_workflow_with_pwsh_20261006.py',
        A / 'launch_service_owned_windows_workflow_20261006.ps1',
        A / 'run_service_owned_windows_workflow_20261006.py']
    pins.update({str(p.resolve()): sha(p) for p in additions})
    for path, digest in pins.items():
        assert sha(path) == digest, path
        if Path(path).suffix == '.py':
            compile(Path(path).read_text(encoding='utf-8-sig'), path, 'exec')
    OUT.mkdir()
    suspended, retired, new_row, bootstrap_identity = [], False, None, None
    try:
        for process in (worker, root):
            process.suspend()
            suspended.append(process)
        assert owned(old)
        snapshot = read(QUEUE / 'state.json')
        assert snapshot['pid'] == worker.pid
        assert not {'gradient_sampling_native', 'gradient_sampling_future'} & set(snapshot['activated_jobs'])
        # An original fit must never be replaced if it already started.
        assert not (QUEUE / 'activated_jobs/gradient_sampling_native').exists()
        assert not (QUEUE / 'activated_jobs/gradient_sampling_future').exists()
        assert not destination.exists() or not list(destination.iterdir())
        assert not target_future.exists()
        create(OUT / 'original_controller_last_snapshot.json', snapshot)
        pins[str(OUT / 'original_controller_last_snapshot.json')] = sha(OUT / 'original_controller_last_snapshot.json')
        for name, row in snapshot['activated_jobs'].items():
            if owned(row):
                scientific[name] = row
        create(OUT / 'frozen_before_handoff.json', {'input_sha256': pins, 'old_controller': old,
            'preserved_scientific_and_publication_identities': scientific,
            'native_main_receipt': receipt, 'original_deferred_jobs': original_plan['deferred_jobs'],
            'queue5_suspended_only_after_all30_fit_holds_released': True,
            'canonical_artifacts_still_staged': True, 'test_labels_read': False})
        completed_row = read(promotion.SERVICE / 'native_launch.json')
        assert not owned(completed_row)
        fulfilled = {}
        for name in ('gradient_sampling_native', 'gradient_sampling_future'):
            fulfilled[name] = {**completed_row, 'name': name,
                'completion_kind': 'original_scientific_scope_completed_through_verified_exact_memmap_backend',
                'actual_replacement_service_execution': str(promotion.SERVICE / 'service_execution.json'),
                'actual_annual_native_fits': 30, 'actual_final_native_fits': 6,
                'actual_native_main_receipt': str(promotion.RECEIPT),
                'copies_and_completed_job_aliases_not_additional_fits': True,
                'old_original_job_not_run_and_no_passed_original_execution_fabricated': True}
        create(OUT / 'original_GOSS_jobs_fulfilled_by_actual_native_scope.json', {
            'status': 'passed_actual36_fit_and_complete_future_scope_main_published',
            'fulfilled_jobs': fulfilled, 'original262_quality_records_still_required': True,
            'original_deferred_job_definitions_preserved': True, 'new_native_fits': 0, 'new_quality_scores': 0})
        pins[str(OUT / 'original_GOSS_jobs_fulfilled_by_actual_native_scope.json')] = sha(OUT / 'original_GOSS_jobs_fulfilled_by_actual_native_scope.json')
        plan = deepcopy(original_plan)
        plan.update(status='frozen_before_actual_GOSS_native_scope_queue6_handoff', input_sha256=pins,
            previously_activated_jobs={**snapshot['activated_jobs'], **fulfilled},
            prior_queue_plan=str(original_plan_path),
            activation_handoff_commit_marker=str(OUT / 'handoff_commit.json'),
            artifact_exposure_proof=str(promotion.OUT / 'verification.json'),
            original_GOSS_jobs_fulfilled_by_actual_native_provenance=fulfilled,
            all_original_scientific_grids_parents_arguments_and_ranking_cache_preserved=True)
        assert plan['deferred_jobs'] == original_plan['deferred_jobs']
        assert plan['preserved_active_jobs'] == original_plan['preserved_active_jobs']
        assert plan['registry'] == original_plan['registry']
        plan_path = QUEUE / 'queue_plan_v6.json'
        create(plan_path, plan)
        SERVICE.mkdir()
        definition = SERVICE / 'job_definition.json'
        create(definition, {'name': 'dependency_queue_v6', 'driver': str(A / 'run_dependency_queue_v6_20261006.py'),
            'arguments': [str(plan_path)], 'scratch': str(ROOT / 'tmp/service_owned_dependency_queue_v6_20261006'),
            'input_sha256': {**pins, str(plan_path): sha(plan_path)},
            'bootstrap_sha256': sha(A / 'run_service_owned_windows_workflow_20261006.py'),
            'command_line': subprocess.list2cmdline([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8',
                str(A / 'run_service_owned_windows_workflow_20261006.py'), str(definition)])})
        result = launch(definition, Path('C:/Users/esesl/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/powershell/pwsh.exe'))
        create(SERVICE / 'verified_hidden_launch.json', result)
        bootstrap = psutil.Process(result['actual_launch_result']['ProcessId'])
        bootstrap_identity = {'pid': bootstrap.pid, 'creation_time': bootstrap.create_time(), 'command_line': bootstrap.cmdline()}
        create(SERVICE / 'actual_bootstrap_identity_before_source_hash_completion.json', bootstrap_identity)
        started = time.monotonic()
        while True:
            if (SERVICE / 'service_execution.json').exists():
                raise RuntimeError(f'Queue6 exited before handoff: {read(SERVICE / "service_execution.json")}')
            if (SERVICE / 'native_launch.json').exists():
                new_row = read(SERVICE / 'native_launch.json')
                assert owned(new_row)
                current = read(QUEUE / 'state.json')
                if current['pid'] == new_row['owned_worker_pid']:
                    assert current['activated_jobs'] == plan['previously_activated_jobs']
                    break
            if time.monotonic() - started > 600:
                raise TimeoutError('Queue6 did not reach the held dispatch loop within the observation bound.')
            print(json.dumps({'stage': 'waiting_actual_queue6_source_verification', 'seconds': time.monotonic() - started}), flush=True)
            time.sleep(5)
        assert new_row['actual_native_console_handle'] == 0 and not new_row['independent_launch_root_in_any_job']
        assert not (promotion.OUT / 'verification.json').exists()
        assert worker.create_time() == old['owned_worker_creation_time'] and root.create_time() == old['owned_parent_creation_time']
        # Exact scheduler processes only. No recursive termination or scientific suspension.
        worker.terminate()
        worker.wait(timeout=15)
        root.terminate()
        root.wait(timeout=15)
        retired = True
        suspended.clear()
        assert not owned(old) and owned(new_row)
        create(OUT / 'handoff_commit.json', {'status': 'retired_original_controller_and_preserved_scientific_workers',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'old_controller': old,
            'actual_new_controller': new_row, 'preserved_scientific_identities': scientific,
            'only_exact_scheduler_processes_terminated': [worker.pid, root.pid],
            'scientific_processes_terminated_or_suspended_by_handoff': 0,
            'new_native_fits': 0, 'new_quality_scores': 0})
        promotion.expose(destination, target_future, OUT / 'handoff_commit.json')
        assert read(promotion.OUT / 'verification.json')['status'] == 'passed' and owned(new_row)
        for source, digest in pins.items():
            assert sha(source) == digest, source
        create(OUT / 'verification.json', {'status': 'passed_actual_queue6_handoff_and_all36_original_GOSS_routes_exposed',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins,
            'actual_new_controller': new_row, 'fulfilled_original_GOSS_jobs': fulfilled,
            'all_original_deferred_definitions_and_grids_and_parent_gates_preserved': True,
            'original67_to94_scope_including262_GOSS_quality_records_still_required': True,
            'same_original_registry': plan['registry'], 'shared_queue_state_path': str(QUEUE / 'state.json'),
            'scientific_processes_terminated_or_suspended': 0, 'copies_counted_as_fits': 0,
            'visible_terminal_windows': visible_terminals(), 'new_native_fits': 0, 'new_quality_scores': 0,
            'test_labels_read': False, 'global_resource_boundary_established': False})
        print('passed_actual_queue6_handoff_and_all36_original_GOSS_routes_exposed', flush=True)
    except BaseException as error:
        if not retired and bootstrap_identity is not None:
            assert not (OUT / 'handoff_commit.json').exists()
            try:
                bootstrap = psutil.Process(bootstrap_identity['pid'])
                if bootstrap.create_time() == bootstrap_identity['creation_time'] and bootstrap.cmdline() == bootstrap_identity['command_line']:
                    matches = [p for p in bootstrap.children() if p.name().lower() == 'python.exe' and p.cmdline()[1:] == bootstrap.cmdline()[1:]]
                    assert all(not [c for c in p.children() if c.name().lower() != 'conhost.exe'] for p in matches)
                    for process in matches:
                        process.terminate()
                        process.wait(timeout=15)
                    bootstrap.terminate()
                    bootstrap.wait(timeout=15)
            except psutil.NoSuchProcess:
                pass
        create(OUT / 'failure.json', {'status': 'failed_preserved_GOSS_native_handoff',
            'error': f'{type(error).__name__}: {error}', 'old_controller_retired': retired,
            'new_controller_if_observed': new_row, 'no_original_job_success_fabricated': True})
        raise
    finally:
        if not retired:
            for process in reversed(suspended):
                if process.is_running():
                    process.resume()


if __name__ == '__main__':
    main()
