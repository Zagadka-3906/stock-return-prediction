"""Lock the three-seed choice using the unmodified competition evaluator.

Only the requested year's original float64 labels are loaded by official_score.
The command-line entry point evaluates 2022/2023 only. Daily evidence is rebuilt
from the same CSV bytes read by evaluate.py, including pandas' default tie sort.
"""
from __future__ import annotations

import json
import tempfile
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd
import polars as pl
from scipy.stats import spearmanr

from evaluate import evaluate
from experiments.seed_ensemble import (
    MODES, OUT, SEEDS, YEARS, file_hash, load_panel, load_seed_raw,
    make_prediction,
)
from run import ROOT
from src.scoring import Panel


@lru_cache(maxsize=3)
def original_labels(year: int) -> pl.DataFrame:
    if year not in (2022, 2023, 2024):
        raise ValueError("Only established annual validation folds are supported")
    return (
        pl.scan_csv(
            ROOT / "data" / "raw" / "训练集.csv",
            schema_overrides={"ts_code": pl.String, "trade_date": pl.Int32,
                              "y_ret_1d": pl.Float64},
            null_values=["NaN", "nan", ""],
        )
        .filter(pl.col("trade_date").is_between(year * 10000 + 101,
                                               year * 10000 + 1231))
        .select("ts_code", "trade_date", "y_ret_1d")
        .collect()
    )


def _same_csv_daily(folder: Path) -> tuple[dict, pl.DataFrame]:
    """Reproduce evaluate.py operations, not the project's stable-sort scorer."""
    prediction = pd.read_csv(folder / "submission.csv")
    labels = pd.read_csv(folder / "测试集_Y.csv")
    flags = pd.read_csv(folder / "测试集_X.csv",
                        usecols=["ts_code", "trade_date", "flag_limit_up"])
    merged = prediction.merge(labels, on=["ts_code", "trade_date"], how="inner")
    merged = merged.merge(flags, on=["ts_code", "trade_date"], how="inner")
    records = {}
    ic_values, excess_values, top_values, turnovers = [], [], [], []
    for date, group in merged.groupby("trade_date"):
        record = {"trade_date": int(date), "rank_ic": np.nan,
                  "excess": np.nan, "top1_return": np.nan, "turnover": np.nan}
        valid = group.dropna(subset=["y_ret_1d"])
        if len(valid) >= 30:
            ic, _ = spearmanr(valid["pred"], valid["y_ret_1d"])
            record["rank_ic"] = float(ic)
            ic_values.append(ic)
        valid = group[(group["flag_limit_up"] == 0)
                      & group["y_ret_1d"].notna()].copy()
        if len(valid) >= 100:
            # Deliberately omit kind: the official evaluator uses the default.
            valid = valid.sort_values("pred", ascending=False).reset_index(drop=True)
            n_top = max(len(valid) // 10, 1)
            top_return = valid["y_ret_1d"].iloc[:n_top].mean()
            excess = top_return - valid["y_ret_1d"].mean()
            record["top1_return"], record["excess"] = float(top_return), float(excess)
            top_values.append(top_return)
            excess_values.append(excess)
        records[int(date)] = record

    previous = None
    for date in sorted(merged["trade_date"].unique()):
        group = merged[merged["trade_date"] == date]
        valid = group[group["flag_limit_up"] == 0].copy()
        if len(valid) < 100:
            previous = None
            continue
        valid = valid.sort_values("pred", ascending=False)
        current = set(valid["ts_code"].iloc[:max(len(valid) // 10, 1)])
        if previous is not None and len(previous) > 0:
            turnover = 1.0 - len(current & previous) / len(current | previous)
            records[int(date)]["turnover"] = float(turnover)
            turnovers.append(turnover)
        previous = current

    mean_ic = np.mean(ic_values)
    ic_std = np.std(ic_values, ddof=1)
    annual_excess = np.mean(excess_values) * 252
    mean_turnover = np.mean(turnovers)
    metrics = {
        "ic_mean": float(mean_ic), "ic_std": float(ic_std),
        "icir": float(mean_ic / ic_std if ic_std > 0 else 0),
        "ic_positive_ratio": float(np.mean(np.array(ic_values) > 0)),
        "annual_excess": float(annual_excess),
        "top1_annual_ret": float(np.mean(top_values) * 252),
        "mean_turnover": float(mean_turnover),
        "final_score": float(mean_ic * .4 + annual_excess * .3
                             + (1 - mean_turnover) * .3),
    }
    return metrics, pl.DataFrame([records[date] for date in sorted(records)])


def official_score(panel: Panel, prediction: np.ndarray,
                   year: int) -> tuple[dict, pl.DataFrame]:
    """Call the original evaluator and return verified matching daily evidence."""
    if not np.all((panel.dates >= year * 10000 + 101)
                  & (panel.dates <= year * 10000 + 1231)):
        raise ValueError("Panel contains dates outside the requested label year")
    prediction = np.asarray(prediction, dtype=float).reshape(-1)
    if len(prediction) != len(panel.frame) or not np.isfinite(prediction).all():
        raise ValueError("Predictions must be finite and aligned with every panel row")
    labels = original_labels(year)
    keys = panel.frame.select("ts_code", "trade_date")
    if len(labels) != len(keys) or not keys.join(labels.select("ts_code", "trade_date"),
                                               on=["ts_code", "trade_date"],
                                               how="anti").is_empty():
        raise ValueError("Original-year label keys do not match the validation panel")
    frame = panel.frame.drop("y_ret_1d").join(
        labels, on=["ts_code", "trade_date"], how="left", validate="1:1"
    ).sort("trade_date", "ts_code")
    if not frame.select("ts_code", "trade_date").equals(keys):
        raise AssertionError("Label join changed prediction row order")
    with tempfile.TemporaryDirectory(prefix="official-seed-score-") as temporary:
        folder = Path(temporary)
        keys.with_columns(pl.Series("pred", prediction)).write_csv(
            folder / "submission.csv", float_precision=17)
        frame.select("ts_code", "trade_date", "flag_limit_up").write_csv(folder / "测试集_X.csv")
        frame.select("ts_code", "trade_date", "y_ret_1d").write_csv(
            folder / "测试集_Y.csv", float_precision=17)
        official = {key: float(value) for key, value in
                    evaluate(str(folder / "submission.csv"), str(folder)).items()}
        rebuilt, daily = _same_csv_daily(folder)
    if set(official) != set(rebuilt):
        raise AssertionError("Daily reconstruction metric keys differ from the original evaluator")
    for key, value in official.items():
        if not np.isfinite(value) or abs(value - rebuilt[key]) > 1e-12:
            raise AssertionError((year, key, value, rebuilt[key]))
    return official, daily


def verify_development_sources(development: dict) -> None:
    if development["selection_years"] != list(YEARS):
        raise AssertionError("Unexpected development years")
    if development["experiment_source_sha256"] != file_hash(ROOT / "experiments/seed_ensemble.py"):
        raise AssertionError("Experiment source changed after development selection")
    for relative, expected_hash in development["artifacts_sha256"].items():
        if file_hash(ROOT / relative) != expected_hash:
            raise AssertionError(f"Development artifact changed: {relative}")


def main() -> None:
    development_path = OUT / "development.json"
    development_sha = file_hash(development_path)
    development = json.loads(development_path.read_text(encoding="utf-8"))
    verify_development_sources(development)
    result = {
        "selection_years": list(YEARS), "development_sha256": development_sha,
        "selection_rule": "maximize_minimum_official_annual_score_2022_2023; exact ties prefer MODES order",
        "tie_policy_note": "Unmodified evaluate.py with pandas default descending sort_values; daily evidence reconstructed from the identical CSV files loaded through pandas.read_csv. No artificial tie breaking.",
        "original_evaluator_sha256": file_hash(ROOT / "evaluate.py"),
        "official_reconstruction_source_sha256": file_hash(Path(__file__)),
        "source_and_artifact_fingerprints_verified": True,
        "daily_reconstruction_metric_tolerance": 1e-12,
        "candidates": {mode: {"years": {}} for mode in MODES},
        "project_score_differences": {mode: {} for mode in MODES},
    }
    for year in YEARS:
        panel = load_panel(year)
        raws = {seed: load_seed_raw(year, seed, panel) for seed in SEEDS}
        for mode in MODES:
            official, daily = official_score(panel, make_prediction(panel, raws, mode), year)
            result["candidates"][mode]["years"][str(year)] = official
            result["project_score_differences"][mode][str(year)] = (
                official["final_score"] - development["candidates"][mode]["years"][str(year)]["final_score"]
            )
            daily.write_csv(OUT / f"official_{mode}_{year}_daily.csv")
            print(f"OFFICIAL {year} {mode}: {official['final_score']:.12f}", flush=True)
    for candidate in result["candidates"].values():
        candidate["minimum_annual_score"] = min(
            candidate["years"][str(year)]["final_score"] for year in YEARS
        )
    result["selected_mode"] = max(MODES, key=lambda mode: result["candidates"][mode]["minimum_annual_score"])
    result["project_selected_mode"] = development["selected_mode"]
    result["selection_changed_from_project"] = result["selected_mode"] != development["selected_mode"]
    result["official_daily_sha256"] = {
        str(path.relative_to(ROOT)): file_hash(path)
        for path in sorted(OUT.glob("official_*_daily.csv"))
        if any(path.name.endswith(f"_{year}_daily.csv") for year in YEARS)
    }
    verify_development_sources(development)
    if file_hash(development_path) != development_sha:
        raise AssertionError("Development selection changed during official verification")
    (OUT / "official_development.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"LOCKED OFFICIAL SELECTION: {result['selected_mode']}; "
          f"changed_from_project={result['selection_changed_from_project']}", flush=True)


if __name__ == "__main__":
    main()
