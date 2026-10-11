"""One diagnostic 2024 evaluation of the preselected Optuna candidate.

The 2024 period has been inspected in prior project iterations, so this is
not a pristine holdout and must not be described as one.
"""

from __future__ import annotations

import json
from pathlib import Path

import lightgbm as lgb
import numpy as np
import polars as pl

from experiments.optuna_regression import ALPHA, BONUS, OUT, load_data
from src.scoring import add_top_persistence, make_scores, score


def main() -> None:
    study = json.loads((OUT / "optuna_regression_2022_2023.json").read_text(encoding="utf-8"))
    best = study["best_params"]
    x, y, xv, panel, columns = load_data(2024)
    params = {
        "objective": "regression", "metric": "l2", "learning_rate": 0.05,
        "num_leaves": best["num_leaves"], "min_data_in_leaf": best["min_data_in_leaf"],
        "feature_fraction": 0.85, "bagging_fraction": 0.85, "bagging_freq": 1,
        "lambda_l2": best["lambda_l2"], "max_bin": 127,
        "num_threads": 16, "seed": 2026, "verbosity": -1,
        "feature_pre_filter": False,
    }
    model = lgb.train(params, lgb.Dataset(x, label=y, feature_name=columns),
                      num_boost_round=best["rounds"])
    raw = np.asarray(model.predict(xv, num_threads=16), dtype=np.float64)
    raw[~panel.valid_price.reshape(-1)] = -1e6
    predicted = add_top_persistence(panel, make_scores(panel, raw, ALPHA), BONUS)
    metrics, _ = score(panel, predicted)
    candidate = panel.frame.drop("pred_raw").with_columns(pl.Series("pred_raw", raw))
    candidate.write_parquet(OUT / "optuna_best_2024.parquet", compression="zstd")
    result = {"best_params_selected_on": [2022, 2023], "best_params": best,
              "year": 2024, "metrics": metrics}
    (OUT / "optuna_best_2024.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
