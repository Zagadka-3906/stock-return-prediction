"""Read-only diagnosis of prefix-sensitive return-head predictions.

Uses only the already trained 2022/2023 models and the 2018 real prefix.
No validation labels, performance scores, retraining, or threshold tuning.
The sole possible write is a new return_market_eval/prefix_failure.json;
an existing file is never overwritten.
"""
from __future__ import annotations

import copy
import json
import time

import lightgbm as lgb
import numpy as np
import polars as pl

from experiments.check_return_market_prefix import (
    CUTOFF, KEYS, OUT, THREADS, _prefix_matrices, added,
)


def _leaf_path(node: dict, leaf: int, path: list | None = None) -> list | None:
    path = [] if path is None else path
    if "leaf_index" in node:
        return path + [{"leaf_index": node["leaf_index"], "leaf_value": node["leaf_value"]}] if node["leaf_index"] == leaf else None
    for branch in ("left", "right"):
        item = {key: node[key] for key in ("split_index", "split_feature", "threshold",
                                         "decision_type", "default_left", "missing_type")}
        item["branch"] = branch
        found = _leaf_path(node[f"{branch}_child"], leaf, path + [item])
        if found is not None:
            return found
    return None


def _stock_window(code: str, date: int, keys: pl.DataFrame, frozen: np.ndarray,
                  features: list[str]) -> dict:
    raw = pl.scan_csv(
        added.TRAIN_FILE,
        schema_overrides={"ts_code": pl.String, "trade_date": pl.Int32, "close": pl.Float64},
        null_values=["NaN", "nan", ""], low_memory=True,
    ).select(*KEYS, "close").filter(
        (pl.col("ts_code") == code) & (pl.col("trade_date") <= CUTOFF)
    ).collect().sort(KEYS)
    dates = raw.get_column("trade_date").to_numpy()
    close = raw.get_column("close").to_numpy().copy()
    close[(close <= 0) | ~np.isfinite(close)] = np.nan
    returns = np.r_[np.nan, close[1:] / close[:-1] - 1]
    current = int(np.flatnonzero(dates == date)[0])
    if current < 61:
        raise ValueError("The root-cause window requires 61 earlier closes")
    values = returns[current - 60:current]
    historical_close = close[current - 61:current]
    row_indices = np.flatnonzero(keys.get_column("ts_code").to_numpy() == code)
    market = frozen[row_indices[current - 60:current], features.index("MARKET_RET1")].astype(np.float64)
    all_valid = bool(np.isfinite(values).all())
    return {
        "window_start": int(dates[current - 60]), "window_end": int(dates[current - 1]),
        "return_count": len(values), "valid_return_count": int(np.isfinite(values).sum()),
        "unique_return_values": np.unique(values).tolist(),
        "all_returns_exactly_zero": bool(all_valid and np.all(values == 0)),
        "returns_exactly_constant": bool(all_valid and np.min(values) == np.max(values)),
        "stock_return_sample_variance": float(np.var(values, ddof=1)),
        "preceding_61_closes_unique": np.unique(historical_close).tolist(),
        "market_sample_variance_from_stored_float32": float(np.var(market, ddof=1)),
        "independent_numpy_sample_covariance": float(np.cov(values, market, ddof=1)[0, 1]),
        "covariance_note": "Market series is the stored Float32 market feature. For an exactly constant finite stock-return vector, covariance is mathematically zero for any finite market vector, independently of its rounding.",
    }


def diagnose() -> dict:
    started = time.monotonic()
    x, z, valid_price, base_record = _prefix_matrices()
    features = base_record["feature_order"]
    keys = pl.scan_parquet(added.ROOT / "data/features.parquet").filter(
        pl.col("is_train") & (pl.col("trade_date") <= CUTOFF)
    ).select(KEYS).collect().sort(KEYS)
    years = {}
    details = []
    for year in (2022, 2023):
        model_path = OUT / f"return_market_z1_99_{year}.txt"
        metadata_path = OUT / f"return_market_z1_99_{year}.json"
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        if added.file_hash(model_path) != metadata["model_sha256"]:
            raise ValueError(f"Saved model hash mismatch for {year}")
        model = lgb.Booster(model_str=model_path.read_text(encoding="utf-8"))
        if model.feature_name() != features or metadata["features"] != features:
            raise ValueError("Model feature order mismatch")
        a, b = model.predict(x, num_threads=THREADS), model.predict(z, num_threads=THREADS)
        a32, b32 = a.astype(np.float32), b.astype(np.float32)
        a32[~valid_price] = b32[~valid_price] = -1e6
        changed = np.flatnonzero(a != b)
        record = copy.deepcopy(base_record)
        record.update({
            "year": year, "model_path": str(model_path.relative_to(added.ROOT)),
            "model_sha256": metadata["model_sha256"],
            "model_metadata_sha256": added.file_hash(metadata_path),
            "model_output_float64_nonexact_count": int(len(changed)),
            "model_output_float64_max_absolute_error": float(np.max(np.abs(a - b))),
            "model_output_valid_price_nonexact_count": int(np.count_nonzero(a[valid_price] != b[valid_price])),
            "production_float32_with_sentinel_nonexact_count": int(np.count_nonzero(a32 != b32)),
            "production_float32_with_sentinel_max_absolute_error": float(np.max(np.abs(a32.astype(float) - b32.astype(float)))),
            "all_predictions_finite": bool(np.isfinite(a).all() and np.isfinite(b).all()
                                            and np.isfinite(a32).all() and np.isfinite(b32).all()),
            "threads": THREADS,
        })
        if len(changed) or np.any(a32 != b32) or not record["all_predictions_finite"]:
            record["status"] = "prediction_difference_detected"
        years[str(year)] = record
        print(f"{year}: raw differences={len(changed)}, max={record['model_output_float64_max_absolute_error']}", flush=True)
        # Detailed original-price and tree inspection is limited to the two
        # already identified 2022 rows; 2023 adds only the requested propagation check.
        if year != 2022 or not len(changed):
            continue
        fresh_leaves = model.predict(x[changed], pred_leaf=True, num_threads=THREADS)
        frozen_leaves = model.predict(z[changed], pred_leaf=True, num_threads=THREADS)
        dump = model.dump_model()
        for k, index in enumerate(changed):
            key = keys.row(int(index), named=True)
            item = {
                **key, "row_index": int(index), "valid_price": bool(valid_price[index]),
                "fresh_beta_float32": float(x[index, features.index("BETA60")]),
                "frozen_beta_float32": float(z[index, features.index("BETA60")]),
                "fresh_prediction_float64": float(a[index]), "frozen_prediction_float64": float(b[index]),
                "prediction_difference_float64": float(a[index] - b[index]),
                "stock_history": _stock_window(key["ts_code"], key["trade_date"], keys, z, features),
                "tree_divergences": [],
            }
            for tree_index in np.flatnonzero(fresh_leaves[k] != frozen_leaves[k]):
                tree = dump["tree_info"][int(tree_index)]["tree_structure"]
                pa = _leaf_path(tree, int(fresh_leaves[k, tree_index]))
                pb = _leaf_path(tree, int(frozen_leaves[k, tree_index]))
                if pa is None or pb is None:
                    raise AssertionError("A reported prediction leaf was not found in the model dump")
                na, nb = next((na, nb) for na, nb in zip(pa[:-1], pb[:-1]) if na["branch"] != nb["branch"])
                if na["split_index"] != nb["split_index"]:
                    raise AssertionError("Expected the first path divergence at a shared split")
                divergence = {key: value for key, value in na.items() if key != "branch"}
                feature_index = divergence["split_feature"]
                divergence.update({
                    "tree_index_zero_based": int(tree_index), "feature_name": features[feature_index],
                    "fresh_feature_value": float(x[index, feature_index]),
                    "frozen_feature_value": float(z[index, feature_index]),
                    "fresh_branch": na["branch"], "frozen_branch": nb["branch"],
                    "fresh_leaf": pa[-1], "frozen_leaf": pb[-1],
                    "leaf_value_difference": pa[-1]["leaf_value"] - pb[-1]["leaf_value"],
                })
                item["tree_divergences"].append(divergence)
            details.append(item)
    return {
        "status": "prefix_prediction_failure_confirmed",
        "labels_read": False, "validation_labels_loaded": False, "scores_computed": False,
        "training_performed": False, "frozen_artifacts_modified": False,
        "models_checked": [2022, 2023], "prefix_records": years, "root_cause_rows_2022": details,
        "root_cause": "Both 2022 rows have exactly constant zero stock returns throughout the complete prior-60 window. Their true covariance and beta are zero when market variance is valid. Floating-point rolling covariance leaves negative residual beta in one computation but exact zero in the other. A tree threshold near negative machine zero separates these values into different leaves.",
        "proposed_mathematical_fix_for_a_separate_experiment": "For a complete finite prior-60 stock-return window, detect exact constancy with max(return)==min(return), not a learned or arbitrary near-zero cutoff. Set covariance exactly to zero for such a window; return beta zero only when the market variance is finite and passes the existing denominator validity condition. Preserve null for incomplete windows or invalid market variance. Alternatively use a numerically stable directly centered covariance implementation with the same exact-constant invariant. Do not amend or retrain this frozen candidate.",
        "interpretation": "Feature-level floating-point tolerance did not guarantee identical tree predictions. This diagnostic does not assess predictive performance and does not justify relaxing the protocol.",
        "diagnostic_source_sha256": added.file_hash(__import__("pathlib").Path(__file__)),
        "seconds": time.monotonic() - started,
    }


def main() -> None:
    target = OUT / "prefix_failure.json"
    if target.exists():
        raise FileExistsError("Refusing to overwrite existing prefix_failure.json")
    record = diagnose()
    # Exclusive creation prevents an existing audit from being overwritten.
    with target.open("x", encoding="utf-8") as stream:
        json.dump(record, stream, ensure_ascii=False, indent=2)
    print(f"Wrote {target}", flush=True)


if __name__ == "__main__":
    main()
