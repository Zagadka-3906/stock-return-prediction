"""Twenty original mature annual fits, four final fits; never reuse small pilots."""
from pathlib import Path
import importlib.util
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
import quantile_tree_candidate_20261006 as core
SOURCE = A / 'train_diverse_backbones_20261003.py'
spec = importlib.util.spec_from_file_location('isolated_quantile_tree_full_trainer_20261006', SOURCE)
engine = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = engine
spec.loader.exec_module(engine)
STORAGE = A / 'quantile_tree_storage_20261006.json'
OUT = Path(core.matched.read(STORAGE)['output_directory'])
CONFIGS, YEARS = core.CONFIGS, engine.YEARS
read, dump, sha, log = engine.read, engine.dump, engine.sha, engine.log
engine.OUT, engine.CONFIGS = OUT, CONFIGS
engine.fit_arrays, engine.predict_arrays = core.fit_arrays, core.predict_arrays
fit_arrays, predict_arrays = core.fit_arrays, core.predict_arrays
RESOURCE = None


def verify():
    return engine.verify()


def freeze():
    OUT.mkdir(parents=True, exist_ok=True)
    if (OUT / 'protocol.json').exists():
        verify()
        return
    proof = A / 'quantile_tree_preflight_20261006/verification.json'
    assert read(proof)['status'] == 'passed_actual_quantile_native_maturity_reload_and_cold80_controls'
    assert read(proof)['actual_annual_fits'] == read(proof)['new_quality_scores'] == 0
    paths = [Path(__file__), Path(core.__file__), Path(core.matched.__file__), SOURCE,
        STORAGE, proof, A / 'quantile_tree_candidate_plan_20261006.json',
        A / 'run_quantile_tree_full_workflow_20261006.py',
        A / 'verify_quantile_tree_full_future_20261006.py',
        A / 'verify_quantile_tree_candidate_20261006.py',
        A / 'verify_linear_leaf_bank_20261005.py',
        A / 'linear_leaf_actual_resource_sampler_20261005.py',
        A / 'frozen_provenance_execution_scope_20261004.py',
        A / 'locked_read_hash_cache_20261004.py',
        A / 'hidden_windows_child_creation_20261006.py',
        A / 'quantile_tree_native_full_workflow_20261006/run.json',
        engine.FEATURE_FILE, engine.MANIFEST, ROOT / 'data/raw/训练集.csv',
        ROOT / 'run.py', ROOT / 'src/features.py', ROOT / '后续选模标准.md']
    paths += [A / f'linear_bank_20261003/{name}/info_{year}.json'
        for name in ('rank_ridge_l01', 'return_ridge_l01') for year in YEARS]
    dump(OUT / 'protocol.json', {
        'status': 'frozen_before20_actual_full_mature300_round_annual_quantile_fits',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'configurations': CONFIGS,
        'features': engine.feature_names(), 'years': YEARS,
        'expected_annual_fits': 20, 'expected_final_fits': 4,
        'expected_complete_validation_rows': 5635800, 'expected_validation_days': 1212,
        'expected_codes': 4650, 'training_boosting_iterations_each_full_fit': 300,
        'validation': 'Original2020-2024 mature expanding OOF, one-day purge, continuous output state.',
        'preprocessing': 'Same finite past mean/std, z clipping8, native NaN, past return quantiles.005/.995 as matched constant leaves.',
        'only_objective_contrast': 'Quantile instead of squared loss; fixed rank median and return.1/.5/.9.',
        'minimum_available_host_RAM_before_each_full_fit_GiB': 14.,
        'memory_reserve_is_scheduling_policy_not_physical_boundary': True,
        'small4096_row48_round_pilots_excluded_from_full_fit_counts': True,
        'no_validation_early_stopping': True, 'selection_bias_uncorrected': True,
        'complete_future_and_complete_official_quality_and_adoption_still_pending': True,
        'new_quality_scores': 0, 'test_labels_read': False,
        'input_sha256': {str(p.resolve()): sha(p) for p in dict.fromkeys(paths)}}, immutable=True)


def boundary_control(year, cfg, features):
    import numpy as np
    import polars as pl
    cutoff = engine.fold_cutoff(year)
    lazy = pl.scan_parquet(engine.FEATURE_FILE)
    columns = engine.KEYS + features + ['y_rank', 'y_ret_1d', 'is_train', 'price_valid']
    past = engine.training_frame(lazy, cutoff, cfg).select(columns).head(4096).collect()
    future = lazy.filter(pl.col('is_train') & (pl.col('trade_date') >= cutoff)).select(columns).head(1024).collect()
    sample = pl.concat([past, future])
    poisoned = sample.with_columns([pl.when(pl.col('trade_date') >= cutoff)
        .then(pl.lit(12345., dtype=sample.schema[t])).otherwise(pl.col(t)).alias(t)
        for t in ('y_rank', 'y_ret_1d')])
    clean = engine.training_frame(sample.lazy(), cutoff, cfg).collect()
    changed = engine.training_frame(poisoned.lazy(), cutoff, cfg).collect()
    assert clean.equals(changed) and len(clean) == 4096
    pilot = dict(cfg, num_boost_round=48)
    x = engine.to_matrix(clean, features)
    a = fit_arrays(x, clean[cfg['target']].to_numpy(), pilot)
    b = fit_arrays(engine.to_matrix(changed, features), changed[cfg['target']].to_numpy(), pilot)
    assert a['model_string'] == b['model_string'] and a['target_bounds'] == b['target_bounds']
    assert np.array_equal(a['mean'], b['mean']) and np.array_equal(a['scale'], b['scale'])
    assert np.array_equal(predict_arrays(a, x), predict_arrays(b, x))
    return {'status': 'passed', 'year': year, 'cutoff_exclusive': cutoff,
        'control_training_rows': len(clean), 'actual_two48_round_controls_bit_identical': True,
        'future_label_poison_mature_filter_and_preprocessing_bit_identical': True,
        'actual_annual_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False}


def enhanced_dump(path, payload, immutable=False):
    if path.name.startswith('info_') and payload.get('training_meta'):
        bundle = engine.load_bundle(path.parent / f"model_{payload['year']}.joblib")
        assert bundle['requested_and_actual_boosting_iterations'] == 300
        assert bundle['config'] == CONFIGS[payload['model']]
        payload.update(actual_native_boosting_iterations=300, new_model_fits=1,
            native_objective='quantile', native_alpha=bundle['config']['alpha'],
            leaf_summary=bundle['leaf_summary'],
            native_model_string_sha256=engine.array_hash(
                __import__('numpy').frombuffer(bundle['model_string'].encode('utf-8'), dtype='uint8')))
    return dump(path, payload, immutable=immutable)


engine.freeze, engine.boundary_control, engine.dump = freeze, boundary_control, enhanced_dump


def train_one(name, year):
    import psutil
    assert name in CONFIGS and year in (*YEARS, 2025)
    while psutil.virtual_memory().available < 14 * 2**30:
        time.sleep(10)
    if RESOURCE is not None:
        RESOURCE.context = {'stage': 'actual_full_mature300_round_quantile_fit_and_native_controls',
                            'model': name, 'year': year}
    engine.train_one(name, year)
    info = read(OUT / name / f'info_{year}.json')
    assert info['actual_native_boosting_iterations'] == 300 and info['native_objective'] == 'quantile'
    reference = A / f"linear_bank_20261003/{'rank_ridge_l01' if CONFIGS[name]['target'] == 'y_rank' else 'return_ridge_l01'}/info_{year}.json"
    for field in ('rows', 'days', 'first', 'last', 'cutoff_exclusive', 'last_label_end',
                  'training_matrix_sha256', 'training_target_sha256', 'training_keys_sha256', 'features'):
        assert info['training_meta'][field] == read(reference)['training_meta'][field], (name, year, field)
    return info


def all_oof():
    freeze()
    fits, controls = [], {}
    for name, cfg in CONFIGS.items():
        for year in YEARS:
            path = OUT / f'boundary_control_{name}_{year}.json'
            if not path.exists():
                dump(path, boundary_control(year, cfg, engine.feature_names()), immutable=True)
            controls[f'{name}_{year}'] = read(path)
            fits.append(train_one(name, year))
    assert len(fits) == 20 and all(x['actual_native_boosting_iterations'] == 300 for x in fits)
    dump(OUT / 'oof_audit.json', {'status': 'passed', 'configurations': CONFIGS,
        'years': YEARS, 'actual_annual_fits': 20, 'actual300_round_complete_models': 20,
        'all_original_full_row_matrix_target_keys_and_maturity_hashes_matched': True,
        'boundary_controls': controls, 'complete_scheme_quality_and_future_still_pending': True,
        'new_quality_scores': 0, 'test_labels_read': False}, immutable=True)
