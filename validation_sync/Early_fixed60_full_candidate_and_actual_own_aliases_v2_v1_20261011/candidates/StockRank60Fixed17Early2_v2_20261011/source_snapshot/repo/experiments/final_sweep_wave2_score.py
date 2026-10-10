"""Scoring stage for the wave-2 mechanism suite.

Kept in its own module so scoring-side fixes never invalidate the protocol that
pins final_sweep_wave2.py: that file still carries its original develop() and its
frozen source hash, and this module supersedes it for scoring only. All rules are
imported from the pinned module, so the two cannot disagree.
"""
from __future__ import annotations

import json
import time

import numpy as np
import polars as pl
from scipy.stats import rankdata

from experiments.bonus_extension import BASE_BONUS, BLEND_WEIGHT, file_hash, load_auxiliary, load_panel, release_scores
from experiments.final_sweep import blend_top_only, retention_scores, RELEASED
from experiments.final_sweep_wave2 import (CANDIDATES, DEVELOPMENT_YEARS, ENSEMBLE_ALPHAS, OUT,
                                           NUMERIC_TOLERANCE, log, verify_protocol)
from experiments.official_seed_development import official_score


def ensemble_prediction(panel, backbone, auxiliary) -> np.ndarray:
    shape = panel.valid_price.shape
    mixed = np.zeros(shape)
    for alpha in ENSEMBLE_ALPHAS:
        stable = retention_scores(panel, backbone, alpha, BASE_BONUS, "standard")
        member = blend_top_only(panel, stable, backbone, auxiliary, BLEND_WEIGHT).reshape(shape)
        for day in range(shape[0]):
            keep = panel.valid_price[day]
            mixed[day][keep] += rankdata(member[day][keep], method="average") / keep.sum()
    return mixed.reshape(-1) / len(ENSEMBLE_ALPHAS)


def develop_wave2() -> None:
    protocol = verify_protocol()
    if tuple(protocol["development_years"]) != DEVELOPMENT_YEARS:
        raise SystemExit("Scorer years disagree with the frozen protocol")
    if protocol["candidates"] != CANDIDATES:
        raise SystemExit("Scorer candidates disagree with the frozen protocol")
    result_path = OUT / "development_wave2.json"
    if result_path.exists():
        raise SystemExit("Wave-2 development already recorded; preserving it")
    released = release_scores()
    started = time.monotonic()
    candidates = {}
    for year in DEVELOPMENT_YEARS:
        panel = load_panel(year)
        auxiliary = load_auxiliary(year, panel)
        backbone = panel.frame["pred_raw"].to_numpy().astype(np.float64)
        baseline = blend_top_only(panel, retention_scores(panel, backbone, RELEASED["alpha"],
                                                          BASE_BONUS, "standard"),
                                  backbone, auxiliary, BLEND_WEIGHT)
        baseline_metrics, _ = official_score(panel, baseline, year)
        if abs(baseline_metrics["final_score"] - released[year]) > NUMERIC_TOLERANCE:
            raise AssertionError(f"{year} wave-2 baseline anchor off")
        log(f"{year} baseline anchor reproduced {released[year]:.15f} exactly")
        for candidate in CANDIDATES:
            key, variant = candidate["key"], candidate["variant"]
            if variant == "pp_ensemble":
                prediction = ensemble_prediction(panel, backbone, auxiliary)
            else:
                frame = pl.read_parquet(OUT / f"{key}_{year}.parquet").sort("trade_date", "ts_code")
                raw = frame["pred_raw"].to_numpy().astype(np.float64)
                stable = retention_scores(panel, raw, candidate["alpha"], BASE_BONUS, "standard")
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
        item["passes_development_gate"] = all(v > NUMERIC_TOLERANCE for v in deltas.values())
        item["two_year_mean_delta"] = sum(deltas.values()) / len(deltas)
        item["two_year_minimax_delta"] = min(deltas.values())
    passing = [k for k, v in candidates.items() if v["passes_development_gate"]]
    output = {"stage": "develop_wave2", "generated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
              "elapsed_seconds": time.monotonic() - started,
              "protocol_sha256": file_hash(OUT / "protocol_wave2.json"),
              "candidates": candidates, "candidates_passing_development_gate": passing,
              "caveat": protocol["limitations"]}
    result_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"WAVE-2 DEVELOPMENT: {len(passing)} of {len(candidates)} pass: {passing}")


if __name__ == "__main__":
    develop_wave2()
