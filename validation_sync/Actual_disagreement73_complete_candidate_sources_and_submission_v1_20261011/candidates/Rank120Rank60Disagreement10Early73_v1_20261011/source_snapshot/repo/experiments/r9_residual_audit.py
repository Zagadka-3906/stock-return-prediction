"""Independent audit helpers for one fixed OOF residual correction experiment.

The synthetic tests read no historical candidate data. The explicit stage audit
rebuilds rank targets, date weights and WLS calibration; it only reloads the
saved tree for inference and never refits the candidate model.
"""
from __future__ import annotations

import os
for _name in ("POLARS_MAX_THREADS", "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_name] = "4"

import argparse
import hashlib
import json
from pathlib import Path
import sys
from unittest.mock import patch

import numpy as np
import polars as pl
from scipy.stats import rankdata, spearmanr

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from experiments.r6_transformer_audit import independent_official_score, _raw_year
from experiments.r7_complement_audit import rebuild_post
from experiments.audit_r5_candidate import paired_block_bootstrap

OUT = ROOT / "experiments/r9_residual_20260926"
R4 = ROOT / "experiments/revalidation_20260926/validation"
KEYS = ["ts_code", "trade_date"]
PRIMARY = "oof_residual"
YEARS = {"development": (2022,), "confirmation": (2023, 2024)}
REFERENCES = ("baseline", "ensemble4")
BOOTSTRAP = {"block_days": 20, "draws": 20000, "seed": 2026, "positive_share_min": .8}
GATES = {
    "development": {"mean_score_delta_min": .001, "mean_ic_delta_min": -.002},
    "confirmation": {"mean_score_delta_min": .0005, "worst_year_score_delta_min": -.003, "mean_ic_delta_min": -.002},
    "mechanism_development": {"relative_daily_mse_improvement_min": .001, "mean_raw_rank_ic_delta_min": 0.},
    "mechanism_confirmation": {"mean_relative_daily_mse_improvement_min": 0.,
        "worst_year_relative_daily_mse_improvement_min": -.001, "mean_raw_rank_ic_delta_min": 0.},
    "bootstrap": BOOTSTRAP,
}
PARAMS = {"objective": "regression", "metric": "l2", "boosting_type": "gbdt", "num_leaves": 7,
    "learning_rate": .05, "min_data_in_leaf": 1000, "lambda_l2": 10., "max_bin": 127,
    "feature_fraction": 1., "bagging_fraction": 1., "bagging_freq": 0, "boost_from_average": True,
    "deterministic": True, "force_col_wise": True, "num_threads": 8, "seed": 2026,
    "data_random_seed": 2026, "feature_fraction_seed": 2026, "bagging_seed": 2026, "verbosity": -1}
ARTIFACTS = (("training_rows", "parquet"), ("calibration", "json"), ("model", "txt"),
             ("predictions_residual", "parquet"), ("mechanism_daily", "csv"),
             ("daily_residual", "csv"), ("daily_ensemble4", "csv"), ("daily_baseline", "csv"))


def sha(path: Path) -> str:
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def read(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def confined(base: Path, relative: str) -> Path:
    path = (base / relative).resolve()
    if not path.is_relative_to(base.resolve()):
        raise ValueError("Artifact path escaped its declared directory")
    return path


def check_hashes(base: Path, manifest: dict) -> dict:
    if not manifest:
        raise AssertionError("Empty artifact binding")
    result = {}
    for relative, digest in manifest.items():
        path = confined(base, relative)
        if sha(path) != digest:
            raise AssertionError(f"Changed bound artifact: {relative}")
        result[path.relative_to(ROOT).as_posix()] = digest
    return result


def close_arrays(actual, expected, context: str, tolerance: float = 1e-12) -> float:
    a, b = np.asarray(actual, dtype=np.float64), np.asarray(expected, dtype=np.float64)
    if a.shape != b.shape or not np.array_equal(np.isfinite(a), np.isfinite(b)):
        raise AssertionError(f"Different shape/finite masks: {context}")
    if not np.array_equal(np.isnan(a), np.isnan(b)) or not np.array_equal(np.isposinf(a), np.isposinf(b)):
        raise AssertionError(f"Different nonfinite values: {context}")
    finite = np.isfinite(a)
    error = float(np.max(np.abs(a[finite] - b[finite]))) if finite.any() else 0.
    if error > tolerance:
        raise AssertionError(f"Independent mismatch {context}: {error}")
    return error


def match(actual, expected, context="", tolerance=1e-12) -> float:
    if isinstance(actual, dict):
        if not isinstance(expected, dict) or actual.keys() != expected.keys():
            raise AssertionError(f"Different keys: {context}")
        return max((match(actual[key], expected[key], f"{context}/{key}", tolerance) for key in actual), default=0.)
    if isinstance(actual, (list, tuple)):
        if not isinstance(expected, (list, tuple)) or len(actual) != len(expected):
            raise AssertionError(f"Different sequence: {context}")
        return max((match(a, b, f"{context}/{i}", tolerance) for i, (a, b) in enumerate(zip(actual, expected))), default=0.)
    if isinstance(actual, (float, int)) and not isinstance(actual, bool):
        if not isinstance(expected, (float, int)) or isinstance(expected, bool):
            raise AssertionError(f"Different numeric type: {context}")
        return close_arrays([actual], [expected], context, tolerance)
    if actual != expected or type(actual) is not type(expected):
        raise AssertionError(f"Different value/type: {context}")
    return 0.


def canonical(frame: pl.DataFrame) -> pl.DataFrame:
    if not len(frame) or any(frame.select(KEYS).null_count().row(0)):
        raise ValueError("Nonempty frame and nonnull keys required")
    if frame.select(pl.struct(KEYS).n_unique()).item() != len(frame):
        raise ValueError("Duplicate stock/date keys")
    return frame.sort("trade_date", "ts_code")


def rank_inputs(frame: pl.DataFrame) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Independent b and u; only u uses labels. Invalid entries are NaN here."""
    if not frame.select(KEYS).equals(canonical(frame).select(KEYS)):
        raise ValueError("Expected canonical row order")
    if frame.schema["price_valid"] != pl.Boolean or frame["price_valid"].null_count():
        raise ValueError("price_valid must be nonnull Boolean")
    if frame.schema["y_ret_1d"] != pl.Float64:
        raise ValueError("Independent targets require original Float64 returns")
    raw = frame["pred_raw"].to_numpy().astype(np.float64)
    price = frame["price_valid"].to_numpy()
    y = frame["y_ret_1d"].to_numpy()
    if not np.isfinite(raw[price]).all():
        raise ValueError("Nonfinite signal in the full price-valid prediction pool")
    dates = frame["trade_date"].to_numpy()
    boundaries = np.r_[0, np.flatnonzero(np.diff(dates)) + 1, len(frame)]
    b, u = np.full(len(frame), np.nan), np.full(len(frame), np.nan)
    target = price & np.isfinite(y)
    for start, end in zip(boundaries[:-1], boundaries[1:]):
        rows = np.arange(start, end)
        current = rows[price[start:end]]
        labeled = rows[target[start:end]]
        if len(current):
            b[current] = rankdata(raw[current], method="average") / len(current)
        if len(labeled):
            u[labeled] = rankdata(y[labeled], method="average") / len(labeled)
    return b, u, target


def label_available_dates(signal_dates: np.ndarray, market_calendar: np.ndarray) -> np.ndarray:
    """Global next market date, never a per-stock shift or calendar-day offset."""
    dates = np.asarray(signal_dates, dtype=np.int64)
    calendar = np.asarray(market_calendar, dtype=np.int64)
    if calendar.ndim != 1 or not len(calendar) or np.any(np.diff(calendar) <= 0):
        raise ValueError("Global market calendar must be strictly increasing")
    index = np.searchsorted(calendar, dates)
    if np.any(index >= len(calendar)) or not np.array_equal(calendar[index], dates):
        raise ValueError("A signal date is absent from the frozen global calendar")
    available = np.full(dates.shape, -1, dtype=np.int64)
    has_next = index + 1 < len(calendar)
    available[has_next] = calendar[index[has_next] + 1]
    return available


def date_balanced_weights(dates: np.ndarray) -> np.ndarray:
    dates = np.asarray(dates, dtype=np.int64)
    unique, inverse, counts = np.unique(dates, return_inverse=True, return_counts=True)
    if not len(unique):
        raise ValueError("No eligible training dates")
    return len(dates) / (len(unique) * counts[inverse].astype(np.float64))


def calibration(b, u, dates) -> dict:
    """Independent unregularized WLS closed form with total sample weight one."""
    b, u = np.asarray(b, dtype=np.float64), np.asarray(u, dtype=np.float64)
    if b.shape != u.shape or b.shape != np.asarray(dates).shape or not np.isfinite(b).all() or not np.isfinite(u).all():
        raise ValueError("Finite aligned calibration inputs required")
    w = date_balanced_weights(dates) / len(b)
    mb, mu = float(np.sum(w * b)), float(np.sum(w * u))
    centered = b - mb
    variance = float(np.sum(w * centered * centered))
    if variance <= 0:
        raise ValueError("Unidentifiable constant calibration predictor")
    slope = float(np.sum(w * centered * (u - mu)) / variance)
    intercept = mu - slope * mb
    if not np.isfinite(slope) or slope <= 0 or not np.isfinite(intercept):
        raise ValueError("Nonpositive calibration is a failed fixed experiment, not a clipping opportunity")
    predicted = intercept + slope * b
    require_monotonic(b, predicted)
    return {"intercept": intercept, "slope": slope,
            "weighted_mse": float(np.sum(w * (u - predicted) ** 2)),
            "training_rows": len(b), "training_dates": len(np.unique(dates)),
            "training_date_values": list(map(int, np.unique(dates)))}


def require_monotonic(b, calibrated) -> None:
    """Strict Float64 monotonicity and exact ties, not just slope > 0."""
    b, m = np.asarray(b, dtype=np.float64), np.asarray(calibrated, dtype=np.float64)
    if not np.isfinite(b).all() or not np.isfinite(m).all() or b.shape != m.shape:
        raise ValueError("Finite aligned calibration values required")
    order = np.argsort(b, kind="stable")
    db, dm = np.diff(b[order]), np.diff(m[order])
    if np.any(dm[db > 0] <= 0) or np.any(dm[db == 0] != 0):
        raise AssertionError("Float64 calibration changed a tie or collapsed/reversed distinct ranks")


def mechanism_daily(frame: pl.DataFrame, raw: np.ndarray, zero: np.ndarray) -> pl.DataFrame:
    """Same label-valid target pool for rank target MSE and both raw rank ICs."""
    _, u, target = rank_inputs(frame)
    dates = frame["trade_date"].to_numpy()
    raw, zero = np.asarray(raw, dtype=np.float64), np.asarray(zero, dtype=np.float64)
    if raw.shape != u.shape or zero.shape != u.shape or not np.isfinite(raw[target]).all() or not np.isfinite(zero[target]).all():
        raise ValueError("Invalid same-target-pool mechanism predictions")
    rows = []
    for date in np.unique(dates):
        take = (dates == date) & target
        n = int(take.sum())
        if n < 30:
            raise ValueError("Validation mechanism requires at least 30 target rows per date")
        with np.errstate(invalid="ignore", divide="ignore"):
            ic0 = float(spearmanr(zero[take], u[take]).statistic) if n >= 2 else np.nan
            ic1 = float(spearmanr(raw[take], u[take]).statistic) if n >= 2 else np.nan
        rows.append({"trade_date": int(date), "n_target": n,
                     "mse_zero": float(np.mean((zero[take] - u[take]) ** 2)),
                     "mse_candidate": float(np.mean((raw[take] - u[take]) ** 2)),
                     "raw_rank_ic_zero": ic0, "raw_rank_ic_candidate": ic1})
    return pl.DataFrame(rows)


def mechanism_summary(daily: pl.DataFrame) -> dict:
    mse0 = float(daily["mse_zero"].mean())
    mse1 = float(daily["mse_candidate"].mean())
    ic0 = float(np.mean(daily["raw_rank_ic_zero"].to_numpy()))
    ic1 = float(np.mean(daily["raw_rank_ic_candidate"].to_numpy()))
    if mse0 <= 0 or not np.isfinite([mse0, mse1, ic0, ic1]).all():
        raise ValueError("Mechanism needs finite daily IC and positive mean zero-model MSE")
    return {"mse_zero": mse0, "mse_candidate": mse1,
            "relative_daily_mse_improvement": 1 - mse1 / mse0,
            "raw_rank_ic_zero": ic0, "raw_rank_ic_candidate": ic1,
            "mean_raw_rank_ic_delta": ic1 - ic0, "days": len(daily)}


def original_label_frame(year: int) -> pl.DataFrame:
    base = canonical(pl.read_parquet(R4 / f"predictions_ensemble4_{year}.parquet"))
    original = _raw_year(year)
    if not base.select(KEYS).equals(original.select(KEYS)):
        raise AssertionError("Original label and r4 stock/date keys differ")
    close_arrays(base["y_ret_1d"].to_numpy(), original["y_ret_1d"].to_numpy(), f"original labels/{year}", 0.)
    close_arrays(base["flag_limit_up"].to_numpy(), original["flag_limit_up"].to_numpy(), f"original flags/{year}", 0.)
    return base.with_columns(original["y_ret_1d"])


def independent_training_rows(frames: list[pl.DataFrame], calendar: np.ndarray, first_validation_date: int) -> tuple[pl.DataFrame, dict]:
    parts = []
    for frame in frames:
        b, u, target = rank_inputs(frame)
        available = label_available_dates(frame["trade_date"].to_numpy(), calendar)
        keep = target & (available > 0) & (available < first_validation_date)
        part = frame.select(KEYS).with_columns(pl.Series("b", b), pl.Series("target_u", u),
            pl.Series("label_available_date", available)).filter(pl.Series(keep))
        parts.append(part)
    rows = canonical(pl.concat(parts))
    dates, b, u = (rows[column].to_numpy() for column in ("trade_date", "b", "target_u"))
    fitted = calibration(b, u, dates)
    m = fitted["intercept"] + fitted["slope"] * b
    rows = rows.with_columns(pl.Series("calibrated_base", m), pl.Series("residual_target", u - m),
                             pl.Series("weight", date_balanced_weights(dates)))
    return rows, fitted


def array_sha(array: np.ndarray) -> str:
    values = np.ascontiguousarray(array)
    digest = hashlib.sha256(f"{values.dtype}|{values.shape}|".encode("ascii"))
    digest.update(memoryview(values).cast("B"))
    return digest.hexdigest()


def load_features(frame: pl.DataFrame, names: list[str]) -> np.ndarray:
    """Only current feature columns, never cached y_rank or Float32 return labels."""
    dates = frame["trade_date"].unique().to_list()
    source = (pl.scan_parquet(ROOT / "data/features.parquet")
        .filter(pl.col("is_train") & pl.col("trade_date").is_in(dates))
        .select(KEYS + ["price_valid"] + names).sort("trade_date", "ts_code").collect())
    if not frame.select(KEYS + ["price_valid"]).equals(source.select(KEYS + ["price_valid"])):
        raise AssertionError("Feature source and r4 panel keys/price validity differ")
    close_arrays(frame["flag_limit_up"].to_numpy(), source["flag_limit_up"].to_numpy(), "feature flags", 0.)
    matrix = np.ascontiguousarray(source.select(names).to_numpy(), dtype=np.float32)
    if np.isinf(matrix).any():
        raise AssertionError("Infinite original feature; no new imputation rule allowed")
    return matrix


def official_and_mechanism_gates(folds: list[dict], stage: str) -> tuple[dict, dict]:
    if tuple(f["year"] for f in folds) != YEARS[stage]:
        raise AssertionError("Incomplete or unexpected stage years")
    comparisons = {}
    for reference in REFERENCES:
        delta = np.array([f["metrics"]["final_score"] - f["references"][reference]["final_score"] for f in folds])
        ic = np.array([f["metrics"]["ic_mean"] - f["references"][reference]["ic_mean"] for f in folds])
        limits = GATES[stage]
        passed = delta.mean() >= limits["mean_score_delta_min"] and ic.mean() >= limits["mean_ic_delta_min"]
        if "worst_year_score_delta_min" in limits:
            passed = passed and delta.min() >= limits["worst_year_score_delta_min"]
        comparisons[reference] = {"score_deltas": dict(zip(map(str, YEARS[stage]), map(float, delta))),
            "mean_score_delta": float(delta.mean()), "worst_year_score_delta": float(delta.min()),
            "mean_ic_delta": float(ic.mean()), "passed": bool(passed)}
    mse = np.array([f["mechanism"]["relative_daily_mse_improvement"] for f in folds])
    raw_ic = np.array([f["mechanism"]["mean_raw_rank_ic_delta"] for f in folds])
    limits = GATES[f"mechanism_{stage}"]
    if stage == "development":
        passed = mse[0] >= limits["relative_daily_mse_improvement_min"] and raw_ic.mean() >= limits["mean_raw_rank_ic_delta_min"]
    else:
        passed = (mse.mean() >= limits["mean_relative_daily_mse_improvement_min"]
            and mse.min() >= limits["worst_year_relative_daily_mse_improvement_min"]
            and raw_ic.mean() >= limits["mean_raw_rank_ic_delta_min"])
    return ({"comparisons": comparisons, "passed": all(v["passed"] for v in comparisons.values())},
        {"relative_mse_by_year": dict(zip(map(str, YEARS[stage]), map(float, mse))),
         "mean_relative_daily_mse_improvement": float(mse.mean()),
         "worst_year_relative_daily_mse_improvement": float(mse.min()),
         "mean_raw_rank_ic_delta": float(raw_ic.mean()), "passed": bool(passed)})


def stage_pass(record: dict, official: dict, mechanism: dict, stage: str) -> bool:
    match(official, record["gate"], "official gate")
    match(mechanism, record["mechanism_gate"], "mechanism gate")
    point = official["passed"] and mechanism["passed"]
    match(point, record["point_gate_passed"], "point gate")
    bootstrap = record["bootstrap"]
    if not point:
        if bootstrap is not None:
            raise AssertionError("Bootstrap prohibited after failed point checks")
        passed = False
    else:
        if not isinstance(bootstrap, dict) or set(bootstrap) != set(REFERENCES):
            raise AssertionError("Both fixed bootstraps required")
        for value in bootstrap.values():
            if any(value[key] != BOOTSTRAP[key] for key in ("block_days", "draws", "seed")):
                raise AssertionError("Bootstrap settings changed")
            if not np.isfinite(value["bootstrap_share_positive"]) or not 0 <= value["bootstrap_share_positive"] <= 1 or value["years"] != list(YEARS[stage]):
                raise AssertionError("Invalid positive bootstrap share")
        passed = all(value["bootstrap_share_positive"] >= .8 for value in bootstrap.values())
    match(passed, record[f"{stage}_gate_passed"], "stage gate")
    return passed


def verify_protocol() -> tuple[dict, dict]:
    protocol = read(OUT / "protocol.json")
    match(protocol["gates"], GATES, "frozen gates", 0.)
    match(protocol["params"], PARAMS, "frozen residual tree", 0.)
    if protocol["rounds"] != 80 or protocol["primary_candidate"] != PRIMARY or protocol["candidate_count"] != 1:
        raise AssertionError("Candidate or iteration budget changed")
    for stage, years in YEARS.items():
        if protocol[f"{stage}_years"] != list(years):
            raise AssertionError("Stage years changed")
    if protocol["training_years"] != {str(y): list(range(2020, y)) for y in (2022, 2023, 2024)}:
        raise AssertionError("Training must use the fixed expanding prior OOF years")
    own = Path(__file__).relative_to(ROOT).as_posix()
    required_sources = {own, "experiments/r9_residual.py", "experiments/r9_residual_core.py"}
    if not required_sources <= protocol["source_sha256"].keys():
        raise AssertionError("Auditor/driver/core were not frozen")
    required_inputs = {"训练集.csv", "data/features.parquet", "data/feature_manifest.json", "evaluate.py",
        "experiments/r6_transformer_audit.py", "experiments/r7_complement_audit.py", "experiments/audit_r5_candidate.py"}
    for year in range(2020, 2025):
        required_inputs |= {f"experiments/revalidation_20260926/validation/predictions_{name}_{year}.parquet" for name in REFERENCES}
        required_inputs.add(f"experiments/revalidation_20260926/validation/result_{year}.json")
    if not required_inputs <= protocol["input_sha256"].keys():
        raise AssertionError("Missing raw labels, features or OOF source bindings")
    artifacts = check_hashes(ROOT, protocol["source_sha256"])
    artifacts.update(check_hashes(ROOT, protocol["input_sha256"]))
    names = read(ROOT / "data/feature_manifest.json")["features"]
    if len(names) != 63 or len(set(names)) != 63 or names != protocol["feature_names"]:
        raise AssertionError("Fixed feature identity/order changed")
    return protocol, artifacts


def checked_stage(stage: str, protocol_sha: str) -> tuple[dict, list[dict], dict]:
    record = read(OUT / f"{stage}.json")
    if (record["stage"] != stage or record["candidate_key"] != PRIMARY or record["years"] != list(YEARS[stage])
            or record["protocol_sha256"] != protocol_sha
            or set(record["fold_sha256"]) != {f"fold_{y}.json" for y in YEARS[stage]}):
        raise AssertionError("Stage/candidate/protocol/fold binding changed")
    folds, artifacts = [], {}
    for year in YEARS[stage]:
        path = OUT / f"fold_{year}.json"
        if sha(path) != record["fold_sha256"][path.name]:
            raise AssertionError("Fold checksum differs from fixed stage")
        fold = read(path)
        if (fold["year"] != year or fold["candidate_key"] != PRIMARY or fold["protocol_sha256"] != protocol_sha
                or fold["train_years"] != list(range(2020, year)) or set(fold["references"]) != set(REFERENCES)
                or set(fold["artifact_sha256"]) != {f"{prefix}_{year}.{extension}" for prefix, extension in ARTIFACTS}):
            raise AssertionError("Fold identity, training years or exact eight artifacts differ")
        artifacts.update(check_hashes(OUT, fold["artifact_sha256"]))
        artifacts[path.relative_to(ROOT).as_posix()] = sha(path)
        folds.append(fold)
    return record, folds, artifacts


def authorize_confirmation(protocol_sha: str) -> dict:
    record, folds, expected_artifacts = checked_stage("development", protocol_sha)
    official, mechanism = official_and_mechanism_gates(folds, "development")
    if not stage_pass(record, official, mechanism, "development"):
        raise ValueError("Failed development forbids confirmation access")
    audit = read(OUT / "independent_audit/audit_development.json")
    if (audit["status"] != "passed" or audit["stage_gate_passed"] is not True
            or audit["stage"] != "development" or audit["candidate_key"] != PRIMARY or audit["years"] != [2022]
            or audit["stage_record_sha256"] != sha(OUT / "development.json")
            or audit["protocol_sha256"] != protocol_sha or audit["source_sha256"] != sha(Path(__file__))):
        raise AssertionError("Unchanged passed independent development audit required")
    expected_artifacts[(OUT / "development.json").relative_to(ROOT).as_posix()] = sha(OUT / "development.json")
    if any(audit["artifacts_sha256"].get(key) != digest for key, digest in expected_artifacts.items()):
        raise AssertionError("Development audit must bind its stage, fold and all eight artifacts")
    check_hashes(ROOT, audit["artifacts_sha256"])
    return record


def audit(stage: str = "development") -> dict:
    if stage not in YEARS:
        raise ValueError(stage)
    output = OUT / "independent_audit"
    destination = output / f"audit_{stage}.json"
    if destination.exists() or any(output.glob(f"{stage}_*")):
        raise FileExistsError("Preserve previous or incomplete independent stage evidence")
    protocol, artifacts = verify_protocol()
    protocol_sha = sha(OUT / "protocol.json")
    if stage == "confirmation":
        authorize_confirmation(protocol_sha)
        prior_path = OUT / "independent_audit/audit_development.json"
        prior = read(prior_path)
        artifacts.update(prior["artifacts_sha256"])
        artifacts[prior_path.relative_to(ROOT).as_posix()] = sha(prior_path)
        artifacts[(OUT / "development.json").relative_to(ROOT).as_posix()] = sha(OUT / "development.json")
    record, folds, fold_artifacts = checked_stage(stage, protocol_sha)
    artifacts.update(fold_artifacts)
    stage_digest = sha(OUT / f"{stage}.json")
    artifacts[(OUT / f"{stage}.json").relative_to(ROOT).as_posix()] = stage_digest
    artifacts[(OUT / "protocol.json").relative_to(ROOT).as_posix()] = protocol_sha
    output.mkdir(parents=True, exist_ok=True)
    names = protocol["feature_names"]
    calendar = (pl.scan_parquet(ROOT / "data/features.parquet").filter(pl.col("is_train"))
        .select("trade_date").unique().sort("trade_date").collect()["trade_date"].to_numpy())
    audited, checks, daily_evidence = [], {}, {key: {} for key in (PRIMARY, *REFERENCES)}
    maxima = {"calibration": 0., "training_rows": 0., "raw_and_post": 0., "mechanism": 0., "official_metrics": 0., "daily_official": 0.}
    import lightgbm as lgb
    for fold in folds:
        year = fold["year"]
        print(json.dumps({"independent_training_rebuild": year}), flush=True)
        frames = [original_label_frame(y) for y in range(2020, year)]
        frame = original_label_frame(year)
        first = int(frame["trade_date"].min())
        train, fit = independent_training_rows(frames, calendar, first)
        saved = canonical(pl.read_parquet(OUT / f"training_rows_{year}.parquet"))
        if set(saved.columns) != set(KEYS + ["b", "target_u", "calibrated_base", "residual_target", "weight"]) or not train.select(KEYS).equals(saved.select(KEYS)):
            raise AssertionError("Saved training membership differs from mature original-label OOF rows")
        cal = read(OUT / f"calibration_{year}.json")
        for key, value in fit.items():
            maxima["calibration"] = max(maxima["calibration"], match(value, cal[key], f"calibration/{year}/{key}"))
        if cal["feature_names"] != names or cal["model_feature_names"] != names + ["r4_percentile"] or cal["params"] != PARAMS or cal["rounds"] != 80:
            raise AssertionError("Calibration/model metadata changes fixed model or feature order")
        for column in ("b", "target_u", "weight", "calibrated_base", "residual_target"):
            maxima["training_rows"] = max(maxima["training_rows"], close_arrays(train[column].to_numpy(), saved[column].to_numpy(), f"train/{year}/{column}"))
        match(len(train), fold["training"]["rows"], "training row count", 0.)
        match(fit["training_dates"], fold["training"]["dates"], "training date count", 0.)
        weights = train["weight"].to_numpy()
        if array_sha(weights) != fold["training"]["weight_sha256"]:
            raise AssertionError("Mean-one tree weights differ at the byte level")
        # The independently verified saved coefficients reproduce actual target
        # bytes; independent closed-form WLS can differ at ~1e-16 by summation.
        residual = train["target_u"].to_numpy() - (cal["intercept"] + cal["slope"] * train["b"].to_numpy())
        if array_sha(residual) != fold["training"]["target_residual_sha256"]:
            raise AssertionError("Saved tree target digest differs from verified original-label residuals")
        if array_sha(saved["residual_target"].to_numpy()) != fold["training"]["target_residual_sha256"]:
            raise AssertionError("Saved training evidence target differs from fitted target digest")
        close_arrays([weights.mean()], [fold["training"]["mean_weight"]], "mean-one weights")
        close_arrays([cal["weight_mean"], cal["calibration_weight_sum"]], [1., 1.], "calibration weight scales")
        if fold["training"]["feature_matrix_dtype"] != "float32" or fold["training"]["model_feature_names"] != names + ["r4_percentile"] or fold["training"]["feature_cache_labels_never_used"] is not True:
            raise AssertionError("Feature matrix contract differs")
        feature_digest = hashlib.sha256(f"float32|{(len(train), 64)}|".encode("ascii"))
        purged_dates, purged_rows, retained = set(), 0, 0
        first_training, last_training, last_available = None, None, None
        for source in frames:
            availability = label_available_dates(source["trade_date"].to_numpy(), calendar)
            mature = (availability > 0) & (availability < first)
            purged_dates.update(map(int, source["trade_date"].to_numpy()[~mature]))
            purged_rows += int((~mature).sum())
            full = source.filter(pl.Series(mature))
            retained += len(full)
            if not len(full):
                continue
            first_training = min(first_training or int(full["trade_date"].min()), int(full["trade_date"].min()))
            last_training, last_available = int(full["trade_date"].max()), int(availability[mature].max())
            b, _, target = rank_inputs(full)
            x = load_features(full, names)
            matrix = np.ascontiguousarray(np.column_stack([x[target], b[target].astype(np.float32)]), dtype=np.float32)
            feature_digest.update(memoryview(matrix).cast("B"))
            del x, matrix
        if feature_digest.hexdigest() != fold["training"]["feature_matrix_sha256"]:
            raise AssertionError("Independent original-feature training matrix SHA differs")
        bounds = {"validation_first": first, "first_training_signal": first_training,
            "last_training_signal": last_training, "last_label_available": last_available,
            "purged_signal_dates": sorted(purged_dates), "purged_panel_rows": purged_rows,
            "retained_panel_rows": retained, "training_oof_years": list(range(2020, year)),
            "strict_next_market_date_before_validation": True, "no_post_validation_training": True,
            "additional_post_test_embargo": "Not applicable: expanding past-only training; no future training segment."}
        match(bounds, fold["boundaries"], "independent training chronology", 0.)
        for prior_year in range(2020, year):
            provenance = read(R4 / f"result_{prior_year}.json")["boundaries"]
            if not (provenance["one_day_label_available"] < provenance["validation_first"]
                    and provenance["two_day_label_available"] < provenance["validation_first"]):
                raise AssertionError("Baseline source is not an earlier trained OOF prediction")
        del frames, train, saved
        model = lgb.Booster(model_str=(OUT / f"model_{year}.txt").read_text(encoding="utf-8"))
        if model.num_feature() != 64 or model.feature_name() != names + ["r4_percentile"] or model.current_iteration() > 80:
            raise AssertionError("Reloaded residual model feature/iteration identity differs")
        b, _, _ = rank_inputs(frame)
        valid = frame["price_valid"].to_numpy()
        zero = np.full(len(frame), -10., dtype=np.float64)
        zero[valid] = cal["intercept"] + cal["slope"] * b[valid]
        require_monotonic(b[valid], zero[valid])
        x = load_features(frame, names)
        matrix = np.ascontiguousarray(np.column_stack([x[valid], b[valid].astype(np.float32)]), dtype=np.float32)
        raw = zero.copy()
        raw[valid] += model.predict(matrix, num_threads=4)
        del x, matrix
        final = rebuild_post(frame, raw)
        close_arrays(rebuild_post(frame, zero), frame["pred"].to_numpy(), "actual zero correction equals r4", 0.)
        prediction = canonical(pl.read_parquet(OUT / f"predictions_residual_{year}.parquet"))
        original_columns = [c for c in frame.columns if c not in ("pred", "pred_raw")]
        if not frame.select(original_columns).equals(prediction.select(original_columns)):
            raise AssertionError("Candidate changed original labels/features/keys/pooled auxiliary")
        for column, values in (("b", b), ("calibrated_base", zero), ("residual_raw", raw - zero), ("pred_raw", raw), ("pred", final)):
            maxima["raw_and_post"] = max(maxima["raw_and_post"], close_arrays(values, prediction[column].to_numpy(), f"prediction/{year}/{column}"))
        mechanism_rows = mechanism_daily(frame, raw, zero)
        recorded_daily = pl.read_csv(OUT / f"mechanism_daily_{year}.csv")
        if mechanism_rows.columns != recorded_daily.columns:
            raise AssertionError("Mechanism daily fields differ")
        maxima["mechanism"] = max(maxima["mechanism"], close_arrays(mechanism_rows.to_numpy(), recorded_daily.to_numpy(), "mechanism daily"))
        mechanism = mechanism_summary(mechanism_rows)
        maxima["mechanism"] = max(maxima["mechanism"], match(mechanism, fold["mechanism"], "mechanism summary"))
        mechanism_rows.write_csv(output / f"{stage}_mechanism_{year}.csv", float_precision=17)
        independent_fold = {"year": year, "mechanism": mechanism, "references": {}}
        checks[str(year)] = {"original_float64_training_targets_verified": True, "global_next_date_strict_purge": True,
            "date_balanced_calibration_and_mean1_tree_weights_verified": True, "training_matrix_sha256": feature_digest.hexdigest(),
            "model_reloaded_without_refit": True, "actual_zero_post_exact_r4": True, "raw_and_post_verified": True}
        for name in (PRIMARY, *REFERENCES):
            path = OUT / f"predictions_residual_{year}.parquet" if name == PRIMARY else R4 / f"predictions_{name}_{year}.parquet"
            metrics, daily, details = independent_official_score(path, year)
            expected = fold["metrics"] if name == PRIMARY else fold["references"][name]
            maxima["official_metrics"] = max(maxima["official_metrics"], match(metrics, expected, f"official/{year}/{name}"))
            runner_daily = pl.read_csv(OUT / f"daily_{'residual' if name == PRIMARY else name}_{year}.csv")
            if daily.columns != runner_daily.columns:
                raise AssertionError("Official daily columns differ")
            maxima["daily_official"] = max(maxima["daily_official"], close_arrays(daily.to_numpy(), runner_daily.to_numpy(), f"official daily/{year}/{name}"))
            daily.write_csv(output / f"{stage}_official_{name}_{year}.csv", float_precision=17)
            daily_evidence[name][year] = daily
            checks[str(year)][name] = details
            if name == PRIMARY:
                independent_fold["metrics"] = metrics
            else:
                independent_fold["references"][name] = metrics
        audited.append(independent_fold)
        print(json.dumps({"independent_fold_completed": year}), flush=True)
    official, mechanism = official_and_mechanism_gates(audited, stage)
    bootstrap = None
    if official["passed"] and mechanism["passed"]:
        bootstrap = {name: paired_block_bootstrap(daily_evidence[PRIMARY], daily_evidence[name],
            block_days=20, draws=20000, seed=2026) for name in REFERENCES}
    match(bootstrap, record["bootstrap"], "independent bootstrap")
    passed = stage_pass(record, official, mechanism, stage)
    # Fail if any frozen input, source, stage or fold changed during the audit.
    # The final decision binds the same bytes that were actually evaluated.
    check_hashes(ROOT, artifacts)
    for path in output.glob(f"{stage}_*.csv"):
        artifacts[path.relative_to(ROOT).as_posix()] = sha(path)
    result = {"status": "passed", "status_meaning": "Independent evidence agreement, not candidate qualification",
        "stage": stage, "candidate_key": PRIMARY, "years": list(YEARS[stage]), "stage_gate_passed": passed,
        "stage_record_sha256": stage_digest, "protocol_sha256": protocol_sha,
        "source_sha256": sha(Path(__file__)), "gate": official, "mechanism_gate": mechanism,
        "bootstrap": bootstrap, "folds": audited, "checks": checks, "max_absolute_difference": maxima,
        "artifacts_sha256": artifacts, "historical_years_previously_viewed": True, "automatic_publication": False,
        "limitation": "Independent targets/calibration/weights/matrix and saved-model inference checked; tree fitting is not repeated. Historical research-selection bias is not corrected."}
    with destination.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2, allow_nan=False)
    return result


def synthetic_tests() -> dict:
    frame = pl.DataFrame({"ts_code": ["a", "b", "c", "d"] * 2,
        "trade_date": [20201230] * 4 + [20201231] * 4,
        "price_valid": [True, True, True, False] * 2,
        "pred_raw": [1., 1., 3., np.nan, 3., 1., 2., np.nan],
        "y_ret_1d": [.1, None, .3, .5, .3, .1, .2, None]})
    b, u, target = rank_inputs(frame)
    np.testing.assert_array_equal(b, [.5, .5, 1., np.nan, 1., 1/3, 2/3, np.nan])
    np.testing.assert_array_equal(u, [.5, np.nan, 1., np.nan, 1., 1/3, 2/3, np.nan])
    changed = frame.with_columns(pl.lit(None, dtype=pl.Float64).alias("y_ret_1d"))
    np.testing.assert_array_equal(rank_inputs(changed)[0], b)
    checks = {"b_full_price_pool_u_same_labeled_pool_average_ties": True,
              "b_independent_of_labels_and_missingness": True}
    calendar = np.array([20201230, 20201231, 20210104])
    available = label_available_dates(frame["trade_date"].to_numpy(), calendar)
    np.testing.assert_array_equal(available, [20201231] * 4 + [20210104] * 4)
    np.testing.assert_array_equal(label_available_dates(np.array([20210104]), calendar), [-1])
    rows, fit = independent_training_rows([frame], calendar, 20210104)
    assert len(rows) == 2 and rows["trade_date"].unique().to_list() == [20201230]
    assert rows["label_available_date"].max() < 20210104
    checks["global_next_market_date_strict_purge_unknown_date_rejected"] = True
    dates = np.array([1, 1, 2, 2, 2, 2])
    x = np.array([0., 1., 0., .25, .5, 1.])
    y = .2 + .4 * x
    w = date_balanced_weights(dates)
    np.testing.assert_array_equal(w, [1.5, 1.5, .75, .75, .75, .75])
    assert w.mean() == 1. and w[:2].sum() == w[2:].sum()
    fit = calibration(x, y, dates)
    close_arrays([fit["intercept"], fit["slope"]], [.2, .4], "hand weighted calibration")
    for scale in (1., 1/len(x)):
        design = np.column_stack([np.ones(len(x)), x])
        expected = np.linalg.lstsq(design * np.sqrt(w * scale)[:, None], y * np.sqrt(w * scale), rcond=None)[0]
        close_arrays([fit["intercept"], fit["slope"]], expected, "weight-scale WLS equivalence")
    checks["date_equal_mass_tree_mean1_and_wls_scale_invariance"] = True
    for bad in ((x, -x, dates), (np.ones(6), y, dates)):
        try:
            calibration(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError("Invalid calibration accepted")
    try:
        require_monotonic(np.array([0., 1.]), np.array([1e20, 1e20]))
    except AssertionError:
        pass
    else:
        raise AssertionError("Float64 collapsed ranks accepted")
    require_monotonic(np.array([1., 1., 2.]), np.array([.3, .3, .4]))
    checks["positive_slope_strict_float64_monotonicity_and_exact_ties"] = True
    toy = pl.DataFrame({"trade_date": [1, 2], "n_target": [2, 7], "mse_zero": [1., 9.],
        "mse_candidate": [.5, 8.5], "raw_rank_ic_zero": [.1, .2], "raw_rank_ic_candidate": [.2, .3]})
    summary = mechanism_summary(toy)
    close_arrays([summary["relative_daily_mse_improvement"]], [.1], "ratio of date means")
    assert abs(summary["relative_daily_mse_improvement"] - np.mean([.5, 1 - 8.5 / 9.])) > .1
    checks["mse_improvement_ratio_of_daily_means_not_mean_ratios"] = True
    matrix = np.arange(640, dtype=np.float32).reshape(10, 64)
    digest = hashlib.sha256(f"float32|{matrix.shape}|".encode("ascii"))
    for block in (matrix[:3], matrix[3:8], matrix[8:]):
        digest.update(memoryview(np.ascontiguousarray(block)).cast("B"))
    assert digest.hexdigest() == array_sha(matrix)
    assert array_sha(matrix.astype(np.float64)) != array_sha(matrix)
    checks["streamed_feature_sha_preserves_dtype_shape_and_c_order"] = True
    fold = {"year": 2022, "metrics": {"final_score": .001, "ic_mean": -.002},
        "references": {name: {"final_score": 0., "ic_mean": 0.} for name in REFERENCES},
        "mechanism": {"relative_daily_mse_improvement": .001, "mean_raw_rank_ic_delta": 0.}}
    official, mechanistic = official_and_mechanism_gates([fold], "development")
    assert official["passed"] and mechanistic["passed"]
    bootstrap = {name: {"block_days": 20, "draws": 20000, "seed": 2026, "years": [2022],
                        "bootstrap_share_positive": .8} for name in REFERENCES}
    record = {"gate": official, "mechanism_gate": mechanistic, "point_gate_passed": True,
              "bootstrap": bootstrap, "development_gate_passed": True}
    assert stage_pass(record, official, mechanistic, "development")
    bootstrap["baseline"]["bootstrap_share_positive"] = float(np.nextafter(.8, 0.))
    record["development_gate_passed"] = False
    assert not stage_pass(record, official, mechanistic, "development")
    fold["mechanism"]["relative_daily_mse_improvement"] = .001 - 1e-12
    official, mechanistic = official_and_mechanism_gates([fold], "development")
    record.update(gate=official, mechanism_gate=mechanistic, point_gate_passed=False, bootstrap=None)
    assert official["passed"] and not mechanistic["passed"]
    assert not stage_pass(record, official, mechanistic, "development")
    with patch.dict(globals(), checked_stage=lambda *a: (record, [fold], {}),
                    read=lambda *a: (_ for _ in ()).throw(AssertionError("Should not read independent audit after failure"))):
        try:
            authorize_confirmation("synthetic")
        except ValueError:
            pass
        else:
            raise AssertionError("Failed development authorized confirmation")
    checks["development_requires_both_official_and_mechanism_before_bootstrap"] = True
    checks["failed_development_blocks_confirmation_before_audit_reads"] = True
    fold["mechanism"]["relative_daily_mse_improvement"] = .002
    official, mechanistic = official_and_mechanism_gates([fold], "development")
    bootstrap["baseline"]["bootstrap_share_positive"] = .8
    record.update(gate=official, mechanism_gate=mechanistic, point_gate_passed=True,
                  bootstrap=bootstrap, development_gate_passed=True)
    bad_audit = {"status": "passed", "stage_gate_passed": True, "stage": "development", "candidate_key": PRIMARY,
                 "years": [2022], "stage_record_sha256": "unchanged",
                 "protocol_sha256": "synthetic", "source_sha256": "changed"}
    with patch.dict(globals(), checked_stage=lambda *a: (record, [fold], {}), read=lambda *a: bad_audit,
                    sha=lambda *a: "unchanged"):
        try:
            authorize_confirmation("synthetic")
        except AssertionError:
            pass
        else:
            raise AssertionError("Changed development auditor authorized confirmation")
    checks["changed_independent_development_binding_blocks_confirmation"] = True
    bootstrap["baseline"]["bootstrap_share_positive"] = float("nan")
    try:
        stage_pass(record, official, mechanistic, "development")
    except AssertionError:
        pass
    else:
        raise AssertionError("NaN bootstrap share accepted")
    bootstrap["baseline"]["bootstrap_share_positive"] = .8
    saved_reference = bootstrap.pop("baseline")
    try:
        stage_pass(record, official, mechanistic, "development")
    except AssertionError:
        pass
    else:
        raise AssertionError("Missing second bootstrap reference accepted")
    bootstrap["baseline"] = saved_reference
    checks["bootstrap_requires_two_references_and_finite_positive_share"] = True
    fold["metrics"]["final_score"] = 0.
    official, mechanistic = official_and_mechanism_gates([fold], "development")
    assert not official["passed"] and mechanistic["passed"]
    record.update(gate=official, mechanism_gate=mechanistic, point_gate_passed=False,
                  bootstrap=None, development_gate_passed=False)
    assert not stage_pass(record, official, mechanistic, "development")
    checks["mechanism_success_cannot_override_official_failure"] = True
    confirm = []
    for year, score, improvement in ((2023, -.003, -.001), (2024, .004, .001)):
        confirm.append({"year": year, "metrics": {"final_score": score, "ic_mean": 0.},
            "references": {name: {"final_score": 0., "ic_mean": 0.} for name in REFERENCES},
            "mechanism": {"relative_daily_mse_improvement": improvement, "mean_raw_rank_ic_delta": 0.}})
    a, m = official_and_mechanism_gates(confirm, "confirmation")
    assert a["passed"] and m["passed"]
    confirm[0]["mechanism"]["relative_daily_mse_improvement"] -= 1e-12
    assert not official_and_mechanism_gates(confirm, "confirmation")[1]["passed"]
    checks["confirmation_equal_year_mean_and_worst_mechanism_boundaries"] = True
    return {"status": "passed", "synthetic_only": True, "historical_data_read": False, "checks": checks}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", nargs="?", choices=list(YEARS))
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()
    if args.test and args.stage:
        parser.error("Synthetic testing and historical audit are separate actions")
    result = synthetic_tests() if args.test or not args.stage else audit(args.stage)
    if args.stage:
        result = {key: result[key] for key in ("status", "stage", "stage_gate_passed", "max_absolute_difference")}
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False), flush=True)
