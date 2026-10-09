"""Add a causal cohort residual without changing any eligible stock prediction."""
import numpy as np


def transform(raw, dates, flags, residual, weight):
    raw, dates, flags, residual = map(np.asarray, (raw, dates, flags, residual))
    assert raw.shape == dates.shape == flags.shape == residual.shape
    assert raw.ndim == 1 and np.isfinite(raw).all() and np.isfinite(residual).all()
    assert 0. <= float(weight) <= 1. and np.all((flags == 0) | (flags == 1))
    assert np.all(residual[dates < 20210101] == 0.)
    if float(weight) == 0.:
        return raw.copy()
    result = raw.copy()
    selected = flags == 1
    result[selected] += float(weight) * residual[selected]
    assert np.isfinite(result).all()
    return result
