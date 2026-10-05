"""Actual largest full-window native fits; retain all required complete quality work."""
from pathlib import Path
import gc
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
OUT = A / 'quantile_tree_memmap_capacity_20261006'
PREPARATION = A / 'mature_training_memmap_controls_20261006'
SERVICE = A / 'service_owned_workflows_20261006/mature_training_memmap_controls'


def create(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def main():
    import numpy as np
    import polars as pl
    import psutil
    import lightgbm as lgb
    import joblib
    import quantile_tree_candidate_20261006 as core
    import mature_training_memmap_20261006 as mapped
    from run_dependency_queue_v3_20261006 import owned
    from locked_read_hash_cache_20261004 import LockedReadHashCache
    from linear_leaf_actual_resource_sampler_20261005 import ResourceSampler
    from verify_linear_leaf_bank_20261005 import manual_native_prediction
    assert not OUT.exists()
    OUT.mkdir()
    while not (SERVICE / 'service_execution.json').exists():
        assert owned(read(SERVICE / 'native_launch.json'))
        time.sleep(10)
    assert read(SERVICE / 'service_execution.json')['status'] == 'passed'
    while owned(read(SERVICE / 'native_launch.json')):
        time.sleep(.2)
    proof = read(PREPARATION / 'verification.json')
    assert proof['status'] == 'passed_actual_full_matrix_preparation_and_native_equivalence'
    assert proof['actual_full300_round_control_fits'] == 2 and proof['additional_actual48_round_control_fits'] == 8
    prepared = read(PREPARATION / 'full2025_preparation.json')
    assert prepared['status'] == 'passed_full_original_matrix_preprocessing'
    artifact, clean = prepared['artifact'], prepared['standardization']
    assert artifact['shape'] == [6754006, 63]
    engine = core.matched.engine
    paths = [Path(__file__), Path(mapped.__file__), Path(core.__file__), Path(core.matched.__file__),
        PREPARATION / 'verification.json', PREPARATION / 'full2025_preparation.json',
        PREPARATION / 'full2020_native_equivalence.json', PREPARATION / 'all_objective_equivalence_controls.json',
        PREPARATION / 'resource_summary.json', SERVICE / 'service_execution.json',
        Path(artifact['raw_path']), Path(clean['path']), engine.FEATURE_FILE, engine.MANIFEST,
        A / 'verify_linear_leaf_bank_20261005.py', A / 'locked_read_hash_cache_20261004.py',
        A / 'linear_leaf_actual_resource_sampler_20261005.py', A / 'train_diverse_backbones_20261003.py',
        ROOT / 'run.py', ROOT / 'src/features.py', ROOT / '后续选模标准.md',
        ROOT / 'deliveries/connected_topk0175_20261003/generation_inputs.parquet',
        ROOT / 'deliveries/connected_topk0175_20261003/train_test.json']
    paths += [Path(v['path']) for v in artifact['targets'].values()]
    paths += [A / f'linear_bank_20261003/{n}/info_2025.json' for n in ('rank_ridge_l01', 'return_ridge_l01')]
    bindings = {str(p.resolve()): mapped.file_sha(p) for p in dict.fromkeys(paths)}
    assert bindings[artifact['raw_path']] == artifact['training_meta_without_target']['training_matrix_sha256']
    assert bindings[clean['path']] == clean['sha256']
    for target in artifact['targets'].values():
        assert bindings[target['path']] == target['sha256']
    create(OUT / 'protocol.json', {'status': 'frozen_before_actual_four_largest_full300_round_native_fits',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': bindings,
        'configurations': core.CONFIGS, 'actual_final_training_rows_each': 6754006,
        'expected_actual_full_final_fits': 4, 'actual_native_iterations_each': 300,
        'future_X_loaded_only_after_each_actual_native_fit': True,
        'same_full_past_statistics_target_caps_and_native_parameters': True,
        'no_early_stopping_no_subsampling_no_feature_reduction': True,
        'minimum_available_host_bytes_before_each_fit': 6 * 2**30,
        'new_admission_is_resource_control_not_redefinition_of_original14GiB_policy': True,
        'all20_annual_fits_and198_official_scores_still_required': True,
        'original_frozen_sources_and_queues_unchanged': True,
        'no_global_resource_boundary_claim': True, 'new_quality_scores': 0, 'test_labels_read': False})
    resource = ResourceSampler(OUT)
    resource.start()
    failure, checks = None, []
    try:
        with LockedReadHashCache(bindings) as cache:
            mean, scale = np.asarray(prepared['mean'], dtype=np.float64), np.asarray(prepared['scale'], dtype=np.float64)
            for name, cfg in core.CONFIGS.items():
                while psutil.virtual_memory().available < 6 * 2**30:
                    resource.context = {'stage': 'waiting_measured_largest_window_control_memory', 'model': name}
                    time.sleep(10)
                resource.context = {'stage': 'actual_full6754006_row300_round_native_fit', 'model': name}
                started = time.monotonic()
                bundle = mapped.fit_preprocessed(core, artifact, cfg, mean, scale, clean)
                fit_seconds = time.monotonic() - started
                assert bundle['requested_and_actual_boosting_iterations'] == 300
                folder = OUT / name
                folder.mkdir()
                model = folder / 'model_2025.joblib'
                joblib.dump(bundle, model, compress=3)
                metadata = dict(artifact['training_meta_without_target'], training_target_sha256=artifact['targets'][cfg['target']]['sha256'])
                expected = read(A / f"linear_bank_20261003/{'rank_ridge_l01' if cfg['target'] == 'y_rank' else 'return_ridge_l01'}/info_2025.json")['training_meta']
                assert metadata == expected
                create(folder / 'info_2025.json', {'status': 'passed_actual_full_native_fit', 'model': name, 'year': 2025,
                    'configuration': cfg, 'training_meta': metadata, 'model_sha256': mapped.file_sha(model),
                    'actual_native_boosting_iterations': 300, 'native_objective': 'quantile',
                    'native_alpha': cfg['alpha'], 'fit_seconds': fit_seconds, 'new_model_fits': 1,
                    'leaf_summary': bundle['leaf_summary'], 'source_protocol_sha256': mapped.file_sha(OUT / 'protocol.json'),
                    'fulltraining_only_test_prediction_not_generated': True,
                    'full24_native_bank_promotion_pending': True, 'new_quality_scores': 0, 'test_labels_read': False})
                resource.context = {'stage': 'actual_full1599600_row_future_native_controls', 'model': name}
                features = engine.feature_names()
                frame = pl.scan_parquet(engine.FEATURE_FILE).filter(~pl.col('is_train')).select(engine.KEYS + features + ['price_valid']).sort('trade_date', 'ts_code').collect()
                expected = pl.read_parquet(ROOT / 'deliveries/connected_topk0175_20261003/generation_inputs.parquet', columns=engine.KEYS + ['price_valid'])
                assert frame.select(engine.KEYS + ['price_valid']).equals(expected)
                assert (len(frame), frame['trade_date'].n_unique(), frame['ts_code'].n_unique()) == (1599600, 344, 4650)
                assert metadata['last_label_end'] <= metadata['cutoff_exclusive'] <= int(frame['trade_date'].min())
                x = engine.to_matrix(frame, features)
                pred = core.predict_arrays(bundle, x)
                assert np.isfinite(pred).all()
                assert np.array_equal(pred, core.predict_arrays(joblib.load(model), x))
                assert np.array_equal(pred[:372000], core.predict_arrays(joblib.load(model), x[:372000]))
                assert np.array_equal(pred[:37 * 4650], core.predict_arrays(bundle, x[:37 * 4650]))
                z = core.matched.standardize(x[:131], bundle['mean'], bundle['scale'], cfg)
                manual = manual_native_prediction(lgb.Booster(model_str=bundle['model_string']), z)
                error = float(np.max(np.abs(manual - pred[:131])))
                assert error < 1e-10
                raw_sha = engine.array_hash(pred)
                pred[~frame['price_valid'].to_numpy()] = -1e6
                raw = folder / 'future_raw.parquet'
                frame.select(engine.KEYS).with_columns(pl.Series('pred_raw', pred)).write_parquet(raw)
                check = {'model': name, 'actual_full_training_rows': 6754006, 'actual_native_iterations': 300,
                    'model_sha256': mapped.file_sha(model), 'raw_parquet_sha256': mapped.file_sha(raw),
                    'full_raw_prediction_array_sha256': raw_sha, 'actual_full_future_rows': len(frame),
                    'actual_full_reload_cold80_and37day_prefix_bit_identical': True,
                    'independent_dumped_leaf_sum131_rows_max_abs_error': error,
                    'entire_original_full_training_matrix_target_keys_and_maturity_matched': True,
                    'new_quality_scores': 0, 'test_labels_read': False}
                create(folder / 'future_verification.json', {'status': 'passed', **check})
                checks.append(check)
                print(json.dumps({'status': 'passed_actual_largest_native_and_full_future', 'model': name, 'fit_seconds': fit_seconds}), flush=True)
                del bundle, frame, expected, x, pred, z, manual
                gc.collect()
            cache.reverify()
        create(OUT / 'verification.json', {'status': 'passed_actual_four_largest_full_native_fits_and_complete_future_controls',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'checks': checks, 'input_sha256': bindings,
            'actual_full_final_fits': 4, 'actual300_iteration_models': 4,
            'actual_annual_fits': 0, 'all20_annual_fits_and198_complete_official_scores_still_pending': True,
            'original_queues_and_sources_unchanged': True, 'new_quality_scores': 0,
            'physical_global_resource_boundary_established': False, 'test_labels_read': False})
    except BaseException as error:
        failure = f'{type(error).__name__}: {error}'
        create(OUT / 'failure.json', {'status': 'failed_preserved_actual_largest_fit_controls', 'error': failure})
        raise
    finally:
        create(OUT / 'resource_summary.json', {'status': 'passed' if failure is None else 'failed',
            'failure': failure, **resource.finish()})


if __name__ == '__main__':
    main()
