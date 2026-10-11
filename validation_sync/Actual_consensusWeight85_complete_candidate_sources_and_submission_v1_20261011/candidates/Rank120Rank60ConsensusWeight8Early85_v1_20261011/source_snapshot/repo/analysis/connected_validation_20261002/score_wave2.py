"""Wave 2: score every candidate whose FINAL per-fold predictions survive, under the connected caliber.

Identical treatment for all: same combined frame, same unmodified evaluate.py, same five validation
years, and each arm's frozen annual composites asserted first where a published record exists. No
test-period data is read. Candidates whose artifacts are incomplete (missing years) or absent are
listed at the end as unscoreable rather than silently dropped.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import polars as pl

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
import connected_scorer as cs  # noqa: E402

ARCHIVE = ROOT.parent / "赛题五_历史归档_20261001"
CLEANUP = ROOT.parent / "赛题五_清理备份_20261001"
R4 = ARCHIVE / "experiments/revalidation_20260926/validation"
YEARS = cs.YEARS
KEYS = cs.KEYS

# Published per-year composites, full precision, used as the calibration target where available.
PUBLISHED = ARCHIVE / "analysis/unbiased_model_comparison_20260929/comparison_unbiased.json"

CANDIDATES = {
    "base63_8": CLEANUP / "experiments/wave14_seed_average_20260927/predictions_average8_{y}.parquet",
    "slow_only8": ARCHIVE / "analysis/slow8_monthly_validation_20260929/predictions_fixed_{y}.parquet",
    "slow8_monthly": ARCHIVE / "analysis/slow8_monthly_validation_20260929/predictions_monthly_{y}.parquet",
    "top2_lightgbm": ARCHIVE / "analysis/top2_training_validation_20260929/predictions_top2_{y}.parquet",
    "ensemble4_r4": R4 / "predictions_ensemble4_{y}.parquet",
    "ensemble4_old_pruned": R4 / "predictions_old_ensemble4_{y}.parquet",
    "pooled_rms25": R4 / "predictions_baseline_{y}.parquet",
    "xgboost_single_seed2026": R4 / "predictions_xgboost_{y}.parquet",
    "xgb_two_mean": ARCHIVE / "experiments/optimization_r5_20260926/predictions_xgb_two_mean_{y}.parquet",
}
# Filled in at runtime if the wave11/12 directories are found.
OPTIONAL = {
    "W11b_early_stop": "experiments/wave11_*/predictions_W11b_*_{y}.parquet",
    "W12c_trailing_ic_two": "experiments/wave12_*/predictions_W12c_*_{y}.parquet",
}
# Names as they appear in the published comparison, for calibration.
PUBLISHED_ALIAS = {"base63_8": "base63_8", "slow_only8": "slow_only8",
                   "top2_lightgbm": "top2_lightgbm", "peer67_slow8": "peer67_slow8",
                   "peer67_slow16": "peer67_slow16"}


def resolve_glob(pattern: str, year: int):
    filled = pattern.replace("{y}", str(year))
    for root in (ARCHIVE, CLEANUP):
        hits = sorted(root.glob(filled))
        if hits:
            return hits[0]
    return None


def load_final(path: Path, year: int) -> np.ndarray:
    """Load a per-fold FINAL prediction column, sorted to the combined frame's key order."""
    df = pl.read_parquet(path)
    for column in ("pred", "pred_final"):
        if column in df.columns:
            df = df.sort("trade_date", "ts_code")
            reference = pl.read_parquet(R4 / f"predictions_ensemble4_{year}.parquet").sort(
                "trade_date", "ts_code").select(KEYS)
            if not df.select(KEYS).equals(reference):
                raise AssertionError(f"{path.name}: keys do not match the fold frame")
            return df[column].to_numpy().astype(np.float64)
    raise AssertionError(f"{path.name}: no final pred column in {df.columns}")


def main() -> None:
    frame = cs.combined_frame()
    published = json.loads(PUBLISHED.read_text(encoding="utf-8"))["arms"]

    for name, pattern in list(OPTIONAL.items()):
        if all(resolve_glob(pattern, y) is not None for y in YEARS):
            CANDIDATES[name] = pattern

    results = {}
    unscoreable = {}
    for name, pattern in CANDIDATES.items():
        paths = {}
        missing = []
        for year in YEARS:
            path = resolve_glob(str(pattern), year) if "*" in str(pattern) else Path(
                str(pattern).format(y=year))
            if path is None or not path.exists():
                missing.append(year)
            else:
                paths[year] = path
        if missing:
            unscoreable[name] = {"reason": "missing years", "missing": missing,
                                 "found": {str(k): str(v) for k, v in paths.items()}}
            cs.log(f"{name}: UNSCOREABLE, missing years {missing}")
            continue

        targets = None
        alias = PUBLISHED_ALIAS.get(name)
        if alias and alias in published:
            targets = {y: published[alias]["per_year"][str(y)] for y in YEARS}
        try:
            preds = {y: load_final(paths[y], y) for y in YEARS}
            results[name] = cs.score_arm_dict(frame, preds, name, frozen_annual=targets,
                                              tolerance=1e-9 if targets else 2e-9)
        except Exception as error:
            unscoreable[name] = {"reason": f"{type(error).__name__}: {error}"}
            cs.log(f"{name}: FAILED - {type(error).__name__}: {error}")

    prior = json.loads((HERE / "connected_results_wave1.json").read_text(encoding="utf-8"))
    merged = dict(prior["results"])
    merged.update(results)
    ranked = sorted(merged.items(), key=lambda kv: -kv[1]["connected_final_score"])

    payload = {
        "status": "complete", "completed_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "caliber": prior["caliber"], "standard": prior["standard"],
        "no_test_period_data_read": True,
        "frame": prior["frame"], "turnover_accounting": prior["turnover_accounting"],
        "wave2_candidates_requested": list(CANDIDATES),
        "results": merged,
        "unscoreable": unscoreable,
        "ranking_by_connected_score": [
            {"rank": i + 1, "name": name, "connected_final_score": r["connected_final_score"],
             "five_year_mean_diagnostic": r["five_year_equal_weight_mean_diagnostic_only"],
             "ic": r["connected_metrics"]["ic_mean"],
             "annual_excess": r["connected_metrics"]["annual_excess"],
             "turnover": r["connected_metrics"]["mean_turnover"]}
            for i, (name, r) in enumerate(ranked)],
    }
    (HERE / "connected_results_all.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("\n| rank | candidate | CONNECTED 2020-2024 | IC | ann.excess | turnover | 5y mean (diag) |")
    print("|---|---|---|---|---|---|---|")
    for i, (name, r) in enumerate(ranked):
        m = r["connected_metrics"]
        print(f"| {i+1} | {name} | **{r['connected_final_score']:.9f}** | {m['ic_mean']:.6f} | "
              f"{m['annual_excess']:.6f} | {m['mean_turnover']:.6f} | "
              f"{r['five_year_equal_weight_mean_diagnostic_only']:.9f} |")
    print("\nunscoreable from surviving artifacts:")
    for name, info in unscoreable.items():
        print(f"  {name}: {info.get('reason')} {info.get('missing', '')}")


if __name__ == "__main__":
    main()
