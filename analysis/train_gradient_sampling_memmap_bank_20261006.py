"""Complete all30 original GOSS annual fits using fully verified existing buffers."""
from pathlib import Path
import gc
import hashlib
import json
import shutil
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
import gradient_sampling_exact_memmap_20261006 as core
import mature_training_memmap_20261006 as mapped
import independent_gradient_sampling_native_codec_20261006 as codec
from handoff_distribution_views_progress_monitor_20261006 import read, sha, create

engine, CONFIGS, YEARS = core.engine, core.CONFIGS, tuple(range(2020, 2025))
OUT = A / 'gradient_sampling_memmap_complete_bank_20261006'
CAPACITY = A / 'gradient_sampling_memmap_capacity_20261006'
CACHE_PROOF = A / 'gradient_sampling_all_annual_cache_controls_20261006/verification.json'
RESOURCE = None


def freeze():
    assert not OUT.exists()
    proof = read(CAPACITY / 'verification.json')
    assert proof['status'] == 'passed_all6_actual_largest_full_GOSS_native_fits_and_complete_future_controls'
    assert proof['actual_full_final_fits'] == proof['actual300_iteration_models'] == 6
    assert proof['actual_bank_annual_fits'] == proof['new_quality_scores'] == 0
    assert read(CACHE_PROOF)['status'] == 'passed_all5_full_original_GOSS_annual_preprocessing_targets_and_maturity'
    assert read(A / 'service_owned_workflows_20261006/gradient_sampling_memmap_capacity/service_execution.json')['status'] == 'passed'
    samples = [json.loads(line) for line in (CAPACITY / 'actual_resource_samples.jsonl').read_text(encoding='utf-8').splitlines()]
    fits = [x for x in samples if x['context']['stage'] == 'actual_full6754006_row300_round_GOSS_native_fit']
    assert fits and {x['context']['model'] for x in fits} == set(CONFIGS)
    peak = max(x['target_and_descendant_rss_bytes'] for x in fits)
    reserve = max(6 * 1024**3, peak + 2 * 1024**3)
    paths = [Path(__file__), Path(core.__file__), Path(core.original.__file__), Path(mapped.__file__), Path(codec.__file__),
        A / 'run_gradient_sampling_memmap_full_workflow_20261006.py',
        A / 'verify_gradient_sampling_memmap_full_future_20261006.py',
        A / 'owned_scheduler_native_fit_hold_20261006.py', A / 'watch_owned_scheduler_fit_lease_20261006.py',
        A / 'windows_hidden_process_launch_20261006.py', A / 'run_dependency_queue_v3_20261006.py',
        A / 'verify_linear_leaf_bank_20261005.py', A / 'locked_read_hash_cache_20261004.py',
        A / 'linear_leaf_actual_resource_sampler_20261005.py', A / 'train_diverse_backbones_20261003.py',
        A / 'gradient_sampling_storage_20261005.json', A / 'gradient_sampling_complete_search_plan_20261005.json',
        CAPACITY / 'protocol.json', CAPACITY / 'verification.json', CAPACITY / 'resource_summary.json',
        A / 'service_owned_workflows_20261006/gradient_sampling_memmap_capacity/service_execution.json',
        A / 'gradient_sampling_exact_memmap_preflight_20261006/verification.json', CACHE_PROOF,
        engine.FEATURE_FILE, engine.MANIFEST, ROOT / 'data/raw/训练集.csv',
        ROOT / 'run.py', ROOT / 'src/features.py', ROOT / '后续选模标准.md']
    paths += [Path(p) for p in read(CACHE_PROOF)['input_sha256']]
    paths += list(CAPACITY.glob('*/model_2025.joblib')) + list(CAPACITY.glob('*/info_2025.json'))
    paths += list(CAPACITY.glob('*/future_verification.json')) + list(CAPACITY.glob('*/future_raw.parquet'))
    paths += [A / f'linear_bank_20261003/{n}/info_{year}.json'
              for n in ('rank_ridge_l01', 'return_ridge_l01') for year in (*YEARS, 2025)]
    bindings = {str(p.resolve()): sha(p) for p in dict.fromkeys(paths)}
    OUT.mkdir()
    protocol = {'status': 'frozen_before30_actual_full_mature300_round_annual_GOSS_fits',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': bindings,
        'configurations': CONFIGS, 'years': YEARS, 'features': engine.feature_names(),
        'expected_annual_fits': 30, 'expected_final_fits': 6, 'actual_iterations_each_full_fit': 300,
        'six_actual_native_final_fits_reused_with_complete_provenance': True,
        'copied_model_files_not_counted_as_additional_fits': True,
        'expected_complete_validation_rows': 5635800, 'expected_validation_days': 1212, 'expected_codes': 4650,
        'minimum_available_host_RAM_before_each_fit_bytes': reserve,
        'measured_largest_window_native_peak_bytes': peak,
        'reserve_derived_from_actual_largest_native_fit_and2GiB_margin': True,
        'original14GiB_config_field_is_scheduling_metadata_not_a_native_parameter': True,
        'same_original_mature_rows63_features_targets_order_and_native_GOSS_params': True,
        'entire_shared_five_year_buffers_verified_read_only': True,
        'only_new_dispatch_temporarily_held_during_native_fit_with_emergency_resume_guard': True,
        'no_active_quality_or_GPU_worker_suspended': True,
        'full124_plus138_complete_output_official_quality_still_required': True,
        'no_validation_early_stopping': True, 'selection_bias_uncorrected': True,
        'new_quality_scores': 0, 'test_labels_read': False, 'physical_global_resource_boundary_established': False}
    create(OUT / 'protocol.json', protocol)
    return protocol


def verified_info(name, year):
    import numpy as np
    info = read(OUT / name / f'info_{year}.json')
    path = OUT / name / f'model_{year}.joblib'
    assert info['status'] == 'passed' and info['configuration'] == CONFIGS[name]
    assert sha(path) == info['model_sha256']
    label = 'rank_ridge_l01' if CONFIGS[name]['target'] == 'y_rank' else 'return_ridge_l01'
    assert info['training_meta'] == read(A / f'linear_bank_20261003/{label}/info_{year}.json')['training_meta']
    bundle = engine.load_bundle(path)
    assert bundle['config'] == CONFIGS[name] and bundle['kind'] == 'lightgbm_gradient_sampling'
    assert bundle['native_training_parameters'] == core.original.parameters(CONFIGS[name])
    assert bundle['leaf_summary']['tree_count'] == bundle['requested_and_actual_boosting_iterations'] == 300
    assert '[data_sample_strategy: goss]' in bundle['model_string']
    assert np.isfinite(bundle['mean']).all() and np.isfinite(bundle['scale']).all()
    assert hashlib.sha256(bundle['model_string'].encode('utf-8')).hexdigest() == info['native_model_string_sha256']
    if year < 2025:
        assert sha(OUT / name / f'raw_{year}.parquet') == info['prediction_sha256']
    return info


def promote_final_models():
    for name in CONFIGS:
        source = CAPACITY / name
        assert read(source / 'future_verification.json')['status'] == 'passed'
        info = read(source / 'info_2025.json')
        assert info['status'] == 'passed_actual_full_native_fit'
        assert sha(source / 'model_2025.joblib') == info['model_sha256']
        folder = OUT / name
        folder.mkdir()
        shutil.copyfile(source / 'model_2025.joblib', folder / 'model_2025.joblib')
        info.update(status='passed', actual_native_boosting_iterations=300, native_objective='regression',
            actual_native_fit_reused_from=str(source), actual_fit_origin_info_sha256=sha(source / 'info_2025.json'),
            copied_file_is_not_an_additional_native_fit=True, test_data_read=False,
            fulltraining_only_test_prediction_not_generated=True,
            source_model_already_used_only_for_native_engineering_future_controls=True)
        create(folder / 'info_2025.json', info)
        verified_info(name, 2025)


def train_one(name, year):
    import numpy as np
    import polars as pl
    import psutil
    import lightgbm as lgb
    from owned_scheduler_native_fit_hold_20261006 import FitHold
    from run_dependency_queue_v3_20261006 import owned
    from verify_linear_leaf_bank_20261005 import manual_native_prediction
    assert name in CONFIGS and year in YEARS
    assert not (OUT / name / f'info_{year}.json').exists()
    reserve = read(OUT / 'protocol.json')['minimum_available_host_RAM_before_each_fit_bytes']
    while psutil.virtual_memory().available < reserve:
        if RESOURCE is not None:
            RESOURCE.context = {'stage': 'waiting_measured_GOSS_annual_capacity_admission', 'model': name, 'year': year}
        time.sleep(10)
    value = read(A / f'quantile_tree_memmap_complete_bank_20261006/exact_training_artifact_{year}.json')
    cfg = CONFIGS[name]
    if RESOURCE is not None:
        RESOURCE.context = {'stage': 'actual_full_mature300_round_annual_GOSS_fit',
            'model': name, 'year': year, 'rows': value['artifact']['shape'][0]}
    controller = read(A / 'service_owned_workflows_20261006/dependency_queue_v5/native_launch.json')
    assert owned(controller)
    with FitHold(OUT, controller, f'{name}_{year}'):
        started = time.monotonic()
        bundle = core.fit_preprocessed(value['artifact'], cfg, np.asarray(value['mean'], dtype=np.float64),
            np.asarray(value['scale'], dtype=np.float64), value['standardization'])
        fit_seconds = time.monotonic() - started
    assert owned(controller)
    model = OUT / name / f'model_{year}.joblib'
    engine.save_bundle(model, bundle)
    metadata = dict(value['artifact']['training_meta_without_target'],
                    training_target_sha256=value['artifact']['targets'][cfg['target']]['sha256'])
    features = engine.feature_names()
    if RESOURCE is not None:
        RESOURCE.context = {'stage': 'whole_annual_original_reload_independent_codec_cold80_checks', 'model': name, 'year': year}
    frame = pl.scan_parquet(engine.FEATURE_FILE).filter(pl.col('is_train') & (pl.col('trade_date') // 10000 == year)).select(
        engine.KEYS + features + ['price_valid']).sort('trade_date', 'ts_code').collect()
    x = engine.to_matrix(frame, features)
    raw = core.predict_arrays(bundle, x)
    assert np.isfinite(raw).all()
    assert np.array_equal(raw, core.predict_arrays(engine.load_bundle(model), x))
    assert np.array_equal(raw, codec.predict(engine.load_bundle(model), x))
    assert np.array_equal(raw[:372000], codec.predict(engine.load_bundle(model), x[:372000]))
    assert np.array_equal(raw[:37 * 4650], codec.predict(engine.load_bundle(model), x[:37 * 4650]))
    manual = manual_native_prediction(lgb.Booster(model_str=bundle['model_string']),
        core.original.standardize(x[:131], bundle['mean'], bundle['scale'], cfg))
    error = float(np.max(np.abs(manual - raw[:131])))
    assert error < 1e-10
    raw_array_sha = engine.array_hash(raw)
    raw[~frame['price_valid'].to_numpy()] = -1e6
    prediction = OUT / name / f'raw_{year}.parquet'
    frame.select(engine.KEYS).with_columns(pl.Series('pred_raw', raw)).write_parquet(prediction)
    info = {'status': 'passed', 'model': name, 'year': year, 'configuration': cfg, 'training_meta': metadata,
        'actual_native_boosting_iterations': 300, 'native_objective': 'regression', 'native_data_sample_strategy': 'goss',
        'native_model_string_sha256': hashlib.sha256(bundle['model_string'].encode('utf-8')).hexdigest(),
        'model_sha256': sha(model), 'prediction_sha256': sha(prediction), 'full_raw_array_sha256': raw_array_sha,
        'rows': len(frame), 'fit_seconds': fit_seconds, 'new_model_fits': 1,
        'model_reload_bit_identical': True, 'full_independent_codec_and_cold80_37day_bit_identical': True,
        'independent_leaf_sum131_rows_max_abs_error': error, 'leaf_summary': bundle['leaf_summary'],
        'test_data_read': False, 'new_quality_scores': 0, 'test_labels_read': False}
    create(OUT / name / f'info_{year}.json', info)
    create(OUT / f'prefix_control_{name}_{year}.json', {'status': 'passed', 'rows': 372000,
        'actual_saved_model_cold80_day_prefix_bit_identical': True,
        'original_mature_training_matrices_targets_andkeys_match': True,
        'full_independent_codec_bit_identical': True, 'test_data_read': False})
    del bundle, frame, x, raw, manual
    gc.collect()
    return verified_info(name, year)


def all_oof():
    import polars as pl
    fits, controls = [], {}
    promote_final_models()
    for year in YEARS:
        for name, cfg in CONFIGS.items():
            if RESOURCE is not None:
                RESOURCE.context = {'stage': 'original_GOSS_future_label_poison_boundary_control', 'model': name, 'year': year}
            path = OUT / f'boundary_control_{name}_{year}.json'
            create(path, core.original.boundary_control(year, cfg, engine.feature_names()))
            controls[f'{name}_{year}'] = read(path)
            assert controls[f'{name}_{year}']['status'] == 'passed'
            fits.append(train_one(name, year))
            print(json.dumps({'stage': 'passed_actual_full_GOSS_annual_model', 'model': name,
                'year': year, 'rows': fits[-1]['training_meta']['rows']}), flush=True)
    assert len(fits) == 30
    coverage = {}
    for name in CONFIGS:
        keys = pl.concat([pl.read_parquet(OUT / name / f'raw_{year}.parquet', columns=engine.KEYS) for year in YEARS])
        assert (len(keys), keys['trade_date'].n_unique(), keys['ts_code'].n_unique()) == (5635800, 1212, 4650)
        assert not keys.is_duplicated().any() and keys.equals(keys.sort('trade_date', 'ts_code'))
        coverage[name] = {'rows': len(keys), 'days': 1212, 'codes': 4650,
            'continuous_sorted_five_year_keys_sha256': engine.array_hash(keys.hash_rows(seed=2026).to_numpy())}
    create(OUT / 'oof_audit.json', {'status': 'passed', 'configurations': CONFIGS, 'years': YEARS,
        'actual_annual_fits': 30, 'actual300_round_complete_models': 30, 'checks': fits,
        'actual_final_native_fits_reused_with_full_provenance': 6,
        'entire_original_five_year_prediction_coverage': coverage, 'boundary_controls': controls,
        'all_original_full_matrix_targets_keys_and_maturity_matched': True,
        'small48_round_poison_control_fits_excluded_from_full_annual_counts': True,
        'complete124_plus138_official_scores_and_adoption_still_pending': True,
        'new_quality_scores': 0, 'test_labels_read': False, 'test_data_read': False})
