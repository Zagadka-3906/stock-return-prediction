"""Paired daily significance test for the sweep's survivors.

Every candidate's official daily evidence is already on disk, and the composite
reconstructs from it exactly:

    composite = 0.4*mean(rank_ic) + 0.3*252*mean(excess) + 0.3*(1 - mean(turnover))

with rank_ic and excess averaged over all scored days and turnover over the days
that have one (day 1 carries no turnover). That identity, verified to 5e-11
against the recorded final_score, lets the composite difference be written as a
sum of *daily* paired contributions:

    d_t = 0.4*(ic_c,t - ic_b,t)/N_ic + 0.3*252*(ex_c,t - ex_b,t)/N_ex
          + 0.3*(tv_b,t - tv_c,t)/N_tv

sum(d_t) is exactly the composite delta, so mean(d_t) can be given a Newey-West
HAC t-statistic. This matters because the project's earlier adoption record
carried the caveat that all paired 95% intervals spanned zero; a survivor should
be checked against that bar rather than adopted on its point estimate.
"""
from __future__ import annotations

import json
import time

import numpy as np
import polars as pl

from run import ROOT

SWEEP = ROOT / "experiments" / "final_sweep_eval"
AUDIT = ROOT / "experiments" / "extended_audit_eval"
ANNUALIZATION = 252.0
WEIGHTS = {"ic": 0.4, "excess": 0.3, "turnover": 0.3}
HAC_LAGS = (5, 10, 20)
SURVIVORS = {
    "T2f_xgboost_backbone": {"scored": (SWEEP, "baseline_released"), "audit": (AUDIT, "released_lgb_backbone")},
    "W3e_lgb_xgb_twoday_pruned": {"scored": (SWEEP, "baseline_released"), "audit": (AUDIT, "released_lgb_backbone")},
}
SCORED_YEARS = (2022, 2023, 2024)
AUDIT_YEARS = (2020, 2021)


def daily(folder, key: str, year: int) -> dict[str, np.ndarray]:
    frame = pl.read_csv(folder / f"{key}_{year}_daily.csv", null_values=["NaN"])
    return {name: frame[name].to_numpy().astype(np.float64)
            for name in ("rank_ic", "excess", "turnover")}


def ensure_baseline_daily(year: int) -> None:
    """Materialize the released baseline's 2024 daily evidence, anchored to 1e-12.

    The T1 suite only wrote baseline daily series for its two development years;
    the third-year reference is rebuilt here from the released stack and asserted
    against the released composite before use.
    """
    path = SWEEP / f"baseline_released_{year}_daily.csv"
    if path.exists():
        return
    from experiments.bonus_extension import (BASE_BONUS, BLEND_WEIGHT, load_auxiliary, load_panel,
                                            release_scores)
    from experiments.final_sweep import blend_top_only, retention_scores, RELEASED
    from experiments.official_seed_development import official_score

    panel = load_panel(year)
    auxiliary = load_auxiliary(year, panel)
    raw = panel.frame["pred_raw"].to_numpy().astype(np.float64)
    stable = retention_scores(panel, raw, RELEASED["alpha"], BASE_BONUS, "standard")
    metrics, frame = official_score(panel, blend_top_only(panel, stable, raw, auxiliary,
                                                          BLEND_WEIGHT), year)
    if abs(metrics["final_score"] - release_scores()[year]) > 1e-12:
        raise AssertionError(f"{year} rebuilt baseline daily evidence does not match the release")
    frame.write_csv(path)
    print(f"  rebuilt baseline_released_{year}_daily.csv (anchored to "
          f"{metrics['final_score']:.15f})")


def contributions(candidate: dict, baseline: dict) -> np.ndarray:
    """Per-day share of the composite difference; sums to the exact delta."""
    ic = candidate["rank_ic"] - baseline["rank_ic"]
    excess = candidate["excess"] - baseline["excess"]
    turnover = np.nan_to_num(baseline["turnover"] - candidate["turnover"], nan=0.0)
    n_ic = int(np.isfinite(ic).sum())
    n_excess = int(np.isfinite(excess).sum())
    n_turnover = int(np.isfinite(candidate["turnover"]).sum())
    return (WEIGHTS["ic"] * np.nan_to_num(ic) / n_ic
            + WEIGHTS["excess"] * ANNUALIZATION * np.nan_to_num(excess) / n_excess
            + WEIGHTS["turnover"] * turnover / n_turnover)


def hac_t(values: np.ndarray, lag: int) -> tuple[float, float, float]:
    n = len(values)
    mean = float(values.mean())
    centered = values - mean
    gamma0 = float(centered @ centered) / n
    variance = gamma0
    for k in range(1, lag + 1):
        weight = 1.0 - k / (lag + 1.0)
        gamma_k = float(centered[k:] @ centered[:-k]) / n
        variance += 2.0 * weight * gamma_k
    standard_error = float(np.sqrt(variance / n))
    return mean, standard_error, (mean / standard_error if standard_error > 0 else float("nan"))


def analyse() -> dict:
    report = {"generated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
              "annualization": ANNUALIZATION, "hac_lags": list(HAC_LAGS), "candidates": {}}
    for year in SCORED_YEARS:
        ensure_baseline_daily(year)
    for key, sources in SURVIVORS.items():
        entry = {"years": {}}
        pooled = []
        for label, years, source in (("scored", SCORED_YEARS, sources["scored"]),
                                     ("audit", AUDIT_YEARS, sources["audit"])):
            folder, baseline_key = source
            for year in years:
                candidate = daily(folder, key, year)
                baseline = daily(folder, baseline_key, year)
                d = contributions(candidate, baseline)
                pooled.append(d)
                delta = float(d.sum())
                row = {"delta": delta, "days": int(len(d)),
                       "positive_days": int((d > 0).sum()),
                       "mean_daily_contribution": float(d.mean())}
                for lag in HAC_LAGS:
                    _, se, t = hac_t(d, lag)
                    row[f"hac{lag}_se"] = se
                    row[f"hac{lag}_t"] = t
                entry["years"][str(year)] = row
        all_days = np.concatenate(pooled)
        entry["pooled"] = {"delta_sum": float(all_days.sum()), "days": int(len(all_days)),
                           "positive_days": int((all_days > 0).sum()),
                           "mean_daily_contribution": float(all_days.mean())}
        for lag in HAC_LAGS:
            mean, se, t = hac_t(all_days, lag)
            entry["pooled"][f"hac{lag}_se"] = se
            entry["pooled"][f"hac{lag}_t"] = t
            entry["pooled"][f"hac{lag}_mean"] = mean
        entry["pooled"]["years"] = [str(y) for y in SCORED_YEARS + AUDIT_YEARS]
        entry["pooled"]["caveat"] = ("Pooled days are not independent across years: folds share "
                                     "training history and features, so the pooled t-statistic is "
                                     "an upper bound on significance.")
        report["candidates"][key] = entry
    return report


def main() -> None:
    report = analyse()
    (SWEEP / "significance.json").write_text(json.dumps(report, ensure_ascii=False, indent=2),
                                             encoding="utf-8")
    for key, entry in report["candidates"].items():
        print(f"=== {key}")
        for year, row in entry["years"].items():
            print(f"  {year}: delta={row['delta']:+.9f} positive_days={row['positive_days']}/{row['days']}"
                  f" hac10_t={row['hac10_t']:+.2f}")
        pooled = entry["pooled"]
        print(f"  pooled(5y): delta={pooled['delta_sum']:+.9f} "
              f"positive_days={pooled['positive_days']}/{pooled['days']} "
              f"hac5_t={pooled['hac5_t']:+.2f} hac10_t={pooled['hac10_t']:+.2f} "
              f"hac20_t={pooled['hac20_t']:+.2f}")


if __name__ == "__main__":
    main()
