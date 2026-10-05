"""Re-verify the admissible-axis comparison from the frozen daily CSVs, and calibrate the instrument.

Read-only. Trusts no markdown: every five-year mean and every paired CI quoted in
analysis/unbiased_model_comparison_20260929/模型无偏对比.md is recomputed here from the daily
evidence, and the bootstrap is calibrated by demanding it reproduce the published
top2-vs-slow_only8 interval [-0.060428, -0.006207] before any new arm is measured with it.

Adds the partial Top-K row (frozen 2020-2022 dev folds) against the tree cluster.
"""
from __future__ import annotations

import itertools
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.official_score_contributions import (  # noqa: E402
    composite, metric_denominators, paired_difference,
)

# The 2026-10-01 cleanup split the historical artifacts across two preserved trees.
ARCHIVES = [
    ROOT.parent / "赛题五_历史归档_20261001",
    ROOT.parent / "赛题五_清理备份_20261001",
    ROOT.parent / "赛题五_清理备份_20260926_003839",
]
OUT = Path(__file__).resolve().parent
YEARS = (2020, 2021, 2022, 2023, 2024)

ARMS = {
    "base63_8": "experiments/wave14_seed_average_20260927/daily_average8_{y}.csv",
    "slow_only8": "analysis/top2_training_validation_20260929/daily_slow_only8_{y}.csv",
    "peer67_slow8": "experiments/wave23_validation_20260928/daily_delivered8_combo_{y}.csv",
    "peer67_slow16": "experiments/wave24_seed16_delivery_20260929/daily_full16_{y}.csv",
    "top2_lightgbm": "analysis/top2_training_validation_20260929/daily_top2_{y}.csv",
    # Frozen 2026-09-26 development folds; 2023/2024 were never run because the dev gate failed.
    "topk_return_backbone": "experiments/r6_topk_20260926/daily_topk_return_backbone_{y}.csv",
}
KNOWN_FIVE_YEAR = {"base63_8": 0.426866, "slow_only8": 0.427924, "peer67_slow8": 0.427671,
                   "peer67_slow16": 0.428183, "top2_lightgbm": 0.390654}
# Published intervals from 模型无偏对比.md, used to calibrate the rebuilt bootstrap.
PUBLISHED_CI = {
    ("top2_lightgbm", "slow_only8"): (-0.060428, -0.006207),
    ("base63_8", "slow_only8"): (-0.002112, -0.000211),
    ("peer67_slow8", "peer67_slow16"): (-0.000926, +0.000279),
}
TOPK_FROZEN_SCORE = {2020: 0.40707290913686545, 2021: 0.4152844359357778, 2022: 0.42089053197633397}


def resolve(relative: str, required: bool = True):
    for archive in ARCHIVES:
        candidate = archive / relative
        if candidate.exists():
            return candidate
    if required:
        raise SystemExit(f"missing daily CSV in any archive: {relative}")
    return None


def block_bootstrap_year(diff: np.ndarray, year: int, draws: int = 20000, block: int = 20):
    """Verbatim copy of the instrument in analysis/unbiased_tree_comparison.py."""
    rng = np.random.default_rng(20260929 + year)
    n = len(diff)
    n_blocks = int(np.ceil(n / block))
    starts = rng.integers(0, n - block + 1, size=(draws, n_blocks))
    out = np.empty(draws)
    for i in range(draws):
        out[i] = np.concatenate([diff[s:s + block] for s in starts[i]])[:n].mean()
    return out


def pair(frames, a, b, years):
    yearly, draws_by_year = [], []
    for y in years:
        diff = paired_difference(frames[a][y], frames[b][y])
        yearly.append(float(diff.mean()))
        draws_by_year.append(block_bootstrap_year(diff, y))
    stacked = np.mean(np.column_stack(draws_by_year), axis=1)
    ci = [float(np.percentile(stacked, 2.5)), float(np.percentile(stacked, 97.5))]
    return {"per_year": yearly, "n_years": len(years),
            "mean": float(np.mean(yearly)),
            "years_positive": int(sum(1 for v in yearly if v > 0)),
            "ci95": ci, "positive_share": float((stacked > 0).mean()),
            "verdict": "resolvable" if ci[0] > 0 or ci[1] < 0 else "tie"}


def main() -> None:
    frames = {}
    for arm, template in ARMS.items():
        required = arm != "topk_return_backbone"
        frames[arm] = {}
        for year in YEARS:
            path = resolve(template.format(y=year), required=required)
            if path is not None:
                frames[arm][year] = pd.read_csv(path)
    available = {arm: sorted(d) for arm, d in frames.items()}
    print("daily CSV coverage:", json.dumps({k: [str(y) for y in v] for k, v in available.items()}))

    # 1. every arm's own annual composite must reproduce its published value
    per_year = {arm: {y: composite(d) for y, d in years.items()} for arm, years in frames.items()}
    sanity = {}
    for arm in ARMS:
        if len(frames[arm]) != 5:
            continue
        mean = float(np.mean([per_year[arm][y] for y in YEARS]))
        sanity[arm] = {"recomputed": mean, "published": KNOWN_FIVE_YEAR[arm],
                       "abs_diff": abs(mean - KNOWN_FIVE_YEAR[arm])}
        assert abs(mean - KNOWN_FIVE_YEAR[arm]) <= 2e-6, f"{arm}: {mean:.9f} vs {KNOWN_FIVE_YEAR[arm]}"
    # the Top-K folds must reproduce the frozen development record
    topk_check = {}
    for year, expected in TOPK_FROZEN_SCORE.items():
        got = per_year["topk_return_backbone"][year]
        topk_check[str(year)] = {"recomputed": got, "frozen": expected, "abs_diff": abs(got - expected)}
        assert abs(got - expected) <= 1e-12, f"topk {year}: {got!r} vs {expected!r}"
    print("five-year means reproduce published values; topk folds reproduce the frozen record to 1e-12")

    # 2. calibrate the rebuilt bootstrap against published intervals
    calibration = {}
    for (a, b), expected in PUBLISHED_CI.items():
        got = pair(frames, a, b, YEARS)["ci95"]
        calibration[f"{a}__vs__{b}"] = {"recomputed": got, "published": list(expected),
                                        "max_abs_diff": max(abs(got[0] - expected[0]), abs(got[1] - expected[1]))}
        assert max(abs(got[0] - expected[0]), abs(got[1] - expected[1])) < 5e-7, \
            f"bootstrap not calibrated on {a} vs {b}: {got} vs {expected}"
    print("bootstrap calibrated: all three published intervals reproduced to <5e-7")

    # 3. the tree-cluster table, recomputed
    tree = {}
    for arm in ("base63_8", "slow_only8", "peer67_slow8", "peer67_slow16"):
        values = [per_year[arm][y] for y in YEARS]
        tree[arm] = {"per_year": {str(y): per_year[arm][y] for y in YEARS},
                     "five_year_mean": float(np.mean(values)), "worst_year": float(np.min(values)),
                     "worst_year_name": int(YEARS[int(np.argmin(values))]),
                     "year_sd": float(np.std(values, ddof=1))}

    # 4. the partial Top-K row: frozen 2020-2022 against every admissible arm
    topk_years = sorted(frames["topk_return_backbone"])
    topk_pairs = {}
    for arm in ("slow_only8", "peer67_slow16", "peer67_slow8", "base63_8", "top2_lightgbm"):
        topk_pairs[f"topk__vs__{arm}"] = pair(frames, "topk_return_backbone", arm, topk_years)

    payload = {
        "status": "complete",
        "completed_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "purpose": "independent re-verification of the admissible-axis comparison plus the partial "
                   "Top-K row; read-only, no candidate scored, no release touched",
        "coverage": {arm: [int(y) for y in years] for arm, years in available.items()},
        "five_year_mean_check": sanity,
        "topk_frozen_fold_check": topk_check,
        "bootstrap_calibration": calibration,
        "tree_arms": tree,
        "topk_partial_pairs_2020_2022": topk_pairs,
        "metric_denominators": {arm: {str(y): metric_denominators(d) for y, d in years.items()}
                                for arm, years in frames.items()},
        "caveat": "all five years have been viewed repeatedly across ~24 prior rounds; these are "
                  "retrospective comparisons, not blind tests",
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "verification.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                                           encoding="utf-8")

    print("\n| arm | " + " | ".join(str(y) for y in YEARS) + " | 5y mean | worst | sd |")
    print("|---|" + "---|" * 8)
    for arm, t in sorted(tree.items(), key=lambda kv: -kv[1]["five_year_mean"]):
        print(f"| {arm} | " + " | ".join(f"{t['per_year'][str(y)]:.6f}" for y in YEARS)
              + f" | {t['five_year_mean']:.6f} | {t['worst_year']:.6f} ({t['worst_year_name']}) "
              f"| {t['year_sd']:.6f} |")
    print(f"\nTop-K partial row, years {topk_years}: "
          + " | ".join(f"{per_year['topk_return_backbone'][y]:.6f}" for y in topk_years))
    print("\n| pair (topk - X) | mean | yrs>0 | CI95 | verdict | P(>0) |")
    print("|---|---|---|---|---|---|")
    for key, v in topk_pairs.items():
        ci = v["ci95"]
        print(f"| {key.replace('__vs__', ' - ')} | {v['mean']:+.6f} | {v['years_positive']}/{v['n_years']} "
              f"| [{ci[0]:+.6f}, {ci[1]:+.6f}] | {v['verdict']} | {v['positive_share']*100:.1f}% |")


if __name__ == "__main__":
    main()
