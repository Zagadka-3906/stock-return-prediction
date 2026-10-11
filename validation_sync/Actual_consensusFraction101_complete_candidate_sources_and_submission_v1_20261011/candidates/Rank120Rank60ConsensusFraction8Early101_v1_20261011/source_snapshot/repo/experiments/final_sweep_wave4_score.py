"""Scoring stage for wave 4: train the pre-selected winner on the scored years, once.

Split from final_sweep_wave4.py so scoring-side fixes never invalidate the
protocol that pins the grid and the selection rule. The winner is read from the
recorded selection file; nothing here can change it. If the selection kept the
released configuration, this stage scores nothing and records that outcome.
"""
from __future__ import annotations

import argparse
import json
import time

import numpy as np
import polars as pl

from src.scoring import Panel
from experiments.bonus_extension import (BASE_BONUS, BLEND_WEIGHT, file_hash, load_auxiliary,
                                         load_panel, release_scores)
from experiments.extended_audit import audit_score
from experiments.final_sweep import blend_top_only, retention_scores, RELEASED
from experiments.final_sweep_wave4 import (DEVELOPMENT_YEARS, DIAGNOSTIC_YEAR, KEYS, OUT,
                                           fit_and_predict, log, verify_protocol)
from experiments.official_seed_development import official_score
from run import feature_names

NUMERIC_TOLERANCE = 1e-12


def scored_prediction(panel: Panel, raw: np.ndarray, auxiliary: np.ndarray) -> np.ndarray:
    stable = retention_scores(panel, raw, RELEASED["alpha"], BASE_BONUS, "standard")
    return blend_top_only(panel, stable, raw, auxiliary, BLEND_WEIGHT)


def anchor(panel: Panel, auxiliary: np.ndarray, year: int, released: dict) -> dict:
    raw = panel.frame["pred_raw"].to_numpy().astype(np.float64)
    metrics, _ = official_score(panel, scored_prediction(panel, raw, auxiliary), year)
    if abs(metrics["final_score"] - released[year]) > NUMERIC_TOLERANCE:
        raise AssertionError(f"{year} wave-4 baseline anchor off")
    replica, _ = audit_score(panel, scored_prediction(panel, raw, auxiliary), year)
    if abs(replica["final_score"] - metrics["final_score"]) > NUMERIC_TOLERANCE:
        raise AssertionError(f"{year} replica scorer disagrees with official_score")
    log(f"{year} baseline anchor reproduced {released[year]:.15f} exactly")
    return metrics


def run_years(years: tuple[int, ...], result_name: str, stage: str,
              require_development_pass: bool = False) -> None:
    protocol = verify_protocol()
    result_path = OUT / result_name
    if result_path.exists():
        raise SystemExit(f"Wave-4 {stage} already recorded; preserving it")
    selection = json.loads((OUT / "selection_wave4.json").read_text(encoding="utf-8"))
    if selection["protocol_sha256"] != file_hash(OUT / "protocol_wave4.json"):
        raise SystemExit("Wave-4 selection was made under a different protocol")
    winner = selection["selected"]
    config = selection["selected_config"]
    if require_development_pass:
        development = json.loads((OUT / "development_wave4.json").read_text(encoding="utf-8"))
        if not development["passes_development_gate"]:
            raise SystemExit("Development gate not passed; nothing to confirm")
    released = release_scores()
    features = feature_names()
    started = time.monotonic()
    record = {"stage": f"{stage}_wave4", "generated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
              "protocol_sha256": file_hash(OUT / "protocol_wave4.json"), "selected": winner,
              "selected_config": config,
              "selected_is_released_configuration": selection["selected_is_released_configuration"],
              "years": {}}
    if selection["selected_is_released_configuration"]:
        record["outcome"] = ("Selection kept the released configuration; there is nothing to score "
                             "and the release stands unchanged.")
        record["passes_development_gate"] = False
        record["elapsed_seconds"] = time.monotonic() - started
        result_path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
        log(f"WAVE-4 {stage.upper()}: selection kept the released configuration; no change")
        return
    for year in years:
        panel = load_panel(year)
        auxiliary = load_auxiliary(year, panel)
        anchor(panel, auxiliary, year, released)
        frame, raw, rows = fit_and_predict(config, year, features)
        if not frame.select(KEYS).equals(panel.frame.select(KEYS)):
            raise AssertionError(f"{winner} {year}: prediction keys differ from the released fold")
        cache = OUT / f"{winner}_{year}.parquet"
        frame.select(KEYS + ["pred_raw"]).write_parquet(cache, compression="zstd")
        substituted = Panel.from_frame(panel.frame.with_columns(pl.Series("pred_raw", raw)))
        prediction = scored_prediction(substituted, raw, auxiliary)
        metrics, daily = official_score(substituted, prediction, year)
        daily.write_csv(OUT / f"{winner}_{year}_daily.csv")
        delta = float(metrics["final_score"]) - released[year]
        record["years"][str(year)] = {**{k: float(v) for k, v in metrics.items()},
                                      "score_delta": delta, "training_rows": rows,
                                      "cache_sha256": file_hash(cache)}
        log(f"{year} {winner}: score={metrics['final_score']:.9f} ic={metrics['ic_mean']:.6f} "
            f"excess={metrics['annual_excess']:.6f} turn={metrics['mean_turnover']:.6f} "
            f"delta={delta:+.9f}")
        del panel, auxiliary, frame, raw, substituted, prediction
    deltas = {y: record["years"][y]["score_delta"] for y in record["years"]}
    record["score_delta"] = deltas
    record["mean_delta"] = sum(deltas.values()) / len(deltas)
    record["minimax_delta"] = min(deltas.values())
    record["passes_development_gate"] = all(v > NUMERIC_TOLERANCE for v in deltas.values())
    record["elapsed_seconds"] = time.monotonic() - started
    record["caveat"] = protocol["limitations"]
    result_path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"WAVE-4 {stage.upper()}: gate {'PASSED' if record['passes_development_gate'] else 'FAILED'} "
        f"deltas={ {k: round(v, 9) for k, v in deltas.items()} }")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("develop", "confirm"))
    arguments = parser.parse_args()
    if arguments.stage == "develop":
        run_years(DEVELOPMENT_YEARS, "development_wave4.json", "develop")
    else:
        run_years((DIAGNOSTIC_YEAR,), "confirmation_wave4.json", "confirm",
                  require_development_pass=True)
