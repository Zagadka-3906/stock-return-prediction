"""Test-slice paired evidence for the Top-K arm, on the identical instrument.

The 2026-09-29 test-slice comparison covered the four tree arms and the two MLP arms but never the
Top-K backbone, so its +0.0102 lead over the tree cluster existed only as a point estimate. This
adds it with the same paired moving-block intervals and the same 2025/2026 segment split, and
calibrates by reproducing two published intervals from comparison_test_period.json.

LABELLED EVALUATION-SET EVIDENCE: descriptive only, never admissible for selection.
"""
from __future__ import annotations

import itertools
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
    composite, metric_denominators, paired_difference,
)

ARCHIVES = [ROOT.parent / "赛题五_历史归档_20261001", ROOT.parent / "赛题五_清理备份_20261001",
            ROOT.parent / "赛题五_清理备份_20260926_003839"]
KEY = "topk_return_backbone"

DAILY = {
    "base63_8": "analysis/unbiased_model_comparison_20260929/daily_test_base63_8.csv",
    "slow_only8": "analysis/unbiased_model_comparison_20260929/daily_test_slow_only8.csv",
    "peer67_slow8": "analysis/unbiased_model_comparison_20260929/daily_test_peer67_slow8.csv",
    "peer67_slow16": "analysis/unbiased_model_comparison_20260929/daily_test_peer67_slow16.csv",
    "mlp_h64": "analysis/all_models_test_20260929/early/supplemental_scores/"
               "early_nn_control_mlp_h64_f361194a.daily.csv",
    "mlp_h128": "analysis/all_models_test_20260929/early/supplemental_scores/"
                "early_nn_control_mlp_h128_547bdfb7.daily.csv",
    KEY: "analysis/all_models_test_20260929/middle/supplemental_scores/"
         "supplemental_topk_fulltrain2024_2861b604.daily.csv",
}
# Published full-period composites, used as the anchor check on every reused daily file.
KNOWN_FULL = {"base63_8": 0.388007, "slow_only8": 0.388060, "peer67_slow8": 0.386907,
              "peer67_slow16": 0.386058, "mlp_h64": 0.397935, "mlp_h128": 0.398590,
              KEY: 0.39827952757098173}
# Full-precision published intervals are read from comparison_test_period.json at runtime; these
# keys name the three contrasts used to calibrate the rebuilt bootstrap.
PUBLISHED_PAIRS = ("mlp_h128__vs__peer67_slow16", "peer67_slow16__vs__peer67_slow8",
                   "mlp_h128__vs__slow_only8")


def resolve(relative: str) -> Path:
    for archive in ARCHIVES:
        candidate = archive / relative
        if candidate.exists():
            return candidate
    raise SystemExit(f"missing daily CSV: {relative}")


def block_bootstrap(diff: np.ndarray, seed: int = 20260929, draws: int = 20000, block: int = 20):
    """Verbatim from analysis/unbiased_test_comparison.py, including its single fixed seed."""
    rng = np.random.default_rng(seed)
    n = len(diff)
    n_blocks = int(np.ceil(n / block))
    starts = rng.integers(0, n - block + 1, size=(draws, n_blocks))
    out = np.empty(draws)
    for i in range(draws):
        out[i] = np.concatenate([diff[s:s + block] for s in starts[i]])[:n].mean()
    return out


def contrast(daily, a, b, mask=None):
    left, right = daily[a], daily[b]
    if mask is not None:
        left, right = left[mask], right[mask]
    diff = paired_difference(left, right)
    draws = block_bootstrap(diff)
    ci = [float(np.percentile(draws, 2.5)), float(np.percentile(draws, 97.5))]
    return {"days": int(len(diff)), "diff": float(diff.mean()), "ci95": ci,
            "positive_share": float((draws > 0).mean()),
            "verdict": "resolvable_ahead" if ci[0] > 0 else (
                "resolvable_behind" if ci[1] < 0 else "tie")}


def main() -> None:
    daily = {}
    for arm, relative in DAILY.items():
        d = pd.read_csv(resolve(relative))
        d = d[d.trade_date <= 20260605].reset_index(drop=True)
        daily[arm] = d

    anchors = {}
    for arm, d in daily.items():
        got = composite(d)
        anchors[arm] = {"recomputed": got, "published": KNOWN_FULL[arm], "abs_diff": abs(got - KNOWN_FULL[arm])}
        tol = 1e-9 if arm == KEY else 1e-6
        assert abs(got - KNOWN_FULL[arm]) <= tol, f"{arm}: {got:.9f} vs {KNOWN_FULL[arm]}"
        assert len(d) == 343, f"{arm}: {len(d)} days"
    reference = daily["slow_only8"]["trade_date"].to_numpy()
    for arm, d in daily.items():
        assert np.array_equal(d["trade_date"].to_numpy(), reference), f"{arm}: dates not aligned"

    published = json.loads(resolve(
        "analysis/unbiased_model_comparison_20260929/comparison_test_period.json"
    ).read_text(encoding="utf-8"))["pairs"]
    calibration = {}
    for key in PUBLISHED_PAIRS:
        a, b = key.split("__vs__")
        got = contrast(daily, a, b)
        expected = published[key]
        calibration[key] = {
            "recomputed_ci95": got["ci95"], "published_ci95": expected["ci95"],
            "recomputed_diff": got["diff"], "published_diff": expected["full343_diff"],
            "max_abs_diff": max(abs(got["ci95"][0] - expected["ci95"][0]),
                                abs(got["ci95"][1] - expected["ci95"][1]),
                                abs(got["diff"] - expected["full343_diff"])),
        }
        assert calibration[key]["max_abs_diff"] < 5e-7, (key, got, expected)
    print("all seven arms reproduce their published full-period composite; intervals calibrated")

    mask_2025 = (daily[KEY]["trade_date"] < 20260101).to_numpy()
    mask_2026 = ~mask_2025
    opponents = ("slow_only8", "peer67_slow16", "peer67_slow8", "base63_8", "mlp_h128", "mlp_h64")
    topk = {f"{KEY}__vs__{arm}": {"full343": contrast(daily, KEY, arm),
                                  "2025": contrast(daily, KEY, arm, mask_2025),
                                  "2026": contrast(daily, KEY, arm, mask_2026)}
            for arm in opponents}
    tree_pairs = {f"{a}__vs__{b}": contrast(daily, a, b)
                  for a, b in itertools.combinations(
                      ("slow_only8", "peer67_slow16", "peer67_slow8", "base63_8"), 2)}

    payload = {
        "status": "complete", "completed_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "axis": "reconstructed test-period labels, 343 days (2025-01-02..2026-06-05)",
        "evaluation_set_evidence_descriptive_only": True,
        "anchors": anchors, "calibration": calibration,
        "composites": {arm: {"full343": composite(d),
                             "2025": composite(d[d.trade_date < 20260101]),
                             "2026": composite(d[d.trade_date >= 20260101])}
                       for arm, d in daily.items()},
        "topk_contrasts": topk, "tree_pairs": tree_pairs,
        "metric_denominators": {arm: metric_denominators(d) for arm, d in daily.items()},
        "absolute_level_noise_note": "the 2026 slice's annualized-excess term carries about "
                                     "+/-0.046 (1SE); absolute levels there are not skill estimates",
    }
    (HERE / "comparison_test_slice.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"\n| arm | full343 | 2025 | 2026 |")
    print("|---|---|---|---|")
    for arm, d in sorted(daily.items(), key=lambda kv: -composite(kv[1])):
        print(f"| {arm} | {composite(d):.6f} | {composite(d[d.trade_date < 20260101]):.6f} "
              f"| {composite(d[d.trade_date >= 20260101]):.6f} |")
    for label, key in (("full 343d", "full343"), ("2025 (243d)", "2025"), ("2026 (100d)", "2026")):
        print(f"\n| topk - X | {label} diff | CI95 | verdict | P(>0) |")
        print("|---|---|---|---|---|")
        for arm in opponents:
            v = topk[f"{KEY}__vs__{arm}"][key]
            ci = v["ci95"]
            print(f"| {arm} | {v['diff']:+.6f} | [{ci[0]:+.6f}, {ci[1]:+.6f}] | {v['verdict']} "
                  f"| {v['positive_share']*100:.1f}% |")


if __name__ == "__main__":
    main()
