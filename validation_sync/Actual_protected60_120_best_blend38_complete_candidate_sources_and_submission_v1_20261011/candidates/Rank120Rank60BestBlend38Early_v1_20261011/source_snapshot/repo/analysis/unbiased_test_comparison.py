"""Test-period (2025-01-02..2026-06-05, 343 days) paired comparison of the tree arms.

LABELLED EVALUATION-SET EVIDENCE. The competition withholds test labels until after scoring, so
nothing here may select a model; it is reported for completeness and because paired differences on
shared days carry ~12x less noise than absolute levels. Absolute levels in the 2026 slice carry
about +/-0.046 of noise from the annualized-excess term alone and must not be read as skill.

Daily official terms are recomputed from each arm's submission against the locally reconstructed
labels in analysis/frozen_holdout_20260928/data/ using the unmodified evaluate.py.
"""
from __future__ import annotations

import itertools
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import polars as pl

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from experiments.revalidate_fold_local import score_official   # noqa: E402
from analysis.official_score_contributions import (  # noqa: E402
    composite, daily_contribution, metric_denominators, paired_difference,
)

OUT = ROOT / "analysis" / "unbiased_model_comparison_20260929"
DATA = ROOT / "analysis" / "frozen_holdout_20260928" / "data"
YEARS = (2025, 2026)

ARMS = {
    "base63_8": ROOT / "releases/xgboost_seed8_r6/submission.csv",
    "slow_only8": ROOT / "deliveries/slow8_fixed_20260929/submission.csv",
    "peer67_slow8": ROOT / "releases/xgboost_peer67_r10/submission.csv",
    "peer67_slow16": ROOT / "deliveries/peer67_slow16_20260929/submission.csv",
}
# Neural arms already carry scored daily CSVs from the 2026-09-29 sweep (unified-postprocess
# caliber); reuse them instead of rescoring.
EXTRA_DAILY = {
    "mlp_h64": ROOT / "analysis/all_models_test_20260929/early/supplemental_scores/"
                     "early_nn_control_mlp_h64_f361194a.daily.csv",
    "mlp_h128": ROOT / "analysis/all_models_test_20260929/early/supplemental_scores/"
                      "early_nn_control_mlp_h128_547bdfb7.daily.csv",
}


def frame() -> pl.DataFrame:
    x = pd.read_csv(DATA / "测试集_X.csv")
    y = pd.read_csv(DATA / "测试集_Y.csv")
    merged = x.merge(y, on=["ts_code", "trade_date"], how="left")
    merged = merged[merged.trade_date <= 20260605]
    return pl.from_pandas(merged)


def block_bootstrap(diff: np.ndarray, seed: int, draws: int = 20000, block: int = 20):
    rng = np.random.default_rng(seed)
    n = len(diff)
    n_blocks = int(np.ceil(n / block))
    starts = rng.integers(0, n - block + 1, size=(draws, n_blocks))
    out = np.empty(draws)
    for i in range(draws):
        out[i] = np.concatenate([diff[s:s + block] for s in starts[i]])[:n].mean()
    return out


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    base = None
    daily, composites = {}, {}
    for arm, path in ARMS.items():
        out_csv = OUT / f"daily_test_{arm}.csv"
        if out_csv.exists():
            daily[arm] = pd.read_csv(out_csv)
        else:
            if base is None:
                base = frame()
            keys = base.select(["ts_code", "trade_date"])
            sub = pd.read_csv(path)
            sub = sub[sub.trade_date <= 20260605].reset_index(drop=True)
            pred = sub["pred"].to_numpy(float)
            if not np.array_equal(sub[["ts_code", "trade_date"]].to_numpy(),
                                  keys.to_numpy()):
                raise AssertionError(f"{arm}: submission keys not in test-X order")
            metrics, dframe = score_official(base, pred)
            dframe.write_csv(out_csv)
            daily[arm] = dframe.to_pandas()
        d = daily[arm]
        composites[arm] = {
            "full343": composite(d),
            "2025": composite(d[d.trade_date < 20260101]),
            "2026": composite(d[d.trade_date >= 20260101]),
        }
        print(f"{arm}: full {composites[arm]['full343']:.6f} | 2025 {composites[arm]['2025']:.6f} "
              f"| 2026 {composites[arm]['2026']:.6f}")

    for arm, path in EXTRA_DAILY.items():
        d = pd.read_csv(path)
        d = d[d.trade_date <= 20260605].reset_index(drop=True)
        daily[arm] = d
        composites[arm] = {
            "full343": composite(d),
            "2025": composite(d[d.trade_date < 20260101]),
            "2026": composite(d[d.trade_date >= 20260101]),
        }
        print(f"{arm}: full {composites[arm]['full343']:.6f} | 2025 {composites[arm]['2025']:.6f} "
              f"| 2026 {composites[arm]['2026']:.6f}  (reused scored daily csv)")

    pairs = {}
    for a, b in itertools.combinations(sorted(daily), 2):
        diff = paired_difference(daily[a], daily[b])
        draws = block_bootstrap(diff, 20260929)
        pairs[f"{a}__vs__{b}"] = {
            "full343_diff": float(diff.mean()),
            "ci95": [float(np.percentile(draws, 2.5)), float(np.percentile(draws, 97.5))],
            "positive_share": float((draws > 0).mean()),
        }
        expected = composites[a]["full343"] - composites[b]["full343"]
        if not np.isclose(diff.mean(), expected, rtol=0, atol=1e-12):
            raise AssertionError(f"{a} minus {b}: test-period delta differs from official scores")
    payload = {
        "status": "complete",
        "completed_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "axis": "reconstructed test-period labels, 343 days; EVALUATION-SET EVIDENCE, admissible "
                "for description only, never for selection",
        "composites": composites,
        "pairs": pairs,
        "metric_denominators": {arm: metric_denominators(d) for arm, d in daily.items()},
        "paired_score_identity_verified": True,
        "method": "20000 non-circular 20-day moving-block draws, seed 20260929; "
                  "original valid-day denominator for each metric in each arm; "
                  "bootstrap positive share is descriptive, not a future-win probability",
        "absolute_level_noise_note": "the 2026 slice's annualized-excess term carries about "
                                     "+/-0.046 (1SE); absolute levels there are not skill estimates",
    }
    (OUT / "comparison_test_period.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print()
    print("| pair (A-B) | full343 diff | CI95 | bootstrap positive share |")
    print("|---|---|---|---|")
    for key, v in sorted(pairs.items(), key=lambda kv: -abs(kv[1]["full343_diff"])):
        a, b = key.split("__vs__")
        ci = v["ci95"]
        verdict = "resolvable" if ci[0] > 0 or ci[1] < 0 else "tie"
        print(f"| {a} - {b} | {v['full343_diff']:+.6f} | [{ci[0]:+.6f}, {ci[1]:+.6f}] {verdict} | "
              f"{v['positive_share'] * 100:.1f}% |")


if __name__ == "__main__":
    main()
