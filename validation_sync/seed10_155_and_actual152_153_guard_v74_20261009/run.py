"""Reproducible end-to-end workflow for competition problem 5.

Usage: python run.py all
"""

from __future__ import annotations

import argparse
import gc
import json
import time
from pathlib import Path

import lightgbm as lgb
import numpy as np
import polars as pl

from src.features import build_features
from src.scoring import Panel, add_top_persistence, make_scores, postprocess_scores, score


ROOT = Path(__file__).resolve().parent
FEATURE_FILE = ROOT / "data" / "features.parquet"
MANIFEST = ROOT / "data" / "feature_manifest.json"
VAL_DIR = ROOT / "validation"
MODEL_DIR = ROOT / "models"
OUT_DIR = ROOT / "outputs"
YEARS = (2022, 2023, 2024)
ALPHAS = (0.0, 0.3, 0.6, 0.8, 0.9, 0.95, 0.97, 0.98, 0.99)
PERSISTENCE_BONUSES = (0.0, 0.002, 0.005, 0.01, 0.02, 0.03, 0.05, 0.07, 0.10, 0.15, 0.20, 0.30, 0.50, 0.75, 1.0)
JOINT_ALPHAS = (0.6, 0.8, 0.9, 0.95)
JOINT_BONUSES = (0.05, 0.15, 0.30)
TOP_CURRENT_WEIGHTS = (0.0, 0.5, 1.0)


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def feature_names() -> list[str]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))["features"]


def feature_stage(rebuild: bool = False) -> None:
    if FEATURE_FILE.exists() and MANIFEST.exists() and not rebuild:
        log(f"Using cached features: {FEATURE_FILE}")
        return
    log("Building Polars panel features from Qlib Alpha158 definitions")
    result = build_features(ROOT, FEATURE_FILE)
    log(f"Feature stage complete: {result['feature_count']} features")


def fold_cutoff(year: int) -> int:
    dates = (
        pl.scan_parquet(FEATURE_FILE)
        .filter(pl.col("is_train"))
        .select("trade_date")
        .unique()
        .sort("trade_date")
        .collect()
        .get_column("trade_date")
        .to_numpy()
    )
    first_valid = int(np.searchsorted(dates, year * 10000 + 101))
    if first_valid < 2:
        raise ValueError("Insufficient training history for the validation fold")
    # y(t) uses close(t+1). Exclude the last training date before validation.
    return int(dates[first_valid - 1])


def fit_model(x: np.ndarray, y: np.ndarray, features: list[str], rounds: int, threads: int) -> lgb.Booster:
    params = {
        "objective": "regression",
        "metric": "l2",
        "learning_rate": 0.05,
        "num_leaves": 31,
        "min_data_in_leaf": 300,
        "feature_fraction": 0.85,
        "bagging_fraction": 0.85,
        "bagging_freq": 1,
        "lambda_l2": 5.0,
        "max_bin": 127,
        "num_threads": threads,
        "seed": 2026,
        "verbosity": -1,
    }
    ds = lgb.Dataset(x, label=y, feature_name=features, free_raw_data=True)
    return lgb.train(params, ds, num_boost_round=rounds)


def to_matrix(frame: pl.DataFrame, features: list[str]) -> np.ndarray:
    return np.ascontiguousarray(frame.select(features).to_numpy(), dtype=np.float32)


def train_fold(year: int, rounds: int, threads: int) -> None:
    features = feature_names()
    VAL_DIR.mkdir(exist_ok=True)
    MODEL_DIR.mkdir(exist_ok=True)
    cutoff = fold_cutoff(year)
    log(f"Fold {year}: training dates < {cutoff}; validation = calendar year {year}")
    lazy = pl.scan_parquet(FEATURE_FILE)
    train = (
        lazy.filter(pl.col("is_train") & (pl.col("trade_date") < cutoff) & pl.col("y_rank").is_not_null() & pl.col("price_valid"))
        .select(features + ["y_rank"])
        .collect()
    )
    x = to_matrix(train, features)
    y = train.get_column("y_rank").to_numpy().astype(np.float32)
    log(f"Fold {year}: fitting LightGBM on {len(y):,} rows, {x.shape[1]} features")
    del train
    gc.collect()
    model = fit_model(x, y, features, rounds, threads)
    # LightGBM's Windows file writer cannot handle this workspace's Chinese path.
    (MODEL_DIR / f"fold_{year}.txt").write_text(model.model_to_string(), encoding="utf-8")
    del x, y
    gc.collect()
    valid = (
        lazy.filter(pl.col("is_train") & pl.col("trade_date").is_between(year * 10000 + 101, year * 10000 + 1231))
        .sort("trade_date", "ts_code")
        .collect()
    )
    x_valid = to_matrix(valid, features)
    raw = model.predict(x_valid, num_threads=threads).astype(np.float32)
    raw[~valid.get_column("price_valid").to_numpy()] = -1e6
    result = valid.select("ts_code", "trade_date", "flag_limit_up", "price_valid", "y_ret_1d", "ROC5", "MA20")
    result = result.with_columns(pl.Series("pred_raw", raw))
    result.write_parquet(VAL_DIR / f"fold_{year}.parquet", compression="zstd")
    log(f"Fold {year}: saved {len(raw):,} validation predictions")
    del x_valid, valid, result, model
    gc.collect()


def train_stage(rounds: int, threads: int, retrain: bool = False) -> None:
    feature_stage()
    for year in YEARS:
        path = VAL_DIR / f"fold_{year}.parquet"
        if path.exists() and not retrain:
            log(f"Using cached fold {year}: {path}")
        else:
            train_fold(year, rounds, threads)


def evaluate_stage() -> dict:
    folds = {}
    joint_candidates = {}
    legacy_optimized = {}
    for year in (2022, 2023):
        frame = pl.read_parquet(VAL_DIR / f"fold_{year}.parquet")
        panel = Panel.from_frame(frame)
        raw = panel.frame.get_column("pred_raw").to_numpy()
        folds[year] = {}
        for alpha in ALPHAS:
            predictions = make_scores(panel, raw, alpha)
            metrics, _ = score(panel, predictions)
            folds[year][str(alpha)] = metrics
        legacy_optimized[year], _ = score(panel, postprocess_scores(panel, raw, .95, .15))
        for alpha in JOINT_ALPHAS:
            for bonus in JOINT_BONUSES:
                for restore in (False, True):
                    key = f"a{alpha}_b{bonus}_restore{int(restore)}"
                    item = joint_candidates.setdefault(key, {
                        "config": {"alpha": alpha, "bonus": bonus, "restore_lower": restore}, "years": {}})
                    item["years"][year], _ = score(panel, postprocess_scores(panel, raw, alpha, bonus, restore))
    selected_key = max(joint_candidates, key=lambda key: min(
        joint_candidates[key]["years"][year]["final_score"] for year in (2022, 2023)))
    config = joint_candidates[selected_key]["config"]
    selected, selected_bonus, restore = config["alpha"], config["bonus"], config["restore_lower"]
    lower_only_folds = dict(joint_candidates[selected_key]["years"])
    top_internal_candidates = {str(w): {"weight": w, "years": {}} for w in TOP_CURRENT_WEIGHTS}
    for year in (2022, 2023):
        panel = Panel.from_frame(pl.read_parquet(VAL_DIR / f"fold_{year}.parquet"))
        raw = panel.frame.get_column("pred_raw").to_numpy()
        for weight in TOP_CURRENT_WEIGHTS:
            if weight and not restore:
                continue
            item = top_internal_candidates[str(weight)]
            item["years"][year], _ = score(panel, postprocess_scores(
                panel, raw, selected, selected_bonus, restore, weight))
    top_internal_candidates = {key: item for key, item in top_internal_candidates.items() if item["years"]}
    top_key = max(top_internal_candidates, key=lambda key: min(
        top_internal_candidates[key]["years"][year]["final_score"] for year in (2022, 2023)))
    top_weight = top_internal_candidates[top_key]["weight"]
    optimized_folds = dict(top_internal_candidates[top_key]["years"])
    frame = pl.read_parquet(VAL_DIR / "fold_2024.parquet")
    panel = Panel.from_frame(frame)
    raw = panel.frame.get_column("pred_raw").to_numpy()
    no_smoothing, _ = score(panel, make_scores(panel, raw, 0.0))
    smoothed = make_scores(panel, raw, selected)
    baseline, _ = score(panel, smoothed)
    stable_only, _ = score(panel, postprocess_scores(panel, raw, selected, selected_bonus))
    lower_only_folds[2024], _ = score(panel, postprocess_scores(panel, raw, selected, selected_bonus, restore))
    optimized, daily = score(panel, postprocess_scores(panel, raw, selected, selected_bonus, restore, top_weight))
    legacy_optimized[2024], _ = score(panel, postprocess_scores(panel, raw, .95, .15))
    folds[2024] = {"0.0": no_smoothing, str(selected): baseline}
    optimized_folds[2024] = optimized
    report = {
        "selected_alpha": selected,
        "selected_persistence_bonus": selected_bonus,
        "selected_restore_lower": restore,
        "selected_top_current_weight": top_weight,
        "top_internal_candidates": top_internal_candidates,
        "top_internal_selection_rule": "maximize_minimum_annual_score_2022_2023_after_joint_selection",
        "lower_only_folds": lower_only_folds,
        "postprocess_selection_rule": "maximize_minimum_annual_score_2022_2023",
        "selected_postprocess_key": selected_key,
        "selection_years": [2022, 2023],
        "holdout_year": 2024,
        "folds": folds,
        "joint_candidates": joint_candidates,
        "legacy_optimized_folds": legacy_optimized,
        "stable_only_2024": stable_only,
        "optimized_folds": optimized_folds,
    }
    VAL_DIR.mkdir(exist_ok=True)
    (VAL_DIR / "metrics.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    daily.write_csv(VAL_DIR / "daily_2024.csv")
    log(f"Selected alpha={selected}, persistence bonus={selected_bonus}, top current weight={top_weight}; "
        f"historical 2024 score={optimized['final_score']:.6f}")
    return report


def final_stage(rounds: int, threads: int, reuse_model: bool = False) -> None:
    report = json.loads((VAL_DIR / "metrics.json").read_text(encoding="utf-8"))
    alpha = float(report["selected_alpha"])
    bonus = float(report["selected_persistence_bonus"])
    features = feature_names()
    lazy = pl.scan_parquet(FEATURE_FILE)
    MODEL_DIR.mkdir(exist_ok=True)
    model_path = MODEL_DIR / "final_lightgbm.txt"
    if reuse_model:
        if not model_path.exists():
            raise FileNotFoundError(model_path)
        model = lgb.Booster(model_str=model_path.read_text(encoding="utf-8"))
        if model.feature_name() != features:
            raise ValueError("Saved model features differ from the current manifest")
        log("Using the saved final LightGBM model")
    else:
        train = lazy.filter(pl.col("is_train") & pl.col("y_rank").is_not_null() & pl.col("price_valid")).select(features + ["y_rank"]).collect()
        x = to_matrix(train, features)
        y = train.get_column("y_rank").to_numpy().astype(np.float32)
        del train
        gc.collect()
        log(f"Final model: fitting {len(y):,} labeled rows")
        model = fit_model(x, y, features, rounds, threads)
        model_path.write_text(model.model_to_string(), encoding="utf-8")
        del x, y
        gc.collect()
    importance = sorted(zip(features, model.feature_importance(importance_type="gain"), strict=True), key=lambda z: z[1], reverse=True)
    (VAL_DIR / "feature_importance.csv").write_text("feature,gain\n" + "\n".join(f"{name},{gain:.6f}" for name, gain in importance), encoding="utf-8")
    test = lazy.filter(~pl.col("is_train")).sort("trade_date", "ts_code").collect()
    raw = model.predict(to_matrix(test, features), num_threads=threads)
    raw[~test.get_column("price_valid").to_numpy()] = -1e6
    panel = Panel.from_frame(test)
    # An affine transform preserves all three official ranking-based metrics.
    ranked = postprocess_scores(panel, raw, alpha, bonus, bool(report.get("selected_restore_lower", False)),
                                float(report.get("selected_top_current_weight", 0.0)))
    pred = np.where(ranked < -1, -0.05, 0.04 * (ranked - 0.5))
    ordered = panel.frame.with_columns(pl.Series("pred", pred)).sort("row_id")
    submission = ordered.select("ts_code", "trade_date", "pred")
    OUT_DIR.mkdir(exist_ok=True)
    target = OUT_DIR / "submission.csv"
    submission.write_csv(target, float_precision=12)
    verify_submission(target)
    log(f"Submission created: {target} ({len(submission):,} rows)")


def verify_submission(path: Path) -> None:
    test = pl.read_csv(ROOT / "data" / "raw" / "测试集_X.csv", columns=["ts_code", "trade_date"], schema_overrides={"ts_code": pl.String, "trade_date": pl.Int32})
    submission = pl.read_csv(path, schema_overrides={"ts_code": pl.String, "trade_date": pl.Int32, "pred": pl.Float64})
    if submission.columns != ["ts_code", "trade_date", "pred"] or len(submission) != len(test):
        raise AssertionError("Submission columns or row count differ from test data")
    if not np.array_equal(test.get_column("ts_code").to_numpy(), submission.get_column("ts_code").to_numpy()):
        raise AssertionError("Submitted stock codes are not identical to test rows")
    if not np.array_equal(test.get_column("trade_date").to_numpy(), submission.get_column("trade_date").to_numpy()):
        raise AssertionError("Submitted dates are not identical to test rows")
    if not np.isfinite(submission.get_column("pred").to_numpy()).all():
        raise AssertionError("Submission predictions contain null, NaN or infinity")
    if submission.select(pl.struct("ts_code", "trade_date").n_unique()).item() != len(test):
        raise AssertionError("Submission contains duplicate keys")






def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("step", choices=["features", "train", "evaluate", "final", "verify", "all"])
    parser.add_argument("--rounds", type=int, default=180)
    parser.add_argument("--threads", type=int, default=16)
    parser.add_argument("--rebuild-features", action="store_true")
    parser.add_argument("--retrain", action="store_true")
    parser.add_argument("--reuse-final-model", action="store_true", help="Regenerate submission from the saved final model")
    args = parser.parse_args()
    if args.step in ("features", "all"):
        feature_stage(rebuild=args.rebuild_features)
    if args.step in ("train", "all"):
        train_stage(args.rounds, args.threads, retrain=args.retrain)
    if args.step in ("evaluate", "all"):
        evaluate_stage()
    if args.step in ("final", "all"):
        final_stage(args.rounds, args.threads, reuse_model=args.reuse_final_model)
    if args.step == "verify":
        verify_submission(OUT_DIR / "submission.csv")
        log("Submission verification passed")


if __name__ == "__main__":
    main()
