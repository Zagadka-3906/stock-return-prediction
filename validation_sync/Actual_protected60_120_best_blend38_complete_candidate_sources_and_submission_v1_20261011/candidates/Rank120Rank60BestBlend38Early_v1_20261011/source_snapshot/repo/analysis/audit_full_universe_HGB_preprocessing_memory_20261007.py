"""Count actual mature training rows and bound simultaneous NumPy allocations."""
from pathlib import Path
import os
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
os.environ['POLARS_MAX_THREADS'] = '2'
from run_dependency_queue_v3_20261006 import read, sha, create


def main():
    import numpy as np
    import polars as pl
    import psutil
    import tracemalloc
    from cpu_conditional_residual_mlp_codec_20261007 import prepare
    out = A / 'full_universe_HGB_preprocessing_memory_audit_20261007'
    assert not out.exists()
    out.mkdir()
    paths = [Path(__file__), ROOT / 'data/features.parquet', ROOT / 'data/feature_manifest.json',
             A / 'cpu_conditional_residual_mlp_codec_20261007.py',
             A / 'train_cpu_full_universe_HGB_bank24_20261007.py',
             A / 'cpu_full_universe_HGB_bank24_plan_20261007.json', ROOT / 'run.py']
    pins = {str(p): sha(p) for p in paths}
    lazy = pl.scan_parquet(ROOT / 'data/features.parquet')
    days = lazy.filter(pl.col('is_train')).select('trade_date').unique().sort('trade_date').collect()['trade_date'].to_numpy()
    cutoffs = {y: int(days[np.searchsorted(days, y * 10000 + 101) - 1]) for y in range(2020, 2026)}
    expressions = [((pl.col('trade_date') < cutoff) & pl.col(target).is_finite()).sum().alias(f'{year}_{target}')
                   for year, cutoff in cutoffs.items() for target in ('y_rank', 'y_ret_1d')]
    counts = lazy.filter(pl.col('is_train') & pl.col('price_valid')).select(expressions).collect().row(0, named=True)
    features = read(ROOT / 'data/feature_manifest.json')['features']
    schema = lazy.collect_schema()
    assert len(features) == 63
    assert all(schema[n] in (pl.Float32, pl.Float64) for n in features)
    arrow_per_row = sum(4 if schema[n] == pl.Float32 else 8 for n in features)
    sample_measurements=[]
    for order in ('C','F'):
        sample=np.ones((100000,63),dtype=np.float64,order=order)
        preprocessing={'median':[0.]*63,'mean':[0.]*63,'scale':[1.]*63,'clip':10.}
        tracemalloc.start();prepared=prepare(sample,preprocessing)
        current,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
        assert peak>=3*sample.nbytes
        sample_measurements.append({'order':order,'rows':len(sample),'matrix_bytes':sample.nbytes,'actual_extra_numpy_tracemalloc_peak_bytes':peak,'actual_extra_peak_matrix_ratio':peak/sample.nbytes,'raw_input_allocated_before_tracing':True})
        del sample,prepared
    rows = []
    for year in range(2020, 2026):
        for target in ('y_rank', 'y_ret_1d'):
            count = int(counts[f'{year}_{target}'])
            matrix = count * 63 * 8
            # At division/clip evaluation, x, imputed values, the arithmetic
            # argument and its newly allocated result coexist. The caller's
            # Polars training frame has not yet been deleted.
            rows.append({'year': year, 'target': target, 'exclusive_cutoff': cutoffs[year],
                'actual_mature_training_rows': count, 'one_float64_matrix_bytes': matrix,
                'four_simultaneous_numpy_matrix_lower_bound_bytes': 4 * matrix,
                'retained_Polars_numeric_feature_bytes': count * arrow_per_row,
                'prepare_simultaneous_feature_storage_lower_bound_GiB': (4 * matrix + count * arrow_per_row) / 2**30,
                'excludes_validation_matrix_keys_targets_other_processes_and_native_model_memory': True})
    for path, digest in pins.items():
        assert sha(path) == digest, path
    report = {'status': 'passed_actual_mature_row_counts_and_source_derived_preprocessing_memory_lower_bounds',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins, 'windows': rows,
        'provided_feature_count': 63, 'numeric_Polars_bytes_per_row': arrow_per_row, 'actual_small_allocation_measurements':sample_measurements, 'numpy_version':np.__version__,
        'actual_available_RAM_GiB_at_observation': psutil.virtual_memory().available / 2**30,
        'HGB_declared_available_RAM_threshold_GiB': 12,
        'estimated_allocation_bound_not_an_observed_peak_or_OOM': True,
        'configuration_specific_not_global_resource_exhaustion': True,
        'source_expression': 'values = np.clip((values - mean) / scale, -clip, clip); x and caller tf are still retained',
        'new_native_fits': 0, 'new_official_scores': 0, 'test_labels_read': False}
    create(out / 'verification.json', report)
    print({'status': report['status'], 'largest_prepare_feature_storage_lower_bound_GiB': max(r['prepare_simultaneous_feature_storage_lower_bound_GiB'] for r in rows),
           'largest_actual_training_rows': max(r['actual_mature_training_rows'] for r in rows)}, flush=True)


if __name__ == '__main__':
    main()
