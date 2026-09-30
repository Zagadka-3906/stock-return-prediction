"""Predeclared, development-only recheck of cached models and rank ensembles.

Selection uses only 2022 and 2023.  Six pure auxiliary signals are evaluated
first; only the two with the best worst-year score enter the blending grid.
The fixed production postprocessor is not retuned in this experiment.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import polars as pl
from scipy.stats import rankdata

from run import ROOT
from src.scoring import Panel, add_top_persistence, make_scores, postprocess_scores, score

OUT = ROOT / "experiments" / "cached_recheck_eval"
SELECTION_YEARS = (2022, 2023)
BASE_CONFIG = {"alpha": 0.9, "bonus": 0.3, "restore_lower": True, "top_current_weight": 1.0}
AUXILIARY_FILES = {
    "huber": "experiments/next_steps_eval/huber_{year}.parquet",
    "recent2x": "experiments/next_steps_eval/recent2x_{year}.parquet",
    "rolling3": "experiments/next_steps_eval/rolling3_{year}.parquet",
    "top2": "experiments/next_steps_eval/top2_{year}.parquet",
    "lambdarank": "experiments/ranking_eval/lightgbm_lambdarank_{year}_80round.parquet",
    "xgboost": "experiments/ranking_eval/xgboost_linear_ndcg_{year}_80round.parquet",
}
FULL_SIGNAL_WEIGHTS = (0.1, 0.25, 0.5)
TOP_ONLY_WEIGHTS = (0.25, 0.5, 1.0)
BASELINE_KEY = "baseline"


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def check_production_config() -> None:
    metrics = json.loads((ROOT / "validation" / "metrics.json").read_text(encoding="utf-8"))
    observed = {
        "alpha": metrics["selected_alpha"],
        "bonus": metrics["selected_persistence_bonus"],
        "restore_lower": metrics["selected_restore_lower"],
        "top_current_weight": metrics["selected_top_current_weight"],
    }
    if observed != BASE_CONFIG:
        raise ValueError(f"Production configuration changed: expected {BASE_CONFIG}, got {observed}")


def load_panel(year: int) -> Panel:
    return Panel.from_frame(pl.read_parquet(ROOT / "validation" / f"fold_{year}.parquet"))


def load_auxiliary(name: str, year: int, panel: Panel) -> np.ndarray:
    """Read only keys and predictions; never use labels embedded in a cache."""
    path = ROOT / AUXILIARY_FILES[name].format(year=year)
    frame = pl.read_parquet(path, columns=["ts_code", "trade_date", "pred_raw"])
    frame = frame.sort("trade_date", "ts_code")
    if not frame.select("trade_date", "ts_code").equals(panel.frame.select("trade_date", "ts_code")):
        raise ValueError(f"Cached prediction keys do not match the baseline panel: {path}")
    raw = frame["pred_raw"].to_numpy().astype(np.float64)
    if not np.isfinite(raw.reshape(panel.valid_price.shape)[panel.valid_price]).all():
        raise ValueError(f"Auxiliary has a nonfinite valid-price prediction: {path}")
    return raw


def daily_percentiles(panel: Panel, raw: np.ndarray) -> np.ndarray:
    values = np.asarray(raw, dtype=np.float64).reshape(panel.valid_price.shape)
    out = np.full_like(values, -10.0)
    for day in range(len(panel.dates)):
        valid = panel.valid_price[day] & np.isfinite(values[day])
        if valid.any():
            out[day, valid] = rankdata(values[day, valid], method="average") / int(valid.sum())
    return out.reshape(-1)


def make_prediction(panel: Panel, auxiliary_raw: np.ndarray | None, mode: str, weight: float) -> np.ndarray:
    """Construct predictions without reading returns or label availability.

    full_signal blends daily valid-price percentile ranks, then applies the
    production postprocessor. top_only retains the baseline's entire state,
    lower ordering and protected membership, mixing percentile ranks computed
    *within* the protected upper block. Ambiguous boundaries or invalid Top
    observations fall back to the production output for that complete day.
    """
    if not np.isfinite(weight) or not 0 <= weight <= 1:
        raise ValueError("weight must be in [0, 1]")
    base_raw = panel.frame["pred_raw"].to_numpy().astype(np.float64)
    if mode == "baseline":
        return postprocess_scores(panel, base_raw, **BASE_CONFIG)
    if mode not in {"pure", "full_signal", "top_only"}:
        raise ValueError(f"Unknown mode: {mode}")
    if auxiliary_raw is None:
        raise ValueError(f"Auxiliary predictions are required for {mode}")
    auxiliary_raw = np.asarray(auxiliary_raw, dtype=np.float64)
    if auxiliary_raw.size != base_raw.size:
        raise ValueError("Auxiliary prediction size does not match baseline")
    if mode == "pure":
        return postprocess_scores(panel, auxiliary_raw, **BASE_CONFIG)
    if mode == "full_signal":
        mixed = ((1 - weight) * daily_percentiles(panel, base_raw)
                 + weight * daily_percentiles(panel, auxiliary_raw))
        return postprocess_scores(panel, mixed, **BASE_CONFIG)

    out = postprocess_scores(panel, base_raw, **BASE_CONFIG).reshape(panel.valid_price.shape)
    stable = add_top_persistence(panel, make_scores(panel, base_raw, BASE_CONFIG["alpha"]),
                                 BASE_CONFIG["bonus"]).reshape(panel.valid_price.shape)
    base_raw = base_raw.reshape(panel.valid_price.shape)
    auxiliary_raw = auxiliary_raw.reshape(panel.valid_price.shape)
    for day in range(len(panel.dates)):
        valid = panel.valid_price[day] & np.isfinite(base_raw[day])
        indices = np.flatnonzero(panel.up[day] == 0)
        n_top = max(len(indices) // 10, 1)
        if not len(indices) or not valid.any():
            continue
        top = indices[np.argsort(-stable[day, indices], kind="stable")[:n_top]]
        if not valid[top].all():
            continue
        protected = valid & (stable[day] >= stable[day, top].min())
        if np.count_nonzero(protected & (panel.up[day] == 0)) != n_top:
            continue
        if not np.isfinite(auxiliary_raw[day, protected]).all():
            continue
        n_upper = int(protected.sum())
        base_rank = rankdata(base_raw[day, protected], method="average") / n_upper
        auxiliary_rank = rankdata(auxiliary_raw[day, protected], method="average") / n_upper
        blended_rank = rankdata((1 - weight) * base_rank + weight * auxiliary_rank, method="average")
        n_valid = int(valid.sum())
        out[day, protected] = (n_valid - n_upper + blended_rank) / n_valid
    return out.reshape(-1)


def candidate_key(config: dict) -> str:
    if config["mode"] == "baseline":
        return BASELINE_KEY
    return f"{config['auxiliary']}_{config['mode']}_w{config['weight']:g}"


def develop() -> None:
    check_production_config()
    OUT.mkdir(parents=True, exist_ok=True)
    panels = {year: load_panel(year) for year in SELECTION_YEARS}
    auxiliaries = {(name, year): load_auxiliary(name, year, panels[year])
                   for name in AUXILIARY_FILES for year in SELECTION_YEARS}
    fingerprints = {}
    for year in SELECTION_YEARS:
        baseline_path = ROOT / "validation" / f"fold_{year}.parquet"
        fingerprints[str(baseline_path.relative_to(ROOT)).replace("\\", "/")] = file_sha256(baseline_path)
        for template in AUXILIARY_FILES.values():
            relative = template.format(year=year)
            fingerprints[relative] = file_sha256(ROOT / relative)
    candidates = {}

    def evaluate(config: dict) -> str:
        key = candidate_key(config)
        item = {"config": config, "years": {}}
        for year, panel in panels.items():
            raw = auxiliaries.get((config["auxiliary"], year))
            predictions = make_prediction(panel, raw, config["mode"], config["weight"])
            metrics, daily = score(panel, predictions)
            item["years"][str(year)] = metrics
            daily.write_csv(OUT / f"{key}_{year}_daily.csv")
            print(f"{year} {key}: score={metrics['final_score']:.9f} IC={metrics['ic_mean']:.6f} "
                  f"excess={metrics['annual_excess']:.6f} turn={metrics['mean_turnover']:.6f}", flush=True)
        item["minimum_annual_score"] = min(m["final_score"] for m in item["years"].values())
        candidates[key] = item
        return key

    evaluate({"auxiliary": None, "mode": "baseline", "weight": 0.0})
    pure_keys = [evaluate({"auxiliary": name, "mode": "pure", "weight": 1.0})
                 for name in AUXILIARY_FILES]
    shortlist = sorted(pure_keys, key=lambda key: candidates[key]["minimum_annual_score"], reverse=True)[:2]
    for pure_key in shortlist:
        name = candidates[pure_key]["config"]["auxiliary"]
        for mode, weights in (("full_signal", FULL_SIGNAL_WEIGHTS), ("top_only", TOP_ONLY_WEIGHTS)):
            for weight in weights:
                evaluate({"auxiliary": name, "mode": mode, "weight": weight})
    selected_key = max(candidates, key=lambda key: candidates[key]["minimum_annual_score"])
    selected = candidates[selected_key]
    baseline = candidates[BASELINE_KEY]
    output = {
        "selection_years": list(SELECTION_YEARS),
        "selection_rule": "maximize_minimum_annual_score_2022_2023; exact ties prefer earlier candidate",
        "shortlist_rule": "two pure auxiliaries with highest minimum annual score; exact ties follow AUXILIARY_FILES order",
        "base_config": BASE_CONFIG,
        "baseline_key": BASELINE_KEY,
        "pure_shortlist": shortlist,
        "cache_sha256": fingerprints,
        "candidate_count": len(candidates),
        "selected_key": selected_key,
        "selected_config": selected["config"],
        "selected_improves_both_years": all(selected["years"][str(y)]["final_score"] >
                                           baseline["years"][str(y)]["final_score"] for y in SELECTION_YEARS),
        "candidates": candidates,
        "caveat": "Exploratory development reusing historical folds, not an untouched holdout. No 2024 labels loaded.",
    }
    (OUT / "development.json").write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"SELECTED {selected_key}: minimum annual score={selected['minimum_annual_score']:.9f}; "
          f"both years improved={output['selected_improves_both_years']}", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("develop",))
    parser.parse_args()
    develop()
