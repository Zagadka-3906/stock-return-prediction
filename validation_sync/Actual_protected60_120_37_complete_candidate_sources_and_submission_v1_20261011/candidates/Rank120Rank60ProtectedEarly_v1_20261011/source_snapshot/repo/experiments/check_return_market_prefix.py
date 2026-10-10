"""Read-only prefix and numerical-propagation checks for the 71-feature head.

``check_model_prefix(year)`` returns evidence but never writes an artifact,
trains a model, loads annual validation labels, or computes performance scores.
The fixed real prefix is 4,650 securities and 99 dates ending on 2018-05-31.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import lightgbm as lgb
import numpy as np
import polars as pl

from experiments import feature_expansion_features as added
from experiments.check_feature_expansion_prefix import (
    ATOL, CUTOFF, KEYS, RTOL, THREADS, _prefix_frames, _verified_manifest,
)
from experiments.feature_expansion import features_for_variant


OUT = added.ROOT / "experiments" / "return_market_eval"


def _prefix_matrices() -> tuple[np.ndarray, np.ndarray, np.ndarray, dict]:
    manifest = _verified_manifest()
    source, fresh, frozen = _prefix_frames()
    features = features_for_variant("market")
    market = added.GROUPS["market_relative"]
    original = features[:-len(market)]
    if len(features) != 71 or len(original) != 63 or features[-8:] != market:
        raise ValueError("Expected the fixed original-63 plus market-8 feature order")
    if source.get_column("trade_date").max() > CUTOFF:
        raise AssertionError("Future rows reached the prefix feature builder")
    date_counts = source.group_by("trade_date").agg(
        pl.len().alias("rows"), pl.col("ts_code").n_unique().alias("securities"))
    if not date_counts.select(((pl.col("rows") == 4650) & (pl.col("securities") == 4650)).all()).item():
        raise AssertionError("Every prefix date must retain the full 4,650-security cross-section")

    comparisons = {}
    for name in market:
        a, b = fresh.get_column(name).to_numpy(), frozen.get_column(name).to_numpy()
        valid = np.isfinite(a) & np.isfinite(b)
        delta = np.abs(a[valid].astype(np.float64) - b[valid].astype(np.float64))
        comparisons[name] = {
            "null_masks_exact": bool(np.array_equal(np.isnan(a), np.isnan(b))),
            "nonnull_compared": int(valid.sum()),
            "nonexact_count": int(np.count_nonzero(a[valid] != b[valid])),
            "max_absolute_difference": float(delta.max()) if delta.size else 0.0,
            "isclose_all": bool(np.allclose(a, b, rtol=RTOL, atol=ATOL, equal_nan=True)),
        }
    base = pl.scan_parquet(added.ROOT / "data/features.parquet").filter(
        pl.col("is_train") & (pl.col("trade_date") <= CUTOFF)
    ).select(*KEYS, "price_valid", *original).collect().sort(KEYS)
    if not base.select(KEYS).equals(fresh.select(KEYS)):
        raise ValueError("The original feature store does not cover the same sorted prefix keys")
    matrices = []
    for extra in (fresh, frozen):
        joined = base.join(extra.select(*KEYS, *market), on=KEYS, how="left",
                           validate="1:1", maintain_order="left")
        if joined.height != base.height or not joined.select(KEYS).equals(base.select(KEYS)):
            raise AssertionError("Feature left join changed prefix row order or count")
        matrices.append(np.ascontiguousarray(joined.select(features).to_numpy(), dtype=np.float32))
    x, z = matrices
    valid_price = base.get_column("price_valid").to_numpy()
    masks_exact = bool(np.array_equal(np.isnan(x), np.isnan(z)))
    finite = np.isfinite(x) & np.isfinite(z)
    delta = np.abs(x[finite].astype(np.float64) - z[finite].astype(np.float64))
    passed = masks_exact and all(item["null_masks_exact"] and item["isclose_all"]
                                 for item in comparisons.values())
    record = {
        "status": "passed" if passed else "feature_difference_detected",
        "cutoff_inclusive": CUTOFF, "rows": base.height, "securities": 4650, "dates": 99,
        "full_cross_section_prefix": True, "original_features": len(original),
        "market_features": market, "total_features": len(features),
        "feature_order": features, "feature_comparison": comparisons,
        "feature_tolerance": {"relative": RTOL, "absolute": ATOL},
        "feature_null_masks_exact": all(item["null_masks_exact"] for item in comparisons.values()),
        "all_market_values_float32_exact": all(item["null_masks_exact"] and item["nonexact_count"] == 0
                                                for item in comparisons.values()),
        "matrix_null_masks_exact": masks_exact,
        "matrix_nonexact_nonnull_cells": int(np.count_nonzero((x != z) & finite)),
        "matrix_max_absolute_error": float(delta.max()) if delta.size else 0.0,
        "valid_price_rows": int(valid_price.sum()), "matrix_dtype": "float32",
        "null_policy": "Unfilled NaN; same matrix conversion and invalid-price -1e6 sentinel as production",
        "invalid_price_sentinel": -1e6, "labels_read": False,
        "validation_labels_loaded": False, "scores_computed": False,
        "future_rows_used_for_feature_build": False,
        "input_columns": added.INPUT_COLUMNS,
        "io_note": "The CSV scanner may physically pass future records to apply its date filter, and provenance hashing reads full file bytes. Only the seven projected input columns and dates <=20180531 are materialized and supplied to build_frame; labels and future rows are not used in feature calculation. Frozen comparison features are filtered to the same prefix.",
        "stored_features_sha256": manifest["features_sha256"],
        "feature_module_sha256": manifest["feature_module_sha256"],
        "prefix_helper_sha256": added.file_hash(added.ROOT / "experiments/check_feature_expansion_prefix.py"),
        "audit_source_sha256": added.file_hash(Path(__file__)),
        "scope_note": "Numerical prefix propagation only; not a historical or out-of-sample performance estimate. No frozen artifacts are modified.",
    }
    return x, z, valid_price, record


def check_prefix_features() -> dict:
    """Check the real input matrices before new models are available; no writes."""
    started = time.monotonic()
    _, _, _, record = _prefix_matrices()
    record["seconds"] = time.monotonic() - started
    return record


def check_model_prefix(year: int) -> dict:
    """Compare both real-prefix matrices through the saved return-head model."""
    if year not in (2022, 2023, 2024):
        raise ValueError("Only the predeclared annual return-head models are supported")
    started = time.monotonic()
    model_path = OUT / f"return_market_z1_99_{year}.txt"
    metadata_path = OUT / f"return_market_z1_99_{year}.json"
    if not model_path.is_file() or not metadata_path.is_file():
        raise FileNotFoundError(f"Saved return-market model and metadata required for {year}")
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    model_sha = added.file_hash(model_path)
    if metadata["model_sha256"] != model_sha:
        raise ValueError("Return-market model differs from its saved metadata")
    features = features_for_variant("market")
    model = lgb.Booster(model_str=model_path.read_text(encoding="utf-8"))
    if model.feature_name() != features or metadata["features"] != features:
        raise ValueError("Return-market model feature order differs from the fixed 71 columns")
    x, z, valid_price, record = _prefix_matrices()
    fresh = model.predict(x, num_threads=THREADS)
    frozen = model.predict(z, num_threads=THREADS)
    fresh32, frozen32 = fresh.astype(np.float32), frozen.astype(np.float32)
    fresh32[~valid_price] = -1e6
    frozen32[~valid_price] = -1e6
    raw_delta = np.abs(fresh - frozen)
    stored_delta = np.abs(fresh32.astype(np.float64) - frozen32.astype(np.float64))
    raw_nonexact = int(np.count_nonzero(fresh != frozen))
    stored_nonexact = int(np.count_nonzero(fresh32 != frozen32))
    all_finite = bool(np.isfinite(fresh).all() and np.isfinite(frozen).all()
                      and np.isfinite(fresh32).all() and np.isfinite(frozen32).all())
    record.update({
        "year": year, "model_path": str(model_path.relative_to(added.ROOT)),
        "model_sha256": model_sha, "model_metadata_sha256": added.file_hash(metadata_path),
        "model_output_float64_nonexact_count": raw_nonexact,
        "model_output_float64_max_absolute_error": float(raw_delta.max()),
        "model_output_valid_price_nonexact_count": int(np.count_nonzero(fresh[valid_price] != frozen[valid_price])),
        "production_float32_with_sentinel_nonexact_count": stored_nonexact,
        "production_float32_with_sentinel_max_absolute_error": float(stored_delta.max()),
        "all_predictions_finite": all_finite, "threads": THREADS,
        "seconds": time.monotonic() - started,
    })
    if record["status"] == "passed" and (raw_nonexact or stored_nonexact or not all_finite):
        record["status"] = "prediction_difference_detected"
    return record
