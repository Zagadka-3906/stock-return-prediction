"""Reproduce the real-data feature-prefix and model-propagation audits.

Run ``python -m experiments.check_feature_expansion_prefix features`` after
rebuilding the feature store and before locking a development audit. Run the
``models`` command only after all three annual market-group models exist.
Each command rewrites only its own named audit JSON; it never changes feature,
training, prediction, or report artifacts. No labels are parsed or scored.
"""
from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path

# Limit the read-only diagnostic's resource use alongside model training.
os.environ.setdefault("POLARS_MAX_THREADS", "4")

import lightgbm as lgb
import numpy as np
import polars as pl

from experiments import feature_expansion_features as added


CUTOFF = 20180531
KEYS = ["ts_code", "trade_date"]
THREADS = 4
RTOL, ATOL = 3e-5, 3e-7


def _verified_manifest() -> dict:
    manifest = json.loads((added.OUT / "feature_manifest.json").read_text(encoding="utf-8"))
    tests = json.loads((added.OUT / "feature_tests.json").read_text(encoding="utf-8"))
    source_sha = added.file_hash(Path(added.__file__))
    if manifest["feature_module_sha256"] != source_sha or tests["feature_module_sha256"] != source_sha:
        raise ValueError("Feature source, manifest, and tests are not from the same build")
    if tests.get("status") != "passed" or not tests.get("passed"):
        raise ValueError("The frozen builder tests must pass before prefix auditing")
    if manifest["features_sha256"] != added.file_hash(added.ADDED_FEATURE_FILE):
        raise ValueError("Stored feature parquet hash differs from its manifest")
    if manifest["source_sha256"] != added.file_hash(added.TRAIN_FILE):
        raise ValueError("Original training CSV hash differs from its manifest")
    if manifest["features"] != added.FEATURE_NAMES or manifest["groups"] != added.GROUPS:
        raise ValueError("Feature declarations differ from the tested builder")
    if manifest.get("labels_used") is not False or manifest.get("test_file_read") is not False:
        raise ValueError("Expected the label-free, training-only feature store")
    return manifest


def _prefix_frames() -> tuple[pl.DataFrame, pl.DataFrame, pl.DataFrame]:
    source = pl.scan_csv(
        added.TRAIN_FILE,
        schema_overrides={"ts_code": pl.String, "trade_date": pl.Int32,
                          **{name: pl.Float64 for name in added.INPUT_COLUMNS[2:]}},
        null_values=["NaN", "nan", ""], low_memory=True,
    ).select(added.INPUT_COLUMNS).filter(pl.col("trade_date") <= CUTOFF).collect()
    if (source.height != 460350 or source.get_column("ts_code").n_unique() != 4650
            or source.get_column("trade_date").n_unique() != 99):
        raise ValueError("Expected the fixed complete-cross-section 2018-05-31 prefix")
    fresh = added.build_frame(source)
    frozen = pl.scan_parquet(added.ADDED_FEATURE_FILE).filter(
        pl.col("trade_date") <= CUTOFF).collect().sort(KEYS)
    if not fresh.select(KEYS).equals(frozen.select(KEYS)):
        raise ValueError("Fresh and frozen prefix keys or ordering differ")
    return source, fresh, frozen


def audit_features() -> dict:
    started = time.monotonic()
    manifest = _verified_manifest()
    source, fresh, frozen = _prefix_frames()
    results = {}
    for name in added.FEATURE_NAMES:
        a, b = fresh.get_column(name).to_numpy(), frozen.get_column(name).to_numpy()
        valid = np.isfinite(a) & np.isfinite(b)
        delta = np.abs(a[valid].astype(np.float64) - b[valid].astype(np.float64))
        results[name] = {
            "null_masks_exact": bool(np.array_equal(np.isnan(a), np.isnan(b))),
            "nonnull_compared": int(valid.sum()),
            "nonexact_count": int(np.count_nonzero(a[valid] != b[valid])),
            "max_absolute_difference": float(delta.max()) if len(delta) else 0.0,
            "isclose_all": bool(np.allclose(a, b, rtol=RTOL, atol=ATOL, equal_nan=True)),
        }
    return {
        "status": "passed" if all(item["null_masks_exact"] and item["isclose_all"]
                                  for item in results.values()) else "failed",
        "cutoff_inclusive": CUTOFF, "rows": source.height,
        "securities": source.get_column("ts_code").n_unique(),
        "dates": source.get_column("trade_date").n_unique(),
        "input_columns": added.INPUT_COLUMNS,
        "comparison": "Full frozen training store prefix vs fresh original-CSV complete-cross-section prefix",
        "all_values_float32_exact": all(item["null_masks_exact"] and item["nonexact_count"] == 0
                                        for item in results.values()),
        "tolerance": {"relative": RTOL, "absolute": ATOL}, "features": results,
        "seconds": time.monotonic() - started,
        "feature_module_sha256": manifest["feature_module_sha256"],
        "stored_features_sha256": manifest["features_sha256"],
        "note": "Parquet byte hashes alone do not establish numerical differences. This audit compares decoded values and exact null masks. Tolerance agreement is not bitwise identity and does not by itself prove model predictions are unchanged. Frozen sources, cache, manifest, and builder tests were not modified.",
    }


def _verified_models(features: list[str]) -> dict[int, tuple[lgb.Booster, dict]]:
    # This reuses the training runner's full source/input fingerprint without
    # loading labeled annual panels or evaluating any prediction performance.
    from experiments.feature_expansion import fingerprint

    result = {}
    for year in (2022, 2023, 2024):
        model_path = added.OUT / f"feature_market_{year}.txt"
        cache_path = added.OUT / f"feature_market_{year}.parquet"
        metadata_path = added.OUT / f"feature_market_{year}.json"
        if not all(path.is_file() for path in (model_path, cache_path, metadata_path)):
            raise FileNotFoundError(f"Market model, cache, and metadata are required for {year}")
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        if metadata["fingerprint_sha256"] != fingerprint(year, "market")["fingerprint_sha256"]:
            raise ValueError(f"Stale training fingerprint for the {year} market model")
        if (metadata["model_sha256"] != added.file_hash(model_path)
                or metadata["cache_sha256"] != added.file_hash(cache_path)):
            raise ValueError(f"Model or prediction-cache hash changed for {year}")
        if metadata["features"] != features:
            raise ValueError(f"Metadata feature order differs for {year}")
        model = lgb.Booster(model_str=model_path.read_text(encoding="utf-8"))
        if model.feature_name() != features:
            raise ValueError(f"Serialized model feature order differs for {year}")
        result[year] = (model, metadata)
    return result


def audit_models() -> dict:
    started = time.monotonic()
    manifest = _verified_manifest()
    original = json.loads((added.ROOT / "data/feature_manifest.json").read_text(encoding="utf-8"))["features"]
    features = original + added.GROUPS["market_relative"]
    if len(original) != 63 or len(features) != 71:
        raise ValueError("Expected 63 original and 8 market-relative features")
    models = _verified_models(features)
    _, fresh, frozen = _prefix_frames()
    base = pl.scan_parquet(added.ROOT / "data/features.parquet").filter(
        pl.col("is_train") & (pl.col("trade_date") <= CUTOFF)
    ).select(*KEYS, "price_valid", *original).collect().sort(KEYS)
    selected = KEYS + added.GROUPS["market_relative"]
    left = base.join(fresh.select(selected), on=KEYS, how="left", validate="1:1", maintain_order="left")
    right = base.join(frozen.select(selected), on=KEYS, how="left", validate="1:1", maintain_order="left")
    if (base.height != 460350 or not base.select(KEYS).equals(fresh.select(KEYS))
            or not left.select(KEYS).equals(right.select(KEYS))):
        raise ValueError("Original and added feature-prefix coverage or ordering differs")
    x = np.ascontiguousarray(left.select(features).to_numpy(), dtype=np.float32)
    z = np.ascontiguousarray(right.select(features).to_numpy(), dtype=np.float32)
    valid_price = base.get_column("price_valid").to_numpy()
    results = {}
    for year, (model, metadata) in models.items():
        a = model.predict(x, num_threads=THREADS)
        b = model.predict(z, num_threads=THREADS)
        stored_a, stored_b = a.astype(np.float32), b.astype(np.float32)
        stored_a[~valid_price] = -1e6
        stored_b[~valid_price] = -1e6
        results[str(year)] = {
            "model_sha256": metadata["model_sha256"],
            "cache_sha256": metadata["cache_sha256"],
            "training_fingerprint_verified": True,
            "model_output_float64_nonexact_count": int(np.count_nonzero(a != b)),
            "model_output_float64_max_absolute_error": float(np.max(np.abs(a - b))),
            "model_output_valid_price_nonexact_count": int(np.count_nonzero(a[valid_price] != b[valid_price])),
            "production_float32_with_sentinel_nonexact_count": int(np.count_nonzero(stored_a != stored_b)),
            "production_float32_with_sentinel_max_absolute_error": float(np.max(np.abs(stored_a.astype(np.float64) - stored_b.astype(np.float64)))),
            "all_predictions_finite": bool(np.isfinite(a).all() and np.isfinite(b).all()
                                            and np.isfinite(stored_a).all() and np.isfinite(stored_b).all()),
        }
    return {
        "status": "passed" if all(item["model_output_float64_nonexact_count"] == 0
                                  and item["production_float32_with_sentinel_nonexact_count"] == 0
                                  and item["all_predictions_finite"] for item in results.values())
                  else "prediction_difference_detected",
        "cutoff_inclusive": CUTOFF, "rows": base.height, "original_features": len(original),
        "market_features": added.GROUPS["market_relative"], "total_features": len(features),
        "valid_price_rows": int(valid_price.sum()), "invalid_price_sentinel": -1e6,
        "matrix_dtype": "float32", "null_policy": "unfilled NaN, matching original to_matrix",
        "matrix_null_masks_exact": bool(np.array_equal(np.isnan(x), np.isnan(z))),
        "matrix_nonexact_nonnull_cells": int(np.count_nonzero((x != z) & np.isfinite(x) & np.isfinite(z))),
        "matrix_max_absolute_error": float(np.nanmax(np.abs(x.astype(np.float64) - z.astype(np.float64)))),
        "models": results, "labels_read": False, "scores_computed": False,
        "threads": THREADS, "seconds": time.monotonic() - started,
        "stored_features_sha256": manifest["features_sha256"],
        "feature_module_sha256": manifest["feature_module_sha256"],
        "scope_note": "Actual first-99-trading-day full-cross-section prefix; checks numerical propagation only, not out-of-sample performance. Frozen source, manifest, tests and feature artifacts were not modified.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("features", "models"))
    args = parser.parse_args()
    if args.stage == "features":
        record, filename = audit_features(), "real_prefix_audit.json"
    else:
        record, filename = audit_models(), "real_prefix_model_audit.json"
    (added.OUT / filename).write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(record, ensure_ascii=False, indent=2), flush=True)
    if record["status"] != "passed":
        raise SystemExit("Prefix audit detected a discrepancy; inspect the recorded result")


if __name__ == "__main__":
    main()
