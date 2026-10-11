"""Replace only verified idle controllers before any residual candidate inference."""
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, create, sha, owned
from handoff_ready_goss_full_execution_20261006 import start_service
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle

OUT = A / 'conditional_residual_admission_recovery_v2_20261006'


def untouched():
    assert not (A / 'conditional_residual_candidate_admission_20261006/actual_admission.json').exists()
    assert not (A / 'conditional_residual_release_20261006').exists()
    assert not (ROOT / 'candidates/conditional_residual_20261006').exists()


def main():
    assert not OUT.exists()
    OUT.mkdir()
    untouched()
    freeze = A / 'conditional_residual_source_freeze_20261006/manifest.json'
    sources = [Path(__file__), A / 'admit_conditional_residual_candidate_inference_v2_20261006.py',
               A / 'wait_and_seal_conditional_residual_candidate_v2_20261006.py', freeze]
    pins = {str(p): sha(p) for p in sources}
    for relative, info in read(freeze)['files'].items():
        assert sha(ROOT / relative) == info['sha256'], relative
    create(OUT / 'frozen_before_idle_administrative_handoff.json', {
        'input_sha256': pins, 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'actual_candidate_inference_not_started': True, 'scientific_driver_and_all_frozen_math_unchanged': True,
        'failed_original101_publication_status_not_rewritten': True, 'test_labels_read': False})
    for name, needle in (
        ('conditional_residual_candidate_sealing', '    main (wait_and_seal_conditional_residual_candidate_20261006.py:21)'),
        ('conditional_residual_candidate_inference', '    main (admit_conditional_residual_candidate_inference_20261006.py:37)')):
        folder = A / 'service_owned_workflows_20261006' / name
        identity = read(folder / 'native_launch.json')
        parent, worker, idle = suspended_idle(identity, needle)
        retired = False
        try:
            untouched()
            assert not worker.children()
            create(OUT / (name + '_verified_idle_before_and_after.json'), {
                'identity': identity, 'stack': idle, 'no_children': True, 'actual_scientific_candidate_not_started': True})
            worker.terminate(); worker.wait(timeout=15)
            parent.terminate(); parent.wait(timeout=15)
            retired = True
            assert not owned(identity)
            create(folder / 'administrative_supersession_for_residual_admission_v2.json', {
                'status': 'administratively_retired_idle_helper_not_claimed_scientifically_complete',
                'identity': identity, 'successor': name + '_v2',
                'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
                'actual_candidate_inference_not_started': True, 'scientific_workers_stopped_or_restarted': 0})
        finally:
            if not retired:
                for p in (parent, worker):
                    if p.is_running(): p.resume()
    untouched()
    create(OUT / 'verification.json', {
        'status': 'passed_verified_idle_controller_handoff_before_actual_residual_inference',
        'input_sha256': pins, 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'old_sealer_retired_before_old_admission': True, 'scientific_workers_stopped_or_restarted': 0,
        'new_native_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})
    inference = start_service('conditional_residual_candidate_inference_v2', sources[1].name, [], pins)
    sealing = start_service('conditional_residual_candidate_sealing_v2', sources[2].name, [], pins)
    create(OUT / 'actual_successor_hidden_launches.json', {'inference': inference, 'sealing': sealing})
    print('passed_verified_idle_controller_handoff_before_actual_residual_inference', flush=True)


if __name__ == '__main__':
    main()
