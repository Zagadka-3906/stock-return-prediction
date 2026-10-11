"""Fixed OOF rank-residual correction; no historical data loading or scoring.

The caller owns OOF provenance, feature construction and mature-label date
boundaries. fit() uses every supplied price-valid finite-label row, including
limit-up rows, without a minimum daily sample count. Prediction uses only
current keys, price validity, raw R4 scores, supplied features and pooled raw.

Calibration is Float64 unregularized date-balanced WLS; tree features are
Float32 and LightGBM internally stores labels/weights at its native precision.
No init_score, weight tuning, early stopping or fallback model is used.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import tempfile

sys.dont_write_bytecode = True
if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import lightgbm as lgb
import numpy as np
import polars as pl
from scipy.stats import rankdata

from experiments.cached_recheck import BASE_CONFIG, make_prediction
from src.scoring import Panel

KEYS = ["trade_date", "ts_code"]
BASE_FEATURE_NAME = "r4_percentile"
ROUNDS = 80
PARAMS = {
    "objective": "regression", "metric": "l2", "boosting_type": "gbdt",
    "num_leaves": 7, "learning_rate": .05, "min_data_in_leaf": 1000,
    "lambda_l2": 10., "max_bin": 127, "feature_fraction": 1.,
    "bagging_fraction": 1., "bagging_freq": 0, "boost_from_average": True,
    "deterministic": True, "force_col_wise": True, "num_threads": 8,
    "seed": 2026, "data_random_seed": 2026, "feature_fraction_seed": 2026,
    "bagging_seed": 2026, "verbosity": -1,
}
EXPECTED_POST = {"alpha": .9, "bonus": .3, "restore_lower": True, "top_current_weight": 1.}


def _layout(frame: pl.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    if not isinstance(frame, pl.DataFrame) or frame.is_empty():
        raise ValueError("A nonempty Polars panel is required")
    if not set(KEYS + ["price_valid"]) <= set(frame.columns):
        raise ValueError("Missing keys or price_valid")
    keys = frame.select(KEYS)
    if any(keys.null_count().row(0)) or not keys.equals(keys.sort(KEYS)):
        raise ValueError("Keys must be non-null and already sorted by trade_date, ts_code")
    if not frame.schema["trade_date"].is_integer():
        raise ValueError("trade_date must contain integer calendar dates")
    n_days = frame["trade_date"].n_unique()
    if len(frame) % n_days:
        raise ValueError("A rectangular date/stock panel is required")
    n_codes = len(frame) // n_days
    codes = frame["ts_code"].to_numpy().reshape(n_days, n_codes)
    dates = frame["trade_date"].to_numpy().reshape(n_days, n_codes)
    if (np.unique(codes[0]).size != n_codes or not np.all(codes == codes[:1])
            or not np.all(dates == dates[:, :1])):
        raise ValueError("Every day must contain the same unique ordered stock codes")
    if frame.schema["price_valid"] != pl.Boolean or frame["price_valid"].null_count():
        raise ValueError("price_valid must be non-null Boolean")
    return dates, frame["price_valid"].to_numpy().reshape(n_days, n_codes)


def base_percentile(frame: pl.DataFrame) -> np.ndarray:
    """Daily average-tie R4 percentile in the complete price-valid pool; else NaN."""
    _, valid = _layout(frame)
    if "pred_raw" not in frame.columns:
        raise ValueError("pred_raw is required")
    raw = frame["pred_raw"].cast(pl.Float64).to_numpy().reshape(valid.shape)
    if not np.isfinite(raw[valid]).all():
        raise ValueError("All price-valid R4 raw predictions must be finite; never shrink the pool")
    result = np.full(valid.shape, np.nan, dtype=np.float64)
    for day, mask in enumerate(valid):
        n = int(mask.sum())
        if n:
            result[day, mask] = rankdata(raw[day, mask], method="average") / n
    return result.reshape(-1)


def target_percentile(frame: pl.DataFrame) -> np.ndarray:
    """Average-tie return percentile only within price-valid finite-label rows."""
    _, price_valid = _layout(frame)
    if "y_ret_1d" not in frame.columns or frame.schema["y_ret_1d"] != pl.Float64:
        raise ValueError("Training requires original Float64 y_ret_1d")
    labels = frame["y_ret_1d"].to_numpy().reshape(price_valid.shape)
    result = np.full(price_valid.shape, np.nan, dtype=np.float64)
    for day in range(len(price_valid)):
        mask = price_valid[day] & np.isfinite(labels[day])
        if mask.any():
            result[day, mask] = rankdata(labels[day, mask], method="average") / int(mask.sum())
    return result.reshape(-1)


def date_weights(frame: pl.DataFrame, mask: np.ndarray, normalize: bool = False) -> np.ndarray:
    """Full-row weights: N/(D*n_day) for tree fitting; 1/(D*n_day) for WLS.

    Non-selected rows have weight zero. D counts only dates with selected rows;
    empty-label dates do not dilute the other dates' weights. Tree weights have
    theoretical mean one over the selected N rows, preserving fixed L2 scale.
    """
    dates, _ = _layout(frame)
    selected = np.asarray(mask)
    if selected.dtype != np.bool_ or selected.shape != (len(frame),):
        raise ValueError("mask must be an aligned one-dimensional Boolean array")
    selected = selected.reshape(dates.shape)
    counts = selected.sum(axis=1)
    n, d = int(counts.sum()), int(np.count_nonzero(counts))
    if n == 0:
        raise ValueError("No observable training labels")
    weights = np.zeros(dates.shape, dtype=np.float64)
    scale = 1. if normalize else float(n)
    for day, count in enumerate(counts):
        if count:
            weights[day, selected[day]] = scale / (d * int(count))
    return weights.reshape(-1)


def make_matrix(features: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Append b as column64, with the exact Float32 C-order matrix contract."""
    values, percentiles = np.asarray(features), np.asarray(b)
    if values.ndim != 2 or values.shape[1] != 63 or percentiles.shape != (len(values),):
        raise ValueError("Expected X with 63 original features and an aligned one-dimensional b")
    return np.ascontiguousarray(np.column_stack([
        np.asarray(values, dtype=np.float32), percentiles.astype(np.float32)]), dtype=np.float32)


def calibrated_base(frame: pl.DataFrame, b: np.ndarray, calibration: dict) -> np.ndarray:
    """Compute actual a+beta*b and reject any floating-point change to its ranks."""
    _, valid = _layout(frame)
    base = np.asarray(b, dtype=np.float64)
    if base.shape != (len(frame),) or not np.isfinite(base.reshape(valid.shape)[valid]).all():
        raise ValueError("b must be finite on every price-valid row")
    intercept, slope = float(calibration["intercept"]), float(calibration["slope"])
    if not np.isfinite(intercept) or not np.isfinite(slope) or slope <= 0:
        raise ValueError("Calibration requires a finite intercept and strictly positive finite slope")
    base = base.reshape(valid.shape)
    out = np.full(valid.shape, -10., dtype=np.float64)
    for day, mask in enumerate(valid):
        if mask.any():
            values = intercept + slope * base[day, mask]
            if (not np.isfinite(values).all() or not np.array_equal(
                    rankdata(values, method="average"), rankdata(base[day, mask], method="average"))):
                raise ValueError("Calibration changed daily ranks through floating-point collapse/overflow")
            out[day, mask] = values
    return out.reshape(-1)


def fit(frame: pl.DataFrame, features: np.ndarray, feature_names: list[str]) -> tuple[lgb.Booster, dict]:
    """Fit date-balanced WLS then the fixed residual tree on the caller's OOF rows.

    The core does not establish OOF validity or purge labels: the driver must
    supply only approved past dates with mature labels. No validation labels,
    early-stopping set, or ranking score is accepted by this function.
    """
    if len(feature_names) != 63 or len(set(feature_names)) != 63 or BASE_FEATURE_NAME in feature_names:
        raise ValueError("Exactly 63 distinct original feature names are required")
    values = np.asarray(features)
    if values.ndim != 2 or values.shape != (len(frame), 63):
        raise ValueError("Feature rows must align exactly with the full panel")
    b, target = base_percentile(frame), target_percentile(frame)
    mask = np.isfinite(target)
    weights = date_weights(frame, mask)
    normalized = date_weights(frame, mask, normalize=True)[mask]
    normalized = normalized / normalized.sum()
    x, y = b[mask], target[mask]
    if np.ptp(x) == 0:
        raise ValueError("Degenerate base percentile; WLS slope is unidentified")
    mean_x, mean_y = np.dot(normalized, x), np.dot(normalized, y)
    centered_x, centered_y = x - mean_x, y - mean_y
    variance = np.dot(normalized, centered_x * centered_x)
    slope = float(np.dot(normalized, centered_x * centered_y) / variance)
    intercept = float(mean_y - slope * mean_x)
    dates = frame["trade_date"].to_numpy()[mask]
    date_values = np.unique(dates)
    calibration = {"intercept": intercept, "slope": slope,
        "training_rows": int(mask.sum()), "training_dates": int(len(date_values)),
        "training_date_values": [int(value) for value in date_values],
        "weight_sum": float(weights.sum()), "weight_mean": float(weights[mask].mean()),
        "calibration_weight_sum": float(normalized.sum()),
        "feature_names": list(feature_names), "model_feature_names": list(feature_names) + [BASE_FEATURE_NAME],
        "params": dict(PARAMS), "rounds": ROUNDS,
        "target": "rank(y)/n among current price_valid AND finite original Float64 y; includes limit-up",
        "base": "rank(r4 raw)/n among all current price_valid; finite raw required; independent of labels",
        "weights": "Tree N/(D*n_day), WLS sum1; D counts dates with observable target; no minimum daily rows",
        "precision": "Float64 ranks/WLS/residual construction; Float32 feature matrix; LightGBM-native internal labels/weights",
        "lightgbm_version": lgb.__version__}
    baseline = calibrated_base(frame, b, calibration)
    residual = target[mask] - baseline[mask]
    calibration["weighted_mse"] = float(np.dot(normalized, residual * residual))
    matrix = make_matrix(values[mask], b[mask])
    dataset = lgb.Dataset(matrix, label=residual, weight=weights[mask],
                          feature_name=calibration["model_feature_names"], free_raw_data=True)
    booster = lgb.train(dict(PARAMS), dataset, num_boost_round=ROUNDS)
    return booster, calibration


def predict_raw(frame: pl.DataFrame, features: np.ndarray, booster: lgb.Booster | None,
                calibration: dict) -> np.ndarray:
    """m(b)+tree(X,b), invalid=-10. booster=None is actual zero correction."""
    b = base_percentile(frame)
    raw = calibrated_base(frame, b, calibration)
    if booster is None:
        return raw
    values = np.asarray(features)
    if values.shape != (len(frame), 63):
        raise ValueError("Prediction features must align with every panel row")
    if booster.num_feature() != 64 or booster.feature_name() != calibration["model_feature_names"]:
        raise ValueError("Residual model feature identity/order differs from calibration")
    valid = np.isfinite(b)
    if valid.any():
        residual = np.asarray(booster.predict(make_matrix(values[valid], b[valid]), num_threads=8), dtype=np.float64)
        if residual.shape != (int(valid.sum()),) or not np.isfinite(residual).all():
            raise ValueError("Residual prediction must be finite for every price-valid row")
        raw[valid] += residual
        if not np.isfinite(raw[valid]).all():
            raise ValueError("Corrected signal overflowed")
    return raw


def prediction(frame: pl.DataFrame, features: np.ndarray, booster: lgb.Booster | None,
               calibration: dict) -> np.ndarray:
    """Full unchanged R4 post; user labels/future availability are never read."""
    raw = predict_raw(frame, features, booster, calibration)
    if BASE_CONFIG != EXPECTED_POST:
        raise RuntimeError("Frozen postprocessing configuration changed")
    if not {"flag_limit_up", "aux_raw"} <= set(frame.columns):
        raise ValueError("Full prediction requires flag_limit_up and aux_raw")
    flags = frame["flag_limit_up"]
    if flags.null_count() or not flags.is_in([0, 1]).all():
        raise ValueError("flag_limit_up must contain only non-null 0/1")
    clean = frame.select(KEYS + ["price_valid", "flag_limit_up"]).with_columns(
        pl.Series("pred_raw", raw), pl.lit(None, dtype=pl.Float64).alias("y_ret_1d"))
    return make_prediction(Panel.from_frame(clean), frame["aux_raw"].cast(pl.Float64).to_numpy(), "top_only", .25)


def synthetic_tests() -> dict:
    """Synthetic fixed-capacity fit only; never read or score historical data."""
    checks = {}

    def equal(name, actual, expected):
        np.testing.assert_array_equal(actual, expected, err_msg=name)
        checks[name] = True

    def reject(name, operation):
        try:
            operation()
        except ValueError:
            checks[name] = True
        else:
            raise AssertionError(f"Expected fail-closed rejection: {name}")

    tiny = pl.DataFrame({"trade_date": [1] * 5 + [2] * 5, "ts_code": list("abcde") * 2,
        "price_valid": [True, True, True, True, False] * 2,
        "pred_raw": [1., 1., 2., 3., np.inf, 4., 3., 2., 1., np.nan],
        "y_ret_1d": [2., 2., 1., np.nan, 999., 2., np.nan, 1., np.nan, 999.],
        "flag_limit_up": [0, 1, 0, 0, 0] * 2, "aux_raw": [1., 2., 3., 4., 5.] * 2})
    b, u = base_percentile(tiny), target_percentile(tiny)
    equal("base_ties_label_independent_full_valid_pool", b,
          np.array([.375, .375, .75, 1., np.nan, 1., .75, .5, .25, np.nan]))
    equal("target_ties_finite_labels_including_limitup", u,
          np.array([2.5/3, 2.5/3, 1/3, np.nan, np.nan, 1., np.nan, .5, np.nan, np.nan]))
    mask = np.isfinite(u)
    w, normalized = date_weights(tiny, mask), date_weights(tiny, mask, True)
    np.testing.assert_allclose([w[:5].sum(), w[5:].sum(), w.sum(), w[mask].mean()], [2.5, 2.5, 5., 1.], rtol=0, atol=1e-14)
    np.testing.assert_allclose([normalized[:5].sum(), normalized[5:].sum(), normalized.sum()], [.5, .5, 1.], rtol=0, atol=1e-14)
    equal("nontraining_weight_zero", w[~mask], np.zeros((~mask).sum()))
    checks["tree_mean1_calibration_sum1_and_equal_date_mass"] = True
    names = [f"f{i:02}" for i in range(63)]
    matrix = make_matrix(np.zeros((10, 63), dtype=np.float64), b)
    assert matrix.shape == (10, 64) and matrix.dtype == np.float32 and matrix.flags.c_contiguous
    equal("matrix_last_column_and_float32_C_order", matrix[:, -1], b.astype(np.float32))
    reject("calibration_tiny_slope_collapse", lambda: calibrated_base(tiny, b, {"intercept": 1., "slope": 1e-300}))
    reject("calibration_nonpositive_slope", lambda: calibrated_base(tiny, b, {"intercept": 0., "slope": 0.}))
    reject("valid_raw_nonfinite_not_silently_removed", lambda: base_percentile(tiny.with_columns(
        pl.when(pl.col("ts_code") == "a").then(float("nan")).otherwise(pl.col("pred_raw")).alias("pred_raw"))))
    reject("float32_training_labels_rejected", lambda: target_percentile(tiny.with_columns(pl.col("y_ret_1d").cast(pl.Float32))))
    reject("duplicate_keys_rejected", lambda: base_percentile(pl.concat([tiny, tiny.head(1)])))
    reject("no_observed_targets_rejected", lambda: date_weights(tiny, np.zeros(10, dtype=bool)))

    n, days = 1200, 3
    stock, day = np.tile(np.arange(n), days), np.repeat(np.arange(days), n)
    rng = np.random.default_rng(2026)
    features = rng.normal(size=(n * days, 63)).astype(np.float32)
    features[:, 0] = ((stock // 300) % 2) * 2 - 1
    raw = ((stock * 17 + day * 31) % n).astype(float)
    labels = raw / n + .3 * features[:, 0]
    labels[(day == 0) & (stock % 4 == 0)] = np.nan
    labels[(day == 1) & (stock % 10 == 0)] = np.nan
    valid = ~((day == 1) & (stock < 5))
    frame = pl.DataFrame({"trade_date": 20200102 + day, "ts_code": [f"S{i:04}" for i in stock],
        "price_valid": valid, "pred_raw": raw, "y_ret_1d": labels,
        "flag_limit_up": (stock % 17 == 0).astype(int), "aux_raw": np.sin(stock / 17),
        "future_available": day < 2})
    booster, calibration = fit(frame, features, names)
    assert calibration["slope"] > 0 and calibration["training_dates"] == days
    assert calibration["params"] == PARAMS and calibration["rounds"] == 80
    assert booster.num_feature() == 64 and booster.current_iteration() == 80
    checks["fixed_7leaf_80round_model_fitted"] = True
    base, target = base_percentile(frame), target_percentile(frame)
    observed = np.isfinite(target)
    q = date_weights(frame, observed, True)[observed]
    design = np.column_stack([np.ones(observed.sum()), base[observed]])
    independently = np.linalg.solve(design.T @ (q[:, None] * design), design.T @ (q * target[observed]))
    np.testing.assert_allclose([calibration["intercept"], calibration["slope"]], independently, rtol=0, atol=1e-12)
    checks["WLS_equals_independent_normal_equations"] = True
    zero_raw = predict_raw(frame, features, None, calibration)
    equal("zero_model_computes_actual_calibration", zero_raw[valid], calibration["intercept"] + calibration["slope"] * base[valid])
    original = make_prediction(Panel.from_frame(frame), frame["aux_raw"].to_numpy(), "top_only", .25)
    equal("actual_zero_calibration_exact_original_post", prediction(frame, features, None, calibration), original)
    corrected = predict_raw(frame, features, booster, calibration)
    pred = prediction(frame, features, booster, calibration)
    assert np.isfinite(corrected).all() and (corrected[~valid] == -10).all() and (pred[~valid] < -1).all()
    poisoned = frame.with_columns(pl.lit(float("nan")).alias("y_ret_1d"), (~pl.col("future_available")).alias("future_available"))
    equal("raw_label_and_future_availability_poison_ignored", predict_raw(poisoned, features, booster, calibration), corrected)
    equal("post_label_and_future_availability_poison_ignored", prediction(poisoned, features, booster, calibration), pred)
    equal("label_columns_unnecessary_for_inference", prediction(frame.drop("y_ret_1d", "future_available"), features, booster, calibration), pred)
    cutoff = 2 * n
    equal("fixed_model_prefix_raw", predict_raw(frame.head(cutoff), features[:cutoff], booster, calibration), corrected[:cutoff])
    equal("fixed_model_prefix_post", prediction(frame.head(cutoff), features[:cutoff], booster, calibration), pred[:cutoff])
    future_features = features.copy()
    future_features[cutoff:] *= -123
    future = frame.with_columns(pl.when(pl.col("trade_date") > 20200103)
        .then(-pl.col("pred_raw")).otherwise(pl.col("pred_raw")).alias("pred_raw"))
    equal("future_raw_features_do_not_change_past", prediction(future, future_features, booster, calibration)[:cutoff], pred[:cutoff])
    with tempfile.TemporaryDirectory(prefix="r9-synthetic-model-") as temporary:
        path = Path(temporary) / "residual.txt"
        booster.save_model(str(path))
        reloaded = lgb.Booster(model_str=path.read_text(encoding="utf-8"))
        saved_calibration = json.loads(json.dumps(calibration, allow_nan=False))
        equal("model_save_reload_raw_exact", predict_raw(frame, features, reloaded, saved_calibration), corrected)
        equal("model_save_reload_post_exact", prediction(frame, features, reloaded, saved_calibration), pred)
    # No alternative model is fitted when WLS cannot identify a positive slope.
    reject("negative_calibration_fails_before_tree_fit", lambda: fit(frame.with_columns(
        (-pl.col("pred_raw")).alias("y_ret_1d")), features, names))
    reject("degenerate_base_fails_before_tree_fit", lambda: fit(frame.with_columns(
        pl.lit(1.).alias("pred_raw")), features, names))
    return {"status": "passed", "checks": checks, "check_count": len(checks),
            "historical_data_read": False, "historical_training_or_scoring": False,
            "synthetic_training_rows": calibration["training_rows"], "params": dict(PARAMS),
            "rounds": ROUNDS, "lightgbm_version": lgb.__version__}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--test", action="store_true", required=True)
    parser.parse_args()
    print(json.dumps(synthetic_tests(), ensure_ascii=False, indent=2, allow_nan=False))
