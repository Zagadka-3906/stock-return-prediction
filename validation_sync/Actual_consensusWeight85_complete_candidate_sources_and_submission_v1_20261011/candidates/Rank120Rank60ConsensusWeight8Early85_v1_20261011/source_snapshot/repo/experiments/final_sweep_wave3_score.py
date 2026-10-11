"""Scoring stage for the wave-3 cross-family ensemble suite.

Split from final_sweep_wave3.py so that scoring-side fixes never invalidate the
protocol that pins the ensemble rules. Before any candidate is scored, the cached
two-member ensemble is asserted bit-identical to rank_average(), the helper that
was already validated against the released baseline in the T1 suite.
"""
from __future__ import annotations

import json
import time

import numpy as np
import polars as pl

from experiments.bonus_extension import (BASE_BONUS, BLEND_WEIGHT, file_hash, load_auxiliary,
                                         load_panel, release_scores)
from experiments.final_sweep import blend_top_only, rank_average, retention_scores, RELEASED
from experiments.final_sweep_wave3 import (CANDIDATES, DEVELOPMENT_YEARS, OUT, log, member_path,
                                           verify_protocol)
from experiments.official_seed_development import official_score

NUMERIC_TOLERANCE = 1e-12


def cross_check_two_member(panel, cache_raw: np.ndarray, left: np.ndarray,
                           right: np.ndarray) -> None:
    reference = rank_average(left, right, 0.5, panel.valid_price)
    if not np.array_equal(reference, cache_raw):
        worst = float(np.nanmax(np.abs(reference - cache_raw)))
        raise AssertionError(f"W3a cache disagrees with the validated rank_average helper ({worst})")
    log("W3a cache is bit-identical to the validated rank_average helper")


def develop_wave3() -> None:
    protocol = verify_protocol()
    if tuple(protocol["development_years"]) != DEVELOPMENT_YEARS:
        raise SystemExit("Scorer years disagree with the frozen protocol")
    if protocol["candidates"] != CANDIDATES:
        raise SystemExit("Scorer candidates disagree with the frozen protocol")
    result_path = OUT / "development_wave3.json"
    if result_path.exists():
        raise SystemExit("Wave-3 development already recorded; preserving it")
    inventory = json.loads((OUT / "training_wave3.json").read_text(encoding="utf-8"))
    if inventory["protocol_sha256"] != file_hash(OUT / "protocol_wave3.json"):
        raise SystemExit("Wave-3 caches were built under a different protocol")
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
            raise AssertionError(f"{year} wave-3 baseline anchor off")
        log(f"{year} baseline anchor reproduced {released[year]:.15f} exactly")
        raws = {}
        for candidate in CANDIDATES:
            key = candidate["key"]
            path = member_path(key, year)
            pinned = inventory["caches"][str(year)][key]["sha256"]
            if file_hash(path) != pinned:
                raise SystemExit(f"{key} {year}: cache hash drifted from the pinned inventory")
            frame = pl.read_parquet(path).sort("trade_date", "ts_code")
            if not frame.select(["ts_code", "trade_date"]).equals(
                    panel.frame.select(["ts_code", "trade_date"])):
                raise AssertionError(f"{key} {year}: cache keys misaligned")
            raw = frame["pred_raw"].to_numpy().astype(np.float64)
            raws[key] = raw
            if key == "W3a_lgb_xgb" and year == DEVELOPMENT_YEARS[0]:
                xgb = pl.read_parquet(member_path("T2f_xgboost_backbone", year)).sort("trade_date", "ts_code")
                cross_check_two_member(panel, raw, backbone,
                                       xgb["pred_raw"].to_numpy().astype(np.float64))
            stable = retention_scores(panel, raw, RELEASED["alpha"], BASE_BONUS, "standard")
            prediction = blend_top_only(panel, stable, raw, auxiliary, BLEND_WEIGHT)
            metrics, daily = official_score(panel, prediction, year)
            item = candidates.setdefault(key, {"years": {}, "primary": candidate["primary"],
                                               "members": candidate["members"]})
            item["years"][str(year)] = {k: float(v) for k, v in metrics.items()}
            daily.write_csv(OUT / f"{key}_{year}_daily.csv")
            log(f"{year} {key}: score={metrics['final_score']:.9f} ic={metrics['ic_mean']:.6f} "
                f"excess={metrics['annual_excess']:.6f} turn={metrics['mean_turnover']:.6f}")
            del raw, stable, prediction
        del raws, panel, auxiliary
    released_years = {str(y): released[y] for y in DEVELOPMENT_YEARS}
    for key, item in candidates.items():
        deltas = {y: item["years"][y]["final_score"] - released_years[y]
                  for y in map(str, DEVELOPMENT_YEARS)}
        item["score_delta"] = deltas
        item["passes_development_gate"] = all(v > NUMERIC_TOLERANCE for v in deltas.values())
        item["two_year_mean_delta"] = sum(deltas.values()) / len(deltas)
        item["two_year_minimax_delta"] = min(deltas.values())
    passing = [k for k, v in candidates.items() if v["passes_development_gate"]]
    output = {"stage": "develop_wave3", "generated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
              "elapsed_seconds": time.monotonic() - started,
              "protocol_sha256": file_hash(OUT / "protocol_wave3.json"),
              "candidates": candidates, "candidates_passing_development_gate": passing,
              "caveat": protocol["limitations"]}
    result_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"WAVE-3 DEVELOPMENT: {len(passing)} of {len(candidates)} pass: {passing}")


if __name__ == "__main__":
    develop_wave3()
