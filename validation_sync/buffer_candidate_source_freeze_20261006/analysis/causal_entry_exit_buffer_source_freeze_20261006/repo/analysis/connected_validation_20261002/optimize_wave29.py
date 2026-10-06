"""Wave 29: limit-up rows are inside the Rank IC universe and the construction never touches them.

Wave 7b established that limit-up rows must be left alone, because lifting the chosen Top set above
everything also demoted them and moved the IC term as an unintended side effect. That fix was right, but
it left a consequence unexamined: `flag_limit_up == 0` is the universe for excess and for turnover, while
Rank IC uses EVERY row with a label, limit-up included. So limit-up rows affect exactly one term - IC, at
weight 0.4 - and the construction currently passes through whatever the orderer happened to give them.

Whether that is suboptimal is an empirical question with a real mechanism behind it, not a scoring
trick. The 63 features include flag_limit_up, so the models see the flag; but they are fitted to a
cross-sectional rank target over the whole universe, and a stock that closed at its up limit is exactly
the kind of name a momentum-flavoured rank target over-scores relative to what it does next day. If
limit-up names systematically underperform, ranking them lower is MORE accurate, and IC rises because
the prediction got better, not because the metric was gamed. If they outperform, the sweep will say so
and the sign flips.

The transformation is a single constant applied to one causal, day-t-known flag:
    pred[flag_limit_up == 1] += delta        (delta in units of the orderer's daily rank scale)
Excess and turnover cannot move, because both universes exclude these rows by construction - which makes
this a clean single-term experiment and means any composite change is pure IC.

One parameter, gridded in both directions, with delta = 0 as the harness proof that must reproduce
0.443190552 exactly. The shipping rule is the one waves 26-28 used: beat the reference on the full
window AND on both halves.

Selection is 后续选模标准.md §3/§4 for the ranking. No test-period data is read anywhere in this file.
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

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
import connected_scorer as cs  # noqa: E402
from experiments.revalidate_fold_local import score_official  # noqa: E402
from optimize_wave13 import build_ab  # noqa: E402
from optimize_wave15 import daily_ranks, weighted_rank_blend, DONOR, M_FRAC, TIE_EPS  # noqa: E402

YEARS = cs.YEARS
W5A_A0B0 = "orderer_a0b0_W5a_five_way_with_gru__final_sweep_eval.npy"
SLOW16_A0B0 = "pp_a0_b0_top_only_w0.25_rl1_tcw1.npy"
PARTNER_WEIGHT = 0.25
CURRENT_BEST = 0.44319055217888365
REF_HALF_DEV = 0.442705356
REF_HALF_CONF = 0.443926938
DELTAS = (-0.50, -0.20, -0.10, -0.05, 0.0, 0.05, 0.10, 0.20, 0.50)


def sha(path) -> str:
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def main() -> None:
    protocol_path = HERE / "protocol_wave29.json"
    if not protocol_path.exists():
        protocol_path.write_text(json.dumps({
            "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "standard": "后续选模标准.md §3 connected composite primary; §4 highest score wins",
            "status": "in_sample_selection_disclosed",
            "hypothesis": "limit-up rows are inside the Rank IC universe but excluded from the excess and "
                          "turnover universes, and the construction passes through whatever the orderer "
                          "gave them. A rank target fitted over the whole universe plausibly over-scores "
                          "a name that closed at its up limit relative to what it does next day, so a "
                          "single constant shift on that causal flag may raise IC. The sign is not "
                          "assumed: the grid runs both ways and the measurement decides.",
            "transformation": "pred[flag_limit_up == 1] += delta, delta in units of the orderer's daily "
                              "rank scale (which is normalized to (0, 1] per day)",
            "why_only_ic_can_move": "the excess universe requires flag_limit_up == 0 and a non-null "
                                    "label; the turnover universe requires flag_limit_up == 0. Both "
                                    "exclude these rows, so any composite change is pure IC.",
            "grid": list(DELTAS),
            "donor_fixed": {"column": DONOR, "provenance": "wave 13 stage 2 argmax"},
            "orderer_fixed": {"members": [W5A_A0B0, SLOW16_A0B0],
                              "weights": [1 - PARTNER_WEIGHT, PARTNER_WEIGHT]},
            "m_frac_fixed_at": M_FRAC, "tie_break_eps": TIE_EPS,
            "applied_where": "to the final hybrid column, after the swap-budget solve and slot "
                             "reassignment, because that is where the untouched limit-up rows live. The "
                             "membership and ordering decisions are unchanged, so this cannot move the "
                             "Top decile.",
            "harness_proof": f"delta = 0 must reproduce {CURRENT_BEST} exactly",
            "shipping_rule_declared_in_advance": f"beat {CURRENT_BEST} on the full window AND on both "
                                                 f"halves ({REF_HALF_DEV:.9f} / {REF_HALF_CONF:.9f})",
            "honest_note_on_gaming": "if limit-up names genuinely underperform, ranking them lower is a "
                                     "more accurate prediction and IC rises for the right reason. If they "
                                     "do not, the sweep will show a positive delta and this wave will "
                                     "have found that the orderers under-rank them. Either way the "
                                     "diagnostic (mean realized return of limit-up rows vs the rest, and "
                                     "their mean IC-rank) is recorded alongside the result so the "
                                     "direction can be judged rather than just taken.",
            "current_best_before_this_wave": CURRENT_BEST,
            "selection_rule": "highest connected 2020-2024 official composite; no other gate",
            "disclosed_selection_cost": "one parameter gridded over the same five repeatedly viewed "
                                        "years; no blind period remains",
            "causality": "flag_limit_up is a day-t flag, known at decision time. No label is read to "
                         "build the transformation; labels are read only to report the diagnostic.",
            "no_test_period_data_read": True,
            "source_sha256": sha(Path(__file__)),
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        cs.log(f"wave-29 protocol frozen: {sha(protocol_path)[:16]}…")

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

    w5a = np.load(HERE / W5A_A0B0)
    slow16 = np.load(HERE / SLOW16_A0B0)
    cache = {"w5a": daily_ranks(w5a, valid, dates), "slow16": daily_ranks(slow16, valid, dates)}
    blended = weighted_rank_blend([w5a, slow16], [1 - PARTNER_WEIGHT, PARTNER_WEIGHT], cache, valid,
                                  dates, ("w5a", "slow16"))
    orderer = np.where(blended > -9.0, blended + TIE_EPS * tie_key, blended) + TIE_EPS * tie_key

    hybrid0, stats0 = build_ab(member, orderer, orderer, dates, flags, codes, n_codes, M_FRAC)

    # ---- diagnostic, so the direction can be judged rather than just taken
    limited = flags == 1
    lab = np.isfinite(y)
    diag = {
        "limit_up_rows": int(limited.sum()),
        "limit_up_share_of_all_rows": float(limited.mean()),
        "limit_up_rows_with_label": int((limited & lab).sum()),
        "mean_realized_return_limit_up": float(np.nanmean(y[limited & lab])),
        "mean_realized_return_other": float(np.nanmean(y[~limited & lab])),
        "mean_return_gap_limit_up_minus_other": float(np.nanmean(y[limited & lab])
                                                      - np.nanmean(y[~limited & lab])),
        "mean_percentile_of_limit_up_in_final_column": None,
    }
    per_day_pct = pd.Series(hybrid0).groupby(dates, sort=False).rank(pct=True).to_numpy()
    diag["mean_percentile_of_limit_up_in_final_column"] = float(np.nanmean(per_day_pct[limited]))
    diag["mean_percentile_of_other_in_final_column"] = float(np.nanmean(per_day_pct[~limited]))
    cs.log("diagnostic: " + json.dumps({k: (round(v, 6) if isinstance(v, float) else v)
                                        for k, v in diag.items()}, ensure_ascii=False))

    masks = {str(yy): (dates >= yy * 10000 + 101) & (dates <= yy * 10000 + 1231) for yy in YEARS}
    half = {"2020_2022": np.zeros(len(dates), dtype=bool),
            "2023_2024": np.zeros(len(dates), dtype=bool)}
    for yy in (2020, 2021, 2022):
        half["2020_2022"] |= masks[str(yy)]
    for yy in (2023, 2024):
        half["2023_2024"] |= masks[str(yy)]

    results: dict = {}
    proofs: dict = {"diagnostic": diag}

    def dump() -> list:
        arms = sorted(((v["connected_final_score"], k, v) for k, v in results.items()
                       if "connected_final_score" in v), reverse=True)
        payload = {"status": "running", "updated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
                   "purpose": "shift the limit-up rows, which affect IC and nothing else",
                   "donor_fixed": DONOR, "m_frac": M_FRAC, "tie_break_eps": TIE_EPS,
                   "harness_proofs": proofs, "current_best_before_this_wave": CURRENT_BEST,
                   "reference_halves": {"2020_2022": REF_HALF_DEV, "2023_2024": REF_HALF_CONF},
                   "results": results, "n_scored": len(arms),
                   "ranking": [{"arm": k, "connected_final_score": s, "margin_full": v["margin_full"],
                                "margin_2020_2022": v["margin_2020_2022"],
                                "margin_2023_2024": v["margin_2023_2024"],
                                "recommended_to_ship": v.get("recommended_to_ship"),
                                "ic_mean": v["connected_metrics"]["ic_mean"],
                                "annual_excess": v["connected_metrics"]["annual_excess"],
                                "mean_turnover": v["connected_metrics"]["mean_turnover"]}
                               for s, k, v in arms],
                   "best": arms[0][1] if arms else None,
                   "best_connected_final_score": arms[0][0] if arms else None,
                   "best_recommended_to_ship": next((k for s, k, v in arms
                                                     if v.get("recommended_to_ship")), None),
                   "no_test_period_data_read": True,
                   "source_sha256": sha(Path(__file__))}
        (HERE / "wave29_results.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return arms

    for delta in DELTAS:
        hybrid = hybrid0.copy()
        if delta != 0.0:
            hybrid[limited] += delta
        metrics, _ = score_official(combined, hybrid)
        halves = {}
        for label, mask in half.items():
            sub, _ = score_official(combined.filter(pl.Series(mask)), hybrid[mask])
            halves[label] = sub["final_score"]
        margin_full = metrics["final_score"] - CURRENT_BEST
        m_dev = halves["2020_2022"] - REF_HALF_DEV
        m_conf = halves["2023_2024"] - REF_HALF_CONF
        name = f"delta{delta:+.2f}"
        results[name] = {"delta": delta, "connected_final_score": metrics["final_score"],
                         "connected_metrics": metrics, "halves": halves,
                         "margin_full": margin_full, "margin_2020_2022": m_dev,
                         "margin_2023_2024": m_conf,
                         "ic_change_vs_reference": metrics["ic_mean"] - 0.116662,
                         "excess_unchanged": abs(metrics["annual_excess"] - 0.354106) < 1e-9,
                         "turnover_unchanged": abs(metrics["mean_turnover"] - 0.032354) < 1e-9,
                         "recommended_to_ship": (None if delta == 0.0 else
                                                 bool(margin_full > 0 and m_dev > 0 and m_conf > 0))}
        cs.log(f"{name:12s} CONNECTED {metrics['final_score']:.9f} ({margin_full:+.2e}) | "
               f"ic {metrics['ic_mean']:.6f} | exc {metrics['annual_excess']:.6f} | "
               f"turn {metrics['mean_turnover']:.6f} | 2020-22 {m_dev:+.2e} | 2023-24 {m_conf:+.2e}")
        if delta == 0.0:
            proofs["P_delta0"] = {"scored": metrics["final_score"], "expected": CURRENT_BEST,
                                  "abs_diff": abs(metrics["final_score"] - CURRENT_BEST)}
            if abs(metrics["final_score"] - CURRENT_BEST) > 1e-12:
                raise AssertionError(f"harness proof failed: {metrics['final_score']!r} vs "
                                     f"{CURRENT_BEST!r}")
            cs.log("harness proof passed: delta = 0 reproduces 0.443190552")
        dump()

    arms = dump()
    payload = json.loads((HERE / "wave29_results.json").read_text(encoding="utf-8"))
    payload["status"] = "complete"
    payload["completed_at_local"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    (HERE / "wave29_results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("\n| delta | CONNECTED | margin | IC | excess | turnover | 2020-22 | 2023-24 | ship? |")
    print("|---|---|---|---|---|---|---|---|---|")
    for delta in DELTAS:
        v = results[f"delta{delta:+.2f}"]
        m = v["connected_metrics"]
        print(f"| {delta:+.2f} | **{v['connected_final_score']:.9f}** | {v['margin_full']:+.2e} | "
              f"{m['ic_mean']:.6f} | {m['annual_excess']:.6f} | {m['mean_turnover']:.6f} | "
              f"{v['margin_2020_2022']:+.2e} | {v['margin_2023_2024']:+.2e} | "
              f"{'YES' if v.get('recommended_to_ship') else '-'} |")
    cs.log(f"diagnostic: limit-up mean return {diag['mean_realized_return_limit_up']:+.6f} vs other "
           f"{diag['mean_realized_return_other']:+.6f}; limit-up mean percentile in the final column "
           f"{diag['mean_percentile_of_limit_up_in_final_column']:.4f}")
    cs.log(f"best: {arms[0][1]} {arms[0][0]:.9f} | best that wins both halves: "
           f"{payload['best_recommended_to_ship'] or 'NONE'}")


if __name__ == "__main__":
    main()
