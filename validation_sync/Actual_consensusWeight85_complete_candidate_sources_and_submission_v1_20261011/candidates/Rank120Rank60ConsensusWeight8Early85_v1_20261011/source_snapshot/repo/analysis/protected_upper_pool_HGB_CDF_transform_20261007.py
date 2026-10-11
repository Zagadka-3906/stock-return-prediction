"""Day-local lower-pool reordering using saved heads, with upper forecasts unchanged."""
import numpy as np


def percentile(values):
    values = np.asarray(values, dtype=np.float64)
    assert values.ndim == 1 and np.isfinite(values).all()
    if not len(values):
        return np.empty(0, dtype=np.float64)
    order = np.argsort(values, kind='stable')
    sorted_values = values[order]
    starts = np.r_[0, np.flatnonzero(sorted_values[1:] != sorted_values[:-1]) + 1]
    ends = np.r_[starts[1:], len(values)]
    ranks = np.repeat((starts + 1 + ends) / (2. * len(values)), ends - starts)
    result = np.empty(len(values), dtype=np.float64)
    result[order] = ranks
    return result


def prepare(parent, dates, flags, valid, lower_fraction):
    parent = np.asarray(parent, dtype=np.float64)
    dates, flags, valid = (np.asarray(x) for x in (dates, flags, valid))
    assert all(x.ndim == 1 and x.shape == parent.shape for x in (parent, dates, flags, valid))
    assert 0. < float(lower_fraction) < 1.
    assert np.all(dates[1:] >= dates[:-1]), 'Sorted, complete date groups required'
    starts = np.r_[0, np.flatnonzero(dates[1:] != dates[:-1]) + 1] if len(dates) else []
    ends = np.r_[starts[1:], len(dates)] if len(dates) else []
    prepared = []
    for left, right in zip(starts, ends):
        positions = np.arange(left, right)
        pool = positions[(flags[left:right] == 0) & valid[left:right].astype(bool)
            & np.isfinite(parent[left:right]) & (parent[left:right] > -9)]
        if len(pool) < 3:
            continue
        ordered_pool = np.sort(parent[pool], kind='stable')
        index = min(len(pool) - 1, max(1, int(np.floor(float(lower_fraction) * len(pool)))))
        boundary = ordered_pool[index]
        # Keep the entire boundary tie group unchanged, rather than splitting ties.
        selected = pool[parent[pool] < boundary]
        if len(selected) < 2:
            continue
        ordered = np.sort(parent[selected], kind='stable')
        prepared.append((selected, percentile(parent[selected]),
            (np.arange(len(selected), dtype=np.float64) + 1.) / len(selected), ordered))
    return prepared


def prepare_heads(heads, prepared):
    heads = [np.asarray(x, dtype=np.float64) for x in heads]
    assert heads and all(x.ndim == 1 and x.shape == heads[0].shape for x in heads)
    result = []
    for positions, _, _, _ in prepared:
        combined = np.zeros(len(positions), dtype=np.float64)
        for head in heads:
            combined += percentile(head[positions])
        result.append(combined / len(heads))
    return result


def apply_prepared(parent, weight, prepared, head_percentiles):
    parent = np.asarray(parent, dtype=np.float64)
    assert parent.ndim == 1 and 0. <= float(weight) <= 1.
    assert len(prepared) == len(head_percentiles)
    output = parent.copy()
    if float(weight) == 0.:
        return output
    for (positions, p, knots, ordered), h in zip(prepared, head_percentiles):
        assert np.asarray(h).shape == p.shape and np.isfinite(h).all()
        q = (1. - float(weight)) * p + float(weight) * h
        output[positions] = np.interp(np.clip(q, knots[0], knots[-1]), knots, ordered)
    return output


def transform(parent, dates, flags, valid, heads, weight, lower_fraction):
    prepared = prepare(parent, dates, flags, valid, lower_fraction)
    assert all(np.asarray(head).shape == np.asarray(parent).shape for head in heads)
    return apply_prepared(parent, weight, prepared, prepare_heads(heads, prepared))
