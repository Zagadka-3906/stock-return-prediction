"""Prospective native quantile trees; no validation labels enter fitting."""
from pathlib import Path
import gc
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis')]
import train_linear_leaf_bank_20261005 as matched

CONFIGS = {}
for label, target, alphas in (('rank', 'y_rank', (.5,)),
                               ('return', 'y_ret_1d', (.1, .5, .9))):
    for alpha in alphas:
        name = f'{label}_lgb_quantile_a{int(alpha * 100):03d}_r300'
        CONFIGS[name] = dict(matched.CONFIGS[f'{label}_lgb_constant_r300'],
            kind='lightgbm_quantile_tree', objective='quantile', alpha=alpha)


def parameters(cfg):
    assert cfg['objective'] == 'quantile' and not cfg['linear_tree']
    assert 0 < cfg['alpha'] < 1
    return dict(matched.parameters(cfg), objective='quantile', alpha=cfg['alpha'])


def fit_arrays(x, y, cfg):
    import lightgbm as lgb
    import numpy as np
    mean, scale = matched.preprocessing(x)
    clean = matched.standardize(x, mean, scale, cfg)
    target = np.asarray(y, dtype=np.float64)
    assert len(target) == len(x) and np.isfinite(target).all()
    bounds = None
    if cfg['target'] == 'y_ret_1d':
        bounds = [float(v) for v in np.quantile(target, cfg['return_quantiles'])]
        target = np.clip(target, *bounds)
    params = parameters(cfg)
    dataset = lgb.Dataset(clean, label=target, params=params, free_raw_data=True)
    booster = lgb.train(params, dataset, num_boost_round=cfg['num_boost_round'])
    assert booster.current_iteration() == cfg['num_boost_round']
    details = matched.leaf_summary(booster)
    assert details['tree_count'] == cfg['num_boost_round']
    assert details['leaves_with_linear_features'] == 0
    assert details['all_leaf_coefficients_finite']
    bundle = {'kind': 'lightgbm_quantile_tree', 'config': dict(cfg),
        'mean': mean, 'scale': scale, 'model_string': booster.model_to_string(),
        'target_bounds': bounds, 'target_units': cfg['target'], 'leaf_summary': details,
        'no_validation_early_stopping': True, 'native_training_parameters': params,
        'requested_and_actual_boosting_iterations': booster.current_iteration(),
        'past_only_preprocessing': True, 'missing_values_preserved_as_nan': True}
    del booster, dataset, clean
    gc.collect()
    return bundle


def predict_arrays(bundle, x):
    import lightgbm as lgb
    import numpy as np
    assert bundle['kind'] == 'lightgbm_quantile_tree'
    cfg = bundle['config']
    booster = lgb.Booster(model_str=bundle['model_string'])
    parts = []
    for offset in range(0, len(x), cfg['chunk_rows']):
        z = matched.standardize(x[offset:offset + cfg['chunk_rows']],
            bundle['mean'], bundle['scale'], cfg)
        parts.append(booster.predict(z, num_threads=1))
    return np.concatenate(parts) if parts else np.empty(0, dtype=np.float64)
