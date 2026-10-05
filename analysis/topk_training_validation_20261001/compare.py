"""Apply the pre-declared interpretation rule to the completed Top-K row.

Reads the frozen 2020-2022 daily evidence from the archive, the new 2023/2024 daily evidence from
this directory, and every tree arm's daily evidence, then reports the five-year paired contrasts on
the admissible axis with the calibrated 20-day moving-block instrument. Also decomposes the contrast
into its IC / excess / turnover contributions, because the Top-K arm's whole profile is a trade of
cross-sectional IC for Top-set excess and the composite weights them 0.4 / 0.3.
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
from analysis.official_score_contributions import (  # noqa: E402
    WEIGHTS, composite, metric_denominators, paired_difference,
)

ARCHIVES = [
    ROOT.parent / "赛题五_历史归档_20261001",
    ROOT.parent / "赛题五_清理备份_20261001",
    ROOT.parent / "赛题五_清理备份_20260926_003839",
]
YEARS = (2020, 2021, 2022, 2023, 2024)
KEY = "topk_return_backbone"

ARMS = {
    "base63_8": "experiments/wave14_seed_average_20260927/daily_average8_{y}.csv",
    "slow_only8": "analysis/top2_training_validation_20260929/daily_slow_only8_{y}.csv",
    "peer67_slow8": "experiments/wave23_validation_20260928/daily_delivered8_combo_{y}.csv",
    "peer67_slow16": "experiments/wave24_seed16_delivery_20260929/daily_full16_{y}.csv",
    "top2_lightgbm": "analysis/top2_training_validation_20260929/daily_top2_{y}.csv",
}
TOPK_SOURCES = {
    2020: "experiments/r6_topk_20260926/daily_topk_return_backbone_2020.csv",
    2021: "experiments/r6_topk_20260926/daily_topk_return_backbone_2021.csv",
    2022: "experiments/r6_topk_20260926/daily_topk_return_backbone_2022.csv",
    2023: None,  # this directory
    2024: None,
}
KNOWN_FIVE_YEAR = {"base63_8": 0.426866, "slow_only8": 0.427924, "peer67_slow8": 0.427671,
                   "peer67_slow16": 0.428183, "top2_lightgbm": 0.390654}
PUBLISHED_CI = {("top2_lightgbm", "slow_only8"): (-0.060428, -0.006207)}


def resolve(relative: str) -> Path:
    for archive in ARCHIVES:
        candidate = archive / relative
        if candidate.exists():
            return candidate
    raise SystemExit(f"missing daily CSV: {relative}")


def block_bootstrap_year(diff: np.ndarray, year: int, draws: int = 20000, block: int = 20):
    """Verbatim from analysis/unbiased_tree_comparison.py - same seeds, same block construction."""
    rng = np.random.default_rng(20260929 + year)
    n = len(diff)
    n_blocks = int(np.ceil(n / block))
    starts = rng.integers(0, n - block + 1, size=(draws, n_blocks))
    out = np.empty(draws)
    for i in range(draws):
        out[i] = np.concatenate([diff[s:s + block] for s in starts[i]])[:n].mean()
    return out


def contrast(frames, a, b, years=YEARS):
    yearly, draws_by_year = [], []
    for y in years:
        diff = paired_difference(frames[a][y], frames[b][y])
        yearly.append(float(diff.mean()))
        draws_by_year.append(block_bootstrap_year(diff, y))
    stacked = np.mean(np.column_stack(draws_by_year), axis=1)
    ci = [float(np.percentile(stacked, 2.5)), float(np.percentile(stacked, 97.5))]
    verdict = "resolvable_ahead" if ci[0] > 0 else ("resolvable_behind" if ci[1] < 0 else "tie")
    return {"per_year": {str(y): v for y, v in zip(years, yearly)},
            "five_year_mean": float(np.mean(yearly)),
            "years_positive": int(sum(1 for v in yearly if v > 0)),
            "n_years": len(years), "ci95": ci,
            "positive_share": float((stacked > 0).mean()), "verdict": verdict}


def term_decomposition(frames, a, b, years=YEARS):
    """Split the composite gap into the three official terms, per year and on average."""
    out = {}
    for y in years:
        left, right = frames[a][y], frames[b][y]
        row = {}
        for name, weight in WEIGHTS.items():
            ln, rn = metric_denominators(left), metric_denominators(right)
            row[name] = weight * (left[name].mean() - right[name].mean())
            row[f"{name}_level_left"] = float(left[name].mean())
            row[f"{name}_level_right"] = float(right[name].mean())
            row["_denominators"] = {"left": ln, "right": rn}
        row["total"] = row["rank_ic"] + row["excess"] + row["turnover"]
        assert abs(row["total"] - (composite(left) - composite(right))) <= 1e-12
        out[str(y)] = row
    out["five_year_mean"] = {name: float(np.mean([out[str(y)][name] for y in years]))
                            for name in ("rank_ic", "excess", "turnover", "total")}
    return out


def main() -> None:
    frames = {}
    for arm, template in ARMS.items():
        frames[arm] = {y: pd.read_csv(resolve(template.format(y=y))) for y in YEARS}
    frames[KEY] = {}
    for year in YEARS:
        source = TOPK_SOURCES[year]
        path = resolve(source) if source else HERE / f"daily_{KEY}_{year}.csv"
        frames[KEY][year] = pd.read_csv(path)

    per_year = {arm: {str(y): composite(d) for y, d in years.items()} for arm, years in frames.items()}
    five_year = {arm: float(np.mean(list(values.values()))) for arm, values in per_year.items()}

    checks = {}
    for arm, published in KNOWN_FIVE_YEAR.items():
        checks[arm] = {"recomputed": five_year[arm], "published": published,
                       "abs_diff": abs(five_year[arm] - published)}
        assert abs(five_year[arm] - published) <= 2e-6, arm
    proof = json.loads((HERE / "harness_proof.json").read_text(encoding="utf-8"))
    assert proof["passed"] and proof["max_abs_metric_diff"] <= 1e-12
    calibration = {}
    for (a, b), expected in PUBLISHED_CI.items():
        got = contrast(frames, a, b)["ci95"]
        calibration[f"{a}__vs__{b}"] = {"recomputed": got, "published": list(expected),
                                        "max_abs_diff": max(abs(got[0] - expected[0]),
                                                            abs(got[1] - expected[1]))}
        assert calibration[f"{a}__vs__{b}"]["max_abs_diff"] < 5e-7
    print("anchors reproduce; bootstrap calibrated against the published interval")

    pairs = {f"{KEY}__vs__{arm}": contrast(frames, KEY, arm)
             for arm in ("slow_only8", "peer67_slow16", "peer67_slow8", "base63_8", "top2_lightgbm")}
    decomposition = {f"{KEY}__vs__{arm}": term_decomposition(frames, KEY, arm)
                     for arm in ("slow_only8", "peer67_slow16")}
    # the partial three-year row, for continuity with what was known before this run
    partial = contrast(frames, KEY, "slow_only8", years=(2020, 2021, 2022))

    rule = json.loads((HERE / "protocol.json").read_text(encoding="utf-8"))[
        "predeclared_interpretation_rule"]
    primary = pairs[f"{KEY}__vs__slow_only8"]
    applied = {"rule_branch": rule[{"resolvable_behind": "ci95_entirely_below_zero",
                                    "tie": "ci95_crosses_zero",
                                    "resolvable_ahead": "ci95_entirely_above_zero"}[primary["verdict"]]],
               "verdict": primary["verdict"], "five_year_mean": primary["five_year_mean"],
               "ci95": primary["ci95"]}

    protocol_sha = hashlib.sha256((HERE / "protocol.json").read_bytes()).hexdigest()
    payload = {
        "status": "complete",
        "completed_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "protocol_sha256": protocol_sha,
        "descriptive_only": True, "promotes_or_adopts_nothing": True,
        "harness_proof": {"year": proof["year"], "max_abs_metric_diff": proof["max_abs_metric_diff"],
                          "passed": proof["passed"]},
        "anchor_and_calibration": {"five_year_means": checks, "bootstrap": calibration},
        "per_year_composite": per_year,
        "five_year_mean": five_year,
        "topk_pairs_five_year": pairs,
        "topk_partial_three_year_vs_slow_only8": partial,
        "term_decomposition": decomposition,
        "predeclared_rule_applied": applied,
        "metric_denominators": {arm: {str(y): metric_denominators(d) for y, d in years.items()}
                                for arm, years in frames.items()},
    }
    (HERE / "comparison.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                                          encoding="utf-8")

    print(f"\n| arm | " + " | ".join(str(y) for y in YEARS) + " | 5y mean |")
    print("|---|" + "---|" * 7)
    for arm in sorted(five_year, key=lambda a: -five_year[a]):
        print(f"| {arm} | " + " | ".join(f"{per_year[arm][str(y)]:.6f}" for y in YEARS)
              + f" | {five_year[arm]:.6f} |")
    print(f"\n| pair ({KEY} - X) | 5y diff | yrs>0 | CI95 | verdict | P(>0) |")
    print("|---|---|---|---|---|---|")
    for key, v in pairs.items():
        ci = v["ci95"]
        print(f"| {key.replace('__vs__', ' - ')} | {v['five_year_mean']:+.6f} | "
              f"{v['years_positive']}/{v['n_years']} | [{ci[0]:+.6f}, {ci[1]:+.6f}] | "
              f"{v['verdict']} | {v['positive_share']*100:.1f}% |")
    print(f"\nper-year topk - slow_only8: "
          + " ".join(f"{y}:{primary['per_year'][str(y)]:+.6f}" for y in YEARS))
    print("\nterm decomposition (topk - slow_only8), five-year mean contribution:")
    for name in ("rank_ic", "excess", "turnover", "total"):
        print(f"  {name:9s} {decomposition[f'{KEY}__vs__slow_only8']['five_year_mean'][name]:+.6f}")
    print("\npre-declared rule ->", applied["rule_branch"])


if __name__ == "__main__":
    main()
