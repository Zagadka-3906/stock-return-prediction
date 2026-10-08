"""Fixed 8192-row inference recipe for native and independent linear states."""
import numpy as np
from nonflag_residual_HGB_preprocessing_20261007 import prepare

BATCH_ROWS = 8192

def export(bundle):
    model = bundle['model']
    assert model.coef_.shape == (64,) and np.isfinite(model.coef_).all()
    return {'kind': 'nonflag_residual_Ridge', 'batch_rows': BATCH_ROWS,
            'coefficients': model.coef_.tolist(), 'intercept': float(model.intercept_),
            'preprocessing': bundle['preprocessing'], 'features': bundle['features']}

def predict_native(bundle, raw):
    result = np.empty(len(raw), dtype=np.float64)
    for left in range(0, len(raw), BATCH_ROWS):
        n = min(BATCH_ROWS, len(raw)-left)
        block = np.zeros((BATCH_ROWS, 64), dtype=np.float64)
        block[:n] = prepare(raw[left:left+n], bundle['preprocessing'])
        result[left:left+n] = bundle['model'].predict(block)[:n]
    return result

def predict_decoded(state, raw):
    assert state['kind'] == 'nonflag_residual_Ridge' and state['batch_rows'] == BATCH_ROWS
    coef = np.asarray(state['coefficients'], dtype=np.float64)
    result = np.empty(len(raw), dtype=np.float64)
    for left in range(0, len(raw), BATCH_ROWS):
        n = min(BATCH_ROWS, len(raw)-left)
        block = np.zeros((BATCH_ROWS, 64), dtype=np.float64)
        block[:n] = prepare(raw[left:left+n], state['preprocessing'])
        result[left:left+n] = (np.matmul(block, coef)+state['intercept'])[:n]
    return result
