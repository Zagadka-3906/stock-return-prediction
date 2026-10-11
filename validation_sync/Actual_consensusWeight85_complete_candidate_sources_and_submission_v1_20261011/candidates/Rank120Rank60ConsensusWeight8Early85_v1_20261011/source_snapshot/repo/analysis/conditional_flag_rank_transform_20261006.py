"""Combine a flag-only native expectation with a causal common-rank curve."""
import numpy as np
from cohort_rank_calibration_20261006 import daily_percentile


def transform(raw, dates, flags, flagged_prediction, annual_global_curves,
              weight, first_year_slope, percentile=None):
    raw, dates, flags = map(np.asarray, (raw, dates, flags))
    assert raw.ndim == dates.ndim == flags.ndim == 1 and len(raw) == len(dates) == len(flags)
    assert np.isfinite(raw).all() and 0. <= float(weight) <= 1.
    if float(weight) == 0.:
        return raw.copy()
    assert first_year_slope in (.08, .125, .2)
    predicted = np.asarray(flagged_prediction)
    assert predicted.shape == raw.shape and np.isfinite(predicted).all()
    percentile = daily_percentile(raw, dates) if percentile is None else np.asarray(percentile)
    output = np.empty(len(raw), dtype=np.float64)
    for year in np.unique(dates // 10000):
        rows = dates // 10000 == year
        model = annual_global_curves.get(str(int(year)))
        p = percentile[rows]
        if model is None:
            assert year == 2020
            # Fixed positive affine prior: chosen as a declared training-CV
            # parameter, with no current-year target used to fit the curve.
            common = .5 + float(first_year_slope) * (p - .5)
        else:
            assert model['last_training_label_date'] < model['exclusive_cutoff'] < int(dates[rows].min())
            common = np.interp(p, model['centers'], model['global_curve'])
        specialist = np.clip(predicted[rows], 0., 1.)
        output[rows] = common + float(weight) * (flags[rows] == 1) * (specialist - common) + 1e-9 * p
    assert np.isfinite(output).all()
    return output
