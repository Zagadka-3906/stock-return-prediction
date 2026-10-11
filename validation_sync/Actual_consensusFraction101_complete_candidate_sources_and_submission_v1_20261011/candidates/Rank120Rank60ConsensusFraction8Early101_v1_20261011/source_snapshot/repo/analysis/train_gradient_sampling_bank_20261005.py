"""Matched GOSS gradient sampling, using only mature past raw63 rows."""
from pathlib import Path
import importlib.util
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis')]
SOURCE = ROOT / 'analysis/train_diverse_backbones_20261003.py'
spec = importlib.util.spec_from_file_location('isolated_gradient_sampling_trainer_20261005', SOURCE)
engine = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = engine
spec.loader.exec_module(engine)
read, dump, sha, log = engine.read, engine.dump, engine.sha, engine.log
STORAGE = ROOT / 'analysis/gradient_sampling_storage_20261005.json'
OUT = Path(read(STORAGE)['output_directory']) if STORAGE.exists() else ROOT / 'analysis/gradient_sampling_bank_20261005'
YEARS = engine.YEARS
CONFIGS = {
    f'{label}_goss_{level}_r300': {
        'kind': 'lightgbm_gradient_sampling', 'target': target,
        'linear_tree': False, 'linear_lambda': 0.,
        'data_sample_strategy': 'goss', 'top_rate': top, 'other_rate': other,
        'num_boost_round': 300, 'learning_rate': .05,
        'num_leaves': 31, 'max_depth': 8, 'min_data_in_leaf': 128,
        'max_bin': 127, 'lambda_l2': 1., 'seed': 20261005,
        'num_threads': 8, 'clip_z': 8., 'chunk_rows': 32768,
        'return_quantiles': [.005, .995], 'reserve_available_ram_GiB': 14.}
    for label, target in (('rank', 'y_rank'), ('return', 'y_ret_1d'))
    for level, top, other in (('low', .1, .1), ('medium', .2, .1), ('high', .4, .2))}
engine.OUT, engine.CONFIGS = OUT, CONFIGS


def preprocessing(x):
    import numpy as np
    mean = np.zeros(x.shape[1], dtype=np.float64)
    scale = np.ones(x.shape[1], dtype=np.float64)
    for column in range(x.shape[1]):
        values = np.asarray(x[:, column], dtype=np.float64)
        values = values[np.isfinite(values)]
        if len(values):
            mean[column] = values.mean()
            deviation = values.std()
            if np.isfinite(deviation) and deviation > 1e-5:
                scale[column] = deviation
    return mean, scale


def standardize(x, mean, scale, cfg):
    import numpy as np
    clean = np.empty(x.shape, dtype=np.float32)
    for offset in range(0, len(x), cfg['chunk_rows']):
        block = np.asarray(x[offset:offset + cfg['chunk_rows']], dtype=np.float64)
        block = np.where(np.isfinite(block), block, np.nan)
        clean[offset:offset + len(block)] = np.clip((block - mean) / scale, -cfg['clip_z'], cfg['clip_z'])
    return clean


def leaf_summary(booster):
    import numpy as np
    summary = {'tree_count': 0, 'total_leaves': 0, 'leaves_with_linear_features': 0,
               'nonzero_linear_coefficients': 0, 'first_tree_constant': True,
               'all_leaf_coefficients_finite': True}
    for tree_index, tree in enumerate(booster.dump_model()['tree_info']):
        summary['tree_count'] += 1
        nodes = [tree['tree_structure']]
        while nodes:
            node = nodes.pop()
            if 'split_index' in node:
                nodes.extend((node['left_child'], node['right_child']))
            else:
                summary['total_leaves'] += 1
                features, coefficients = node.get('leaf_features', []), node.get('leaf_coeff', [])
                assert len(features) == len(coefficients)
                if features:
                    summary['leaves_with_linear_features'] += 1
                    summary['first_tree_constant'] &= tree_index > 0
                summary['nonzero_linear_coefficients'] += sum(float(c) != 0. for c in coefficients)
                summary['all_leaf_coefficients_finite'] &= bool(np.isfinite(coefficients).all())
    return summary


def parameters(cfg):
    return {'objective': 'regression', 'metric': 'None', 'boosting_type': 'gbdt',
        'device_type': 'cpu', 'tree_learner': 'serial', 'verbosity': -1,
        'linear_tree': cfg['linear_tree'], 'linear_lambda': cfg['linear_lambda'],
        'learning_rate': cfg['learning_rate'], 'num_leaves': cfg['num_leaves'],
        'max_depth': cfg['max_depth'], 'min_data_in_leaf': cfg['min_data_in_leaf'],
        'max_bin': cfg['max_bin'], 'lambda_l2': cfg['lambda_l2'],
        'deterministic': True, 'force_col_wise': True, 'num_threads': cfg['num_threads'],
        'seed': cfg['seed'], 'data_random_seed': cfg['seed'],
        'feature_fraction': 1., 'bagging_fraction': 1., 'bagging_freq': 0,
        'data_sample_strategy': cfg['data_sample_strategy'],
        'top_rate': cfg['top_rate'], 'other_rate': cfg['other_rate'],
        'use_missing': True, 'zero_as_missing': False}


def fit_arrays(x, y, cfg):
    import lightgbm as lgb
    import numpy as np
    mean, scale = preprocessing(x)
    clean = standardize(x, mean, scale, cfg)
    target = np.asarray(y, dtype=np.float64)
    assert len(target) == len(x) and np.isfinite(target).all()
    bounds = None
    if cfg['target'] == 'y_ret_1d':
        bounds = [float(v) for v in np.quantile(target, cfg['return_quantiles'])]
        target = np.clip(target, *bounds)
    params = parameters(cfg)
    dataset = lgb.Dataset(clean, label=target, params=params, free_raw_data=True)
    booster = lgb.train(params, dataset, num_boost_round=cfg['num_boost_round'])
    details = leaf_summary(booster)
    assert details['first_tree_constant'] and details['all_leaf_coefficients_finite']
    if cfg['linear_tree']:
        assert details['leaves_with_linear_features'] > 0 and details['nonzero_linear_coefficients'] > 0
    else:
        assert details['leaves_with_linear_features'] == 0
    model = booster.model_to_string()
    assert '[data_sample_strategy: goss]' in model
    assert booster.current_iteration() == cfg['num_boost_round']
    log(f"GOSS {cfg['target']} top{cfg['top_rate']} other{cfg['other_rate']}: actual{booster.current_iteration()} trees")
    del booster, dataset, clean
    engine.gc.collect()
    return {'kind': 'lightgbm_gradient_sampling', 'config': dict(cfg), 'mean': mean, 'scale': scale,
        'model_string': model, 'target_bounds': bounds, 'target_units': cfg['target'],
        'leaf_summary': details, 'missing_values_preserved_as_nan': True,
        'no_validation_early_stopping': True, 'native_training_parameters': params}


def predict_arrays(bundle, x):
    import lightgbm as lgb
    import numpy as np
    assert bundle['kind'] == 'lightgbm_gradient_sampling'
    booster = lgb.Booster(model_str=bundle['model_string'])
    parts = []
    cfg = bundle['config']
    for offset in range(0, len(x), cfg['chunk_rows']):
        clean = standardize(x[offset:offset + cfg['chunk_rows']], bundle['mean'], bundle['scale'], cfg)
        parts.append(booster.predict(clean, num_threads=1))
    return np.concatenate(parts) if parts else np.empty(0, dtype=np.float64)


def enhanced_dump(path, payload, immutable=False):
    if path.name.startswith('info_') and payload.get('training_meta'):
        bundle = engine.load_bundle(path.parent / f"model_{payload['year']}.joblib")
        payload.update(new_model_fits=1, leaf_summary=bundle['leaf_summary'],
                       native_model_string_sha256=engine.array_hash(
                           __import__('numpy').frombuffer(bundle['model_string'].encode('utf-8'), dtype='uint8')),
                       missing_values_preserved_as_nan=True)
    return dump(path, payload, immutable=immutable)


engine.fit_arrays, engine.predict_arrays, engine.dump = fit_arrays, predict_arrays, enhanced_dump


def verify():
    return engine.verify()


def freeze():
    OUT.mkdir(parents=True, exist_ok=True)
    if (OUT / 'protocol.json').exists():
        verify()
        return
    proof = ROOT / 'analysis/gradient_sampling_preflight_20261005/verification.json'
    assert read(proof)['status'] == 'passed_actual_gradient_sampling_maturity_native_reload_and_prefix_controls'
    paths = [Path(__file__), SOURCE, STORAGE, proof,
        ROOT / 'analysis/prepare_gradient_sampling_sources_20261005.py',
        ROOT / 'analysis/train_linear_leaf_bank_20261005.py',
        ROOT / 'analysis/gradient_sampling_complete_search_plan_20261005.json',
        ROOT / 'analysis/verify_gradient_sampling_bank_20261005.py',
        ROOT / 'analysis/run_gradient_sampling_bank_20261005.py',
        ROOT / 'analysis/prepare_gradient_sampling_bank_20261005.py',
        ROOT / 'analysis/gradient_sampling_bank_run_20261005.json',
        engine.FEATURE_FILE, engine.MANIFEST, ROOT / 'data/raw/训练集.csv',
        ROOT / 'run.py', ROOT / 'src/features.py', ROOT / '后续选模标准.md']
    paths += [ROOT / 'analysis/linear_bank_20261003' / name / f'info_{year}.json'
              for name in ('rank_ridge_l01', 'return_ridge_l01') for year in YEARS]
    dump(OUT / 'protocol.json', {'status': 'frozen_before30_actual_mature_annual_fits',
        'frozen_at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'configurations': CONFIGS,
        'features': engine.feature_names(), 'years': YEARS, 'expected_annual_fits': 30,
        'expected_five_year_configurations': 6,
        'validation': 'Original2020–2024 expanding OOF and mature one-day label purge.',
        'contrast': 'Six300-round GOSS configurations: top/other=.1/.1,.2/.1,.4/.2, rank and return; remaining parameters and training rows match the existing constant-leaf models.',
        'preprocessing': 'Past eligible rows per-column finite mean/std; float32 z clipped8; NaN retained, zero is a valid value; return quantiles.005/.995 past only.',
        'no_validation_early_stopping': True, 'selection_bias_uncorrected': True,
        'minimum_available_host_RAM_before_each_fit_GiB': 14.,
        'reserve_is_scheduling_policy_not_physical_boundary': True,
        'fulltraining_future_and_complete_output_quality_are_separate_pending_steps': True,
        'method_reference': 'https://lightgbm.readthedocs.io/en/stable/Parameters.html#data_sample_strategy',
        'versions': {name: engine.importlib.metadata.version(name) for name in ('lightgbm', 'numpy', 'polars', 'joblib')},
        'new_quality_scores': 0, 'test_data_read': False,
        'input_sha256': {str(path.resolve()): sha(path) for path in paths}}, immutable=True)


def boundary_control(year, cfg, features):
    import numpy as np
    import polars as pl
    cutoff = engine.fold_cutoff(year)
    lazy = pl.scan_parquet(engine.FEATURE_FILE)
    cols = engine.KEYS + features + [c for c in ('y_rank', 'y_ret_1d', 'is_train', 'price_valid') if c not in features]
    past = engine.training_frame(lazy, cutoff, cfg).select(cols).head(4096).collect()
    future = lazy.filter(pl.col('is_train') & (pl.col('trade_date') >= cutoff)).select(cols).head(1024).collect()
    sample = pl.concat([past, future])
    poisoned = sample.with_columns([
        pl.when(pl.col('trade_date') >= cutoff).then(pl.lit(12345., dtype=sample.schema[c])).otherwise(pl.col(c)).alias(c)
        for c in ('y_rank', 'y_ret_1d')])
    clean = engine.training_frame(sample.lazy(), cutoff, cfg).collect()
    changed = engine.training_frame(poisoned.lazy(), cutoff, cfg).collect()
    assert clean.equals(changed)
    small = dict(cfg, num_boost_round=48)
    x = engine.to_matrix(clean, features)
    a = fit_arrays(x, clean[cfg['target']].to_numpy(), small)
    b = fit_arrays(engine.to_matrix(changed, features), changed[cfg['target']].to_numpy(), small)
    assert a['model_string'] == b['model_string'] and a['target_bounds'] == b['target_bounds']
    assert np.array_equal(a['mean'], b['mean']) and np.array_equal(a['scale'], b['scale'])
    assert np.array_equal(predict_arrays(a, x), predict_arrays(b, x))
    return {'status': 'passed', 'year': year, 'cutoff_exclusive': cutoff,
        'control_training_rows': len(clean), 'boundary_future_label_poisoning_bit_identical': True,
        'actual48_round_control_models_and_past_preprocessing_bit_identical': True,
        'small_control_fits_excluded_from_actual_annual_counts': True, 'test_data_read': False}


def train_one(name, year):
    engine.train_one(name, year)
    return read(OUT / name / f'info_{year}.json')


def all_oof():
    import numpy as np
    import polars as pl
    import psutil
    freeze()
    features, checks = engine.feature_names(), []
    for name, cfg in CONFIGS.items():
        for year in YEARS:
            while not (OUT / name / f'info_{year}.json').exists() and psutil.virtual_memory().available < 14 * 2**30:
                time.sleep(10)
            boundary = OUT / f'boundary_control_{name}_{year}.json'
            if not boundary.exists():
                dump(boundary, boundary_control(year, cfg, features), immutable=True)
            info = train_one(name, year)
            reference = ROOT / 'analysis/linear_bank_20261003' / ('rank_ridge_l01' if cfg['target'] == 'y_rank' else 'return_ridge_l01') / f'info_{year}.json'
            baseline = read(reference)
            for key in ('rows', 'days', 'first', 'last', 'cutoff_exclusive', 'last_label_end',
                        'features', 'training_matrix_sha256', 'training_target_sha256', 'training_keys_sha256'):
                assert info['training_meta'][key] == baseline['training_meta'][key], key
            matched = read(ROOT / 'analysis/linear_leaf_bank_20261005' /
                ('rank_lgb_constant_r300' if cfg['target'] == 'y_rank' else 'return_lgb_constant_r300') / f'info_{year}.json')
            assert info['training_meta'] == matched['training_meta']
            assert info['configuration']['num_boost_round'] == matched['configuration']['num_boost_round']
            prefix_path = OUT / f'prefix_control_{name}_{year}.json'
            if not prefix_path.exists():
                frame = pl.scan_parquet(engine.FEATURE_FILE).filter(pl.col('is_train') & (pl.col('trade_date') // 10000 == year)).select(engine.KEYS + features + ['price_valid']).sort('trade_date', 'ts_code').collect()
                cutoff = int(frame['trade_date'].unique().sort()[79])
                prefix = frame.filter(pl.col('trade_date') <= cutoff)
                values = predict_arrays(engine.load_bundle(OUT / name / f'model_{year}.joblib'), engine.to_matrix(prefix, features))
                values[~prefix['price_valid'].to_numpy()] = -1e6
                saved = pl.read_parquet(OUT / name / f'raw_{year}.parquet').filter(pl.col('trade_date') <= cutoff)
                assert prefix.select(engine.KEYS).equals(saved.select(engine.KEYS))
                assert np.array_equal(values, saved['pred_raw'].to_numpy())
                dump(prefix_path, {'status': 'passed', 'rows': len(prefix),
                    'actual_saved_model_cold80_day_prefix_bit_identical': True,
                    'original_mature_training_matrices_targets_andkeys_match': True,
                    'reference_info_sha256': sha(reference), 'test_data_read': False}, immutable=True)
                del frame, prefix, values, saved
                engine.gc.collect()
            checks.append({'model': name, 'year': year, 'boundary': read(boundary), 'prefix': read(prefix_path)})
    verify()
    dump(OUT / 'oof_audit.json', {'status': 'passed', 'actual_annual_fits': 30,
        'configurations': CONFIGS, 'checks': checks, 'new_quality_scores': 0,
        'complete_output_quality_and_final_future_controls_pending': True, 'test_data_read': False}, immutable=True)


if __name__ == '__main__':
    all_oof()
