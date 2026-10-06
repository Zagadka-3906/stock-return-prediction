"""Causal same-day CDF routing, with reusable immutable per-day sorting."""
import numpy as np


def prepare(raw, dates, flags, price_valid, universe):
    raw, dates, flags, price_valid = map(np.asarray, (raw, dates, flags, price_valid))
    assert raw.ndim == dates.ndim == flags.ndim == price_valid.ndim == 1
    assert len(raw) == len(dates) == len(flags) == len(price_valid)
    assert np.isfinite(raw).all()
    assert universe in ('all_current_raw_forecasts', 'current_price_valid_forecasts_only')
    days, starts = np.unique(dates, return_index=True)
    ends = np.r_[starts[1:], len(raw)]
    assert np.all(np.diff(dates) >= 0)
    result = []
    for day, left, right in zip(days, starts, ends):
        pool = raw[left:right] if universe == 'all_current_raw_forecasts' else raw[left:right][price_valid[left:right]]
        assert len(pool), 'A current-day valid CDF requires a nonempty current pool'
        ordered = np.sort(pool, kind='stable')
        positions = np.flatnonzero(flags[left:right] == 1) + left
        values = raw[positions]
        lo = np.searchsorted(ordered, values, side='left')
        hi = np.searchsorted(ordered, values, side='right')
        # Average rank/N for values in the pool; insertion CDF lo/N for values
        # outside the price-valid pool. Neither uses any return label.
        percentile = np.where(hi > lo, (lo + hi + 1.) / (2. * len(pool)), lo / len(pool))
        knots = np.arange(1, len(pool) + 1, dtype=np.float64) / len(pool)
        for array in (positions, ordered, percentile, knots):
            array.flags.writeable = False
        result.append((int(day), positions, percentile, knots, ordered))
    return result


def apply_prepared(raw, centered_prediction, weight, prepared):
    raw, centered_prediction = np.asarray(raw), np.asarray(centered_prediction)
    assert raw.shape == centered_prediction.shape and np.isfinite(centered_prediction).all()
    assert 0. <= float(weight) <= 1.
    output = raw.astype(np.float64, copy=True)
    if float(weight) == 0.:
        return output
    for _, positions, percentile, knots, ordered in prepared:
        q = (1. - float(weight)) * percentile + float(weight) * (centered_prediction[positions] + .5)
        output[positions] = np.interp(np.clip(q, knots[0], knots[-1]), knots, ordered)
    assert np.isfinite(output).all()
    return output


def transform(raw, dates, flags, price_valid, centered_prediction, weight, universe):
    return apply_prepared(raw, centered_prediction, weight,
        prepare(raw, dates, flags, price_valid, universe))
