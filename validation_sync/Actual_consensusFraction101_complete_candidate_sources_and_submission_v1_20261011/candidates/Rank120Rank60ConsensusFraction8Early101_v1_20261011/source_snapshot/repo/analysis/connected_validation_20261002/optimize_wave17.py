"""Wave 17: the swap-budget solve picks WHICH names to swap using the donor's score. It could use the orderer's.

The retention floor solves, each day: keep at least m of yesterday's realized Top decile, and among the
sets that do so, take the one the donor likes best. Concretely it drops the `need` lowest-DONOR names
from today's unconstrained Top and adds the `need` highest-DONOR names from yesterday's Top that are
still eligible. Turnover depends only on how many names are retained, never on which ones, so every
rule that meets the floor gets the same turnover. Excess, however, reads the top len//10 of the label-
filtered universe ordered by the orderer A - and since every chosen row is assigned a value above every
non-chosen row, that is a prefix of the chosen set in A's order. So which names the solve swaps in and
out changes excess while leaving turnover untouched.

That is a free axis nobody has searched: every wave from 7b to 16 hard-coded "donor score" for both the
drop and the add. Choosing by A instead should raise excess at identical turnover, and a rank blend of
the two should sit in between. Drop and add are separable, so both orderings are tested.

Harness proof: the "base" rule must reproduce the current selection bit-for-bit, since it is wave 7b's
solve verbatim.

Selection is 后续选模标准.md §3/§4: highest connected 2020-2024 official composite, no other gate.
No test-period data is read anywhere in this file.
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
import connected_scorer as cs  # noqa: E402
from experiments.revalidate_fold_local import score_official  # noqa: E402
from optimize_wave15 import DONOR, M_FRAC, TIE_EPS, W5A_ORDERER, daily_ranks  # noqa: E402

CURRENT_BEST = 0.4424812067218111
CURRENT_BEST_NAME = "nested_x_W5a_a0_b0_m0.985_tiebreak"
# drop rule, add rule
RULES = [("base", "base"), ("orderer", "orderer"), ("rank", "rank"),
         ("base", "orderer"), ("orderer", "base"), ("base", "rank"), ("rank", "base")]
M_GRID = (0.98, 0.985, 0.99)


def sha(path) -> str:
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def build_swap(base: np.ndarray, orderer_top: np.ndarray, orderer_rest: np.ndarray,
               dates: np.ndarray, flags: np.ndarray, codes: np.ndarray, n_codes: int,
               m_frac: float, drop_key: np.ndarray, add_key: np.ndarray) -> tuple[np.ndarray, dict]:
    """Wave 13's build_ab with the swap-selection score parameterized.

    `drop_key` ranks today's unconstrained Top to decide which names leave it; `add_key` ranks
    yesterday's still-eligible Top members to decide which names enter. Both default to `base` in every
    earlier wave. The membership candidate set, the retention floor and the slot reassignment are
    unchanged, so with drop_key == add_key == base this is wave 13's build_ab exactly.
    """
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
                drop_scores = drop_key[eligible][order[:n_top]]
                drop = not_held[np.argsort(drop_scores[not_held], kind="stable")][:need]
                keep = np.setdiff1d(np.arange(n_top), drop, assume_unique=True)
                picked = set(codes[unconstrained[keep]].tolist())
                add = []
                for idx in np.argsort(-add_key[pool], kind="stable"):
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

        values = orderer_rest[eligible]
        order_e = np.argsort(-values, kind="stable")
        sorted_values = values[order_e]
        chosen_local = np.isin(eligible, chosen)
        s_pos = order_e[chosen_local[order_e]]
        ns_pos = order_e[~chosen_local[order_e]]
        if len(s_pos) != n_top:
            raise AssertionError("slot reassignment size mismatch")
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


def main() -> None:
    protocol_path = HERE / "protocol_wave17.json"
    if not protocol_path.exists():
        protocol_path.write_text(json.dumps({
            "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "standard": "后续选模标准.md §3 connected composite primary; §4 highest score wins",
            "status": "in_sample_selection_disclosed",
            "hypothesis": "turnover depends only on HOW MANY names are retained, never on WHICH, while "
                          "excess reads the chosen set in the orderer's order. So the swap-budget "
                          "solve's drop and add rules can be switched from the donor's score to the "
                          "orderer's, or to a rank blend, and should raise excess at identical "
                          "turnover. Waves 7b-16 all hard-coded the donor's score for both.",
            "donor_fixed": {"column": DONOR, "provenance": "wave 13 stage 2 argmax"},
            "orderer_fixed": {"column": W5A_ORDERER, "provenance": "wave 12 argmax; wave 15/16 blends "
                                                                   "are re-tested separately"},
            "m_grid": list(M_GRID),
            "rules": [{"drop": d, "add": a} for d, a in RULES],
            "harness_proof": f"drop=add=base at m={M_FRAC} must reproduce {CURRENT_BEST} exactly",
            "current_best_before_this_wave": {"name": CURRENT_BEST_NAME,
                                              "connected_final_score": CURRENT_BEST},
            "selection_rule": "highest connected 2020-2024 official composite; no significance, "
                              "worst-year or single-metric gate",
            "disclosed_selection_cost": "thirteenth consecutive search over the same five viewed years; "
                                        "no blind period remains and the winner carries upward "
                                        "selection bias this protocol cannot quantify",
            "causality": "the drop and add keys are day-t predictions (the donor's and the orderer's) "
                         "and the previous day's realized Top decile. No label is read.",
            "no_test_period_data_read": True,
            "source_sha256": sha(Path(__file__)),
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        cs.log(f"wave-17 protocol frozen: {sha(protocol_path)[:16]}…")

    combined = cs.combined_frame()
    dates = combined["trade_date"].to_numpy()
    flags = combined["flag_limit_up"].to_numpy().astype(np.int64)
    valid = combined["price_valid"].to_numpy().astype(bool)
    codes, uniques = pd.factorize(combined["ts_code"].to_pandas(), sort=True)
    codes = codes.astype(np.int64)
    n_codes = len(uniques)
    tie_key = 1.0 - codes / max(n_codes - 1, 1)

    member = np.load(HERE / DONOR)
    orderer = np.load(HERE / f"{W5A_ORDERER}.npy") + TIE_EPS * tie_key
    # the rank key must be comparable in scale to the donor's own values, so use the per-day normalized
    # rank rescaled onto the donor's range; only the ORDER of the key is used, so the rescaling is
    # cosmetic and keeps the array finite and sentinel-free where the donor is
    ranks = daily_ranks(orderer, valid, dates)
    rank_key = np.where(ranks > -9.0, ranks, -1.0)
    keys = {"base": member, "orderer": orderer, "rank": rank_key}

    results: dict = {}
    proofs: dict = {}

    def dump() -> list:
        arms = sorted(((v["connected_final_score"], k, v) for k, v in results.items()
                       if "connected_final_score" in v), reverse=True)
        payload = {"status": "running", "updated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
                   "purpose": "search the swap-budget solve's drop and add rules",
                   "donor_fixed": DONOR, "orderer_fixed": W5A_ORDERER, "tie_break_eps": TIE_EPS,
                   "harness_proofs": proofs,
                   "current_best_before_this_wave": {"name": CURRENT_BEST_NAME,
                                                     "connected_final_score": CURRENT_BEST},
                   "results": results, "n_scored": len(arms),
                   "ranking": [{"arm": k, "connected_final_score": s,
                                "ic_mean": v["connected_metrics"]["ic_mean"],
                                "annual_excess": v["connected_metrics"]["annual_excess"],
                                "mean_turnover": v["connected_metrics"]["mean_turnover"],
                                "swaps": v["swaps"]} for s, k, v in arms[:25]],
                   "best": arms[0][1] if arms else None,
                   "best_connected_final_score": arms[0][0] if arms else None,
                   "improves_on_current_best": bool(arms and arms[0][0] > CURRENT_BEST),
                   "no_test_period_data_read": True,
                   "source_sha256": sha(Path(__file__))}
        (HERE / "wave17_results.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return arms

    # ---- harness proof: the base rule at m = 0.985 must reproduce the shipped number
    ref, ref_stats = build_swap(member, orderer, orderer, dates, flags, codes, n_codes, M_FRAC,
                                member, member)
    from optimize_wave13 import build_ab
    ref2, _ = build_ab(member, orderer, orderer, dates, flags, codes, n_codes, M_FRAC)
    proofs["P_base_rule_equals_wave13"] = {
        "bit_identical": bool(np.array_equal(ref, ref2)),
        "max_abs_diff": float(np.abs(ref - ref2).max())}
    if not np.array_equal(ref, ref2):
        raise AssertionError(f"harness proof failed: the base rule is not wave 13's build_ab "
                             f"(max diff {proofs['P_base_rule_equals_wave13']['max_abs_diff']:.3e})")
    metrics, _ = score_official(combined, ref)
    proofs["P_base_rule_score"] = {"scored": metrics["final_score"], "expected": CURRENT_BEST,
                                   "abs_diff": abs(metrics["final_score"] - CURRENT_BEST)}
    if abs(metrics["final_score"] - CURRENT_BEST) > 1e-12:
        raise AssertionError(f"harness proof failed: base rule scored {metrics['final_score']!r}, "
                             f"expected {CURRENT_BEST!r}")
    cs.log(f"harness proof passed: drop=add=base reproduces wave 13's array bit-for-bit and scores "
           f"{metrics['final_score']:.9f}")

    for drop_rule, add_rule in RULES:
        for m_frac in M_GRID:
            name = f"drop_{drop_rule}__add_{add_rule}__m{m_frac:g}"
            try:
                hybrid, stats = build_swap(member, orderer, orderer, dates, flags, codes, n_codes,
                                           m_frac, keys[drop_rule], keys[add_rule])
                m, _ = score_official(combined, hybrid)
                results[name] = {"drop_rule": drop_rule, "add_rule": add_rule, "m_frac": m_frac,
                                 "connected_final_score": m["final_score"], "connected_metrics": m,
                                 "boundary_tie_days": stats["boundary_tie_days"],
                                 "eligibility_limited_days": stats["eligibility_limited_days"],
                                 "swaps": stats["swaps"],
                                 "mean_retention_ratio": stats["mean_retention_ratio"],
                                 "beats_current_best": bool(m["final_score"] > CURRENT_BEST)}
                cs.log(f"{name[:52]:52s} CONNECTED {m['final_score']:.9f} "
                       f"(ic {m['ic_mean']:.6f}, excess {m['annual_excess']:.6f}, "
                       f"turn {m['mean_turnover']:.6f}, swaps {stats['swaps']})")
                dump()
            except BaseException as error:  # noqa: BLE001
                results[name] = {"drop_rule": drop_rule, "add_rule": add_rule, "m_frac": m_frac,
                                 "error": f"{type(error).__name__}: {error}"}
                cs.log(f"{name[:52]:52s} FAILED {type(error).__name__}: {error}")
                dump()

    arms = dump()
    payload = json.loads((HERE / "wave17_results.json").read_text(encoding="utf-8"))
    payload["status"] = "complete"
    payload["completed_at_local"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    (HERE / "wave17_results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("\n| rank | arm | CONNECTED | IC | excess | turnover | swaps |")
    print("|---|---|---|---|---|---|---|")
    for i, (s, name, v) in enumerate(arms[:20]):
        m = v["connected_metrics"]
        print(f"| {i+1} | {name[:44]} | **{s:.9f}** | {m['ic_mean']:.6f} | {m['annual_excess']:.6f} "
              f"| {m['mean_turnover']:.6f} | {v['swaps']} |")
    cs.log(f"best: {arms[0][1] if arms else None} {arms[0][0] if arms else 0:.9f} "
           f"({'IMPROVES' if arms and arms[0][0] > CURRENT_BEST else 'does not improve'})")


if __name__ == "__main__":
    main()
