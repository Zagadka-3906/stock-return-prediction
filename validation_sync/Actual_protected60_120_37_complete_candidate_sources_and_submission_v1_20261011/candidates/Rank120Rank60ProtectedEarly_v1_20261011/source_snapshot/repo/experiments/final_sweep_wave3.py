"""Final sweep, wave 3: cross-family rank-average ensembles of already-scored backbones.

Why this wave exists. After 22 candidates the only three-year survivor is the
XGBoost backbone (T2f), which beats the released LightGBM backbone by +0.000238
(2022), +0.001379 (2023) and +0.003022 (2024). Two wave-2 candidates won the
development years and then lost 2024, which is exactly the failure mode an
ensemble is meant to damp: averaging two learners with different inductive
biases reduces the variance that let a single retargeted backbone win two years
and lose the third.

This is NOT the previously rejected "seed ensemble". That record averaged the
same learner family across seeds, so the members shared one inductive bias and
one failure mode. The members here are LightGBM (released), XGBoost (T2f), a
two-day-horizon LightGBM (W2c) and a pruned-feature LightGBM (W2d): different
splitting algorithms, different regularization and, for two of them, different
labels and feature sets. Nothing is retrained; every member is the exact cache
that was already scored under its own frozen protocol, so the only new degrees
of freedom are the member set and the weights, both fixed here before scoring.

One candidate is declared PRIMARY in advance. The others are diagnostics: they
are reported but adopting one instead of the primary would require a fresh
protocol, because choosing the best of five on the development years is exactly
the selection bias the three-year gate is meant to police.
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np
import polars as pl
from scipy.stats import rankdata

from run import ROOT
from experiments.bonus_extension import file_hash, load_panel

OUT = ROOT / "experiments" / "final_sweep_eval"
KEYS = ["ts_code", "trade_date"]
YEARS = (2022, 2023, 2024)
DEVELOPMENT_YEARS = (2022, 2023)
DIAGNOSTIC_YEAR = 2024
SENTINEL = -10.0

MEMBERS = {
    "released_lgb": {"source": "panel_column", "column": "pred_raw",
                     "note": "the released LightGBM backbone, unchanged"},
    "T2f_xgboost_backbone": {"source": "cache",
                             "note": "passed the three-year gate on its own"},
    "W2c_two_day_horizon": {"source": "cache",
                            "note": "won 2022+2023, lost 2024; diversity member only"},
    "W2d_pruned_features": {"source": "cache",
                            "note": "won 2022+2023, lost 2024; diversity member only"},
}

CANDIDATES = [
    {"key": "W3a_lgb_xgb", "primary": True,
     "members": {"released_lgb": 0.5, "T2f_xgboost_backbone": 0.5}},
    {"key": "W3b_lgb_xgb_xgb0.35", "primary": False,
     "members": {"released_lgb": 0.65, "T2f_xgboost_backbone": 0.35}},
    {"key": "W3c_lgb_xgb_xgb0.65", "primary": False,
     "members": {"released_lgb": 0.35, "T2f_xgboost_backbone": 0.65}},
    {"key": "W3d_lgb_xgb_twoday", "primary": False,
     "members": {"released_lgb": 1.0, "T2f_xgboost_backbone": 1.0, "W2c_two_day_horizon": 1.0}},
    {"key": "W3e_lgb_xgb_twoday_pruned", "primary": False,
     "members": {"released_lgb": 1.0, "T2f_xgboost_backbone": 1.0, "W2c_two_day_horizon": 1.0,
                 "W2d_pruned_features": 1.0}},
]

PROTOCOL = {
    "experiment": "final_sweep_wave3_cross_family_ensembles",
    "members": MEMBERS,
    "candidates": CANDIDATES,
    "primary_candidate": "W3a_lgb_xgb",
    "ensemble_rule": "per day, over rows that are price-valid and finite in every member: the "
                     "weighted mean of each member's cross-sectional average rank divided by the "
                     "day's member count, weights normalized to sum to one; all other rows take the "
                     "sentinel -10.0, matching the already-validated rank_average convention",
    "postprocess": "the released stack exactly: alpha 0.9, bonus 0.3, protected-block restoration "
                   "with top_current_weight 1.0, then the 25% top-only pooled blend",
    "scorer": "Unmodified evaluate.py via official_score",
    "development_years": list(DEVELOPMENT_YEARS),
    "diagnostic_year": DIAGNOSTIC_YEAR,
    "adoption_gate": "strict improvement over the released composite in 2022 AND 2023, then 2024; "
                     "identical to every earlier suite",
    "baseline_anchor": "the released backbone through the same code path reproduces the released "
                       "composite to 1e-12 in every scored year",
    "retraining": "none; members are byte-pinned caches already scored under their own protocols",
    "distinct_from_seed_ensemble": "the rejected seed-ensemble record averaged one learner family "
                                   "across seeds; these members differ in algorithm, regularization "
                                   "and, for W2c and W2d, in label and feature set",
    "prohibited_after_results": [
        "Adding or dropping ensemble members",
        "Retuning weights, including promoting a diagnostic weight over the primary",
        "Adopting a diagnostic candidate without a fresh protocol frozen before further scoring",
        "Re-scoring years or modifying the release",
    ],
    "limitations": [
        "2022-2024 are repeatedly examined historical years, so a three-year pass is evidence "
        "against a fluke, not proof of out-of-sample edge.",
        "The pooled auxiliary is still the one fitted against the released backbone; a genuinely "
        "different backbone deserves a refitted auxiliary and does not have one here.",
        "Five candidates are scored on the same two development years; only the pre-declared "
        "primary is adoptable without a new protocol.",
    ],
}


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def member_path(key: str, year: int) -> Path:
    return OUT / f"{key}_{year}.parquet"


def ensemble_raw(panel, members: dict, cache_raws: dict) -> np.ndarray:
    """Weighted cross-sectional rank average; weights are normalized to sum to one."""
    shape = panel.valid_price.shape
    total = sum(members.values())
    arrays = []
    for name in members:
        if name not in cache_raws:
            raise KeyError(name)
        arrays.append((np.asarray(cache_raws[name], dtype=np.float64).reshape(shape),
                       members[name] / total))
    out = np.full(shape, SENTINEL, dtype=np.float64)
    for day in range(shape[0]):
        keep = panel.valid_price[day].copy()
        for array, _ in arrays:
            keep &= np.isfinite(array[day])
        count = int(keep.sum())
        if not count:
            continue
        mixed = np.zeros(count, dtype=np.float64)
        for array, weight in arrays:
            mixed += weight * rankdata(array[day][keep], method="average") / count
        out[day][keep] = mixed
    return out.reshape(-1)


def write_protocol() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "protocol_wave3.json"
    if path.exists():
        raise SystemExit("Wave-3 protocol already frozen")
    payload = {**PROTOCOL, "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "source_sha256": file_hash(Path(__file__)),
               "released_baseline_scores": {str(k): v for k, v in
                                            json.loads(json.dumps(_released())).items()}}
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    log("Froze wave-3 protocol before any scoring")


def _released() -> dict:
    from experiments.bonus_extension import release_scores

    return {str(k): float(v) for k, v in release_scores().items()}


def verify_protocol() -> dict:
    protocol = json.loads((OUT / "protocol_wave3.json").read_text(encoding="utf-8"))
    if protocol["source_sha256"] != file_hash(Path(__file__)):
        raise SystemExit("final_sweep_wave3.py changed after its protocol was frozen; stop")
    return protocol


def build() -> None:
    """Materialize every ensemble cache and pin the bytes it was built from."""
    protocol = verify_protocol()
    result_path = OUT / "training_wave3.json"
    if result_path.exists():
        raise SystemExit("Wave-3 caches already built and pinned; preserving them")
    started = time.monotonic()
    inventory = {}
    for year in YEARS:
        panel = load_panel(year)
        frame = panel.frame
        cache_raws = {"released_lgb": frame["pred_raw"].to_numpy().astype(np.float64)}
        inventory.setdefault("members", {})[str(year)] = {}
        for name in MEMBERS:
            if name == "released_lgb":
                inventory["members"][str(year)][name] = {"source": "panel_column",
                                                         "rows": int(len(frame))}
                continue
            path = member_path(name, year)
            if not path.exists():
                raise SystemExit(f"Missing member cache {path.name}")
            member = pl.read_parquet(path).sort("trade_date", "ts_code")
            if not member.select(KEYS).equals(frame.select(KEYS)):
                raise AssertionError(f"{name} {year}: cache keys misaligned with the panel")
            cache_raws[name] = member["pred_raw"].to_numpy().astype(np.float64)
            inventory["members"][str(year)][name] = {"source": path.name,
                                                     "sha256": file_hash(path),
                                                     "rows": int(len(member))}
        for candidate in CANDIDATES:
            unknown = [m for m in candidate["members"] if m not in cache_raws]
            if unknown:
                raise SystemExit(f"{candidate['key']} {year}: members not loaded {unknown}")
            raw = ensemble_raw(panel, candidate["members"], cache_raws)
            out_path = OUT / f"{candidate['key']}_{year}.parquet"
            frame.select(KEYS).with_columns(pl.Series("pred_raw", raw)).write_parquet(out_path)
            inventory.setdefault("caches", {}).setdefault(str(year), {})[candidate["key"]] = {
                "path": out_path.name, "sha256": file_hash(out_path),
                "finite_rows": int(np.isfinite(raw).sum()),
                "sentinel_rows": int((raw == SENTINEL).sum())}
            log(f"{candidate['key']} {year}: built ({inventory['caches'][str(year)][candidate['key']]['sentinel_rows']:,} sentinel rows)")
        del panel, frame, cache_raws
    output = {"stage": "build_wave3", "generated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
              "elapsed_seconds": time.monotonic() - started,
              "protocol_sha256": file_hash(OUT / "protocol_wave3.json"),
              "years": list(YEARS), **inventory,
              "note": "No model was trained; caches are deterministic functions of the frozen "
                      "ensemble rule and the byte-pinned member caches."}
    result_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"Wrote {result_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("protocol", "build"))
    arguments = parser.parse_args()
    if arguments.stage == "protocol":
        write_protocol()
    else:
        build()
