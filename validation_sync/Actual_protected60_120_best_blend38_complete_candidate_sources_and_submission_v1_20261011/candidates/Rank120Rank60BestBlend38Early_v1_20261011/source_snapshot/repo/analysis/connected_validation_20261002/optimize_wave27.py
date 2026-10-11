"""Wave 27: make the orderer blend weights adaptive, using trailing IC that is causal.

Every blend weight in this project has been a constant fitted once over the whole window: wave 16 gridded
a single partner weight and wave 20 confirmed 0.25. A constant weight says the relative merit of W5a and
slow16 never changes across 1212 days and two very different market regimes - and this project has
already measured that it does change, which is exactly why the 48-candidate transfer study found
Spearman -0.7477 between the 2020-2022 and 2023-2024 halves, and why wave 26 finds that every m
refinement wins the first half and loses the second.

The standard fix is adaptive ensemble weighting, and it is available here without reading anything
illegal: on day t the labels for days up to t-1 are realized returns, known at decision time. So each
component's trailing rank-IC over [t-W, t-1] is a strictly causal statistic, and weighting components by
it is not selection on the scored day's label. The lag is the whole point and it is enforced by
construction - the trailing window for day t ends at t-1 and the code raises if it does not.

Rule, with shrinkage so the constant blend is a nested special case:
    a_i(t) = max(trailing_IC_i(t), 0) ** p              (0 if the window has no history)
    adaptive_i(t) = a_i(t) / sum_j a_j(t), or the fixed weight if sum_j a_j(t) == 0
    w_i(t) = (1 - lambda) * fixed_i + lambda * adaptive_i(t)
lambda = 0 must reproduce the shipped constant blend exactly, which is the harness proof.

Two safeguards are declared in advance rather than chosen after seeing the result:
  * the shipping rule is the one wave 26 used - beat the reference on the FULL window AND on BOTH
    halves. Waves 23/25/26 all produced full-window gains that were pure redistribution across halves,
    so a full-window-only win is not evidence here.
  * W, p and lambda are gridded, but the trailing-IC statistic itself has no free parameters: it is the
    component's own realized rank-IC, the same quantity the official metric's first term measures.

Selection is 后续选模标准.md §3/§4 for the recorded ranking; the both-halves rule governs the shipping
recommendation only. No test-period data is read anywhere in this file.
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import polars as pl
from scipy.stats import spearmanr

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
import connected_scorer as cs  # noqa: E402
from experiments.revalidate_fold_local import score_official  # noqa: E402
from optimize_wave13 import build_ab  # noqa: E402
from optimize_wave15 import daily_ranks, DONOR, M_FRAC, TIE_EPS  # noqa: E402

YEARS = cs.YEARS
COMPONENTS = ["orderer_a0b0_W5a_five_way_with_gru__final_sweep_eval.npy",
              "pp_a0_b0_top_only_w0.25_rl1_tcw1.npy"]
FIXED_WEIGHTS = [0.75, 0.25]
WINDOWS = (10, 20, 40, 60)
POWERS = (1.0, 2.0)
LAMBDAS = (0.0, 0.5, 1.0)
REFERENCE = 0.44319055217888365
REF_HALF_DEV = 0.442705356
REF_HALF_CONF = 0.443926938


def sha(path) -> str:
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def daily_ic_series(values: np.ndarray, dates: np.ndarray, y: np.ndarray,
                    starts: np.ndarray, ends: np.ndarray) -> np.ndarray:
    """Per-day rank IC of one component against realized returns, NaN where not computable.

    Uses the official IC universe: rows with a non-null label, limit-up rows INCLUDED, day skipped when
    fewer than 30 rows survive. NaN days are skipped by the trailing window rather than treated as zero.
    """
    out = np.full(len(starts), np.nan)
    finite = np.isfinite(y)
    for i, (start, end) in enumerate(zip(starts, ends)):
        rows = np.arange(start, end)
        use = rows[finite[start:end]]
        if len(use) < 30:
            continue
        rho = spearmanr(values[use], y[use]).statistic
        if np.isfinite(rho):
            out[i] = float(rho)
    return out


def trailing_mean(series: np.ndarray, window: int) -> np.ndarray:
    """Mean of series over [t-window, t-1]. Strictly causal: day t is never included."""
    n = len(series)
    out = np.full(n, np.nan)
    for t in range(n):
        lo = max(0, t - window)
        if lo >= t:
            continue
        chunk = series[lo:t]
        known = chunk[np.isfinite(chunk)]
        if len(known):
            out[t] = float(known.mean())
    if n > window and np.isfinite(series[:window]).any():
        # a self-check that the window never touches t: recomputing t=window must exclude index window
        lo, hi = max(0, window - window), window
        manual = series[lo:hi]
        manual = manual[np.isfinite(manual)]
        if len(manual) and abs(float(manual.mean()) - out[window]) > 1e-12:
            raise AssertionError("trailing_mean window is not [t-window, t-1]")
    return out


def blend_daily_weights(ranks: list[np.ndarray], weight_rows: np.ndarray, valid: np.ndarray,
                        usable: list[np.ndarray]) -> np.ndarray:
    """Per-day weighted rank blend where the weights vary by day.

    weight_rows is (n_rows, n_components) and already normalized per row. Rows where any component is
    unusable get the sentinel, matching weighted_rank_blend's convention.
    """
    acc = np.zeros(len(valid), dtype=np.float64)
    norm = np.zeros(len(valid), dtype=np.float64)
    keep = valid.copy()
    for r, u, w_col in zip(ranks, usable, weight_rows.T):
        acc += np.where(u, w_col * r, 0.0)
        norm += np.where(u, w_col, 0.0)
        keep &= u
    out = np.full(len(valid), -10.0, dtype=np.float64)
    good = keep & (norm > 0)
    out[good] = acc[good] / norm[good]
    return out


def main() -> None:
    protocol_path = HERE / "protocol_wave27.json"
    if not protocol_path.exists():
        protocol_path.write_text(json.dumps({
            "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "standard": "后续选模标准.md §3 connected composite primary; §4 highest score wins",
            "status": "in_sample_selection_disclosed",
            "hypothesis": "the orderer blend weight has always been a single constant fitted over the "
                          "whole window, which asserts that W5a and slow16 have constant relative merit "
                          "across 1212 days and two regimes. The project has already measured that "
                          "rankings move between halves (Spearman -0.7477 over 48 candidates; every m "
                          "refinement in wave 26 wins 2020-22 and loses 2023-24), so weight by each "
                          "component's trailing realized rank-IC instead.",
            "causality": "on day t the labels for days <= t-1 are realized returns known at decision "
                         "time. trailing_mean(series, W)[t] averages series[t-W:t], which excludes t. "
                         "The exclusion is asserted inside trailing_mean, not assumed.",
            "ic_universe": "the official one: rows with a non-null label, limit-up rows included, day "
                           "skipped below 30 rows",
            "rule": "a_i(t) = max(trailing_IC_i(t), 0)**p; adaptive = a/sum(a) or the fixed weight when "
                    "sum(a) == 0; w_i(t) = (1-lambda)*fixed_i + lambda*adaptive_i(t)",
            "components": COMPONENTS, "fixed_weights": FIXED_WEIGHTS,
            "grid": {"windows": list(WINDOWS), "powers": list(POWERS), "lambdas": list(LAMBDAS)},
            "donor_fixed": {"column": DONOR, "provenance": "wave 13 stage 2 argmax"},
            "m_frac_fixed_at": M_FRAC,
            "m_provenance": "wave 20/25; wave 25's finer peak at 0.982 is deliberately NOT used here so "
                            "this wave isolates the weighting axis, and because wave 26 showed the 0.982 "
                            "gain is a redistribution across halves rather than an improvement",
            "tie_break_eps": TIE_EPS,
            "harness_proof": f"lambda = 0 must reproduce {REFERENCE} exactly",
            "shipping_rule_declared_in_advance": f"beat {REFERENCE} on the full window AND on both "
                                                 f"halves (reference {REF_HALF_DEV:.9f} / "
                                                 f"{REF_HALF_CONF:.9f}). A full-window-only win is not "
                                                 "evidence: waves 23/25/26 all produced one.",
            "no_free_parameters_in_the_statistic": "the trailing IC is the component's own realized rank "
                                                   "IC, the same quantity the official metric's first "
                                                   "term measures; only the window, the power and the "
                                                   "shrinkage are gridded",
            "current_best_before_this_wave": REFERENCE,
            "disclosed_selection_cost": "search over the same five repeatedly viewed years; no blind "
                                        "period remains",
            "no_test_period_data_read": True,
            "source_sha256": sha(Path(__file__)),
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        cs.log(f"wave-27 protocol frozen: {sha(protocol_path)[:16]}…")

    combined = cs.combined_frame()
    dates = combined["trade_date"].to_numpy()
    flags = combined["flag_limit_up"].to_numpy().astype(np.int64)
    valid = combined["price_valid"].to_numpy().astype(bool)
    y = combined["y_ret_1d"].to_numpy().astype(np.float64)
    codes, uniques = pd.factorize(combined["ts_code"].to_pandas(), sort=True)
    codes = codes.astype(np.int64)
    n_codes = len(uniques)
    tie_key = 1.0 - codes / max(n_codes - 1, 1)
    member = np.load(HERE / DONOR)

    unique_days, starts = np.unique(dates, return_index=True)
    ends = np.append(starts[1:], len(dates))
    n_days = len(unique_days)
    day_of_row = np.repeat(np.arange(n_days), ends - starts)

    columns = [np.load(HERE / stem) for stem in COMPONENTS]
    ranks = [daily_ranks(c, valid, dates) for c in columns]
    usable = [np.isfinite(c) & (c > -9.0) for c in columns]

    # ---- per-day IC of each component, and the trailing means
    ic = np.vstack([daily_ic_series(c, dates, y, starts, ends) for c in columns])
    for i, stem in enumerate(COMPONENTS):
        known = np.isfinite(ic[i])
        cs.log(f"IC[{stem[:44]:44s}] days {int(known.sum())}/{n_days}, mean "
               f"{np.nanmean(ic[i]):.6f}, sd {np.nanstd(ic[i]):.6f}")
    trailing = {W: np.vstack([trailing_mean(ic[i], W) for i in range(len(columns))])
                for W in WINDOWS}
    for W in WINDOWS:
        cs.log(f"trailing W={W}: first usable day {int(np.argmax(np.isfinite(trailing[W]).any(axis=0)))}"
               f", mean W5a {np.nanmean(trailing[W][0]):.6f}, mean slow16 "
               f"{np.nanmean(trailing[W][1]):.6f}")

    masks = {str(yy): (dates >= yy * 10000 + 101) & (dates <= yy * 10000 + 1231) for yy in YEARS}
    half = {"2020_2022": np.zeros(len(dates), dtype=bool),
            "2023_2024": np.zeros(len(dates), dtype=bool)}
    for yy in (2020, 2021, 2022):
        half["2020_2022"] |= masks[str(yy)]
    for yy in (2023, 2024):
        half["2023_2024"] |= masks[str(yy)]

    results: dict = {}
    proofs: dict = {}

    def dump() -> list:
        arms = sorted(((v["connected_final_score"], k, v) for k, v in results.items()
                       if "connected_final_score" in v), reverse=True)
        payload = {"status": "running", "updated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
                   "purpose": "adaptive orderer blend weights from causal trailing rank-IC",
                   "donor_fixed": DONOR, "m_frac": M_FRAC, "tie_break_eps": TIE_EPS,
                   "components": COMPONENTS, "fixed_weights": FIXED_WEIGHTS,
                   "harness_proofs": proofs,
                   "component_daily_ic_mean": {stem: float(np.nanmean(ic[i]))
                                               for i, stem in enumerate(COMPONENTS)},
                   "current_best_before_this_wave": REFERENCE,
                   "reference_halves": {"2020_2022": REF_HALF_DEV, "2023_2024": REF_HALF_CONF},
                   "results": results, "n_scored": len(arms),
                   "ranking": [{"arm": k, "connected_final_score": s,
                                "margin_full": v["margin_full"],
                                "margin_2020_2022": v["margin_2020_2022"],
                                "margin_2023_2024": v["margin_2023_2024"],
                                "recommended_to_ship": v.get("recommended_to_ship"),
                                "ic_mean": v["connected_metrics"]["ic_mean"],
                                "annual_excess": v["connected_metrics"]["annual_excess"],
                                "mean_turnover": v["connected_metrics"]["mean_turnover"]}
                               for s, k, v in arms[:25]],
                   "best": arms[0][1] if arms else None,
                   "best_connected_final_score": arms[0][0] if arms else None,
                   "best_recommended_to_ship": next((k for s, k, v in arms
                                                     if v.get("recommended_to_ship")), None),
                   "no_test_period_data_read": True,
                   "source_sha256": sha(Path(__file__))}
        (HERE / "wave27_results.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return arms

    def weights_for(window: int, power: float, lam: float) -> np.ndarray:
        tr = trailing[window]                                  # (n_components, n_days)
        a = np.clip(np.nan_to_num(tr, nan=0.0), 0.0, None) ** power
        total = a.sum(axis=0)
        adaptive = np.where(total > 0, a / np.where(total > 0, total, 1.0),
                            np.array(FIXED_WEIGHTS)[:, None])
        per_day = (1.0 - lam) * np.array(FIXED_WEIGHTS)[:, None] + lam * adaptive
        return np.repeat(per_day.T, ends - starts, axis=0)       # (n_rows, n_components)

    def score(name: str, weight_rows: np.ndarray, extra: dict) -> float:
        blended = blend_daily_weights(ranks, weight_rows, valid, usable)
        orderer = np.where(blended > -9.0, blended + TIE_EPS * tie_key, blended) + TIE_EPS * tie_key
        hybrid, stats = build_ab(member, orderer, orderer, dates, flags, codes, n_codes, M_FRAC)
        metrics, _ = score_official(combined, hybrid)
        halves = {}
        for label, mask in half.items():
            sub, _ = score_official(combined.filter(pl.Series(mask)), hybrid[mask])
            halves[label] = sub["final_score"]
        margin_full = metrics["final_score"] - REFERENCE
        m_dev = halves["2020_2022"] - REF_HALF_DEV
        m_conf = halves["2023_2024"] - REF_HALF_CONF
        recommended = bool(margin_full > 0 and m_dev > 0 and m_conf > 0) \
            if extra.get("role") != "harness_proof" else None
        results[name] = {**extra, "connected_final_score": metrics["final_score"],
                         "connected_metrics": metrics, "halves": halves,
                         "margin_full": margin_full, "margin_2020_2022": m_dev,
                         "margin_2023_2024": m_conf,
                         "boundary_tie_days": stats["boundary_tie_days"],
                         "mean_retention_ratio": stats["mean_retention_ratio"],
                         "recommended_to_ship": recommended}
        cs.log(f"{name[:26]:26s} CONNECTED {metrics['final_score']:.9f} ({margin_full:+.2e}) | "
               f"2020-22 {m_dev:+.2e} | 2023-24 {m_conf:+.2e} | ship={recommended}")
        dump()
        return metrics["final_score"]

    # ---- harness proof: lambda 0 is the constant blend
    got = score("P_lambda0", weights_for(WINDOWS[0], POWERS[0], 0.0),
                {"window": WINDOWS[0], "power": POWERS[0], "lambda": 0.0,
                 "role": "harness_proof"})
    proofs["P_lambda0_reproduces_the_constant_blend"] = {
        "scored": got, "expected": REFERENCE, "abs_diff": abs(got - REFERENCE)}
    if abs(got - REFERENCE) > 1e-12:
        raise AssertionError(f"harness proof failed: lambda=0 scored {got!r}, expected {REFERENCE!r}")
    cs.log("harness proof passed: lambda = 0 reproduces the shipped constant blend exactly")

    for window in WINDOWS:
        for power in POWERS:
            for lam in LAMBDAS:
                if lam == 0.0:
                    continue
                score(f"W{window}_p{power:g}_l{lam:g}", weights_for(window, power, lam),
                      {"window": window, "power": power, "lambda": lam})

    arms = dump()
    payload = json.loads((HERE / "wave27_results.json").read_text(encoding="utf-8"))
    payload["status"] = "complete"
    payload["completed_at_local"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    (HERE / "wave27_results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("\n| arm | CONNECTED | margin full | margin 2020-22 | margin 2023-24 | IC | excess | ship? |")
    print("|---|---|---|---|---|---|---|---|")
    for s, name, v in arms:
        m = v["connected_metrics"]
        print(f"| {name[:18]} | **{s:.9f}** | {v['margin_full']:+.2e} | {v['margin_2020_2022']:+.2e} "
              f"| {v['margin_2023_2024']:+.2e} | {m['ic_mean']:.6f} | {m['annual_excess']:.6f} | "
              f"{'YES' if v.get('recommended_to_ship') else '-'} |")
    cs.log(f"best by full window: {arms[0][1]} {arms[0][0]:.9f}")
    cs.log(f"best that also wins both halves: {payload['best_recommended_to_ship'] or 'NONE'}")


if __name__ == "__main__":
    main()
