"""R10 selector, adapted from frozen wave13; zero-priority equivalence is audited."""
import numpy as np

def build_priority(base: np.ndarray, orderer_top: np.ndarray, orderer_rest: np.ndarray, dates: np.ndarray,
             flags: np.ndarray, codes: np.ndarray, n_codes: int,
             m_frac: float, add_scores: np.ndarray, drop_scores: np.ndarray) -> tuple[np.ndarray, dict]:
    """Wave 7b's swap-budget construction with the orderer's two roles split.

    Unconstrained membership uses base; retention additions/removals use separate priorities. Then the
    eligible rows' own values - taken from `orderer_rest`, so the multiset is preserved - are
    reassigned: the chosen set receives the n_top largest, ordered among themselves by `orderer_top`,
    and the remaining eligible rows receive the rest in `orderer_rest` order. Ineligible rows are
    untouched, because limit-up names sit inside the Rank IC universe.
    """
    assert len(add_scores) == len(drop_scores) == len(base)
    assert np.isfinite(add_scores).all() and np.isfinite(drop_scores).all()
    out = orderer_rest.copy()
    _, starts = np.unique(dates, return_index=True)
    ends = np.append(starts[1:], len(dates))
    in_prev = np.zeros(n_codes, dtype=bool)
    in_cur = np.zeros(n_codes, dtype=bool)
    stats = {"days": 0, "m_frac": m_frac, "retention": [], "boundary_tie_days": 0,
             "eligibility_limited_days": 0, "swaps": 0}
    have_prev = False
    for start, end in zip(starts, ends):
        rows = np.arange(start, end)
        eligible = rows[flags[start:end] == 0]
        if len(eligible) < 100:
            have_prev = False
            continue
        n_top = max(len(eligible) // 10, 1)
        m = int(round(m_frac * n_top))
        scores = base[eligible]
        order = np.argsort(-scores, kind="stable")
        unconstrained = eligible[order[:n_top]]
        if not have_prev or m == 0:
            chosen = unconstrained
        else:
            pool = eligible[in_prev[codes[eligible]]]
            if len(pool) < m:
                stats["eligibility_limited_days"] += 1
                m = len(pool)
            held = in_prev[codes[unconstrained]]
            r = int(held.sum())
            if r >= m:
                chosen = unconstrained
            else:
                need = m - r
                not_held = np.flatnonzero(~held)
                drop = not_held[np.argsort(drop_scores[unconstrained][not_held], kind="stable")][:need]
                keep = np.setdiff1d(np.arange(n_top), drop, assume_unique=True)
                picked = set(codes[unconstrained[keep]].tolist())
                add = []
                for idx in np.argsort(-add_scores[pool], kind="stable"):
                    if len(add) >= need:
                        break
                    code = codes[pool[idx]]
                    if code in picked:
                        continue
                    add.append(int(pool[idx]))
                    picked.add(code)
                if len(add) != need:
                    raise AssertionError("swap budget could not be met")
                chosen = np.concatenate([unconstrained[keep], np.array(add, dtype=np.int64)])
                stats["swaps"] += need
        if len(chosen) != n_top or len(np.unique(codes[chosen])) != n_top:
            raise AssertionError("chosen set is not exactly n_top distinct names")

        if have_prev:
            assert int(in_prev[codes[chosen]].sum()) >= m, "retention floor violated"

        values = orderer_rest[eligible]
        order_e = np.argsort(-values, kind="stable")
        sorted_values = values[order_e]
        chosen_local = np.isin(eligible, chosen)
        s_pos = order_e[chosen_local[order_e]]
        ns_pos = order_e[~chosen_local[order_e]]
        if len(s_pos) != n_top:
            raise AssertionError("slot reassignment size mismatch")
        # order the chosen slots by orderer_top instead; ns_pos is already orderer_rest-descending
        a_vals = orderer_top[eligible][s_pos]
        s_pos = s_pos[np.argsort(-a_vals, kind="stable")]
        if n_top < len(sorted_values) and sorted_values[n_top - 1] == sorted_values[n_top]:
            stats["boundary_tie_days"] += 1
        new_values = np.empty_like(values)
        new_values[s_pos] = sorted_values[:n_top]
        new_values[ns_pos] = sorted_values[n_top:]
        out[eligible] = new_values

        stats["days"] += 1
        stats["retention"].append(int(in_prev[codes[chosen]].sum()) / n_top if have_prev else np.nan)
        in_cur[:] = False
        in_cur[codes[chosen]] = True
        in_prev, in_cur = in_cur, in_prev
        have_prev = True
    if not np.isfinite(out).all():
        raise AssertionError("non-finite prediction")
    known = np.array([r for r in stats["retention"] if not np.isnan(r)])
    stats["mean_retention_ratio"] = float(known.mean()) if len(known) else None
    stats["retention"] = None
    return out, stats
