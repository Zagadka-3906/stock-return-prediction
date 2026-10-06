"""Route CPU MLP residuals with same-day forecast CDF; preserve2020 identity."""
import numpy as np
from direct_flag_centered_rank_CDF_transform_20261007 import prepare


def apply_prepared(raw, residual_prediction, weight, prepared):
    raw, residual_prediction = np.asarray(raw), np.asarray(residual_prediction)
    assert raw.shape == residual_prediction.shape and np.isfinite(residual_prediction).all()
    assert 0. <= float(weight) <= 1.
    output = raw.astype(np.float64, copy=True)
    if float(weight) == 0.:
        return output
    for day, positions, percentile, knots, ordered in prepared:
        if day < 20210101:
            assert np.all(residual_prediction[positions] == 0.)
            continue
        q = percentile + float(weight) * residual_prediction[positions]
        output[positions] = np.interp(np.clip(q, knots[0], knots[-1]), knots, ordered)
    assert np.isfinite(output).all()
    return output


def transform(raw, dates, flags, price_valid, residual_prediction, weight, universe):
    return apply_prepared(raw, residual_prediction, weight,
        prepare(raw, dates, flags, price_valid, universe))
