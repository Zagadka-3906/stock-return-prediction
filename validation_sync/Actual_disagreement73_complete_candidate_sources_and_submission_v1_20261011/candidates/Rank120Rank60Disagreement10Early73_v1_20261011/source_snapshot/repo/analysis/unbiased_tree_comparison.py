"""Unbiased training-period comparison of the five tree arms, with paired uncertainty.

No arm is privileged: the currently deployed arm enters the table on exactly the same footing as
every other. The axis is the only admissible one - 2020-2024 same-protocol official-evaluator
validation - because the competition withholds test labels until after scoring.

Per-day paired contribution follows the project's established convention: IC, excess and turnover
each keep the year's own valid-day count as a fixed denominator, and a day on which either arm has
no turnover contributes zero for the turnover part. The five-year difference is the equal-weight
mean of the five annual differences; its CI95 comes from 20-day moving-block resampling drawn
independently per year (20,000 draws, seed 20260929 + year), i.e. the same instrument the top2 and
monthly validations used.

Reads only existing daily CSVs. Writes comparison_unbiased.json inside this directory.
"""
from __future__ import annotations

import itertools
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from analysis.official_score_contributions import (  # noqa: E402
    composite, daily_contribution, metric_denominators, paired_difference,
)
OUT = ROOT / "analysis" / "unbiased_model_comparison_20260929"
YEARS = (2020, 2021, 2022, 2023, 2024)

ARMS = {
    "base63_8": "experiments/wave14_seed_average_20260927/daily_average8_{y}.csv",
    "slow_only8": "analysis/top2_training_validation_20260929/daily_slow_only8_{y}.csv",
    "peer67_slow8": "experiments/wave23_validation_20260928/daily_delivered8_combo_{y}.csv",
    "peer67_slow16": "experiments/wave24_seed16_delivery_20260929/daily_full16_{y}.csv",
    "top2_lightgbm": "analysis/top2_training_validation_20260929/daily_top2_{y}.csv",
}
# Five-year means recorded elsewhere, used only as a sanity check on this recomputation.
KNOWN_FIVE_YEAR = {"base63_8": 0.426866, "slow_only8": 0.427924, "peer67_slow8": 0.427671,
                   "peer67_slow16": 0.428183, "top2_lightgbm": 0.390654}


def load() -> dict:
    frames = {}
    for arm, template in ARMS.items():
        frames[arm] = {}
        for year in YEARS:
            path = ROOT / template.format(y=year)
            if not path.exists():
                raise SystemExit(f"missing daily CSV: {path}")
            frames[arm][year] = pd.read_csv(path)
    return frames


def paired_year_diff(left: pd.DataFrame, right: pd.DataFrame) -> np.ndarray:
    """Mean of paired contributions equals the official annual score delta."""
    return paired_difference(left, right)


def block_bootstrap_year(diff: np.ndarray, year: int, draws: int = 20000, block: int = 20):
    """Moving-block replicate of the ANNUAL mean: draw enough 20-day starts to cover the year,
    concatenate, truncate to the original length, then average. Drawing a single block mean would
    overstate the variance by sqrt(n/block)."""
    rng = np.random.default_rng(20260929 + year)
    n = len(diff)
    n_blocks = int(np.ceil(n / block))
    starts = rng.integers(0, n - block + 1, size=(draws, n_blocks))
    out = np.empty(draws)
    for i in range(draws):
        out[i] = np.concatenate([diff[s:s + block] for s in starts[i]])[:n].mean()
    return out


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    frames = load()
    per_year = {arm: {y: composite(frames[arm][y]) for y in YEARS} for arm in ARMS}

    sanity = {}
    for arm in ARMS:
        mean = float(np.mean([per_year[arm][y] for y in YEARS]))
        sanity[arm] = {"recomputed": mean, "known": KNOWN_FIVE_YEAR[arm],
                       "abs_diff": abs(mean - KNOWN_FIVE_YEAR[arm])}
        if abs(mean - KNOWN_FIVE_YEAR[arm]) > 2e-6:
            raise AssertionError(f"{arm}: recomputed five-year mean {mean:.9f} disagrees with the "
                                 f"recorded {KNOWN_FIVE_YEAR[arm]:.9f}")

    pairs = {}
    for a, b in itertools.combinations(ARMS, 2):
        yearly, draws_by_year = [], []
        for y in YEARS:
            diff = paired_year_diff(frames[a][y], frames[b][y])
            yearly.append(float(diff.mean()))
            draws_by_year.append(block_bootstrap_year(diff, y))
        stacked = np.mean(np.column_stack(draws_by_year), axis=1)
        pairs[f"{a}__vs__{b}"] = {
            "per_year": yearly,
            "five_year_mean": float(np.mean(yearly)),
            "years_positive": int(sum(1 for v in yearly if v > 0)),
            "ci95": [float(np.percentile(stacked, 2.5)), float(np.percentile(stacked, 97.5))],
            "positive_share": float((stacked > 0).mean()),
        }
        expected = np.mean([per_year[a][y] - per_year[b][y] for y in YEARS])
        if not np.isclose(pairs[f"{a}__vs__{b}"]["five_year_mean"], expected,
                          rtol=0, atol=1e-12):
            raise AssertionError(f"{a} minus {b}: five-year delta differs from official scores")

    table = {}
    for arm in ARMS:
        values = [per_year[arm][y] for y in YEARS]
        table[arm] = {"per_year": per_year[arm], "five_year_mean": float(np.mean(values)),
                      "worst_year": float(np.min(values)),
                      "worst_year_name": int(YEARS[int(np.argmin(values))]),
                      "year_sd": float(np.std(values, ddof=1))}

    payload = {
        "status": "complete",
        "completed_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "axis": "2020-2024 same-protocol official-evaluator validation; the only admissible "
                "selection axis because test labels are withheld until after scoring",
        "no_arm_privileged": True,
        "arms": table,
        "pairs": pairs,
        "sanity_against_recorded_means": sanity,
        "metric_denominators": {arm: {y: metric_denominators(frames[arm][y]) for y in YEARS}
                                for arm in ARMS},
        "paired_score_identity_verified": True,
        "method": "per-day paired contributions with fixed per-year denominators; five-year "
                  "difference = equal-weight mean of annual differences; CI95 from 20-day "
                  "moving-block resampling drawn independently per year, 20000 draws, "
                  "seed 20260929+year; non-circular blocks; each arm retains the original "
                  "valid-day denominator of each metric, including N-1 for first-day-missing turnover",
        "caveat": "all five years have been viewed repeatedly; these are retrospective comparisons, "
                  "not blind tests; a CI excluding zero here is evidence about these recorded years "
                  "only",
    }
    (OUT / "comparison_unbiased.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("| arm | " + " | ".join(str(y) for y in YEARS) + " | 5y mean | worst | worst yr | sd |")
    print("|---|" + "---|" * 9)
    for arm in sorted(table, key=lambda a: -table[a]["five_year_mean"]):
        t = table[arm]
        print(f"| {arm} | " + " | ".join(f"{t['per_year'][y]:.6f}" for y in YEARS)
              + f" | {t['five_year_mean']:.6f} | {t['worst_year']:.6f} | {t['worst_year_name']} "
              f"| {t['year_sd']:.6f} |")
    print()
    print("| pair (A-B) | 5y diff | yrs>0 | CI95 | bootstrap positive share |")
    print("|---|---|---|---|---|")
    for key, v in sorted(pairs.items(), key=lambda kv: -abs(kv[1]["five_year_mean"])):
        a, b = key.split("__vs__")
        ci = v["ci95"]
        verdict = "resolvable" if ci[0] > 0 or ci[1] < 0 else "tie"
        print(f"| {a} - {b} | {v['five_year_mean']:+.6f} | {v['years_positive']}/5 | "
              f"[{ci[0]:+.6f}, {ci[1]:+.6f}] {verdict} | {v['positive_share'] * 100:.1f}% |")


if __name__ == "__main__":
    main()
