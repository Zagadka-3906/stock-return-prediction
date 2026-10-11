"""Small, time-ordered Optuna study for the competition's exact score.

Only 2022 and 2023 validation folds are loaded. The objective is the weaker
annual score, not LightGBM's training loss. This study is exploratory because
those years have already informed earlier post-processing choices.
"""

from __future__ import annotations

import argparse
import gc
import json
from pathlib import Path
import time

import lightgbm as lgb
import numpy as np
import optuna
import polars as pl

from run import ROOT, FEATURE_FILE, feature_names, fold_cutoff, to_matrix
from src.scoring import Panel, add_top_persistence, make_scores, score


OUT = ROOT / "experiments" / "ranking_eval"
ALPHA = 0.95
BONUS = 0.15


def load_data(year: int):
    columns = feature_names()
    cutoff = fold_cutoff(year)
    lazy = pl.scan_parquet(FEATURE_FILE)
    train = (
        lazy.filter(pl.col("is_train") & (pl.col("trade_date") < cutoff)
                    & pl.col("y_rank").is_not_null() & pl.col("price_valid"))
        .select(columns + ["y_rank"])
        .collect()
    )
    x = to_matrix(train, columns)
    y = train.get_column("y_rank").to_numpy().astype(np.float32)
    del train
    gc.collect()
    valid = (
        lazy.filter(pl.col("is_train") & pl.col("trade_date").is_between(year * 10000 + 101, year * 10000 + 1231))
        .select(["ts_code", "trade_date"] + columns)
        .sort("trade_date", "ts_code")
        .collect()
    )
    xv = to_matrix(valid, columns)
    fold = pl.read_parquet(ROOT / "validation" / f"fold_{year}.parquet").sort("trade_date", "ts_code")
    if not valid.select("ts_code", "trade_date").equals(fold.select("ts_code", "trade_date")):
        raise AssertionError("Validation key mismatch")
    panel = Panel.from_frame(fold)
    del valid, fold
    gc.collect()
    print(f"Loaded {year}: train={len(y):,}, valid={len(xv):,}, cutoff={cutoff}", flush=True)
    return x, y, xv, panel, columns


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=5)
    parser.add_argument("--threads", type=int, default=16)
    args = parser.parse_args()
    data = {year: load_data(year) for year in (2022, 2023)}
    OUT.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()

    def objective(trial: optuna.Trial) -> float:
        leaves = trial.suggest_categorical("num_leaves", [15, 31, 63])
        min_leaf = trial.suggest_categorical("min_data_in_leaf", [200, 300, 600])
        rounds = trial.suggest_categorical("rounds", [120, 180, 240])
        l2 = trial.suggest_categorical("lambda_l2", [1.0, 5.0, 10.0])
        params = {
            "objective": "regression", "metric": "l2", "learning_rate": 0.05,
            "num_leaves": leaves, "min_data_in_leaf": min_leaf,
            "feature_fraction": 0.85, "bagging_fraction": 0.85,
            "bagging_freq": 1, "lambda_l2": l2, "max_bin": 127,
            "num_threads": args.threads, "seed": 2026, "verbosity": -1,
            "feature_pre_filter": False,
        }
        yearly = {}
        for year in (2022, 2023):
            x, y, xv, panel, columns = data[year]
            dataset = lgb.Dataset(x, label=y, feature_name=columns, free_raw_data=True)
            model = lgb.train(params, dataset, num_boost_round=rounds)
            raw = np.asarray(model.predict(xv, num_threads=args.threads), dtype=np.float64)
            raw[~panel.valid_price.reshape(-1)] = -1e6
            predicted = add_top_persistence(panel, make_scores(panel, raw, ALPHA), BONUS)
            yearly[year], _ = score(panel, predicted)
            del dataset, model, raw, predicted
            gc.collect()
        worst = min(yearly[y]["final_score"] for y in (2022, 2023))
        mean = float(np.mean([yearly[y]["final_score"] for y in (2022, 2023)]))
        trial.set_user_attr("annual_scores", {str(y): yearly[y] for y in (2022, 2023)})
        trial.set_user_attr("mean_score", mean)
        print(f"trial={trial.number} params={trial.params} worst={worst:.6f} mean={mean:.6f}", flush=True)
        return worst

    study = optuna.create_study(direction="maximize", sampler=optuna.samplers.TPESampler(seed=2026))
    study.enqueue_trial({"num_leaves": 31, "min_data_in_leaf": 300, "rounds": 180, "lambda_l2": 5.0})
    study.optimize(objective, n_trials=args.trials, gc_after_trial=True)
    result = {
        "selection_period": [2022, 2023],
        "objective": "maximize_minimum_annual_official_compatible_score",
        "alpha": ALPHA, "bonus": BONUS,
        "best_value": study.best_value, "best_params": study.best_params,
        "elapsed_seconds": time.monotonic() - started,
        "trials": [
            {"number": t.number, "state": t.state.name, "value": t.value,
             "params": t.params, "annual_scores": t.user_attrs.get("annual_scores"),
             "mean_score": t.user_attrs.get("mean_score")}
            for t in study.trials
        ],
    }
    target = OUT / "optuna_regression_2022_2023.json"
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("best_value", "best_params", "elapsed_seconds")}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
