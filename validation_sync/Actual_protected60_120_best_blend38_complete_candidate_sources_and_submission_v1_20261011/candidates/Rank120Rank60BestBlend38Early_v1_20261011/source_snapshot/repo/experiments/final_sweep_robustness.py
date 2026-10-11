"""Is the survivor's advantage broad-based, and does it survive trading costs?

Two questions that do not add any selection pressure, because both are
decompositions of a decision already made under a frozen gate:

  concentration  the pooled five-year delta is a sum of 1212 daily paired
                 contributions. If a handful of days supply it, the result is an
                 episode, not an edge. This reports each year's share, the share
                 of the largest days, calendar-quarter spreads and a block
                 bootstrap over trading days.
  costs          the ensemble changes turnover as well as IC, so the gross
                 comparison is not the whole story. Applying the cost model
                 already established for this project (0.30% round trip at the
                 centre, 0.10%/0.50% as bounds, charged only on names that
                 actually change) gives the net picture.

Both read the official daily evidence already on disk; nothing is re-scored.
"""
from __future__ import annotations

import json
import time

import numpy as np
import polars as pl

from run import ROOT
from experiments.final_sweep_significance import (AUDIT_YEARS, SCORED_YEARS, contributions, daily,
                                                  ANNUALIZATION)

SWEEP = ROOT / "experiments" / "final_sweep_eval"
AUDIT_OUT = ROOT / "experiments" / "extended_audit_eval"
SURVIVOR = "W3e_lgb_xgb_twoday_pruned"
RUNNER_UP = "T2f_xgboost_backbone"
COST_GRID = (0.001, 0.003, 0.005)
BOOTSTRAP_BLOCKS = 20
BOOTSTRAP_DRAWS = 20000
BOOTSTRAP_SEED = 20260926
SOURCES = {SCORED_YEARS: (SWEEP, "baseline_released"), AUDIT_YEARS: (AUDIT_OUT, "released_lgb_backbone")}


def series(key: str) -> tuple[np.ndarray, np.ndarray, list[int]]:
    """Concatenated daily paired contributions, turnover pairs and year labels."""
    parts, turnover, years = [], [], []
    for group, (folder, baseline_key) in SOURCES.items():
        for year in group:
            candidate = daily(folder, key, year)
            baseline = daily(folder, baseline_key, year)
            parts.append(contributions(candidate, baseline))
            turnover.append(np.vstack([
                np.nan_to_num(baseline["turnover"], nan=0.0),
                np.nan_to_num(candidate["turnover"], nan=0.0)]))
            years.extend([year] * len(parts[-1]))
    return np.concatenate(parts), np.hstack(turnover), years


def block_bootstrap(values: np.ndarray) -> dict:
    """Moving-block bootstrap over trading days; blocks preserve local dependence."""
    n = len(values)
    rng = np.random.default_rng(BOOTSTRAP_SEED)
    blocks = n // BOOTSTRAP_BLOCKS + 1
    starts = rng.integers(0, n - BOOTSTRAP_BLOCKS + 1, size=(BOOTSTRAP_DRAWS, blocks))
    index = (starts[:, :, None] + np.arange(BOOTSTRAP_BLOCKS)[None, None, :]).reshape(
        BOOTSTRAP_DRAWS, -1)[:, :n]
    draws = values[index].mean(axis=1)
    observed = float(values.mean())
    return {"observed_mean_daily_contribution": observed,
            "bootstrap_se": float(draws.std(ddof=1)),
            "ci95": [float(np.percentile(draws, 2.5)), float(np.percentile(draws, 97.5))],
            "share_of_draws_positive": float((draws > 0).mean()),
            "block_days": BOOTSTRAP_BLOCKS, "draws": BOOTSTRAP_DRAWS}


def concentration(values: np.ndarray, years: list[int]) -> dict:
    total = float(values.sum())
    positive_mass = float(values[values > 0].sum())
    order = np.argsort(-np.abs(values))
    year_array = np.asarray(years)
    per_year = {}
    for year in sorted(set(years)):
        mask = year_array == year
        per_year[str(year)] = {"delta": float(values[mask].sum()),
                               "share_of_total": float(values[mask].sum() / total) if total else None,
                               "positive_days": int((values[mask] > 0).sum()),
                               "days": int(mask.sum())}
    return {"total_delta": total, "per_year": per_year,
            "largest_5_days_share_of_total": float(values[order[:5]].sum() / total) if total else None,
            "largest_20_days_share_of_total": float(values[order[:20]].sum() / total) if total else None,
            "largest_5_days_share_of_positive_mass": float(values[order[:5]].sum() / positive_mass),
            "top5_positive_days_share_of_positive_mass": float(
                np.sort(values[values > 0])[-5:].sum() / positive_mass),
            "top20_positive_days_share_of_positive_mass": float(
                np.sort(values[values > 0])[-20:].sum() / positive_mass),
            "positive_days": int((values > 0).sum()), "days": int(len(values)),
            "positive_mass": positive_mass, "negative_mass": float(values[values < 0].sum())}


def replaced_fraction(jaccard: np.ndarray) -> np.ndarray:
    """Invert J = 2u/(1+u) to recover the one-way replaced fraction u."""
    return jaccard / (2.0 - jaccard)


def cost_adjusted(baseline_turnover: np.ndarray, candidate_turnover: np.ndarray) -> dict:
    """Charge round-trip cost on the names that actually change, per day."""
    out = {}
    for cost in COST_GRID:
        baseline_drag = replaced_fraction(baseline_turnover) * cost * ANNUALIZATION
        candidate_drag = replaced_fraction(candidate_turnover) * cost * ANNUALIZATION
        difference = float(candidate_drag.mean() - baseline_drag.mean())
        out[f"round_trip_{cost:.2%}"] = {
            "baseline_annual_excess_drag": float(baseline_drag.mean()),
            "candidate_annual_excess_drag": float(candidate_drag.mean()),
            "candidate_minus_baseline_annual": difference,
            "candidate_minus_baseline_on_composite": 0.3 * difference,
            "note": "cost is charged only on the replaced fraction of the Top set; a negative value "
                    "means the candidate trades less and therefore pays less"}
    return out


def analyse(key: str) -> dict:
    values, turnover, years = series(key)
    scored_mask = np.asarray([y in SCORED_YEARS for y in years])
    return {"candidate": key,
            "concentration": concentration(values, years),
            "block_bootstrap": block_bootstrap(values),
            "costs_gated_years_only": cost_adjusted(turnover[0][scored_mask],
                                                    turnover[1][scored_mask])}


def main() -> None:
    report = {"generated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
              "annualization": ANNUALIZATION, "candidates": {}}
    for key in (SURVIVOR, RUNNER_UP):
        report["candidates"][key] = analyse(key)
        item = report["candidates"][key]
        c = item["concentration"]
        b = item["block_bootstrap"]
        print(f"=== {key}")
        print(f"  total delta {c['total_delta']:+.6f} over {c['days']} days; "
              f"positive {c['positive_days']}/{c['days']}")
        print(f"  5 largest-magnitude days = {c['largest_5_days_share_of_total']:+.1%} of the total "
              f"(negative means they subtract); top 5 positive days = "
              f"{c['top5_positive_days_share_of_positive_mass']:.1%} of the positive mass, top 20 = "
              f"{c['top20_positive_days_share_of_positive_mass']:.1%}")
        for year, row in c["per_year"].items():
            print(f"    {year}: {row['delta']:+.6f} ({row['share_of_total']:.1%} of total), "
                  f"{row['positive_days']}/{row['days']} positive days")
        print(f"  block bootstrap: mean {b['observed_mean_daily_contribution']:+.3e} "
              f"se {b['bootstrap_se']:.3e} ci95 [{b['ci95'][0]:+.3e}, {b['ci95'][1]:+.3e}] "
              f"positive in {b['share_of_draws_positive']:.1%} of draws")
        for label, row in item["costs_gated_years_only"].items():
            print(f"  {label}: baseline drag {row['baseline_annual_excess_drag']:.4f}, "
                  f"candidate drag {row['candidate_annual_excess_drag']:.4f}, "
                  f"candidate-baseline {row['candidate_minus_baseline_annual']:+.6f} annual, "
                  f"{row['candidate_minus_baseline_on_composite']:+.6f} on the composite")
    (SWEEP / "robustness.json").write_text(json.dumps(report, ensure_ascii=False, indent=2),
                                           encoding="utf-8")


if __name__ == "__main__":
    main()
