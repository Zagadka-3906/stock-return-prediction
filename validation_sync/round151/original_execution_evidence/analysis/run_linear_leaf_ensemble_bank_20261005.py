"""Construct all40 actual mature virtual outputs after native parent scope closes."""
from pathlib import Path
import json
import os
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis')]


def main():
    import build_linear_leaf_ensemble_bank_20261005 as bank
    audit, execution = bank.parent.OUT / 'oof_audit.json', bank.parent.OUT / 'training_execution_scope.json'
    while not (audit.exists() and execution.exists()):
        if execution.exists() and bank.read(execution)['status'] != 'passed':
            raise RuntimeError('Preserve failed parent scope; no ensemble output is admissible.')
        time.sleep(10)
    run = ROOT / 'analysis/linear_leaf_ensemble_bank_run_20261005.json'
    from locked_read_hash_cache_20261004 import fresh_sha
    for source, expected in bank.read(run)['input_sha256'].items():
        assert fresh_sha(source) == expected, source
    for key in ('TMP', 'TEMP', 'TMPDIR'):
        assert Path(os.environ[key]) == Path(bank.read(bank.STORAGE)['temporary_directory'])
    from frozen_provenance_execution_scope_20261004 import FrozenProvenanceExecutionScope
    scope = FrozenProvenanceExecutionScope(bank, [Path(__file__), run,
        ROOT / 'analysis/frozen_provenance_execution_scope_20261004.py',
        ROOT / 'analysis/locked_read_hash_cache_20261004.py'], {
        'script': str(Path(__file__)), 'driver_source_sha256': fresh_sha(Path(__file__)),
        'requires_actual40_composite_outputs_and_native80_day_controls': True,
        'independent_native_model_fits': 0}, ROOT / 'analysis').install()
    failure = None
    try:
        bank.all_oof()
    except BaseException as error:
        failure = f'{type(error).__name__}: {error}'
        raise
    finally:
        report = scope.close(failed=failure is not None)
        bank.OUT.mkdir(parents=True, exist_ok=True)
        with (bank.OUT / 'construction_execution_scope.json').open('x', encoding='utf-8') as stream:
            json.dump({'status': 'passed' if failure is None else 'failed', 'failure': failure, **report,
                'new_native_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False}, stream, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main()
