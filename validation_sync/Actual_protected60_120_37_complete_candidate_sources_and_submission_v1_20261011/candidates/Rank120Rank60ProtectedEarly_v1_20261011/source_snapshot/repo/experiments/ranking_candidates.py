"""Time-ordered ranking-model experiments; never overwrites submission files.

Examples:
    python -m experiments.ranking_candidates --model lightgbm --year 2022
    python -m experiments.ranking_candidates --model xgboost --year 2022

Each training fold ends before the existing one-day purge boundary. Candidate
metrics use the project's official-compatible scorer and fixed current
post-processing. No 2024 fold is used for model selection in this module.
"""

from __future__ import annotations

import argparse
import gc
import json
from pathlib import Path
import time

import lightgbm as lgb
import numpy as np
import polars as pl

from run import ROOT, FEATURE_FILE, feature_names, fold_cutoff, to_matrix
from src.scoring import Panel, add_top_persistence, make_scores, score


OUT = ROOT / "experiments" / "ranking_eval"
ALPHA = 0.95
BONUS = 0.15


def load_fold(year: int):
    if year not in (2022, 2023, 2024):
        raise ValueError("Unsupported validation year")
    columns = feature_names()
    lazy = pl.scan_parquet(FEATURE_FILE)
    cutoff = fold_cutoff(year)
    train = (
        lazy.filter(pl.col("is_train") & (pl.col("trade_date") < cutoff)
                    & pl.col("y_rank").is_not_null() & pl.col("price_valid"))
        .select(["trade_date", "y_rank"] + columns)
        .sort("trade_date")
        .collect()
    )
    dates = train.get_column("trade_date").to_numpy()
    _, group = np.unique(dates, return_counts=True)
    labels = np.clip(np.floor((train.get_column("y_rank").to_numpy() + 0.5) * 10), 0, 9).astype(np.int32)
    train_x = to_matrix(train, columns)
    del train, dates
    gc.collect()
    valid = (
        lazy.filter(pl.col("is_train") & pl.col("trade_date").is_between(year * 10000 + 101, year * 10000 + 1231))
        .select(["ts_code", "trade_date", "price_valid"] + columns)
        .sort("trade_date", "ts_code")
        .collect()
    )
    valid_x = to_matrix(valid, columns)
    fold = pl.read_parquet(ROOT / "validation" / f"fold_{year}.parquet").sort("trade_date", "ts_code")
    if not valid.select("ts_code", "trade_date").equals(fold.select("ts_code", "trade_date")):
        raise AssertionError("Validation keys differ from existing fold")
    valid_price = valid.get_column("price_valid").to_numpy()
    del valid
    gc.collect()
    return train_x, labels, group, valid_x, valid_price, fold, columns


def train_lightgbm(x, y, group, columns, rounds: int, threads: int, objective: str):
    params = {
        "objective": objective, "metric": "ndcg", "learning_rate": 0.05,
        "num_leaves": 31, "min_data_in_leaf": 300, "feature_fraction": 0.85,
        "bagging_fraction": 0.85, "bagging_freq": 1, "lambda_l2": 5.0,
        "max_bin": 127, "num_threads": threads, "seed": 2026,
        "verbosity": -1,
    }
    if objective == "lambdarank":
        params["label_gain"] = list(range(10))
        params["lambdarank_truncation_level"] = 500
    data = lgb.Dataset(x, label=y, group=group, feature_name=columns, free_raw_data=True)
    model = lgb.train(params, data, num_boost_round=rounds)
    return model


def train_xgboost(x, y, group, rounds: int, threads: int):
    import xgboost as xgb

    model = xgb.XGBRanker(
        objective="rank:ndcg", tree_method="hist", n_estimators=rounds,
        learning_rate=0.05, max_depth=5, min_child_weight=20,
        subsample=0.85, colsample_bytree=0.85, reg_lambda=5.0,
        max_bin=127, n_jobs=threads, random_state=2026,
        lambdarank_pair_method="mean", lambdarank_num_pair_per_sample=1,
        ndcg_exp_gain=False,
    )
    model.fit(x, y, group=group, verbose=False)
    return model


def evaluate(model_name: str, year: int, rounds: int, threads: int, objective: str = "rank_xendcg") -> dict:
    started = time.monotonic()
    x, y, group, valid_x, valid_price, fold, columns = load_fold(year)
    print(f"Loaded {year}: train={len(y):,}, groups={len(group):,}, valid={len(valid_x):,}", flush=True)
    if model_name == "lightgbm":
        model = train_lightgbm(x, y, group, columns, rounds, threads, objective)
        raw = model.predict(valid_x, num_threads=threads)
    elif model_name == "xgboost":
        model = train_xgboost(x, y, group, rounds, threads)
        raw = model.predict(valid_x)
    else:
        raise ValueError(model_name)
    raw = np.asarray(raw, dtype=np.float64)
    raw[~valid_price] = -1e6
    candidate = fold.drop("pred_raw").with_columns(pl.Series("pred_raw", raw))
    panel = Panel.from_frame(candidate)
    predictions = add_top_persistence(panel, make_scores(panel, raw, ALPHA), BONUS)
    metrics, _ = score(panel, predictions)
    OUT.mkdir(parents=True, exist_ok=True)
    stem = f"{model_name}_{objective if model_name == 'lightgbm' else 'linear_ndcg'}_{year}_{rounds}round"
    candidate.write_parquet(OUT / f"{stem}.parquet", compression="zstd")
    result = {
        "model": model_name, "objective": objective if model_name == "lightgbm" else "rank:ndcg_linear_gain",
        "year": year, "rounds": rounds,
        "alpha": ALPHA, "bonus": BONUS, "train_rows": len(y),
        "train_groups": len(group), "purge_cutoff_exclusive": fold_cutoff(year),
        "metrics": metrics, "elapsed_seconds": time.monotonic() - started,
    }
    (OUT / f"{stem}.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)
    del x, y, group, valid_x, valid_price, fold, model, panel
    gc.collect()
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", choices=("lightgbm", "xgboost"), required=True)
    parser.add_argument("--year", type=int, choices=(2022, 2023, 2024), required=True)
    parser.add_argument("--rounds", type=int, default=80)
    parser.add_argument("--threads", type=int, default=16)
    parser.add_argument("--objective", choices=("rank_xendcg", "lambdarank"), default="rank_xendcg")
    args = parser.parse_args()
    evaluate(args.model, args.year, args.rounds, args.threads, args.objective)


if __name__ == "__main__":
    main()
