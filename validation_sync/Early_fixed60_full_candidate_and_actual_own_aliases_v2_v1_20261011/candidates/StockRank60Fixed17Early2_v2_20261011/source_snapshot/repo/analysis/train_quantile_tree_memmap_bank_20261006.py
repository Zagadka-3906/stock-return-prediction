"""Full original20 annual models with a measured exact-memory backend."""
from pathlib import Path
import gc
import json
import shutil
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
import quantile_tree_candidate_20261006 as core
import mature_training_memmap_20261006 as mapped
import train_quantile_tree_bank_20261006 as original

engine, CONFIGS, YEARS = core.matched.engine, core.CONFIGS, tuple(range(2020, 2025))
OUT = A / 'quantile_tree_memmap_complete_bank_20261006'
CAPACITY = A / 'quantile_tree_memmap_capacity_20261006'
STORAGE = A / 'quantile_tree_storage_20261006.json'
SCRATCH = ROOT / 'tmp/quantile_tree_memmap_complete_bank_20261006'
RESOURCE = None
sha = mapped.file_sha
read = engine.read
predict_arrays = core.predict_arrays


def dump(path, value, immutable=False):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x' if immutable else 'w', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def verify():
    protocol = read(OUT / 'protocol.json')
    for path, digest in protocol['input_sha256'].items():
        assert sha(Path(path)) == digest, path
    return protocol


def freeze():
    if (OUT / 'protocol.json').exists():
        return verify()
    proof = read(CAPACITY / 'verification.json')
    assert proof['status'] == 'passed_actual_four_largest_full_native_fits_and_complete_future_controls'
    assert proof['actual_full_final_fits'] == proof['actual300_iteration_models'] == 4
    assert proof['actual_annual_fits'] == proof['new_quality_scores'] == 0
    samples = [json.loads(line) for line in (CAPACITY / 'actual_resource_samples.jsonl').read_text(encoding='utf-8').splitlines()]
    fits = [x for x in samples if x['context']['stage'] == 'actual_full6754006_row300_round_native_fit']
    assert fits and {x['context']['model'] for x in fits} == set(CONFIGS)
    reserve = max(6 * 2**30, max(x['target_and_descendant_rss_bytes'] for x in fits) + 2 * 2**30)
    paths = [Path(__file__), Path(core.__file__), Path(core.matched.__file__), Path(mapped.__file__), Path(original.__file__),
        A / 'run_quantile_tree_memmap_full_workflow_20261006.py',
        A / 'verify_quantile_tree_memmap_full_future_20261006.py',
        A / 'verify_full2025_quantile_memmap_capacity_20261006.py',
        A / 'verify_mature_training_memmap_20261006.py',
        A / 'train_diverse_backbones_20261003.py', A / 'verify_linear_leaf_bank_20261005.py',
        A / 'locked_read_hash_cache_20261004.py', A / 'linear_leaf_actual_resource_sampler_20261005.py',
        STORAGE, CAPACITY / 'protocol.json', CAPACITY / 'verification.json', CAPACITY / 'resource_summary.json',
        A / 'service_owned_workflows_20261006/quantile_tree_memmap_capacity/service_execution.json',
        A / 'mature_training_memmap_controls_20261006/verification.json',
        A / 'quantile_tree_candidate_plan_20261006.json',
        engine.FEATURE_FILE, engine.MANIFEST, ROOT / 'data/raw/训练集.csv',
        ROOT / 'run.py', ROOT / 'src/features.py', ROOT / '后续选模标准.md']
    paths += list(CAPACITY.glob('*/model_2025.joblib')) + list(CAPACITY.glob('*/info_2025.json')) + list(CAPACITY.glob('*/future_verification.json'))
    paths += [A / f'linear_bank_20261003/{n}/info_{year}.json'
        for n in ('rank_ridge_l01', 'return_ridge_l01') for year in (*YEARS, 2025)]
    OUT.mkdir(parents=True, exist_ok=True)
    protocol = {'status': 'frozen_before20_actual_full_mature300_round_annual_quantile_fits',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'configurations': CONFIGS,
        'features': engine.feature_names(), 'years': YEARS, 'expected_annual_fits': 20,
        'expected_final_fits': 4, 'four_original_full_native_final_fits_reused_with_complete_provenance': True,
        'copied_model_files_not_counted_as_additional_fits': True,
        'expected_complete_validation_rows': 5635800, 'expected_validation_days': 1212, 'expected_codes': 4650,
        'actual_iterations_each_full_fit': 300, 'no_validation_early_stopping': True,
        'same_original_full_mature_rows63_features_params_and_native_objectives': True,
        'backend': 'Exact original sorted float32 matrix, per-column original full mean/std, chunk-identical standardization on D disk maps.',
        'minimum_available_host_RAM_before_each_fit_bytes': reserve,
        'measured_largest_window_native_peak_bytes': max(x['target_and_descendant_rss_bytes'] for x in fits),
        'reserve_derived_from_actual_largest_native_fit_and2GiB_margin': True,
        'legacy14GiB_configuration_field_is_not_a_native_model_parameter': True,
        'old_frozen_sources_queues_and_scientific_parameters_not_edited': True,
        'complete198_official_scores_and_adoption_still_pending': True,
        'physical_global_resource_boundary_established': False, 'selection_bias_uncorrected': True,
        'new_quality_scores': 0, 'test_labels_read': False,
        'input_sha256': {str(p.resolve()): sha(p) for p in dict.fromkeys(paths)}}
    dump(OUT / 'protocol.json', protocol, immutable=True)
    return protocol


def verified_info(name, year):
    import numpy as np
    info = read(OUT / name / f'info_{year}.json')
    model = OUT / name / f'model_{year}.joblib'
    assert sha(model) == info['model_sha256'] and info['configuration'] == CONFIGS[name]
    assert info['actual_native_boosting_iterations'] == 300 and info['native_objective'] == 'quantile'
    label = 'rank_ridge_l01' if CONFIGS[name]['target'] == 'y_rank' else 'return_ridge_l01'
    assert info['training_meta'] == read(A / f'linear_bank_20261003/{label}/info_{year}.json')['training_meta']
    bundle = engine.load_bundle(model)
    assert bundle['config'] == CONFIGS[name] and bundle['native_training_parameters'] == core.parameters(CONFIGS[name])
    assert bundle['requested_and_actual_boosting_iterations'] == bundle['leaf_summary']['tree_count'] == 300
    assert np.isfinite(bundle['mean']).all() and np.isfinite(bundle['scale']).all()
    if year < 2025:
        assert sha(OUT / name / f'raw_{year}.parquet') == info['prediction_sha256']
    return info


def promote_final_models():
    for name in CONFIGS:
        source = CAPACITY / name
        info = read(source / 'info_2025.json')
        assert read(source / 'future_verification.json')['status'] == 'passed'
        assert sha(source / 'model_2025.joblib') == info['model_sha256']
        folder = OUT / name
        folder.mkdir()
        shutil.copyfile(source / 'model_2025.joblib', folder / 'model_2025.joblib')
        assert sha(folder / 'model_2025.joblib') == info['model_sha256']
        info.update(status='passed', full24_native_bank_promotion_pending=False,
            actual_native_fit_reused_from=str(source), actual_fit_origin_info_sha256=sha(source / 'info_2025.json'),
            copied_file_is_not_an_additional_native_fit=True)
        dump(folder / 'info_2025.json', info, immutable=True)
        verified_info(name, 2025)


def annual_artifact(year):
    cfg = next(iter(CONFIGS.values()))
    record = OUT / f'exact_training_artifact_{year}.json'
    if record.exists():
        return read(record)
    artifact = mapped.build(engine, year, SCRATCH / str(year), RESOURCE)
    mean, scale, clean = mapped.standardize(core, artifact, cfg, Path(artifact['folder']) / 'standardized_float32.bin', RESOURCE)
    value = {'artifact': artifact, 'mean': mean.tolist(), 'scale': scale.tolist(), 'standardization': clean}
    dump(record, value, immutable=True)
    return value


def train_one(name, year):
    import numpy as np
    import polars as pl
    import psutil
    assert name in CONFIGS and year in (*YEARS, 2025)
    if (OUT / name / f'info_{year}.json').exists():
        return verified_info(name, year)
    assert year in YEARS
    reserve = read(OUT / 'protocol.json')['minimum_available_host_RAM_before_each_fit_bytes']
    while psutil.virtual_memory().available < reserve:
        time.sleep(10)
    value = annual_artifact(year)
    cfg = CONFIGS[name]
    if RESOURCE is not None:
        RESOURCE.context = {'stage': 'actual_full_mature300_round_annual_quantile_fit', 'model': name, 'year': year,
                            'rows': value['artifact']['shape'][0]}
    started = time.monotonic()
    bundle = mapped.fit_preprocessed(core, value['artifact'], cfg, np.asarray(value['mean']), np.asarray(value['scale']), value['standardization'])
    fit_seconds = time.monotonic() - started
    model = OUT / name / f'model_{year}.joblib'
    engine.save_bundle(model, bundle)
    metadata = dict(value['artifact']['training_meta_without_target'],
                    training_target_sha256=value['artifact']['targets'][cfg['target']]['sha256'])
    features = engine.feature_names()
    frame = pl.scan_parquet(engine.FEATURE_FILE).filter(pl.col('is_train') & (pl.col('trade_date') // 10000 == year)).select(engine.KEYS + features + ['price_valid']).sort('trade_date', 'ts_code').collect()
    x = engine.to_matrix(frame, features)
    raw = predict_arrays(bundle, x)
    assert np.isfinite(raw).all() and np.array_equal(raw, predict_arrays(engine.load_bundle(model), x))
    raw[~frame['price_valid'].to_numpy()] = -1e6
    prediction = OUT / name / f'raw_{year}.parquet'
    frame.select(engine.KEYS).with_columns(pl.Series('pred_raw', raw)).write_parquet(prediction)
    info = {'status': 'passed', 'model': name, 'year': year, 'configuration': cfg, 'training_meta': metadata,
        'actual_native_boosting_iterations': 300, 'native_objective': 'quantile', 'native_alpha': cfg['alpha'],
        'model_sha256': sha(model), 'prediction_sha256': sha(prediction), 'rows': len(frame),
        'fit_seconds': fit_seconds, 'new_model_fits': 1, 'model_reload_bit_identical': True,
        'leaf_summary': bundle['leaf_summary'], 'new_quality_scores': 0, 'test_labels_read': False}
    dump(OUT / name / f'info_{year}.json', info, immutable=True)
    del bundle, frame, x, raw
    gc.collect()
    return verified_info(name, year)


def all_oof():
    import polars as pl
    fits, controls = [], {}
    promote_final_models()
    for year in YEARS:
        for name, cfg in CONFIGS.items():
            path = OUT / f'boundary_control_{name}_{year}.json'
            dump(path, original.boundary_control(year, cfg, engine.feature_names()), immutable=True)
            controls[f'{name}_{year}'] = read(path)
            fits.append(train_one(name, year))
            print(json.dumps({'status': 'passed_actual_full_annual_model', 'model': name, 'year': year,
                              'training_rows': fits[-1]['training_meta']['rows']}), flush=True)
    assert len(fits) == 20
    coverage = {}
    for name in CONFIGS:
        keys = pl.concat([pl.read_parquet(OUT / name / f'raw_{year}.parquet', columns=engine.KEYS) for year in YEARS])
        assert (len(keys), keys['trade_date'].n_unique(), keys['ts_code'].n_unique()) == (5635800, 1212, 4650)
        assert not keys.is_duplicated().any() and keys.equals(keys.sort('trade_date', 'ts_code'))
        coverage[name] = {'rows': len(keys), 'days': 1212, 'codes': 4650,
                          'continuous_sorted_five_year_keys_sha256': engine.array_hash(keys.hash_rows(seed=2026).to_numpy())}
    dump(OUT / 'oof_audit.json', {'status': 'passed', 'configurations': CONFIGS, 'years': YEARS,
        'actual_annual_fits': 20, 'actual300_round_complete_models': 20,
        'actual_final_native_fits_reused_with_full_provenance': 4,
        'entire_original_five_year_prediction_coverage': coverage,
        'all_original_full_matrix_target_keys_and_maturity_metadata_matched': True,
        'boundary_controls': controls, 'complete198_official_scores_and_adoption_still_pending': True,
        'new_quality_scores': 0, 'test_labels_read': False}, immutable=True)
