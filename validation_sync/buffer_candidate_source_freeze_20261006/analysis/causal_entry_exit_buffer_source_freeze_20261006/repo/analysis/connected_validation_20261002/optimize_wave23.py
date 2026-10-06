"""Wave 23: a per-day retention floor driven by a causal day-level signal.

m has been a constant 0.985 since wave 10, and waves 13/17/19/20 all re-confirmed that constant as the
argmax. But a constant floor is a strong assumption: it says the right amount of forced retention is the
same on a day when the donor's ranking barely moved as on a day when it turned over completely. On a
stable day, keeping yesterday's names costs almost no excess, so a tighter floor is nearly free
turnover; on an unstable day, the same floor forces you to hold names the donor has already abandoned,
which is exactly the excess collapse seen as m rises past 0.985.

Two causal signals are tested. Both are computable on day t from information available on day t:
  rho   Spearman correlation between the donor's day-t and day-(t-1) cross-sections, over the codes
        eligible on both days. The donor's own predictions on both days are known at decision time.
  elig  |yesterday's realized Top decile that is still eligible today| / n_top. This is already computed
        inside the swap-budget solve as the pool size, and is a function of past predictions and past
        limit-up flags only.

The rule is a two-parameter family, not a per-day free choice:
    m_frac_t = clip(m_base + k * (signal_t - expanding_mean_of_signal_up_to_t-1), 0.95, 1.0)
The expanding mean keeps the centring strictly causal - it never sees day t or later - and two fitted
parameters over 1212 days is a different overfitting problem from 1212 free choices. It is still fitted
on the same five repeatedly viewed years and is disclosed as such.

Harness proof: k = 0 with m_base = 0.985 must reproduce 0.443190552 exactly, since the rule then
degenerates to the constant floor the selection was made on.

Selection is 后续选模标准.md §3/§4: highest connected 2020-2024 official composite, no other gate. The
bar for shipping is higher than the rule requires and is stated in the protocol: wave 20's top six arms
span 2.2e-4, so an adaptive floor that wins by less than that is indistinguishable from the plateau it
sits on. No test-period data is read anywhere in this file.
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
import connected_scorer as cs  # noqa: E402
from experiments.revalidate_fold_local import score_official  # noqa: E402
from optimize_wave15 import daily_ranks, weighted_rank_blend, DONOR, M_FRAC, TIE_EPS  # noqa: E402

W5A_A0B0 = "orderer_a0b0_W5a_five_way_with_gru__final_sweep_eval.npy"
SLOW16_A0B0 = "pp_a0_b0_top_only_w0.25_rl1_tcw1.npy"
PARTNER_WEIGHT = 0.25
CURRENT_BEST = 0.44319055217888365
PLATEAU_WIDTH = 2.2e-4
M_BASES = (0.983, 0.985, 0.987)
K_GRID = (-0.5, -0.2, 0.0, 0.2, 0.5, 1.0)
CLIP = (0.95, 1.0)


def sha(path) -> str:
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def donor_autocorrelation(donor: np.ndarray, dates: np.ndarray, flags: np.ndarray,
                          codes: np.ndarray) -> dict[int, float]:
    """Spearman correlation between the donor's day-t and day-(t-1) eligible cross-sections.

    Causal: reads only the donor's own predictions on two consecutive days and their limit-up flags.
    Day 0 has no predecessor and is absent from the returned map.
    """
    _, starts = np.unique(dates, return_index=True)
    ends = np.append(starts[1:], len(dates))
    out: dict[int, float] = {}
    prev_code: np.ndarray | None = None
    prev_val: np.ndarray | None = None
    for i, (start, end) in enumerate(zip(starts, ends)):
        rows = np.arange(start, end)
        eligible = rows[flags[start:end] == 0]
        c = codes[eligible]
        v = donor[eligible]
        if prev_code is not None and len(prev_code) >= 100 and len(c) >= 100:
            index = pd.Index(prev_code)
            pos = index.get_indexer(c)
            both = pos >= 0
            if both.sum() >= 100:
                rho = spearmanr(v[both], prev_val[pos[both]]).statistic
                if np.isfinite(rho):
                    out[i] = float(rho)
        prev_code, prev_val = c, v
    return out


def build_adaptive(base: np.ndarray, orderer: np.ndarray, dates: np.ndarray, flags: np.ndarray,
                   codes: np.ndarray, n_codes: int, m_fracs: np.ndarray) -> tuple[np.ndarray, dict]:
    """Wave 13's build_ab with a per-day retention fraction.

    `m_fracs` is indexed by day ordinal; days outside its range or with a non-finite entry fall back to
    the constant M_FRAC. Everything else - membership candidate set, exact swap-budget solve, slot
    reassignment, sentinel handling - is unchanged, so with a constant m_fracs this is build_ab.
    """
    out = orderer.copy()
    unique_days, starts = np.unique(dates, return_index=True)
    ends = np.append(starts[1:], len(dates))
    in_prev = np.zeros(n_codes, dtype=bool)
    in_cur = np.zeros(n_codes, dtype=bool)
    stats = {"days": 0, "retention": [], "boundary_tie_days": 0, "eligibility_limited_days": 0,
             "swaps": 0, "m_frac_used": []}
    have_prev = False
    for day_index, (start, end) in enumerate(zip(starts, ends)):
        rows = np.arange(start, end)
        eligible = rows[flags[start:end] == 0]
        if len(eligible) < 100:
            have_prev = False
            continue
        n_top = max(len(eligible) // 10, 1)
        m_frac = float(m_fracs[day_index]) if day_index < len(m_fracs) and np.isfinite(
            m_fracs[day_index]) else M_FRAC
        stats["m_frac_used"].append(m_frac)
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
                drop = not_held[np.argsort(scores[order[:n_top]][not_held], kind="stable")][:need]
                keep = np.setdiff1d(np.arange(n_top), drop, assume_unique=True)
                picked = set(codes[unconstrained[keep]].tolist())
                add = []
                for idx in np.argsort(-base[pool], kind="stable"):
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

        values = orderer[eligible]
        order_e = np.argsort(-values, kind="stable")
        sorted_values = values[order_e]
        chosen_local = np.isin(eligible, chosen)
        s_pos = order_e[chosen_local[order_e]]
        ns_pos = order_e[~chosen_local[order_e]]
        if len(s_pos) != n_top:
            raise AssertionError("slot reassignment size mismatch")
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
    used = np.array(stats["m_frac_used"], dtype=np.float64)
    stats["m_frac_used"] = {"n_days": int(len(used)), "min": float(used.min()),
                            "max": float(used.max()), "mean": float(used.mean()),
                            "std": float(used.std())}
    stats["retention"] = None
    return out, stats


def main() -> None:
    protocol_path = HERE / "protocol_wave23.json"
    if not protocol_path.exists():
        protocol_path.write_text(json.dumps({
            "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "standard": "后续选模标准.md §3 connected composite primary; §4 highest score wins",
            "status": "in_sample_selection_disclosed",
            "hypothesis": "a constant retention floor assumes the right amount of forced retention is "
                          "the same on a day the donor's ranking barely moved as on a day it turned "
                          "over. On stable days a tighter floor is nearly free turnover; on unstable "
                          "days the same floor holds abandoned names, which is the excess collapse seen "
                          "past m = 0.985.",
            "signals": {
                "rho": "Spearman between the donor's day-t and day-(t-1) eligible cross-sections",
                "elig": "|yesterday's realized Top still eligible today| / n_top, already computed "
                        "inside the solve",
            },
            "rule": "m_frac_t = clip(m_base + k*(signal_t - expanding_mean_of_signal_up_to_t-1), "
                    f"{CLIP[0]}, {CLIP[1]})",
            "causality_of_the_centring": "the expanding mean uses days strictly before t, so the rule "
                                         "never sees day t or later",
            "grid": {"m_base": list(M_BASES), "k": list(K_GRID)},
            "donor_fixed": {"column": DONOR, "provenance": "wave 13 stage 2 argmax"},
            "orderer_fixed": {"members": [W5A_A0B0, SLOW16_A0B0],
                              "weights": [1 - PARTNER_WEIGHT, PARTNER_WEIGHT],
                              "provenance": "wave 20 argmax over shippable arms"},
            "tie_break_eps": TIE_EPS,
            "harness_proof": f"k = 0 with m_base = 0.985 must reproduce {CURRENT_BEST} exactly, since "
                             "the rule then degenerates to the constant floor the selection was made on",
            "shipping_bar_higher_than_the_rule": f"wave 20's top six arms span {PLATEAU_WIDTH}, so an "
                                                 "adaptive floor winning by less than that is "
                                                 "indistinguishable from the plateau it sits on. §4 "
                                                 "requires only that it be highest; this protocol "
                                                 "records that a win inside the plateau width should "
                                                 "not be shipped.",
            "overfitting_disclosure": "two fitted parameters over 1212 days, on the same five "
                                      "repeatedly viewed years, with no blind period. The family is "
                                      "deliberately two-parameter rather than per-day free for that "
                                      "reason.",
            "current_best_before_this_wave": CURRENT_BEST,
            "selection_rule": "highest connected 2020-2024 official composite; no other gate",
            "no_test_period_data_read": True,
            "source_sha256": sha(Path(__file__)),
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        cs.log(f"wave-23 protocol frozen: {sha(protocol_path)[:16]}…")

    combined = cs.combined_frame()
    dates = combined["trade_date"].to_numpy()
    flags = combined["flag_limit_up"].to_numpy().astype(np.int64)
    valid = combined["price_valid"].to_numpy().astype(bool)
    codes, uniques = pd.factorize(combined["ts_code"].to_pandas(), sort=True)
    codes = codes.astype(np.int64)
    n_codes = len(uniques)
    tie_key = 1.0 - codes / max(n_codes - 1, 1)
    member = np.load(HERE / DONOR)

    w5a = np.load(HERE / W5A_A0B0)
    slow16 = np.load(HERE / SLOW16_A0B0)
    cache: dict = {}
    for stem, col in (("w5a", w5a), ("slow16", slow16)):
        cache[stem] = daily_ranks(col, valid, dates)
    blended = weighted_rank_blend([w5a, slow16], [1 - PARTNER_WEIGHT, PARTNER_WEIGHT], cache, valid,
                                  dates, ("w5a", "slow16"))
    orderer = np.where(blended > -9.0, blended + TIE_EPS * tie_key, blended)

    unique_days = np.unique(dates)
    n_days = len(unique_days)
    cs.log(f"{n_days} days, {len(combined):,} rows")

    # ---- signals
    rho_map = donor_autocorrelation(member, dates, flags, codes)
    rho = np.full(n_days, np.nan)
    for i, value in rho_map.items():
        rho[i] = value
    finite = np.isfinite(rho)
    cs.log(f"rho signal: {int(finite.sum())} of {n_days} days, mean {np.nanmean(rho):.6f}, "
           f"sd {np.nanstd(rho):.6f}, range [{np.nanmin(rho):.4f}, {np.nanmax(rho):.4f}]")

    # eligibility ratio, from the same loop the solve uses
    _, starts_idx = np.unique(dates, return_index=True)
    ends_idx = np.append(starts_idx[1:], len(dates))
    elig = np.full(n_days, np.nan)
    in_prev = np.zeros(n_codes, dtype=bool)
    in_cur = np.zeros(n_codes, dtype=bool)
    have_prev = False
    for day_index, (start, end) in enumerate(zip(starts_idx, ends_idx)):
        rows = np.arange(start, end)
        eligible = rows[flags[start:end] == 0]
        if len(eligible) < 100:
            have_prev = False
            continue
        n_top = max(len(eligible) // 10, 1)
        order = np.argsort(-member[eligible], kind="stable")
        top = eligible[order[:n_top]]
        if have_prev:
            elig[day_index] = int(in_prev[codes[top]].sum()) / n_top
        in_cur[:] = False
        in_cur[codes[top]] = True
        in_prev, in_cur = in_cur, in_prev
        have_prev = True
    cs.log(f"elig signal: {int(np.isfinite(elig).sum())} of {n_days} days, "
           f"mean {np.nanmean(elig):.6f}, sd {np.nanstd(elig):.6f}")

    def expanding_center(signal: np.ndarray) -> np.ndarray:
        """Mean of the signal over days strictly before t; NaN where no history exists."""
        out = np.full(len(signal), np.nan)
        total, count = 0.0, 0
        for i, value in enumerate(signal):
            out[i] = total / count if count else np.nan
            if np.isfinite(value):
                total += float(value)
                count += 1
        return out

    centers = {"rho": expanding_center(rho), "elig": expanding_center(elig)}

    results: dict = {}
    proofs: dict = {}

    def dump() -> list:
        arms = sorted(((v["connected_final_score"], k, v) for k, v in results.items()
                       if "connected_final_score" in v), reverse=True)
        payload = {"status": "running", "updated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
                   "purpose": "per-day adaptive retention floor from a causal day-level signal",
                   "rule": "m_frac_t = clip(m_base + k*(signal_t - expanding_mean_before_t), 0.95, 1.0)",
                   "donor_fixed": DONOR, "tie_break_eps": TIE_EPS,
                   "signal_stats": {"rho": {"days": int(np.isfinite(rho).sum()),
                                            "mean": float(np.nanmean(rho)),
                                            "sd": float(np.nanstd(rho))},
                                    "elig": {"days": int(np.isfinite(elig).sum()),
                                             "mean": float(np.nanmean(elig)),
                                             "sd": float(np.nanstd(elig))}},
                   "harness_proofs": proofs, "plateau_width": PLATEAU_WIDTH,
                   "current_best_before_this_wave": CURRENT_BEST,
                   "results": results, "n_scored": len(arms),
                   "ranking": [{"arm": k, "connected_final_score": s,
                                "ic_mean": v["connected_metrics"]["ic_mean"],
                                "annual_excess": v["connected_metrics"]["annual_excess"],
                                "mean_turnover": v["connected_metrics"]["mean_turnover"],
                                "margin_over_best": s - CURRENT_BEST,
                                "inside_plateau_width": bool(abs(s - CURRENT_BEST) < PLATEAU_WIDTH)}
                               for s, k, v in arms[:25]],
                   "best": arms[0][1] if arms else None,
                   "best_connected_final_score": arms[0][0] if arms else None,
                   "best_margin": (arms[0][0] - CURRENT_BEST) if arms else None,
                   "improves_beyond_plateau": bool(arms and arms[0][0] - CURRENT_BEST > PLATEAU_WIDTH),
                   "no_test_period_data_read": True,
                   "source_sha256": sha(Path(__file__))}
        (HERE / "wave23_results.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return arms

    def m_series(signal_name: str, m_base: float, k: float) -> np.ndarray:
        signal = rho if signal_name == "rho" else elig
        centre = centers[signal_name]
        deviation = np.where(np.isfinite(signal) & np.isfinite(centre), signal - centre, 0.0)
        return np.clip(m_base + k * deviation, CLIP[0], CLIP[1])

    def score(name: str, m_fracs: np.ndarray, extra: dict) -> float:
        hybrid, stats = build_adaptive(member, orderer + TIE_EPS * tie_key, dates, flags, codes,
                                       n_codes, m_fracs)
        metrics, _ = score_official(combined, hybrid)
        results[name] = {**extra, "connected_final_score": metrics["final_score"],
                         "connected_metrics": metrics, "boundary_tie_days": stats["boundary_tie_days"],
                         "eligibility_limited_days": stats["eligibility_limited_days"],
                         "swaps": stats["swaps"],
                         "mean_retention_ratio": stats["mean_retention_ratio"],
                         "m_frac_used": stats["m_frac_used"],
                         "margin_over_best": metrics["final_score"] - CURRENT_BEST}
        cs.log(f"{name[:46]:46s} CONNECTED {metrics['final_score']:.9f} "
               f"(ic {metrics['ic_mean']:.6f}, excess {metrics['annual_excess']:.6f}, "
               f"turn {metrics['mean_turnover']:.6f}) margin {metrics['final_score']-CURRENT_BEST:+.3e}")
        dump()
        return metrics["final_score"]

    # ---- harness proof: k = 0 at m_base = 0.985 is the constant floor
    got = score("P_constant_m0.985", np.full(n_days, M_FRAC),
                {"signal": "none", "m_base": M_FRAC, "k": 0.0, "role": "harness_proof"})
    proofs["P_k0_reproduces_the_constant_floor"] = {"scored": got, "expected": CURRENT_BEST,
                                                    "abs_diff": abs(got - CURRENT_BEST)}
    if abs(got - CURRENT_BEST) > 1e-12:
        raise AssertionError(f"harness proof failed: {got!r} vs {CURRENT_BEST!r}")
    cs.log("harness proof passed: k = 0 reproduces the constant-floor selection exactly")

    for signal_name in ("rho", "elig"):
        for m_base in M_BASES:
            for k in K_GRID:
                if k == 0.0 and m_base == M_FRAC:
                    continue
                score(f"{signal_name}_m{m_base:g}_k{k:+g}", m_series(signal_name, m_base, k),
                      {"signal": signal_name, "m_base": m_base, "k": k})

    arms = dump()
    payload = json.loads((HERE / "wave23_results.json").read_text(encoding="utf-8"))
    payload["status"] = "complete"
    payload["completed_at_local"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    (HERE / "wave23_results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("\n| rank | arm | CONNECTED | margin | IC | excess | turnover | m range |")
    print("|---|---|---|---|---|---|---|---|")
    for i, (s, name, v) in enumerate(arms[:20]):
        m = v["connected_metrics"]
        used = v["m_frac_used"]
        print(f"| {i+1} | {name[:28]} | **{s:.9f}** | {s - CURRENT_BEST:+.2e} | {m['ic_mean']:.6f} | "
              f"{m['annual_excess']:.6f} | {m['mean_turnover']:.6f} | "
              f"[{used['min']:.3f}, {used['max']:.3f}] |")
    best_margin = arms[0][0] - CURRENT_BEST if arms else 0.0
    cs.log(f"best: {arms[0][1] if arms else None} {arms[0][0] if arms else 0:.9f} "
           f"(margin {best_margin:+.3e}, plateau width {PLATEAU_WIDTH:.1e} -> "
           f"{'MEANINGFUL' if best_margin > PLATEAU_WIDTH else 'inside the plateau, not shippable'})")


if __name__ == "__main__":
    main()
