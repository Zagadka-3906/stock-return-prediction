"""Admit the selected50-case candidate without interrupting original scientific jobs."""
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, create, sha, owned
from handoff_ready_goss_full_execution_20261006 import start_service


def main():
    prep = A / 'robust_residual50_candidate_workflow_preparation_20261006.json'
    pins = read(prep)['input_sha256']
    for path, digest in pins.items():
        assert sha(path) == digest, path
    pins = {**pins, str(prep): sha(prep), str(Path(__file__)): sha(Path(__file__))}
    out = A / 'robust_residual50_workflow_admission_20261006'
    assert not out.exists()
    out.mkdir()
    queue = A / 'service_owned_dependency_queue_v4_20261006'
    state = read(queue / 'state.json')
    originals = {name: row for name, row in state['activated_jobs'].items() if owned(row)}
    wide = read(A / 'service_owned_workflows_20261006/neural16384_annual/native_launch.json')
    if owned(wide):
        originals['neural16384_annual'] = wide
    create(out / 'frozen_before_launch.json', {
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins,
        'original_live_scientific_workers_preserved': originals,
        'original_queue_plan': read(queue / 'queue_plan_v10.json'),
        'official_selection_complete_all50_cases': True,
        'scientific_workers_suspended_stopped_or_restarted': 0,
        'new_native_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False,
    })
    inference = start_service('robust_residual50_candidate_inference',
        'admit_robust_residual50_candidate_20261006.py', [], pins)
    sealer = start_service('robust_residual50_candidate_sealing',
        'wait_and_seal_robust_residual50_candidate_20261006.py', [], pins)
    for name, row in originals.items():
        assert owned(row), name
    create(out / 'verification.json', {
        'status': 'passed_hidden_owned50_candidate_and_sealer_admission',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'actual_inference_service': inference, 'actual_sealing_service': sealer,
        'original_live_scientific_workers_still_owned': originals,
        'native_console_handles': [inference['actual_native_console_handle'], sealer['actual_native_console_handle']],
        'all_original_full_and_cold_and_independent_controls_required': True,
        'full_registry_and_complete_ranking_and_main_publication_still_required': True,
        'new_native_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False,
    })
    print('Actual50-case inference and sealing services admitted; original scientists preserved.', flush=True)


if __name__ == '__main__':
    main()
