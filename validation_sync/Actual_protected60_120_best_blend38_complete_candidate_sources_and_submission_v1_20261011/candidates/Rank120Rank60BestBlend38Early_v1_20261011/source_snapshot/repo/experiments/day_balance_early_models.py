"""Refit the frozen equal-day candidate on two additional historical folds.

Only 2020 and 2021 are supported. The 63-feature unweighted baselines are reused
from the audited early-year experiment. No validation labels enter this module.
"""
from __future__ import annotations

import argparse
import gc
import hashlib
import json
import time
from pathlib import Path

import lightgbm as lgb
import numpy as np
import polars as pl

from experiments import day_balance_models as frozen
from experiments import early_year_models as early
from experiments.seed_ensemble import params_for_seed
from run import FEATURE_FILE, MANIFEST, ROOT, feature_names, fold_cutoff, to_matrix
from src.scoring import Panel


OUT = ROOT / "experiments" / "day_balance_early_eval"
YEARS = (2020, 2021)
CANDIDATE_KEY = "equal_day"
ROUNDS, SEED, THREADS = 180, 2026, 16
POSTPROCESS = {"alpha": .9, "bonus": .3, "restore_lower": True, "top_current_weight": 1.0}
KEYS = ["ts_code", "trade_date"]
EXPECTED = {
    2020: {"training_cutoff_exclusive": 20191231, "training_first_date": 20180102,
           "training_last_date": 20191230, "training_rows": 1694259, "training_days": 486},
    2021: {"training_cutoff_exclusive": 20201231, "training_first_date": 20180102,
           "training_last_date": 20201230, "training_rows": 2594048, "training_days": 729},
}
# Reuse the actual frozen implementations, not copied or retuned alternatives.
training_weights = frozen.training_weights
file_hash = frozen.file_hash


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def _check_year(year: int) -> None:
    if year not in YEARS:
        raise ValueError("Only the fixed additional historical years 2020 and 2021 are permitted")


def read_protocol() -> dict:
    protocol = json.loads((OUT / "protocol.json").read_text(encoding="utf-8"))
    fixed = {"experiment": "fixed_equal_day_additional_historical_folds",
             "declared_before_training": True, "candidate_key": CANDIDATE_KEY,
             "years": list(YEARS), "feature_count": 63,
             "rounds": ROUNDS, "seed": SEED, "threads": THREADS,
             "postprocess": POSTPROCESS,
             "training_filter": "is_train & trade_date < fold_cutoff(year) & y_rank.not_null & price_valid"}
    if any(protocol.get(key) != value for key, value in fixed.items()):
        raise ValueError("Additional historical-check protocol differs from its fixed design")
    original = frozen.read_protocol()
    if protocol.get("weighting") != original["weighting"]:
        raise ValueError("The original equal-day weighting specification must remain unchanged")
    if protocol.get("folds") != {str(year): values for year, values in EXPECTED.items()}:
        raise ValueError("Historical training boundaries differ from the declared manifest")
    fixed_sources = {
        "previous_protocol_sha256": frozen.OUT / "protocol.json",
        "previous_model_source_sha256": Path(frozen.__file__),
        "baseline_source_sha256": Path(early.__file__),
        "baseline_results_sha256": early.OUT / "results.json",
    }
    for field, path in fixed_sources.items():
        if file_hash(path) != protocol[field]:
            raise ValueError(f"Previously frozen source or baseline evidence changed: {path.name}")
    return protocol


def _baseline_metadata(year: int) -> dict:
    """Verify the old complete baseline fingerprint; never reinterpret its cache."""
    _check_year(year)
    model_path, cache_path, meta_path = early._paths(year, "baseline")
    metadata = json.loads(meta_path.read_text(encoding="utf-8"))
    expected = early.fingerprint(year, "baseline")
    if any(metadata.get(key) != value for key, value in expected.items()):
        raise ValueError("The saved early baseline differs from its original fingerprint")
    if (metadata["model_sha256"] != file_hash(model_path)
            or metadata["cache_sha256"] != file_hash(cache_path)
            or metadata["features"] != feature_names()
            or metadata["params"] != params_for_seed(SEED, THREADS)
            or metadata["rounds"] != ROUNDS
            or metadata["reload_check_rows"] != 4096
            or metadata["reload_max_abs_error"] != 0):
        raise ValueError("The early baseline model, parameters, features or reload checks changed")
    for field in ("training_cutoff_exclusive", "training_first_date", "training_last_date", "training_rows"):
        if metadata[field] != EXPECTED[year][field]:
            raise ValueError(f"The early baseline {field} differs from the additional-fold design")
    return metadata


def _locked_sources(year: int) -> dict[str, str]:
    protocol = read_protocol()
    source_tests_path = frozen.OUT / "weight_tests.json"
    if json.loads(source_tests_path.read_text(encoding="utf-8")) != frozen.test_weights():
        raise ValueError("Frozen equal-day weight tests or implementation changed")
    prior_paths = {
        "previous_development_sha256": frozen.OUT / "development.json",
        "previous_diagnostic_2024_sha256": frozen.OUT / "diagnostic_2024.json",
        "previous_decision_sha256": frozen.OUT / "decision.json",
    }
    sources = {}
    for field, path in prior_paths.items():
        if file_hash(path) != protocol[field]:
            raise ValueError(f"Prior fixed equal-day evidence changed: {path.name}")
        record = json.loads(path.read_text(encoding="utf-8"))
        if record.get("candidate_key") != CANDIDATE_KEY:
            raise ValueError("Prior evidence belongs to another candidate")
        sources.update(record.get("artifacts_sha256", {}))
    if file_hash(Path(early.__file__)) != protocol["baseline_source_sha256"]:
        raise ValueError("The original early-year baseline implementation changed")
    baseline_results_path = early.OUT / "results.json"
    baseline_results = json.loads(baseline_results_path.read_text(encoding="utf-8"))
    sources.update(baseline_results["source_and_artifacts_sha256"])
    baseline = _baseline_metadata(year)
    sources.update(baseline["source_sha256"])
    audit_path = ROOT / "validation/prediction_audit.json"
    production = json.loads(audit_path.read_text(encoding="utf-8"))
    sources.update(production["input_sha256"])
    for relative, expected_hash in sources.items():
        if file_hash(ROOT / relative) != expected_hash:
            raise ValueError(f"Prior locked artifact/source or production file changed: {relative}")
    paths = [FEATURE_FILE, MANIFEST, ROOT / "data" / "raw" / "训练集.csv", ROOT / "run.py",
             ROOT / "src/features.py", ROOT / "src/scoring.py", ROOT / "evaluate.py",
             ROOT / "experiments/seed_ensemble.py", Path(frozen.__file__), Path(early.__file__),
             Path(__file__), OUT / "protocol.json", frozen.OUT / "protocol.json",
             source_tests_path, audit_path, ROOT / "validation/metrics.json",
             baseline_results_path, *prior_paths.values(), *early._paths(year, "baseline")]
    sources.update({str(path.relative_to(ROOT)): file_hash(path) for path in paths})
    return dict(sorted(sources.items()))


def fingerprint(year: int) -> dict:
    _check_year(year)
    cutoff = fold_cutoff(year)
    if cutoff != EXPECTED[year]["training_cutoff_exclusive"]:
        raise ValueError("The one-day historical purge boundary changed")
    features = feature_names()
    if len(features) != 63:
        raise ValueError("Exactly the original 63 features must be reused")
    payload = {"year": year, "candidate_key": CANDIDATE_KEY,
               "rounds": ROUNDS, "seed": SEED, "threads": THREADS,
               "params": params_for_seed(SEED, THREADS), "features": features,
               "training_cutoff_exclusive": cutoff,
               "training_filter": read_protocol()["training_filter"],
               "weighting": read_protocol()["weighting"], "postprocess": POSTPROCESS,
               "validation_labels_loaded": False, "candidate_selection_performed": False,
               "lightgbm_version": lgb.__version__, "numpy_version": np.__version__,
               "polars_version": pl.__version__, "source_sha256": _locked_sources(year)}
    payload["fingerprint_sha256"] = hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
    return payload


def _paths(year: int) -> tuple[Path, Path, Path]:
    _check_year(year)
    stem = f"{CANDIDATE_KEY}_{year}"
    return OUT / f"{stem}.txt", OUT / f"{stem}.parquet", OUT / f"{stem}.json"


def load_panel(year: int) -> Panel:
    _check_year(year)
    _baseline_metadata(year)
    panel = early.load_panel(year)
    if (np.isfinite(panel.y).any() or panel.frame["y_ret_1d"].null_count() != len(panel.frame)
            or panel.frame["y_ret_1d"].dtype != pl.Float64):
        raise AssertionError("Prediction panel must contain only null Float64 labels")
    if (panel.frame.select(pl.struct(KEYS).n_unique()).item() != len(panel.frame)
            or not panel.frame.select(KEYS).equals(panel.frame.sort("trade_date", "ts_code").select(KEYS))
            or not panel.frame["trade_date"].is_between(year * 10000 + 101, year * 10000 + 1231).all()):
        raise ValueError("Early baseline keys, ordering or calendar-year coverage differ")
    return panel


def load_raw(year: int, panel: Panel | None = None) -> np.ndarray:
    model_path, cache_path, meta_path = _paths(year)
    metadata = json.loads(meta_path.read_text(encoding="utf-8"))
    expected = fingerprint(year)
    if any(metadata.get(key) != value for key, value in expected.items()):
        raise ValueError(f"Stale historical equal-day model fingerprint/metadata: {year}")
    if (metadata["model_sha256"] != file_hash(model_path)
            or metadata["cache_sha256"] != file_hash(cache_path)):
        raise ValueError("Historical equal-day model or prediction cache hash changed")
    base = load_panel(year) if panel is None else panel
    frame = pl.read_parquet(cache_path)
    if (frame.columns != KEYS + ["pred_raw"]
            or not frame.select(KEYS).equals(base.frame.select(KEYS))
            or frame.select(pl.struct(KEYS).n_unique()).item() != len(frame)):
        raise ValueError("Historical equal-day raw keys/order/coverage differ from baseline")
    for field in ("training_first_date", "training_last_date", "training_rows"):
        if metadata[field] != EXPECTED[year][field]:
            raise ValueError(f"Historical equal-day {field} changed")
    weights = metadata["weight_statistics"]
    if (weights["training_days"] != EXPECTED[year]["training_days"]
            or metadata["validation_rows"] != len(frame)
            or metadata["reload_check_rows"] != min(4096, len(frame))
            or metadata["reload_max_abs_error"] != 0
            or abs(weights["actual_mean_float64"] - 1) > 1e-7
            or weights["max_relative_day_total_error"] > 1e-7):
        raise ValueError("Historical weight, coverage or reload assertions differ")
    raw = frame["pred_raw"].to_numpy()
    if (raw.dtype != np.float32 or not np.isfinite(raw).all()
            or np.any(raw[~base.valid_price.reshape(-1)] != np.float32(-1e6))):
        raise ValueError("Raw predictions must be finite Float32 with invalid-price sentinel")
    return raw


def train(year: int) -> None:
    expected = fingerprint(year)
    model_path, cache_path, meta_path = _paths(year)
    if any(path.exists() for path in (model_path, cache_path, meta_path)):
        if not all(path.exists() for path in (model_path, cache_path, meta_path)):
            raise ValueError("Incomplete historical equal-day cache exists; preserve for inspection")
        load_raw(year)
        log(f"Validated frozen historical equal-day cache: {year}")
        return
    features = expected["features"]
    cutoff = expected["training_cutoff_exclusive"]
    lazy = pl.scan_parquet(FEATURE_FILE)
    training_mask = (pl.col("is_train") & (pl.col("trade_date") < cutoff)
                     & pl.col("y_rank").is_not_null() & pl.col("price_valid"))
    frame = lazy.filter(training_mask).select(features + ["y_rank", "trade_date"]).collect()
    x = to_matrix(frame, features)
    y = frame["y_rank"].to_numpy().astype(np.float32)
    dates = frame["trade_date"].to_numpy()
    rows = len(y)
    first_date, last_date = int(dates.min()), int(dates.max())
    if (rows != EXPECTED[year]["training_rows"]
            or first_date != EXPECTED[year]["training_first_date"]
            or last_date != EXPECTED[year]["training_last_date"] or last_date >= cutoff
            or not np.isfinite(y).all()):
        raise AssertionError("Filtered historical rows, boundaries or finite targets differ")
    weights = training_weights(dates)
    _, inverse, counts = np.unique(dates, return_inverse=True, return_counts=True)
    daily_totals = np.bincount(inverse, weights=weights.astype(np.float64))
    days = len(counts)
    actual_mean = float(weights.mean(dtype=np.float64))
    relative_error = float(np.max(np.abs(daily_totals / (rows / days) - 1)))
    if (days != EXPECTED[year]["training_days"] or abs(actual_mean - 1) > 1e-7
            or relative_error > 1e-7):
        raise AssertionError("Historical equal-day normalization or daily totals differ")
    weight_stats = {"training_days": days,
                    "daily_rows_min": int(counts.min()), "daily_rows_max": int(counts.max()),
                    "min_weight": float(weights.min()), "max_weight": float(weights.max()),
                    "actual_mean_float64": actual_mean,
                    "target_total_weight_per_day": rows / days,
                    "max_relative_day_total_error": relative_error,
                    "weight_array_sha256": hashlib.sha256(weights.tobytes()).hexdigest(),
                    "scope": "Dates of final filtered training rows only; no validation/test labels or counts"}
    del frame, dates, inverse, counts, daily_totals
    gc.collect()
    log(f"Training {year}: rows={rows:,}, days={days}, features={len(features)}, "
        f"dates={first_date}..{last_date}, purged={cutoff}, mean_weight={actual_mean:.10f}")
    started = time.monotonic()
    dataset = lgb.Dataset(x, label=y, weight=weights, feature_name=features, free_raw_data=True)
    model = lgb.train(expected["params"], dataset, num_boost_round=ROUNDS)
    model_path.write_text(model.model_to_string(), encoding="utf-8")
    del dataset, x, y, weights
    gc.collect()
    valid = (lazy.filter(pl.col("is_train") & pl.col("trade_date").is_between(
        year * 10000 + 101, year * 10000 + 1231)).sort("trade_date", "ts_code")
        .select(features + KEYS + ["price_valid"]).collect())
    matrix = to_matrix(valid, features)
    raw = model.predict(matrix, num_threads=THREADS).astype(np.float32)
    valid_price = valid["price_valid"].to_numpy()
    raw[~valid_price] = -1e6
    if not np.isfinite(raw).all():
        raise AssertionError("Historical equal-day model emitted nonfinite raw predictions")
    reloaded = lgb.Booster(model_str=model_path.read_text(encoding="utf-8"))
    if reloaded.feature_name() != features or reloaded.current_iteration() != ROUNDS:
        raise AssertionError("Saved historical model feature order or rounds differ")
    indices = np.linspace(0, len(raw) - 1, min(4096, len(raw)), dtype=int)
    checked = reloaded.predict(matrix[indices], num_threads=THREADS).astype(np.float32)
    checked[~valid_price[indices]] = -1e6
    reload_error = float(np.max(np.abs(checked.astype(float) - raw[indices].astype(float))))
    if reload_error != 0:
        raise AssertionError(f"Reloaded historical equal-day model differs: {reload_error}")
    result = valid.select(KEYS).with_columns(pl.Series("pred_raw", raw))
    if not result.select(KEYS).equals(load_panel(year).frame.select(KEYS)):
        raise AssertionError("Historical cache coverage or order differs from early baseline")
    result.write_parquet(cache_path, compression="zstd")
    if fingerprint(year) != expected:
        raise AssertionError("A frozen source/input changed during historical equal-day training")
    metadata = {**expected, "training_rows": rows, "training_first_date": first_date,
                "training_last_date": last_date, "validation_rows": len(raw),
                "validation_days": valid["trade_date"].n_unique(),
                "validation_first_date": int(valid["trade_date"].min()),
                "validation_last_date": int(valid["trade_date"].max()),
                "weight_statistics": weight_stats,
                "model_sha256": file_hash(model_path), "cache_sha256": file_hash(cache_path),
                "reload_check_rows": len(indices), "reload_max_abs_error": reload_error,
                "elapsed_seconds": time.monotonic() - started}
    meta_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"Saved {year}: rows={len(raw):,}, elapsed={metadata['elapsed_seconds']:.1f}s, reload={reload_error}")
    del model, reloaded, matrix, valid, raw, result
    gc.collect()
    load_raw(year)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("step", choices=("train",))
    parser.add_argument("--year", type=int, required=True, choices=YEARS)
    args = parser.parse_args()
    train(args.year)
