"""Final sweep, wave 4: backbone hyperparameters chosen on years no gate has seen.

Why this wave exists. The released LightGBM configuration (31 leaves, 180 rounds,
lambda_l2 5.0) was fixed a priori: run.fit_model trains with no validation set and
no early stopping, so nothing in the released pipeline ever checked that those
numbers are right. The project's only hyperparameter search, experiments/
optuna_regression.py, ran under a superseded post-processing stack (alpha 0.95,
bonus 0.15) and its 2024 composite was 0.3597 against the released 0.4092, so its
winner (15 leaves, lambda_l2 10) was never examined under the stack actually in
force. This is therefore an open question, not a retry of a frozen record.

Design. Nested and one-shot. A small pre-declared grid is trained and scored on
2020 and 2021 - years that no adoption gate in this project has ever used - and
the winner is chosen by the maximin composite over those two years before any
scored year is touched. Only that single winner is then trained on 2022, 2023 and
2024 and scored once each, against the standing three-year strict gate. The
released configuration is itself in the grid, so "keep the release" is a possible
and perfectly good outcome.

Selection years are scored without the 25% pooled blend because the auxiliary
cache exists only for 2022-2024; that blend is Top-set inert, so it cannot change
which configuration wins on turnover or excess, and it is disabled identically
for every config. Scored years use the full released stack, auxiliary included.

Harness proof: retraining the released configuration for 2022 through this
module's own code path must reproduce validation/fold_2022.parquet bit-for-bit.
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

from run import FEATURE_FILE, ROOT, feature_names, fold_cutoff, to_matrix
from src.scoring import Panel
from experiments.bonus_extension import file_hash

OUT = ROOT / "experiments" / "final_sweep_eval"
AUDIT_FOLDS = ROOT / "experiments" / "extended_audit_eval" / "folds"
KEYS = ["ts_code", "trade_date"]
SELECTION_YEARS = (2020, 2021)
DEVELOPMENT_YEARS = (2022, 2023)
DIAGNOSTIC_YEAR = 2024
THREADS = 16

BASE_PARAMS = {"objective": "regression", "metric": "l2", "learning_rate": 0.05,
               "min_data_in_leaf": 300, "feature_fraction": 0.85, "bagging_fraction": 0.85,
               "bagging_freq": 1, "max_bin": 127, "num_threads": THREADS, "seed": 2026,
               "verbosity": -1}
RELEASED = {"num_leaves": 31, "lambda_l2": 5.0, "rounds": 180}

GRID = [
    {"key": "W4_leaves31_rounds180_l2_5", "num_leaves": 31, "lambda_l2": 5.0, "rounds": 180,
     "is_released_configuration": True},
    {"key": "W4_leaves31_rounds300_l2_5", "num_leaves": 31, "lambda_l2": 5.0, "rounds": 300},
    {"key": "W4_leaves31_rounds180_l2_10", "num_leaves": 31, "lambda_l2": 10.0, "rounds": 180},
    {"key": "W4_leaves31_rounds300_l2_10", "num_leaves": 31, "lambda_l2": 10.0, "rounds": 300},
    {"key": "W4_leaves15_rounds180_l2_5", "num_leaves": 15, "lambda_l2": 5.0, "rounds": 180},
    {"key": "W4_leaves15_rounds300_l2_5", "num_leaves": 15, "lambda_l2": 5.0, "rounds": 300},
    {"key": "W4_leaves15_rounds180_l2_10", "num_leaves": 15, "lambda_l2": 10.0, "rounds": 180},
    {"key": "W4_leaves15_rounds300_l2_10", "num_leaves": 15, "lambda_l2": 10.0, "rounds": 300},
    {"key": "W4_leaves63_rounds180_l2_5", "num_leaves": 63, "lambda_l2": 5.0, "rounds": 180},
    {"key": "W4_leaves63_rounds300_l2_10", "num_leaves": 63, "lambda_l2": 10.0, "rounds": 300},
    {"key": "W4_leaves63_rounds120_l2_10", "num_leaves": 63, "lambda_l2": 10.0, "rounds": 120},
    {"key": "W4_leaves31_rounds120_l2_5", "num_leaves": 31, "lambda_l2": 5.0, "rounds": 120},
]

PROTOCOL = {
    "experiment": "final_sweep_wave4_nested_hyperparameter_selection",
    "grid": GRID,
    "base_params": BASE_PARAMS,
    "released_configuration": RELEASED,
    "selection_years": list(SELECTION_YEARS),
    "selection_rule": "maximin official composite over the selection years, ties broken toward the "
                      "released configuration; the winner is fixed before any scored year is "
                      "trained or scored",
    "selection_scorer": "released stack with alpha 0.9, bonus 0.3 and protected-block restoration "
                        "at top_current_weight 1.0, without the pooled blend, identical for every "
                        "grid member",
    "development_years": list(DEVELOPMENT_YEARS),
    "diagnostic_year": DIAGNOSTIC_YEAR,
    "scored_scorer": "the full released stack including the 25% top-only pooled blend",
    "scorer_implementation": "the unmodified evaluate.py through the audit replica, anchored on "
                             "the released 2022 composite to 1e-12",
    "adoption_gate": "the selected configuration must strictly raise the released composite in "
                     "2022 AND 2023, then 2024; identical to every earlier suite",
    "harness_proof": "retraining the released configuration for 2022 through this module must "
                     "reproduce validation/fold_2022.parquet bit-for-bit",
    "training_recipe": "exactly run.fit_model's parameters and filters, with only num_leaves, "
                       "lambda_l2 and num_boost_round varying; training rows are is_train, "
                       "trade_date < fold_cutoff(year), y_rank not null and price_valid",
    "prohibited_after_results": [
        "Adding grid points, years or parameters after any score is seen",
        "Re-selecting the winner on a scored year",
        "Scoring a second configuration on 2022-2024",
        "Re-scoring years or modifying the release",
    ],
    "limitations": [
        "Selection years have less training history than scored years, so the optimal capacity may "
        "differ between them.",
        "2022-2024 have been examined repeatedly by earlier suites; a three-year pass is evidence "
        "against a fluke, not proof of out-of-sample edge.",
        "Twelve configurations are compared on two selection years; the maximin rule and the "
        "pre-declared grid are the only guards against selection noise.",
    ],
}


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def params_for(config: dict) -> dict:
    return {**BASE_PARAMS, "num_leaves": config["num_leaves"], "lambda_l2": config["lambda_l2"]}


def fit_and_predict(config: dict, year: int,
                    features: list[str]) -> tuple[pl.DataFrame, np.ndarray, int]:
    """Train one configuration on one fold and predict that year, run.fit_model's recipe."""
    cutoff = fold_cutoff(year)
    lazy = pl.scan_parquet(FEATURE_FILE)
    train = (lazy.filter(pl.col("is_train") & (pl.col("trade_date") < cutoff)
                         & pl.col("y_rank").is_not_null() & pl.col("price_valid"))
             .select(features + ["y_rank"]).collect())
    x = to_matrix(train, features)
    y = train.get_column("y_rank").to_numpy().astype(np.float32)
    rows = len(y)
    del train
    gc.collect()
    model = lgb.train(params_for(config), lgb.Dataset(x, label=y, feature_name=features,
                                                      free_raw_data=True),
                      num_boost_round=config["rounds"])
    del x, y
    gc.collect()
    valid = (lazy.filter(pl.col("is_train")
                        & pl.col("trade_date").is_between(year * 10000 + 101, year * 10000 + 1231))
             .sort("trade_date", "ts_code").collect())
    raw = model.predict(to_matrix(valid, features), num_threads=THREADS).astype(np.float64)
    raw[~valid.get_column("price_valid").to_numpy()] = -1e6
    frame = valid.select(KEYS).with_columns(pl.Series("pred_raw", raw))
    del valid, model
    gc.collect()
    return frame, raw, rows


def write_protocol() -> None:
    path = OUT / "protocol_wave4.json"
    if path.exists():
        raise SystemExit("Wave-4 protocol already frozen")
    payload = {**PROTOCOL, "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "source_sha256": file_hash(Path(__file__))}
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    log("Froze wave-4 protocol before any training or scoring")


def verify_protocol() -> dict:
    protocol = json.loads((OUT / "protocol_wave4.json").read_text(encoding="utf-8"))
    if protocol["source_sha256"] != file_hash(Path(__file__)):
        raise SystemExit("final_sweep_wave4.py changed after its protocol was frozen; stop")
    return protocol


def harness_proof(features: list[str]) -> dict:
    released = next(c for c in GRID if c.get("is_released_configuration"))
    frame, raw, rows = fit_and_predict(released, 2022, features)
    reference = pl.read_parquet(ROOT / "validation" / "fold_2022.parquet").sort("trade_date", "ts_code")
    identical = bool(frame.select(KEYS).equals(reference.select(KEYS))
                     and np.array_equal(raw.astype(np.float32),
                                        reference["pred_raw"].to_numpy().astype(np.float32)))
    log(f"Harness proof: released configuration rebuilt for 2022 identical = {identical} "
        f"({rows:,} training rows)")
    if not identical:
        raise AssertionError("Wave-4 training path does not reproduce the released 2022 fold")
    return {"released_configuration_2022_bit_identical": identical, "training_rows": rows}


def select() -> None:
    """Train and score every grid member on the selection years, then fix one winner."""
    verify_protocol()
    result_path = OUT / "selection_wave4.json"
    if result_path.exists():
        raise SystemExit("Wave-4 selection already recorded; preserving it")
    from experiments.extended_audit import audit_score, released_stack

    features = feature_names()
    started = time.monotonic()
    proof = harness_proof(features)
    panels = {}
    for year in SELECTION_YEARS:
        path = AUDIT_FOLDS / f"fold_{year}.parquet"
        if not path.exists():
            raise SystemExit(f"Missing audit fold {path}; run experiments.extended_audit train")
        panels[year] = Panel.from_frame(pl.read_parquet(path))
    results = {}
    for config in GRID:
        key = config["key"]
        composites = {}
        for year in SELECTION_YEARS:
            panel = panels[year]
            frame, raw, _ = fit_and_predict(config, year, features)
            if not frame.select(KEYS).equals(panel.frame.select(KEYS)):
                raise AssertionError(f"{key} {year}: prediction keys differ from the audit fold")
            substituted = Panel.from_frame(panel.frame.with_columns(pl.Series("pred_raw", raw)))
            metrics, _ = audit_score(substituted, released_stack(substituted, raw, None), year)
            composites[str(year)] = {k: float(v) for k, v in metrics.items()}
            frame.select(KEYS + ["pred_raw"]).write_parquet(
                OUT / f"{key}_selection_{year}.parquet", compression="zstd")
            del frame, raw, substituted
            gc.collect()
            log(f"{key} {year}: composite={metrics['final_score']:.9f} ic={metrics['ic_mean']:.6f}")
        values = [item["final_score"] for item in composites.values()]
        results[key] = {"config": config, "years": composites, "minimax": min(values),
                        "mean": sum(values) / len(values)}
    released_key = next(c["key"] for c in GRID if c.get("is_released_configuration"))
    ranked = sorted(results, key=lambda k: (-results[k]["minimax"], k != released_key))
    winner = ranked[0]
    output = {"stage": "select_wave4", "generated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
              "elapsed_seconds": time.monotonic() - started,
              "protocol_sha256": file_hash(OUT / "protocol_wave4.json"),
              "harness_proof": proof, "selection_years": list(SELECTION_YEARS),
              "results": results, "ranking_by_maximin": ranked, "selected": winner,
              "selected_config": results[winner]["config"],
              "released_configuration_key": released_key,
              "selected_is_released_configuration": winner == released_key,
              "note": "Winner fixed here, before any scored year was trained or scored."}
    result_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"WAVE-4 SELECTION: winner={winner} maximin={results[winner]['minimax']:.9f} "
        f"(released maximin={results[released_key]['minimax']:.9f})")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("protocol", "select"))
    arguments = parser.parse_args()
    if arguments.stage == "protocol":
        write_protocol()
    else:
        select()
