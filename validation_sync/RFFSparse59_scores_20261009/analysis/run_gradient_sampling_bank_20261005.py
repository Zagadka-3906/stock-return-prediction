"""Run actual GOSS controls, then serialized annual fits after the wide fit closes."""
from pathlib import Path
import json
import os
import sys
import time
import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]


def main():
    run_path = A / 'gradient_sampling_bank_run_20261005.json'
    deadline = time.monotonic() + 60
    while not run_path.exists():
        assert time.monotonic() < deadline
        time.sleep(.1)
    run = json.loads(run_path.read_text(encoding='utf-8'))
    from locked_read_hash_cache_20261004 import fresh_sha
    for path, expected in run['input_sha256'].items():
        assert fresh_sha(path) == expected, path
    import train_gradient_sampling_bank_20261005 as bank
    for key in ('TMP', 'TEMP', 'TMPDIR'):
        assert Path(os.environ[key]) == Path(bank.read(bank.STORAGE)['temporary_directory'])
    import verify_gradient_sampling_bank_20261005 as controls
    controls.main()
    print('Six actual GOSS native preflights passed; awaiting closure of full16384 annual fit attempt.', flush=True)
    wide = A / 'neural16384_full_bank_20261005/training_execution_scope.json'
    while not wide.exists():
        time.sleep(10)
    print('Actual wide annual attempt closed: ' + bank.read(wide)['status'], flush=True)
    while psutil.virtual_memory().available < 14 * 2**30:
        time.sleep(10)
    from frozen_provenance_execution_scope_20261004 import FrozenProvenanceExecutionScope
    scope = FrozenProvenanceExecutionScope(bank, [Path(__file__), run_path,
        A / 'gradient_sampling_resource_recorder_20261005.py',
        A / 'frozen_provenance_execution_scope_20261004.py',
        A / 'locked_read_hash_cache_20261004.py'], {
        'script': str(Path(__file__)), 'driver_source_sha256': fresh_sha(Path(__file__)),
        'actual30_complete_annual_fits_required': True,
        'original_native_fitter_not_wrapped_or_replaced': True,
        'small_control_fits_excluded_from_complete_annual_fit_counts': True,
        'wide_training_attempt_closed_before_first_full_GOSS_fit': True}, A).install()
    from gradient_sampling_resource_recorder_20261005 import Recorder
    recorder = Recorder(bank.OUT)
    failure, resources = None, None
    try:
        recorder.start()
        bank.all_oof()
    except BaseException as error:
        failure = f'{type(error).__name__}: {error}'
        raise
    finally:
        try:
            resources = recorder.finish()
        finally:
            report = scope.close(failed=failure is not None)
        bank.dump(bank.OUT / 'training_execution_scope.json', {
            'status': 'passed' if failure is None else 'failed', 'failure': failure,
            **report, 'actual_resources': resources, 'new_quality_scores': 0,
            'test_labels_read': False}, immutable=True)


if __name__ == '__main__':
    main()
