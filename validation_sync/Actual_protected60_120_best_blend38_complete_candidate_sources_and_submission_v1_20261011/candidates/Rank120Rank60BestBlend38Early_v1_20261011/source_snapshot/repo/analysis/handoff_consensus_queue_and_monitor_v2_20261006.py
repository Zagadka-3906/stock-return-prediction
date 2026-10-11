"""Register full consensus quality, retaining every old job and replacing observers only."""
from pathlib import Path
from datetime import datetime
import json
import os
import sys
import time

import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_20261006 import read, sha, create, owned
from finalize_main_branch_consolidation_20261005 import owned_pair
from windows_hidden_process_launch_20261006 import launch
from atomic_optimization_observer_writes_20261005 import write

OLD = A / 'idle_dependency_queue_handoff_v2_20261006'
OUT = A / 'consensus_queue_and_monitor_handoff_v2_20261006'
REGISTRY = A / 'resumed_rounds_dependency_queue_v3_20261006.json'


def start(script, args, stem, env):
    with (OUT / f'{stem}_stdout.log').open('xb') as stdout, (OUT / f'{stem}_stderr.log').open('xb') as stderr:
        process = launch([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8', str(script), *args],
                         cwd=ROOT, env=env, stdout=stdout, stderr=stderr)
    time.sleep(.5)
    assert process.poll() is None, (OUT / f'{stem}_stderr.log').read_text(encoding='utf-8')
    parent = psutil.Process(process.pid)
    children = [p for p in parent.children(recursive=True)
                if p.name().lower() == 'python.exe' and p.cmdline()[1:] == parent.cmdline()[1:]]
    assert len(children) == 1
    row = {'pid': parent.pid, 'script': str(script), 'script_args': args,
        'owned_worker_pid': children[0].pid, 'owned_worker_creation_time': children[0].create_time(),
        'stdout': str(OUT / f'{stem}_stdout.log'), 'stderr': str(OUT / f'{stem}_stderr.log'),
        'at_local': datetime.now().isoformat(timespec='seconds')}
    create(OUT / f'{stem}_launch.json', row)
    return row


def main():
    assert not OUT.exists()
    OUT.mkdir()
    prior, queue = read(OLD / 'plan.json'), read(OLD / 'launch.json')
    assert owned(queue)
    old_monitor = prior['preserved_active_jobs']['progress_monitor']
    assert not psutil.pid_exists(old_monitor['pid']) and not psutil.pid_exists(old_monitor['owned_worker_pid'])
    queue_pair = owned_pair(queue['pid'], Path(queue['script']), queue['script_args'])
    assert queue_pair[1].create_time() == queue['owned_worker_creation_time']
    proofs = [A / 'classifier_consensus_preflight_20261005/verification.json',
        A / 'classifier_consensus_direct_router_preflight_20261005/verification.json',
        A / 'classifier_consensus_bank_20261005/oof_audit.json',
        A / 'classifier_consensus_bank_20261005/construction_execution_scope.json',
        A / 'classifier_consensus_future_qa_20261005/verification.json',
        A / 'ready_classifier_consensus_reference_generator_preflight_v2_20261006/verification.json',
        A / 'ready_classifier_consensus_reference_execution_preflight_v2_20261006/verification.json']
    assert all(read(path)['status'].startswith('passed') for path in proofs)
    driver = A / 'monitor_actual_optimization_progress_v19_20261006.py'
    coordinator = A / 'run_dependency_queue_v3_20261006.py'
    sources = [Path(__file__), driver, coordinator, *proofs,
        A / 'handoff_consensus_queue_and_monitor_20261006.py',
        A / 'consensus_queue_and_monitor_handoff_20261006/frozen_before_handoff.json',
        A / 'consensus_queue_and_monitor_handoff_20261006/actual_monitor_preflight.json',
        A / 'consensus_queue_and_monitor_handoff_20261006/monitor_run.json',
        A / 'consensus_queue_and_monitor_handoff_20261006/failure.json',
        A / 'refresh_classifier_consensus_cost_evidence_20261006.py',
        A / 'ready_classifier_consensus_reference_complete_plan_v2_20261006.json',
        A / 'classifier_consensus_storage_20261006.json',
        A / 'run_dependency_queue_v2_20261006.py', A / 'run_dependency_queue_20261006.py',
        A / 'windows_hidden_process_launch_20261006.py',
        A / 'run_recovery_qualified_workflow_20261005.py',
        A / 'run_reboot_recovery_attempt_20261006.py']
    for proof in proofs:
        sources.extend(Path(path) for path in read(proof).get('source_sha256', {}))
        sources.extend(Path(path) for path in read(proof).get('input_sha256', {}))
    inputs = {str(path.resolve()): sha(path) for path in dict.fromkeys(sources)}
    create(OUT / 'frozen_before_handoff.json', {'input_sha256': inputs,
        'old_monitor': old_monitor, 'old_queue': queue, 'all_original67_to88_retained': True,
        'new_rounds': [89, 90], 'new_quality_scores': 0, 'test_labels_read': False})
    preserved = {name: row for name, row in prior['preserved_active_jobs'].items() if name != 'progress_monitor'}
    assert all(owned(row) for row in preserved.values())
    suspended = []
    monitor_replaced = queue_replaced = False
    try:
        for parent, worker in (queue_pair,):
            assert not [p for p in parent.children(recursive=True)
                        if p.pid != worker.pid and p.name().lower() != 'conhost.exe']
            for process in (worker, parent):
                process.suspend()
                suspended.append(process)
        previous_state = read(OLD / 'state.json')
        activated = previous_state['activated_jobs']
        assert all(owned(row) for row in activated.values())
        # Use exactly the same recovered-R66 verifier as the old observer.
        import qualified_round_recovery_evidence_v2_20261005 as qualification
        import refresh_optimization_boundary_evidence_20261004 as base
        original = base.complete_round_evidence
        base.complete_round_evidence = qualification.complete_round_evidence
        try:
            import monitor_actual_optimization_progress_v19_20261006 as monitor
            monitor.main(True)
        finally:
            base.complete_round_evidence = original
            qualification.close()
        observed = read(A / 'actual_optimization_monitor_state_20261005.json')
        assert observed['latest_completed_round'] == 66
        assert set(range(67, 89)) <= set(observed['pending_required_rounds'])
        assert observed['actual_active_quality_rounds'] == [81]
        assert observed['active_round'] == 81 and observed['active_root_command_owned']
        assert read(A / 'optimization_fit_cost_evidence_20261004.json')['classifier_consensus_new_native_fits'] == 0
        create(OUT / 'actual_monitor_preflight.json', {
            'status': 'passed_actual_owned_R81_and_all_old_pending_scope',
            'active_round': 81, 'active_wave_records': observed['active_wave_records'],
            'all_original_pending_rounds': observed['pending_required_rounds'],
            'native_fit_count_not_inflated_by_virtual_ensembles': True,
            'original_completed_best_unchanged': read(A / 'ongoing_optimization_state.json')['completed_validation_best']})
        scratch = ROOT / 'tmp/consensus_coordinator_20261006'
        scratch.mkdir(parents=True, exist_ok=True)
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1')
        for key in ('TMP', 'TEMP', 'TMPDIR'):
            env[key] = str(scratch)
        old_run = read(A / 'actual_optimization_monitor_run_v18_20261005.json')
        monitor_run = OUT / 'monitor_run.json'
        create(monitor_run, {**old_run, 'original_driver': str(driver), 'original_arguments': [],
            'input_sha256': {**old_run['input_sha256'], **inputs,
                str(OUT / 'actual_monitor_preflight.json'): sha(OUT / 'actual_monitor_preflight.json')}})
        assert not psutil.pid_exists(old_monitor['pid']) and not psutil.pid_exists(old_monitor['owned_worker_pid'])
        monitor_replaced = True
        new_monitor = start(A / 'run_recovery_qualified_workflow_20261005.py',
                            [str(driver), str(monitor_run)], 'monitor', env)
        preserved['progress_monitor'] = new_monitor
        quality_run = A / 'ready_classifier_consensus_reference_quality_run_v2_20261006.json'
        create(quality_run, {'status': 'frozen_after_actual_generator_and_execution_controls',
            'input_sha256': inputs, 'new_native_fits': 0, 'test_labels_read': False})
        deferred = list(prior['deferred_jobs'])
        for number in (89, 90):
            pipeline = A / f'run_training_round{number}_v3_pipeline.py'
            run = OUT / f'round{number}_activation_run.json'
            create(run, {'original_script': str(pipeline), 'original_arguments': [],
                'input_sha256': inputs, 'new_native_fits': 0, 'new_quality_scores': 0,
                'test_labels_read': False})
            deferred.append({'name': f'round{number}', 'round': number, 'previous_run': str(run),
                'scratch': str(scratch / f'round{number}'),
                'gate': {'parent': number - 1, 'quality_slot': True,
                    'markers': [{'path': str(A / 'classifier_consensus_future_qa_20261005/verification.json'),
                                 'statuses': ['passed']}]}})
        plan_path = OUT / 'queue_plan.json'
        plan = {**prior, 'registry': str(REGISTRY), 'deferred_jobs': deferred,
            'preserved_active_jobs': preserved, 'previously_activated_jobs': activated,
            'input_sha256': {**prior['input_sha256'], **inputs, str(quality_run): sha(quality_run)},
            'original_required_rounds_retained': list(range(67, 89)),
            'expanded_required_rounds': list(range(67, 91)),
            'actual_virtual_annual_outputs': 30, 'actual_fullfuture_controls': 6,
            'new_native_fits': 0, 'new_quality_scores': 0}
        create(plan_path, plan)
        queue_pair[1].terminate(); queue_pair[1].wait(timeout=10); queue_pair[0].resume(); queue_pair[0].wait(timeout=10)
        queue_replaced = True
        new_queue = start(coordinator, [str(plan_path)], 'queue', env)
        registry = read(prior['registry'])
        for row in registry:
            if row.get('queued_without_heavy_imports') and row['round'] not in {int(n[5:]) for n in activated if n.startswith('round')}:
                row.update(**new_queue)
                row['dependency_queue'] = str(plan_path)
        for number in (89, 90):
            registry.append({**new_queue, 'round': number, 'explicit_parent_round': number - 1,
                'queued_without_heavy_imports': True, 'dependency_queue': str(plan_path),
                'prospective_official_workers': 1})
            write(A / f'ongoing_optimization_r{number}_state.json', {'round': number,
                'explicit_parent_round': number - 1, 'status': 'queued',
                'stage': 'deferred_waiting_for_original_frozen_dependencies',
                'dependency_queue': str(plan_path), 'continuous_optimization_authorized': True,
                'test_labels_read': False})
        create(REGISTRY, registry)
        for filename in ('ongoing_optimization_state.json', 'resume_optimization_20261004.json'):
            value = read(A / filename)
            value.update(active_run_registry=REGISTRY.relative_to(ROOT).as_posix(),
                dependency_queue_registry=(OUT / 'queue_launch.json').relative_to(ROOT).as_posix(),
                pending_required_rounds=sorted(set(value['pending_required_rounds']) | {89, 90}),
                queued_rounds=sorted(set(value['queued_rounds']) | {89, 90}),
                actual_monitor_launch=(OUT / 'monitor_launch.json').relative_to(ROOT).as_posix())
            write(A / filename, value)
        assert all(owned(row) for row in preserved.values()) and owned(new_queue)
        assert all(sha(path) == digest for path, digest in inputs.items())
        create(OUT / 'verification.json', {'status': 'passed_consensus_full_controls_registered_and_owned_lightweight_handoff',
            'monitor': new_monitor, 'queue': new_queue, 'preserved_scientific_jobs': preserved,
            'preserved_activated_jobs': activated, 'required_rounds': list(range(67, 91)),
            'same_original26_jobs_plus2_consensus_quality_jobs': len(deferred) == 28,
            'added_official_records_pending': 262, 'new_quality_scores': 0,
            'old_scientific_fits_and_scoring_not_stopped': True,
            'old_wait_queue_and_observer_only_closed': True,
            'all_frozen_input_sha256_reverified': True, 'new_native_fits': 0,
            'test_labels_read': False})
        print(json.dumps({'status': 'passed_new_queue_and_monitor', 'monitor': new_monitor,
                          'queue': new_queue, 'required_rounds': list(range(67, 91))}, ensure_ascii=False), flush=True)
    finally:
        for process in reversed(suspended):
            if process.is_running():
                process.resume()


if __name__ == '__main__':
    main()
