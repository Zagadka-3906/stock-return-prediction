"""Frozen robust return-amplitude auxiliary model, without validation labels.

Only the TRAINING target differs from the production regression. Candidate
prediction construction is intentionally outside this label-free module.
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

from experiments.day_balance_models import file_hash
from experiments.seed_ensemble import params_for_seed
from run import FEATURE_FILE, MANIFEST, ROOT, feature_names, fold_cutoff, to_matrix
from src.scoring import Panel


OUT = ROOT / "experiments" / "return_head_eval"
PRIMARY_YEARS = (2022, 2023)
CANDIDATE_KEY = "protected_return_w0p25"
MODEL_KEY = "return_z1_99"
ROUNDS, SEED, THREADS = 180, 2026, 16
BLEND = {"mode": "top_only", "weight": .25}
POSTPROCESS = {"alpha": .9, "bonus": .3, "restore_lower": True, "top_current_weight": 1.0}
KEYS = ["ts_code", "trade_date"]
EXPECTED = {
    2022: {"training_cutoff_exclusive": 20211231, "training_first_date": 20180102,
           "training_last_date": 20211230, "training_rows": 3568878, "training_days": 972},
    2023: {"training_cutoff_exclusive": 20221230, "training_first_date": 20180102,
           "training_last_date": 20221229, "training_rows": 4597785, "training_days": 1214},
    2024: {"training_cutoff_exclusive": 20231229, "training_first_date": 20180102,
           "training_last_date": 20231228, "training_rows": 5659954, "training_days": 1456},
}


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def read_protocol() -> dict:
    protocol = json.loads((OUT / "protocol.json").read_text(encoding="utf-8"))
    fixed = {"experiment": "fixed_return_amplitude_head_protected_top_rerank",
             "declared_before_training": True, "candidate_key": CANDIDATE_KEY,
             "model_key": MODEL_KEY, "primary_years": list(PRIMARY_YEARS),
             "conditional_diagnostic_year": 2024, "candidate_count": 1,
             "feature_count": 63, "rounds": ROUNDS, "seed": SEED, "threads": THREADS,
             "blend": BLEND, "postprocess": POSTPROCESS,
             "training_filter": "is_train & trade_date < fold_cutoff(year) & y_rank.not_null & price_valid"}
    if any(protocol.get(key) != value for key, value in fixed.items()):
        raise ValueError("Return-head protocol differs from the single frozen design")
    fixed_target = {
        "input": "cached Float32 y_ret_1d for final filtered training rows only, promoted to Float64 before all statistics",
        "quantiles": [.01, .99], "quantile_method": "linear",
        "formula": "For each training date: clipped=clip(return,q01,q99); z=(clipped-mean(clipped))/std(clipped,ddof=0)",
        "standard_deviation_ddof": 0, "near_constant_std_threshold": 1e-12,
        "near_constant_action": "Set every target on that date to zero; do not delete rows",
        "output": "Float32 target in original training row order",
        "weights": "None; no equal-day, top-label or recency weights", "tuning": "None",
    }
    if protocol.get("target") != fixed_target:
        raise ValueError("The return-amplitude target specification changed")
    if protocol.get("folds") != {str(year): values for year, values in EXPECTED.items()}:
        raise ValueError("Declared training fold boundaries changed")
    return protocol


def _target_with_stats(dates: np.ndarray, returns: np.ndarray) -> tuple[np.ndarray, dict]:
    """Normalize final filtered TRAINING labels only, retaining original order."""
    dates = np.asarray(dates)
    values = np.asarray(returns)
    if (dates.ndim != 1 or not len(dates) or dates.dtype.kind not in "iuf"
            or not np.isfinite(dates).all() or not np.equal(dates, np.floor(dates)).all()):
        raise ValueError("Dates must be a nonempty vector of finite integers")
    if (values.ndim != 1 or len(values) != len(dates) or values.dtype.kind not in "iuf"
            or not np.isfinite(values).all()):
        raise ValueError("Training returns must be finite numeric values aligned to dates")
    with np.errstate(over="ignore", invalid="ignore"):
        cached = values.astype(np.float32)
    if not np.isfinite(cached).all():
        raise ValueError("Training return input must be representable as finite Float32")
    values = cached.astype(np.float64)
    # Stable date indices gather groups but never reorder the model's rows.
    order = np.argsort(dates, kind="stable")
    ordered_dates = dates[order]
    bounds = np.r_[0, np.flatnonzero(ordered_dates[1:] != ordered_dates[:-1]) + 1, len(dates)]
    result = np.empty(len(dates), dtype=np.float32)
    mean_errors, std_errors = [], []
    nearconstant = 0
    minimum_clipped_std = np.inf
    maximum_clipped_std = 0.0
    for left, right in zip(bounds[:-1], bounds[1:]):
        indices = order[left:right]
        daily = values[indices]
        low, high = np.quantile(daily, [.01, .99], method="linear")
        clipped = np.clip(daily, low, high)
        center = float(clipped.mean(dtype=np.float64))
        scale = float(clipped.std(ddof=0, dtype=np.float64))
        minimum_clipped_std = min(minimum_clipped_std, scale)
        maximum_clipped_std = max(maximum_clipped_std, scale)
        if scale <= 1e-12:
            normalized = np.zeros(len(daily), dtype=np.float32)
            nearconstant += 1
        else:
            normalized = ((clipped - center) / scale).astype(np.float32)
            std_errors.append(abs(float(normalized.std(ddof=0, dtype=np.float64)) - 1))
        mean_errors.append(abs(float(normalized.mean(dtype=np.float64))))
        result[indices] = normalized
    if not np.isfinite(result).all():
        raise AssertionError("Daily return-amplitude target contains nonfinite values")
    stats = {"target_array_sha256": hashlib.sha256(result.tobytes()).hexdigest(),
             "training_days": len(bounds) - 1, "training_rows": len(result),
             "nearconstant_days": nearconstant,
             "max_abs_daily_mean": float(max(mean_errors)),
             "max_abs_daily_std_minus_one_nonconstant": float(max(std_errors, default=0.0)),
             "target_min": float(result.min()), "target_max": float(result.max()),
             "clipped_std_min": float(minimum_clipped_std),
             "clipped_std_max": float(maximum_clipped_std),
             "input_dtype": "Float32_promoted_to_Float64", "output_dtype": "Float32",
             "scope": "Only final filtered historical training labels; validation/test labels excluded"}
    return result, stats


def training_target(dates: np.ndarray, returns: np.ndarray) -> np.ndarray:
    return _target_with_stats(dates, returns)[0]


def test_target() -> dict:
    dates = np.array([1, 2, 1, 3, 1, 2, 1, 4, 1, 4], dtype=np.int32)
    returns = np.array([-100, 5, 0, 12, 0, 5, 1, -1e-14, 100, 1e-14], dtype=np.float32)
    target, stats = _target_with_stats(dates, returns)
    clipped = np.array([-96.0, 0, 0, 1, 96.04], dtype=np.float64)
    expected = ((clipped - clipped.mean()) / clipped.std(ddof=0)).astype(np.float32)
    assert np.array_equal(target[dates == 1], expected)
    assert np.all(target[dates != 1] == 0)
    assert target.dtype == np.float32 and len(target) == len(returns)
    assert stats["nearconstant_days"] == 3
    assert stats["training_days"] == 4
    assert target[2] == target[4]  # Tied original labels remain tied.
    assert stats["max_abs_daily_mean"] < 1e-7
    assert stats["max_abs_daily_std_minus_one_nonconstant"] < 1e-7
    permutation = np.array([8, 4, 0, 7, 2, 5, 9, 6, 1, 3])
    assert np.allclose(training_target(dates[permutation], returns[permutation]),
                       target[permutation], rtol=0, atol=1e-7)
    assert np.array_equal(training_target([7], [2]), np.zeros(1, np.float32))
    assert np.array_equal(training_target([1, 1], [8, 8]), np.zeros(2, np.float32))
    assert np.array_equal(training_target(dates, returns.astype(np.float64)), target)
    # Original Float32 cached returns, not new high-precision input, define labels.
    float64_rounded = returns.astype(np.float64)
    float64_rounded[1] += 1e-10
    assert np.array_equal(training_target(dates, float64_rounded), target)
    rejected = []
    invalid = (("empty", [], []), ("non_vector_date", [[1, 2]], [1, 2]),
               ("non_vector_return", [1, 2], [[1, 2]]), ("length_mismatch", [1], [1, 2]),
               ("fractional_date", [1, 2.5], [1, 2]), ("nan_date", [1, np.nan], [1, 2]),
               ("infinite_date", [1, np.inf], [1, 2]), ("string_date", ["1"], [1]),
               ("nan_return", [1, 1], [0, np.nan]), ("infinite_return", [1], [np.inf]),
               ("string_return", [1], ["1"]), ("float32_overflow", [1], [1e100]),
               ("boolean_date", [True], [1]), ("boolean_return", [1], [True]))
    for name, bad_dates, bad_returns in invalid:
        try:
            training_target(bad_dates, bad_returns)
        except ValueError:
            rejected.append(name)
        else:
            raise AssertionError(f"Invalid target inputs accepted: {name}")
    with_dates = np.r_[dates, [20250102, 20250103]]
    with_returns = np.r_[returns, [np.nan, np.inf]]
    training_mask = np.arange(len(with_dates)) < len(dates)
    assert np.array_equal(training_target(with_dates[training_mask], with_returns[training_mask]), target)
    with_returns[~training_mask] = [-10000, 10000]
    assert np.array_equal(training_target(with_dates[training_mask], with_returns[training_mask]), target)
    # Distinct future TRAINING dates also cannot alter an existing date's target.
    appended = training_target(with_dates, with_returns)
    assert np.array_equal(appended[:len(target)], target)
    return {"status": "passed", "manual_linear_quantile_outlier_fixture_exact": True,
            "constant_single_row_nearconstant_zero": True, "ties_retained": True,
            "original_row_order_retained": True, "permutation_equivariant_tolerance": 1e-7,
            "cached_float32_rounding_before_float64_statistics": True,
            "invalid_inputs_rejected": rejected,
            "future_suffix_filtered_before_target_construction": True,
            "distinct_date_append_leaves_existing_targets_exact": True,
            "fixture_stats": stats, "source_sha256": file_hash(Path(__file__)),
            "protocol_sha256": file_hash(OUT / "protocol.json")}


def _locked_sources() -> dict[str, str]:
    protocol = read_protocol()
    tests_path = OUT / "target_tests.json"
    if json.loads(tests_path.read_text(encoding="utf-8")) != test_target():
        raise ValueError("Frozen target tests no longer match source/protocol")
    prior_out = ROOT / "experiments/day_balance_early_eval"
    results_path, decision_path = prior_out / "results.json", prior_out / "decision.json"
    if (file_hash(results_path) != protocol["previous_results_sha256"]
            or file_hash(decision_path) != protocol["previous_decision_sha256"]):
        raise ValueError("Prior evidence differs from the predeclared chain")
    prior = json.loads(results_path.read_text(encoding="utf-8"))
    decision = json.loads(decision_path.read_text(encoding="utf-8"))
    if decision.get("results_sha256") != file_hash(results_path):
        raise ValueError("Prior decision and results no longer match")
    sources = dict(prior["artifacts_sha256"])
    audit_path = ROOT / "validation/prediction_audit.json"
    sources.update(json.loads(audit_path.read_text(encoding="utf-8"))["input_sha256"])
    for relative, expected_hash in sources.items():
        if file_hash(ROOT / relative) != expected_hash:
            raise ValueError(f"Prior locked source/artifact or production file changed: {relative}")
    paths = [FEATURE_FILE, MANIFEST, ROOT / "data" / "raw" / "训练集.csv", ROOT / "run.py",
             ROOT / "src/features.py", ROOT / "src/scoring.py", ROOT / "evaluate.py",
             ROOT / "experiments/seed_ensemble.py", ROOT / "experiments/day_balance_models.py",
             ROOT / "experiments/cached_recheck.py", ROOT / "experiments/official_seed_development.py",
             Path(__file__), OUT / "protocol.json", tests_path,
             results_path, decision_path, audit_path, ROOT / "validation/metrics.json"]
    sources.update({str(path.relative_to(ROOT)): file_hash(path) for path in paths})
    return dict(sorted(sources.items()))


def _check_year(year: int) -> None:
    if year not in (*PRIMARY_YEARS, 2024):
        raise ValueError("Only predeclared primary folds and the gated 2024 diagnostic are permitted")


def _paths(year: int) -> tuple[Path, Path, Path]:
    _check_year(year)
    stem = f"{MODEL_KEY}_{year}"
    return OUT / f"{stem}.txt", OUT / f"{stem}.parquet", OUT / f"{stem}.json"


def diagnostic_gate() -> dict:
    path = OUT / "development.json"
    if not path.exists():
        raise ValueError("2024 is forbidden until the complete primary gate passes")
    record = json.loads(path.read_text(encoding="utf-8"))
    if (record.get("primary_gate_passed") is not True
            or record.get("candidate_key") != CANDIDATE_KEY
            or record.get("primary_years") != list(PRIMARY_YEARS)
            or record.get("candidate_count") != 1
            or record.get("blend") != BLEND
            or record.get("postprocess") != POSTPROCESS
            or record.get("protocol_sha256") != file_hash(OUT / "protocol.json")):
        raise ValueError("2024 development gate is missing, failed or mismatched")
    audit_source = ROOT / "experiments/audit_return_head.py"
    if record.get("audit_source_sha256") != file_hash(audit_source):
        raise ValueError("The primary audit implementation changed after development")
    required = {str(path.relative_to(ROOT)) for path in (
        audit_source, OUT / "protocol.json", OUT / "target_tests.json", OUT / "prediction_tests.json")}
    for year in PRIMARY_YEARS:
        yearly = record.get("years", {}).get(str(year), {})
        baseline, candidate = yearly.get("baseline", {}), yearly.get("candidate", {})
        for metric in ("ic_mean", "annual_excess", "final_score"):
            old, new = baseline.get(metric, np.nan), candidate.get(metric, np.nan)
            if not np.isfinite(old) or not np.isfinite(new) or not new > old:
                raise ValueError(f"2024 forbidden: {year} did not improve {metric}")
        if (yearly.get("official_turnover_top_identities_equal") is not True
                or yearly.get("official_daily_turnover_exact") is not True):
            raise ValueError("2024 requires actual daily Top identities AND exact turnover-series preservation")
        if (baseline.get("mean_turnover") != candidate.get("mean_turnover")
                or yearly.get("prediction_checks", {}).get("official_top_identity", {}).get(
                    "daily_top_identities_exact") is not True):
            raise ValueError("2024 daily Top evidence or aggregate turnover is inconsistent")
        current_fingerprint = fingerprint(year)
        if record.get("model_fingerprints", {}).get(str(year)) != current_fingerprint["fingerprint_sha256"]:
            raise ValueError("Primary model fingerprint differs from development")
        load_raw(year)
        required.update(current_fingerprint["source_sha256"])
        required.update(str(path.relative_to(ROOT)) for path in _paths(year))
        for kind in ("baseline", "candidate"):
            required.add(str((OUT / f"official_{kind}_{year}_daily.csv").relative_to(ROOT)))
            required.add(str((OUT / f"{kind}_processed_{year}.parquet").relative_to(ROOT)))
    artifacts = record.get("artifacts_sha256", {})
    if not required.issubset(artifacts):
        raise ValueError("Development must lock primary sources, models, caches and daily prediction evidence")
    for relative, expected_hash in artifacts.items():
        if file_hash(ROOT / relative) != expected_hash:
            raise ValueError(f"Development artifact changed: {relative}")
    return {"development_sha256": file_hash(path), "primary_gate_passed": True}


def fingerprint(year: int) -> dict:
    _check_year(year)
    gate = diagnostic_gate() if year == 2024 else None
    cutoff = fold_cutoff(year)
    if cutoff != EXPECTED[year]["training_cutoff_exclusive"]:
        raise ValueError("One-day purge boundary changed")
    features = feature_names()
    if len(features) != 63:
        raise ValueError("Exactly the original 63 features must be retained")
    sources = _locked_sources()
    for path in (ROOT / f"models/fold_{year}.txt", ROOT / f"validation/fold_{year}.parquet"):
        sources[str(path.relative_to(ROOT))] = file_hash(path)
    payload = {"year": year, "candidate_key": CANDIDATE_KEY, "model_key": MODEL_KEY,
               "rounds": ROUNDS, "seed": SEED, "threads": THREADS,
               "params": params_for_seed(SEED, THREADS), "features": features,
               "training_cutoff_exclusive": cutoff,
               "training_filter": read_protocol()["training_filter"],
               "target": read_protocol()["target"], "sample_weight": None,
               "blend": BLEND, "postprocess": POSTPROCESS,
               "validation_labels_loaded": False,
               "lightgbm_version": lgb.__version__, "numpy_version": np.__version__,
               "polars_version": pl.__version__, "source_sha256": dict(sorted(sources.items()))}
    if gate is not None:
        payload["diagnostic_gate"] = gate
    payload["fingerprint_sha256"] = hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
    return payload


def load_panel(year: int) -> Panel:
    _check_year(year)
    if year == 2024:
        diagnostic_gate()
    frame = pl.read_parquet(ROOT / f"validation/fold_{year}.parquet",
                            columns=KEYS + ["flag_limit_up", "price_valid", "pred_raw"])
    if (frame.select(pl.struct(KEYS).n_unique()).item() != len(frame)
            or not frame.select(KEYS).equals(frame.sort("trade_date", "ts_code").select(KEYS))
            or not frame["trade_date"].is_between(year * 10000 + 101, year * 10000 + 1231).all()):
        raise ValueError("Baseline keys/order/year differ")
    panel = Panel.from_frame(frame.with_columns(pl.lit(None, dtype=pl.Float64).alias("y_ret_1d")))
    if np.isfinite(panel.y).any():
        raise AssertionError("Prediction panel must not contain validation labels")
    return panel


def load_raw(year: int, panel: Panel | None = None) -> np.ndarray:
    model_path, cache_path, meta_path = _paths(year)
    metadata = json.loads(meta_path.read_text(encoding="utf-8"))
    expected = fingerprint(year)
    if any(metadata.get(key) != value for key, value in expected.items()):
        raise ValueError(f"Stale return-head fingerprint/metadata: {year}")
    if (metadata["model_sha256"] != file_hash(model_path)
            or metadata["cache_sha256"] != file_hash(cache_path)):
        raise ValueError("Return-head model or prediction cache hash changed")
    base = load_panel(year) if panel is None else panel
    frame = pl.read_parquet(cache_path)
    if (frame.columns != KEYS + ["pred_raw"]
            or not frame.select(KEYS).equals(base.frame.select(KEYS))
            or frame.select(pl.struct(KEYS).n_unique()).item() != len(frame)):
        raise ValueError("Auxiliary raw keys/order/coverage differ from baseline")
    for field in ("training_first_date", "training_last_date", "training_rows"):
        if metadata[field] != EXPECTED[year][field]:
            raise ValueError(f"Saved training {field} changed")
    stats = metadata["target_stats"]
    if (stats["training_days"] != EXPECTED[year]["training_days"]
            or stats["training_rows"] != EXPECTED[year]["training_rows"]
            or metadata["validation_rows"] != len(frame)
            or metadata["reload_check_rows"] != min(4096, len(frame))
            or metadata["reload_max_abs_error"] != 0):
        raise ValueError("Saved target, coverage or reload assertions differ")
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
            raise ValueError("Incomplete return-head cache exists; preserve for inspection")
        load_raw(year)
        log(f"Validated frozen return-head cache: {year}")
        return
    features = expected["features"]
    cutoff = expected["training_cutoff_exclusive"]
    lazy = pl.scan_parquet(FEATURE_FILE)
    training_mask = (pl.col("is_train") & (pl.col("trade_date") < cutoff)
                     & pl.col("y_rank").is_not_null() & pl.col("price_valid"))
    # Identical filter, original row order and nullable features; only y differs.
    frame = lazy.filter(training_mask).select(features + ["trade_date", "y_ret_1d"]).collect()
    if frame["y_ret_1d"].dtype != pl.Float32:
        raise AssertionError("Training source returns must be the frozen Float32 cache")
    x = to_matrix(frame, features)
    dates, returns = frame["trade_date"].to_numpy(), frame["y_ret_1d"].to_numpy()
    rows, first_date, last_date = len(frame), int(dates.min()), int(dates.max())
    if (rows != EXPECTED[year]["training_rows"]
            or first_date != EXPECTED[year]["training_first_date"]
            or last_date != EXPECTED[year]["training_last_date"] or last_date >= cutoff
            or not np.isfinite(returns).all()):
        raise AssertionError("Training mask rows, dates or finite returns differ")
    y, target_stats = _target_with_stats(dates, returns)
    if target_stats["training_days"] != EXPECTED[year]["training_days"]:
        raise AssertionError("Target training-day count changed")
    del frame, dates, returns
    gc.collect()
    log(f"Training {year}/{MODEL_KEY}: rows={rows:,}, days={target_stats['training_days']}, "
        f"features={len(features)}, dates={first_date}..{last_date}, purge={cutoff}")
    started = time.monotonic()
    dataset = lgb.Dataset(x, label=y, feature_name=features, free_raw_data=True)
    model = lgb.train(expected["params"], dataset, num_boost_round=ROUNDS)
    model_path.write_text(model.model_to_string(), encoding="utf-8")
    del dataset, x, y
    gc.collect()
    valid = (lazy.filter(pl.col("is_train") & pl.col("trade_date").is_between(
        year * 10000 + 101, year * 10000 + 1231)).sort("trade_date", "ts_code")
        .select(features + KEYS + ["price_valid"]).collect())
    matrix = to_matrix(valid, features)
    raw = model.predict(matrix, num_threads=THREADS).astype(np.float32)
    valid_price = valid["price_valid"].to_numpy()
    raw[~valid_price] = -1e6
    if not np.isfinite(raw).all():
        raise AssertionError("Return-head model emitted nonfinite raw predictions")
    reloaded = lgb.Booster(model_str=model_path.read_text(encoding="utf-8"))
    if reloaded.feature_name() != features or reloaded.current_iteration() != ROUNDS:
        raise AssertionError("Saved return-head feature order or rounds differ")
    indices = np.linspace(0, len(raw) - 1, min(4096, len(raw)), dtype=int)
    checked = reloaded.predict(matrix[indices], num_threads=THREADS).astype(np.float32)
    checked[~valid_price[indices]] = -1e6
    reload_error = float(np.max(np.abs(checked.astype(float) - raw[indices].astype(float))))
    if reload_error != 0:
        raise AssertionError(f"Reloaded return-head model differs: {reload_error}")
    result = valid.select(KEYS).with_columns(pl.Series("pred_raw", raw))
    if not result.select(KEYS).equals(load_panel(year).frame.select(KEYS)):
        raise AssertionError("Return-head cache coverage/order differs from baseline")
    result.write_parquet(cache_path, compression="zstd")
    if fingerprint(year) != expected:
        raise AssertionError("A frozen source/input changed during return-head training")
    metadata = {**expected, "training_rows": rows, "training_first_date": first_date,
                "training_last_date": last_date, "validation_rows": len(raw),
                "validation_days": valid["trade_date"].n_unique(),
                "validation_first_date": int(valid["trade_date"].min()),
                "validation_last_date": int(valid["trade_date"].max()),
                "target_stats": target_stats,
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
        result = test_target()
        tests_path = OUT / "target_tests.json"
        if tests_path.exists() and json.loads(tests_path.read_text(encoding="utf-8")) != result:
            raise ValueError("Preserve prior tests: frozen source or protocol changed")
        if not tests_path.exists():
            tests_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        log("All frozen return-head target tests passed")
    else:
        if args.year is None:
            parser.error("train requires one explicit --year; 2024 is independently gated")
        train(args.year)
