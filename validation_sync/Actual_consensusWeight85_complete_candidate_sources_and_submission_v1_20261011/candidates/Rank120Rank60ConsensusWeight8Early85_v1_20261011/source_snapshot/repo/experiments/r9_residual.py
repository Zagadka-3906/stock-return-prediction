"""One frozen OOF residual correction with a 2022 development stop gate."""
from __future__ import annotations

import os
for _name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "POLARS_MAX_THREADS"):
    os.environ[_name] = "8"
import argparse
from datetime import datetime
import gc
import hashlib
from pathlib import Path
import sys
import time

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import lightgbm as lgb
import numpy as np
import polars as pl
import scipy
from scipy.stats import spearmanr

from experiments.r8_diagnose_and_speed import sha, read, write_new, save_frame, hash_map, verify_map, log
from experiments.r8_fast_official import PreparedOfficialPanel
from experiments.audit_r5_candidate import paired_block_bootstrap
from experiments import r9_residual_core as core

OUT = ROOT / "experiments/r9_residual_20260926"
R4 = ROOT / "experiments/revalidation_20260926/validation"
R8 = ROOT / "experiments/r8_diagnostics_20260926"
KEYS = ["ts_code", "trade_date"]
PRIMARY = "oof_residual"
DEVELOPMENT, CONFIRMATION = (2022,), (2023, 2024)
GATES = {
    "development": {"mean_score_delta_min": .001, "mean_ic_delta_min": -.002},
    "confirmation": {"mean_score_delta_min": .0005, "worst_year_score_delta_min": -.003, "mean_ic_delta_min": -.002},
    "mechanism_development": {"relative_daily_mse_improvement_min": .001, "mean_raw_rank_ic_delta_min": 0.},
    "mechanism_confirmation": {"mean_relative_daily_mse_improvement_min": 0.,
                               "worst_year_relative_daily_mse_improvement_min": -.001,
                               "mean_raw_rank_ic_delta_min": 0.},
    "bootstrap": {"block_days": 20, "draws": 20000, "seed": 2026, "positive_share_min": .8},
}
SOURCE_NAMES = ("r9_residual.py", "r9_residual_core.py", "r9_residual_audit.py", "r9_research_notes_20260926.md")
DEPENDENCIES = ("evaluate.py", "src/scoring.py", "run.py", "src/features.py",
    "experiments/cached_recheck.py", "experiments/r8_fast_official.py",
    "experiments/r8_diagnose_and_speed.py", "experiments/audit_r5_candidate.py",
    "experiments/r7_complement_audit.py", "experiments/r6_transformer_audit.py",
    "experiments/official_seed_development.py")


def calendar():
    return (pl.scan_parquet(ROOT / "data/features.parquet").filter(pl.col("is_train"))
            .select("trade_date").unique().sort("trade_date").collect()["trade_date"].to_numpy())


def mature_mask(signal_dates, market_dates, validation_first):
    """One-day Y[t] becomes known on the next full-market date, strictly before prediction."""
    signal_dates = np.asarray(signal_dates)
    market_dates = np.asarray(market_dates)
    if (market_dates.ndim != 1 or len(market_dates) < 2 or np.any(np.diff(market_dates) <= 0)):
        raise ValueError("Strictly increasing full-market calendar required")
    positions = np.searchsorted(market_dates, signal_dates)
    if np.any(positions >= len(market_dates)) or not np.array_equal(market_dates[positions], signal_dates):
        raise ValueError("Signal date missing from full-market calendar")
    available = np.full(len(signal_dates), -1, dtype=np.int64)
    known = positions + 1 < len(market_dates)
    available[known] = market_dates[positions[known] + 1]
    return known & (available < validation_first), available


def array_sha(values):
    array = np.ascontiguousarray(values)
    digest = hashlib.sha256(f"{array.dtype}|{array.shape}|".encode("ascii"))
    digest.update(memoryview(array).cast("B"))
    return digest.hexdigest()


def feature_names():
    names = read(ROOT / "data/feature_manifest.json")["features"]
    if len(names) != 63 or len(set(names)) != 63:
        raise AssertionError("Expected original fixed 63 features")
    return names


def load_year(year):
    frame = pl.read_parquet(R4 / f"predictions_ensemble4_{year}.parquet").sort("trade_date", "ts_code")
    if frame["y_ret_1d"].dtype != pl.Float64 or not np.all(frame["trade_date"].to_numpy() // 10000 == year):
        raise AssertionError("Wrong year or label precision")
    provenance = read(R4 / f"result_{year}.json")
    bounds = provenance["boundaries"]
    if not (bounds["one_day_label_available"] < bounds["validation_first"]
            and bounds["two_day_label_available"] < bounds["validation_first"]):
        raise AssertionError("R4 source model used immature labels")
    return frame


def load_features(frame):
    names = feature_names()
    # Never select the Float32 feature-cache label or its precomputed y_rank.
    dates = frame["trade_date"].unique().to_list()
    feature = (pl.scan_parquet(ROOT / "data/features.parquet")
        .filter(pl.col("is_train") & pl.col("trade_date").is_in(dates))
        .select(KEYS + ["price_valid"] + names).sort("trade_date", "ts_code").collect())
    if not frame.select(KEYS + ["price_valid"]).equals(feature.select(KEYS + ["price_valid"])):
        raise AssertionError("Full feature keys or price-valid flags differ from OOF frame")
    if not np.array_equal(frame["flag_limit_up"].to_numpy(), feature["flag_limit_up"].to_numpy()):
        raise AssertionError("OOF and feature limit flags differ")
    x = np.ascontiguousarray(feature.select(names).to_numpy(), dtype=np.float32)
    if np.isinf(x).any():
        raise AssertionError("Infinite feature; no post-result imputation rule is permitted")
    return x


def training_frame(year, market_dates):
    train_years = list(range(2020, year))
    validation_first = int(market_dates[np.searchsorted(market_dates, year * 10000 + 101)])
    full = pl.concat([load_year(y) for y in train_years], how="vertical_relaxed").sort("trade_date", "ts_code")
    keep, available = mature_mask(full["trade_date"].to_numpy(), market_dates, validation_first)
    frame = full.filter(pl.Series(keep))
    if frame.is_empty() or not np.all(frame["trade_date"].to_numpy() < validation_first):
        raise AssertionError("Empty or nonhistorical training frame")
    boundaries = {"validation_first": validation_first, "first_training_signal": int(frame["trade_date"].min()),
        "last_training_signal": int(frame["trade_date"].max()), "last_label_available": int(available[keep].max()),
        "purged_signal_dates": sorted(map(int, np.unique(full["trade_date"].to_numpy()[~keep]))),
        "purged_panel_rows": int((~keep).sum()), "retained_panel_rows": frame.height,
        "training_oof_years": train_years, "strict_next_market_date_before_validation": True,
        "no_post_validation_training": True, "additional_post_test_embargo": "Not applicable: expanding past-only training; no future training segment."}
    assert boundaries["last_label_available"] < validation_first
    return frame, boundaries


def mechanism(frame, calibrated, raw):
    target = core.target_percentile(frame)
    dates = frame["trade_date"].to_numpy()
    rows = []
    for date in np.unique(dates):
        mask = (dates == date) & np.isfinite(target)
        if mask.sum() < 30:
            raise AssertionError("Too few measured labels in a validation date")
        rows.append({"trade_date": int(date), "n_target": int(mask.sum()),
            "mse_zero": float(np.mean((target[mask] - calibrated[mask]) ** 2)),
            "mse_candidate": float(np.mean((target[mask] - raw[mask]) ** 2)),
            "raw_rank_ic_zero": float(spearmanr(calibrated[mask], target[mask]).statistic),
            "raw_rank_ic_candidate": float(spearmanr(raw[mask], target[mask]).statistic)})
    daily = pl.DataFrame(rows)
    zero, candidate = float(daily["mse_zero"].mean()), float(daily["mse_candidate"].mean())
    result = {"days": len(rows), "mse_zero": zero, "mse_candidate": candidate,
              "relative_daily_mse_improvement": 1 - candidate / zero,
              "raw_rank_ic_zero": float(daily["raw_rank_ic_zero"].mean()),
              "raw_rank_ic_candidate": float(daily["raw_rank_ic_candidate"].mean())}
    result["mean_raw_rank_ic_delta"] = result["raw_rank_ic_candidate"] - result["raw_rank_ic_zero"]
    if not all(np.isfinite(value) for value in result.values()):
        raise AssertionError("Undefined mechanism measure")
    return result, daily


def point_gate(folds, stage):
    expected = DEVELOPMENT if stage == "development" else CONFIRMATION
    if tuple(f["year"] for f in folds) != expected:
        raise AssertionError("Incomplete, reordered or unexpected stage years")
    thresholds = GATES[stage]
    comparisons = {}
    for reference in ("ensemble4", "baseline"):
        delta = np.array([f["metrics"]["final_score"] - f["references"][reference]["final_score"] for f in folds])
        ic = np.array([f["metrics"]["ic_mean"] - f["references"][reference]["ic_mean"] for f in folds])
        passed = delta.mean() >= thresholds["mean_score_delta_min"] and ic.mean() >= thresholds["mean_ic_delta_min"]
        if "worst_year_score_delta_min" in thresholds:
            passed &= delta.min() >= thresholds["worst_year_score_delta_min"]
        comparisons[reference] = {"score_deltas": dict(zip(map(str, expected), map(float, delta))),
            "mean_score_delta": float(delta.mean()), "worst_year_score_delta": float(delta.min()),
            "mean_ic_delta": float(ic.mean()), "passed": bool(passed)}
    improvement = np.array([f["mechanism"]["relative_daily_mse_improvement"] for f in folds])
    raw_ic = np.array([f["mechanism"]["mean_raw_rank_ic_delta"] for f in folds])
    if stage == "development":
        threshold = GATES["mechanism_development"]
        passed = improvement[0] >= threshold["relative_daily_mse_improvement_min"] and raw_ic.mean() >= threshold["mean_raw_rank_ic_delta_min"]
    else:
        threshold = GATES["mechanism_confirmation"]
        passed = (improvement.mean() >= threshold["mean_relative_daily_mse_improvement_min"]
            and improvement.min() >= threshold["worst_year_relative_daily_mse_improvement_min"]
            and raw_ic.mean() >= threshold["mean_raw_rank_ic_delta_min"])
    official = {"comparisons": comparisons, "passed": all(v["passed"] for v in comparisons.values())}
    mechanistic = {"relative_mse_by_year": dict(zip(map(str, expected), map(float, improvement))),
        "mean_relative_daily_mse_improvement": float(improvement.mean()),
        "worst_year_relative_daily_mse_improvement": float(improvement.min()),
        "mean_raw_rank_ic_delta": float(raw_ic.mean()), "passed": bool(passed)}
    return official, mechanistic


def synthetic_tests():
    from unittest.mock import patch
    dates = np.array([20201230, 20201231, 20210104, 20210105, 20210106])
    signals = np.repeat(dates, 2)
    keep, available = mature_mask(signals, dates, 20210104)
    np.testing.assert_array_equal(keep, [True, True] + [False] * 8)
    assert set(available[keep]) == {20201231}
    # A label realized exactly on the prediction date is rejected.
    assert not keep[signals == 20201231].any()
    try:
        mature_mask([20210103], dates, 20210105)
    except ValueError:
        pass
    else:
        raise AssertionError("Compressed/missing market dates accepted")
    fold = {"year": 2022, "metrics": {"final_score": .5, "ic_mean": .15},
        "references": {name: {"final_score": .49, "ic_mean": .15} for name in ("ensemble4", "baseline")},
        "mechanism": {"relative_daily_mse_improvement": .002, "mean_raw_rank_ic_delta": .001}}
    a, b = point_gate([fold], "development")
    assert a["passed"] and b["passed"]
    fold["mechanism"]["relative_daily_mse_improvement"] = -.001
    assert not point_gate([fold], "development")[1]["passed"]
    fold["references"]["ensemble4"]["final_score"] = .5
    assert not point_gate([fold], "development")[0]["passed"]
    with patch(__name__ + ".sha", return_value="protocol"):
        malformed = {"year": 2022, "candidate_key": PRIMARY, "protocol_sha256": "protocol",
                     "train_years": [2020, 2021], "artifact_sha256": {}}
        try:
            check_fold(malformed, 2022)
        except AssertionError:
            pass
        else:
            raise AssertionError("An empty completed-fold manifest was accepted")
    failed = {"stage": "development", "candidate_key": PRIMARY, "years": [2022],
              "development_gate_passed": False, "point_gate_passed": False}
    with patch(__name__ + ".verify_protocol"), patch(__name__ + ".read", return_value=failed) as reader:
        try:
            confirmation_guard()
        except RuntimeError:
            pass
        else:
            raise AssertionError("Failed development allowed confirmation")
        assert reader.call_count == 1
    return {"status": "passed", "strict_label_maturity": True, "global_calendar_required": True,
            "official_and_mechanism_gates_both_required": True, "empty_fold_rejected": True,
            "failed_development_stops_before_confirmation_access": True, "historical_data_read": False}


def freeze():
    if (OUT / "protocol.json").exists():
        raise FileExistsError("Frozen experiment already exists")
    from experiments import r9_residual_audit
    from experiments.r8_diagnose_and_speed import verify as verify_previous
    tests = {"core": core.synthetic_tests(), "runner": synthetic_tests(), "audit": r9_residual_audit.synthetic_tests()}
    assert all(v["status"] == "passed" for v in tests.values())
    previous = verify_previous()
    inputs = [ROOT / "active_release.json", ROOT / "data/features.parquet", ROOT / "data/feature_manifest.json",
        ROOT / "data" / "raw" / "训练集.csv", ROOT / "releases/ensemble4_r4/release_manifest.json",
        R8 / "result_manifest.json", R4 / "protocol.json", R4 / "summary.json"]
    inputs += [ROOT / name for name in DEPENDENCIES]
    for year in range(2020, 2025):
        inputs += [R4 / f"result_{year}.json", R4 / f"predictions_ensemble4_{year}.parquet",
                   R4 / f"predictions_baseline_{year}.parquet"]
    write_new(OUT / "tests.json", tests)
    inputs.append(OUT / "tests.json")
    protocol = {"experiment": "fixed_oof_conditional_rank_residual", "primary_candidate": PRIMARY,
        "frozen_at_local": datetime.now().astimezone().isoformat(), "candidate_count": 1,
        "development_years": list(DEVELOPMENT), "confirmation_years": list(CONFIRMATION),
        "training_years": {str(year): list(range(2020, year)) for year in (*DEVELOPMENT, *CONFIRMATION)},
        "feature_names": feature_names(), "params": core.PARAMS, "rounds": core.ROUNDS,
        "gates": GATES, "weights": "Calibrator sum1=1/(D*n_day); residual LightGBM mean1=N/(D*n_day), counts after purge and finite-label filtering.",
        "calibration": "Positive-slope date-balanced WLS on price-valid rank b and finite-label target rank u. No clipping of slope. Actual zero residual m(b) must preserve ranks and the entire R4 postprocessor exactly.",
        "target": "Original Float64 label is ranked within same date price_valid & finite-Y pool, including limit-up stocks. Predictor b ranks the FULL current price_valid pool without reading Y or Y availability.",
        "prediction": "m(b)+LightGBM residual in a shared target-rank unit; never rank the residual alone, fit a blend weight, or use init_score. Invalid raw=-10. Existing .9 EMA/.3 retention/.25 pooled postprocessing remains fixed.",
        "time_boundary": "Train only previous years' corrected R4 OOF. Use full market calendar; Y availability=next market date, strictly before first prediction date. Remove entire final immature date. No training after validation and no post-test embargo segment.",
        "stage_order": "2022 full mechanism and official point checks; bootstrap only if both pass; independent audit required before any 2023/24 training/inference. Confirmation refits on prior OOF years with identical recipe. No model or weight selection after results.",
        "historical_years_previously_viewed": True, "hypothesis_after_r8": True,
        "limitations": "Repeated history, not a blind test. Bootstrap positive share is an engineering gate, not alpha probability or research-selection correction. No automatic release, competition upload or trading.",
        "source_sha256": hash_map([ROOT / "experiments" / name for name in SOURCE_NAMES]),
        "input_sha256": hash_map(inputs), "previous_r8_verification": previous,
        "versions": {"python": sys.version, "numpy": np.__version__, "polars": pl.__version__, "scipy": scipy.__version__, "lightgbm": lgb.__version__}}
    write_new(OUT / "protocol.json", protocol)
    return {"status": "frozen", "protocol_sha256": sha(OUT / "protocol.json")}


def verify_protocol():
    protocol = read(OUT / "protocol.json")
    verify_map(protocol["source_sha256"])
    verify_map(protocol["input_sha256"])
    if protocol["gates"] != GATES or protocol["params"] != core.PARAMS or protocol["rounds"] != core.ROUNDS:
        raise AssertionError("Frozen configuration differs")
    return protocol


def check_fold(record, year):
    if record["year"] != year or record["candidate_key"] != PRIMARY or record["protocol_sha256"] != sha(OUT / "protocol.json"):
        raise AssertionError("Fold identity differs")
    if set(record["artifact_sha256"]) != set(required_artifacts(year)) or record["train_years"] != list(range(2020, year)):
        raise AssertionError("Missing/extra fold artifacts or wrong OOF years")
    verify_map({f"experiments/r9_residual_20260926/{name}": digest for name, digest in record["artifact_sha256"].items()})
    return record


def confirmation_guard():
    verify_protocol()
    development = read(OUT / "development.json")
    if development["stage"] != "development" or development["candidate_key"] != PRIMARY or development["years"] != list(DEVELOPMENT):
        raise AssertionError("Wrong development identity")
    if not development["development_gate_passed"] or not development["point_gate_passed"]:
        raise RuntimeError("Development failed; confirmation is forbidden")
    if development["protocol_sha256"] != sha(OUT / "protocol.json"):
        raise AssertionError("Development belongs to another protocol")
    if set(development["fold_sha256"]) != {"fold_2022.json"}:
        raise AssertionError("Wrong development folds")
    if development["fold_sha256"]["fold_2022.json"] != sha(OUT / "fold_2022.json"):
        raise AssertionError("Development fold changed")
    fold = check_fold(read(OUT / "fold_2022.json"), 2022)
    official, mechanistic = point_gate([fold], "development")
    if (official != development["gate"] or mechanistic != development["mechanism_gate"]
            or not official["passed"] or not mechanistic["passed"]):
        raise AssertionError("Development gate does not follow the verified fold")
    if not isinstance(development["bootstrap"], dict) or set(development["bootstrap"]) != {"ensemble4", "baseline"}:
        raise AssertionError("Both bootstrap references required")
    for name in ("ensemble4", "baseline"):
        bootstrap = development["bootstrap"][name]
        share = bootstrap["bootstrap_share_positive"]
        if (bootstrap["block_days"], bootstrap["draws"], bootstrap["seed"]) != (20, 20000, 2026) or not np.isfinite(share) or not .8 <= share <= 1 or bootstrap["years"] != [2022]:
            raise RuntimeError("Development bootstrap gate failed")
    audit_path = OUT / "independent_audit/audit_development.json"
    audit = read(audit_path)
    if (audit.get("stage") != "development" or audit.get("candidate_key") != PRIMARY
            or audit.get("years") != [2022] or audit.get("protocol_sha256") != sha(OUT / "protocol.json")):
        raise AssertionError("Independent audit identity differs")
    if audit["status"] != "passed" or not audit["stage_gate_passed"] or audit["stage_record_sha256"] != sha(OUT / "development.json"):
        raise RuntimeError("Independent development audit required")
    required = {f"experiments/r9_residual_20260926/{name}" for name in ["development.json", "fold_2022.json", *required_artifacts(2022)]}
    if not required <= set(audit["artifacts_sha256"]):
        raise AssertionError("Independent audit omits development evidence")
    verify_map(audit["artifacts_sha256"])
    return development


def required_artifacts(year):
    return [f"{name}_{year}.{suffix}" for name, suffix in
        (("training_rows", "parquet"), ("calibration", "json"), ("model", "txt"),
         ("predictions_residual", "parquet"), ("mechanism_daily", "csv"),
         ("daily_residual", "csv"), ("daily_ensemble4", "csv"), ("daily_baseline", "csv"))]


def train_and_score(year, market_dates):
    if year not in (*DEVELOPMENT, *CONFIRMATION):
        raise ValueError("Unplanned fold")
    if year in CONFIRMATION:
        confirmation_guard()
    existing = OUT / f"fold_{year}.json"
    if existing.exists():
        return check_fold(read(existing), year)
    if any(OUT.glob(f"*_{year}.*")):
        raise FileExistsError("Incomplete fold artifacts preserved; do not overwrite them")
    started = time.monotonic()
    train, boundaries = training_frame(year, market_dates)
    x = load_features(train)
    log(f"{year}: training on OOF {boundaries['training_oof_years']}, {train.height:,} panel rows")
    booster, calibration = core.fit(train, x, feature_names())
    b, target = core.base_percentile(train), core.target_percentile(train)
    mask = np.isfinite(target)
    weights = core.date_weights(train, mask)
    calibrated = calibration["intercept"] + calibration["slope"] * b
    matrix = core.make_matrix(x, b)
    training = {"rows": int(mask.sum()), "dates": int(train.filter(pl.Series(mask))["trade_date"].n_unique()),
        "feature_matrix_sha256": array_sha(matrix[mask]), "feature_matrix_dtype": str(matrix.dtype),
        "target_residual_sha256": array_sha((target - calibrated)[mask]),
        "weight_sha256": array_sha(weights[mask]), "mean_weight": float(weights[mask].mean()),
        "model_feature_names": booster.feature_name(), "feature_cache_labels_never_used": True}
    evidence = train.select(KEYS).with_columns(pl.Series("b", b), pl.Series("target_u", target),
        pl.Series("calibrated_base", calibrated), pl.Series("residual_target", target - calibrated),
        pl.Series("weight", weights)).filter(pl.Series(mask))
    save_frame(OUT / f"training_rows_{year}.parquet", evidence)
    write_new(OUT / f"calibration_{year}.json", calibration)
    write_new(OUT / f"model_{year}.txt", booster.model_to_string())
    reloaded = lgb.Booster(model_str=(OUT / f"model_{year}.txt").read_text(encoding="utf-8"))
    del train, x, b, target, mask, weights, calibrated, matrix, evidence
    gc.collect()
    frame = load_year(year)
    x = load_features(frame)
    b = core.base_percentile(frame)
    zero_raw = core.predict_raw(frame, x, None, calibration)
    zero_final = core.prediction(frame, x, None, calibration)
    np.testing.assert_array_equal(zero_final, frame["pred"].to_numpy(), err_msg="Zero residual changed R4")
    raw = core.predict_raw(frame, x, booster, calibration)
    np.testing.assert_array_equal(raw, core.predict_raw(frame, x, reloaded, calibration), err_msg="Model reload changed raw")
    pred = core.prediction(frame, x, booster, calibration)
    poisoned = frame.with_columns(pl.lit(-98765.).alias("y_ret_1d"), pl.lit(False).alias("future_available"))
    np.testing.assert_array_equal(pred, core.prediction(poisoned, x, booster, calibration), err_msg="Prediction reads labels")
    prefix = 50 * frame["ts_code"].n_unique()
    np.testing.assert_array_equal(pred[:prefix], core.prediction(frame.head(prefix), x[:prefix], booster, calibration), err_msg="Future observations changed prefix")
    if not np.isfinite(pred).all() or not (pred[~frame["price_valid"].to_numpy()] < -1).all():
        raise AssertionError("Final predictions invalid")
    mechanistic, daily_mechanism = mechanism(frame, zero_raw, raw)
    output = frame.with_columns(pl.Series("b", b), pl.Series("calibrated_base", zero_raw),
        pl.Series("residual_raw", raw - zero_raw), pl.Series("pred_raw", raw), pl.Series("pred", pred))
    save_frame(OUT / f"predictions_residual_{year}.parquet", output)
    save_frame(OUT / f"mechanism_daily_{year}.csv", daily_mechanism)
    context = PreparedOfficialPanel.from_frame(frame)
    metrics, daily = context.score(pred)
    save_frame(OUT / f"daily_residual_{year}.csv", daily)
    references = {}
    old_metrics = read(R4 / f"result_{year}.json")["metrics"]
    for name in ("ensemble4", "baseline"):
        reference = frame if name == "ensemble4" else pl.read_parquet(R4 / f"predictions_{name}_{year}.parquet").sort("trade_date", "ts_code")
        if not frame.select(KEYS).equals(reference.select(KEYS)):
            raise AssertionError("Reference keys differ")
        references[name], daily = context.score(reference["pred"].to_numpy())
        assert all(abs(references[name][key] - value) <= 1e-12 for key, value in old_metrics[name].items())
        save_frame(OUT / f"daily_{name}_{year}.csv", daily)
    artifacts = required_artifacts(year)
    record = {"year": year, "candidate_key": PRIMARY, "protocol_sha256": sha(OUT / "protocol.json"),
        "train_years": list(range(2020, year)), "boundaries": boundaries, "training": training,
        "metrics": metrics, "references": references, "mechanism": mechanistic,
        "tests": {"actual_zero_calibration_exact_r4": True, "model_reload_exact": True,
                  "label_and_availability_invariance": True, "prefix_50days_exact": True,
                  "finite_and_invalid_price_excluded": True},
        "artifact_sha256": {name: sha(OUT / name) for name in artifacts},
        "elapsed_seconds": time.monotonic() - started}
    write_new(existing, record)
    log(f"{year}: score={metrics['final_score']:.9f}; delta R4={metrics['final_score']-references['ensemble4']['final_score']:+.9f}; relative MSE improvement={mechanistic['relative_daily_mse_improvement']:.6%}")
    return record


def stage(name):
    verify_protocol()
    if name == "confirmation":
        confirmation_guard()
    destination = OUT / f"{name}.json"
    if destination.exists():
        raise FileExistsError("Completed stage preserved")
    years = DEVELOPMENT if name == "development" else CONFIRMATION
    market_dates = calendar()
    folds = [train_and_score(year, market_dates) for year in years]
    official, mechanistic = point_gate(folds, name)
    point_pass = official["passed"] and mechanistic["passed"]
    bootstrap = None
    if point_pass:
        candidates = {year: pl.read_csv(OUT / f"daily_residual_{year}.csv") for year in years}
        bootstrap = {reference: paired_block_bootstrap(candidates,
            {year: pl.read_csv(OUT / f"daily_{reference}_{year}.csv") for year in years},
            block_days=20, draws=20000, seed=2026) for reference in ("ensemble4", "baseline")}
    passed = point_pass and all(v["bootstrap_share_positive"] >= .8 for v in bootstrap.values()) if bootstrap is not None else False
    record = {"stage": name, "candidate_key": PRIMARY, "years": list(years),
        "protocol_sha256": sha(OUT / "protocol.json"), "gate": official, "mechanism_gate": mechanistic,
        "point_gate_passed": bool(point_pass), "bootstrap": bootstrap, f"{name}_gate_passed": bool(passed),
        "fold_sha256": {f"fold_{year}.json": sha(OUT / f"fold_{year}.json") for year in years},
        "historical_years_previously_viewed": True, "formal_promotion": False}
    verify_protocol()
    write_new(destination, record)
    return record


if __name__ == "__main__":
    import json
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("freeze", "development", "confirmation", "verify-inputs", "test"))
    action = parser.parse_args().action
    result = freeze() if action == "freeze" else synthetic_tests() if action == "test" else verify_protocol() if action == "verify-inputs" else stage(action)
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
