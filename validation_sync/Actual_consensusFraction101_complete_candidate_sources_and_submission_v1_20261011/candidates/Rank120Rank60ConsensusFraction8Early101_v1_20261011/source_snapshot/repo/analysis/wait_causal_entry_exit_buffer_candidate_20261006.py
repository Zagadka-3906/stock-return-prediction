"""Wait for the unchanged candidate program's memory admission, then execute it."""
from pathlib import Path
import json
import os
import runpy
import sys
import time
import traceback

import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create
from atomic_optimization_observer_writes_20261005 import write

OUT = A / 'causal_entry_exit_buffer_candidate_waiter_20261006'
RELEASE = A / 'causal_entry_exit_buffer_release_20261006'
CANDIDATE = ROOT / 'candidates/causal_entry_exit_buffer_20261006'


def main():
    assert not OUT.exists() and not RELEASE.exists() and not CANDIDATE.exists()
    OUT.mkdir()
    source = A / 'freeze_and_infer_causal_entry_exit_buffer_20261006.py'
    pins = {str(path): sha(path) for path in (Path(__file__), source,
        A / 'service_owned_workflows_20261006/causal_entry_exit_buffer_frozen_inference/service_execution.json')}
    create(OUT / 'frozen_before_actual_wait.json', {'input_sha256': pins,
        'initial_attempt_failed_only_before_outputs_at8GiB_admission': True,
        'science_script_and_selection_rule_unchanged': True, 'test_labels_read': False})
    consecutive = rejected = 0
    while True:
        available = psutil.virtual_memory().available
        consecutive = consecutive + 1 if available >= 9 * 2**30 else 0
        write(OUT / 'state.json', {'status': 'waiting_for_candidate_memory_admission',
            'pid': os.getpid(), 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'available_host_bytes': available, 'waiting_guard_bytes': 9 * 2**30,
            'original_scientific_admission_bytes': 8 * 2**30,
            'consecutive_safe_samples': consecutive, 'resource_gate_rejections_before_outputs': rejected,
            'scientific_processes_suspended_or_restarted': 0, 'test_labels_read': False})
        if consecutive < 2:
            time.sleep(2)
            continue
        for path, digest in pins.items(): assert sha(path) == digest, path
        try:
            runpy.run_path(str(source), run_name='__main__')
        except AssertionError as error:
            last = traceback.extract_tb(error.__traceback__)[-1]
            if (Path(last.filename).resolve() == source.resolve() and last.lineno == 21
                    and not RELEASE.exists() and not CANDIDATE.exists()):
                rejected += 1
                consecutive = 0
                continue
            raise
        assert read(RELEASE / 'verification.json')['status'] == 'passed_actual_frozen_zero_buffer_full_candidate_saved_model_reload_and_cold80'
        write(OUT / 'state.json', {'status': 'completed_actual_frozen_candidate_inference',
            'pid': os.getpid(), 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'actual_verification': str(RELEASE / 'verification.json'),
            'test_labels_read': False, 'formal_full_ranking_qualification_pending': True})
        return


if __name__ == '__main__':
    try: main()
    except BaseException as exc:
        if OUT.exists() and not (OUT / 'failure.json').exists():
            create(OUT / 'failure.json', {'status': 'failed_preserved_candidate_wait_and_execution',
                'error': f'{type(exc).__name__}: {exc}'})
        raise
