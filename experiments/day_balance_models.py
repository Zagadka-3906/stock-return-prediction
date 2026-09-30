"""Single equal-day training-weight experiment, without validation labels.

Only Dataset(weight=...) changes from the production 63-feature regression.
No label magnitude, recency preference, or validation counts enter weights.
"""
from __future__ import annotations

import argparse
import gc
import hashlib
import json
import time
from functools import lru_cache
from pathlib import Path

import lightgbm as lgb
import numpy as np
import polars as pl

from experiments.seed_ensemble import file_hash as source_file_hash, params_for_seed
from run import FEATURE_FILE, MANIFEST, ROOT, feature_names, fold_cutoff, to_matrix
from src.scoring import Panel


OUT = ROOT / "experiments" / "day_balance_eval"
PRIMARY_YEARS = (2022, 2023)
POSTPROCESS = {"alpha": .9, "bonus": .3, "restore_lower": True, "top_current_weight": 1.0}
ROUNDS, SEED, THREADS = 180, 2026, 16
CANDIDATE_KEY = "equal_day"
KEYS = ["ts_code", "trade_date"]
EXPECTED = {
    2022: {"training_cutoff_exclusive": 20211231, "training_last_date": 20211230,
           "training_rows": 3568878, "training_days": 972},
    2023: {"training_cutoff_exclusive": 20221230, "training_last_date": 20221229,
           "training_rows": 4597785, "training_days": 1214},
    2024: {"training_cutoff_exclusive": 20231229, "training_last_date": 20231228,
           "training_rows": 5659954, "training_days": 1456},
}


@lru_cache(maxsize=512)
def _cached_hash(path: str, size: int, mtime_ns: int) -> str:
    del size, mtime_ns
    return source_file_hash(Path(path))


def file_hash(path: Path) -> str:
    stat = path.stat()
    return _cached_hash(str(path.resolve()), stat.st_size, stat.st_mtime_ns)


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def read_protocol() -> dict:
    protocol = json.loads((OUT / "protocol.json").read_text(encoding="utf-8"))
    fixed = {"experiment": "equal_total_training_weight_per_trade_date",
             "declared_before_training": True, "candidate_key": CANDIDATE_KEY,
             "primary_years": list(PRIMARY_YEARS), "conditional_diagnostic_year": 2024,
             "feature_count": 63, "rounds": ROUNDS, "seed": SEED, "threads": THREADS,
             "postprocess": POSTPROCESS,
             "training_filter": "is_train & trade_date < fold_cutoff(year) & y_rank.not_null & price_valid"}
    if any(protocol.get(key) != value for key, value in fixed.items()):
        raise ValueError("Equal-day protocol differs from its fixed design")
    expected_weight = {"input": "trade_date_of_final_filtered_training_rows_only",
                       "formula": "w_i = N / (D * n_date_i)",
                       "calculation": "float64_then_cast_float32", "tunables": "none"}
    if any(protocol["weighting"].get(key) != value for key, value in expected_weight.items()):
        raise ValueError("The single predeclared weighting rule changed")
    if protocol["folds"] != {str(year): values for year, values in EXPECTED.items()}:
        raise ValueError("Training boundaries differ from the predeclared manifest")
    return protocol


def training_weights(dates: np.ndarray) -> np.ndarray:
    """Pass only dates of the final filtered TRAINING rows, in model row order.

    The caller enforces temporal scope. Refitting on more training days/rows may
    legitimately change the date counts and normalization; fitted prediction
    causality, not weight-prefix invariance across refits, is required.
    """
    values = np.asarray(dates)
    if values.ndim != 1 or not len(values) or values.dtype.kind not in "iuf":
        raise ValueError("Weights require nonempty one-dimensional numeric training dates")
    if not np.isfinite(values).all() or not np.equal(values, np.floor(values)).all():
        raise ValueError("Training dates must be finite integers")
    _, inverse, counts = np.unique(values, return_inverse=True, return_counts=True)
    per_day_weight = len(values) / (len(counts) * counts.astype(np.float64))
    return per_day_weight[inverse].astype(np.float32)


def test_weights() -> dict:
    dates = np.array([20190102, 20190102, 20190103, 20190104, 20190104, 20190104], np.int32)
    weights = training_weights(dates)
    expected = np.array([1, 1, 2, 2 / 3, 2 / 3, 2 / 3], np.float32)
    assert weights.dtype == np.float32 and np.array_equal(weights, expected)
    totals = []
    for date in np.unique(dates):
        date_weights = weights[dates == date]
        assert np.all(date_weights == date_weights[0])
        totals.append(date_weights.sum(dtype=np.float64))
    assert np.max(np.abs(np.asarray(totals) / 2 - 1)) <= 1e-7
    assert abs(weights.mean(dtype=np.float64) - 1) <= 1e-7
    assert np.array_equal(training_weights([1, 1, 1]), np.ones(3, np.float32))
    assert np.array_equal(training_weights([1, 2, 2, 1]), np.ones(4, np.float32))
    permutation = np.array([5, 2, 0, 4, 1, 3])
    assert np.array_equal(training_weights(dates[permutation]), weights[permutation])
    assert np.array_equal(training_weights(dates.astype(np.float64)), weights)
    rejected = []
    for name, bad in (("empty", []), ("non_vector", [[1, 2]]), ("fractional", [1, 2.5]),
                      ("nan", [1, np.nan]), ("positive_infinity", [1, np.inf]),
                      ("negative_infinity", [-np.inf, 2]), ("strings", ["1", "2"]),
                      ("booleans", [True, False]), ("complex", [1 + 0j])):
        try:
            training_weights(bad)
        except ValueError:
            rejected.append(name)
        else:
            raise AssertionError(f"Invalid dates accepted: {name}")
    # Appending future validation observations does not alter filtered inputs.
    with_suffix = np.concatenate([dates.astype(float), [20220104, 20220105]])
    training_mask = np.arange(len(with_suffix)) < len(dates)
    assert np.array_equal(training_weights(with_suffix[training_mask]), weights)
    with_suffix[~training_mask] = [np.nan, np.inf]
    assert np.array_equal(training_weights(with_suffix[training_mask]), weights)
    more_training = np.append(dates, dates[0])
    assert not np.array_equal(training_weights(more_training)[:len(dates)], weights)
    return {"status": "passed", "unequal_date_counts_formula_exact": True,
            "equal_weights_within_date": True, "equal_total_weight_per_date": True,
            "global_mean_one": True, "single_date_and_balanced_dates_all_one": True,
            "permutation_equivariance_passed": True, "integer_float_dates_same": True,
            "invalid_inputs_rejected": rejected,
            "validation_suffix_excluded_before_weighting_passed": True,
            "changed_training_counts_can_change_weights_passed": True,
            "example_mean_float64": float(weights.mean(dtype=np.float64)),
            "example_daily_weight_totals": totals,
            "source_sha256": file_hash(Path(__file__)),
            "protocol_sha256": file_hash(OUT / "protocol.json")}


def _locked_sources() -> dict[str, str]:
    protocol = read_protocol()
    tests_path = OUT / "weight_tests.json"
    if json.loads(tests_path.read_text(encoding="utf-8")) != test_weights():
        raise ValueError("Weight tests no longer match the frozen implementation/protocol")
    prior_path = ROOT / "experiments/top_weight_eval/development.json"
    if file_hash(prior_path) != protocol["previous_top_weight_development_sha256"]:
        raise ValueError("Prior development evidence differs from the predeclared hash")
    prior = json.loads(prior_path.read_text(encoding="utf-8"))
    sources = dict(prior["artifacts_sha256"])
    audit_path = ROOT / "validation/prediction_audit.json"
    production_audit = json.loads(audit_path.read_text(encoding="utf-8"))
    sources.update(production_audit["input_sha256"])
    for relative, expected_hash in sources.items():
        if file_hash(ROOT / relative) != expected_hash:
            raise ValueError(f"Prior artifact or production file changed: {relative}")
    paths = [FEATURE_FILE, MANIFEST, ROOT / "data" / "raw" / "训练集.csv", ROOT / "run.py",
             ROOT / "src/features.py", ROOT / "src/scoring.py",
             ROOT / "experiments/seed_ensemble.py", ROOT / "evaluate.py",
             ROOT / "experiments/official_seed_development.py",
             ROOT / "experiments/cached_recheck.py", Path(__file__),
             OUT / "protocol.json", tests_path, prior_path, audit_path,
             ROOT / "validation/metrics.json"]
    sources.update({str(path.relative_to(ROOT)): file_hash(path) for path in paths})
    return dict(sorted(sources.items()))


def _check_year(year: int) -> None:
    if year not in (*PRIMARY_YEARS, 2024):
        raise ValueError("Only predeclared 2022/2023 folds and gated 2024 are permitted")


def _paths(year: int) -> tuple[Path, Path, Path]:
    stem = f"{CANDIDATE_KEY}_{year}"
    return OUT / f"{stem}.txt", OUT / f"{stem}.parquet", OUT / f"{stem}.json"


def _diagnostic_gate() -> dict:
    path = OUT / "development.json"
    if not path.exists():
        raise ValueError("2024 is forbidden until both primary folds pass the fixed gate")
    record = json.loads(path.read_text(encoding="utf-8"))
    if (record.get("primary_gate_passed") is not True
            or record.get("candidate_key") != CANDIDATE_KEY
            or record.get("primary_years") != list(PRIMARY_YEARS)
            or record.get("protocol_sha256") != file_hash(OUT / "protocol.json")):
        raise ValueError("2024 development gate is missing, failed or mismatched")
    for year in PRIMARY_YEARS:
        yearly = record.get("years", {}).get(str(year), {})
        baseline, candidate = yearly.get("baseline", {}), yearly.get("candidate", {})
        for metric in ("final_score", "annual_excess"):
            old, new = baseline.get(metric, np.nan), candidate.get(metric, np.nan)
            if not np.isfinite(old) or not np.isfinite(new) or not new > old:
                raise ValueError(f"2024 forbidden: {year} did not improve {metric}")
        if record.get("model_fingerprints", {}).get(str(year)) != fingerprint(year)["fingerprint_sha256"]:
            raise ValueError("Primary model source fingerprint differs from development")
        load_raw(year)
    artifacts = record.get("artifacts_sha256", {})
    required = {str(path.relative_to(ROOT)) for year in PRIMARY_YEARS for path in _paths(year)}
    if not required.issubset(artifacts):
        raise ValueError("Development must lock both trained primary models/caches/metadata")
    for relative, expected_hash in artifacts.items():
        if file_hash(ROOT / relative) != expected_hash:
            raise ValueError(f"Development artifact changed: {relative}")
    return {"development_sha256": file_hash(path), "primary_gate_passed": True}


def fingerprint(year: int) -> dict:
    _check_year(year)
    diagnostic_gate = _diagnostic_gate() if year == 2024 else None
    cutoff = fold_cutoff(year)
    if cutoff != EXPECTED[year]["training_cutoff_exclusive"]:
        raise ValueError("The one-day purge boundary changed")
    features = feature_names()
    if len(features) != 63:
        raise ValueError("The fixed experiment requires the original 63 features")
    sources = _locked_sources()
    for path in (ROOT / f"models/fold_{year}.txt", ROOT / f"validation/fold_{year}.parquet"):
        sources[str(path.relative_to(ROOT))] = file_hash(path)
    payload = {"year": year, "candidate_key": CANDIDATE_KEY,
               "rounds": ROUNDS, "seed": SEED, "threads": THREADS,
               "params": params_for_seed(SEED, THREADS), "features": features,
               "training_cutoff_exclusive": cutoff,
               "training_filter": read_protocol()["training_filter"],
               "weighting": read_protocol()["weighting"], "postprocess": POSTPROCESS,
               "validation_labels_loaded": False,
               "lightgbm_version": lgb.__version__, "numpy_version": np.__version__,
               "polars_version": pl.__version__, "source_sha256": dict(sorted(sources.items()))}
    if diagnostic_gate is not None:
        payload["diagnostic_gate"] = diagnostic_gate
    payload["fingerprint_sha256"] = hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
    return payload


def load_panel(year: int) -> Panel:
    _check_year(year)
    if year == 2024:
        _diagnostic_gate()
    frame = pl.read_parquet(ROOT / f"validation/fold_{year}.parquet",
                            columns=KEYS + ["flag_limit_up", "price_valid", "pred_raw"])
    if (frame.select(pl.struct(KEYS).n_unique()).item() != len(frame)
            or not frame.select(KEYS).equals(frame.sort("trade_date", "ts_code").select(KEYS))
            or not frame["trade_date"].is_between(year * 10000 + 101, year * 10000 + 1231).all()):
        raise ValueError("Baseline panel keys, ordering or year differ")
    panel = Panel.from_frame(frame.with_columns(pl.lit(None, dtype=pl.Float64).alias("y_ret_1d")))
    if np.isfinite(panel.y).any():
        raise AssertionError("Prediction panel unexpectedly contains validation labels")
    return panel


def load_raw(year: int, panel: Panel | None = None) -> np.ndarray:
    _check_year(year)
    model_path, cache_path, meta_path = _paths(year)
    metadata = json.loads(meta_path.read_text(encoding="utf-8"))
    expected = fingerprint(year)
    if any(metadata.get(key) != value for key, value in expected.items()):
        raise ValueError(f"Stale equal-day model fingerprint/metadata: {year}")
    if (metadata["model_sha256"] != file_hash(model_path)
            or metadata["cache_sha256"] != file_hash(cache_path)):
        raise ValueError("Equal-day model or raw cache hash changed")
    base = load_panel(year) if panel is None else panel
    frame = pl.read_parquet(cache_path)
    if (frame.columns != KEYS + ["pred_raw"]
            or not frame.select(KEYS).equals(base.frame.select(KEYS))
            or frame.select(pl.struct(KEYS).n_unique()).item() != len(frame)):
        raise ValueError("Equal-day raw prediction keys/order/coverage differ from baseline")
    if (metadata["training_rows"] != EXPECTED[year]["training_rows"]
            or metadata["training_last_date"] != EXPECTED[year]["training_last_date"]
            or metadata["weight_statistics"]["training_days"] != EXPECTED[year]["training_days"]
            or metadata["validation_rows"] != len(frame)
            or metadata["reload_check_rows"] != min(4096, len(frame))
            or metadata["reload_max_abs_error"] != 0):
        raise ValueError("Equal-day model boundary or reload assertions differ")
    weights = metadata["weight_statistics"]
    if (abs(weights["actual_mean_float64"] - 1) > 1e-7
            or weights["max_relative_day_total_error"] > 1e-7):
        raise ValueError("Equal-day weight normalization differs")
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
            raise ValueError("Incomplete equal-day cache exists; preserve for inspection")
        load_raw(year)
        log(f"Validated frozen equal-day model cache: {year}")
        return
    features = expected["features"]
    cutoff = expected["training_cutoff_exclusive"]
    lazy = pl.scan_parquet(FEATURE_FILE)
    training_mask = (pl.col("is_train") & (pl.col("trade_date") < cutoff)
                     & pl.col("y_rank").is_not_null() & pl.col("price_valid"))
    # Preserve production row order and retain all nullable feature values.
    frame = lazy.filter(training_mask).select(features + ["y_rank", "trade_date"]).collect()
    x = to_matrix(frame, features)
    y = frame["y_rank"].to_numpy().astype(np.float32)
    dates = frame["trade_date"].to_numpy()
    rows = len(y)
    first_date, last_date = int(dates.min()), int(dates.max())
    if (rows != EXPECTED[year]["training_rows"]
            or last_date != EXPECTED[year]["training_last_date"] or last_date >= cutoff
            or not np.isfinite(y).all()):
        raise AssertionError("Filtered training rows, dates or finite targets differ")
    weights = training_weights(dates)
    unique_dates, inverse, counts = np.unique(dates, return_inverse=True, return_counts=True)
    daily_totals = np.bincount(inverse, weights=weights.astype(np.float64))
    days = len(counts)
    actual_mean = float(weights.mean(dtype=np.float64))
    relative_error = float(np.max(np.abs(daily_totals / (rows / days) - 1)))
    if (days != EXPECTED[year]["training_days"] or abs(actual_mean - 1) > 1e-7
            or relative_error > 1e-7):
        raise AssertionError("Equal-day weight normalization or daily totals differ")
    weight_stats = {"training_days": days,
                    "daily_rows_min": int(counts.min()), "daily_rows_max": int(counts.max()),
                    "min_weight": float(weights.min()), "max_weight": float(weights.max()),
                    "actual_mean_float64": actual_mean,
                    "target_total_weight_per_day": rows / days,
                    "max_relative_day_total_error": relative_error,
                    "weight_array_sha256": hashlib.sha256(weights.tobytes()).hexdigest(),
                    "scope": "Dates of final filtered training rows only; no validation/test labels or counts"}
    del frame, dates, unique_dates, inverse, counts, daily_totals
    gc.collect()
    log(f"Training {year}: rows={rows:,}, days={days}, features={len(features)}, "
        f"dates={first_date}..{last_date}, purged={cutoff}, mean_weight={actual_mean:.10f}")
    started = time.monotonic()
    dataset = lgb.Dataset(x, label=y, weight=weights, feature_name=features, free_raw_data=True)
    model = lgb.train(expected["params"], dataset, num_boost_round=ROUNDS)
    model_path.write_text(model.model_to_string(), encoding="utf-8")
    del dataset, x, y, weights
    gc.collect()
    validation_mask = pl.col("is_train") & pl.col("trade_date").is_between(
        year * 10000 + 101, year * 10000 + 1231)
    valid = (lazy.filter(validation_mask).sort("trade_date", "ts_code")
             .select(features + KEYS + ["price_valid"]).collect())
    matrix = to_matrix(valid, features)
    raw = model.predict(matrix, num_threads=THREADS).astype(np.float32)
    valid_price = valid["price_valid"].to_numpy()
    raw[~valid_price] = -1e6
    if not np.isfinite(raw).all():
        raise AssertionError("Equal-day model emitted nonfinite raw predictions")
    reloaded = lgb.Booster(model_str=model_path.read_text(encoding="utf-8"))
    if reloaded.feature_name() != features or reloaded.current_iteration() != ROUNDS:
        raise AssertionError("Saved model feature order or rounds differ")
    indices = np.linspace(0, len(raw) - 1, min(4096, len(raw)), dtype=int)
    checked = reloaded.predict(matrix[indices], num_threads=THREADS).astype(np.float32)
    checked[~valid_price[indices]] = -1e6
    reload_error = float(np.max(np.abs(checked.astype(float) - raw[indices].astype(float))))
    if reload_error != 0:
        raise AssertionError(f"Reloaded equal-day model differs: {reload_error}")
    result = valid.select(KEYS).with_columns(pl.Series("pred_raw", raw))
    if not result.select(KEYS).equals(load_panel(year).frame.select(KEYS)):
        raise AssertionError("Equal-day cache coverage or order differs from baseline")
    result.write_parquet(cache_path, compression="zstd")
    if fingerprint(year) != expected:
        raise AssertionError("A frozen source/input changed during equal-day training")
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
    parser.add_argument("step", choices=("test", "train"))
    parser.add_argument("--year", type=int, choices=(*PRIMARY_YEARS, 2024))
    args = parser.parse_args()
    if args.step == "test":
        read_protocol()
        result = test_weights()
        tests_path = OUT / "weight_tests.json"
        if tests_path.exists() and json.loads(tests_path.read_text(encoding="utf-8")) != result:
            raise ValueError("Preserve previous tests: frozen source or protocol changed")
        if not tests_path.exists():
            tests_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        log("All frozen equal-day weighting unit tests passed")
    else:
        if args.year is None:
            parser.error("train requires one explicit --year; 2024 is independently gated")
        train(args.year)
