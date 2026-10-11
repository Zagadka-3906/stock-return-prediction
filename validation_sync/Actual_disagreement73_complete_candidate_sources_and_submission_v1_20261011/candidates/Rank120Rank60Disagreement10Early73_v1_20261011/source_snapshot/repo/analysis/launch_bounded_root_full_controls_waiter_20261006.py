"""Validate admission rejection and the real independently owned hidden waiter."""
from pathlib import Path
import json
import sys
import time

import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from handoff_ready_goss_full_execution_20261006 import start_service
from wait_bounded_root_full_controls_20261006 import acceptable, NEEDLE


def main():
    folder = A / 'bounded_root_full_controls_waiter_20261006'
    assert not folder.exists()
    enough = {'available_host_bytes': 15 * 2**30, 'required_admission_bytes': 14 * 2**30,
        'D_free_bytes': 3 * 2**30, 'minimum_D_free_bytes': 2 * 2**30}
    assert acceptable(enough, [], {}, NEEDLE)
    assert not acceptable({**enough, 'available_host_bytes': 13 * 2**30}, [], {}, NEEDLE)
    assert not acceptable({**enough, 'D_free_bytes': 1 * 2**30}, [], {}, NEEDLE)
    assert not acceptable(enough, [24224], {}, NEEDLE)
    assert not acceptable(enough, [], {'round95': {'owned_worker_pid': 24224}}, NEEDLE)
    assert not acceptable(enough, [], {}, 'spawn active scientific worker')
    preserved = [read(A / 'service_owned_dependency_queue_v4_20261006/activated_jobs/round95/launch.json'),
        read(A / 'service_owned_workflows_20261006/neural16384_annual/native_launch.json')]
    assert all(owned(row) for row in preserved)
    before_cpu = {str(row['owned_worker_pid']): sum(psutil.Process(row['owned_worker_pid']).cpu_times()[:2])
        for row in preserved}
    sources = [Path(__file__), A / 'wait_bounded_root_full_controls_20261006.py',
        A / 'publish_bounded_root_full_controls_waiter_20261006.py',
        A / 'verify_bounded_root_replay_full_controls_20261006.py',
        A / 'bounded_root_replay_memoization_20261006.py',
        A / 'bounded_root_replay_memoization_semantic_controls_20261006/verification.json']
    for source in sources:
        if source.suffix == '.py': compile(source.read_text(encoding='utf-8'), str(source), 'exec')
    pins = {str(path): sha(path) for path in sources}
    row = start_service('bounded_root_full_controls_waiter',
        'wait_bounded_root_full_controls_20261006.py', [], pins)
    for _ in range(30):
        assert owned(row)
        if (folder / 'state.json').exists(): break
        time.sleep(.5)
    state = read(folder / 'state.json')
    assert state['pid'] == row['owned_worker_pid'] and state['full_controls_started'] is False
    assert state['scientific_processes_held'] == 0
    assert all(owned(value) for value in preserved)
    assert row['actual_native_console_handle'] == 0 and row['independent_launch_root_in_any_job'] is False
    after_cpu = {str(value['owned_worker_pid']): sum(psutil.Process(value['owned_worker_pid']).cpu_times()[:2])
        for value in preserved}
    assert all(after_cpu[pid] >= seconds for pid, seconds in before_cpu.items())
    for path, digest in pins.items(): assert sha(path) == digest, path
    create(folder / 'actual_launch_control.json', {
        'status': 'passed_actual_consoleless_waiter_preserving_live_scientific_processes',
        'actual_waiter': row, 'input_sha256': pins,
        'insufficient_RAM_disk_live_children_live_round_and_nonidle_stack_rejected': True,
        'preserved_live_scientific_processes': preserved, 'before_cpu_seconds': before_cpu,
        'after_cpu_seconds': after_cpu, 'initial_actual_state': state,
        'full5635800_row_control_started': False, 'runtime_adopted': False,
        'new_quality_scores': 0, 'new_native_fits': 0, 'test_labels_read': False})
    print(json.dumps({'status': 'passed_actual_consoleless_waiter_preserving_live_scientific_processes',
        'waiter_pid': row['owned_worker_pid'], 'full_controls_started': False}, ensure_ascii=False), flush=True)


if __name__ == '__main__': main()
