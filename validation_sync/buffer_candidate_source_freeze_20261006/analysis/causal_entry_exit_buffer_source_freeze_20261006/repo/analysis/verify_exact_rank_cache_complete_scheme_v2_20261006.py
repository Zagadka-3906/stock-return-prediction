"""Actual full R65 replay with a 1GiB cache after the 512MiB LRU capacity control."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import os
import subprocess
import sys
import time

for variable in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'POLARS_MAX_THREADS'):
    os.environ[variable] = '8'
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A), str(A / 'connected_validation_20261002')]
OUT = A / 'exact_rank_cache_complete_scheme_v2_20261006'
from handoff_distribution_views_progress_monitor_20261006 import read, sha, create
from locked_read_hash_cache_20261004 import LockedReadHashCache


def clear_case_caches(ctx):
    cleared = []
    for owner in (ctx, ctx._whole_base):
        for name in ('_diverse_cache', '_final_cache', '_regime_cache', '_raw_cache',
                     '_linear_cache', '_regularization_cache', '_whole_signal_cache', '_whole_regime_cache'):
            value = getattr(owner, name, None)
            if isinstance(value, dict):
                value.clear()
                cleared.append(type(owner).__name__ + '.' + name)
    return cleared


def worker():
    import numpy as np
    import polars as pl
    import psutil
    import optimize_training_round65 as experiment
    from exact_daily_rank_memoization_20261006 import install
    from return_mapping import daily_percentile, apply_mapping
    frozen = read(OUT / 'frozen_before_actual_full_scheme.json')
    selected = read(A / 'optimization_20261003_r65/selection.json')
    expected = np.load(A / 'optimization_20261003_r65/selected_validation.npy', mmap_mode='r')
    measurements = []
    with LockedReadHashCache(frozen['input_sha256']):
        started = time.perf_counter()
        ctx = experiment.Context(fixture=selected['winner'])
        initialize_seconds = time.perf_counter() - started
        assert len(ctx.dates) == 5635800 and len(np.unique(ctx.dates)) == 1212
        cache, restore = None, None
        try:
            for mode in ('original', 'memoized_cold', 'memoized_warm'):
                if mode == 'memoized_cold':
                    cache, restore = install(maximum_bytes=1024 * 1024**2)
                cleared = clear_case_caches(ctx)
                before = cache.statistics() if cache else None
                started = time.perf_counter()
                prediction, construction = ctx.predict(ctx.donor(ctx.finished('baseline')), 0., 0.)
                seconds = time.perf_counter() - started
                assert prediction.dtype == expected.dtype == np.dtype('float64')
                assert np.array_equal(prediction.view(np.uint64), expected.view(np.uint64)), mode
                if measurements:
                    assert construction == reference_construction, mode
                else:
                    reference_construction = construction
                measurement = {'mode': mode, 'prediction_seconds': seconds,
                    'full5635800_float64_bits_identical_to_frozen_selected_prediction': True,
                    'complete_construction_statistics_identical': True, 'cleared_case_caches': cleared,
                    'cache_before': before, 'cache_after': cache.statistics() if cache else None,
                    'worker_rss_bytes': psutil.Process().memory_info().rss}
                measurements.append(measurement)
                create(OUT / (mode + '.json'), measurement)
                print(json.dumps(measurement, ensure_ascii=False), flush=True)
            # The original frozen, past-only per-year mappings define the scored CSV.
            percentile = daily_percentile(ctx.frame.select('trade_date').to_pandas(), prediction)
            mapped = np.empty_like(prediction)
            boundaries = read(A / 'optimization_20261003_r65/causal_validation.json')['fold_calibration_boundaries']
            for year in range(2020, 2025):
                mask = ctx.dates // 10000 == year
                boundary = boundaries[str(year)]
                assert boundary['mapping_last_label_date'] < boundary['exclusive_cutoff'] < int(ctx.dates[mask].min())
                mapping = read(A / f'optimization_20261003_r65/causal_mapping_{year}.json')
                if mapping.get('type') == 'affine_training_moments_fallback':
                    mapped[mask] = mapping['mean'] + mapping['scale'] * (percentile[mask] - .5)
                else:
                    mapped[mask] = apply_mapping(mapping, percentile[mask])
            assert np.array_equal(percentile, daily_percentile(ctx.frame.select('trade_date').to_pandas(), mapped))
            csv = ctx.frame.select(['ts_code', 'trade_date']).with_columns(pl.Series('pred', mapped)).write_csv(float_precision=17)
            csv_sha = hashlib.sha256(csv.encode('utf-8')).hexdigest()
            official = read(A / 'optimization_20261003_r65/calibrated_csv_official.json')
            assert csv_sha == official['csv_sha256']
            assert official['metrics'] == selected['winner']['metrics']
            proof = {'status': 'passed_actual_full_scheme_original_cold_warm_and_official_CSV_bytes',
                'at_local': datetime.now().isoformat(timespec='seconds'), 'actual_worker_pid': os.getpid(),
                'actual_worker_creation_time': psutil.Process().create_time(),
                'actual_spawned_interpreter_command': psutil.Process().cmdline(),
                'cache_installed_inside_spawned_worker': True, 'context_initialization_seconds': initialize_seconds,
                'measurements': measurements, 'cache_statistics': cache.statistics(),
                'validation_shape': [5635800, 1212, 4650], 'official_csv_sha256': csv_sha,
                'official_metrics_for_identical_frozen_CSV': official['metrics'],
                'official_evaluator_rerun_this_control': False,
                'all_original_past_only_mapping_boundaries_preserved': boundaries,
                'new_quality_scores': 0, 'new_model_fits': 0, 'test_labels_read': False,
                'production_adoption_performed': False, 'full_pipeline_speedup_not_inferred_from_function_speedup': True,
                'input_sha256': frozen['input_sha256']}
        finally:
            if restore:
                restore()
    create(OUT / 'verification.json', proof)


def main():
    import psutil
    assert not OUT.exists()
    assert psutil.virtual_memory().available >= 6 * 1024**3, 'Wait for the declared memory scheduling margin.'
    selected = read(A / 'optimization_20261003_r65/selection.json')
    assert read(A / 'exact_daily_rank_memoization_preflight_20261006/verification.json')['status'].startswith('passed_')
    bindings = {str((ROOT / name).resolve()): digest for name, digest in selected['frozen_sha256'].items()}
    paths = [Path(__file__), A / 'verify_exact_rank_cache_complete_scheme_20261006.py', A / 'exact_rank_cache_complete_scheme_20261006/verification.json', A / 'exact_daily_rank_memoization_20261006.py',
        A / 'exact_daily_rank_memoization_preflight_20261006/verification.json',
        A / 'optimization_20261003_r65/selection.json',
        A / 'optimization_20261003_r65/calibrated_csv_official.json',
        A / 'optimization_20261003_r65/calibrated_validation.csv',
        A / 'optimization_20261003_r65/causal_validation.json',
        A / 'connected_validation_20261002/combined_fold_frame.parquet']
    paths += list((A / 'optimization_20261003_r65').glob('causal_mapping_202[0-4].json'))
    for path in paths:
        digest = sha(path)
        if str(path.resolve()) in bindings:
            assert bindings[str(path.resolve())] == digest
        bindings[str(path.resolve())] = digest
    OUT.mkdir()
    create(OUT / 'frozen_before_actual_full_scheme.json', {
        'at_local': datetime.now().isoformat(timespec='seconds'), 'input_sha256': bindings,
        'execution_modes': ['original', 'memoized_cold', 'memoized_warm'], 'memory_cap_bytes': 1024 * 1024**2,
        'original_selected_round': 65, 'original_selected_score': selected['winner']['connected_final_score'],
        'new_quality_scores': 0, 'test_labels_read': False})
    startup = subprocess.STARTUPINFO()
    startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startup.wShowWindow = subprocess.SW_HIDE
    with (OUT / 'actual_worker.log').open('x', encoding='utf-8') as log:
        process = subprocess.Popen([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8',
            str(Path(__file__).resolve()), '--worker'], cwd=ROOT, stdin=subprocess.DEVNULL,
            stdout=log, stderr=subprocess.STDOUT, startupinfo=startup, creationflags=subprocess.CREATE_NO_WINDOW)
        create(OUT / 'actual_worker_launch.json', {'pid': process.pid,
            'creation_time': psutil.Process(process.pid).create_time(), 'command_line': psutil.Process(process.pid).cmdline(),
            'creationflags': subprocess.CREATE_NO_WINDOW, 'show_window': subprocess.SW_HIDE})
        code = process.wait()
    if code:
        create(OUT / 'failure.json', {'status': 'failed_preserved_full_scheme_control', 'exit_code': code})
        raise RuntimeError(f'Actual full scheme worker exited {code}; see {OUT / "actual_worker.log"}')
    assert read(OUT / 'verification.json')['status'].startswith('passed_')
    print(read(OUT / 'verification.json')['status'], flush=True)


if __name__ == '__main__':
    worker() if '--worker' in sys.argv else main()
