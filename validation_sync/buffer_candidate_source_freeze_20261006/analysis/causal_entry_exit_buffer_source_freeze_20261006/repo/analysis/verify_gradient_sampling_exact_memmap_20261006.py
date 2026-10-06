"""Verify full original preprocessing plus all six native parameter sets and paired full2020 GOSS fits."""
from pathlib import Path
from datetime import datetime
import gc
import hashlib
import io
import json
import os
import sys
import time

for variable in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'POLARS_MAX_THREADS'):
    os.environ[variable] = '8'
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
OUT = A / 'gradient_sampling_exact_memmap_preflight_20261006'
SCRATCH = ROOT / 'tmp/gradient_sampling_exact_memmap_preflight_20261006'
from handoff_distribution_views_progress_monitor_20261006 import read, sha, create
from locked_read_hash_cache_20261004 import LockedReadHashCache


def bits(left, right):
    import numpy as np
    assert left.dtype == right.dtype == np.dtype('float64') and left.shape == right.shape
    assert np.array_equal(left.view(np.uint64), right.view(np.uint64))


def main():
    import numpy as np
    import polars as pl
    import psutil
    import joblib
    import gradient_sampling_exact_memmap_20261006 as core
    from linear_leaf_actual_resource_sampler_20261005 import ResourceSampler
    assert not OUT.exists() and not SCRATCH.exists()
    assert psutil.virtual_memory().available >= 6 * 1024**3
    preparation = A / 'mature_training_memmap_controls_20261006'
    full2025 = read(preparation / 'full2025_preparation.json')
    full2020 = read(preparation / 'full2020_native_equivalence.json')
    assert full2025['status'] == 'passed_full_original_matrix_preprocessing'
    assert full2020['status'] == 'passed'
    assert full2025['artifact']['shape'] == [6754006, 63]
    assert full2020['artifact']['shape'] == [1694259, 63]
    paths = [Path(__file__).resolve(), Path(core.__file__).resolve(), Path(core.original.__file__).resolve(),
        Path(core.mapped.__file__).resolve(), preparation / 'full2025_preparation.json',
        preparation / 'full2020_native_equivalence.json', preparation / 'verification.json',
        A / 'gradient_sampling_preflight_20261005/verification.json',
        A / 'gradient_sampling_complete_search_plan_20261005.json',
        A / 'linear_leaf_actual_resource_sampler_20261005.py', A / 'locked_read_hash_cache_20261004.py',
        core.engine.FEATURE_FILE, core.engine.MANIFEST, A / 'train_diverse_backbones_20261003.py',
        ROOT / 'run.py', ROOT / 'src/features.py', ROOT / '后续选模标准.md']
    for record in (full2025, full2020):
        artifact, standardized = record['artifact'], record['standardization']
        paths += [Path(artifact['raw_path']), Path(standardized['path']),
                  *[Path(v['path']) for v in artifact['targets'].values()]]
    bindings = {str(path.resolve()): sha(path) for path in dict.fromkeys(paths)}
    for record in (full2025, full2020):
        artifact, standardized = record['artifact'], record['standardization']
        assert bindings[artifact['raw_path']] == artifact['training_meta_without_target']['training_matrix_sha256']
        assert bindings[standardized['path']] == standardized['sha256']
        for target in artifact['targets'].values():
            assert bindings[target['path']] == target['sha256']
    OUT.mkdir()
    SCRATCH.mkdir()
    create(OUT / 'frozen_before_actual_GOSS_memmap_controls.json', {
        'at_local': datetime.now().isoformat(timespec='seconds'), 'input_sha256': bindings,
        'configurations': core.CONFIGS, 'actual_full2025_preprocessing_rows': 6754006,
        'all6_paired300_round_pilot_rows': 32768, 'paired_full2020_rows': 1694259,
        'all63_features_and_original300_round_native_parameters_preserved': True,
        'shared_existing_buffers_reused_without_deleting_or_rewriting_any_original_cache': True,
        'expected_small_native_control_fits': 12, 'expected_full2020_native_control_fits': 2,
        'actual_bank_annual_fits': 0, 'actual_full_final_fits': 0, 'new_quality_scores': 0,
        'all30_annual_and6_final_GOSS_fits_and_original262_quality_records_still_required': True,
        'test_labels_read': False})
    sampler = ResourceSampler(OUT)
    sampler.start()
    failure = None
    controls = []
    try:
        with LockedReadHashCache(bindings):
            largest = full2025['artifact']
            raw = np.memmap(largest['raw_path'], mode='r', dtype=np.float32, shape=tuple(largest['shape']))
            sampler.context = {'stage': 'actual_original_GOSS_full6754006_row_preprocessing_bits'}
            started = time.monotonic()
            mean, scale = core.original.preprocessing(raw)
            bits(mean, np.asarray(full2025['mean'], dtype=np.float64))
            bits(scale, np.asarray(full2025['scale'], dtype=np.float64))
            digest = hashlib.sha256()
            cfg = next(iter(core.CONFIGS.values()))
            for offset in range(0, len(raw), cfg['chunk_rows']):
                block = core.original.standardize(raw[offset:offset + cfg['chunk_rows']], mean, scale, cfg)
                digest.update(memoryview(block).cast('B'))
            assert digest.hexdigest() == full2025['standardization']['sha256']
            create(OUT / 'full2025_original_GOSS_preprocessing.json', {
                'status': 'passed', 'rows': len(raw), 'features': 63,
                'full_original_GOSS_mean_std_float64_bits_and_all_standardized_bytes_match': True,
                'standardized_sha256': digest.hexdigest(), 'seconds': time.monotonic() - started,
                'actual_native_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})
            pilot_x = np.array(raw[:32768], copy=True)
            raw._mmap.close()
            del raw, block
            gc.collect()
            pilot_mean, pilot_scale = core.original.preprocessing(pilot_x)
            for name, config in core.CONFIGS.items():
                sampler.context = {'stage': 'paired32768_row300_round_GOSS_parameter_control', 'model': name}
                target = largest['targets'][config['target']]
                labels = np.memmap(target['path'], mode='r', dtype=target['dtype'], shape=(largest['shape'][0],))
                pilot_y = np.array(labels[:32768], copy=True)
                labels._mmap.close()
                clean = core.original.standardize(pilot_x, pilot_mean, pilot_scale, config)
                path = SCRATCH / (name + '_control.bin')
                clean.tofile(path)
                reference = core.original.fit_arrays(pilot_x, pilot_y, config)
                actual = core.fit_preprocessed(dict(largest, shape=[32768, 63]), config,
                    pilot_mean, pilot_scale, {'path': str(path)})
                assert actual['model_string'] == reference['model_string']
                assert actual['native_training_parameters'] == reference['native_training_parameters']
                assert actual['target_bounds'] == reference['target_bounds']
                bits(actual['mean'], reference['mean'])
                bits(actual['scale'], reference['scale'])
                bits(core.predict_arrays(actual, pilot_x), core.original.predict_arrays(reference, pilot_x))
                controls.append({'model': name, 'rows': 32768, 'actual_native_iterations_each': 300,
                    'paired_native_control_fits': 2, 'entire_original_native_model_string_bit_identical': True,
                    'native_parameters_target_caps_preprocessing_and_predictions_bit_identical': True,
                    'control_clean_file_sha256': sha(path),
                    'native_model_string_sha256': hashlib.sha256(actual['model_string'].encode('utf-8')).hexdigest()})
                create(OUT / (name + '_paired_control.json'), controls[-1])
                print(json.dumps(controls[-1]), flush=True)
                del reference, actual, labels, clean, pilot_y
                gc.collect()
            del pilot_x
            gc.collect()
            past = full2020['artifact']
            cfg = core.CONFIGS['rank_goss_medium_r300']
            sampler.context = {'stage': 'actual_original_full1694259_row300_round_GOSS_reference_fit'}
            raw = np.memmap(past['raw_path'], mode='r', dtype=np.float32, shape=tuple(past['shape']))
            yinfo = past['targets']['y_rank']
            labels = np.memmap(yinfo['path'], mode='r', dtype=yinfo['dtype'], shape=(len(raw),))
            reference = core.original.fit_arrays(np.array(raw, copy=True), np.array(labels, copy=True), cfg)
            raw._mmap.close()
            labels._mmap.close()
            del raw, labels
            gc.collect()
            sampler.context = {'stage': 'actual_original_full1694259_row300_round_GOSS_memmap_fit'}
            actual = core.fit_preprocessed(past, cfg, reference['mean'], reference['scale'], full2020['standardization'])
            assert actual['model_string'] == reference['model_string']
            assert actual['native_training_parameters'] == reference['native_training_parameters']
            frame = pl.scan_parquet(core.engine.FEATURE_FILE).filter(pl.col('is_train') &
                (pl.col('trade_date') // 10000 == 2020)).select(core.engine.KEYS + core.engine.feature_names()).sort('trade_date', 'ts_code').collect()
            canonical = pl.read_parquet(A / 'connected_validation_20261002/combined_fold_frame.parquet', columns=core.engine.KEYS).filter(pl.col('trade_date') // 10000 == 2020)
            assert frame.select(core.engine.KEYS).equals(canonical)
            x = core.engine.to_matrix(frame, core.engine.feature_names())
            first, second = core.original.predict_arrays(reference, x), core.predict_arrays(actual, x)
            bits(first, second)
            buffer = io.BytesIO()
            joblib.dump(actual, buffer, compress=3)
            buffer.seek(0)
            bits(second, core.predict_arrays(joblib.load(buffer), x))
            dates = frame['trade_date'].to_numpy()
            n80 = int(np.searchsorted(dates, np.unique(dates)[79], side='right'))
            assert n80 == 372000
            bits(second[:n80], core.predict_arrays(actual, x[:n80]))
            create(OUT / 'full2020_original_GOSS_native_equivalence.json', {
                'status': 'passed', 'actual_full_training_rows_each': 1694259,
                'actual_full300_round_control_fits': 2, 'model': 'rank_goss_medium_r300',
                'original_native_model_string_parameters_and_preprocessing_bit_identical': True,
                'entire_original2020_validation_predictions_reload_and_cold80_bits_identical': True,
                'actual_full2020_validation_rows': len(frame), 'actual_cold80_rows': n80,
                'native_model_string_sha256': hashlib.sha256(actual['model_string'].encode('utf-8')).hexdigest(),
                'full2020_raw_array_sha256': core.engine.array_hash(second),
                'control_model_files_written': 0, 'actual_bank_annual_fits': 0,
                'actual_full_final_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})
        create(OUT / 'verification.json', {
            'status': 'passed_all6_native_GOSS_parameters_and_full_original_preprocessing_and_full2020_equivalence',
            'at_local': datetime.now().isoformat(timespec='seconds'), 'input_sha256': bindings,
            'paired_small_controls': controls, 'actual_pilot_native_fits': 12,
            'actual_full2020_native_control_fits': 2, 'control_weights_written': 0,
            'actual_full2025_GOSS_native_fit_not_performed': True,
            'actual_bank_annual_fits': 0, 'actual_full_final_fits': 0, 'new_quality_scores': 0,
            'all30_annual_and6_final_and_original262_quality_records_still_required': True,
            'physical_resource_boundary_established': False, 'test_labels_read': False})
        print('passed_all6_native_GOSS_parameters_and_full_original_preprocessing_and_full2020_equivalence', flush=True)
    except BaseException as error:
        failure = f'{type(error).__name__}: {error}'
        create(OUT / 'failure.json', {'status': 'failed_preserved_actual_GOSS_memmap_controls', 'error': failure})
        raise
    finally:
        create(OUT / 'resource_summary.json', {'status': 'passed' if failure is None else 'failed',
            'failure': failure, **sampler.finish()})


if __name__ == '__main__':
    main()
