"""Final sweep, wave 5: add the only non-tree signal to the surviving ensemble.

W3e - the four-way cross-family rank average of released LightGBM, XGBoost, a
two-day-horizon LightGBM and a pruned-feature LightGBM - is the sweep's strongest
survivor: +0.005241/+0.001262/+0.001341 on 2022-2024 and +0.003120/+0.004657 on
the never-gated 2020/2021 audit years, pooled HAC t = 3.02.

All four of its members are gradient-boosted trees on the same Alpha158 features.
The one structurally different signal the project has is the selected GRU-cat
sequence model, whose raw 2021 IC (0.1324 against an MLP control at 0.1198)
showed the 63 daily features do not exhaust the temporal information. Standalone
it was rejected - the released post-processing stack is tuned for daily
cross-sectional tree ranks, and the sequence ensemble failed its own gate - but
rejection as a *replacement* says nothing about its value as a *minority member*
of a rank average, which is exactly the mechanism that made W3e work.

Caches already exist for all five years, so nothing is trained here:
2022-2024 from the sequence-ensemble suite, 2020-2021 from the retrain suite's
out-of-fold GRU runs (same selected configuration, cutoffs 20191231/20201231).
Verified before use: the GRU's unavailable rows are exactly the price-invalid
rows in both cache conventions, so no tradeable observation loses coverage.

One candidate is declared PRIMARY. The other is a diagnostic; adopting it instead
would require a fresh protocol.
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np
import polars as pl

from run import ROOT
from experiments.bonus_extension import file_hash
from experiments.final_sweep_wave3 import ensemble_raw

OUT = ROOT / "experiments" / "final_sweep_eval"
AUDIT = ROOT / "experiments" / "extended_audit_eval"
SEQUENCE = ROOT / "experiments" / "sequence_ensemble_eval"
KEYS = ["ts_code", "trade_date"]
SCORED_YEARS = (2022, 2023, 2024)
AUDIT_YEARS = (2020, 2021)
ALL_YEARS = AUDIT_YEARS + SCORED_YEARS
DEVELOPMENT_YEARS = (2022, 2023)
DIAGNOSTIC_YEAR = 2024
TREE_MEMBERS = ("T2f_xgboost_backbone", "W2c_two_day_horizon", "W2d_pruned_features")

MEMBERS = {
    "released_lgb": {"source": "panel_column", "column": "pred_raw",
                     "note": "the released LightGBM backbone"},
    "T2f_xgboost_backbone": {"source": "tree_cache", "note": "passed the three-year gate alone"},
    "W2c_two_day_horizon": {"source": "tree_cache", "note": "diversity member; failed 2024 alone"},
    "W2d_pruned_features": {"source": "tree_cache", "note": "diversity member; failed 2024 alone"},
    "gru_cat_sequence": {"source": "sequence_cache",
                         "note": "the selected gru_cat_h64_w20 sequence model; rejected standalone, "
                                 "tested here only as a minority member of a rank average"},
}

CANDIDATES = [
    {"key": "W5a_five_way_with_gru", "primary": True,
     "members": {"released_lgb": 1.0, "T2f_xgboost_backbone": 1.0, "W2c_two_day_horizon": 1.0,
                 "W2d_pruned_features": 1.0, "gru_cat_sequence": 1.0}},
    {"key": "W5b_gru_half_weight", "primary": False,
     "members": {"released_lgb": 1.0, "T2f_xgboost_backbone": 1.0, "W2c_two_day_horizon": 1.0,
                 "W2d_pruned_features": 1.0, "gru_cat_sequence": 0.5}},
]

PROTOCOL = {
    "experiment": "final_sweep_wave5_sequence_member_in_the_surviving_ensemble",
    "members": MEMBERS,
    "candidates": CANDIDATES,
    "primary_candidate": "W5a_five_way_with_gru",
    "reference_candidate": "W3e_lgb_xgb_twoday_pruned, already recorded in development_wave3.json "
                           "and confirmation_wave3.json; it is the comparator, not a re-run",
    "ensemble_rule": "imported unchanged from the frozen wave-3 module: per day, over rows "
                     "price-valid and finite in every member, the weighted mean of each member's "
                     "cross-sectional average rank divided by the day's count, sentinel -10.0 "
                     "elsewhere",
    "member_sources": {
        "2022-2024": "trees from final_sweep_eval/{key}_{year}.parquet; sequence from "
                     "sequence_ensemble_eval/nn_raw_{year}.parquet (column pred_raw)",
        "2020-2021": "trees from extended_audit_eval/{key}_{year}.parquet; sequence from "
                     "final_sweep_eval/gru_oof_{year}.parquet (column gru_raw)",
        "released_lgb": "the fold panel's own pred_raw column: validation/fold_{year}.parquet for "
                        "2022-2024, extended_audit_eval/folds/fold_{year}.parquet for 2020-2021",
    },
    "coverage_check": "a member's non-finite rows must be a subset of the price-invalid rows in "
                      "every year, otherwise the ensemble would drop tradeable observations",
    "postprocess": "the released stack exactly: alpha 0.9, bonus 0.3, protected-block restoration "
                   "with top_current_weight 1.0, then the 25% top-only pooled blend for 2022-2024; "
                   "the blend is disabled for 2020-2021 because no auxiliary cache exists there, "
                   "identically for baseline and candidate",
    "scorer": "the unmodified evaluate.py: official_score for 2022-2024, the anchored audit replica "
              "for 2020-2021",
    "development_years": list(DEVELOPMENT_YEARS),
    "diagnostic_year": DIAGNOSTIC_YEAR,
    "audit_years": list(AUDIT_YEARS),
    "adoption_gate": "strict improvement over the released composite in 2022 AND 2023, then 2024, "
                     "then a positive delta in both never-gated audit years",
    "baseline_anchor": "the released backbone through the same code path reproduces the released "
                       "composite to 1e-12 in 2022, 2023 and 2024",
    "retraining": "none; every member is a byte-pinned cache already scored under its own protocol",
    "prohibited_after_results": [
        "Adding or dropping members, or changing the GRU weight",
        "Adopting the diagnostic candidate without a fresh protocol",
        "Re-scoring years or modifying the release",
    ],
    "limitations": [
        "2022-2024 have been examined repeatedly; 2020-2021 were used once already, for the W3e "
        "and T2f audit, so they are no longer pristine for this wave.",
        "The GRU caches for 2020-2021 come from the retrain suite's out-of-fold runs rather than "
        "the sequence suite, though both use the same selected configuration.",
        "The pooled auxiliary was fitted against the released backbone and is not refit here.",
    ],
}


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def panel_frame(year: int) -> pl.DataFrame:
    if year in SCORED_YEARS:
        return pl.read_parquet(ROOT / "validation" / f"fold_{year}.parquet").sort("trade_date", "ts_code")
    return pl.read_parquet(AUDIT / "folds" / f"fold_{year}.parquet").sort("trade_date", "ts_code")


def member_frame(name: str, year: int) -> pl.DataFrame | None:
    if name == "released_lgb":
        return None
    if name == "gru_cat_sequence":
        if year in SCORED_YEARS:
            path, column = SEQUENCE / f"nn_raw_{year}.parquet", "pred_raw"
        else:
            path, column = OUT / f"gru_oof_{year}.parquet", "gru_raw"
    else:
        folder = OUT if year in SCORED_YEARS else AUDIT
        path, column = folder / f"{name}_{year}.parquet", "pred_raw"
    if not path.exists():
        raise SystemExit(f"Missing member cache {path}")
    frame = pl.read_parquet(path).sort("trade_date", "ts_code")
    return frame.select(KEYS).with_columns(pl.Series("pred_raw", frame[column].cast(pl.Float64)))


def member_raws(year: int, frame: pl.DataFrame) -> dict:
    valid = frame["price_valid"].to_numpy()
    raws = {"released_lgb": frame["pred_raw"].to_numpy().astype(np.float64)}
    coverage = {}
    for name in MEMBERS:
        if name == "released_lgb":
            unavailable = ~np.isfinite(raws[name])
        else:
            cache = member_frame(name, year)
            if not cache.select(KEYS).equals(frame.select(KEYS)):
                raise AssertionError(f"{name} {year}: cache keys misaligned with the fold panel")
            raws[name] = cache["pred_raw"].to_numpy().astype(np.float64)
            unavailable = ~np.isfinite(raws[name]) | (raws[name] == -1e6)
        leaked = int((unavailable & valid).sum())
        if leaked:
            raise AssertionError(f"{name} {year}: {leaked} tradeable rows lack a prediction")
        coverage[name] = {"unavailable_rows": int(unavailable.sum()),
                          "unavailable_on_tradeable_rows": leaked}
    return raws, coverage


def write_protocol() -> None:
    path = OUT / "protocol_wave5.json"
    if path.exists():
        raise SystemExit("Wave-5 protocol already frozen")
    payload = {**PROTOCOL, "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "source_sha256": file_hash(Path(__file__))}
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    log("Froze wave-5 protocol before any scoring")


def verify_protocol() -> dict:
    protocol = json.loads((OUT / "protocol_wave5.json").read_text(encoding="utf-8"))
    if protocol["source_sha256"] != file_hash(Path(__file__)):
        raise SystemExit("final_sweep_wave5.py changed after its protocol was frozen; stop")
    return protocol


def build() -> None:
    """Materialize every ensemble cache for all five years and pin the member bytes."""
    verify_protocol()
    result_path = OUT / "training_wave5.json"
    if result_path.exists():
        raise SystemExit("Wave-5 caches already built and pinned; preserving them")
    started = time.monotonic()
    record = {"generated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
              "protocol_sha256": file_hash(OUT / "protocol_wave5.json"),
              "years": {}, "caches": {}}
    for year in ALL_YEARS:
        frame = panel_frame(year)
        raws, coverage = member_raws(year, frame)
        record["years"][str(year)] = {"rows": int(len(frame)), "coverage": coverage,
                                      "panel_sha256": file_hash(
                                          (ROOT / "validation" / f"fold_{year}.parquet")
                                          if year in SCORED_YEARS else
                                          (AUDIT / "folds" / f"fold_{year}.parquet"))}
        from src.scoring import Panel

        panel = Panel.from_frame(frame)
        for candidate in CANDIDATES:
            raw = ensemble_raw(panel, candidate["members"], raws)
            path = OUT / f"{candidate['key']}_{year}.parquet"
            frame.select(KEYS).with_columns(pl.Series("pred_raw", raw)).write_parquet(
                path, compression="zstd")
            record["caches"].setdefault(str(year), {})[candidate["key"]] = {
                "path": path.name, "sha256": file_hash(path),
                "sentinel_rows": int((raw == -10.0).sum())}
            log(f"{candidate['key']} {year}: built "
                f"({int((raw == -10.0).sum()):,} sentinel rows)")
        del panel, frame, raws
    record["elapsed_seconds"] = time.monotonic() - started
    record["note"] = ("No model was trained; caches are deterministic functions of the frozen "
                      "ensemble rule and the byte-pinned member caches.")
    result_path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"Wrote {result_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("protocol", "build"))
    arguments = parser.parse_args()
    if arguments.stage == "protocol":
        write_protocol()
    else:
        build()
