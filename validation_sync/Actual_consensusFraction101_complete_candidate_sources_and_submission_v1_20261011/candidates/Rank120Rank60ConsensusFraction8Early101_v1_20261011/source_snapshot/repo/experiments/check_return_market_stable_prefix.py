"""Exact real-prefix and prediction propagation checks for the stable repair.

Public check functions return evidence without writing files. They do not load
validation labels, train models, or compute performance scores.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import lightgbm as lgb
import numpy as np
import polars as pl

from experiments import return_market_stable_features as stable
from run import feature_names

CUTOFF = 20180531
THREADS = 4
OUT = stable.OUT
KEYS = stable.KEYS


def _prefix_matrices() -> tuple[np.ndarray, np.ndarray, np.ndarray, dict]:
    stable.verify_feature_inputs(require_prefix=False)
    manifest = json.loads((OUT/"feature_manifest.json").read_text(encoding="utf-8"))
    source = stable._source().filter(pl.col("trade_date") <= CUTOFF).collect()
    if (source.height != 460350 or source["ts_code"].n_unique() != 4650
            or source["trade_date"].n_unique() != 99):
        raise ValueError("Expected the complete 2018-05-31 real prefix")
    daily = source.group_by("trade_date").agg(pl.len().alias("rows"), pl.col("ts_code").n_unique().alias("stocks"))
    if not daily.select(((pl.col("rows") == 4650) & (pl.col("stocks") == 4650)).all()).item():
        raise ValueError("Every prefix date must contain all 4,650 securities")
    fresh = stable.build_frame(source)
    frozen = pl.scan_parquet(stable.ADDED_FEATURE_FILE).filter(pl.col("trade_date") <= CUTOFF).collect().sort(KEYS)
    comparison = stable._comparison(fresh, frozen)
    for name in stable.FEATURE_NAMES:
        if fresh.schema[name] != pl.Float32 or frozen.schema[name] != pl.Float32:
            raise ValueError("The real-prefix audit requires Float32 feature storage")
    exact = all(item["null_masks_exact"] and item["nonexact_count"] == 0
                and item["nonfinite_nonnull_count"] == 0 for item in comparison.values())
    original = feature_names()
    features = original+stable.FEATURE_NAMES
    if len(original) != 63 or len(features) != 71:
        raise ValueError("Expected the fixed 63+8 feature order")
    base = pl.scan_parquet(stable.ROOT/"data/features.parquet").filter(
        pl.col("is_train") & (pl.col("trade_date") <= CUTOFF)
    ).select(*KEYS, "price_valid", *original).collect().sort(KEYS)
    if not base.select(KEYS).equals(fresh.select(KEYS)):
        raise ValueError("Original and new features do not cover identical prefix keys")
    matrices = []
    for extra in (fresh, frozen):
        joined = base.join(extra, on=KEYS, how="left", validate="1:1", maintain_order="left")
        if not joined.select(KEYS).equals(base.select(KEYS)):
            raise ValueError("Prefix left join changed original row order")
        matrices.append(np.ascontiguousarray(joined.select(features).to_numpy(), dtype=np.float32))
    x, z = matrices
    valid = np.isfinite(x) & np.isfinite(z)
    mask_exact = bool(np.array_equal(np.isnan(x), np.isnan(z)))
    count = int(np.count_nonzero((x != z) & valid))
    delta = np.abs(x[valid].astype(float)-z[valid].astype(float))
    price_valid = base["price_valid"].to_numpy()
    record = {"status": "passed" if exact and mask_exact and count == 0 else "feature_difference_detected",
              "cutoff_inclusive": CUTOFF, "rows": len(base), "securities": 4650, "dates": 99,
              "full_cross_section_prefix": True, "original_features": 63, "total_features": 71,
              "market_features": stable.FEATURE_NAMES, "feature_order": features,
              "feature_comparison": comparison, "all_market_values_float32_exact": exact,
              "matrix_null_masks_exact": mask_exact, "matrix_nonexact_nonnull_cells": count,
              "matrix_max_absolute_error": float(delta.max()) if delta.size else 0.0,
              "matrix_dtype": "float32", "valid_price_rows": int(price_valid.sum()),
              "invalid_price_sentinel": -1e6, "null_policy": "No filling; null becomes NaN",
              "labels_read": False, "validation_labels_loaded": False, "scores_computed": False,
              "future_rows_used_for_feature_build": False,
              "input_columns": stable.INPUT_COLUMNS,
              "io_note": "CSV scanning and provenance hashes may read future file bytes; only projected raw input columns and rows through 20180531 are supplied to feature computation. No labels are materialized.",
              "stored_features_sha256": manifest["features_sha256"],
              "feature_module_sha256": manifest["feature_module_sha256"],
              "prefix_source_sha256": stable.file_hash(Path(__file__)),
              "scope_note": "Pure numerical prefix test, not a performance evaluation. No model, cache, source or audit artifact is modified."}
    return x, z, price_valid, record


def check_prefix_features() -> dict:
    started = time.monotonic()
    _, _, _, record = _prefix_matrices()
    record["seconds"] = time.monotonic()-started
    return record


def check_model_prefix(year: int) -> dict:
    if year not in (2022, 2023, 2024):
        raise ValueError("Only the three predeclared annual models are supported")
    started = time.monotonic()
    model_path = OUT/f"return_market_stable_z1_99_{year}.txt"
    meta_path = OUT/f"return_market_stable_z1_99_{year}.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    model_sha = stable.file_hash(model_path)
    if model_sha != meta["model_sha256"]:
        raise ValueError("Stable return model differs from its saved metadata")
    model = lgb.Booster(model_str=model_path.read_text(encoding="utf-8"))
    x, z, valid_price, record = _prefix_matrices()
    if model.feature_name() != record["feature_order"] or meta["features"] != record["feature_order"]:
        raise ValueError("Stable return model feature order differs from the fixed 71 columns")
    a, b = model.predict(x, num_threads=THREADS), model.predict(z, num_threads=THREADS)
    a32, b32 = a.astype(np.float32), b.astype(np.float32)
    a32[~valid_price] = b32[~valid_price] = -1e6
    raw_nonexact = int(np.count_nonzero(a != b))
    stored_nonexact = int(np.count_nonzero(a32 != b32))
    finite = bool(np.isfinite(a).all() and np.isfinite(b).all() and np.isfinite(a32).all() and np.isfinite(b32).all())
    record.update({"year": year, "model_sha256": model_sha, "model_metadata_sha256": stable.file_hash(meta_path),
                   "model_output_float64_nonexact_count": raw_nonexact,
                   "model_output_float64_max_absolute_error": float(np.max(np.abs(a-b))),
                   "model_output_valid_price_nonexact_count": int(np.count_nonzero(a[valid_price] != b[valid_price])),
                   "production_float32_with_sentinel_nonexact_count": stored_nonexact,
                   "production_float32_with_sentinel_max_absolute_error": float(np.max(np.abs(a32.astype(float)-b32.astype(float)))),
                   "all_predictions_finite": finite, "threads": THREADS, "seconds": time.monotonic()-started})
    if record["status"] == "passed" and (raw_nonexact or stored_nonexact or not finite):
        record["status"] = "prediction_difference_detected"
    return record
