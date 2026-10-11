"""Frozen upper-return training-weight experiment; never load validation labels.

Only the training Dataset weight differs from the 63-feature production model.
Primary folds are 2022/2023. A separate, hash-verified development gate is needed
before the single predeclared 2024 diagnostic model can be trained or loaded.
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

from experiments.seed_ensemble import file_hash, params_for_seed
from run import FEATURE_FILE, MANIFEST, ROOT, feature_names, fold_cutoff, to_matrix
from src.scoring import Panel


OUT = ROOT / "experiments" / "top_weight_eval"
PRIMARY_YEARS = (2022, 2023)
POSTPROCESS = {"alpha": .9, "bonus": .3, "restore_lower": True, "top_current_weight": 1.0}
ROUNDS, SEED, THREADS = 180, 2026, 16
CANDIDATE_KEY = "top10_weight1p5"
KEYS = ["ts_code", "trade_date"]
EXPECTED = {
    2022: {"training_cutoff_exclusive": 20211231, "training_last_date": 20211230,
           "training_rows": 3568878},
    2023: {"training_cutoff_exclusive": 20221230, "training_last_date": 20221229,
           "training_rows": 4597785},
    2024: {"training_cutoff_exclusive": 20231229, "training_last_date": 20231228,
           "training_rows": 5659954},
}


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def read_protocol() -> dict:
    protocol = json.loads((OUT / "protocol.json").read_text(encoding="utf-8"))
    fixed = {"experiment": "single_training_top_decile_weight_1p5",
             "declared_before_training": True, "candidate_key": CANDIDATE_KEY,
             "primary_years": list(PRIMARY_YEARS), "conditional_diagnostic_year": 2024,
             "feature_count": 63, "rounds": ROUNDS, "seed": SEED, "threads": THREADS,
             "postprocess": POSTPROCESS,
             "training_filter": "is_train & trade_date < fold_cutoff(year) & y_rank.not_null & price_valid"}
    if any(protocol.get(key) != value for key, value in fixed.items()):
        raise ValueError("Training-weight protocol differs from its fixed design")
    expected_weight = {"target_column": "y_rank", "threshold": .4,
                       "threshold_dtype": "float32", "comparison": "strictly_greater",
                       "top_weight": 1.5, "other_weight": 1.0,
                       "normalization": "divide_by_mean_of_weights_in_filtered_training_fold_then_cast_float32"}
    if any(protocol["weighting"].get(key) != value for key, value in expected_weight.items()):
        raise ValueError("The single predeclared weighting rule changed")
    if protocol["folds"] != {str(year): values for year, values in EXPECTED.items()}:
        raise ValueError("Training boundaries differ from the predeclared fold manifest")
    return protocol


def training_weights(y: np.ndarray) -> np.ndarray:
    """The caller must pass already filtered TRAINING targets, never validation.

    The caller enforces the temporal/filter scope. Across folds the mean changes
    with the training sample mix, so training-weight prefix invariance is neither
    expected nor a valid test of prediction causality.
    """
    with np.errstate(over="ignore", invalid="ignore"):
        values = np.asarray(y, dtype=np.float32)
    if values.ndim != 1 or not len(values) or not np.isfinite(values).all():
        raise ValueError("Weights require a nonempty finite one-dimensional training target")
    raw = np.where(values > np.float32(.4), 1.5, 1.0)
    return (raw / raw.mean(dtype=np.float64)).astype(np.float32)


def test_weights() -> dict:
    """Deterministic unit tests of the frozen threshold and normalization rule."""
    boundary = np.float32(.4)
    below, above = np.nextafter(boundary, np.float32(-np.inf)), np.nextafter(boundary, np.float32(np.inf))
    values = np.array([-.5, 0, below, boundary, boundary, above, .5], dtype=np.float32)
    weights = training_weights(values)
    mask = values > boundary
    raw = np.where(mask, 1.5, 1.0)
    expected = (raw / raw.mean(dtype=np.float64)).astype(np.float32)
    assert weights.dtype == np.float32 and np.array_equal(weights, expected)
    assert np.all(weights[values == boundary] == weights[~mask][0])
    assert weights[-2] > weights[-3]
    assert abs(weights.mean(dtype=np.float64) - 1) < 1e-7
    ratio = float(weights[mask][0]) / float(weights[~mask][0])
    assert abs(ratio - 1.5) < 2e-7
    assert np.array_equal(training_weights(np.array([.41, .5], np.float32)), np.ones(2, np.float32))
    assert np.array_equal(training_weights(np.array([-.5, .4], np.float32)), np.ones(2, np.float32))
    rejected = []
    for name, bad in (("nan", [0, np.nan]), ("positive_infinity", [0, np.inf]),
                      ("negative_infinity", [-np.inf, .5]), ("empty", []),
                      ("non_vector", [[0, .5]]), ("float32_overflow", [1e100])):
        try:
            training_weights(bad)
        except ValueError:
            rejected.append(name)
        else:
            raise AssertionError(f"Invalid targets accepted: {name}")
    permutation = np.array([6, 0, 4, 1, 5, 3, 2])
    assert np.array_equal(training_weights(values[permutation]), weights[permutation])
    extended = np.concatenate([values, np.array([.5] * 5, np.float32)])
    extended_weights = training_weights(extended)
    rescaling = extended_weights[:len(values)].astype(float) / weights.astype(float)
    assert np.max(rescaling) - np.min(rescaling) < 2e-7
    assert not np.array_equal(extended_weights[:len(values)], weights)
    # A synthetic validation suffix never enters the filtered training call.
    with_suffix = np.concatenate([values, [np.nan, .45]])
    training_mask = np.arange(len(with_suffix)) < len(values)
    assert np.array_equal(training_weights(with_suffix[training_mask]), weights)
    with_suffix[~training_mask] = [-.5, np.inf]
    assert np.array_equal(training_weights(with_suffix[training_mask]), weights)
    return {"status": "passed", "threshold_float32": float(boundary),
            "strict_boundary_and_ties_passed": True, "normalization_and_ratio_passed": True,
            "all_upper_and_no_upper_passed": True, "permutation_equivariance_passed": True,
            "invalid_inputs_rejected": rejected,
            "validation_suffix_excluded_before_weighting_passed": True,
            "training_append_only_common_rescaling_passed": True,
            "training_append_note": "Adding TRAINING rows legitimately changes the fold normalization. Validation/test rows must never enter this function; the training mask enforces that boundary.",
            "example_mean_float64": float(weights.mean(dtype=np.float64)),
            "example_upper_to_other_ratio": ratio,
            "source_sha256": file_hash(Path(__file__)),
            "protocol_sha256": file_hash(OUT / "protocol.json")}


def _locked_sources() -> dict[str, str]:
    protocol = read_protocol()
    tests_path = OUT / "weight_tests.json"
    tests = json.loads(tests_path.read_text(encoding="utf-8"))
    if tests != test_weights():
        raise ValueError("Weight tests no longer match the frozen implementation/protocol")
    diagnosis_path = ROOT / "experiments/top_loss_diagnosis/results.json"
    if file_hash(diagnosis_path) != protocol["previous_top_diagnosis_results_sha256"]:
        raise ValueError("Prior Top-loss diagnosis differs from the predeclared evidence")
    diagnosis = json.loads(diagnosis_path.read_text(encoding="utf-8"))
    sources = {**diagnosis["sources_sha256"], **diagnosis["artifacts_sha256"]}
    audit_path = ROOT / "validation/prediction_audit.json"
    production_audit = json.loads(audit_path.read_text(encoding="utf-8"))
    sources.update(production_audit["input_sha256"])
    for relative, expected_hash in sources.items():
        if file_hash(ROOT / relative) != expected_hash:
            raise ValueError(f"Prior source/artifact or production file changed: {relative}")
    paths = [FEATURE_FILE, MANIFEST, ROOT / "data" / "raw" / "训练集.csv", ROOT / "run.py",
             ROOT / "src/features.py", ROOT / "src/scoring.py",
             ROOT / "experiments/seed_ensemble.py", ROOT / "evaluate.py",
             ROOT / "experiments/official_seed_development.py",
             ROOT / "experiments/cached_recheck.py", Path(__file__),
             OUT / "protocol.json", tests_path, diagnosis_path, audit_path,
             ROOT / "validation/metrics.json"]
    sources.update({str(path.relative_to(ROOT)): file_hash(path) for path in paths})
    return dict(sorted(sources.items()))


def _check_year(year: int) -> None:
    if year not in (*PRIMARY_YEARS, 2024):
        raise ValueError("Only the predeclared 2022/2023 folds and gated 2024 are permitted")


def _diagnostic_gate() -> dict:
    """Do not let a CLI call bypass the independent primary evaluation decision."""
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
        raise ValueError("Development gate must lock both trained primary models/caches/metadata")
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


def _paths(year: int) -> tuple[Path, Path, Path]:
    stem = f"{CANDIDATE_KEY}_{year}"
    return OUT / f"{stem}.txt", OUT / f"{stem}.parquet", OUT / f"{stem}.json"


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
        raise ValueError(f"Stale weighted-model fingerprint/metadata: {year}")
    if (metadata["model_sha256"] != file_hash(model_path)
            or metadata["cache_sha256"] != file_hash(cache_path)):
        raise ValueError("Weighted model or raw cache hash changed")
    base = load_panel(year) if panel is None else panel
    frame = pl.read_parquet(cache_path)
    if (frame.columns != KEYS + ["pred_raw"]
            or not frame.select(KEYS).equals(base.frame.select(KEYS))
            or frame.select(pl.struct(KEYS).n_unique()).item() != len(frame)):
        raise ValueError("Weighted raw prediction keys/order/coverage differ from the baseline")
    if (metadata["training_rows"] != EXPECTED[year]["training_rows"]
            or metadata["training_last_date"] != EXPECTED[year]["training_last_date"]
            or metadata["validation_rows"] != len(frame)
            or metadata["reload_check_rows"] != min(4096, len(frame))
            or metadata["reload_max_abs_error"] != 0):
        raise ValueError("Weighted-model boundary or reload assertions differ")
    raw = frame["pred_raw"].to_numpy()
    if (raw.dtype != np.float32 or not np.isfinite(raw).all()
            or np.any(raw[~base.valid_price.reshape(-1)] != np.float32(-1e6))):
        raise ValueError("Weighted raw predictions must be finite Float32 with invalid-price sentinel")
    return raw


def train(year: int) -> None:
    expected = fingerprint(year)
    model_path, cache_path, meta_path = _paths(year)
    if any(path.exists() for path in (model_path, cache_path, meta_path)):
        if not all(path.exists() for path in (model_path, cache_path, meta_path)):
            raise ValueError("Incomplete weighted-model cache exists; preserve it for inspection")
        load_raw(year)
        log(f"Validated frozen weighted-model cache: {year}")
        return
    features = expected["features"]
    cutoff = expected["training_cutoff_exclusive"]
    lazy = pl.scan_parquet(FEATURE_FILE)
    training_mask = (pl.col("is_train") & (pl.col("trade_date") < cutoff)
                     & pl.col("y_rank").is_not_null() & pl.col("price_valid"))
    # Preserve production row order and do not drop nullable feature values.
    frame = lazy.filter(training_mask).select(features + ["y_rank", "trade_date"]).collect()
    x = to_matrix(frame, features)
    y = frame["y_rank"].to_numpy().astype(np.float32)
    rows = len(y)
    first_date, last_date = int(frame["trade_date"].min()), int(frame["trade_date"].max())
    if (rows != EXPECTED[year]["training_rows"]
            or last_date != EXPECTED[year]["training_last_date"] or last_date >= cutoff
            or not np.isfinite(y).all()):
        raise AssertionError("Filtered training rows, dates or finite targets differ")
    weights = training_weights(y)
    top = y > np.float32(.4)
    top_count = int(top.sum())
    normalization_mean = float(np.where(top, 1.5, 1.0).mean(dtype=np.float64))
    actual_mean = float(weights.mean(dtype=np.float64))
    effective_upper = float(weights[top][0]) if top_count else None
    effective_other = float(weights[~top][0]) if top_count != rows else None
    ratio = effective_upper / effective_other if effective_upper is not None and effective_other is not None else None
    if abs(actual_mean - 1) > 1e-7 or ratio is None or abs(ratio - 1.5) > 2e-7:
        raise AssertionError("Training weight normalization or upper-to-other ratio differs")
    daily = (frame.select("trade_date").with_columns(pl.Series("upper", top))
             .group_by("trade_date").agg(pl.col("upper").mean().alias("upper_fraction")))
    weight_stats = {"upper_count": top_count, "upper_fraction": top_count / rows,
                    "training_days": len(daily),
                    "daily_upper_fraction_min": float(daily["upper_fraction"].min()),
                    "daily_upper_fraction_max": float(daily["upper_fraction"].max()),
                    "threshold_float32": float(np.float32(.4)),
                    "threshold_tie_count": int(np.count_nonzero(y == np.float32(.4))),
                    "normalization_mean_float64": normalization_mean,
                    "effective_upper_weight_float32": effective_upper,
                    "effective_other_weight_float32": effective_other,
                    "actual_mean_float64": actual_mean, "upper_to_other_ratio": ratio,
                    "weight_array_sha256": hashlib.sha256(weights.tobytes()).hexdigest(),
                    "scope": "Only filtered training targets; no validation or test labels loaded"}
    del frame, daily, top
    gc.collect()
    log(f"Training {year}: rows={rows:,}, upper={top_count:,}, features={len(features)}, "
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
        raise AssertionError("Weighted model emitted nonfinite raw predictions")
    reloaded = lgb.Booster(model_str=model_path.read_text(encoding="utf-8"))
    if reloaded.feature_name() != features or reloaded.current_iteration() != ROUNDS:
        raise AssertionError("Saved weighted model feature order or rounds differ")
    indices = np.linspace(0, len(raw) - 1, min(4096, len(raw)), dtype=int)
    checked = reloaded.predict(matrix[indices], num_threads=THREADS).astype(np.float32)
    checked[~valid_price[indices]] = -1e6
    reload_error = float(np.max(np.abs(checked.astype(float) - raw[indices].astype(float))))
    if reload_error != 0:
        raise AssertionError(f"Reloaded weighted model differs: {reload_error}")
    result = valid.select(KEYS).with_columns(pl.Series("pred_raw", raw))
    if not result.select(KEYS).equals(load_panel(year).frame.select(KEYS)):
        raise AssertionError("Weighted cache coverage or ordering differs from frozen baseline")
    result.write_parquet(cache_path, compression="zstd")
    if fingerprint(year) != expected:
        raise AssertionError("A frozen input/source changed during weighted-model training")
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
        log("All frozen weighting unit tests passed")
    else:
        if args.year is None:
            parser.error("train requires one explicit --year; 2024 is independently gated")
        train(args.year)
