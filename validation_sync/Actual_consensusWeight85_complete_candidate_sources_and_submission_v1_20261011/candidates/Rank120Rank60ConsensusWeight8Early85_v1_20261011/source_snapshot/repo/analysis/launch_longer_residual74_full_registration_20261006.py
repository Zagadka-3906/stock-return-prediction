"""Launch the genuine full104 waiting service and preserve its admission evidence."""
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from handoff_ready_goss_full_execution_20261006 import start_service


def main():
    prep = A / 'longer_residual74_full_registration_preparation_20261006.json'
    pins = {**read(prep)['input_sha256'], str(prep): sha(prep), str(Path(__file__)): sha(Path(__file__))}
    for path, digest in pins.items(): assert sha(path) == digest, path
    assert not (A / 'optimization_20261003_r104').exists()
    original88 = read(A / 'service_owned_dependency_queue_v4_20261006/state.json')['activated_jobs']['round88']
    assert owned(original88)
    row = start_service('longer_residual74_round104_full_registration',
        'admit_longer_residual74_round104_full_registration_20261006.py', [], pins)
    assert owned(row) and owned(original88)
    create(A / 'longer_residual74_workflow_admission_20261006/full_registration_hidden_launch.json', {
        'status': 'passed_actual_hidden_owned_full104_admission_waiting_for_genuine_dependencies',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'identity': row, 'original88_still_live_and_preserved': original88,
        'input_sha256': pins, 'actual_native_console_handle': row['actual_native_console_handle'],
        'actual_scientific_selection_and_future_candidate_and_full_ranking_not_claimed_complete': True,
        'scientific_workers_suspended_stopped_or_restarted': 0,
        'test_labels_read': False,
    })
    print('Full104 registration admitted behind actual candidate seal and natural R88 completion.', flush=True)


if __name__ == '__main__': main()
