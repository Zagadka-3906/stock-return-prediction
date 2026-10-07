"""Independent numerical-tree decoder for identity-link histogram regressors."""
import numpy as np
from cpu_conditional_residual_mlp_codec_20261007 import BATCH, fit_preprocessing, prepare


RUNTIME_BATCH = 8192

def export(model, preprocessing, features):
    assert model.loss in ('squared_error', 'absolute_error', 'quantile')
    probes = np.array([-2., -0., 0., 3.], dtype=np.float64)
    assert np.array_equal(model._loss.link.inverse(probes).view('u8'), probes.view('u8'))
    if model.loss == 'quantile':assert np.isfinite(model.quantile) and 0. < model.quantile < 1.
    assert model.n_trees_per_iteration_ == 1 and model.n_features_in_ == len(features)
    fields = ('value', 'feature_idx', 'num_threshold', 'missing_go_to_left', 'left', 'right', 'is_leaf')
    trees = []
    for iteration in model._predictors:
        assert len(iteration) == 1
        nodes = iteration[0].nodes
        assert not np.any(nodes['is_categorical'])
        assert np.isfinite(nodes['value']).all() and np.isfinite(nodes['num_threshold']).all()
        trees.append({field: nodes[field].tolist() for field in fields})
    assert len(trees) == model.n_iter_
    return {'kind': 'sklearn_HistGradientBoostingRegressor_numerical_trees', 'loss': model.loss,
        'quantile': float(model.quantile) if model.loss == 'quantile' else None,
        'prediction_link': 'identity', 'baseline': float(model._baseline_prediction[0, 0]),
        'trees': trees, 'preprocessing': preprocessing, 'features': features,
        'fixed_inference_batch': BATCH, 'dtype': 'float64'}


def predict_decoded(state, raw):
    assert state['kind'] == 'sklearn_HistGradientBoostingRegressor_numerical_trees'
    assert state['loss'] in ('squared_error', 'absolute_error', 'quantile') and state['prediction_link'] == 'identity'
    if state['loss'] == 'quantile':assert np.isfinite(state['quantile']) and 0. < state['quantile'] < 1.
    assert state['fixed_inference_batch'] == BATCH
    x = prepare(raw, state['preprocessing'])
    assert x.shape[1] == len(state['features'])
    trees = []
    for tree in state['trees']:
        arrays = {k: np.asarray(v, dtype=np.float64 if k in ('value', 'num_threshold') else np.int64)
            for k, v in tree.items()}
        assert len({len(v) for v in arrays.values()}) == 1
        trees.append(arrays)
    result = np.empty(len(x), dtype=np.float64)
    for left in range(0, len(x), RUNTIME_BATCH):
        size = min(RUNTIME_BATCH, len(x) - left)
        padded = np.zeros((RUNTIME_BATCH, x.shape[1]), dtype=np.float64)
        padded[:size] = x[left:left+size]
        values = np.full(RUNTIME_BATCH, state['baseline'], dtype=np.float64)
        for tree in trees:
            node = np.zeros(RUNTIME_BATCH, dtype=np.int64)
            for _ in range(len(tree['value']) + 1):
                positions = np.flatnonzero(tree['is_leaf'][node] == 0)
                if not len(positions):
                    break
                current = node[positions]
                feature = tree['feature_idx'][current]
                tested = padded[positions, feature]
                go_left = np.where(np.isnan(tested), tree['missing_go_to_left'][current] != 0,
                    tested <= tree['num_threshold'][current])
                node[positions] = np.where(go_left, tree['left'][current], tree['right'][current])
                assert np.all((node >= 0) & (node < len(tree['value'])))
            else:
                raise AssertionError('Exported numerical tree did not terminate')
            assert np.all(tree['is_leaf'][node] != 0)
            # sklearn adds each tree output in this order to its float64 baseline.
            values += tree['value'][node]
        result[left:left+size] = values[:size]
    assert np.isfinite(result).all()
    return result


def predict_native(bundle, raw):
    assert bundle['model'].loss in ('squared_error', 'absolute_error', 'quantile')
    x = prepare(raw, bundle['preprocessing'])
    result = np.empty(len(x), dtype=np.float64)
    for left in range(0, len(x), RUNTIME_BATCH):
        size = min(RUNTIME_BATCH, len(x)-left)
        padded = np.zeros((RUNTIME_BATCH, x.shape[1]), dtype=np.float64)
        padded[:size] = x[left:left+size]
        result[left:left+size] = bundle['model'].predict(padded)[:size]
    assert np.isfinite(result).all()
    return result
