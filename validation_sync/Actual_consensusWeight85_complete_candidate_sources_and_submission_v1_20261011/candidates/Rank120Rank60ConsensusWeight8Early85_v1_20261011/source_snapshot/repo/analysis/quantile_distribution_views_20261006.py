"""Fixed causal distribution views; no native fit or fitted weights."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis')]
import train_quantile_tree_memmap_bank_20261006 as parent

MEMBERS = tuple(f'return_lgb_quantile_a{alpha:03d}_r300' for alpha in (10, 50, 90))


def config(operation, penalty=0.):
    return {'kind': 'quantile_distribution_view', 'target': 'y_ret_1d',
        'members': list(MEMBERS), 'operation': operation, 'width_penalty': penalty,
        'ordered_heads': 'Pointwise sort of raw10/50/90percent native predictions.',
        'fixed_before_any_new_full_quality_scores': True,
        'score_requires_past_only_return_mapping': True}


CONFIGS = {
    'quantile_ordered_tail_midpoint': config('midpoint'),
    'quantile_ordered_negative_width': config('negative_width'),
    'quantile_ordered_reflected_upper': config('reflected_upper'),
    **{f'quantile_ordered_median_width_p{int(penalty * 100):03d}': config('median_minus_width', penalty)
       for penalty in (.25, .5, 1.)},
}


def from_heads(cfg, heads):
    import numpy as np
    assert cfg in CONFIGS.values() and len(heads) == 3
    heads = np.asarray(heads, dtype=np.float64)
    assert heads.ndim == 2 and np.isfinite(heads).all()
    lower, middle, upper = np.min(heads, axis=0), np.median(heads, axis=0), np.max(heads, axis=0)
    width = upper - lower
    assert np.all(width >= 0)
    op = cfg['operation']
    if op == 'midpoint':
        pred = .5 * (lower + upper)
    elif op == 'negative_width':
        pred = -width
    elif op == 'reflected_upper':
        pred = -upper
    elif op == 'median_minus_width':
        pred = middle - cfg['width_penalty'] * width
    else:
        raise AssertionError(op)
    assert np.isfinite(pred).all()
    return pred


def predict_arrays(bundle, x):
    assert bundle['kind'] == 'quantile_distribution_view'
    assert [item['name'] for item in bundle['members']] == list(MEMBERS)
    return from_heads(bundle['config'], [parent.predict_arrays(item['bundle'], x) for item in bundle['members']])


def bundle_from(name, year):
    import lightgbm as lgb
    cfg = CONFIGS[name]
    members, metadata, sources = [], None, {}
    for member in MEMBERS:
        folder = parent.OUT / member
        info_path, model_path = folder / f'info_{year}.json', folder / f'model_{year}.joblib'
        info = parent.read(info_path)
        assert info['status'] == 'passed' and info['actual_native_boosting_iterations'] == 300
        assert parent.sha(model_path) == info['model_sha256']
        model = parent.engine.load_bundle(model_path)
        booster = lgb.Booster(model_str=model['model_string'])
        assert booster.current_iteration() == booster.num_trees() == 300
        assert model['config'] == parent.CONFIGS[member]
        assert model['target_units'] == 'y_ret_1d'
        metadata = info['training_meta'] if metadata is None else metadata
        assert metadata == info['training_meta']
        assert metadata['last'] < metadata['cutoff_exclusive']
        assert metadata['last_label_end'] <= metadata['cutoff_exclusive']
        members.append({'name': member, 'bundle': model, 'model_sha256': info['model_sha256']})
        sources[str(info_path.resolve())] = parent.sha(info_path)
        sources[str(model_path.resolve())] = info['model_sha256']
    return {'kind': 'quantile_distribution_view', 'config': cfg, 'members': members,
        'new_model_fits': 0, 'fixed_transform_no_fitted_parameters': True}, metadata, sources
