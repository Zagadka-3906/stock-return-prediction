"""Descriptive head-to-head of the corrected-caliber candidates, from frozen daily evidence only.

Nothing here trains, selects or gates. It reads the daily official evidence that two already
frozen rounds wrote (the 2026-09-26 fold-local revalidation and the r5 fixed-candidate round)
and answers one question the user asked: between the XGBoost backbone and the shipped r4
four-member ensemble, which is better, and does the r5 two-model combination dominate either?

Outputs a new directory; no frozen artifact is read-write or overwritten.
"""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

import numpy as np
import polars as pl

from run import ROOT
from experiments.final_sweep_significance import ANNUALIZATION, WEIGHTS, contributions, hac_t

REVALIDATION = ROOT / "experiments" / "revalidation_20260926" / "validation"
R5 = ROOT / "experiments" / "optimization_r5_20260926"
OUT = ROOT / "experiments" / "xgb_vs_r4_eval"
YEARS = (2020, 2021, 2022, 2023, 2024)
HAC_LAGS = (5, 10, 20)
COLUMNS = ("rank_ic", "excess", "turnover")
SOURCES = {
    "baseline": REVALIDATION,
    "xgboost": REVALIDATION,
    "ensemble4": REVALIDATION,
    "xgb_two_mean": R5,
}


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def load(name: str, year: int) -> dict:
    frame = pl.read_csv(SOURCES[name] / f"daily_{name}_{year}.csv", null_values=["NaN"])
    return {key: frame[key].to_numpy() for key in COLUMNS}


def composite(daily: dict) -> float:
    """Rebuild the annual composite from the daily official evidence."""
    turnover = daily["turnover"]
    return (WEIGHTS["ic"] * float(np.nanmean(daily["rank_ic"]))
            + WEIGHTS["excess"] * ANNUALIZATION * float(np.nanmean(daily["excess"]))
            + WEIGHTS["turnover"] * float(1.0 - np.nanmean(turnover[np.isfinite(turnover)])))


def terms(candidate: dict, reference: dict) -> dict:
    """Split the paired composite delta into its three official components."""
    ic = np.nan_to_num(candidate["rank_ic"] - reference["rank_ic"])
    excess = np.nan_to_num(candidate["excess"] - reference["excess"])
    turnover = np.nan_to_num(reference["turnover"] - candidate["turnover"], nan=0.0)
    counts = {key: int(np.isfinite(candidate[key]).sum()) for key in COLUMNS}
    return {"ic": WEIGHTS["ic"] * float(ic.sum()) / counts["rank_ic"],
            "excess": WEIGHTS["excess"] * ANNUALIZATION * float(excess.sum()) / counts["excess"],
            "turnover": WEIGHTS["turnover"] * float(turnover.sum()) / counts["turnover"]}


def paired(name: str, reference: str) -> dict:
    pieces, per_year = [], {}
    for year in YEARS:
        candidate, base = load(name, year), load(reference, year)
        values = contributions(candidate, base)
        pieces.append(values)
        per_year[str(year)] = {"score_delta": float(values.sum()),
                               "positive_days": int((values > 0).sum()), "days": len(values),
                               **terms(candidate, base)}
    pooled = np.concatenate(pieces)
    ordered = np.sort(np.abs(pooled))[::-1]
    entry = {
        "days": len(pooled), "per_year": per_year,
        "annual_score_deltas": [float(piece.sum()) for piece in pieces],
        "positive_years": int(sum(piece.sum() > 0 for piece in pieces)),
        "cumulative_delta": float(pooled.sum()),
        "mean_annual_delta": float(pooled.sum() / len(YEARS)),
        "worst_year": min(float(piece.sum()) for piece in pieces),
        "mean_terms": {key: float(np.mean([per_year[str(y)][key] for y in YEARS]))
                       for key in ("ic", "excess", "turnover")},
        "concentration": {"largest_5_abs_days_share_of_total": float(ordered[:5].sum() / pooled.sum())
        if pooled.sum() else None,
                          "largest_5_positive_share_of_positive_mass": float(
                              np.sort(pooled[pooled > 0])[::-1][:5].sum()
                              / pooled[pooled > 0].sum()) if (pooled > 0).any() else None},
    }
    for lag in HAC_LAGS:
        mean, se, statistic = hac_t(pooled, lag)
        scale = len(pooled) / len(YEARS)
        entry[f"hac{lag}"] = {"t": statistic, "mean_annual_delta": mean * scale,
                              "ci95": [(mean - 1.96 * se) * scale, (mean + 1.96 * se) * scale]}
    return entry


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    destination = OUT / "comparison.json"
    if destination.exists():
        raise SystemExit("comparison.json already recorded; preserving it")
    shared = {}
    for year in YEARS:
        for name in ("baseline", "ensemble4"):
            a = hashlib.sha256((REVALIDATION / f"daily_{name}_{year}.csv").read_bytes()).hexdigest()
            b = hashlib.sha256((R5 / f"daily_{name}_{year}.csv").read_bytes()).hexdigest()
            shared[f"{name}_{year}_identical_in_both_rounds"] = bool(a == b)
            if a != b:
                raise AssertionError(f"{name} {year}: the two frozen rounds disagree on the daily "
                                     "evidence; refusing to mix calibers")
    log("Daily evidence for baseline and ensemble4 is byte-identical across both frozen rounds")

    recorded = {"xgb_two_mean": {str(y): s for y, s in zip(
        YEARS, (0.433551293, 0.421141856, 0.451106749, 0.420417425, 0.409084390))}}
    composites = {}
    for name in SOURCES:
        composites[name] = {str(year): composite(load(name, year)) for year in YEARS}
    for year in YEARS:
        expected = recorded["xgb_two_mean"][str(year)]
        if abs(composites["xgb_two_mean"][str(year)] - expected) > 5e-9:
            raise AssertionError(f"xgb_two_mean {year}: daily evidence does not rebuild the "
                                 f"recorded composite ({composites['xgb_two_mean'][str(year)]:.9f} "
                                 f"vs {expected:.9f})")
    log("Every annual composite rebuilds from its daily evidence; the r5 winner matches its record")

    result = {
        "stage": "descriptive_head_to_head",
        "generated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "role": "Descriptive only. No candidate was selected, gated or adopted here; the r5 "
                "confirmation already failed its pre-frozen bootstrap gate against pooled.",
        "caliber": "corrected fold-local column selection, pooled auxiliary + 25% Top blend in all "
                   "five years, identical for every candidate",
        "selection_bias_corrected": False,
        "limitations": "All five years have been viewed repeatedly; pooled HAC and bootstrap "
                       "intervals do not correct for cumulative candidate selection.",
        "annual_composites": composites,
        "shared_evidence_check": shared,
        "comparisons": {},
        "input_sha256": {},
    }
    for name, reference in (("xgboost", "ensemble4"), ("xgb_two_mean", "ensemble4"),
                            ("xgb_two_mean", "xgboost"), ("ensemble4", "baseline"),
                            ("xgboost", "baseline"), ("xgb_two_mean", "baseline")):
        result["comparisons"][f"{name}_minus_{reference}"] = paired(name, reference)
        log(f"{name} − {reference}: mean {result['comparisons'][f'{name}_minus_{reference}']
                                              ['mean_annual_delta']:+.6f}")
    for name in SOURCES:
        for year in YEARS:
            path = SOURCES[name] / f"daily_{name}_{year}.csv"
            result["input_sha256"][path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("\n年度综合分（更正口径，五年同栈）")
    print(f"{'年份':<8}" + "".join(f"{n:>16}" for n in ("baseline", "ensemble4", "xgboost",
                                                          "xgb_two_mean")))
    for year in YEARS:
        print(f"{year:<8}" + "".join(f"{composites[n][str(year)]:>16.9f}"
                                     for n in ("baseline", "ensemble4", "xgboost", "xgb_two_mean")))
    print("\n配对比较（正数=前者更好）")
    header = f"{'比较':<34}{'年均':>12}{'最差年':>12}{'正年':>7}{'t(10)':>9}{'CI95 下限':>13}"
    print(header + "\n" + "-" * len(header))
    for key, entry in result["comparisons"].items():
        print(f"{key:<34}{entry['mean_annual_delta']:>+12.6f}{entry['worst_year']:>+12.6f}"
              f"{entry['positive_years']:>5}/5{entry['hac10']['t']:>9.2f}"
              f"{entry['hac10']['ci95'][0]:>+13.6f}")
    print("\n三项分解（年均，正数=前者更好）")
    print(f"{'比较':<34}{'IC':>12}{'超额':>12}{'换手':>12}")
    for key, entry in result["comparisons"].items():
        t = entry["mean_terms"]
        print(f"{key:<34}{t['ic']:>+12.6f}{t['excess']:>+12.6f}{t['turnover']:>+12.6f}")
    log(f"Wrote {destination}")


if __name__ == "__main__":
    main()
