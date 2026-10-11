"""Replace only the exactly idle observer after verified prefit recovery routes."""
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from handoff_ready_goss_full_execution_20261006 import start_service
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle


def main():
    out = A / 'local_only_monitor_v10_actual_handoff_20261007'
    assert not out.exists()
    out.mkdir()
    old_dir = A / 'service_owned_workflows_20261006/local_only_progress_monitor_v9'
    old = read(old_dir / 'native_launch.json')
    names = ('neural16384_annual', 'dependency_queue_v12_local_cache',
        'cpu_full_universe_HGB_native_bank24_v2', 'cpu_full_universe_ElasticNet_native_bank24_v2')
    preserved = {n: read(A / 'service_owned_workflows_20261006' / n / 'native_launch.json') for n in names}
    assert all(owned(r) for r in preserved.values())
    sources = [Path(__file__), A / 'monitor_local_only_runtime_v10_20261007.py',
        A / 'monitor_local_only_runtime_v9_20261007.py',
        A / 'local_cpu_recovery_observer10_source_preflight_v1_20261007.json',
        A / 'local_cpu_validation_recovery_actual16_hidden_launches_v1_20261007.json']
    pins = {str(p): sha(p) for p in sources}
    create(out / 'frozen_before_handoff.json', {'input_sha256': pins, 'preserved_actual_workers': preserved})
    parent, worker, idle = suspended_idle(old, '    <module> (monitor_local_only_runtime_v9_20261007.py:244)')
    retired = False
    try:
        create(out / 'old_observer_exact_idle_before_and_after.json', idle)
        new = start_service('local_only_progress_monitor_v10', 'monitor_local_only_runtime_v10_20261007.py', [], pins)
        for _ in range(60):
            assert owned(new)
            current = read(A / 'actual_optimization_monitor_state_20261005.json')
            if current.get('actual_observer_version') == 'local_only_v10' and current['local_only_live_status']['monitor_pid'] == new['owned_worker_pid']:
                break
            time.sleep(1)
        else:
            raise RuntimeError('Observer10 has not published a complete actual generation')
        assert current['local_only_live_status']['R90_actual_full_scope_and_main_qualified'] is True
        assert current['local_only_live_status']['services']['cpu_full_universe_HGB_native_bank24_v2']['worker_pid'] == preserved['cpu_full_universe_HGB_native_bank24_v2']['owned_worker_pid']
        assert not worker.children()
        assert all(owned(r) for r in preserved.values())
        create(out / 'actual_first_complete_public_generation.json', current)
        worker.terminate()
        worker.wait(timeout=15)
        parent.terminate()
        parent.wait(timeout=15)
        retired = True
        create(old_dir / 'administrative_supersession_local_v10_20261007.json', {
            'status': 'administratively_retired_exact_idle_observer_not_scientific_completion',
            'identity': old, 'successor': new, 'idle_before_and_after': idle,
            'scientific_workers_stopped_or_restarted': 0})
        assert all(sha(p) == digest for p, digest in pins.items())
        assert all(owned(r) for r in preserved.values())
        create(out / 'verification.json', {
            'status': 'passed_actual_idle_observer10_complete_current_recovery_routes_and_R90_full_qualification_generation',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins, 'new_identity': new,
            'generation': current['complete_observer_generation'], 'preserved_actual_workers': preserved,
            'new_model_fits': 0, 'new_official_scores': 0, 'scientific_workers_stopped_or_restarted': 0,
            'test_labels_read': False})
    finally:
        if not retired:
            for p in (parent, worker):
                if p.is_running():
                    p.resume()


if __name__ == '__main__':
    main()
