"""Real complete-OOF causal controls for a new postprocessor; no selection scores."""
from pathlib import Path
import hashlib
import json
import os
import sys

import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create
from causal_entry_exit_buffer_20261006 import transform

OUT = A / 'causal_entry_exit_buffer_full_controls_20261006'


def main():
    assert not OUT.exists()
    resources = {'available_RAM_bytes': psutil.virtual_memory().available,
        'required_admission_bytes': 4 * 2**30, 'D_free_bytes': psutil.disk_usage('D:/').free}
    assert resources['available_RAM_bytes'] >= resources['required_admission_bytes']
    assert resources['D_free_bytes'] >= 2 * 2**30
    OUT.mkdir()
    scratch = ROOT / 'tmp/causal_entry_exit_buffer_controls_20261006'
    scratch.mkdir(exist_ok=True)
    for key in ('TMP', 'TEMP', 'TMPDIR'): os.environ[key] = str(scratch)
    import tempfile
    tempfile.tempdir = str(scratch)
    for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'POLARS_MAX_THREADS'): os.environ[key] = '8'
    import numpy as np
    import polars as pl
    from locked_read_hash_cache_20261004 import LockedReadHashCache
    predecessor = A / 'optimization_20261003_r85'
    panel = A / 'connected_validation_20261002/combined_fold_frame.parquet'
    paths = [Path(__file__), A / 'causal_entry_exit_buffer_20261006.py',
        predecessor / 'selected_validation.npy', predecessor / 'calibrated_csv_official.json',
        predecessor / 'component_audit.json', predecessor / 'streaming_rank_classifier_causal_checks.json', panel]
    assert read(predecessor / 'component_audit.json')['status'] == 'passed'
    audit = read(predecessor / 'calibrated_csv_official.json')
    assert audit['status'] == 'passed' and audit['metrics']['final_score'] == .4510081068915626
    pins = {str(path): sha(path) for path in paths}
    margins = [0., .00025, .0005, .001, .002, .004, .008, .016]
    create(OUT / 'frozen_before_full_controls.json', {
        'status': 'frozen_before_actual_full_entry_exit_buffer_causal_controls',
        'input_sha256': pins, 'margins': margins, 'parent_complete_round': 85,
        'expected_rows_days_stocks': [5635800, 1212, 4650], 'resources': resources,
        'uses_only_current_predictions_current_flags_and_past_membership': True,
        'label_columns_not_loaded': True, 'new_quality_scores': 0,
        'not_a_frozen_submission_scheme_or_an_official_score': True, 'test_labels_read': False})
    results = []
    with LockedReadHashCache(pins):
        # The underlying file is the training OOF panel, not the future panel.
        frame = pl.read_parquet(panel, columns=['ts_code', 'trade_date', 'flag_limit_up'])
        symbols = frame.select('ts_code').unique().sort('ts_code').with_row_index('code')
        frame = frame.join(symbols, on='ts_code', how='left', maintain_order='left')
        dates = frame['trade_date'].to_numpy()
        flags = frame['flag_limit_up'].to_numpy()
        codes = frame['code'].to_numpy()
        raw = np.load(predecessor / 'selected_validation.npy', mmap_mode='r')
        unique_dates = np.unique(dates)
        assert (len(raw), len(unique_dates), len(symbols)) == (5635800, 1212, 4650)
        boundaries = np.r_[0, np.flatnonzero(dates[1:] != dates[:-1]) + 1, len(raw)]
        for margin in margins:
            prediction, diagnostics = transform(raw, dates, flags, codes, margin, True)
            if margin == 0.:
                assert np.array_equal(prediction, raw)
                assert diagnostics['continuous_Jaccard_mean_diagnostic'] == audit['metrics']['mean_turnover']
            assert np.array_equal(prediction[flags == 1], raw[flags == 1])
            for start, end in zip(boundaries[:-1], boundaries[1:]):
                selected = flags[start:end] == 0
                assert np.array_equal(np.sort(prediction[start:end][selected]), np.sort(raw[start:end][selected]))
            prefixes = []
            for days in (80, 260, 975):
                n = int(np.searchsorted(dates, unique_dates[days-1], side='right'))
                prefix = transform(raw[:n], dates[:n], flags[:n], codes[:n], margin)
                assert np.array_equal(prefix, prediction[:n])
                prefixes.append({'days': days, 'rows': n, 'independent_cold_state_bit_identical': True})
            n = int(np.searchsorted(dates, unique_dates[259], side='right'))
            changed_raw = np.array(raw, copy=True)
            changed_raw[n:] *= -1
            changed_flags = flags.copy()
            changed_flags[n:] = 1 - changed_flags[n:]
            suffix_changed = transform(changed_raw, dates, changed_flags, codes, margin)
            assert np.array_equal(suffix_changed[:n], prediction[:n])
            digest = hashlib.sha256(memoryview(np.ascontiguousarray(prediction)).cast('B')).hexdigest()
            results.append({'margin': margin, 'diagnostics': diagnostics,
                'full_prediction_numeric_bytes_sha256': digest, 'prefixes': prefixes,
                'changed_future_scores_and_flags_do_not_change_first260_days': True,
                'every_day_eligible_score_multiset_and_flagged_values_bit_preserved': True})
            del prediction, prefix, changed_raw, changed_flags, suffix_changed
    assert all(row['diagnostics']['changed_membership_days'] > 0 for row in results[1:])
    create(OUT / 'verification.json', {
        'status': 'passed_full5635800_row_entry_exit_buffer_causal_and_zero_identity_controls',
        'input_sha256': pins, 'actual_rows': 5635800, 'actual_days': 1212, 'actual_stocks': 4650,
        'actual_all8_margin_controls': results, 'zero_margin_official_parent_turnover_exact': True,
        'label_columns_not_loaded_or_accepted_by_postprocessor': True,
        'original_parent_sources_and_outputs_unchanged': True,
        'final_mature_return_mapping_8_official_metrics_freeze_and_candidate_controls_pending': True,
        'runtime_adopted': False, 'new_quality_scores': 0, 'new_native_fits': 0, 'test_labels_read': False,
        'global_resource_exhaustion_established': False})
    print(json.dumps({'status': 'passed_full5635800_row_entry_exit_buffer_causal_and_zero_identity_controls',
        'margins': [{'margin': row['margin'], **row['diagnostics']} for row in results]}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    try: main()
    except BaseException as exc:
        if OUT.exists() and not (OUT / 'failure.json').exists():
            create(OUT / 'failure.json', {'status': 'failed_preserved_full_entry_exit_buffer_controls',
                'error': f'{type(exc).__name__}: {exc}'})
        raise
