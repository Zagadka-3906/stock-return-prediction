"""Scoring stage for the extra learner-family suite.

Kept in its own module so scoring-side fixes never invalidate the protocol that
pins final_sweep_extra.py (which owns the frozen rules and the training path).
The lineage check accepts training caches produced under a recorded superseded
protocol only when that protocol's rules are byte-identical to the current one.
"""
from __future__ import annotations

import hashlib
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
KEYS = ["ts_code", "trade_date"]
DEVELOPMENT_YEARS = (2022, 2023)
NUMERIC_TOLERANCE = 1e-12
AUDIT_KEYS = ("frozen_at_local", "source_sha256", "superseded_reason")


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def protocol_bytes(payload: dict) -> bytes:
    """Reproduce the on-disk bytes write_text() produced on Windows."""
    return json.dumps(payload, ensure_ascii=False, indent=2).replace("\n", "\r\n").encode("utf-8")


def verify_protocol() -> dict:
    from experiments import final_sweep_extra as pinned

    protocol = json.loads((OUT / "protocol_extra.json").read_text(encoding="utf-8"))
    if protocol["source_sha256"] != file_hash(Path(pinned.__file__)):
        raise SystemExit("final_sweep_extra.py changed after its protocol was frozen; stop")
    return protocol


def verify_lineage(training: dict) -> str:
    """Accept cached predictions only from a protocol whose RULES match the frozen one."""
    current_path = OUT / "protocol_extra.json"
    current = json.loads(current_path.read_text(encoding="utf-8"))
    for path in sorted(OUT.glob("protocol_extra_superseded_*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        pristine = {k: v for k, v in payload.items() if k != "superseded_reason"}
        if hashlib.sha256(protocol_bytes(pristine)).hexdigest() != training["protocol_sha256"]:
            continue
        drift = [k for k in current if k not in AUDIT_KEYS and pristine.get(k) != current[k]]
        if drift:
            raise SystemExit(f"Protocol rules changed between training and scoring: {drift}")
        return path.name
    raise SystemExit("Extra training was produced under an unrecorded protocol")


def develop_extra() -> None:
    protocol = verify_protocol()
    training = json.loads((OUT / "training_extra.json").read_text(encoding="utf-8"))
    if training["protocol_sha256"] != file_hash(OUT / "protocol_extra.json"):
        log(f"Lineage verified via {verify_lineage(training)}: rules byte-identical to the "
            "current protocol; only the scoring stage changed since training")
    result_path = OUT / "development_extra.json"
    if result_path.exists():
        raise SystemExit("Extra development results already recorded; preserving them")
    released = release_scores()
    started = time.monotonic()
    candidates = {}
    years = tuple(protocol["development_years"])
    if years != DEVELOPMENT_YEARS:
        raise SystemExit("Scorer years disagree with the frozen protocol")
    for year in DEVELOPMENT_YEARS:
        panel = load_panel(year)
        auxiliary = load_auxiliary(year, panel)
        backbone = panel.frame["pred_raw"].to_numpy().astype(np.float64)
        baseline = blend_top_only(panel, retention_scores(panel, backbone, RELEASED["alpha"],
                                                          BASE_BONUS, "standard"),
                                  backbone, auxiliary, BLEND_WEIGHT)
        baseline_metrics, _ = official_score(panel, baseline, year)
        if abs(baseline_metrics["final_score"] - released[year]) > NUMERIC_TOLERANCE:
            raise AssertionError(f"{year} extra-suite baseline anchor off")
        log(f"{year} baseline anchor reproduced {released[year]:.15f} exactly")
        for candidate in protocol["candidates"]:
            frame = pl.read_parquet(OUT / f"{candidate['key']}_{year}.parquet").sort("trade_date", "ts_code")
            if not frame.select(KEYS).equals(panel.frame.select(KEYS)):
                raise AssertionError(f"{candidate['key']} {year}: cache keys misaligned")
            raw = frame["pred_raw"].to_numpy().astype(np.float64)
            stable = retention_scores(panel, raw, RELEASED["alpha"], BASE_BONUS, "standard")
            prediction = blend_top_only(panel, stable, raw, auxiliary, BLEND_WEIGHT)
            metrics, daily = official_score(panel, prediction, year)
            item = candidates.setdefault(candidate["key"], {"years": {}})
            item["years"][str(year)] = {k: float(v) for k, v in metrics.items()}
            daily.write_csv(OUT / f"{candidate['key']}_{year}_daily.csv")
            log(f"{year} {candidate['key']}: score={metrics['final_score']:.9f} "
                f"ic={metrics['ic_mean']:.6f} excess={metrics['annual_excess']:.6f} "
                f"turn={metrics['mean_turnover']:.6f}")
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
    output = {"stage": "develop_extra", "generated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
              "elapsed_seconds": time.monotonic() - started,
              "protocol_sha256": file_hash(OUT / "protocol_extra.json"),
              "candidates": candidates, "candidates_passing_development_gate": passing,
              "caveat": protocol["limitations"]}
    result_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"EXTRA DEVELOPMENT: {len(passing)} of {len(candidates)} pass: {passing}")




if __name__ == "__main__":
    develop_extra()
