"""Six original largest-window GOSS fits and actual complete future inference controls."""
from pathlib import Path
from datetime import datetime
import gc
import importlib.util
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
OUT = A / 'gradient_sampling_memmap_capacity_20261006'
from handoff_distribution_views_progress_monitor_20261006 import read, sha, create
from locked_read_hash_cache_20261004 import LockedReadHashCache


def main():
    import numpy as np
    import polars as pl
    import psutil
    import joblib
    import lightgbm as lgb
    import gradient_sampling_exact_memmap_20261006 as core
    from owned_scheduler_native_fit_hold_20261006 import FitHold
    from run_dependency_queue_v3_20261006 import owned
    from linear_leaf_actual_resource_sampler_20261005 import ResourceSampler
    from verify_linear_leaf_bank_20261005 import manual_native_prediction
    assert not OUT.exists()
    run = read(Path(sys.argv[1]).resolve())
    assert run['expected_full_final_fits'] == 6 and run['actual_bank_annual_fits'] == 0
    control = read(A / 'gradient_sampling_exact_memmap_preflight_20261006/verification.json')
    assert control['status'] == 'passed_all6_native_GOSS_parameters_and_full_original_preprocessing_and_full2020_equivalence'
    preparation = read(A / 'mature_training_memmap_controls_20261006/full2025_preparation.json')
    artifact, clean = preparation['artifact'], preparation['standardization']
    assert artifact['shape'] == [6754006, 63]
    bindings = run['input_sha256']
    for path, digest in bindings.items():
        assert sha(path) == digest, path
    OUT.mkdir()
    create(OUT / 'protocol.json', {'status': 'frozen_before6_actual_full6754006_row300_round_GOSS_fits',
        'at_local': datetime.now().isoformat(timespec='seconds'), 'input_sha256': bindings,
        'configurations': core.CONFIGS, 'actual_full_training_rows_each': 6754006,
        'expected_actual_full_final_fits': 6, 'actual_native_iterations_each': 300,
        'minimum_available_host_bytes_before_each_fit': 12 * 1024**3,
        '12GiB_is_new_conservative_capacity_admission_policy_not_a_physical_boundary': True,
        'original_model_configuration_reserve14GiB_field_preserved_as_legacy_scheduling_metadata': True,
        'same_original_full_mature_matrix_targets_and_preprocessing': True,
        'briefly_hold_only_exact_dependency_dispatch_during_native_fit_with_emergency_resume_guard': True,
        'no_current_quality_worker_or_GPU_fit_suspended': True,
        'all30_annual_and_original262_quality_records_still_required': True,
        'future_X_loaded_only_after_each_complete_native_fit': True,
        'model_configs_fixed_before_future_only_native_inference_controls': True,
        'future_controls_do_not_select_or_submit_a_complete_scheme': True,
        'new_quality_scores': 0, 'test_labels_read': False, 'global_resource_boundary_established': False})
    resource = ResourceSampler(OUT)
    resource.start()
    failure = None
    completed = []
    mean, scale = np.asarray(preparation['mean'], dtype=np.float64), np.asarray(preparation['scale'], dtype=np.float64)
    try:
        with LockedReadHashCache(bindings):
            for name, cfg in core.CONFIGS.items():
                while psutil.virtual_memory().available < 12 * 1024**3:
                    resource.context = {'stage': 'waiting_actual12GiB_conservative_capacity_admission', 'model': name}
                    print(json.dumps({'stage': resource.context['stage'], 'model': name,
                        'actual_available_GiB': psutil.virtual_memory().available / 1024**3}), flush=True)
                    time.sleep(10)
                controller = read(A / 'service_owned_workflows_20261006/dependency_queue_v5/native_launch.json')
                assert owned(controller)
                resource.context = {'stage': 'actual_full6754006_row300_round_GOSS_native_fit', 'model': name}
                with FitHold(OUT, controller, name):
                    started = time.monotonic()
                    bundle = core.fit_preprocessed(artifact, cfg, mean, scale, clean)
                    seconds = time.monotonic() - started
                assert owned(controller)
                folder = OUT / name
                folder.mkdir()
                model = folder / 'model_2025.joblib'
                joblib.dump(bundle, model, compress=3)
                metadata = dict(artifact['training_meta_without_target'],
                    training_target_sha256=artifact['targets'][cfg['target']]['sha256'])
                original = read(A / f"linear_bank_20261003/{'rank_ridge_l01' if cfg['target'] == 'y_rank' else 'return_ridge_l01'}/info_2025.json")['training_meta']
                assert metadata == original
                create(folder / 'info_2025.json', {'status': 'passed_actual_full_native_fit', 'model': name, 'year': 2025,
                    'configuration': cfg, 'training_meta': metadata, 'model_sha256': sha(model),
                    'actual_native_iterations': 300, 'native_parameters': bundle['native_training_parameters'],
                    'native_model_string_sha256': __import__('hashlib').sha256(bundle['model_string'].encode('utf-8')).hexdigest(),
                    'fit_seconds': seconds, 'new_model_fits': 1, 'actual_bank_annual_fits': 0,
                    'source_protocol_sha256': sha(OUT / 'protocol.json'), 'new_quality_scores': 0, 'test_labels_read': False})
                print(json.dumps({'stage': 'passed_actual_largest_full_native_fit', 'model': name, 'fit_seconds': seconds}), flush=True)
                resource.context = {'stage': 'actual_complete1599600_row_GOSS_native_future_controls', 'model': name}
                codec_path = folder / 'independent_native_codec.py'
                codec_path.write_bytes((A / 'independent_gradient_sampling_native_codec_20261006.py').read_bytes())
                spec = importlib.util.spec_from_file_location('independent_' + name, codec_path)
                codec = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(codec)
                features = core.engine.feature_names()
                frame = pl.scan_parquet(core.engine.FEATURE_FILE).filter(~pl.col('is_train')).select(
                    core.engine.KEYS + features + ['price_valid']).sort('trade_date', 'ts_code').collect()
                keys = pl.read_parquet(ROOT / 'deliveries/connected_topk0175_20261003/generation_inputs.parquet',
                    columns=core.engine.KEYS + ['price_valid'])
                assert frame.select(core.engine.KEYS + ['price_valid']).equals(keys)
                assert (len(frame), frame['trade_date'].n_unique(), frame['ts_code'].n_unique()) == (1599600, 344, 4650)
                assert metadata['last_label_end'] <= metadata['cutoff_exclusive'] <= int(frame['trade_date'].min())
                x = core.engine.to_matrix(frame, features)
                prediction = core.predict_arrays(bundle, x)
                assert np.isfinite(prediction).all()
                assert np.array_equal(prediction, core.predict_arrays(joblib.load(model), x))
                assert np.array_equal(prediction, codec.predict(joblib.load(model), x))
                assert np.array_equal(prediction[:372000], codec.predict(joblib.load(model), x[:372000]))
                assert np.array_equal(prediction[:37 * 4650], codec.predict(joblib.load(model), x[:37 * 4650]))
                standardized = core.original.standardize(x[:131], bundle['mean'], bundle['scale'], cfg)
                manual = manual_native_prediction(lgb.Booster(model_str=bundle['model_string']), standardized)
                error = float(np.max(np.abs(manual - prediction[:131])))
                assert error < 1e-10
                raw_array_sha = core.engine.array_hash(prediction)
                prediction[~frame['price_valid'].to_numpy()] = -1e6
                raw_path = folder / 'future_raw.parquet'
                frame.select(core.engine.KEYS).with_columns(pl.Series('pred_raw', prediction)).write_parquet(raw_path)
                check = {'model': name, 'actual_full_training_rows': 6754006, 'actual_native_iterations': 300,
                    'model_sha256': sha(model), 'full_future_raw_array_sha256': raw_array_sha,
                    'future_parquet_sha256': sha(raw_path), 'actual_full_future_shape': [1599600, 344, 4650],
                    'full_saved_reload_independent_codec_and_cold80_37day_predictions_bit_identical': True,
                    'independent_dumped_leaf_sum131_rows_max_abs_error': error,
                    'independent_codec_sha256': sha(codec_path), 'entire_original_training_matrix_target_keys_maturity_matched': True,
                    'complete_scheme_not_selected_or_submitted_by_future_controls': True,
                    'actual_bank_annual_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False}
                create(folder / 'future_verification.json', {'status': 'passed', **check})
                completed.append(check)
                print(json.dumps({'stage': 'passed_actual_largest_native_and_complete_future_GOSS_controls', 'model': name}), flush=True)
                del bundle, frame, keys, x, prediction, standardized, manual, codec
                gc.collect()
            create(OUT / 'verification.json', {'status': 'passed_all6_actual_largest_full_GOSS_native_fits_and_complete_future_controls',
                'at_local': datetime.now().isoformat(timespec='seconds'), 'input_sha256': bindings, 'checks': completed,
                'actual_full_final_fits': 6, 'actual300_iteration_models': 6, 'actual_bank_annual_fits': 0,
                'all30_annual_and_original262_complete_output_quality_records_still_required': True,
                'original_GPU_fit_and_current_official_quality_workers_never_suspended': True,
                'all_temporary_dependency_dispatch_holds_released': True,
                'new_quality_scores': 0, 'physical_global_resource_boundary_established': False, 'test_labels_read': False})
    except BaseException as error:
        failure = f'{type(error).__name__}: {error}'
        create(OUT / 'failure.json', {'status': 'failed_preserved_actual_full_GOSS_capacity_and_future_controls',
            'error': failure, 'actual_completed_models': [row['model'] for row in completed]})
        raise
    finally:
        create(OUT / 'resource_summary.json', {'status': 'passed' if failure is None else 'failed',
            'failure': failure, **resource.finish()})


if __name__ == '__main__':
    main()
