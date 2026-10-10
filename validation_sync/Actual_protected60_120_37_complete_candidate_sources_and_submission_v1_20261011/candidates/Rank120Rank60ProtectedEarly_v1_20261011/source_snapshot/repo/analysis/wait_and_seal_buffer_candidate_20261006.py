"""Wait for the owned actual inference to exit naturally, then seal its sources."""
from pathlib import Path
import os
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from atomic_optimization_observer_writes_20261005 import write

OUT = A / 'causal_entry_exit_buffer_package_waiter_20261006'


def main():
    assert not OUT.exists()
    OUT.mkdir()
    original = A / 'service_owned_workflows_20261006/causal_entry_exit_buffer_candidate_waiter'
    native = read(original / 'native_launch.json')
    sources = [Path(__file__), A / 'seal_buffer_candidate_source_package_20261006.py',
        A / 'replay_sealed_buffer_candidate_20261006.py',
        A / 'causal_entry_exit_buffer_source_freeze_20261006/manifest.json']
    pins = {str(p): sha(p) for p in sources}
    create(OUT / 'frozen_before_actual_wait.json', {'input_sha256': pins,
        'actual_inference_waiter': native, 'no_training_or_inference_process_changes': True,
        'source_freeze_does_not_count_as_candidate_inference': True, 'test_labels_read': False})
    while True:
        if owned(native):
            write(OUT / 'state.json', {'status': 'waiting_for_owned_actual_candidate_inference_natural_exit',
                'pid': os.getpid(), 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
                'observed_native_inference_pid': native['owned_worker_pid'], 'live_matching_identity': True,
                'scientific_processes_suspended_or_restarted': 0, 'test_labels_read': False})
            time.sleep(5)
            continue
        execution_path = original / 'service_execution.json'
        assert execution_path.exists(), 'Missing native handle alone does not prove successful inference'
        execution = read(execution_path)
        assert execution['status'] == 'passed', execution
        assert read(A / 'causal_entry_exit_buffer_candidate_waiter_20261006/state.json')['status'] == 'completed_actual_frozen_candidate_inference'
        for path, digest in pins.items():
            assert sha(path) == digest, path
        from seal_buffer_candidate_source_package_20261006 import main as seal
        seal()
        write(OUT / 'state.json', {'status': 'completed_actual_candidate_source_package_seal',
            'pid': os.getpid(), 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'actual_sealed_verification': str(A / 'causal_entry_exit_buffer_release_20261006/source_package_verification.json'),
            'formal_full_ranking_and_main_publication_pending': True, 'test_labels_read': False})
        return


if __name__ == '__main__':
    try:
        main()
    except BaseException as error:
        if OUT.exists() and not (OUT / 'failure.json').exists():
            create(OUT / 'failure.json', {'status': 'failed_preserved_actual_candidate_package_wait_or_seal',
                'error': f'{type(error).__name__}: {error}', 'scientific_processes_changed': False})
        raise
