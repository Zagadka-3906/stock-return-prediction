"""Past-fitted monotone cohort curves, with label-free per-day prediction."""
import numpy as np
from scipy.stats import rankdata
from sklearn.isotonic import IsotonicRegression

EPSILON = 1e-9


def daily_percentile(values, dates):
    values, dates = np.asarray(values), np.asarray(dates)
    assert values.ndim == dates.ndim == 1 and len(values) == len(dates)
    assert len(values) and np.isfinite(values).all()
    assert np.all(dates[1:] >= dates[:-1])
    result = np.empty(len(values), dtype=np.float64)
    bounds = np.r_[0, np.flatnonzero(dates[1:] != dates[:-1]) + 1, len(values)]
    for left, right in zip(bounds[:-1], bounds[1:]):
        result[left:right] = rankdata(values[left:right], method='average') / (right - left)
    return result


def historical_label_percentile(labels, dates):
    labels, dates = np.asarray(labels), np.asarray(dates)
    assert labels.ndim == dates.ndim == 1 and len(labels) == len(dates)
    result = np.full(len(labels), np.nan, dtype=np.float64)
    bounds = np.r_[0, np.flatnonzero(dates[1:] != dates[:-1]) + 1, len(labels)]
    for left, right in zip(bounds[:-1], bounds[1:]):
        finite = np.isfinite(labels[left:right])
        if finite.sum() >= 30:
            # The target uses only the historical official finite-label pool.
            result[left:right][finite] = rankdata(labels[left:right][finite], method='average') / (finite.sum() + 1.)
    return result


def fit(percentile, targets, flags, dates, exclusive_cutoff, bins, pseudocount):
    percentile, targets, flags, dates = map(np.asarray, (percentile, targets, flags, dates))
    assert bins in (8, 16, 32, 64, 128, 256) and pseudocount in (0., 50., 200., 1000.)
    mask = (dates < int(exclusive_cutoff)) & np.isfinite(targets)
    assert mask.any()
    centers = (np.arange(bins, dtype=np.float64) + .5) / bins
    index = np.minimum((percentile[mask] * bins).astype(np.int64), bins - 1)
    counts = np.bincount(index, minlength=bins).astype(np.float64)
    sums = np.bincount(index, weights=targets[mask], minlength=bins)
    used = counts > 0
    global_curve = IsotonicRegression(increasing=True, out_of_bounds='clip').fit(
        centers[used], sums[used] / counts[used], sample_weight=counts[used]).predict(centers)
    flagged = flags[mask] == 1
    flag_counts = np.bincount(index[flagged], minlength=bins).astype(np.float64)
    flag_sums = np.bincount(index[flagged], weights=targets[mask][flagged], minlength=bins)
    weights = flag_counts + float(pseudocount)
    flag_used = weights > 0
    if flag_used.any():
        flag_curve = IsotonicRegression(increasing=True, out_of_bounds='clip').fit(
            centers[flag_used],
            ((flag_sums + float(pseudocount) * global_curve) / np.maximum(weights, 1.))[flag_used],
            sample_weight=weights[flag_used]).predict(centers)
    else:
        flag_curve = global_curve.copy()
    assert np.all(np.diff(global_curve) >= 0) and np.all(np.diff(flag_curve) >= 0)
    last = int(dates[mask].max())
    assert last < int(exclusive_cutoff)
    return {'bins': bins, 'pseudocount_per_bin': float(pseudocount),
        'centers': centers.tolist(), 'global_curve': global_curve.tolist(),
        'flagged_curve': flag_curve.tolist(), 'historical_bin_counts': counts.tolist(),
        'historical_flagged_bin_counts': flag_counts.tolist(),
        'historical_finite_rows': int(mask.sum()), 'historical_flagged_rows': int(flagged.sum()),
        'last_training_label_date': last, 'exclusive_cutoff': int(exclusive_cutoff),
        'target': 'historical daily finite-label average rank divided by finite count plus one',
        'prediction_features': 'current complete-scheme daily percentile and supplied flag_limit_up only'}


def transform(raw, dates, flags, annual_models, weight, percentile=None):
    raw, dates, flags = map(np.asarray, (raw, dates, flags))
    assert raw.ndim == dates.ndim == flags.ndim == 1 and len(raw) == len(dates) == len(flags)
    assert np.isfinite(raw).all() and np.all((flags == 0) | (flags == 1))
    assert np.all(dates[1:] >= dates[:-1]) and 0 <= float(weight) <= 1
    if float(weight) == 0.:
        return raw.copy()
    percentile = daily_percentile(raw, dates) if percentile is None else np.asarray(percentile)
    assert len(percentile) == len(raw) and np.isfinite(percentile).all()
    output = raw.copy()
    for year in np.unique(dates // 10000):
        model = annual_models.get(str(int(year)))
        if model is None:
            continue  # First validation year has no preceding full-scheme OOF history.
        mask = dates // 10000 == year
        assert model['last_training_label_date'] < model['exclusive_cutoff'] < int(dates[mask].min())
        p = percentile[mask]
        common = np.interp(p, model['centers'], model['global_curve'])
        flagged = np.interp(p, model['centers'], model['flagged_curve'])
        output[mask] = common + float(weight) * (flags[mask] == 1) * (flagged - common) + EPSILON * p
    assert np.isfinite(output).all()
    return output
