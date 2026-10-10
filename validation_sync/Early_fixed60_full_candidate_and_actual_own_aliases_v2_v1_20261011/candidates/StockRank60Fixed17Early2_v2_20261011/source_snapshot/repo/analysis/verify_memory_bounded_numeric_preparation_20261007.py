"""Measure numeric preparation on actual historical63 features, not model quality."""
from pathlib import Path
import gc
import hashlib
import os
import sys
import time
import tracemalloc

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
os.environ['POLARS_MAX_THREADS'] = '2'
from run_dependency_queue_v3_20261006 import read, sha, create


def main():
    import numpy as np
    import polars as pl
    import psutil
    from cpu_conditional_residual_mlp_codec_20261007 import fit_preprocessing, prepare as original
    from memory_bounded_numeric_preparation_20261007 import prepare as bounded
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    out = A / 'memory_bounded_numeric_preparation_preflight_20261007'
    assert not out.exists()
    out.mkdir()
    while psutil.virtual_memory().available < 3 * 2**30:
        time.sleep(15)
    paths = [Path(__file__), A / 'memory_bounded_numeric_preparation_20261007.py',
             A / 'cpu_conditional_residual_mlp_codec_20261007.py',
             ROOT / 'data/features.parquet', ROOT / 'data/feature_manifest.json',
             A / 'full_universe_HGB_preprocessing_memory_audit_20261007/verification.json']
    pins = {str(p): sha(p) for p in paths}
    create(out / 'frozen_before_actual_controls.json', {'input_sha256': pins,
        'actual_historical_control_rows': 372000, 'target_labels_not_loaded': True,
        'same_original_statistics_no_reduction_algorithm_changed': True,
        'model_quality_or_original_full24_model_training_not_executed': True})
    controls, measurements = [], []
    with LockedReadHashCache(pins) as scope:
        features = read(ROOT / 'data/feature_manifest.json')['features']
        frame = pl.scan_parquet(ROOT / 'data/features.parquet').filter(
            pl.col('is_train') & (pl.col('trade_date') < 20191231)).select(features).head(372000).collect()
        raw = frame.to_numpy().astype(np.float64)
        assert raw.shape == (372000, 63)
        preprocessing = fit_preprocessing(raw[:8193])
        del frame
        gc.collect()
        for label, matrix in [('historical_F64', np.asfortranarray(raw)),
                              ('historical_C64', np.ascontiguousarray(raw)),
                              ('historical_F32', np.asfortranarray(raw.astype(np.float32))),
                              ('historical_strided', raw[::2])]:
            before = hashlib.sha256(matrix.tobytes(order='C')).hexdigest()
            expected = None
            for repeat, order in enumerate((('original', 'bounded'), ('bounded', 'original'))):
                for backend in order:
                    tracemalloc.start()
                    started = time.perf_counter()
                    actual = (original if backend == 'original' else bounded)(matrix, preprocessing)
                    elapsed = time.perf_counter() - started
                    current, peak = tracemalloc.get_traced_memory()
                    tracemalloc.stop()
                    if expected is None:
                        assert backend == 'original'
                        expected = actual.copy()
                    assert actual.flags.c_contiguous
                    assert np.array_equal(actual.view('u8'), expected.view('u8')), label
                    measurements.append({'layout': label, 'backend': backend, 'repeat': repeat,
                        'rows': len(matrix), 'seconds': elapsed,
                        'actual_extra_tracemalloc_peak_bytes': peak,
                        'raw_input_allocated_before_tracing': True,
                        'float64_C_matrix_bits_exact': True})
                    del actual
                    gc.collect()
            for n in (0, 1, 79, 256, 8191, 8192, 8193, len(matrix)):
                actual = bounded(matrix[:n], preprocessing)
                assert np.array_equal(actual.view('u8'), expected[:n].view('u8'))
                controls.append({'layout': label, 'prefix_rows': n, 'prefix_is_rows_not_trading_days': True,
                                 'independent_prefix_bits_exact': True})
            assert hashlib.sha256(matrix.tobytes(order='C')).hexdigest() == before
            del expected
            gc.collect()
        edge = raw[:8193].copy()
        edge[0, :] = np.nan
        edge[1, :21] = np.inf
        edge[1, 21:42] = -np.inf
        edge[2, :] = -0.0
        expected, actual = original(edge, preprocessing), bounded(edge, preprocessing)
        assert np.array_equal(expected.view('u8'), actual.view('u8'))
        controls.append({'layout': 'all_missing_infinite_and_signed_zero_rows', 'rows': len(edge),
                         'float64_C_matrix_bits_exact': True})
        scope.reverify()
        create(out / 'verification.json', {'status': 'passed_actual_historical372000_rows63_feature_preparation_bits_prefixes_and_allocation_controls',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins,
            'actual_historical_rows': len(raw), 'actual_feature_count': 63,
            'measurements': measurements, 'controls': controls,
            'original_statistics_reused_without_mean_or_std_algorithm_change': True,
            'input_matrices_not_modified': True,
            'tracemalloc_peak_excludes_input_Polars_other_processes_and_native_fits': True,
            'not_adopted_in_frozen_or_live_workflows': True,
            'full6754006_row_training_preparation_and_actual24_native_fits_not_claimed': True,
            'whole_goal_or_whole_training_speedup_not_measured': True,
            'new_native_fits': 0, 'new_official_scores': 0, 'test_labels_read': False})
    print({'status': 'passed', 'actual_historical_rows': len(raw)}, flush=True)


if __name__ == '__main__':
    main()
