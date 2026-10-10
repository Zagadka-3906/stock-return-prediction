"""Replace positively idle waiting processes with one declared dependency queue."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import os
import time

import psutil
from windows_hidden_process_launch_20261006 import launch
from atomic_optimization_observer_writes_20261005 import write
from run_dependency_queue_20261006 import ready, owned

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
OUT = A / 'idle_dependency_queue_handoff_20261006'
RECOVERY = A / 'system_reboot_workflow_recovery_20261006'
REGISTRY = A / 'resumed_rounds_dependency_queue_20261006.json'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def create(path, value):
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    assert not OUT.exists()
    OUT.mkdir()
    rows = read(RECOVERY / 'verification.json')['jobs']
    jobs = {row['name']: row for row in rows}
    jobs['gradient_sampling_native'] = read(RECOVERY / 'gradient_sampling_native_v2/launch.json')
    deferred, processes, initial = [], {}, {}
    native_proofs = {
        **{n: 'neural16384_full_future_qa_20261005' for n in (67, 68)},
        **{n: 'linear_leaf_future_qa_20261005' for n in (69, 70, 82)},
        **{n: 'linear_leaf_ensemble_future_qa_20261005' for n in (71, 72)},
        **{n: 'factorization_machine_future_qa_v2_20261005' for n in (73, 74, 83, 84)},
        **{n: 'gradient_sampling_future_qa_20261005' for n in (75, 76)},
        **{n: 'memory_efficient_neural_future_qa_20261005' for n in (77, 78)},
        **{n: 'streaming_rank_classifier_future_qa_v3_20261005' for n in (79, 80, 85, 86)},
        **{n: 'streaming_robust_regression_future_qa_20261005' for n in (87, 88)}}
    wide_exec = A / 'neural16384_full_bank_20261005/training_execution_scope.json'
    goss_exec = A / 'gradient_sampling_bank_20261005/training_execution_scope.json'
    mem = Path(read(A / 'memory_efficient_neural_storage_20261005.json')['output_directory'])
    gpu = Path(read(A / 'memory_efficient_mlp_storage_20261005.json')['GPU_control_directory'])
    native_gates = {
        'neural16384_future': {'markers': [{'path': str(wide_exec)}], 'closed_jobs': ['neural16384_annual']},
        'gradient_sampling_native': {'markers': [{'path': str(wide_exec)}],
                                    'closed_jobs': ['neural16384_annual', 'neural16384_future']},
        'gradient_sampling_future': {'markers': [{'path': str(goss_exec)}], 'closed_jobs': ['gradient_sampling_native']},
        'memory_efficient_neural_native': {
            'markers': [{'path': str(goss_exec)}, {'path': str(gpu / 'verification.json'), 'statuses': ['passed']}],
            'closed_jobs': ['gradient_sampling_native', 'gradient_sampling_future', 'memory_efficient_gpu_controls']},
        'memory_efficient_neural_future': {'markers': [{'path': str(mem / 'training_execution_scope.json')}],
                                          'closed_jobs': ['memory_efficient_neural_native']}}
    for name, row in jobs.items():
        if name.startswith('round') and name != 'round81':
            number = row['round']
            state = read(A / f'ongoing_optimization_r{number}_state.json')
            assert state['status'] == 'running' and state['stage'].startswith('waiting_for_'), name
            gate = {'parent': row['explicit_parent_round'], 'quality_slot': True,
                    'markers': [{'path': str(A / native_proofs[number] / 'verification.json'), 'statuses': ['passed']}]}
            spec = {'name': name, 'round': number, 'gate': gate}
        elif name in native_gates:
            spec = {'name': name, 'gate': native_gates[name]}
            if name.startswith('gradient_sampling'):
                spec['scratch'] = read(A / 'gradient_sampling_storage_20261005.json')['temporary_directory']
            elif name.startswith('memory_efficient_neural'):
                spec['scratch'] = read(A / 'memory_efficient_neural_storage_20261005.json')['temporary_directory']
        else:
            continue
        assert owned(row) and not ready(spec, jobs), name
        worker, parent = psutil.Process(row['owned_worker_pid']), psutil.Process(row['pid'])
        assert worker.ppid() == parent.pid and not [p for p in worker.children(recursive=True) if p.name().lower() != 'conhost.exe'], name
        assert not (Path(row['script_args'][0]).parent / 'resources').exists(), name
        spec.update(previous_run=row['script_args'][0], previous_job=row)
        deferred.append(spec)
        processes[name] = (worker, parent)
        initial[name] = {'cpu': sum(worker.cpu_times()[:2]), 'creation_time': worker.create_time(),
                         'worker_rss': worker.memory_info().rss, 'parent_rss': parent.memory_info().rss}
    assert len(deferred) == 26
    time.sleep(.3)
    for spec in deferred:
        name = spec['name']
        worker, _ = processes[name]
        assert worker.create_time() == initial[name]['creation_time'] and not ready(spec, jobs)
        assert sum(worker.cpu_times()[:2])-initial[name]['cpu'] < .15, name
        assert not [p for p in worker.children(recursive=True) if p.name().lower() != 'conhost.exe'], name
    preserved = {name: row for name, row in jobs.items() if name not in processes}
    for row in preserved.values():
        assert owned(row)
    sources = [Path(__file__), A / 'run_dependency_queue_20261006.py', A / 'windows_hidden_process_launch_20261006.py',
               A / 'run_reboot_recovery_attempt_20261006.py', A / 'atomic_optimization_observer_writes_20261005.py']
    plan = {'status': 'frozen_before_replacing_only26_idle_dependency_waiters',
        'at_local': datetime.now().isoformat(timespec='seconds'),
        'input_sha256': {str(p.resolve()): sha(p) for p in sources}, 'deferred_jobs': deferred,
        'preserved_active_jobs': preserved, 'registry': str(REGISTRY),
        'observed_idle_worker_counters': initial,
        'host_available_bytes_before': psutil.virtual_memory().available,
        'original_required_rounds': list(range(67, 89)),
        'native_epoch_batch_training_inputs_and_scoring_grids_unchanged': True,
        'complete_qualified_checks_still_performed_by_original_drivers': True,
        'no_active_fit_or_official_worker_to_be_closed': True, 'test_labels_read': False}
    plan_path = OUT / 'plan.json'
    create(plan_path, plan)
    closed = []
    for spec in deferred:
        name = spec['name'];worker, parent = processes[name]
        assert owned(spec['previous_job']) and not ready(spec, jobs)
        assert not [p for p in worker.children(recursive=True) if p.name().lower() != 'conhost.exe'], name
        worker.terminate();worker.wait(timeout=10)
        try:
            parent.wait(timeout=2)
        except psutil.TimeoutExpired:
            assert not parent.children(), name
            parent.terminate();parent.wait(timeout=5)
        closed.append(name)
    driver = A / 'run_dependency_queue_20261006.py'
    with (OUT / 'stdout.log').open('xb') as out, (OUT / 'stderr.log').open('xb') as err:
        coordinator = launch([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8', str(driver), str(plan_path)],
                             cwd=ROOT, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1'), stdout=out, stderr=err)
    time.sleep(.5)
    assert coordinator.poll() is None
    parent = psutil.Process(coordinator.pid)
    children = [p for p in parent.children(recursive=True)
                if p.name().lower() == 'python.exe' and p.cmdline()[1:] == parent.cmdline()[1:]]
    assert len(children) == 1
    queue = {'pid': parent.pid, 'script': str(driver), 'script_args': [str(plan_path)],
        'owned_worker_pid': children[0].pid, 'owned_worker_creation_time': children[0].create_time(),
        'stdout': str(OUT / 'stdout.log'), 'stderr': str(OUT / 'stderr.log'),
        'at_local': datetime.now().isoformat(timespec='seconds')}
    create(OUT / 'launch.json', queue)
    registry = read(A / 'resumed_rounds_reboot_20261006.json')
    for row in registry:
        spec = next((item for item in deferred if item.get('round') == row['round']), None)
        if spec:
            row.update(**queue, deferred_original_job=spec['previous_job'], dependency_gate=spec['gate'],
                       queued_without_heavy_imports=True)
            state_path = A / f'ongoing_optimization_r{row["round"]}_state.json'
            state = read(state_path)
            state.update(stage='deferred_waiting_for_original_frozen_dependencies', status='queued',
                         dependency_queue=str(plan_path), updated_at_local=datetime.now().isoformat(timespec='seconds'))
            write(state_path, state)
    create(REGISTRY, registry)
    for name in ('ongoing_optimization_state.json', 'resume_optimization_20261004.json'):
        path = A / name;state = read(path)
        state['active_run_registry'] = REGISTRY.relative_to(ROOT).as_posix()
        state['dependency_queue_registry'] = (OUT / 'launch.json').relative_to(ROOT).as_posix()
        write(path, state)
    for row in preserved.values():
        assert owned(row)
    proof = {'status': 'passed26_verified_idle_waiters_replaced_with_one_live_consoleless_dependency_queue',
        'at_local': datetime.now().isoformat(timespec='seconds'), 'closed_idle_waiters': closed,
        'preserved_active_jobs': preserved, 'dependency_queue': queue,
        'sum_closed_waiter_worker_RSS_bytes_before': sum(row['worker_rss'] for row in initial.values()),
        'queue_RSS_bytes_now': children[0].memory_info().rss,
        'host_available_bytes_after': psutil.virtual_memory().available,
        'host_available_bytes_change': psutil.virtual_memory().available-plan['host_available_bytes_before'],
        'all_required_rounds_preserved': list(range(67, 89)),
        'actual_fits_or_official_workers_stopped': 0, 'scientific_sources_modified': 0,
        'new_model_fits_by_handoff': 0, 'new_quality_scores_by_handoff': 0,
        'global_resource_boundary_established': False, 'test_labels_read': False}
    create(OUT / 'verification.json', proof)
    print(json.dumps({k:v for k,v in proof.items() if k not in ('preserved_active_jobs',)}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
