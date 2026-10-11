"""Run preflight and serialized30 actual annual fits under frozen source scope."""
from pathlib import Path
import json
import os
import sys
import time

import psutil

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis')]


def main():
    run_path = ROOT / 'analysis/linear_leaf_bank_run_20261005.json'
    deadline = time.monotonic() + 60
    while not run_path.exists():
        assert time.monotonic() < deadline
        time.sleep(.1)
    run = json.loads(run_path.read_text(encoding='utf-8'))
    from locked_read_hash_cache_20261004 import fresh_sha
    for source, expected in run['input_sha256'].items():
        assert fresh_sha(source) == expected, source
    import train_linear_leaf_bank_20261005 as bank
    for key in ('TMP', 'TEMP', 'TMPDIR'):
        assert Path(os.environ[key]) == Path(bank.read(bank.STORAGE)['temporary_directory'])
    import verify_linear_leaf_bank_20261005 as preflight
    preflight.main()
    print('All6 actual linear-leaf native preflights passed; waiting for14GiB host fit reserve.', flush=True)
    while psutil.virtual_memory().available < 14 * 2**30:
        time.sleep(10)
    from frozen_provenance_execution_scope_20261004 import FrozenProvenanceExecutionScope
    scope = FrozenProvenanceExecutionScope(bank, [Path(__file__), run_path,
        ROOT / 'analysis/frozen_provenance_execution_scope_20261004.py',
        ROOT / 'analysis/locked_read_hash_cache_20261004.py'], {
        'script': str(Path(__file__)), 'driver_source_sha256': fresh_sha(Path(__file__)),
        'actual30_complete_annual_fits_required': True,
        'small48_round_controls_excluded_from_complete_annual_fit_counts': True}, ROOT / 'analysis').install()
    failure = None
    try:
        bank.all_oof()
    except BaseException as error:
        failure = f'{type(error).__name__}: {error}'
        raise
    finally:
        report = scope.close(failed=failure is not None)
        bank.OUT.mkdir(parents=True, exist_ok=True)
        with (bank.OUT / 'training_execution_scope.json').open('x', encoding='utf-8') as stream:
            json.dump({'status': 'passed' if failure is None else 'failed', 'failure': failure,
                **report, 'new_quality_scores': 0, 'test_labels_read': False}, stream, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main()
