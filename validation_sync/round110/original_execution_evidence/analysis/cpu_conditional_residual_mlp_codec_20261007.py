"""Training-only preprocessing and a pure NumPy decoder independent of sklearn models."""
import numpy as np

BATCH = 256


def fit_preprocessing(x):
    x = np.asarray(x, dtype=np.float64)
    med = np.array([np.median(c[np.isfinite(c)]) if np.isfinite(c).any() else 0. for c in x.T])
    clean = np.where(np.isfinite(x), x, med)
    mean, scale = clean.mean(axis=0), clean.std(axis=0)
    scale = np.where(scale > 1e-8, scale, 1.)
    return {'median': med.tolist(), 'mean': mean.tolist(), 'scale': scale.tolist(), 'clip': 10.}


def prepare(x, preprocessing):
    x = np.asarray(x, dtype=np.float64)
    med, mean, scale = (np.asarray(preprocessing[k], dtype=np.float64) for k in ('median', 'mean', 'scale'))
    values = np.where(np.isfinite(x), x, med)
    values = np.clip((values - mean) / scale, -preprocessing['clip'], preprocessing['clip'])
    assert np.isfinite(values).all()
    return np.ascontiguousarray(values)


def export(model, preprocessing, features):
    assert model.out_activation_ == 'identity' and model.activation in ('relu', 'tanh')
    return {'activation': model.activation, 'output_activation': 'identity',
        'layers': [{'weight': w.tolist(), 'bias': b.tolist()} for w, b in zip(model.coefs_, model.intercepts_)],
        'preprocessing': preprocessing, 'features': features, 'dtype': 'float64', 'fixed_inference_batch': BATCH}


def predict_native(bundle, raw):
    x = prepare(raw, bundle['preprocessing'])
    result = np.empty(len(x), dtype=np.float64)
    for left in range(0, len(x), BATCH):
        size = min(BATCH, len(x) - left)
        padded = np.zeros((BATCH, x.shape[1]), dtype=np.float64)
        padded[:size] = x[left:left+size]
        result[left:left+size] = bundle['model'].predict(padded)[:size]
    return result


def predict_decoded(state, raw):
    x = prepare(raw, state['preprocessing'])
    assert state['output_activation'] == 'identity' and state['fixed_inference_batch'] == BATCH
    weights = [(np.asarray(r['weight'], dtype=np.float64), np.asarray(r['bias'], dtype=np.float64)) for r in state['layers']]
    result = np.empty(len(x), dtype=np.float64)
    for left in range(0, len(x), BATCH):
        size = min(BATCH, len(x) - left)
        current = np.zeros((BATCH, x.shape[1]), dtype=np.float64)
        current[:size] = x[left:left+size]
        for index, (weight, bias) in enumerate(weights):
            current = np.dot(current, weight)
            current += bias
            if index != len(weights)-1:
                if state['activation'] == 'relu':
                    np.maximum(current, 0., out=current)
                else:
                    np.tanh(current, out=current)
        result[left:left+size] = current[:size, 0]
    assert np.isfinite(result).all()
    return result
