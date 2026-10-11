"""Scoring stage for the retrain suite of the final sweep."""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import polars as pl

from run import ROOT
from experiments.bonus_extension import BASE_BONUS, BLEND_WEIGHT, file_hash, load_auxiliary, load_panel, release_scores
from experiments.final_sweep import blend_top_only, retention_scores, RELEASED
from experiments.official_seed_development import official_score

OUT = ROOT / "experiments" / "final_sweep_eval"
DEVELOPMENT_YEARS = (2022, 2023)
NUMERIC_TOLERANCE = 1e-12


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def develop_retrain() -> None:
    protocol_path = OUT / "protocol_retrain.json"
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    training = json.loads((OUT / "training_retrain.json").read_text(encoding="utf-8"))
    if training["protocol_sha256"] != file_hash(protocol_path):
        raise SystemExit("Retraining was produced under a different protocol")
    result_path = OUT / "development_retrain.json"
    if result_path.exists():
        raise SystemExit("Retrain development results already recorded; preserving them")
    released = release_scores()
    started = time.monotonic()
    candidates = {}
    for year in DEVELOPMENT_YEARS:
        panel = load_panel(year)
        auxiliary = load_auxiliary(year, panel)
        baseline_prediction = blend_top_only(
            panel,
            retention_scores(panel, panel.frame["pred_raw"].to_numpy().astype(np.float64),
                             RELEASED["alpha"], BASE_BONUS, "standard"),
            panel.frame["pred_raw"].to_numpy().astype(np.float64), auxiliary, BLEND_WEIGHT)
        baseline_metrics, _ = official_score(panel, baseline_prediction, year)
        if abs(baseline_metrics["final_score"] - released[year]) > NUMERIC_TOLERANCE:
            raise AssertionError(f"{year} retrain-suite baseline anchor off by "
                                 f"{baseline_metrics['final_score'] - released[year]:.3e}")
        log(f"{year} baseline anchor reproduced {released[year]:.15f} exactly")
        for candidate in protocol["candidates"]:
            key = candidate["key"]
            cache = OUT / f"{key}_{year}.parquet"
            frame = pl.read_parquet(cache).sort("trade_date", "ts_code")
            if not frame.select("trade_date", "ts_code").equals(
                    panel.frame.select("trade_date", "ts_code")):
                raise AssertionError(f"{key} {year}: cache keys do not align with the fold panel")
            raw = frame["pred_raw"].to_numpy().astype(np.float64)
            stable = retention_scores(panel, raw, RELEASED["alpha"], BASE_BONUS, "standard")
            prediction = blend_top_only(panel, stable, raw, auxiliary, BLEND_WEIGHT)
            metrics, daily = official_score(panel, prediction, year)
            item = candidates.setdefault(key, {"years": {}})
            item["years"][str(year)] = {k: float(v) for k, v in metrics.items()}
            daily.write_csv(OUT / f"{key}_{year}_daily.csv")
            log(f"{year} {key}: score={metrics['final_score']:.9f} ic={metrics['ic_mean']:.6f} "
                f"excess={metrics['annual_excess']:.6f} turn={metrics['mean_turnover']:.6f}")
        del panel, auxiliary

    released_years = {str(y): released[y] for y in DEVELOPMENT_YEARS}
    for key, item in candidates.items():
        deltas = {y: item["years"][y]["final_score"] - released_years[y]
                  for y in map(str, DEVELOPMENT_YEARS)}
        item["score_delta"] = deltas
        item["ic_delta"] = {y: item["years"][y]["ic_mean"]
                            - json.loads((OUT / "development.json").read_text(encoding="utf-8"))
                            ["candidates"]["baseline_released"]["years"][y]["ic_mean"]
                            for y in map(str, DEVELOPMENT_YEARS)}
        item["passes_development_gate"] = all(v > NUMERIC_TOLERANCE for v in deltas.values())
        item["two_year_mean_delta"] = sum(deltas.values()) / len(deltas)
        item["two_year_minimax_delta"] = min(deltas.values())
    passing = [k for k, v in candidates.items() if v["passes_development_gate"]]
    output = {
        "stage": "develop_retrain",
        "generated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "elapsed_seconds": time.monotonic() - started,
        "protocol_sha256": file_hash(protocol_path),
        "training_sha256": file_hash(OUT / "training_retrain.json"),
        "candidates": candidates,
        "candidates_passing_development_gate": passing,
        "caveat": protocol["limitations"],
    }
    result_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"RETRAIN DEVELOPMENT: {len(passing)} of {len(candidates)} pass the two-year gate: {passing}")
