"""Transfer only the dependency controller; preserve live fits, full grids and shared queue state."""
from pathlib import Path
from datetime import datetime
from copy import deepcopy
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

OUT = A / 'exact_rank_cache_dependency_handoff_20261006'
SERVICE = A / 'service_owned_workflows_20261006/dependency_queue_v5'
QUEUE = A / 'service_owned_dependency_queue_v4_20261006'


def identities():
    rows = {}
    for name in ('neural16384_annual', 'main_publisher_v5', 'progress_monitor_v25',
                 'quantile_tree_quality_queue_v2', 'quantile_distribution_views_quality_queue',
                 'distribution_views_full_ranking_publisher'):
        row = read(A / f'service_owned_workflows_20261006/{name}/native_launch.json')
        assert owned(row), name
        rows[name] = row
    row = read(QUEUE / 'activated_jobs/round83/launch.json')
    assert owned(row), 'The existing R83 must remain live throughout this handoff.'
    rows['round83'] = row
    return rows


def main():
    assert not OUT.exists() and not SERVICE.exists() and not (QUEUE / 'queue_plan_v5.json').exists()
    control_path = A / 'exact_rank_cache_actual_scoring_adapter_v2_20261006/verification.json'
    control = read(control_path)
    assert control['status'] == 'passed_actual_two_candidate_adapter_calls_original_official_capsule_and_full_bits'
    assert control['unexpected_official_evaluator_calls'] == control['new_quality_records'] == 0
    route_path = A / 'exact_rank_cache_queue_routes_20261006/verification.json'
    assert read(route_path)['status'] == 'passed_all23_actual_original_round_routes_and_direct89_90_argument_preservation'
    assert psutil.virtual_memory().available >= 8 * 1024**3
    original_plan_path = QUEUE / 'queue_plan.json'
    original_plan = read(original_plan_path)
    old = read(A / 'service_owned_workflows_20261006/dependency_queue_v4/native_launch.json')
    assert owned(old)
    root, worker = psutil.Process(old['pid']), psutil.Process(old['owned_worker_pid'])
    assert root.create_time() == old['owned_parent_creation_time']
    assert root.cmdline()[1:] == worker.cmdline()[1:]
    assert old['script'] in worker.cmdline()
    preserved = identities()
    native_plans = {name: read(A / name / 'plan.json') for name in (
        'quantile_tree_quality_queue_v2_20261006', 'quantile_distribution_views_quality_queue_20261006')}
    assert native_plans['quantile_tree_quality_queue_v2_20261006']['expected_full_records'] == [100, 98]
    assert native_plans['quantile_distribution_views_quality_queue_20261006']['quality_records'] == [124, 138]
    pins = dict(original_plan['input_sha256'])
    additions = [Path(__file__).resolve(), original_plan_path, control_path, route_path,
        A / 'service_owned_workflows_20261006/dependency_queue_v4/job_definition.json',
        A / 'service_owned_workflows_20261006/dependency_queue_v4/native_launch.json',
        *[A / name for name in (
            'run_dependency_queue_v5_20261006.py',
            'run_recovery_qualified_workflow_with_exact_rank_cache_v2_20261006.py',
            'exact_daily_rank_memoization_20261006.py',
            'exact_rank_cache_official_worker_adapter_20261006.py',
            'verify_exact_rank_cache_actual_scoring_adapter_v2_20261006.py',
            'verify_exact_rank_cache_queue_routes_20261006.py',
            'exact_daily_rank_memoization_preflight_20261006/verification.json',
            'exact_rank_cache_complete_scheme_20261006/verification.json',
            'exact_rank_cache_complete_scheme_v2_20261006/verification.json',
            'exact_rank_cache_windows_scoring_initializer_20261006/verification.json',
            'run_recovery_qualified_workflow_v2_20261006.py',
            'launch_service_owned_workflow_with_pwsh_20261006.py',
            'launch_service_owned_windows_workflow_20261006.ps1',
            'run_service_owned_windows_workflow_20261006.py')]]
    pins.update({str(path.resolve()): sha(path) for path in additions})
    for path, digest in pins.items():
        assert sha(path) == digest, path
        if Path(path).suffix == '.py':
            compile(Path(path).read_text(encoding='utf-8-sig'), path, 'exec')
    OUT.mkdir()
    suspended = []
    retired = False
    new_row = None
    new_bootstrap = None
    try:
        for process in (worker, root):
            process.suspend()
            suspended.append(process)
        assert owned(old)
        snapshot = read(QUEUE / 'state.json')
        assert snapshot['pid'] == worker.pid
        assert owned(snapshot['activated_jobs']['round83'])
        assert set(snapshot['activated_jobs']) == {'round82', 'round83'}
        for job in original_plan['deferred_jobs']:
            if job['name'] in snapshot['activated_jobs']:
                continue
            if 'round' in job:
                assert not (A / f'optimization_20261003_r{job["round"]}/protocol.json').exists(), job['name']
        create(OUT / 'original_controller_last_snapshot.json', snapshot)
        pins[str(OUT / 'original_controller_last_snapshot.json')] = sha(OUT / 'original_controller_last_snapshot.json')
        create(OUT / 'frozen_before_controller_handoff.json', {
            'at_local': datetime.now().isoformat(timespec='seconds'), 'input_sha256': pins,
            'old_controller': old, 'preserved_live_scientific_and_publication_identities': preserved,
            'original_all_deferred_jobs': original_plan['deferred_jobs'],
            'original_plan_registry_and_shared_state_directory_preserved': True,
            'original198_and_additional262_quality_grids_preserved': True,
            'old_controller_suspended_only_not_its_children': True,
            'new_quality_scores_by_handoff': 0, 'test_labels_read': False,
            'visible_terminal_windows': visible_terminals()})
        plan = deepcopy(original_plan)
        plan.update(status='frozen_before_exact_rank_cache_queue_v5_actual_handoff',
            at_local=datetime.now().isoformat(timespec='seconds'), input_sha256=pins,
            previously_activated_jobs=deepcopy(snapshot['activated_jobs']),
            prior_queue_plan=str(original_plan_path),
            exact_rank_execution_for_unstarted_single_worker_reference_rounds_only=True,
            exact_rank_cached_rounds=list(range(84, 91)),
            exact_rank_cache_maximum_bytes_per_scoring_worker=1024 * 1024**2,
            activation_handoff_commit_marker=str(OUT / 'handoff_commit.json'),
            minimum_available_bytes_before_new_quality_job=8 * 1024**3,
            original_scientific_parameters_and_native_fits_unchanged=True,
            current_round83_and_all_completed_frozen_protocols_preserved=True,
            shared_queue_state_required_by_original91_92_waiter_preserved=True)
        assert plan['deferred_jobs'] == original_plan['deferred_jobs']
        assert plan['preserved_active_jobs'] == original_plan['preserved_active_jobs']
        assert plan['registry'] == original_plan['registry']
        plan_path = QUEUE / 'queue_plan_v5.json'
        create(plan_path, plan)
        SERVICE.mkdir()
        definition = SERVICE / 'job_definition.json'
        create(definition, {'name': 'dependency_queue_v5',
            'driver': str(A / 'run_dependency_queue_v5_20261006.py'), 'arguments': [str(plan_path)],
            'scratch': str(ROOT / 'tmp/service_owned_dependency_queue_v5_20261006'),
            'input_sha256': {**pins, str(plan_path): sha(plan_path)},
            'bootstrap_sha256': sha(A / 'run_service_owned_windows_workflow_20261006.py'),
            'command_line': subprocess.list2cmdline([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8',
                str(A / 'run_service_owned_windows_workflow_20261006.py'), str(definition)])})
        result = launch(definition, Path('C:/Users/esesl/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/powershell/pwsh.exe'))
        create(SERVICE / 'verified_hidden_launch.json', result)
        bootstrap = psutil.Process(result['actual_launch_result']['ProcessId'])
        assert bootstrap.cmdline()[1:] == ['-B', '-X', 'utf8',
            str(A / 'run_service_owned_windows_workflow_20261006.py'), str(definition)]
        new_bootstrap = {'pid': bootstrap.pid, 'creation_time': bootstrap.create_time(), 'command_line': bootstrap.cmdline()}
        create(SERVICE / 'actual_bootstrap_identity_before_source_hash_completion.json', new_bootstrap)
        started = time.monotonic()
        while True:
            terminal = SERVICE / 'service_execution.json'
            if terminal.exists():
                raise RuntimeError(f'New dependency controller exited before handoff: {read(terminal)}')
            native = SERVICE / 'native_launch.json'
            if native.exists():
                new_row = read(native)
                assert owned(new_row)
                current = read(QUEUE / 'state.json')
                if current['pid'] == new_row['owned_worker_pid']:
                    assert current['activated_jobs'] == snapshot['activated_jobs'], 'New activation must remain held until the old controller is retired.'
                    assert owned(current['activated_jobs']['round83'])
                    break
            if time.monotonic() - started > 600:
                raise TimeoutError('New controller has not reached its original queue loop within the handoff observation bound.')
            print(json.dumps({'stage': 'waiting_actual_queue5_source_verification',
                'seconds_observed': time.monotonic() - started, 'original_R83_and_wide_still_live': all(owned(r) for r in preserved.values())}), flush=True)
            time.sleep(5)
        assert new_row['actual_native_console_handle'] == 0 and not new_row['independent_launch_root_in_any_job']
        for row in preserved.values():
            assert owned(row)
        # Terminate these two exact scheduler processes only. Never recurse into children.
        assert worker.create_time() == old['owned_worker_creation_time'] and root.create_time() == old['owned_parent_creation_time']
        worker.terminate()
        worker.wait(timeout=15)
        root.terminate()
        root.wait(timeout=15)
        retired = True
        suspended.clear()
        assert not owned(old) and owned(new_row)
        assert all(owned(row) for row in preserved.values())
        create(OUT / 'handoff_commit.json', {'status': 'retired_original_controller_and_preserved_scientific_workers',
            'at_local': datetime.now().isoformat(timespec='seconds'), 'old_controller': old,
            'actual_new_controller': new_row, 'original_scientific_workers_preserved': preserved,
            'new_quality_scores': 0, 'test_labels_read': False})
        for source, digest in pins.items():
            assert sha(source) == digest, source
        create(OUT / 'verification.json', {
            'status': 'passed_actual_queue5_controller_handoff_original_full_grids_and_live_workers_preserved',
            'at_local': datetime.now().isoformat(timespec='seconds'), 'input_sha256': pins,
            'old_controller': old, 'actual_new_controller': new_row,
            'preserved_live_scientific_and_publication_identities': preserved,
            'old_controller_only_processes_retired': [worker.pid, root.pid],
            'original_deferred_jobs_exactly_preserved': True, 'original198_and_additional262_grids_preserved': True,
            'shared_queue_state_path': str(QUEUE / 'state.json'), 'same_original_registry': plan['registry'],
            'original_completed_and_R83_protocols_and_scientific_sources_unchanged': True,
            'unstarted_rounds_armed_for_qualified_exact_rank_execution': [job['round'] for job in plan['deferred_jobs']
                if 'round' in job and job['round'] in plan['exact_rank_cached_rounds']],
            'original_four_worker67_to80_execution_preserved_without_extra_rank_cache_RAM': True,
            'direct89_90_original_driver_and_empty_arguments_preserved_and_qualified': True,
            'actual_original_scoring_adapter_two_calls_control': str(control_path),
            'future_armed_rounds_not_claimed_completed': True,
            'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False,
            'global_resource_exhaustion_established': False, 'visible_terminal_windows_after': visible_terminals()})
        print('passed_actual_queue5_controller_handoff_original_full_grids_and_live_workers_preserved', flush=True)
    except BaseException as error:
        # Before retirement the new controller cannot activate any scientific job.
        # Remove only its exact launch processes before resuming the old scheduler.
        if not retired and new_bootstrap is not None:
            assert not (OUT / 'handoff_commit.json').exists()
            try:
                bootstrap = psutil.Process(new_bootstrap['pid'])
                if bootstrap.create_time() == new_bootstrap['creation_time'] and bootstrap.cmdline() == new_bootstrap['command_line']:
                    matches = [p for p in bootstrap.children() if p.name().lower() == 'python.exe'
                        and p.cmdline()[1:] == bootstrap.cmdline()[1:]]
                    assert all(not p.children() for p in matches)
                    for process in matches:
                        process.terminate()
                        process.wait(timeout=15)
                    bootstrap.terminate()
                    bootstrap.wait(timeout=15)
            except psutil.NoSuchProcess:
                pass
        create(OUT / 'failure.json', {'status': 'failed_preserved_controller_handoff',
            'error': f'{type(error).__name__}: {error}', 'old_controller_retired': retired,
            'new_controller_identity_if_observed': new_row})
        raise
    finally:
        if not retired:
            for process in reversed(suspended):
                if process.is_running():
                    process.resume()


if __name__ == '__main__':
    main()
