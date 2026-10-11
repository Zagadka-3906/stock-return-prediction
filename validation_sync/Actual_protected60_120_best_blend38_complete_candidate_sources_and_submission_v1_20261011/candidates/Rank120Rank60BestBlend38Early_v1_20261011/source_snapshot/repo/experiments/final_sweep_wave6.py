"""Final sweep, wave 6: cross-sectional normalization of the existing 63 features.

The last mechanism class not covered by a frozen record. "Feature expansion" was
about *adding* columns and is rejected; this changes the *representation* of the
columns already in force and nothing else - same label, same LightGBM parameters,
same 180 rounds, same post-processing, same gate.

Why it could matter. Trees are invariant to any global monotone transform of a
feature, so normalizing per column over the whole history would be a no-op. They
are *not* invariant to a per-day cross-sectional transform, because that removes
day-to-day level shifts before the pooled split thresholds are chosen. Features
such as volume, amount, illiquidity and volatility carry strong regime levels
across 2018-2024, while the prediction target is a *within-day* rank and the
score is a *within-day* cross-sectional statistic. Making the inputs
cross-sectionally comparable is the standard remedy, and it has never been tried
here.

Two variants, one declared PRIMARY before any scoring:

  W6a daily rank    each feature becomes its percentile rank among that day's
                    price-valid stocks, in (0, 1]; robust to outliers and to
                    fat-tailed levels, and monotone within the day so no
                    within-day ordering information is lost.
  W6b daily z-score  each feature is centered and scaled by that day's
                    cross-sectional mean and standard deviation; keeps magnitude
                    information that ranking discards, at the cost of sensitivity
                    to outliers.

An identity-transform harness run proves the plumbing: rebuilding the released
2022 fold through this module's own training path must reproduce
validation/fold_2022.parquet bit-for-bit, so any difference in the scored
candidates is attributable to the transform alone.
"""
from __future__ import annotations

import argparse
import gc
import json
import time
from pathlib import Path

import lightgbm as lgb
import numpy as np
import polars as pl
from scipy.stats import rankdata

from run import FEATURE_FILE, ROOT, feature_names, fold_cutoff, to_matrix
from experiments.bonus_extension import file_hash
from experiments.final_sweep_wave2 import BASE_PARAMS, ROUNDS, flat_indices
from experiments.final_sweep_wave5 import log
from experiments.sequence_model import load_panel as load_seq_panel

OUT = ROOT / "experiments" / "final_sweep_eval"
AUDIT_FOLDS = ROOT / "experiments" / "extended_audit_eval" / "folds"
KEYS = ["ts_code", "trade_date"]
SCORED_YEARS = (2022, 2023, 2024)
AUDIT_YEARS = (2020, 2021)
ALL_YEARS = AUDIT_YEARS + SCORED_YEARS
DEVELOPMENT_YEARS = (2022, 2023)
DIAGNOSTIC_YEAR = 2024
SENTINEL = -1e6

CANDIDATES = [
    {"key": "W6a_daily_rank_features", "primary": True, "transform": "rank"},
    {"key": "W6b_daily_zscore_features", "primary": False, "transform": "zscore"},
]

PROTOCOL = {
    "experiment": "final_sweep_wave6_cross_sectional_feature_normalization",
    "candidates": CANDIDATES,
    "primary_candidate": "W6a_daily_rank_features",
    "transforms": {
        "rank": "per day and feature, rankdata(method='average', nan_policy='omit') over the "
                "price-valid stocks divided by that day's count of finite values, giving (0, 1]; "
                "an entry that is missing in the source stays missing, because LightGBM routes "
                "missing values natively and the released recipe already relies on that",
        "zscore": "per day and feature, (x - nanmean) / nanstd over the price-valid stocks; when "
                  "that day's mean is non-finite or its standard deviation is non-finite or exactly "
                  "zero the feature carries no cross-sectional information that day, so every "
                  "stock takes the neutral value 0.0 rather than being divided by a floor (which "
                  "would fabricate extreme values) or being marked missing (which would destroy "
                  "finite source values); a source-missing entry stays missing. Genuinely tiny "
                  "scales are preserved, not floored (ILLIQ has a pooled std of 8.15e-09)",
        "identity": "harness only: no transform, used to prove the training path reproduces the "
                    "released 2022 fold bit-for-bit; never scored",
    },
    "missing_value_invariant": "the transform may never destroy a finite source value; it may only "
                               "add missing entries where a day/feature has no usable dispersion. "
                               "Both counts are recorded per candidate and year",
    "everything_else_unchanged": "label y_rank, LightGBM parameters, 180 rounds, seed 2026, the "
                                 "released post-processing stack and the 25% pooled blend",
    "postprocess": "the released stack exactly: alpha 0.9, bonus 0.3, protected-block restoration "
                   "with top_current_weight 1.0, then the 25% top-only pooled blend",
    "scorer": "the unmodified evaluate.py via official_score for 2022-2024, and via the anchored "
              "audit replica for 2020-2021 without the pooled blend",
    "development_years": list(DEVELOPMENT_YEARS),
    "diagnostic_year": DIAGNOSTIC_YEAR,
    "audit_years": list(AUDIT_YEARS),
    "adoption_gate": "strict improvement over the released composite in 2022 AND 2023, then 2024, "
                     "then a positive delta in both never-gated audit years",
    "baseline_anchor": "the released backbone through the same code path reproduces the released "
                       "composite to 1e-12 in 2022, 2023 and 2024",
    "harness_proof": "the identity transform must rebuild validation/fold_2022.parquet bit-for-bit",
    "training_rows": "is_train, trade_date < fold_cutoff(year), y_rank not null and price_valid, "
                     "sorted by trade_date then ts_code, identical to the released recipe",
    "prohibited_after_results": [
        "Adding transforms, mixing them, or normalizing over multi-day windows",
        "Retuning LightGBM parameters for a transformed representation",
        "Adopting the diagnostic candidate without a fresh protocol",
        "Re-scoring years or modifying the release",
    ],
    "limitations": [
        "2022-2024 have been examined repeatedly by six earlier suites.",
        "Wave-4 showed that a configuration winning on 2020-2021 can lose on 2022-2023, so the "
        "audit years are corroborating evidence, not a substitute for the gate.",
        "Rank normalization discards cross-sectional magnitude, which may matter for the excess "
        "term even when it does not matter for rank IC.",
    ],
}


def write_protocol() -> None:
    path = OUT / "protocol_wave6.json"
    if path.exists():
        raise SystemExit("Wave-6 protocol already frozen")
    payload = {**PROTOCOL, "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "source_sha256": file_hash(Path(__file__))}
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    log("Froze wave-6 protocol before any training or scoring")


def verify_protocol() -> dict:
    protocol = json.loads((OUT / "protocol_wave6.json").read_text(encoding="utf-8"))
    if protocol["source_sha256"] != file_hash(Path(__file__)):
        raise SystemExit("final_sweep_wave6.py changed after its protocol was frozen; stop")
    return protocol


def transform_panel(x: np.ndarray, valid: np.ndarray, kind: str) -> np.ndarray:
    """Apply a per-day cross-sectional transform; invalid entries stay NaN."""
    if kind == "identity":
        out = x.astype(np.float32, copy=True)
        out[~valid] = np.nan
        return out
    days, stocks, features = x.shape
    out = np.full((days, stocks, features), np.nan, dtype=np.float32)
    masked = x.astype(np.float32, copy=True)
    masked[~valid] = np.nan
    for index in range(features):
        column = masked[:, :, index].astype(np.float64)
        if kind == "rank":
            ranked = rankdata(column, method="average", axis=1, nan_policy="omit")
            counts = np.isfinite(column).sum(axis=1, keepdims=True)
            with np.errstate(invalid="ignore", divide="ignore"):
                scaled = np.where(counts > 0, ranked / np.maximum(counts, 1), np.nan)
        elif kind == "zscore":
            with np.errstate(invalid="ignore"):
                mean = np.nanmean(column, axis=1, keepdims=True)
                std = np.nanstd(column, axis=1, keepdims=True)
            undefined = ~np.isfinite(std) | (std == 0.0) | ~np.isfinite(mean)
            safe_std = np.where(undefined, 1.0, std)
            scaled = (column - mean) / safe_std
            scaled[np.broadcast_to(undefined, column.shape)] = 0.0
            scaled[~np.isfinite(column)] = np.nan
        else:
            raise ValueError(f"Unknown transform {kind}")
        out[:, :, index] = scaled.astype(np.float32)
    del masked
    gc.collect()
    return out


def released_training_frame(features: list[str], cutoff: int) -> pl.DataFrame:
    """run.train_fold's exact training query: unsorted, because bagging is order-sensitive."""
    return (pl.scan_parquet(FEATURE_FILE)
            .filter(pl.col("is_train") & (pl.col("trade_date") < cutoff)
                    & pl.col("y_rank").is_not_null() & pl.col("price_valid"))
            .select(KEYS + features + ["y_rank"]).collect())


def released_validation_frame(year: int) -> pl.DataFrame:
    return (pl.scan_parquet(FEATURE_FILE)
            .filter(pl.col("is_train")
                    & pl.col("trade_date").is_between(year * 10000 + 101, year * 10000 + 1231))
            .sort("trade_date", "ts_code").collect())


def fit(features: list[str], matrix: np.ndarray, label: np.ndarray) -> lgb.Booster:
    return lgb.train(BASE_PARAMS, lgb.Dataset(matrix, label=label, feature_name=features,
                                              free_raw_data=True), num_boost_round=ROUNDS)


def harness_proof(features: list[str]) -> dict:
    """Two separate proofs: the plumbing, then the panel mapping the candidates rely on."""
    year = 2022
    cutoff = fold_cutoff(year)
    train_frame = released_training_frame(features, cutoff)
    label = train_frame["y_rank"].to_numpy().astype(np.float32)
    model = fit(features, to_matrix(train_frame, features), label)
    valid_frame = released_validation_frame(year)
    raw = model.predict(to_matrix(valid_frame, features)).astype(np.float32)
    raw[~valid_frame["price_valid"].to_numpy()] = SENTINEL
    reference = pl.read_parquet(ROOT / "validation" / f"fold_{year}.parquet").sort("trade_date", "ts_code")
    plumbing = bool(valid_frame.select(KEYS).equals(reference.select(KEYS))
                    and np.array_equal(raw, reference["pred_raw"].to_numpy().astype(np.float32)))
    log(f"Harness proof A (plumbing): rebuilt the released 2022 fold identical = {plumbing}")
    if not plumbing:
        raise AssertionError("Wave-6 training path does not reproduce the released 2022 fold")
    del model, raw, valid_frame
    gc.collect()
    dates, codes, x, _, valid, _ = load_seq_panel(features, 2024)
    idx = flat_indices(train_frame, np.asarray(dates), np.asarray(codes), len(codes))
    mapped = np.ascontiguousarray(x.reshape(-1, len(features))[idx], dtype=np.float32)
    direct = to_matrix(train_frame, features)
    panel_faithful = bool(np.array_equal(mapped, direct, equal_nan=True))
    worst = float(np.nanmax(np.abs(mapped - direct))) if not panel_faithful else 0.0
    log(f"Harness proof B (panel mapping): sequence panel equals the frame matrix = "
        f"{panel_faithful} (max abs difference {worst:.3e})")
    if not panel_faithful:
        raise AssertionError("The sequence panel is not a faithful copy of the feature frame")
    del mapped, direct, idx, x, valid, dates, codes
    gc.collect()
    return {"released_fold_2022_bit_identical": plumbing,
            "sequence_panel_equals_feature_frame": panel_faithful}


def train() -> None:
    protocol = verify_protocol()
    result_path = OUT / "training_wave6.json"
    if result_path.exists():
        raise SystemExit("Wave-6 training already recorded; preserving it")
    features = feature_names()
    started = time.monotonic()
    record = {"generated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
              "protocol_sha256": file_hash(OUT / "protocol_wave6.json"), "candidates": {}}
    record["harness_proof"] = harness_proof(features)
    dates, codes, x, _, valid, _ = load_seq_panel(features, 2024)
    dates_arr, codes_arr = np.asarray(dates), np.asarray(codes)
    n_codes = len(codes)
    record["panel"] = {"days": len(dates), "stocks": n_codes, "features": len(features)}
    source_missing = ~np.isfinite(x.reshape(-1, len(features)))
    folds = {}
    for year in ALL_YEARS:
        fold = ((ROOT / "validation" / f"fold_{year}.parquet") if year in SCORED_YEARS
                else (AUDIT_FOLDS / f"fold_{year}.parquet"))
        folds[year] = (pl.read_parquet(fold).sort("trade_date", "ts_code")
                       .select(KEYS + ["price_valid"]))
    for candidate in CANDIDATES:
        key, transform = candidate["key"], candidate["transform"]
        record["candidates"][key] = {}
        transform_started = time.monotonic()
        z = transform_panel(x, valid, transform)
        flat = z.reshape(-1, len(features))
        del z
        gc.collect()
        record["candidates"][key]["transform_seconds"] = time.monotonic() - transform_started
        log(f"{key}: transformed panel in {record['candidates'][key]['transform_seconds']:.0f}s")
        for year in ALL_YEARS:
            train_frame = released_training_frame(features, fold_cutoff(year))
            idx = flat_indices(train_frame, dates_arr, codes_arr, n_codes)
            label = train_frame["y_rank"].to_numpy().astype(np.float32)
            matrix = np.ascontiguousarray(flat[idx], dtype=np.float32)
            source = source_missing[idx]
            destroyed = int((~np.isfinite(matrix) & ~source).sum())
            if destroyed:
                raise AssertionError(f"{key} {year}: the transform destroyed {destroyed} finite "
                                     "source values")
            missing_cells = int((~np.isfinite(matrix)).sum())
            added_missing = missing_cells - int(source.sum())
            model = fit(features, matrix, label)
            del matrix, idx, label, train_frame, source
            gc.collect()
            predict_frame = folds[year]
            predict_idx = flat_indices(predict_frame, dates_arr, codes_arr, n_codes)
            predict_matrix = np.ascontiguousarray(flat[predict_idx], dtype=np.float32)
            raw = model.predict(predict_matrix).astype(np.float64)
            raw[~predict_frame["price_valid"].to_numpy()] = SENTINEL
            cache = OUT / f"{key}_{year}.parquet"
            predict_frame.select(KEYS).with_columns(pl.Series("pred_raw", raw)).write_parquet(
                cache, compression="zstd")
            record["candidates"][key][str(year)] = {
                "cache": cache.name, "cache_sha256": file_hash(cache), "rows": int(len(raw)),
                "sentinel_rows": int((raw == SENTINEL).sum()),
                "training_missing_cells": missing_cells,
                "training_added_missing_cells": added_missing}
            log(f"{key} {year}: rows={len(raw):,}")
            del model, raw, predict_matrix, predict_idx
            gc.collect()
        del flat
        gc.collect()
    record["elapsed_seconds"] = time.monotonic() - started
    result_path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"Wrote {result_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("protocol", "train"))
    arguments = parser.parse_args()
    if arguments.stage == "protocol":
        write_protocol()
    else:
        train()
