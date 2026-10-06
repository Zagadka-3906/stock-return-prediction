"""Causal Top10 entry/exit buffer, preserving each day's score distribution.

The margin is in current eligible cross-sectional rank units. Prior selected
members receive that margin only for membership selection. Raw order inside
the resulting member/nonmember groups is retained. The output permutes the
same eligible raw values; flagged values are untouched. No labels are accepted.
"""
import numpy as np


def transform(raw, dates, flags, codes, margin, return_diagnostics=False):
    raw = np.asarray(raw, dtype=np.float64)
    dates, flags, codes = map(np.asarray, (dates, flags, codes))
    margin = float(margin)
    assert 0. <= margin <= 1.
    assert raw.ndim == dates.ndim == flags.ndim == codes.ndim == 1
    assert len(raw) == len(dates) == len(flags) == len(codes) and len(raw)
    assert np.isfinite(raw).all() and np.all(dates[1:] >= dates[:-1])
    assert np.issubdtype(codes.dtype, np.integer) and np.all(codes >= 0)
    assert np.all((flags == 0) | (flags == 1))
    result = raw.copy()
    previous = np.zeros(int(codes.max()) + 1, dtype=bool)
    previous_ids = None
    turns = []
    changed_days = replaced_members = eligible_days = 0
    bounds = np.r_[0, np.flatnonzero(dates[1:] != dates[:-1]) + 1, len(raw)]
    for start, end in zip(bounds[:-1], bounds[1:]):
        assert len(np.unique(codes[start:end])) == end - start
        index = np.arange(start, end)[flags[start:end] == 0]
        if len(index) < 100:
            previous.fill(False)
            previous_ids = None
            continue
        eligible_days += 1
        # Codes only resolve ties; their numeric magnitude is not a feature.
        order = np.lexsort((codes[index], -raw[index]))
        ranked = index[order]
        n_top = max(len(index) // 10, 1)
        baseline = ranked[:n_top]
        if margin > 0 and previous_ids is not None:
            ranks = 1. - np.arange(len(ranked), dtype=np.float64) / max(len(ranked) - 1, 1)
            priority = ranks + margin * previous[codes[ranked]]
            buffered = np.lexsort((codes[ranked], -ranks, -priority))[:n_top]
            # Keep the original raw order within the member/nonmember groups.
            selected_mask = np.zeros(len(ranked), dtype=bool)
            selected_mask[buffered] = True
            selected = ranked[selected_mask]
            if not np.array_equal(selected, baseline):
                changed_days += 1
                replaced_members += int(np.count_nonzero(~np.isin(codes[selected], codes[baseline])))
                rearranged = np.r_[selected, ranked[~selected_mask]]
                result[rearranged] = raw[ranked]
        else:
            selected = baseline
        current_ids = set(map(int, codes[selected]))
        if previous_ids is not None:
            turns.append(1. - len(current_ids & previous_ids) / len(current_ids | previous_ids))
        previous.fill(False)
        previous[codes[selected]] = True
        previous_ids = current_ids
    assert np.isfinite(result).all()
    if margin == 0.: assert np.array_equal(result, raw)
    diagnostics = {'margin': margin, 'eligible_days': eligible_days,
        'changed_membership_days': changed_days, 'total_replaced_baseline_members': replaced_members,
        'continuous_Jaccard_observations': len(turns),
        'continuous_Jaccard_mean_diagnostic': float(np.mean(turns)) if turns else None,
        'official_full8_metrics_not_computed_here': True, 'labels_used': False}
    return (result, diagnostics) if return_diagnostics else result
