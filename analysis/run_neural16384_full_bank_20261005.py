"""Wait for qualifiedR66, then measure the actual complete-fit feasibility."""
from pathlib import Path
import json
import os
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis')]


def main():
    from refresh_optimization_boundary_evidence_20261004 import complete_round_evidence
    while complete_round_evidence(66) is None:
        time.sleep(10)
    run = json.loads((ROOT / 'analysis/neural16384_full_run_20261005.json').read_text(encoding='utf-8'))
    from locked_read_hash_cache_20261004 import fresh_sha
    for source, digest in run['input_sha256'].items():
        assert fresh_sha(source) == digest, source
    import psutil
    while psutil.virtual_memory().available < 14 * 2**30:
        time.sleep(10)
    import train_neural16384_full_bank_20261005 as bank
    for variable in ('TMP', 'TEMP', 'TMPDIR'):
        os.environ[variable] = bank.read(bank.STORAGE)['temporary_directory']
    from frozen_provenance_execution_scope_20261004 import FrozenProvenanceExecutionScope
    scope = FrozenProvenanceExecutionScope(bank, [Path(__file__),
        ROOT / 'analysis/neural16384_full_run_20261005.json',
        ROOT / 'analysis/frozen_provenance_execution_scope_20261004.py',
        ROOT / 'analysis/locked_read_hash_cache_20261004.py'], {
        'script': str(Path(__file__)), 'driver_source_sha256': fresh_sha(Path(__file__)),
        'actual_full16384_training_no_one_step_substitution': True,
        'all_qualified_round66_scientific_scope_complete_before_start': True}, ROOT / 'analysis').install()
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
            json.dump({'status': 'passed' if failure is None else 'failed', 'failure': failure, **report,
                'new_quality_scores': 0, 'test_labels_read': False}, stream, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main()
