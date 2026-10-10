"""Measure full largest-window preparation and paired full2020 native fits."""
from pathlib import Path
import gc
import hashlib
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
OUT = A / 'mature_training_memmap_controls_20261006'
SCRATCH = ROOT / 'tmp/mature_training_memmap_controls_20261006'


def create(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    import numpy as np
    import polars as pl
    import psutil
    import quantile_tree_candidate_20261006 as core
    import mature_training_memmap_20261006 as mapped
    from locked_read_hash_cache_20261004 import LockedReadHashCache
    from linear_leaf_actual_resource_sampler_20261005 import ResourceSampler
    assert not OUT.exists()
    OUT.mkdir()
    engine = core.matched.engine
    paths = [Path(__file__), Path(mapped.__file__), Path(core.__file__), Path(core.matched.__file__),
        A / 'train_diverse_backbones_20261003.py', A / 'locked_read_hash_cache_20261004.py',
        A / 'linear_leaf_actual_resource_sampler_20261005.py', engine.FEATURE_FILE, engine.MANIFEST,
        ROOT / 'run.py', ROOT / 'src/features.py', ROOT / '后续选模标准.md']
    paths += [A / f'linear_bank_20261003/{name}/info_{year}.json'
        for name in ('rank_ridge_l01', 'return_ridge_l01') for year in (2020, 2025)]
    bindings = {str(p.resolve()): mapped.file_sha(p) for p in paths}
    create(OUT / 'frozen_before_actual_controls.json', {'input_sha256': bindings,
        'full_original_windows': [2025, 2020], 'full_original_2025_rows': 6754006,
        'paired_full2020_native300_round_rank_median_fits': 2,
        'all_four_objectives_additional_pair_controls_rows': 65536,
        'all_four_objectives_additional_pair_controls_iterations': 48,
        'complete_native24_fits_and198_official_scores_still_required': True,
        'minimum_available_bytes_before_controls': 6 * 2**30,
        'physical_boundary_established': False, 'test_labels_read': False})
    resource = ResourceSampler(OUT)
    resource.start()
    failure, checks = None, []
    try:
        while psutil.virtual_memory().available < 6 * 2**30:
            time.sleep(10)
        with LockedReadHashCache(bindings) as cache:
            cfg = core.CONFIGS['rank_lgb_quantile_a050_r300']
            largest = mapped.build(engine, 2025, SCRATCH / '2025', resource)
            mean, scale, clean = mapped.standardize(core, largest, cfg, Path(largest['folder']) / 'standardized_float32.bin', resource)
            create(OUT / 'full2025_preparation.json', {'status': 'passed_full_original_matrix_preprocessing',
                'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'artifact': largest,
                'standardization': clean, 'mean': mean.tolist(), 'scale': scale.tolist(),
                'new_model_fits': 0, 'new_quality_scores': 0, 'physical_boundary_established': False})
            # Four native objective comparisons use the same full-window statistics;
            # the paired48-round controls are explicitly excluded from annual counts.
            for name, full_cfg in core.CONFIGS.items():
                pilot = dict(full_cfg, num_boost_round=48)
                raw = np.memmap(largest['raw_path'], mode='r', dtype=np.float32, shape=tuple(largest['shape']))
                tiny_path = SCRATCH / ('control_' + name + '.bin')
                core.matched.standardize(raw[:65536], mean, scale, pilot).tofile(tiny_path)
                target = largest['targets'][pilot['target']]
                y = np.memmap(target['path'], mode='r', dtype=target['dtype'], shape=(largest['shape'][0],))
                # Reference is a normal C-contiguous array, independently fit by
                # the original Dataset/train/target-cap algebra, with same statistics.
                import lightgbm as lgb
                normal = core.matched.standardize(raw[:65536], mean, scale, pilot)
                labels = np.asarray(y[:65536], dtype=np.float64)
                if pilot['target'] == 'y_ret_1d':
                    bounds = [float(v) for v in np.quantile(labels, pilot['return_quantiles'])]
                    labels = np.clip(labels, *bounds)
                params = core.parameters(pilot)
                reference = lgb.train(params, lgb.Dataset(normal, label=labels, params=params, free_raw_data=True), num_boost_round=48)
                tiny = dict(largest, shape=[65536, largest['shape'][1]])
                actual = mapped.fit_preprocessed(core, tiny, pilot, mean, scale, {'path': str(tiny_path)})
                assert reference.model_to_string() == actual['model_string']
                assert reference.current_iteration() == actual['requested_and_actual_boosting_iterations'] == 48
                checks.append({'model': name, 'rows': 65536, 'native_iterations': 48,
                    'entire_native_model_string_bit_identical': True, 'actual_control_fits': 2,
                    'actual_annual_fits': 0, 'new_quality_scores': 0})
                raw._mmap.close()
                y._mmap.close()
                del reference, actual, normal, labels, raw, y
                gc.collect()
            create(OUT / 'all_objective_equivalence_controls.json', {'status': 'passed', 'checks': checks,
                'actual_control_fits': 8, 'actual_annual_fits': 0, 'new_quality_scores': 0})
            past = mapped.build(engine, 2020, SCRATCH / '2020', resource)
            mean, scale, clean = mapped.standardize(core, past, cfg, Path(past['folder']) / 'standardized_float32.bin', resource)
            resource.context = {'stage': 'actual_original_full2020_reference300_round_native_fit', 'rows': past['shape'][0]}
            raw = np.memmap(past['raw_path'], mode='r', dtype=np.float32, shape=tuple(past['shape']))
            target = past['targets']['y_rank']
            y = np.memmap(target['path'], mode='r', dtype=target['dtype'], shape=(len(raw),))
            reference = core.fit_arrays(np.array(raw, copy=True), np.array(y, copy=True), cfg)
            raw._mmap.close()
            y._mmap.close()
            del raw, y
            gc.collect()
            resource.context = {'stage': 'actual_original_full2020_memmap300_round_native_fit', 'rows': past['shape'][0]}
            actual = mapped.fit_preprocessed(core, past, cfg, mean, scale, clean)
            assert reference['model_string'] == actual['model_string']
            assert np.array_equal(reference['mean'], actual['mean']) and np.array_equal(reference['scale'], actual['scale'])
            assert reference['native_training_parameters'] == actual['native_training_parameters']
            features = engine.feature_names()
            valid = pl.scan_parquet(engine.FEATURE_FILE).filter(pl.col('is_train') & (pl.col('trade_date') // 10000 == 2020)).select(engine.KEYS + features).sort('trade_date', 'ts_code').collect()
            vx = engine.to_matrix(valid, features)
            first, second = core.predict_arrays(reference, vx), core.predict_arrays(actual, vx)
            assert np.array_equal(first, second) and np.isfinite(first).all()
            import joblib
            model_path = OUT / 'full2020_memmap_reload_control.joblib'
            joblib.dump(actual, model_path, compress=3)
            assert np.array_equal(second, core.predict_arrays(joblib.load(model_path), vx))
            dates = valid['trade_date'].to_numpy()
            n80 = int(np.searchsorted(dates, np.unique(dates)[79], side='right'))
            assert n80 == 372000 and np.array_equal(second[:n80], core.predict_arrays(actual, vx[:n80]))
            create(OUT / 'full2020_native_equivalence.json', {'status': 'passed', 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
                'artifact': past, 'standardization': clean, 'actual_full300_round_control_fits': 2,
                'native_model_string_sha256': hashlib.sha256(actual['model_string'].encode('utf-8')).hexdigest(),
                'original_native_model_string_parameters_and_preprocessing_bit_identical': True,
                'full_original2020_prediction_rows': len(vx), 'full_original2020_raw_array_sha256': engine.array_hash(second),
                'full_original2020_native_reload_bit_identical': True, 'actual_cold80_rows': n80,
                'cold80_prefix_bit_identical': True, 'model_path': str(model_path), 'model_file_sha256': mapped.file_sha(model_path),
                'actual_qualified_bank_annual_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})
            cache.reverify()
        create(OUT / 'verification.json', {'status': 'passed_actual_full_matrix_preparation_and_native_equivalence',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'source_sha256': bindings,
            'actual_largest_window_original_rows': 6754006, 'actual_full300_round_control_fits': 2,
            'additional_actual48_round_control_fits': 8, 'actual_qualified_bank_annual_fits': 0,
            'full2025_native_fit_not_tested': True, 'new_quality_scores': 0,
            'complete_native24_fits_and198_official_scores_still_pending': True,
            'physical_resource_boundary_established': False, 'test_labels_read': False})
    except BaseException as error:
        failure = f'{type(error).__name__}: {error}'
        create(OUT / 'failure.json', {'status': 'failed_preserved_actual_controls', 'error': failure})
        raise
    finally:
        create(OUT / 'resource_summary.json', {'status': 'passed' if failure is None else 'failed',
            'failure': failure, **resource.finish()})


if __name__ == '__main__':
    main()
