"""Compare actual full OOF daily ranks in opposite orders without changing science."""
from pathlib import Path
import ast
import gc
import hashlib
import os
import statistics
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'POLARS_MAX_THREADS'):
    os.environ[key] = '2'
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from atomic_optimization_observer_writes_20261005 import write


def main():
    import numpy as np
    import pandas as pd
    import polars as pl
    import psutil
    from exact_numpy_daily_ranks_20261007 import DaywiseNumpyRanks
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    out = A / 'exact_numpy_daily_ranks_benchmark_20261007'
    assert not out.exists()
    out.mkdir()
    while psutil.virtual_memory().available < 4 * 2**30:
        time.sleep(15)
    original_path = A / 'connected_validation_20261002/optimize_wave15.py'
    tree = ast.parse(original_path.read_text(encoding='utf-8'))
    definition = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'daily_ranks')
    namespace = {'np': np, 'pd': pd}
    exec(compile(ast.fix_missing_locations(ast.Module(body=[definition], type_ignores=[])), str(original_path), 'exec'), namespace)
    original = namespace['daily_ranks']
    operator = DaywiseNumpyRanks(original)
    panel_path = A / 'connected_validation_20261002/combined_fold_frame.parquet'
    heads = {
        'actual_R88_selected': A / 'optimization_20261003_r88/selected_validation.npy',
        'actual_R106_selected': A / 'optimization_20261003_r106/selected_validation.npy',
        'actual_W5a_raw': A / 'connected_validation_20261002/w5a_raw_fold.npy',
    }
    sources = [Path(__file__), A / 'exact_numpy_daily_ranks_20261007.py', original_path,
               panel_path, ROOT / '后续选模标准.md', *heads.values()]
    pins = {str(p.resolve()): sha(p) for p in sources}
    preserved_names = ('neural16384_annual', 'classifier_consensus_R90_root_resolution_recovery_v3')
    identities = {n: read(A / 'service_owned_workflows_20261006' / n / 'native_launch.json') for n in preserved_names}
    create(out / 'frozen_before_actual_controls.json', {
        'input_sha256': pins, 'heads': {k: str(v) for k, v in heads.items()},
        'orders': [['original', 'numpy'], ['numpy', 'original']], 'repeats': 2,
        'full_rows': 5635800, 'full_days': 1212, 'cold_whole_day_prefixes': [80, 260, 975],
        'existing_scientific_process_identities': identities,
        'no_bindings_in_live_scientific_processes_modified': True,
        'official_scoring_and_whole_graph_replay_not_executed_by_this_operator_control': True,
        'new_model_fits': 0, 'new_official_scores': 0, 'test_labels_read': False})
    started = time.perf_counter()
    timings, prefix_controls, small_controls = [], [], []
    with LockedReadHashCache(pins) as scope:
        # Full edge coverage uses the literal original Pandas function as oracle.
        base = np.array([-10., -9., np.nextafter(-9., np.inf), -9.1, np.nan,
                         np.inf, -np.inf, -0., 0., 1., 1., 2.])
        for dtype in (np.float32, np.float64):
            values = np.tile(base.astype(dtype), 4)
            dates = np.repeat(np.arange(4, dtype=np.int64), len(base))
            valid = np.ones(len(values), dtype=bool)
            for label, mask in [('all_valid', valid), ('some_invalid', np.arange(len(values)) % 3 != 0),
                                ('all_invalid', np.zeros(len(values), dtype=bool))]:
                expected = original(values, mask, dates)
                actual = operator(values, mask, dates)
                assert np.array_equal(expected.view('u8'), actual.view('u8'))
                small_controls.append({'label': label, 'dtype': np.dtype(dtype).name, 'rows': len(values), 'raw_float64_bits_exact': True})
        for label, values, valid, dates in [
            ('empty', np.array([], dtype=float), np.array([], dtype=bool), np.array([], dtype=np.int64)),
            ('unsorted_dates_fallback', np.array([1., 2., 2., 3.]), np.ones(4, dtype=bool), np.array([2, 1, 2, 1])),
            ('noninteger_dates_fallback', np.array([1., 2., 2., 3.]), np.ones(4, dtype=bool), np.array([2., np.nan, 2., 1.])),
            ('large_integer_values_fallback', np.array([2**60, 2**60+1, 2**60+2], dtype=np.int64), np.ones(3, dtype=bool), np.ones(3, dtype=np.int64)),
        ]:
            expected, actual = original(values, valid, dates), operator(values, valid, dates)
            assert np.array_equal(expected.view('u8'), actual.view('u8')), label
            small_controls.append({'label': label, 'rows': len(values), 'raw_float64_bits_exact': True})
        frame = pl.read_parquet(panel_path, columns=['trade_date', 'price_valid'])
        dates, valid = frame['trade_date'].to_numpy(), frame['price_valid'].to_numpy()
        days = np.unique(dates)
        assert len(dates) == 5635800 and len(days) == 1212
        assert dates.dtype.kind in 'iu' and valid.dtype == np.dtype(bool)
        del frame
        gc.collect()
        for label, path in heads.items():
            values = np.load(path, mmap_mode='r')
            assert len(values) == len(dates)
            oracle = None
            for repeat, order in enumerate((('original', 'numpy'), ('numpy', 'original'))):
                for backend in order:
                    write(out / 'actual_stage.json', {'status': 'actual_full_OOF_daily_rank_operator_benchmark',
                        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'head': label,
                        'repeat': repeat, 'backend': backend, 'test_labels_read': False})
                    t = time.perf_counter()
                    result = (original if backend == 'original' else operator)(values, valid, dates)
                    elapsed = time.perf_counter() - t
                    if oracle is None:
                        assert backend == 'original'
                        oracle = result.copy()
                    assert np.array_equal(result.view('u8'), oracle.view('u8'))
                    timings.append({'head': label, 'repeat': repeat, 'backend': backend,
                        'rows': len(values), 'seconds': elapsed, 'full_float64_bits_exact': True})
                    del result
                    gc.collect()
            for count in (80, 260, 975):
                n = int(np.searchsorted(dates, days[count-1], side='right'))
                actual = operator(values[:n], valid[:n], dates[:n])
                assert np.array_equal(actual.view('u8'), oracle[:n].view('u8'))
                prefix_controls.append({'head': label, 'days': count, 'rows': n,
                                        'cold_no_full_prediction_cache_and_prefix_bits_exact': True})
                del actual
            create(out / (label + '_rank_digest.json'), {'rows': len(oracle),
                'numeric_sha256': hashlib.sha256(memoryview(oracle).cast('B')).hexdigest()})
            del oracle, values
            gc.collect()
        assert len(timings) == 12 and len(prefix_controls) == 9
        medians = {backend: statistics.median(r['seconds'] for r in timings if r['backend'] == backend)
                   for backend in ('original', 'numpy')}
        scope.reverify()
        create(out / 'verification.json', {
            'status': 'passed_actual_three_full5635800_heads_two_opposite_orders_daily_rank_and_cold_prefix_controls',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins,
            'timings': timings, 'median_seconds': medians,
            'median_operator_phase_speedup': medians['original'] / medians['numpy'],
            'small_controls': small_controls, 'cold_prefix_controls': prefix_controls,
            'operator_statistics': operator.statistics(), 'elapsed_seconds': time.perf_counter()-started,
            'numpy_version': np.__version__, 'pandas_version': pd.__version__,
            'full5635800_graph_inference_official_metrics_future_candidate_not_verified_by_this_operator_control': True,
            'operator_not_adopted_in_live_or_previously_frozen_scientific_workflows': True,
            'whole_goal_speedup_not_measured': True, 'scientific_processes_stopped_or_restarted': 0,
            'original_scientific_worker_live_at_end': {n: owned(r) for n, r in identities.items()},
            'new_model_fits': 0, 'new_official_scores': 0, 'test_labels_read': False})
        print({'status': 'passed', 'median_operator_phase_speedup': medians['original']/medians['numpy']}, flush=True)


if __name__ == '__main__':
    main()
