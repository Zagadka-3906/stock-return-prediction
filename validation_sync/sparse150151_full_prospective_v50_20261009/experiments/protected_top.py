"""Causal separation of stable Top holdings and current lower-universe ranks.

The transform protects every score at or above the old tradable Top cutoff.
Only the remaining valid-price stocks are re-ranked by the current raw signal.
No returns or label-availability mask are read by the transform.
"""

from __future__ import annotations

import argparse
import json

import numpy as np
import polars as pl

from run import ROOT
from src.scoring import Panel, postprocess_scores, restore_lower_ranks, score

OUT = ROOT / "experiments" / "protected_top_eval"
ALPHAS = (0.6, 0.8, 0.9, 0.95)
BONUSES = (0.05, 0.15, 0.30)


def make_candidate(panel: Panel, raw: np.ndarray, config: dict) -> np.ndarray:
    return postprocess_scores(panel, raw, config["alpha"], config["bonus"], config["restore_lower"])


def candidate_key(config: dict) -> str:
    return f"a{config['alpha']}_b{config['bonus']}_restore{int(config['restore_lower'])}"


def load_panel(year: int) -> Panel:
    return Panel.from_frame(pl.read_parquet(ROOT / "validation" / f"fold_{year}.parquet"))


def develop() -> None:
    configs = [{"alpha": alpha, "bonus": bonus, "restore_lower": restore}
               for alpha in ALPHAS for bonus in BONUSES for restore in (False, True)]
    results = {candidate_key(c): {"config": c, "years": {}} for c in configs}
    for year in (2022, 2023):
        panel = load_panel(year)
        raw = panel.frame["pred_raw"].to_numpy()
        for config in configs:
            key = candidate_key(config)
            metrics, _ = score(panel, make_candidate(panel, raw, config))
            results[key]["years"][str(year)] = metrics
            print(f"{year} {key}: {metrics['final_score']:.6f} IC={metrics['ic_mean']:.6f} "
                  f"excess={metrics['annual_excess']:.6f} turn={metrics['mean_turnover']:.6f}", flush=True)
    for item in results.values():
        item["minimum_annual_score"] = min(m["final_score"] for m in item["years"].values())
    selected_key = max(results, key=lambda key: results[key]["minimum_annual_score"])
    output = {"selection_years": [2022, 2023], "selection_rule": "maximize_minimum_annual_score",
              "selected_key": selected_key, "selected_config": results[selected_key]["config"],
              "candidates": results,
              "caveat": "Development years and 2024 have informed previous experiments; this is exploratory."}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "development.json").write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"SELECTED {selected_key}: {results[selected_key]['minimum_annual_score']:.6f}", flush=True)


def diagnose() -> None:
    development = json.loads((OUT / "development.json").read_text(encoding="utf-8"))
    config = development["selected_config"]
    panel = load_panel(2024)
    raw = panel.frame["pred_raw"].to_numpy()
    pred = make_candidate(panel, raw, config)
    metrics, daily = score(panel, pred)
    baseline_config = {"alpha": 0.95, "bonus": 0.15, "restore_lower": False}
    baseline, _ = score(panel, make_candidate(panel, raw, baseline_config))
    output = {"config": config, "metrics": metrics, "baseline": baseline,
              "delta": metrics["final_score"] - baseline["final_score"]}
    (OUT / "diagnostic_2024.json").write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    panel.frame.select("ts_code", "trade_date").with_columns(pl.Series("pred", pred)).write_parquet(OUT / "selected_2024.parquet")
    daily.write_csv(OUT / "selected_2024_daily.csv")
    print(json.dumps(output, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("develop", "diagnose"))
    args = parser.parse_args()
    develop() if args.stage == "develop" else diagnose()
