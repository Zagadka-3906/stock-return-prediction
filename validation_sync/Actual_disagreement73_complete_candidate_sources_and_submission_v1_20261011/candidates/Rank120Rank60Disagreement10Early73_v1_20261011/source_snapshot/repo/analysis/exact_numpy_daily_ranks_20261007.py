"""Day-local average ranks; unsupported layouts retain the original implementation.

This operator changes execution only. The usable subset and sentinel follow
connected_validation_20261002/optimize_wave15.py exactly.
"""
from functools import wraps
import sys
import types
import numpy as np


class DaywiseNumpyRanks:
    def __init__(self, original):
        self.original = original
        self.fast_calls = self.fallback_calls = self.empty_calls = 0

    def __call__(self, values, valid, dates):
        values, valid, dates = map(np.asarray, (values, valid, dates))
        supported = (
            values.ndim == valid.ndim == dates.ndim == 1
            and values.shape == valid.shape == dates.shape
            and values.dtype.kind == 'f'
            and values.dtype.itemsize in (4, 8)
            and valid.dtype == np.dtype(bool)
            and dates.dtype.kind in 'iu'
            and np.all(dates[1:] >= dates[:-1])
        )
        if not supported:
            self.fallback_calls += 1
            return self.original(values, valid, dates)
        self.fast_calls += 1
        result = np.full(len(values), -10.0, dtype=np.float64)
        keep = valid & np.isfinite(values) & (values > -9.0)
        if not keep.any():
            self.empty_calls += 1
            return result
        boundaries = np.r_[0, np.flatnonzero(dates[1:] != dates[:-1]) + 1, len(dates)]
        for left, right in zip(boundaries[:-1], boundaries[1:]):
            positions = np.flatnonzero(keep[left:right])
            count = len(positions)
            if not count:
                continue
            selected = values[left:right][positions]
            order = np.argsort(selected, kind='stable')
            ordered = selected[order]
            starts = np.r_[0, np.flatnonzero(ordered[1:] != ordered[:-1]) + 1]
            ends = np.r_[starts[1:], count]
            average = (starts + 1 + ends) / 2.0
            ranks = np.empty(count, dtype=np.float64)
            ranks[order] = np.repeat(average, ends - starts)
            result[left + positions] = ranks / count
        return result

    def statistics(self):
        return {'fast_calls': self.fast_calls, 'fallback_calls': self.fallback_calls,
                'empty_calls': self.empty_calls,
                'usable_subset_valid_finite_and_greater_than_minus9': True,
                'unsupported_layout_uses_original_function': True,
                'tie_method': 'average', 'normalization': 'usable_count_per_day',
                'sentinel': -10.0, 'retained_full_prediction_cache_bytes': 0}


def install():
    import optimize_wave15 as ranks
    original = ranks.daily_ranks
    operator = DaywiseNumpyRanks(original)

    @wraps(original)
    def replacement(values, valid, dates):
        return operator(values, valid, dates)

    bindings = []
    for module in tuple(sys.modules.values()):
        if isinstance(module, types.ModuleType):
            for name, value in tuple(vars(module).items()):
                if value is original:
                    setattr(module, name, replacement)
                    bindings.append((module, name))
    assert (ranks, 'daily_ranks') in bindings

    def restore():
        for module, name in reversed(bindings):
            assert getattr(module, name) is replacement
            setattr(module, name, original)
        return operator.statistics()

    return operator, restore
