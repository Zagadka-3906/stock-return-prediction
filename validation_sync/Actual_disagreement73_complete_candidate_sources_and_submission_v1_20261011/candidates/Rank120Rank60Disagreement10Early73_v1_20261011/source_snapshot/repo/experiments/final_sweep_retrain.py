"""Final sweep, retrain suite: backbone-level candidates under their own frozen protocol.

Four candidates change the backbone itself, because the released Top set -- and
therefore the Excess and Turnover terms that dominate the composite -- is
controlled solely by the backbone signal and its post-processing:

  T2a  stacking: the phase-1 GRU's raw output as a 64th backbone feature, so the
       tree learns when to trust the sequence signal instead of rank-averaging
  T2b  overnight-gap rank target: 143% of the close-to-close excess lives in the
       close(t)->open(t+1) leg, so train the backbone on that leg's rank
  T2d  calendar features: month, weekday and day-of-year terms, the only
       information class never offered to the backbone
  T2e  LambdaRank objective: a listwise ranking loss per trading day instead of
       squared error on the daily rank

Causality of the stacked GRU feature: a training row dated t receives the GRU
prediction of a model trained strictly before t. The three released fold GRUs
cover 2022-2024 rows; three additional GRUs with year-end 2018/2019/2020 cutoffs
cover 2019-2021 rows; 2018 rows carry a missing value, which LightGBM handles
natively rather than by imputation.
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import lightgbm as lgb
import numpy as np
import polars as pl

from run import FEATURE_FILE, ROOT, feature_names, fold_cutoff, to_matrix
from experiments.bonus_extension import (AUXILIARY, BASE_BONUS, BLEND_WEIGHT, FOLD,
                                         file_hash, load_auxiliary, load_panel)
from experiments.final_sweep import blend_top_only, log, retention_scores
from experiments.official_seed_development import official_score
from experiments.sequence_model import apply_scaler, fit_scaler, load_panel as load_seq_panel
import experiments.sequence_training as st

OUT = ROOT / "experiments" / "final_sweep_eval"
KEYS = ["ts_code", "trade_date"]
ROUNDS, SEED, THREADS = 180, 2026, 16
GRU_EXTRA_CUTOFFS = (20181231, 20191231, 20201231)
FOLD_YEARS = (2022, 2023, 2024)
DEVELOPMENT_YEARS = (2022, 2023)
NUMERIC_TOLERANCE = 1e-12

BASE_PARAMS = {"learning_rate": 0.05, "num_leaves": 31, "min_data_in_leaf": 300,
               "feature_fraction": 0.85, "bagging_fraction": 0.85, "bagging_freq": 1,
               "lambda_l2": 5.0, "max_bin": 127, "num_threads": THREADS,
               "seed": SEED, "verbosity": -1}

CANDIDATES = [
    {"key": "T2a_stacked_gru_feature", "variant": "stacked"},
    {"key": "T2b_overnight_rank_target", "variant": "overnight"},
    {"key": "T2d_calendar_features", "variant": "calendar"},
    {"key": "T2e_lambdarank_backbone", "variant": "lambdarank"},
]

PROTOCOL = {
    "experiment": "final_sweep_retrain_backbone_candidates",
    "candidates": CANDIDATES,
    "folds": "the released three expanding folds with their published cutoffs; 180 rounds and the "
             "released hyper-parameters, unchanged",
    "postprocess": "the released stack exactly: alpha 0.9, bonus 0.3, protected-block restoration "
                   "with top_current_weight 1.0, then the 25% top-only pooled blend",
    "pooled_auxiliary": "unchanged cached auxiliary; not refitted against any new backbone",
    "scorer": "Unmodified evaluate.py via official_score",
    "development_years": list(DEVELOPMENT_YEARS),
    "diagnostic_year": 2024,
    "adoption_gate": "strict improvement over the released composite in 2022 AND 2023, then 2024; "
                     "identical to the T1 suite gate",
    "baseline_anchor": "the released backbone raw prediction through the same code path must "
                       "reproduce the released composite to 1e-12 in every scored year",
    "prohibited_after_results": [
        "Retuning rounds, learning rate, leaves or any hyper-parameter for a new backbone",
        "Refitting the pooled auxiliary or the post-processing for a new backbone",
        "Adding candidates or re-scoring years",
        "Modifying the release or any frozen source",
    ],
    "limitations": [
        "New backbones are compared through a post-processing stack tuned on the old backbone's "
        "autocorrelation; part of any loss may be a stack mismatch rather than a worse signal.",
        "2022-2024 are repeatedly examined historical years.",
    ],
}


def params_for(variant: str) -> dict:
    params = dict(BASE_PARAMS)
    if variant == "lambdarank":
        params.update({"objective": "lambdarank", "metric": "ndcg",
                       "ndcg_eval_at": [10], "label_gain": ",".join(str(i) for i in range(64))})
    else:
        params.update({"objective": "regression", "metric": "l2"})
    return params


def calendar_columns(frame: pl.DataFrame) -> pl.DataFrame:
    date = frame["trade_date"]
    month = (date // 100) % 100
    day = date % 100
    doy = (date % 10000) // 100 * 30 + day
    return frame.with_columns([
        (month / 12.0).cast(pl.Float32).alias("CAL_MONTH"),
        ((month % 2 == 1).cast(pl.Int8) - 0.5).cast(pl.Float32).alias("CAL_MONTH_PARITY"),
        (date % 7 / 7.0).cast(pl.Float32).alias("CAL_WEEKDAY"),
        np.sin(2 * np.pi * doy / 365.0).cast(pl.Float32).alias("CAL_DOY_SIN"),
        np.cos(2 * np.pi * doy / 365.0).cast(pl.Float32).alias("CAL_DOY_COS"),
    ])


def overnight_target(frame: pl.DataFrame) -> pl.DataFrame:
    """Cross-sectional rank of open(t+1)/close(t) - 1 on a non-rectangular frame.

    overnight(t) = OPEN0(t+1) * (1 + y_ret_1d(t)) - 1, taken per stock with a
    one-day lead. The final training day is nulled because its label uses the
    first validation day's open, matching the released fold purge convention.
    """
    overnight = (pl.col("OPEN0").shift(-1).over("ts_code") * (1.0 + pl.col("y_ret_1d")) - 1.0)
    frame = frame.with_columns(overnight.alias("ov_return"))
    frame = frame.with_columns(
        (pl.col("ov_return").rank(method="average").over("trade_date")
         / pl.col("ov_return").count().over("trade_date") - 0.5).alias("ov_rank"))
    last = frame["trade_date"].max()
    return frame.with_columns(
        pl.when(pl.col("trade_date") == last).then(None).otherwise(pl.col("ov_rank"))
        .cast(pl.Float32).alias("ov_rank"))


def gru_oof() -> None:
    path = OUT / "gru_oof.json"
    if path.exists():
        raise SystemExit("GRU out-of-fold cache already recorded; preserving it")
    protocol_path = OUT / "protocol_retrain.json"
    if not protocol_path.exists():
        raise SystemExit("Freeze the retrain protocol first")
    features = feature_names()
    dates, codes, x, y, valid, _ = load_seq_panel(features, 2024)
    record = {"generated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"), "folds": {}}
    search = json.loads((ROOT / "experiments/sequence_ensemble_eval/training.json").read_text(encoding="utf-8"))
    config = search["configuration"]
    for cutoff in GRU_EXTRA_CUTOFFS:
        mean, std, stats = fit_scaler(x, valid, dates, cutoff)
        z = apply_scaler(x, mean, std)
        tensors = st.Tensors(dates, codes, z, y, valid)
        del z
        train_days = tensors.usable_days([t for t, d in enumerate(dates) if d < cutoff],
                                         config["window"])
        target_year = cutoff // 10000 + 1
        outer_days = [t for t, d in enumerate(dates)
                      if target_year * 10000 + 101 <= d <= target_year * 10000 + 1231]
        usable_outer = tensors.usable_days(outer_days, config["window"])
        log(f"GRU cutoff {cutoff}: train {len(train_days)} days -> {target_year} "
            f"({len(usable_outer)} days)")
        model = torch_seed_and_train(tensors, train_days, config)
        raw = st.predict_days(tensors, model, usable_outer, config["window"])
        prediction = np.full((len(outer_days), tensors.stocks), np.nan, dtype=np.float64)
        for row, position in enumerate(outer_days):
            prediction[row] = raw[usable_outer.index(position)]
        cache = OUT / f"gru_oof_{target_year}.parquet"
        pl.DataFrame({"ts_code": [str(c) for c in codes] * len(outer_days),
                      "trade_date": np.repeat([dates[t] for t in outer_days], tensors.stocks),
                      "gru_raw": prediction.reshape(-1)}).write_parquet(cache, compression="zstd")
        record["folds"][str(target_year)] = {"cutoff": cutoff, "train_days": len(train_days),
                                             "cache": cache.relative_to(ROOT).as_posix(),
                                             "cache_sha256": file_hash(cache)}
        del tensors, model
    path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"Wrote {path}")


def torch_seed_and_train(tensors, train_days, config):
    import torch
    torch.manual_seed(SEED)
    model = st.build_model(config["architecture"], tensors.features, config["hidden"]).to(st.DEVICE)
    optimizer = torch.optim.Adam(model.parameters(), lr=st.LEARNING_RATE,
                                 weight_decay=st.WEIGHT_DECAY)
    generator = np.random.default_rng(SEED)
    for epoch in range(config["epochs"]):
        model.train()
        order = generator.permutation(np.asarray(train_days, dtype=np.int64))
        for start in range(0, len(order), st.BATCH_DAYS):
            chunk = order[start:start + st.BATCH_DAYS]
            if len(chunk) < 2:
                continue
            prediction = model(tensors.windows(chunk, config["window"]))
            target, mask = tensors.batch_targets(chunk)
            ic, usable = st.daily_pearson_ic(prediction.view(len(chunk), -1), target, mask)
            if not bool(usable.any()):
                continue
            loss = -ic[usable].mean()
            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            optimizer.step()
    return model


def train() -> None:
    protocol_path = OUT / "protocol_retrain.json"
    if not protocol_path.exists():
        raise SystemExit("Freeze the retrain protocol first")
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    if protocol["source_sha256"] != file_hash(Path(__file__)):
        raise SystemExit("final_sweep_retrain.py changed after its protocol was frozen; stop")
    result_path = OUT / "training_retrain.json"
    if result_path.exists():
        raise SystemExit("Retrain results already recorded; preserving them")
    features = feature_names()
    gru_record = json.loads((OUT / "gru_oof.json").read_text(encoding="utf-8"))
    # Causal GRU feature per target year: the extra out-of-fold GRUs cover
    # 2019-2021 rows, the released phase-2 fold GRUs cover 2022-2024 rows.
    gru_by_year = {int(year): pl.read_parquet(ROOT / item["cache"])
                   .sort("trade_date", "ts_code").rename({"gru_raw": "GRU_RAW"})
                   for year, item in gru_record["folds"].items()}
    for fold_year in FOLD_YEARS:
        gru_by_year[fold_year] = (
            pl.read_parquet(ROOT / f"experiments/sequence_ensemble_eval/nn_raw_{fold_year}.parquet")
            .sort("trade_date", "ts_code").rename({"pred_raw": "GRU_RAW"}))
    record = {"generated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
              "protocol_sha256": file_hash(protocol_path), "candidates": {}}
    lazy = pl.scan_parquet(FEATURE_FILE)
    for candidate in CANDIDATES:
        variant = candidate["variant"]
        record["candidates"][candidate["key"]] = {}
        for year in FOLD_YEARS:
            cutoff = fold_cutoff(year)
            extra = [c for c in ("y_rank", "OPEN0", "y_ret_1d") if c not in features]
            train_frame = (lazy.filter(pl.col("is_train") & (pl.col("trade_date") < cutoff)
                                       & pl.col("price_valid"))
                           .select(KEYS + features + extra)
                           .sort("trade_date", "ts_code").collect())
            valid_frame = (lazy.filter(pl.col("trade_date").is_between(
                year * 10000 + 101, year * 10000 + 1231))
                .select(KEYS + features + ["price_valid", "y_rank"])
                .sort("trade_date", "ts_code").collect())
            use_features = list(features)
            label = train_frame["y_rank"].to_numpy().astype(np.float32)
            if variant == "calendar":
                train_frame = calendar_columns(train_frame)
                valid_frame = calendar_columns(valid_frame)
                use_features += ["CAL_MONTH", "CAL_MONTH_PARITY", "CAL_WEEKDAY",
                                 "CAL_DOY_SIN", "CAL_DOY_COS"]
            if variant == "stacked":
                nan32 = pl.lit(None, dtype=pl.Float32)
                train_frame = (train_frame.with_row_index("ri")
                               .with_columns(nan32.alias("GRU_RAW")))
                for target_year, gframe in gru_by_year.items():
                    kept = train_frame.filter(pl.col("trade_date") // 10000 != target_year)
                    updated = (train_frame.filter(pl.col("trade_date") // 10000 == target_year)
                               .drop("GRU_RAW")
                               .join(gframe.select(KEYS + ["GRU_RAW"]), on=KEYS, how="left")
                               .with_columns(pl.col("GRU_RAW").cast(pl.Float32)))
                    train_frame = pl.concat([kept, updated]).sort("ri")
                train_frame = train_frame.drop("ri")
                gframe = gru_by_year.get(year)
                valid_frame = valid_frame.with_columns(nan32.alias("GRU_RAW"))
                if gframe is not None:
                    valid_frame = (valid_frame.drop("GRU_RAW")
                                   .join(gframe.select(KEYS + ["GRU_RAW"]), on=KEYS, how="left")
                                   .with_columns(pl.col("GRU_RAW").cast(pl.Float32))
                                   .sort("trade_date", "ts_code"))
                use_features += ["GRU_RAW"]
            if variant == "overnight":
                train_frame = overnight_target(train_frame)
                label = train_frame["ov_rank"].to_numpy().astype(np.float32)
            x = to_matrix(train_frame, use_features)
            keep = np.isfinite(label)
            x, label, groups = x[keep], label[keep], train_frame["trade_date"].to_numpy()[keep]
            if variant == "lambdarank":
                # LambdaRank needs graded integer relevance; map the centered
                # daily percentile rank onto 0..63.
                label = np.clip(np.round((label + 0.5) * 63), 0, 63).astype(np.int32)
            params = params_for(variant)
            if variant == "lambdarank":
                unique_days, counts = np.unique(groups, return_counts=True)
                dataset = lgb.Dataset(x, label=label, feature_name=use_features,
                                      group=counts, free_raw_data=True)
            else:
                dataset = lgb.Dataset(x, label=label, feature_name=use_features, free_raw_data=True)
            started = time.monotonic()
            model = lgb.train(params, dataset, num_boost_round=ROUNDS)
            elapsed = time.monotonic() - started
            matrix = to_matrix(valid_frame, use_features)
            raw = model.predict(matrix, num_threads=THREADS).astype(np.float64)
            raw[~valid_frame["price_valid"].to_numpy()] = -1e6
            cache = OUT / f"{candidate['key']}_{year}.parquet"
            valid_frame.select(KEYS).with_columns(pl.Series("pred_raw", raw)).write_parquet(
                cache, compression="zstd")
            record["candidates"][candidate["key"]][str(year)] = {
                "train_rows": int(len(label)), "features": len(use_features),
                "elapsed_seconds": elapsed, "cache": cache.relative_to(ROOT).as_posix(),
                "cache_sha256": file_hash(cache)}
            log(f"{candidate['key']} {year}: rows={len(label):,} feats={len(use_features)} "
                f"{elapsed:.0f}s")
            del train_frame, valid_frame, x, label, dataset, model, matrix
    result_path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"Wrote {result_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("protocol", "gru_oof", "train", "develop"))
    arguments = parser.parse_args()
    if arguments.stage == "protocol":
        OUT.mkdir(parents=True, exist_ok=True)
        path = OUT / "protocol_retrain.json"
        if path.exists():
            raise SystemExit("Retrain protocol already frozen")
        payload = {**PROTOCOL, "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
                   "source_sha256": file_hash(Path(__file__))}
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        log("Froze retrain protocol before any training")
    elif arguments.stage == "gru_oof":
        gru_oof()
    elif arguments.stage == "train":
        train()
    else:
        from experiments.final_sweep_retrain_score import develop_retrain
        develop_retrain()
