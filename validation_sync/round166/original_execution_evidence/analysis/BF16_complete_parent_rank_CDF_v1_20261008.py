"""Full-parent/new-neural rank mixing, including2020; only the declared valid cohort changes."""
import numpy as np

ROLES = ('all_valid', 'nonflag_valid', 'flag_valid')


def prepare(parent, neural, dates, flags, valid):
    parent, neural = np.asarray(parent), np.asarray(neural)
    dates, flags, valid = np.asarray(dates), np.asarray(flags), np.asarray(valid, dtype=bool)
    assert parent.dtype == neural.dtype == np.float64
    assert parent.ndim == neural.ndim == dates.ndim == flags.ndim == valid.ndim == 1
    assert len(parent) == len(neural) == len(dates) == len(flags) == len(valid)
    assert np.isfinite(parent).all() and np.isfinite(neural).all()
    assert len(dates) and np.all(dates[1:] >= dates[:-1])
    boundaries = np.r_[0, np.flatnonzero(dates[1:] != dates[:-1])+1, len(dates)]
    result = []
    for left, right in zip(boundaries[:-1], boundaries[1:]):
        percentiles = []
        for values in (parent[left:right], neural[left:right]):
            order = np.argsort(values, kind='stable')
            ordered = values[order]
            starts = np.r_[0, np.flatnonzero(ordered[1:] != ordered[:-1])+1]
            ends = np.r_[starts[1:], right-left]
            ranks = np.empty(right-left, dtype=np.float64)
            ranks[order] = np.repeat((starts+1+ends)/2., ends-starts)
            percentiles.append(ranks/(right-left))
        result.append((left, right, percentiles[0], percentiles[1],
                       np.arange(1, right-left+1, dtype=np.float64)/(right-left),
                       np.sort(parent[left:right], kind='stable')))
    return result


def selected(flags, valid, role):
    assert role in ROLES
    valid = np.asarray(valid, dtype=bool)
    if role == 'all_valid':return valid
    if role == 'nonflag_valid':return valid & (np.asarray(flags) != 1)
    return valid & (np.asarray(flags) == 1)


def apply_prepared(parent, flags, valid, role, weight, prepared):
    assert np.isfinite(weight) and 0. <= weight <= 1.
    values = np.asarray(parent, dtype=np.float64).copy()
    if weight == 0.:return values
    cohort = selected(flags, valid, role)
    for left, right, parent_pct, neural_pct, knots, ordered in prepared:
        positions = np.flatnonzero(cohort[left:right])
        q = (1.-float(weight))*parent_pct[positions] + float(weight)*neural_pct[positions]
        values[left+positions] = np.interp(np.clip(q, knots[0], knots[-1]), knots, ordered)
    return values


def transform(parent, neural, dates, flags, valid, role, weight):
    return apply_prepared(parent, flags, valid, role, weight, prepare(parent, neural, dates, flags, valid))


def pandas_oracle(parent, neural, dates, flags, valid, role, weight):
    import pandas as pd
    assert role in ROLES and 0. <= weight <= 1.
    result = np.asarray(parent, dtype=np.float64).copy()
    if weight == 0.:return result
    pp = pd.Series(parent).groupby(dates, sort=False).rank(method='average', pct=True).to_numpy()
    npct = pd.Series(neural).groupby(dates, sort=False).rank(method='average', pct=True).to_numpy()
    valid = np.asarray(valid, dtype=bool)
    mask = valid if role == 'all_valid' else (valid & ((np.asarray(flags) == 1) if role == 'flag_valid' else (np.asarray(flags) != 1)))
    groups = pd.Series(np.arange(len(dates), dtype=np.int64)).groupby(dates, sort=False).indices
    for positions in groups.values():
        chosen = positions[mask[positions]]
        knots = np.arange(1, len(positions)+1, dtype=np.float64)/len(positions)
        q = (1.-float(weight))*pp[chosen] + float(weight)*npct[chosen]
        result[chosen] = np.interp(np.minimum(np.maximum(q, knots[0]), knots[-1]), knots,
                                  np.sort(np.asarray(parent)[positions], kind='stable'))
    return result

