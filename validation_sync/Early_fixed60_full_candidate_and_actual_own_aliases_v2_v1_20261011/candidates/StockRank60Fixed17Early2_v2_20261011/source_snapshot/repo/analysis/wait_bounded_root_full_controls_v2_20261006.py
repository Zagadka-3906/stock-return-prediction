"""Run full cache controls only in an owned empty queue's idle resource window.

The scientific queue is held only after its child tree is empty and its
unchanged sleep stack is verified twice. Existing scientific workers are
never suspended. A separate child runs the controls, so its failure releases
the idle queue in the parent finally block. This does not adopt the cache.
"""
from pathlib import Path
import json
import os
import subprocess
import sys
import time

import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from atomic_optimization_observer_writes_20261005 import write
from handoff_joint_goss_round97_full_execution_20261006 import pair, stack
from windows_hidden_process_launch_20261006 import launch
from verify_bounded_root_replay_full_controls_20261006 import admission

OUT = A / 'bounded_root_full_controls_waiter_v2_20261006'
FULL = A / 'bounded_root_replay_full_controls_20261006'
NEEDLE = '    main (run_dependency_queue_v3_20261006.py:141)'


def acceptable(resources, children, live_rounds, stack_text):
    return (resources['available_host_bytes'] >= resources['required_admission_bytes']
            and resources['D_free_bytes'] >= resources['minimum_D_free_bytes']
            and not children and not live_rounds and NEEDLE in stack_text)


def live_scientific_rounds():
    state = read(A / 'service_owned_dependency_queue_v4_20261006/state.json')
    return {name: row for name, row in state['activated_jobs'].items()
            if name.startswith('round') and owned(row)}


def publish(phase):
    import publish_bounded_root_full_controls_waiter_v2_20261006 as publisher
    publisher.main(phase)


def main():
    assert not OUT.exists() and not FULL.exists()
    OUT.mkdir()
    pins = {str(path): sha(path) for path in (
        Path(__file__), A / 'verify_bounded_root_replay_full_controls_20261006.py',
        A / 'bounded_root_replay_memoization_20261006.py',
        A / 'bounded_root_replay_memoization_semantic_controls_20261006/verification.json',
        A / 'publish_bounded_root_full_controls_waiter_v2_20261006.py',
        A / 'run_dependency_queue_v3_20261006.py',
        A / 'run_dependency_queue_v10_20261006.py',
        A / 'handoff_joint_goss_round97_full_execution_20261006.py',
        A / 'windows_hidden_process_launch_20261006.py',
        A / 'prepare_root_waiter_safe_publication_v2_20261006.py',
        A / 'launch_bounded_root_full_controls_waiter_v2_20261006.py',
        A / 'bounded_root_waiter_safe_publication_preparation_20261006.json',
        A / 'bounded_root_waiter_safe_publication_adoption_20261006/activation.json')}
    create(OUT / 'frozen_before_actual_wait.json', {
        'status': 'frozen_full5635800_row_controls_wait_for_owned_idle_queue10',
        'input_sha256': pins, 'required_admission_bytes': 14 * 2**30,
        'guard_is_scheduling_policy_not_physical_exhaustion': True,
        'original_scientific_grids_and_sources_unchanged': True,
        'new_quality_scores': 0, 'new_native_fits': 0, 'runtime_adopted': False,
        'test_labels_read': False})
    suspended = []
    child = None
    try:
        while True:
            resources = admission()
            handoff = A / 'joint_goss_round97_actual_handoff_20261006/handoff_commit.json'
            native = A / 'service_owned_workflows_20261006/dependency_queue_v10/native_launch.json'
            if not handoff.exists() or not native.exists():
                old = read(A / 'service_owned_workflows_20261006/dependency_queue_v7/native_launch.json')
                rounds = live_scientific_rounds()
                write(OUT / 'state.json', {
                    'status': 'waiting_for_actual_queue10_handoff_and_safe_full_control_admission',
                    'pid': os.getpid(), 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
                    'original_queue_owned_live_now': owned(old),
                    'actual_live_round_pids': {k: v['owned_worker_pid'] for k, v in rounds.items()},
                    'resources': resources, 'scientific_processes_held': 0,
                    'full_controls_started': False, 'new_quality_scores': 0})
                time.sleep(1)
                continue
            assert read(handoff)['status'] == 'retired_original_controller_and_preserved_scientific_workers'
            identity = read(native)
            parent, worker = pair(identity)
            children = worker.children(recursive=True)
            rounds = live_scientific_rounds()
            write(OUT / 'state.json', {
                'status': 'waiting_for_owned_queue10_empty_child_tree_and_resource_window',
                'pid': os.getpid(), 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
                'queue_owned_live_now': True, 'queue_identity': identity,
                'actual_child_pids': [p.pid for p in children],
                'actual_live_round_pids': {k: v['owned_worker_pid'] for k, v in rounds.items()},
                'resources': resources, 'scientific_processes_held': 0,
                'full_controls_started': False, 'new_quality_scores': 0})
            if children or rounds or resources['available_host_bytes'] < resources['required_admission_bytes']:
                time.sleep(1)
                continue
            before = stack(worker.pid)
            if not acceptable(resources, children, rounds, before):
                time.sleep(1)
                continue
            worker.suspend()
            suspended.append(worker)
            parent.suspend()
            suspended.append(parent)
            after = stack(worker.pid)
            second = admission()
            if not acceptable(second, worker.children(recursive=True), live_scientific_rounds(), after):
                for process in reversed(suspended): process.resume()
                suspended = []
                time.sleep(1)
                continue
            for path, digest in pins.items(): assert sha(path) == digest, path
            assert not FULL.exists()
            create(OUT / 'actual_idle_queue_reservation.json', {
                'status': 'passed_actual_empty_queue10_idle_before_and_after_hold_and_14GiB_admission',
                'queue_identity': identity, 'before': before, 'after': after,
                'initial_resources': resources, 'held_resources': second,
                'scientific_workers_held': 0, 'only_empty_queue_helper_pair_held': True})
            with (OUT / 'full_control_stdout.log').open('xb') as stdout, (OUT / 'full_control_stderr.log').open('xb') as stderr:
                child = launch([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8',
                    str(A / 'verify_bounded_root_replay_full_controls_20261006.py'), '--execute'],
                    cwd=ROOT, env=dict(os.environ), stdout=stdout, stderr=stderr)
                launched = psutil.Process(child.pid)
                create(OUT / 'actual_full_control_launch.json', {
                    'pid': child.pid, 'creation_time': launched.create_time(),
                    'command': launched.cmdline(), 'CREATE_NO_WINDOW': True,
                    'original_controls_source_sha256': pins[str(A / 'verify_bounded_root_replay_full_controls_20261006.py')]})
                while child.poll() is None:
                    assert owned(identity)
                    write(OUT / 'state.json', {
                        'status': 'running_actual_full_root_cache_controls_with_idle_queue_reserved',
                        'pid': os.getpid(), 'control_root_pid': child.pid,
                        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
                        'queue_identity': identity, 'scientific_workers_held': 0,
                        'resources': admission(), 'new_quality_scores': 0, 'runtime_adopted': False})
                    time.sleep(1)
            # Release the idle scheduler before any publication or interpretation.
            for process in reversed(suspended): process.resume()
            suspended = []
            for path, digest in pins.items(): assert sha(path) == digest, path
            result = read(FULL / 'verification.json') if (FULL / 'verification.json').exists() else None
            create(OUT / 'actual_full_control_execution.json', {
                'status': 'passed' if child.returncode == 0 and result else 'failed_preserved',
                'returncode': child.returncode, 'full_result': str(FULL / 'verification.json') if result else None,
                'failure_record': str(FULL / 'failure.json') if (FULL / 'failure.json').exists() else None,
                'original_queue_resumed': owned(identity), 'scientific_workers_stopped_or_restarted': 0,
                'runtime_adopted': False, 'new_quality_scores': 0, 'test_labels_read': False})
            publish('execution')
            write(OUT / 'state.json', {
                'status': 'full_controls_finished_result_preserved_and_main_published',
                'pid': os.getpid(), 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
                'returncode': child.returncode, 'runtime_adopted': False,
                'new_quality_scores': 0, 'scientific_workers_stopped_or_restarted': 0})
            return
    finally:
        # The parent outlives its heavy child and resumes the queue even on a
        # child assertion/native failure. Do not resume admission while it runs.
        if child is not None and child.poll() is None: child.wait()
        for process in reversed(suspended):
            if process.is_running(): process.resume()


if __name__ == '__main__':
    while not (A / 'bounded_root_waiter_safe_publication_adoption_20261006/activation.json').exists():
        time.sleep(.25)
    try: main()
    except BaseException as exc:
        if OUT.exists() and not (OUT / 'failure.json').exists():
            create(OUT / 'failure.json', {'status': 'failed_preserved_full_control_waiter',
                'error': f'{type(exc).__name__}: {exc}', 'runtime_adopted': False})
        raise
