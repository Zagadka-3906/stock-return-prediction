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
from causal_entry_exit_buffer_v2_20261006 import transform

OUT = A / 'causal_entry_exit_buffer_full_controls_v3_20261006'


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
    paths = [Path(__file__), A / 'causal_entry_exit_buffer_v2_20261006.py',
        predecessor / 'selected_validation.npy', predecessor / 'calibrated_csv_official.json',
        predecessor / 'component_audit.json', predecessor / 'streaming_rank_classifier_causal_checks.json', panel,
        A / 'recover_causal_entry_exit_buffer_controls_v2_20261006.py',
        A / 'expand_causal_entry_exit_buffer_controls_v3_20261006.py',
        A / 'causal_entry_exit_buffer_full_controls_v2_20261006/verification.json',
        A / 'causal_entry_exit_buffer_full_controls_v2_20261006/actual_parent_transition_diagnostic.json',
        A / 'causal_entry_exit_buffer_full_controls_20261006/failure.json',
        A / 'causal_entry_exit_buffer_full_controls_20261006/frozen_before_full_controls.json']
    assert read(predecessor / 'component_audit.json')['status'] == 'passed'
    audit = read(predecessor / 'calibrated_csv_official.json')
    assert audit['status'] == 'passed' and audit['metrics']['final_score'] == .4510081068915626
    pins = {str(path): sha(path) for path in paths}
    margins = [0., .00025, .0005, .001, .002, .004, .008, .016, .032, .064, .1, .2, .4, .6, .8, 1.]
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
            _, emitted = transform(prediction, dates, flags, codes, 0., True)
            assert emitted['continuous_Jaccard_mean_diagnostic'] == diagnostics['continuous_Jaccard_mean_diagnostic']
            diagnostics['actual_emitted_output_turnover_matches_internal_membership_state'] = True
            digest = hashlib.sha256(memoryview(np.ascontiguousarray(prediction)).cast('B')).hexdigest()
            results.append({'margin': margin, 'diagnostics': diagnostics,
                'full_prediction_numeric_bytes_sha256': digest, 'prefixes': prefixes,
                'changed_future_scores_and_flags_do_not_change_first260_days': True,
                'every_day_eligible_score_multiset_and_flagged_values_bit_preserved': True})
            del prediction, prefix, changed_raw, changed_flags, suffix_changed
    # A positive parameter can be equivalent; this is evidence, not a failure.
    # Diagnose the current parent path. This is not a global turnover bound.
    previous = None
    compulsory_exits = capacity_exits = optional_exits = transitions = 0
    required_margins = []
    for start, end in zip(boundaries[:-1], boundaries[1:]):
        index = np.arange(start, end)[flags[start:end] == 0]
        if len(index) < 100:
            previous = None
            continue
        order = np.lexsort((codes[index], -raw[index]))
        ranked = index[order]
        k = max(len(index) // 10, 1)
        current = set(map(int, codes[ranked[:k]]))
        eligible = set(map(int, codes[index]))
        if previous is not None:
            transitions += 1
            available = previous & eligible
            compulsory_exits += len(previous - eligible)
            mandatory = max(len(available) - k, 0)
            capacity_exits += mandatory
            discretionary = len(available - current) - mandatory
            assert discretionary >= 0
            optional_exits += discretionary
            if discretionary:
                positions = {int(code): i for i, code in enumerate(codes[ranked])}
                best_exiting = min(positions[code] for code in available - current)
                entrants = current - available
                if entrants:
                    worst_entering = max(positions[code] for code in entrants)
                    required_margins.append((best_exiting - worst_entering) / max(len(index)-1, 1))
        previous = current
    path_diagnostic = {'transitions': transitions, 'flag_or_absent_stock_compulsory_exits': compulsory_exits,
        'current_pool_size_compulsory_exits': capacity_exits, 'optional_exits_on_actual_parent_path': optional_exits,
        'first_potential_swap_margin_minimum': min(required_margins) if required_margins else None,
        'first_potential_swap_margin_median': float(np.median(required_margins)) if required_margins else None,
        'not_a_global_bound_or_a_new_official_score': True}
    create(OUT / 'actual_parent_transition_diagnostic.json', path_diagnostic)
    create(OUT / 'verification.json', {
        'status': 'passed_full5635800_row_entry_exit_buffer_causal_and_zero_identity_controls',
        'input_sha256': pins, 'actual_rows': 5635800, 'actual_days': 1212, 'actual_stocks': 4650,
        'actual_all16_margin_controls': results, 'actual_parent_transition_diagnostic': path_diagnostic, 'zero_margin_official_parent_turnover_exact': True, 'positive_noop_cases_preserved_as_evidence': True,
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
