"""Reproducible, full-panel audit of the saved prediction workflow.

Run after ``run.py all --rebuild-features --retrain``.  This script never fits a
model or changes submission.csv.  Temporary synthetic/raw-label fixtures are
removed automatically; the only persistent output is prediction_audit.json.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import gc
import hashlib
import json
from pathlib import Path
import sys
import tempfile

import lightgbm as lgb
import numpy as np
import polars as pl

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from evaluate import evaluate  # noqa: E402
from src.features import build_features  # noqa: E402
from src.scoring import Panel, add_top_persistence, make_scores, postprocess_scores, score  # noqa: E402


def log(message: str) -> None:
    print(message, flush=True)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(4 * 1024 * 1024):
            value.update(chunk)
    return value.hexdigest()


def check_feature_prefix() -> dict:
    """Appending future dates/altering labels must not change past features.

    This deliberately uses a synthetic full cross-section (not a subset of the
    real panel, which would change cross-sectional ranks). It tests the actual
    production feature builder, including missing/resumed price observations.
    """
    rng = np.random.default_rng(20260923)
    days = np.arange("2024-01-01", "2024-05-06", dtype="datetime64[D]")
    days = days[np.is_busday(days)][:90]
    dates = [int(str(x).replace("-", "")) for x in days]
    rows = []
    for stock in range(6):
        close = 10.0 + stock * 3
        for i, date in enumerate(dates):
            close *= np.exp(rng.normal(0, 0.018))
            opening = close * np.exp(rng.normal(0, 0.006))
            high, low = max(close, opening) * 1.015, min(close, opening) * 0.985
            volume = float(rng.uniform(1000, 100000))
            missing = stock == 1 and i in (12, 13, 61)
            rows.append((f"S{stock:02d}", date, None if missing else opening,
                         None if missing else high, None if missing else low,
                         None if missing else close, None if missing else volume,
                         None if missing else volume * close, int(i % 17 == 0),
                         int(i % 29 == 0), float(rng.normal(0, 0.02))))
    source = pl.DataFrame(rows, schema=["ts_code", "trade_date", "open", "high",
        "low", "close", "vol", "amount", "flag_limit_up", "flag_limit_down",
        "y_ret_1d"], orient="row")
    with tempfile.TemporaryDirectory(prefix="prediction-prefix-") as temporary:
        root = Path(temporary)
        results = {}
        for name, last_day, perturb_labels in (("full", dates[-1], False),
                                                ("prefix", dates[74], False),
                                                ("changed_labels", dates[-1], True)):
            folder = root / name
            folder.mkdir()
            selected = source.filter(pl.col("trade_date") <= last_day)
            if perturb_labels:
                selected = selected.with_columns((-pl.col("y_ret_1d") * 13 + 7).alias("y_ret_1d"))
            selected.filter(pl.col("trade_date") <= dates[59]).write_csv(folder / "训练集.csv")
            selected.filter(pl.col("trade_date") > dates[59]).drop("y_ret_1d").write_csv(folder / "测试集_X.csv")
            info = build_features(folder, folder / "features.parquet")
            results[name] = pl.read_parquet(folder / "features.parquet").sort("ts_code", "trade_date")
        features = info["features"]
        past = results["full"].filter(pl.col("trade_date") <= dates[74]).select(features).to_numpy()
        shortened = results["prefix"].select(features).to_numpy()
        all_features = results["full"].select(features).to_numpy()
        perturbed = results["changed_labels"].select(features).to_numpy()
        assert np.array_equal(past, shortened, equal_nan=True), "A future row changed a past feature"
        assert np.array_equal(all_features, perturbed, equal_nan=True), "Labels leaked into feature values"
        # Verify the production smoother's own prefix invariance and resumption.
        tiny = pl.DataFrame({"ts_code": ["A", "B", "A", "B", "A", "B"],
            "trade_date": [1, 1, 2, 2, 3, 3], "y_ret_1d": [0.] * 6,
            "flag_limit_up": [0] * 6, "price_valid": [True, False, True, True, True, True]})
        raw = np.array([.2, -1e6, .1, .3, .4, .1])
        full_scores = make_scores(Panel.from_frame(tiny), raw, .95)
        short_scores = make_scores(Panel.from_frame(tiny.head(4)), raw[:4], .95)
        assert np.array_equal(full_scores[:4], short_scores)
        assert full_scores[1] == -10 and full_scores[3] == 1.0
        # Exercise the Top-list state on a large enough synthetic cross-section.
        codes = [f"S{i:03d}" for i in range(120)]
        top_fixture = pl.DataFrame({
            "ts_code": codes * 3,
            "trade_date": [1] * 120 + [2] * 120 + [3] * 120,
            "y_ret_1d": [0.0] * 360,
            "flag_limit_up": [0] * 360,
            "price_valid": [True] * 360,
        })
        top_panel = Panel.from_frame(top_fixture)
        top_base = np.tile(np.linspace(0, 1, 120), 3)
        top_full = add_top_persistence(top_panel, top_base, .05)
        top_prefix = add_top_persistence(Panel.from_frame(top_fixture.head(240)), top_base[:240], .05)
        assert np.array_equal(top_full[:240], top_prefix)
        assert np.count_nonzero(top_full[120:240] != top_base[120:240]) == 12
    return {"status": "passed", "fixture": "synthetic 6-symbol / 90-business-day complete panel",
            "feature_count": len(features), "prefix_rows_compared": len(past),
            "all_rows_label_perturbation_compared": len(all_features),
            "prefix_equal_including_nulls": True, "label_perturbation_invariant": True,
            "smoothing_prefix_invariant": True, "top_persistence_prefix_invariant": True,
            "resumption_reset_passed": True,
            "limitation": "Tests implementation causality; cannot establish point-in-time universe/price-adjustment provenance of organizer data."}


def check_time_boundaries() -> dict:
    frame = pl.scan_parquet(ROOT / "data/features.parquet")
    dates = frame.select("trade_date", "is_train").unique().sort("trade_date").collect()
    train_dates = dates.filter(pl.col("is_train")).get_column("trade_date").to_numpy()
    test_dates = dates.filter(~pl.col("is_train")).get_column("trade_date").to_numpy()
    folds = []
    for year in (2022, 2023, 2024):
        start_index = int(np.searchsorted(train_dates, year * 10000 + 101))
        validation_start = int(train_dates[start_index])
        excluded = int(train_dates[start_index - 1])
        training_end = int(train_dates[start_index - 2])
        assert training_end < excluded < validation_start
        folds.append({"year": year, "training_end": training_end,
                      "purged_date": excluded, "last_training_label_price_date": excluded,
                      "validation_start": validation_start, "non_overlapping": True})
    assert int(train_dates[-1]) < int(test_dates[0])
    return {"status": "passed", "folds": folds,
            "parameter_selection_years": [2022, 2023], "holdout_year": 2024,
            "train_end": int(train_dates[-1]), "test_start": int(test_dates[0]),
            "information_cutoff": "Predictions for date t are generated after that day's close; features include day t, labels concern t+1.",
            "first_test_day_note": "The last supplied training label may use the first test day's close; that close is known at the stated prediction time."}


def check_official_score(alpha: float, bonus: float, recorded: dict, restore_lower: bool = False,
                         top_current_weight: float = 0.0) -> dict:
    fold = pl.read_parquet(ROOT / "validation/fold_2024.parquet").sort("trade_date", "ts_code")
    stored_panel = Panel.from_frame(fold)
    predictions = postprocess_scores(stored_panel, fold.get_column("pred_raw").to_numpy(), alpha, bonus,
                                      restore_lower, top_current_weight)
    # Load original source labels as float64, avoiding irreversible float32 ties.
    original = pl.scan_csv(ROOT / "data" / "raw" / "训练集.csv", schema_overrides={"ts_code": pl.String,
        "trade_date": pl.Int32, "y_ret_1d": pl.Float64}, null_values=["NaN", "nan", ""])
    original = original.filter(pl.col("trade_date").is_between(20240101, 20241231)).select(
        "ts_code", "trade_date", "y_ret_1d").collect()
    exact = fold.drop("y_ret_1d").join(original, on=["ts_code", "trade_date"], how="left", validate="1:1").sort("trade_date", "ts_code")
    exact_panel = Panel.from_frame(exact)
    ours_exact, _ = score(exact_panel, predictions)
    ours_stored, _ = score(stored_panel, predictions)
    keys = exact.select("ts_code", "trade_date")
    with tempfile.TemporaryDirectory(prefix="prediction-official-") as temporary:
        path = Path(temporary)
        keys.with_columns(pl.Series("pred", predictions)).write_csv(path / "submission.csv", float_precision=17)
        keys.with_columns(exact.get_column("y_ret_1d")).write_csv(path / "测试集_Y.csv", float_precision=17)
        keys.with_columns(exact.get_column("flag_limit_up")).write_csv(path / "测试集_X.csv")
        official = {key: float(value) for key, value in evaluate(str(path / "submission.csv"), str(path)).items()}
    differences = {key: abs(ours_exact[key] - value) for key, value in official.items()}
    stored_differences = {key: abs(ours_stored[key] - value) for key, value in official.items()}
    tolerances = {key: (1e-4 if key == "icir" else 1e-5) for key in official}
    tolerances["mean_turnover"] = 1e-12
    tolerances["ic_positive_ratio"] = 1e-12
    for key in official:
        assert differences[key] <= tolerances[key], f"Official scoring mismatch: {key} = {differences[key]}"
        assert stored_differences[key] <= tolerances[key], f"Stored float32 score differs materially: {key}"
        assert abs(ours_stored[key] - recorded[key]) < 1e-12, f"metrics.json is stale: {key}"
    # Show realistic low-complexity baselines without selecting on holdout.
    baselines = {}
    for name in ("ROC5", "MA20"):
        factor_raw = fold.get_column(name).fill_null(-1e6).to_numpy()
        baseline, _ = score(stored_panel, postprocess_scores(stored_panel, factor_raw, alpha, bonus,
                                                            restore_lower, top_current_weight))
        baselines[name] = baseline
    return {"status": "passed", "rows": len(fold), "trading_days": len(stored_panel.dates),
        "label_precision": "Original training CSV labels read as float64 for the official-script comparison.",
        "official_script": "evaluate.py (unmodified organizer script)", "official_metrics": official,
        "independent_scorer_float64_metrics": ours_exact, "stored_float32_metrics": ours_stored,
        "absolute_difference_float64_vs_official": differences,
        "absolute_difference_recorded_vs_official": stored_differences,
        "absolute_tolerances": tolerances, "recorded_metrics_reproduced": True,
        "difference_note": "CSV parser rounding and float32 label storage can change ties in Spearman ranks; all metric deviations must remain within stated tolerances.",
        "holdout_baselines_same_alpha": baselines}


def check_submission(alpha: float, bonus: float, features: list[str], threads: int, restore_lower: bool = False,
                      top_current_weight: float = 0.0) -> dict:
    test_source = pl.read_csv(ROOT / "data" / "raw" / "测试集_X.csv", columns=["ts_code", "trade_date", "close"],
        schema_overrides={"ts_code": pl.String, "trade_date": pl.Int32, "close": pl.Float64},
        null_values=["NaN", "nan", ""])
    submitted = pl.read_csv(ROOT / "outputs/submission.csv", schema_overrides={
        "ts_code": pl.String, "trade_date": pl.Int32, "pred": pl.Float64})
    assert submitted.columns == ["ts_code", "trade_date", "pred"]
    assert len(submitted) == len(test_source)
    for name in ("ts_code", "trade_date"):
        assert np.array_equal(test_source.get_column(name).to_numpy(), submitted.get_column(name).to_numpy())
    assert submitted.select(pl.struct("ts_code", "trade_date").n_unique()).item() == len(submitted)
    values = submitted.get_column("pred").to_numpy()
    assert np.isfinite(values).all()
    invalid = test_source.select((pl.col("close").is_null() | pl.col("close").is_nan() | (pl.col("close") <= 0)).fill_null(True)).to_series().to_numpy()
    assert np.all(values[invalid] == -.05)
    assert np.all(values[~invalid] > -.02) and np.all(values[~invalid] <= .04)
    model = lgb.Booster(model_str=(ROOT / "models/final_lightgbm.txt").read_text(encoding="utf-8"))
    assert model.feature_name() == features
    test = pl.scan_parquet(ROOT / "data/features.parquet").filter(~pl.col("is_train")).sort("trade_date", "ts_code").collect()
    matrix = np.ascontiguousarray(test.select(features).to_numpy(), dtype=np.float32)
    raw = model.predict(matrix, num_threads=threads)
    del matrix
    raw[~test.get_column("price_valid").to_numpy()] = -1e6
    panel = Panel.from_frame(test)
    ranks = postprocess_scores(panel, raw, alpha, bonus, restore_lower, top_current_weight)
    rebuilt = np.where(ranks < -1, -.05, .04 * (ranks - .5))
    ordered = test.select("row_id").with_columns(pl.Series("rebuilt", rebuilt)).sort("row_id").get_column("rebuilt").to_numpy()
    absolute_error = np.abs(ordered - values)
    assert float(absolute_error.max()) <= 5.01e-13, "Submission cannot be regenerated from the saved model"
    qs = (0, .01, .25, .5, .75, .99, 1)
    result = {"status": "passed", "rows": len(submitted), "stocks": submitted.get_column("ts_code").n_unique(),
        "trading_days": submitted.get_column("trade_date").n_unique(),
        "first_date": submitted.get_column("trade_date").min(), "last_date": submitted.get_column("trade_date").max(),
        "exact_source_key_order": True, "unique_keys": True, "all_predictions_finite": True,
        "missing_price_rows": int(invalid.sum()), "missing_price_value": -.05,
        "missing_price_low_score_check": True, "valid_price_min": float(values[~invalid].min()),
        "valid_price_max": float(values[~invalid].max()), "prediction_mean": float(values.mean()),
        "prediction_std": float(values.std()),
        "prediction_quantiles": {str(q): float(v) for q, v in zip(qs, np.quantile(values, qs))},
        "full_model_reload_rows_verified": len(values), "full_model_reload_max_absolute_error": float(absolute_error.max()),
        "serialization_tolerance": 5.01e-13,
        "prediction_semantics": "Ordinal score with temporal smoothing, prior-Top persistence, protected Top membership and separately restored current ranks inside/outside the Top block; not a calibrated expected return.",
        "test_outcome_validation": "Unavailable: official test labels were not supplied; no test IC, return or accuracy is claimed."}
    del test, raw, ranks, model, ordered, submitted, test_source
    gc.collect()
    return result


def check_fold_reload(features: list[str], threads: int) -> dict:
    tests = []
    for year in (2022, 2023, 2024):
        cached = pl.read_parquet(ROOT / f"validation/fold_{year}.parquet").sort("trade_date", "ts_code")
        indexes = np.linspace(0, len(cached) - 1, 4096, dtype=int)
        keys = cached[indexes].select("ts_code", "trade_date", "pred_raw")
        sample = pl.scan_parquet(ROOT / "data/features.parquet").filter(
            pl.col("is_train") & pl.col("trade_date").is_between(year * 10000 + 101, year * 10000 + 1231)
        ).join(keys.lazy(), on=["ts_code", "trade_date"], how="inner").collect()
        model = lgb.Booster(model_str=(ROOT / f"models/fold_{year}.txt").read_text(encoding="utf-8"))
        assert model.feature_name() == features
        pred = model.predict(np.ascontiguousarray(sample.select(features).to_numpy(), dtype=np.float32), num_threads=threads).astype(np.float32)
        pred[~sample.get_column("price_valid").to_numpy()] = -1e6
        error = float(np.max(np.abs(pred - sample.get_column("pred_raw").to_numpy())))
        assert error == 0, f"Fold {year} raw predictions do not match its saved model"
        tests.append({"year": year, "sample_rows": len(sample), "max_absolute_error": error, "status": "passed"})
        del cached, sample, model
        gc.collect()
    return {"status": "passed", "folds": tests}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--threads", type=int, default=16)
    parser.add_argument("--check-prefix-only", action="store_true")
    args = parser.parse_args()
    log("Checking production feature/smoothing causality on an isolated synthetic fixture...")
    prefix = check_feature_prefix()
    if args.check_prefix_only:
        print(json.dumps(prefix, indent=2, ensure_ascii=False))
        return
    started = datetime.now(timezone.utc).isoformat()
    input_paths = [ROOT / "data/feature_manifest.json", ROOT / "validation/metrics.json",
        ROOT / "outputs/submission.csv", ROOT / "models/final_lightgbm.txt",
        ROOT / "evaluate.py", ROOT / "src/features.py", ROOT / "src/scoring.py", ROOT / "run.py"]
    fingerprints = {str(path.relative_to(ROOT)): digest(path) for path in input_paths}
    manifest = json.loads((ROOT / "data/feature_manifest.json").read_text(encoding="utf-8"))
    metrics = json.loads((ROOT / "validation/metrics.json").read_text(encoding="utf-8"))
    alpha = metrics["selected_alpha"]
    bonus = metrics["selected_persistence_bonus"]
    restore = bool(metrics.get("selected_restore_lower", False))
    top_weight = float(metrics.get("selected_top_current_weight", 0.0))
    assert metrics["selection_years"] == [2022, 2023] and metrics["holdout_year"] == 2024
    candidates = metrics["joint_candidates"]
    assert all(set(item["years"]) == {"2022", "2023"} for item in candidates.values())
    assert metrics["postprocess_selection_rule"] == "maximize_minimum_annual_score_2022_2023"
    chosen = max(candidates, key=lambda key: min(candidates[key]["years"][str(y)]["final_score"] for y in (2022, 2023)))
    assert chosen == metrics["selected_postprocess_key"]
    assert candidates[chosen]["config"] == {"alpha": alpha, "bonus": bonus, "restore_lower": restore}
    internal = metrics["top_internal_candidates"]
    assert all(set(item["years"]) == {"2022", "2023"} for item in internal.values())
    assert metrics["top_internal_selection_rule"] == "maximize_minimum_annual_score_2022_2023_after_joint_selection"
    chosen_top = max(internal, key=lambda key: min(internal[key]["years"][str(y)]["final_score"] for y in (2022, 2023)))
    assert internal[chosen_top]["weight"] == top_weight
    log("Checking date boundaries and complete 2024 scoring with the organizer's evaluate.py...")
    boundaries = check_time_boundaries()
    official = check_official_score(alpha, bonus, metrics["optimized_folds"]["2024"], restore, top_weight)
    log("Regenerating every submitted prediction from the saved final model (read-only comparison)...")
    submission = check_submission(alpha, bonus, manifest["features"], args.threads, restore, top_weight)
    log("Checking deterministic saved-fold model samples...")
    reloaded = check_fold_reload(manifest["features"], args.threads)
    for path in input_paths:
        assert digest(path) == fingerprints[str(path.relative_to(ROOT))], f"Input changed during audit: {path}"
    result = {"status": "passed", "started_at_utc": started,
        "completed_at_utc": datetime.now(timezone.utc).isoformat(), "selected_alpha": alpha,
        "selected_persistence_bonus": bonus,
        "selected_restore_lower": restore,
        "selected_top_current_weight": top_weight,
        "feature_causality": prefix, "time_boundaries": boundaries,
        "official_full_2024": official, "submission": submission,
        "fold_model_reload": reloaded, "input_sha256": fingerprints,
        "limitations": ["The official 2025-2026 test labels are unavailable; prediction outcomes cannot be validated locally.",
            "Reported Top-group excess is the organizer's uncosted close-to-close statistic, not an executable net strategy return.",
            "Provided adjusted prices/universe may have provenance limitations not resolvable from the supplied files."]}
    output = ROOT / "validation/prediction_audit.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"All prediction audits passed: {output}")


if __name__ == "__main__":
    main()
