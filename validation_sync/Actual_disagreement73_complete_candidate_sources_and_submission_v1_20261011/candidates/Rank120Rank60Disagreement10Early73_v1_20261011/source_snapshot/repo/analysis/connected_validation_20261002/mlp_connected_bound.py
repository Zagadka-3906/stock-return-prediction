"""Gap 1: place the MLP arms in the connected ranking without rebuilding deleted caches.

后续选模标准.md requires XGBoost and MLP to compete under the same standard. The MLP fold validation of
2026-09-29 recorded each arm's per-year official metrics but not its predictions or daily series, and
the 2026-10-01 cleanup deleted both the daily CSVs and the artifacts a re-run needs
(`neural_data/z.npy` and the fulltrain checkpoints `raw/nn_mlp_h{64,128}.npy`), so the script's
mandatory harness-proof gate cannot be satisfied and its folds cannot be re-scored as-is.

A point estimate is nevertheless unnecessary to rank them. The connected composite differs from the
annual caliber in exactly one place: four extra turnover observations, one per year boundary. The IC
and excess terms are unaffected because their denominators are arm-independent day counts, so both can
be recomputed EXACTLY from the frozen annual metrics. Only the turnover term is unknown, and each
missing boundary observation is a Jaccard distance bounded in [0, 1]. That yields a rigorous interval.

Interval width on the composite is 0.3 * 4 / 1211 = 0.000991.
"""
from __future__ import annotations

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

ARCHIVE = ROOT.parent / "赛题五_历史归档_20261001"
MLP_DIR = ARCHIVE / "analysis/mlp_training_validation_20260929"
HYBRID_DIR = ROOT / "analysis/topset_hybrid_20261002"
YEARS = cs.YEARS
BOUNDARY_OBSERVATIONS = 4


def denominators() -> dict:
    """Per-year valid-day counts for each official metric. These depend only on labels and
    flag_limit_up, never on the predictions, so they are identical for every arm - asserted here
    across three structurally different arms rather than assumed."""
    counts = {}
    for arm in ("A", "B", "H"):
        per_year = {}
        for year in YEARS:
            daily = pd.read_csv(HYBRID_DIR / f"daily_{arm}_{year}.csv")
            per_year[year] = {name: int(daily[name].notna().sum())
                              for name in ("rank_ic", "excess", "turnover")}
            per_year[year]["rows"] = len(daily)
        counts[arm] = per_year
    for year in YEARS:
        for name in ("rank_ic", "excess", "turnover", "rows"):
            values = {counts[arm][year][name] for arm in ("A", "B", "H")}
            if len(values) != 1:
                raise AssertionError(f"{year}/{name}: denominators differ across arms {values}")
    return counts["A"]


def connected_exact(annual: dict[int, dict], denom: dict) -> dict:
    """Exact connected IC and excess; bounded connected turnover."""
    ic_num = sum(denom[y]["rank_ic"] * annual[y]["ic_mean"] for y in YEARS)
    ic_den = sum(denom[y]["rank_ic"] for y in YEARS)
    ex_num = sum(denom[y]["excess"] * annual[y]["annual_excess"] for y in YEARS)
    ex_den = sum(denom[y]["excess"] for y in YEARS)
    tu_num = sum(denom[y]["turnover"] * annual[y]["mean_turnover"] for y in YEARS)
    tu_den = sum(denom[y]["turnover"] for y in YEARS)
    if tu_den + BOUNDARY_OBSERVATIONS != 1211:
        raise AssertionError(f"turnover denominators {tu_den}+{BOUNDARY_OBSERVATIONS} != 1211")
    ic_conn = ic_num / ic_den
    ex_conn = ex_num / ex_den
    tu_low = tu_num / (tu_den + BOUNDARY_OBSERVATIONS)
    tu_high = (tu_num + BOUNDARY_OBSERVATIONS) / (tu_den + BOUNDARY_OBSERVATIONS)
    score = lambda t: 0.4 * ic_conn + 0.3 * ex_conn + 0.3 * (1 - t)
    return {"ic_days": ic_den, "excess_days": ex_den, "turnover_days_annual": tu_den,
            "turnover_days_connected": tu_den + BOUNDARY_OBSERVATIONS,
            "ic_mean_connected_exact": ic_conn, "annual_excess_connected_exact": ex_conn,
            "turnover_connected_low": tu_low, "turnover_connected_high": tu_high,
            "connected_score_upper": score(tu_low), "connected_score_lower": score(tu_high),
            "interval_width": score(tu_low) - score(tu_high),
            "five_year_equal_weight_mean": float(np.mean([annual[y]["final_score"] for y in YEARS]))}


def main() -> None:
    denom = denominators()
    cs.log(f"arm-independent denominators verified across three arms: "
           f"ic {sum(denom[y]['rank_ic'] for y in YEARS)}, "
           f"excess {sum(denom[y]['excess'] for y in YEARS)}, "
           f"turnover {sum(denom[y]['turnover'] for y in YEARS)} + "
           f"{BOUNDARY_OBSERVATIONS} boundary = "
           f"{sum(denom[y]['turnover'] for y in YEARS) + BOUNDARY_OBSERVATIONS}")

    results = json.loads((HERE / "connected_results_all.json").read_text(encoding="utf-8"))["results"]
    leader = max(results.items(), key=lambda kv: kv[1]["connected_final_score"])
    confirmed = results["peer67_slow16"]["connected_final_score"]

    arms = {}
    for arm in ("mlp_h64", "mlp_h128"):
        annual = {}
        for year in YEARS:
            record = json.loads((MLP_DIR / f"{arm}_{year}.json").read_text(encoding="utf-8"))
            annual[year] = {k: float(v) for k, v in record["official_metrics"].items()}
        bound = connected_exact(annual, denom)
        bound["annual_official_metrics"] = {str(y): {k: annual[y][k] for k in
                                                     ("ic_mean", "annual_excess", "mean_turnover",
                                                      "final_score")} for y in YEARS}
        # would the arm reach the leader even if every boundary turnover were zero?
        bound["beats_leader_even_at_best_boundary"] = bool(
            bound["connected_score_upper"] > leader[1]["connected_final_score"])
        bound["beats_confirmed_even_at_best_boundary"] = bool(
            bound["connected_score_upper"] > confirmed)
        bound["gap_to_leader_at_upper_bound"] = (leader[1]["connected_final_score"]
                                                 - bound["connected_score_upper"])
        arms[arm] = bound
        cs.log(f"{arm}: connected in [{bound['connected_score_lower']:.9f}, "
               f"{bound['connected_score_upper']:.9f}] (width {bound['interval_width']:.6f}); "
               f"leader {leader[0]} {leader[1]['connected_final_score']:.9f}; "
               f"gap at the upper bound {bound['gap_to_leader_at_upper_bound']:+.6f}")

    payload = {
        "status": "complete", "completed_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "purpose": "place the MLP arms in the connected 2020-2024 ranking under 后续选模标准.md §3 "
                   "without rebuilding deleted caches",
        "why_not_a_point_estimate": {
            "missing_artifacts": ["analysis/mlp_training_validation_20260929/daily_mlp_*_{year}.csv "
                                  "(written by the frozen run, deleted in the cleanup)",
                                  "analysis/all_models_test_20260929/early/neural_data/z.npy",
                                  "analysis/all_models_test_20260929/early/raw/nn_mlp_h64.npy",
                                  "analysis/all_models_test_20260929/early/raw/nn_mlp_h128.npy"],
            "consequence": "the frozen script's proof stage cannot run, and its folds stage refuses "
                           "to score without a passing proof gate; re-running would require "
                           "rebuilding the 2.4 GB normalized tensor cache and retraining the "
                           "fulltrain checkpoints, then bypassing or re-satisfying that gate",
            "what_survives": "per-year official_metrics for both arms, computed by the same "
                             "unmodified evaluate.py on the same fold frames",
        },
        "method": "the connected and annual calibers differ only by four boundary turnover "
                  "observations; IC and excess denominators are arm-independent day counts so both "
                  "terms are exact, and each Jaccard distance is bounded in [0,1]",
        "denominators": {str(y): denom[y] for y in YEARS},
        "interval_width_on_composite": 0.3 * BOUNDARY_OBSERVATIONS / 1211,
        "leader": {"name": leader[0], "connected_final_score": leader[1]["connected_final_score"]},
        "confirmed_model": {"name": "peer67_slow16", "connected_final_score": confirmed},
        "arms": arms,
        "no_test_period_data_read": True,
    }
    (HERE / "mlp_connected_bound.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"\nleader: {leader[0]} {leader[1]['connected_final_score']:.9f} | confirmed "
          f"peer67_slow16 {confirmed:.9f}")
    print("\n| arm | connected lower | connected upper | width | beats leader at the upper bound? |")
    print("|---|---|---|---|---|")
    for arm, b in arms.items():
        print(f"| {arm} | {b['connected_score_lower']:.9f} | {b['connected_score_upper']:.9f} | "
              f"{b['interval_width']:.6f} | {b['beats_leader_even_at_best_boundary']} |")
    print("\nfor reference, the same arms' five-year equal-weight means (diagnostic only): "
          + ", ".join(f"{a} {b['five_year_equal_weight_mean']:.6f}" for a, b in arms.items()))


if __name__ == "__main__":
    main()
