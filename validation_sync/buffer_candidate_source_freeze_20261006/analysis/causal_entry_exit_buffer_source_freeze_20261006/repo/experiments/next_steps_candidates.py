"""Small, purged walk-forward tests of target weighting and recency.

This script never writes production models, predictions, or reports. Candidate
choice must use 2022 and 2023 before running any 2024 diagnostic.
"""

from __future__ import annotations

import argparse
import gc
import json
from pathlib import Path

import lightgbm as lgb
import numpy as np
import polars as pl

from run import FEATURE_FILE, ROOT, feature_names, fold_cutoff, to_matrix
from src.scoring import Panel, add_top_persistence, make_scores, score


OUT = ROOT / "experiments" / "next_steps_eval"
ALPHA = 0.95
BONUS = 0.15
VARIANTS = ("top2", "huber", "recent2x", "rolling3")


def model_params(variant: str, threads: int) -> dict:
    params = {
        "objective": "huber" if variant == "huber" else "regression",
        "metric": "None",
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
    if variant == "huber":
        params["alpha"] = 0.9
    return params


def load_fold(year: int):
    features = feature_names()
    cutoff = fold_cutoff(year)
    lazy = pl.scan_parquet(FEATURE_FILE)
    train = (
        lazy.filter(
            pl.col("is_train")
            & (pl.col("trade_date") < cutoff)
            & pl.col("y_rank").is_not_null()
            & pl.col("price_valid")
        )
        .select(["trade_date", "y_rank"] + features)
        .collect()
    )
    train_dates = train.get_column("trade_date").to_numpy()
    y = train.get_column("y_rank").to_numpy().astype(np.float32)
    x = to_matrix(train, features)
    del train
    valid = (
        lazy.filter(
            pl.col("is_train")
            & pl.col("trade_date").is_between(year * 10000 + 101, year * 10000 + 1231)
        )
        .select(["ts_code", "trade_date"] + features)
        .sort("trade_date", "ts_code")
        .collect()
    )
    xv = to_matrix(valid, features)
    fold = pl.read_parquet(ROOT / "validation" / f"fold_{year}.parquet").sort("trade_date", "ts_code")
    if not valid.select("ts_code", "trade_date").equals(fold.select("ts_code", "trade_date")):
        raise AssertionError("Validation row keys do not match the production fold")
    panel = Panel.from_frame(fold)
    del valid, fold
    gc.collect()
    print(f"Loaded {year}: cutoff={cutoff}, train={len(y):,}, valid={len(xv):,}", flush=True)
    return x, y, train_dates, xv, panel, features, cutoff


def train_variant(year: int, variant: str, data, threads: int) -> dict:
    x, y, dates, xv, panel, features, cutoff = data
    if variant == "rolling3":
        start = (year - 3) * 10000 + 101
        mask = dates >= start
        train_x, train_y = x[mask], y[mask]
        weights = None
    else:
        start = None
        train_x, train_y = x, y
        if variant == "top2":
            weights = np.where(y >= 0.4, 2.0, 1.0).astype(np.float32)
        elif variant == "recent2x":
            recent_start = (year - 2) * 10000 + 101
            weights = np.where(dates >= recent_start, 2.0, 1.0).astype(np.float32)
        else:
            weights = None
    dataset = lgb.Dataset(train_x, label=train_y, weight=weights, feature_name=features)
    model = lgb.train(model_params(variant, threads), dataset, num_boost_round=180)
    raw = np.asarray(model.predict(xv, num_threads=threads), dtype=np.float32)
    raw[~panel.valid_price.reshape(-1)] = -1e6
    pred = add_top_persistence(panel, make_scores(panel, raw, ALPHA), BONUS)
    metrics, daily = score(panel, pred)
    OUT.mkdir(parents=True, exist_ok=True)
    stem = f"{variant}_{year}"
    panel.frame.select("ts_code", "trade_date").with_columns(pl.Series("pred_raw", raw)).write_parquet(
        OUT / f"{stem}.parquet", compression="zstd"
    )
    daily.write_csv(OUT / f"{stem}_daily.csv")
    result = {
        "variant": variant,
        "year": year,
        "train_cutoff_exclusive": cutoff,
        "train_start_inclusive": start,
        "train_rows": int(len(train_y)),
        "alpha": ALPHA,
        "bonus": BONUS,
        "metrics": metrics,
    }
    (OUT / f"{stem}.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{stem}: score={metrics['final_score']:.6f} IC={metrics['ic_mean']:.6f} "
          f"excess={metrics['annual_excess']:.6f} turnover={metrics['mean_turnover']:.6f}", flush=True)
    del train_x, train_y, weights, dataset, model, raw, pred, daily
    gc.collect()
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--years", type=int, nargs="+", default=[2022, 2023])
    parser.add_argument("--variants", nargs="+", choices=VARIANTS, default=list(VARIANTS))
    parser.add_argument("--threads", type=int, default=16)
    args = parser.parse_args()
    for year in args.years:
        if year not in (2022, 2023, 2024):
            raise ValueError("Only the established annual folds are supported")
        data = load_fold(year)
        for variant in args.variants:
            train_variant(year, variant, data, args.threads)
        del data
        gc.collect()


if __name__ == "__main__":
    main()
