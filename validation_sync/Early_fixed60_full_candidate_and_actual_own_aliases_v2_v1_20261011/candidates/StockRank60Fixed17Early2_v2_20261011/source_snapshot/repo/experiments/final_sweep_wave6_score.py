"""Scoring stage for wave 6: cross-sectional feature normalization.

Split from final_sweep_wave6.py so scoring-side fixes never invalidate the
protocol that pins the transforms. Both stages are one-shot.
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
from experiments.final_sweep_wave5_score import released_stack
from experiments.final_sweep_wave6 import (AUDIT_YEARS, CANDIDATES, DEVELOPMENT_YEARS, KEYS, OUT,
                                           verify_protocol)
from experiments.final_sweep_wave5 import log, panel_frame
from experiments.official_seed_development import official_score

NUMERIC_TOLERANCE = 1e-12


def cache_raw(year: int, key: str, panel: Panel, inventory: dict) -> np.ndarray:
    pinned = inventory["candidates"][key][str(year)]["cache_sha256"]
    path = OUT / f"{key}_{year}.parquet"
    if file_hash(path) != pinned:
        raise SystemExit(f"{key} {year}: cache hash drifted from the pinned inventory")
    frame = pl.read_parquet(path).sort("trade_date", "ts_code")
    if not frame.select(KEYS).equals(panel.frame.select(KEYS)):
        raise AssertionError(f"{key} {year}: cache keys misaligned with the panel")
    return frame["pred_raw"].to_numpy().astype(np.float64)


def develop() -> None:
    protocol = verify_protocol()
    if tuple(protocol["development_years"]) != DEVELOPMENT_YEARS:
        raise SystemExit("Scorer years disagree with the frozen protocol")
    if protocol["candidates"] != CANDIDATES:
        raise SystemExit("Scorer candidates disagree with the frozen protocol")
    result_path = OUT / "development_wave6.json"
    if result_path.exists():
        raise SystemExit("Wave-6 development already recorded; preserving it")
    inventory = json.loads((OUT / "training_wave6.json").read_text(encoding="utf-8"))
    if inventory["protocol_sha256"] != file_hash(OUT / "protocol_wave6.json"):
        raise SystemExit("Wave-6 caches were trained under a different protocol")
    if not all(inventory["harness_proof"].values()):
        raise SystemExit("Wave-6 harness proofs did not all pass")
    released = release_scores()
    started = time.monotonic()
    candidates = {}
    for year in DEVELOPMENT_YEARS:
        panel = load_panel(year)
        auxiliary = load_auxiliary(year, panel)
        backbone = panel.frame["pred_raw"].to_numpy().astype(np.float64)
        baseline_metrics, _ = official_score(panel, released_stack(panel, backbone, auxiliary), year)
        if abs(baseline_metrics["final_score"] - released[year]) > NUMERIC_TOLERANCE:
            raise AssertionError(f"{year} wave-6 baseline anchor off")
        log(f"{year} baseline anchor reproduced {released[year]:.15f} exactly")
        for candidate in CANDIDATES:
            key = candidate["key"]
            raw = cache_raw(year, key, panel, inventory)
            metrics, daily = official_score(panel, released_stack(panel, raw, auxiliary), year)
            daily.write_csv(OUT / f"{key}_{year}_daily.csv")
            item = candidates.setdefault(key, {"years": {}, "primary": candidate["primary"],
                                               "transform": candidate["transform"]})
            item["years"][str(year)] = {k: float(v) for k, v in metrics.items()}
            log(f"{year} {key}: score={metrics['final_score']:.9f} ic={metrics['ic_mean']:.6f} "
                f"excess={metrics['annual_excess']:.6f} turn={metrics['mean_turnover']:.6f} "
                f"delta={metrics['final_score'] - released[year]:+.9f}")
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
    output = {"stage": "develop_wave6", "generated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
              "elapsed_seconds": time.monotonic() - started,
              "protocol_sha256": file_hash(OUT / "protocol_wave6.json"),
              "harness_proof": inventory["harness_proof"],
              "candidates": candidates, "candidates_passing_development_gate": passing,
              "caveat": protocol["limitations"]}
    result_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"WAVE-6 DEVELOPMENT: {len(passing)} of {len(candidates)} pass: {passing}")


def audit() -> None:
    verify_protocol()
    result_path = OUT / "audit_wave6.json"
    if result_path.exists():
        raise SystemExit("Wave-6 audit already recorded; preserving it")
    development = json.loads((OUT / "development_wave6.json").read_text(encoding="utf-8"))
    inventory = json.loads((OUT / "training_wave6.json").read_text(encoding="utf-8"))
    eligible = development["candidates_passing_development_gate"]
    if not eligible:
        raise SystemExit("No wave-6 candidate passed the development gate; nothing to audit")
    prior = json.loads((OUT.parent / "extended_audit_eval" / "audit_results.json").read_text(encoding="utf-8"))
    started = time.monotonic()
    results = {"years": {}}
    for year in AUDIT_YEARS:
        frame = panel_frame(year)
        panel = Panel.from_frame(frame)
        backbone = frame["pred_raw"].to_numpy().astype(np.float64)
        baseline, _ = audit_score(panel, released_stack(panel, backbone, None), year)
        expected = prior["years"][str(year)]["released_lgb_backbone"]["final_score"]
        if abs(baseline["final_score"] - expected) > NUMERIC_TOLERANCE:
            raise AssertionError(f"{year} audit baseline differs from the recorded audit run")
        log(f"{year} audit baseline reproduced {expected:.9f} exactly")
        entries = {"released_lgb_backbone": {k: float(v) for k, v in baseline.items()}}
        for key in eligible:
            raw = cache_raw(year, key, panel, inventory)
            metrics, daily = audit_score(panel, released_stack(panel, raw, None), year)
            daily.write_csv(OUT / f"{key}_{year}_daily.csv")
            entries[key] = {**{k: float(v) for k, v in metrics.items()},
                            "delta_vs_released": float(metrics["final_score"]) - baseline["final_score"]}
            log(f"{year} {key}: score={metrics['final_score']:.9f} ic={metrics['ic_mean']:.6f} "
                f"delta={entries[key]['delta_vs_released']:+.9f}")
        results["years"][str(year)] = entries
        del panel, frame
    summary = {}
    for key in eligible:
        deltas = [results["years"][str(y)][key]["delta_vs_released"] for y in AUDIT_YEARS]
        summary[key] = {"audit_deltas": deltas, "mean_delta": sum(deltas) / len(deltas),
                        "positive_both_years": all(d > 0 for d in deltas)}
    output = {"stage": "audit_wave6", "generated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
              "elapsed_seconds": time.monotonic() - started, "audit_years": list(AUDIT_YEARS),
              "protocol_sha256": file_hash(OUT / "protocol_wave6.json"),
              "caliber": "released stack without the pooled blend, identical for baseline and "
                         "candidate; matches the recorded extended-year audit",
              "results": results, "summary": summary}
    result_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    for key, item in summary.items():
        log(f"WAVE-6 AUDIT {key}: deltas={['%+.6f' % d for d in item['audit_deltas']]} "
            f"positive_both={item['positive_both_years']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("develop", "audit"))
    arguments = parser.parse_args()
    if arguments.stage == "develop":
        develop()
    else:
        audit()
