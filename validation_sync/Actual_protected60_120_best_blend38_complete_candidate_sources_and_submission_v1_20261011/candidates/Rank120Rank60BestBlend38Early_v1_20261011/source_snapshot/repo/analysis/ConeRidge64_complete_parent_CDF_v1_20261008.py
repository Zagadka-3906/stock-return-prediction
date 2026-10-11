"""Ordered signed residual mixtures followed by the complete parent's daily CDF."""
import numpy as np

HEADS = ('cone_a010_positive', 'cone_a010_negative', 'cone_a100_positive', 'cone_a100_negative')
GROUPS = (((('cone_a010_positive',), 1.0), (('cone_a010_positive',), 1.0)), ((('cone_a010_positive',), -1.0), (('cone_a010_positive',), -1.0)), ((('cone_a010_negative',), 1.0), (('cone_a010_negative',), 1.0)), ((('cone_a010_negative',), -1.0), (('cone_a010_negative',), -1.0)), ((('cone_a100_positive',), 1.0), (('cone_a100_positive',), 1.0)), ((('cone_a100_positive',), -1.0), (('cone_a100_positive',), -1.0)), ((('cone_a100_negative',), 1.0), (('cone_a100_negative',), 1.0)), ((('cone_a100_negative',), -1.0), (('cone_a100_negative',), -1.0)))


def mixture(raw, group, share):
    assert group in range(len(GROUPS)) and share in (.25, .5, .75)
    parts = []
    for names, sign in GROUPS[group]:
        part = np.asarray(raw[names[0]], dtype=np.float64).copy()
        if len(names) == 2:
            part += np.asarray(raw[names[1]], dtype=np.float64)
            part /= 2.
        part *= sign
        parts.append(part)
    parts[0] *= float(share)
    parts[1] *= 1. - float(share)
    parts[0] += parts[1]
    assert np.isfinite(parts[0]).all()
    return parts[0]


def independent_mixture(raw, group, share):
    components = GROUPS[group]
    names0, sign0 = components[0]
    names1, sign1 = components[1]
    a = np.array(raw[names0[0]], dtype=np.float64, copy=True)
    b = np.array(raw[names1[0]], dtype=np.float64, copy=True)
    if len(names0) == 2:
        a = np.add(a, raw[names0[1]])
        a = np.divide(a, 2.)
    if len(names1) == 2:
        b = np.add(b, raw[names1[1]])
        b = np.divide(b, 2.)
    a = np.multiply(a, sign0)
    b = np.multiply(b, sign1)
    a = np.multiply(a, float(share))
    b = np.multiply(b, 1. - float(share))
    return np.add(a, b)


def prepare(parent, dates):
    parent = np.asarray(parent)
    dates = np.asarray(dates)
    assert parent.dtype == np.float64 and parent.ndim == dates.ndim == 1
    assert len(parent) == len(dates) and len(dates) and np.isfinite(parent).all()
    assert np.all(dates[1:] >= dates[:-1])
    boundaries = np.r_[0, np.flatnonzero(dates[1:] != dates[:-1])+1, len(dates)]
    result = []
    for left, right in zip(boundaries[:-1], boundaries[1:]):
        order = np.argsort(parent[left:right], kind='stable')
        ordered = parent[left:right][order]
        starts = np.r_[0, np.flatnonzero(ordered[1:] != ordered[:-1])+1]
        ends = np.r_[starts[1:], right-left]
        ranks = np.empty(right-left, dtype=np.float64)
        ranks[order] = np.repeat((starts+1+ends)/2., ends-starts)
        result.append((left, right, ranks/(right-left),
                       np.arange(1, right-left+1, dtype=np.float64)/(right-left), ordered))
    return result


def selected(dates, flags, valid):
    return (np.asarray(dates) >= 20210101) & (np.asarray(flags) != 1) & np.asarray(valid, dtype=bool)


def apply_prepared(parent, residual, dates, flags, valid, amplitude, prepared):
    assert np.isfinite(amplitude) and 0. <= amplitude <= .1
    residual = np.asarray(residual)
    assert residual.dtype == np.float64 and residual.shape == np.asarray(parent).shape
    assert np.isfinite(residual).all()
    values = np.array(parent, dtype=np.float64, copy=True)
    if amplitude == 0.:
        return values
    mask = selected(dates, flags, valid)
    for left, right, percentile, knots, ordered in prepared:
        pos = np.flatnonzero(mask[left:right])
        q = percentile[pos] + float(amplitude)*residual[left+pos]
        values[left+pos] = np.interp(np.clip(q, knots[0], knots[-1]), knots, ordered)
    return values


def transform(parent, residual, dates, flags, valid, amplitude):
    return apply_prepared(parent, residual, dates, flags, valid, amplitude, prepare(parent, dates))


def pandas_oracle(parent, residual, dates, flags, valid, amplitude):
    import pandas as pd
    result = np.array(parent, dtype=np.float64, copy=True)
    if amplitude == 0.:
        return result
    percentile = pd.Series(parent).groupby(dates, sort=False).rank(method='average', pct=True).to_numpy()
    # Express the preserved cohorts independently of selected().
    mask = (np.asarray(dates)//10000 > 2020) & (np.asarray(flags) != 1) & np.asarray(valid, dtype=bool)
    for positions in pd.Series(np.arange(len(dates))).groupby(dates, sort=False).indices.values():
        chosen = positions[mask[positions]]
        knots = np.arange(1, len(positions)+1, dtype=np.float64)/len(positions)
        q = percentile[chosen] + float(amplitude)*np.asarray(residual)[chosen]
        result[chosen] = np.interp(np.minimum(np.maximum(q, knots[0]), knots[-1]), knots,
                                  np.sort(np.asarray(parent)[positions], kind='stable'))
    return result
