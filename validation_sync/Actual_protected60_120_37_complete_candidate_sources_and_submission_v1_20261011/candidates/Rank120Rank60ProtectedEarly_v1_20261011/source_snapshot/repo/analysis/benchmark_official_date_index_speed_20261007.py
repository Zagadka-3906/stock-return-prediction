"""Actual full continuous official evaluator equivalence and local elapsed-time benchmark."""
from pathlib import Path
import gc
import json
import os
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'POLARS_MAX_THREADS'):
    os.environ[key] = '2'


def main():
    import numpy as np
    import pandas as pd
    import evaluate
    from run_dependency_queue_v3_20261006 import read, create, sha
    from official_date_index_dataframe_adapter_20261007 import installed, IndexedFrame
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    OUT = A / 'official_date_index_speed_benchmark_20261007'
    assert not OUT.exists()
    OUT.mkdir()
    source = A / 'direct_flag_rank92_official_comparison_20261007/scoring_validation_only'
    original = source / 'submission.csv'
    case = read(source.parent / 'case91_official.json')
    capsule = read(Path(case['official_score_cache']['official_metrics_source']))
    assert sha(original) == capsule['scope']['submission_csv_sha256']
    pins = {str(p): sha(p) for p in [Path(__file__), A / 'official_date_index_dataframe_adapter_20261007.py', ROOT / 'evaluate.py', original, source / '测试集_X.csv', source / '测试集_Y.csv', Path(case['official_score_cache']['official_metrics_source'])]}
    create(OUT / 'frozen_before_actual_benchmark.json', {'input_sha256': pins,
        'all_metrics_must_match_float64_bits': True, 'full_rows_days_stocks': [5635800, 1212, 4650],
        'tests': ['actual_case91_return_mapped_CSV', 'deterministic_tied_return_predictions', 'cold80_prefix'],
        'new_native_fits': 0, 'new_model_selection_scores': 0, 'test_labels_read': False})
    records = []
    with LockedReadHashCache(pins) as scope:
        # All date positions are independently checked against original pandas masks in row order.
        dates = pd.read_csv(original, usecols=['trade_date'])
        events = {'date_index_lookups': 0}
        indexed = IndexedFrame(dates, events)
        for day in sorted(dates.trade_date.unique()):
            actual = indexed[indexed['trade_date'] == day]
            expected = dates[dates['trade_date'] == day]
            assert actual.equals(expected)
        assert events['date_index_lookups'] == 1212
        del dates, indexed
        gc.collect()
        folder = OUT / 'scoring_validation_only'
        folder.mkdir()
        for filename in ('测试集_X.csv', '测试集_Y.csv'):
            os.link(source / filename, folder / filename)
        frame = pd.read_csv(original)
        assert len(frame) == 5635800 and frame.trade_date.nunique() == 1212
        tied = folder / 'tied_submission.csv'
        frame['pred'] = np.round(frame['pred'].to_numpy(), 3)
        frame.to_csv(tied, index=False, float_format='%.17g')
        cold = folder / 'cold80_submission.csv'
        last = sorted(frame.trade_date.unique())[79]
        frame.loc[frame.trade_date <= last].to_csv(cold, index=False, float_format='%.17g')
        del frame
        gc.collect()
        for name, path, full in [('actual_case91', original, True), ('tied_predictions', tied, True), ('cold80', cold, False)]:
            for repetition in range(2 if full else 1):
                # Alternate order; include normal CSV reads, merges and index construction in timings.
                modes = ['original', 'indexed'] if repetition == 0 else ['indexed', 'original']
                measurements = {}
                for mode in modes:
                    gc.collect()
                    start = time.perf_counter()
                    if mode == 'indexed':
                        with installed(path) as observed:
                            metrics = evaluate.evaluate(str(path), str(folder))
                        assert observed['date_index_lookups'] == (1212 if full else 80)
                    else:
                        metrics = evaluate.evaluate(str(path), str(folder))
                    elapsed = time.perf_counter() - start
                    measurements[mode] = {'elapsed_seconds': elapsed, 'metrics': {k: float(v) for k, v in metrics.items()}}
                assert list(measurements['original']['metrics']) == list(measurements['indexed']['metrics'])
                for key in measurements['original']['metrics']:
                    assert np.float64(measurements['original']['metrics'][key]).view(np.uint64) == np.float64(measurements['indexed']['metrics'][key]).view(np.uint64), (name, key)
                if name == 'actual_case91':
                    assert measurements['original']['metrics'] == case['metrics']
                item = {'name': name, 'repetition': repetition, 'measurements': measurements, 'all8_metric_bits_identical': True}
                records.append(item)
                create(OUT / f'{name}_{repetition}.json', item)
                print(json.dumps(item), flush=True)
        scope.reverify()
    ratios = [r['measurements']['original']['elapsed_seconds'] / r['measurements']['indexed']['elapsed_seconds'] for r in records if r['name'] != 'cold80']
    create(OUT / 'verification.json', {'status': 'passed_actual_full_official_date_index_equivalence_and_benchmark',
        'input_sha256': pins, 'records': records, 'median_full_official_evaluation_speedup': float(np.median(ratios)),
        'all1212_date_index_row_orders_exact_original_masks': True, 'all8_metrics_bit_identical_each_actual_comparison': True,
        'unchanged_official_evaluate_source_sha256': pins[str(ROOT / 'evaluate.py')],
        'cold80_independent_official_comparison_passed': True, 'new_native_fits': 0, 'new_model_selection_scores': 0,
        'test_labels_read': False, 'whole_pipeline_speedup_not_measured': True})


if __name__ == '__main__':
    main()
