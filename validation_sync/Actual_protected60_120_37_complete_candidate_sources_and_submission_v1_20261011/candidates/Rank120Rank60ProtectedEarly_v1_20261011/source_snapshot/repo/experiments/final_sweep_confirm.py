"""One-shot third-year confirmation for sweep suites.

A suite's frozen protocol names a diagnostic year and requires strict improvement
there as well before adoption. This stage runs exactly once per suite, after the
development years are already recorded, and never re-scores a development year.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import time

import numpy as np
import polars as pl

from run import ROOT
from experiments.bonus_extension import (BASE_BONUS, BLEND_WEIGHT, file_hash, load_auxiliary,
                                         load_panel, release_scores)
from experiments.final_sweep import blend_top_only, retention_scores, RELEASED
from experiments.official_seed_development import official_score

OUT = ROOT / "experiments" / "final_sweep_eval"
KEYS = ["ts_code", "trade_date"]
NUMERIC_TOLERANCE = 1e-12
AUDIT_KEYS = ("frozen_at_local", "source_sha256", "superseded_reason")

SUITES = {
    "extra": {"protocol": "protocol_extra.json", "training": "training_extra.json",
              "development": "development_extra.json", "confirmation": "confirmation_extra.json",
              "superseded_glob": "protocol_extra_superseded_*.json",
              "pinned_module": "experiments/final_sweep_extra.py"},
    "wave2": {"protocol": "protocol_wave2.json", "training": "training_wave2.json",
              "development": "development_wave2.json", "confirmation": "confirmation_wave2.json",
              "superseded_glob": "protocol_wave2_superseded_*.json",
              "pinned_module": "experiments/final_sweep_wave2.py"},
    "wave3": {"protocol": "protocol_wave3.json", "training": "training_wave3.json",
              "development": "development_wave3.json", "confirmation": "confirmation_wave3.json",
              "superseded_glob": "protocol_wave3_superseded_*.json",
              "pinned_module": "experiments/final_sweep_wave3.py"},
    "wave5": {"protocol": "protocol_wave5.json", "training": "training_wave5.json",
              "development": "development_wave5.json", "confirmation": "confirmation_wave5.json",
              "superseded_glob": "protocol_wave5_superseded_*.json",
              "pinned_module": "experiments/final_sweep_wave5.py"},
    "wave6": {"protocol": "protocol_wave6.json", "training": "training_wave6.json",
              "development": "development_wave6.json", "confirmation": "confirmation_wave6.json",
              "superseded_glob": "protocol_wave6_superseded_*.json",
              "pinned_module": "experiments/final_sweep_wave6.py"},
}


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def protocol_bytes(payload: dict) -> bytes:
    """Reproduce the on-disk bytes write_text() produced on Windows."""
    return json.dumps(payload, ensure_ascii=False, indent=2).replace("\n", "\r\n").encode("utf-8")


def verify_lineage(suite: dict, training: dict, protocol: dict) -> None:
    if training["protocol_sha256"] == file_hash(OUT / suite["protocol"]):
        return
    for path in sorted(OUT.glob(suite["superseded_glob"])):
        payload = json.loads(path.read_text(encoding="utf-8"))
        pristine = {k: v for k, v in payload.items() if k != "superseded_reason"}
        if hashlib.sha256(protocol_bytes(pristine)).hexdigest() != training["protocol_sha256"]:
            continue
        drift = [k for k in protocol if k not in AUDIT_KEYS and pristine.get(k) != protocol[k]]
        if drift:
            raise SystemExit(f"Protocol rules changed between training and scoring: {drift}")
        log(f"Lineage verified via {path.name}: rules byte-identical to the frozen protocol")
        return
    raise SystemExit("Training caches were produced under an unrecorded protocol")


def confirm(suite_name: str) -> None:
    suite = SUITES[suite_name]
    protocol = json.loads((OUT / suite["protocol"]).read_text(encoding="utf-8"))
    if protocol["source_sha256"] != file_hash(ROOT / suite["pinned_module"]):
        raise SystemExit(f"{suite['pinned_module']} changed after its protocol was frozen; stop")
    year = int(protocol["diagnostic_year"])
    training = json.loads((OUT / suite["training"]).read_text(encoding="utf-8"))
    verify_lineage(suite, training, protocol)
    development = json.loads((OUT / suite["development"]).read_text(encoding="utf-8"))
    passing = development["candidates_passing_development_gate"]
    if not passing:
        raise SystemExit("No candidate passed the development gate; nothing to confirm")
    result_path = OUT / suite["confirmation"]
    if result_path.exists():
        raise SystemExit(f"{suite_name} confirmation already recorded; preserving it")
    released = release_scores()
    panel = load_panel(year)
    auxiliary = load_auxiliary(year, panel)
    backbone = panel.frame["pred_raw"].to_numpy().astype(np.float64)
    baseline = blend_top_only(panel, retention_scores(panel, backbone, RELEASED["alpha"],
                                                      BASE_BONUS, "standard"),
                              backbone, auxiliary, BLEND_WEIGHT)
    baseline_metrics, _ = official_score(panel, baseline, year)
    if abs(baseline_metrics["final_score"] - released[year]) > NUMERIC_TOLERANCE:
        raise AssertionError(f"{year} confirmation baseline anchor off")
    log(f"{year} baseline anchor reproduced {released[year]:.15f} exactly")
    records = {"released_backbone": {k: float(v) for k, v in baseline_metrics.items()}}
    for key in passing:
        frame = pl.read_parquet(OUT / f"{key}_{year}.parquet").sort("trade_date", "ts_code")
        if not frame.select(KEYS).equals(panel.frame.select(KEYS)):
            raise AssertionError(f"{key} {year}: cache keys misaligned")
        raw = frame["pred_raw"].to_numpy().astype(np.float64)
        stable = retention_scores(panel, raw, RELEASED["alpha"], BASE_BONUS, "standard")
        prediction = blend_top_only(panel, stable, raw, auxiliary, BLEND_WEIGHT)
        metrics, daily = official_score(panel, prediction, year)
        daily.write_csv(OUT / f"{key}_{year}_daily.csv")
        delta = float(metrics["final_score"]) - released[year]
        records[key] = {**{k: float(v) for k, v in metrics.items()}, "score_delta": delta,
                        "passes_diagnostic_gate": bool(delta > NUMERIC_TOLERANCE)}
        log(f"{year} {key}: score={metrics['final_score']:.9f} ic={metrics['ic_mean']:.6f} "
            f"excess={metrics['annual_excess']:.6f} turn={metrics['mean_turnover']:.6f} "
            f"delta={delta:+.9f}")
    three_year = {}
    for key in passing:
        deltas = dict(development["candidates"][key]["score_delta"])
        deltas[str(year)] = records[key]["score_delta"]
        three_year[key] = {"score_delta": deltas, "mean_delta": sum(deltas.values()) / len(deltas),
                           "minimax_delta": min(deltas.values()),
                           "passes_three_year_gate": all(v > NUMERIC_TOLERANCE for v in deltas.values())}
    adopted = [k for k, v in three_year.items() if v["passes_three_year_gate"]]
    output = {"stage": f"confirm_{suite_name}", "generated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
              "diagnostic_year": year, "protocol_sha256": file_hash(OUT / suite["protocol"]),
              "released_composite": float(released[year]), "records": records,
              "three_year_summary": three_year, "candidates_passing_three_year_gate": adopted,
              "note": "Scored once, after the development years were recorded; no development year "
                      "was re-scored and no rule was changed.",
              "caveat": protocol.get("limitations", [])}
    result_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"{suite_name.upper()} CONFIRMATION: {len(adopted)} of {len(passing)} pass all three "
        f"years: {adopted}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("suite", choices=sorted(SUITES))
    confirm(parser.parse_args().suite)
