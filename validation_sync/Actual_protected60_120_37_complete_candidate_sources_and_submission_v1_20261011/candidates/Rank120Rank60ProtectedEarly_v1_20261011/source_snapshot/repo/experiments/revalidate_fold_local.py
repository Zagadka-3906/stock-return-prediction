"""Retrospective five-year revalidation with training-fold-only feature pruning.

All writes are isolated under revalidation_20260926/validation. No release is
selected here. Freeze the protocol before fitting any new model.
"""
from __future__ import annotations

import argparse
import gc
import hashlib
import json
import os
import tempfile
import time
from pathlib import Path

os.environ.setdefault("POLARS_MAX_THREADS", "8")
os.environ.setdefault("OMP_NUM_THREADS", "8")
import lightgbm as lgb
import numpy as np
import polars as pl
from scipy.stats import rankdata

from evaluate import evaluate
from run import ROOT, FEATURE_FILE, feature_names, fit_model, to_matrix
from src.scoring import Panel
from experiments.cached_recheck import make_prediction
from experiments.official_seed_development import _same_csv_daily
from experiments.return_pooled_models import _target_with_stats
from experiments.final_sweep_significance import contributions, hac_t

OUT = ROOT / "experiments/revalidation_20260926/validation"
YEARS = (2020, 2021, 2022, 2023, 2024)
KEYS = ["ts_code", "trade_date"]
THREADS, ROUNDS, SEED, PRUNE = 8, 180, 2026, 20
SWEEP = ROOT / "experiments/final_sweep_eval"
AUDIT = ROOT / "experiments/extended_audit_eval"
PARAMS = dict(objective="regression", metric="l2", learning_rate=.05,
              num_leaves=31, min_data_in_leaf=300, feature_fraction=.85,
              bagging_fraction=.85, bagging_freq=1, lambda_l2=5., max_bin=127,
              num_threads=THREADS, seed=SEED, verbosity=-1)


def log(message):
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def write_new(path, payload):
    path = Path(path)
    if path.exists():
        raise FileExistsError(f"Preserving existing evidence: {path}")
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def paths(year):
    folder = SWEEP if year >= 2022 else AUDIT
    return {
        "rank_model": ROOT / f"models/fold_{year}.txt" if year >= 2022 else AUDIT / f"models/fold_{year}.txt",
        "rank_cache": ROOT / f"validation/fold_{year}.parquet" if year >= 2022 else AUDIT / f"folds/fold_{year}.parquet",
        "xgboost": folder / f"T2f_xgboost_backbone_{year}.parquet",
        "two_day": folder / f"W2c_two_day_horizon_{year}.parquet",
        "old_pruned": folder / f"W2d_pruned_features_{year}.parquet",
        "pooled": ROOT / f"experiments/return_pooled_eval/return_pooled1_99_{year}.parquet",
        "pooled_metadata": ROOT / f"experiments/return_pooled_eval/return_pooled1_99_{year}.json",
        "xgboost_metadata": folder / "training_extra.json",
        "two_day_metadata": folder / "training_wave2.json",
    }


def original_cache_checks(year):
    p = paths(year)
    checks = {}
    for name, candidate, metadata in (("xgboost", "T2f_xgboost_backbone", "xgboost_metadata"),
                                       ("two_day", "W2c_two_day_horizon", "two_day_metadata"),
                                       ("old_pruned", "W2d_pruned_features", "two_day_metadata")):
        if p[name].exists():
            expected = read(p[metadata])["candidates"][candidate][str(year)]["cache_sha256"]
            actual = digest(p[name])
            if actual != expected:
                raise AssertionError(f"Original cache fingerprint mismatch: {p[name]}")
            checks[name] = {"path": p[name].relative_to(ROOT).as_posix(), "sha256": actual,
                            "verified_against": p[metadata].relative_to(ROOT).as_posix()}
    if p["pooled"].exists():
        metadata = read(p["pooled_metadata"])
        if digest(p["pooled"]) != metadata["cache_sha256"]:
            raise AssertionError("Pooled cache mismatch")
        checks["pooled"] = {"sha256": metadata["cache_sha256"],
                             "training_cutoff_exclusive": metadata["training_cutoff_exclusive"]}
    return checks


def freeze():
    OUT.mkdir(parents=True, exist_ok=True)
    if (OUT / "protocol.json").exists():
        raise FileExistsError("Protocol already frozen")
    sources = [Path(__file__), ROOT / "run.py", ROOT / "evaluate.py", ROOT / "src/scoring.py",
               ROOT / "src/features.py", ROOT / "experiments/cached_recheck.py",
               ROOT / "experiments/official_seed_development.py",
               ROOT / "experiments/return_pooled_models.py",
               ROOT / "experiments/return_head_models.py", ROOT / "experiments/seed_ensemble.py",
               ROOT / "experiments/final_sweep_significance.py", FEATURE_FILE,
               ROOT / "data/feature_manifest.json", ROOT / "data" / "raw" / "训练集.csv", ROOT / "active_release.json",
               ROOT / "models/final_lightgbm.txt", ROOT / "releases/ensemble4/W2d_pruned.txt"]
    for year in YEARS:
        sources.extend(p for p in paths(year).values() if p.exists())
    sources = list(dict.fromkeys(sources))
    payload = {
        "experiment": "fixed_five_year_fold_local_feature_selection_revalidation",
        "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "years": list(YEARS), "all_years_previously_viewed": True,
        "candidates": ["baseline", "xgboost", "ensemble4"],
        "diagnostic_only": "old_ensemble4 reconstructed with old pruned cache, same pooled stack; not a new selection candidate",
        "selection": "Gain comes solely from the saved rank model fitted BEFORE this fold. Drop lowest 20; ties by feature name. No full-history feature importance for historical folds.",
        "postprocess": {"alpha": .9, "bonus": .3, "restore_lower": True,
                        "top_current_weight": 1., "pooled_top_only_weight": .25},
        "parameters": PARAMS, "rounds": ROUNDS, "seed": SEED,
        "reuse": "Hash-verified old rank, XGBoost and two-day raw caches are permitted. Saved rank model gains are fold-specific. Missing caches are rebuilt with fixed recipes.",
        "auxiliary": "Same pooled RMS target and 180-round model on each year's purged training fold; 2020/2021 fitted anew, 2022-2024 frozen caches reused",
        "one_day_purge": "Last one calendar training day before validation removed; label end strictly before first validation day",
        "two_day_purge": "Retain old recipe's conservative three removed prevalidation trading days (one-day cutoff plus two further dates); t+2 label end strictly before validation",
        "embargo": "No future/postvalidation training samples exist in expanding windows; no additional postvalidation embargo is needed",
        "training_order": "Original stock-major cache order for rank/pooled; date/code order for XGBoost, two-day and pruned members, matching original recipes",
        "tests": ["Real-data future-label poisoning leaves filtered full training keys/labels exact",
                  "Real-data fixture train/refit with poisoned validation/future labels gives identical gain selection",
                  "Each training label available before validation begins",
                  "Saved fold rank model reproduces 4096 cached predictions",
                  "Prediction label perturbation and 50-day prefix invariance",
                  "2022-2024 baseline official score equals frozen release"],
        "reporting": "All years and all fixed candidates; paired daily HAC lags 5/10/20, selection bias uncorrected; no automatic release switch",
        "input_sha256": {p.relative_to(ROOT).as_posix(): digest(p) for p in sources},
        "original_cache_checks": {str(y): original_cache_checks(y) for y in YEARS},
    }
    write_new(OUT / "protocol.json", payload)
    log("Frozen protocol and verified cache fingerprints before training")


def verify_protocol():
    protocol = read(OUT / "protocol.json")
    for relative, expected in protocol["input_sha256"].items():
        if digest(ROOT / relative) != expected:
            raise AssertionError(f"Frozen input changed: {relative}")
    return protocol


def calendar():
    return (pl.scan_parquet(FEATURE_FILE).filter(pl.col("is_train"))
            .select("trade_date").unique().sort("trade_date").collect()["trade_date"].to_numpy())


def boundaries(year, dates):
    first = int(np.searchsorted(dates, year * 10000 + 101))
    return {"validation_first": int(dates[first]), "one_day_cutoff_exclusive": int(dates[first - 1]),
            "one_day_last": int(dates[first - 2]), "one_day_label_available": int(dates[first - 1]),
            "two_day_cutoff_exclusive": int(dates[first - 3]),
            "two_day_last": int(dates[first - 4]), "two_day_label_available": int(dates[first - 2]),
            "one_day_purged_dates": [int(dates[first - 1])],
            "two_day_purged_dates": [int(x) for x in dates[first - 3:first]]}


def filter_training(lazy, cutoff):
    return lazy.filter(pl.col("is_train") & (pl.col("trade_date") < cutoff)
                       & pl.col("price_valid") & pl.col("y_rank").is_not_null())


def prune_names(model, features):
    gains = dict(zip(model.feature_name(), map(float, model.feature_importance(importance_type="gain"))))
    dropped = sorted(features, key=lambda f: (gains[f], f))[:PRUNE]
    kept = [f for f in features if f not in set(dropped)]
    return kept, dropped, gains


def target_hash(frame):
    h = hashlib.sha256(frame.select(KEYS).write_csv().encode("utf-8"))
    for column in ("y_rank", "y_ret_1d"):
        h.update(frame[column].to_numpy().tobytes())
    return h.hexdigest()


def invariant_tests(year, bound, features):
    lazy = pl.scan_parquet(FEATURE_FILE)
    cutoff = bound["one_day_cutoff_exclusive"]
    poisoned = lazy.with_columns(*[
        pl.when(pl.col("trade_date") >= cutoff).then(pl.lit(12345., dtype=pl.Float32))
        .otherwise(pl.col(c)).alias(c) for c in ("y_rank", "y_ret_1d")])
    columns = KEYS + ["y_rank", "y_ret_1d"]
    clean = filter_training(lazy, cutoff).select(columns).collect()
    changed = filter_training(poisoned, cutoff).select(columns).collect()
    assert clean.equals(changed), "Future-label poisoning changed full training data"
    rows = len(clean)
    full_hash = target_hash(clean)
    del clean, changed
    # Real observations on both sides of the boundary enter the test wrapper.
    fixture = pl.concat([
        filter_training(lazy, cutoff).select(features + columns + ["is_train", "price_valid"]).head(24000).collect(),
        lazy.filter(pl.col("trade_date") >= cutoff).select(features + columns + ["is_train", "price_valid"]).head(12000).collect(),
    ])
    altered = fixture.with_columns(*[
        pl.when(pl.col("trade_date") >= cutoff).then(pl.lit(-98765., dtype=pl.Float32))
        .otherwise(pl.col(c)).alias(c) for c in ("y_rank", "y_ret_1d")])
    selected = []
    arrays = []
    for data in (fixture, altered):
        train = filter_training(data.lazy(), cutoff).collect()
        booster = fit_model(to_matrix(train, features), train["y_rank"].to_numpy(), features, 12, THREADS)
        selected.append(prune_names(booster, features)[:2])
        arrays.append(booster.feature_importance(importance_type="gain"))
    assert selected[0] == selected[1] and np.array_equal(*arrays)
    assert bound["one_day_label_available"] < bound["validation_first"]
    assert bound["two_day_label_available"] < bound["validation_first"]
    return {"all_training_rows": rows, "full_training_keys_labels_sha256": full_hash,
            "future_label_poisoning_full_training_exact": True,
            "real_fixture_gain_and_selected_features_exact_after_poisoning": True,
            "fixture_rows": len(fixture), "fixture_training_rounds": 12,
            "label_availability_before_validation": True}


def load_raw(path, keys):
    frame = pl.read_parquet(path).sort("trade_date", "ts_code")
    assert frame.select(KEYS).equals(keys), f"Cache key mismatch {path}"
    return frame["pred_raw"].to_numpy().astype(np.float64)


def save_model_predict(frame, features, target, valid, name, year, float32=False):
    log(f"{year} training {name}: {len(frame):,} rows x {len(features)} features")
    matrix = to_matrix(frame, features)
    booster = lgb.train(PARAMS, lgb.Dataset(matrix, label=target, feature_name=features), num_boost_round=ROUNDS)
    model_path = OUT / f"model_{name}_{year}.txt"
    model_path.write_text(booster.model_to_string(), encoding="utf-8")
    del matrix, booster
    gc.collect()
    reloaded = lgb.Booster(model_str=model_path.read_text(encoding="utf-8"))
    raw = reloaded.predict(to_matrix(valid, features), num_threads=THREADS)
    if float32:
        raw = raw.astype(np.float32)
    raw[~valid["price_valid"].to_numpy()] = -1e6
    valid.select(KEYS).with_columns(pl.Series("pred_raw", raw)).write_parquet(OUT / f"raw_{name}_{year}.parquet")
    return raw.astype(np.float64), {"training_rows": len(frame), "model_sha256": digest(model_path)}


def rank_average(raws, valid, n_codes):
    matrices = [np.asarray(r).reshape(-1, n_codes) for r in raws]
    mask = valid.reshape(-1, n_codes)
    out = np.full(mask.shape, -10., dtype=np.float64)
    for day in range(len(mask)):
        keep = mask[day].copy()
        for matrix in matrices:
            keep &= np.isfinite(matrix[day])
        count = int(keep.sum())
        if count:
            out[day, keep] = sum(rankdata(m[day, keep], method="average") / count for m in matrices) / len(matrices)
    return out.reshape(-1)


def score_official(frame, prediction):
    with tempfile.TemporaryDirectory(prefix="fold-local-score-") as tmp:
        folder = Path(tmp)
        frame.select(KEYS).with_columns(pl.Series("pred", prediction)).write_csv(folder / "submission.csv", float_precision=17)
        frame.select(KEYS + ["flag_limit_up"]).write_csv(folder / "测试集_X.csv")
        frame.select(KEYS + ["y_ret_1d"]).write_csv(folder / "测试集_Y.csv", float_precision=17)
        metrics = {k: float(v) for k, v in evaluate(str(folder / "submission.csv"), str(folder)).items()}
        rebuilt, daily = _same_csv_daily(folder)
        assert all(abs(metrics[k] - rebuilt[k]) <= 1e-12 for k in metrics)
    return metrics, daily


def paired(left, right):
    names = ("rank_ic", "excess", "turnover")
    values = contributions({n: left[n].to_numpy() for n in names}, {n: right[n].to_numpy() for n in names})
    results = {"score_delta": float(values.sum()), "days": len(values), "selection_bias_corrected": False}
    for lag in (5, 10, 20):
        mean, se, statistic = hac_t(values, lag)
        results[f"hac{lag}"] = {"t": statistic, "score_delta_ci95": [(mean - 1.96 * se) * len(values), (mean + 1.96 * se) * len(values)]}
    return results


def run_year(year, features, dates):
    destination = OUT / f"result_{year}.json"
    if destination.exists():
        log(f"{year} completed result preserved")
        return read(destination)
    started = time.monotonic()
    p, bound = paths(year), boundaries(year, dates)
    checks = invariant_tests(year, bound, features)
    lazy = pl.scan_parquet(FEATURE_FILE)
    valid = (lazy.filter(pl.col("is_train") & pl.col("trade_date").is_between(year*10000+101, year*10000+1231))
             .select(KEYS + features + ["price_valid"]).sort("trade_date", "ts_code").collect())
    keys = valid.select(KEYS)
    base_frame = (pl.scan_csv(ROOT / "data" / "raw" / "训练集.csv", schema_overrides={"ts_code": pl.String,
                    "trade_date": pl.Int32, "y_ret_1d": pl.Float64, "close": pl.Float64}, null_values=["NaN", "nan", ""])
                  .filter(pl.col("trade_date").is_between(year*10000+101, year*10000+1231))
                  .select(KEYS + ["close", "flag_limit_up", "y_ret_1d"]).sort("trade_date", "ts_code").collect())
    assert base_frame.select(KEYS).equals(keys)
    base_frame = base_frame.with_columns(valid["price_valid"])
    metadata = {"year": year, "retrospective_previously_viewed": True, "boundaries": bound,
                "tests": checks, "cache_sources": original_cache_checks(year), "models": {}}
    if not p["rank_model"].exists():
        frame = filter_training(lazy, bound["one_day_cutoff_exclusive"]).select(features + ["y_rank"]).collect()
        rank, item = save_model_predict(frame, features, frame["y_rank"].to_numpy(), valid, "rank", year, True)
        rank_model_path = OUT / f"model_rank_{year}.txt"
        metadata["models"]["rank"] = item
        del frame
    else:
        rank_model_path = p["rank_model"]
        rank_model = lgb.Booster(model_str=rank_model_path.read_text(encoding="utf-8"))
        if p["rank_cache"].exists():
            rank = load_raw(p["rank_cache"], keys)
        else:
            rank = rank_model.predict(to_matrix(valid, features), num_threads=THREADS).astype(np.float32).astype(np.float64)
            rank[~valid["price_valid"].to_numpy()] = -1e6
        indices = np.linspace(0, len(valid)-1, 4096, dtype=int)
        sample = rank_model.predict(to_matrix(valid[indices], features), num_threads=THREADS).astype(np.float32)
        sample[~valid["price_valid"].to_numpy()[indices]] = -1e6
        assert np.array_equal(sample.astype(float), rank[indices]), "Saved rank model/cache disagree"
        checks["rank_reload_4096_exact"] = True
    rank_model = lgb.Booster(model_str=rank_model_path.read_text(encoding="utf-8"))
    kept, dropped, gains = prune_names(rank_model, features)
    metadata["feature_selection"] = {"selector_model": rank_model_path.relative_to(ROOT).as_posix(),
                                      "selector_sha256": digest(rank_model_path), "gain": gains,
                                      "kept": kept, "dropped": dropped, "uses_future_labels": False}
    del rank_model
    frame = (filter_training(lazy, bound["one_day_cutoff_exclusive"]).select(KEYS + kept + ["y_rank"])
             .sort("trade_date", "ts_code").collect())
    pruned, item = save_model_predict(frame, kept, frame["y_rank"].to_numpy(), valid, "fold_local_pruned", year)
    metadata["models"]["fold_local_pruned"] = item
    del frame
    gc.collect()
    if p["pooled"].exists():
        aux = load_raw(p["pooled"], keys)
        item = read(p["pooled_metadata"])
        assert item["training_cutoff_exclusive"] == bound["one_day_cutoff_exclusive"]
        metadata["models"]["pooled"] = {"reused": True, "training_rows": item["training_rows"], "target_stats": item["target_stats"]}
    else:
        frame = filter_training(lazy, bound["one_day_cutoff_exclusive"]).select(KEYS + features + ["y_ret_1d"]).collect()
        target, target_stats = _target_with_stats(frame["trade_date"].to_numpy(), frame["y_ret_1d"].to_numpy())
        aux, item = save_model_predict(frame, features, target, valid, "pooled", year, True)
        metadata["models"]["pooled"] = {**item, "target_stats": target_stats, "reused": False}
        del frame, target
        gc.collect()
    if p["xgboost"].exists():
        xgb_raw = load_raw(p["xgboost"], keys)
    else:
        import xgboost as xgb
        frame = (filter_training(lazy, bound["one_day_cutoff_exclusive"]).select(KEYS + features + ["y_rank"])
                 .sort("trade_date", "ts_code").collect())
        model = xgb.XGBRegressor(n_estimators=ROUNDS, max_depth=7, learning_rate=.05,
                                 subsample=.85, colsample_bytree=.85, reg_lambda=5., tree_method="hist", seed=SEED, n_jobs=THREADS)
        model.fit(to_matrix(frame, features), frame["y_rank"].to_numpy())
        model.save_model(OUT / f"model_xgboost_{year}.ubj")
        xgb_raw = model.predict(to_matrix(valid, features)).astype(np.float64)
        xgb_raw[~valid["price_valid"].to_numpy()] = -1e6
        del frame, model
        gc.collect()
    if p["two_day"].exists():
        two_raw = load_raw(p["two_day"], keys)
    else:
        frame = (lazy.sort("ts_code", "trade_date").with_columns(
                    (.5*pl.col("y_rank") + .5*pl.col("y_rank").shift(-1).over("ts_code")).alias("two_target"))
                 .filter(pl.col("is_train") & pl.col("price_valid")
                         & (pl.col("trade_date") < bound["two_day_cutoff_exclusive"]) & pl.col("two_target").is_finite())
                 .select(KEYS + features + ["two_target"]).sort("trade_date", "ts_code").collect())
        two_raw, item = save_model_predict(frame, features, frame["two_target"].to_numpy(), valid, "two_day", year)
        metadata["models"]["two_day"] = item
        del frame
        gc.collect()
    n_codes = base_frame["ts_code"].n_unique()
    valid_mask = valid["price_valid"].to_numpy()
    raw_candidates = {"baseline": rank, "xgboost": xgb_raw,
                      "ensemble4": rank_average([rank, xgb_raw, two_raw, pruned], valid_mask, n_codes)}
    if p["old_pruned"].exists():
        old_raw = load_raw(p["old_pruned"], keys)
        raw_candidates["old_ensemble4"] = rank_average([rank, xgb_raw, two_raw, old_raw], valid_mask, n_codes)
    del valid
    gc.collect()
    metadata["metrics"] = {}
    daily_results = {}
    for name, raw in raw_candidates.items():
        panel = Panel.from_frame(base_frame.with_columns(pl.Series("pred_raw", raw)))
        pred = make_prediction(panel, aux, "top_only", .25)
        poisoned_panel = Panel.from_frame(panel.frame.with_columns(pl.lit(-123.).alias("y_ret_1d")))
        assert np.array_equal(pred, make_prediction(poisoned_panel, aux, "top_only", .25))
        prefix_rows = 50 * panel.rows_per_day
        prefix = Panel.from_frame(panel.frame.head(prefix_rows))
        assert np.array_equal(pred[:prefix_rows], make_prediction(prefix, aux[:prefix_rows], "top_only", .25))
        output = panel.frame.with_columns(pl.Series("pred", pred), pl.Series("aux_raw", aux))
        output.write_parquet(OUT / f"predictions_{name}_{year}.parquet", compression="zstd")
        metrics, daily = score_official(base_frame, pred)
        metadata["metrics"][name] = metrics
        daily_results[name] = daily
        daily.write_csv(OUT / f"daily_{name}_{year}.csv")
        if name == "ensemble4" and year == 2024:
            daily.write_csv(OUT / "corrected_2024_daily.csv")
        log(f"{year} {name}: score={metrics['final_score']:.9f}")
        del panel, pred, output, poisoned_panel, prefix
    checks["all_prediction_label_and_50day_prefix_invariance"] = True
    if year >= 2022:
        baseline_expected = read(ROOT / "experiments/return_pooled_eval/decision.json")["years"][str(year)]["candidate_score"]
        assert abs(metadata["metrics"]["baseline"]["final_score"] - baseline_expected) <= 1e-12
        checks["baseline_frozen_score_exact"] = True
        old_expected = read(ROOT / "releases/ensemble4/release_manifest.json")["historical_official_metrics"][str(year)]["final_score"]
        assert abs(metadata["metrics"]["old_ensemble4"]["final_score"] - old_expected) <= 1e-12
        checks["old_ensemble_frozen_score_exact"] = True
    metadata["paired"] = {f"{name}_minus_baseline": paired(daily_results[name], daily_results["baseline"])
                          for name in ("xgboost", "ensemble4")}
    if "old_ensemble4" in daily_results:
        metadata["paired"]["corrected_minus_old_ensemble4"] = paired(daily_results["ensemble4"], daily_results["old_ensemble4"])
    metadata["elapsed_seconds"] = time.monotonic() - started
    metadata["artifacts_sha256"] = {p.name: digest(p) for p in OUT.glob(f"*_{year}.*") if p != destination}
    write_new(destination, metadata)
    log(f"YEAR COMPLETE {year} ({metadata['elapsed_seconds']:.1f}s)")
    return metadata


def summarize(results):
    summary = {"protocol_sha256": digest(OUT / "protocol.json"), "all_years_previously_viewed": True,
               "all_folds_include_pooled_auxiliary": True, "automatic_release_switch": False,
               "year_results": {str(r["year"]): r for r in results}, "aggregate": {},
               "metrics": {str(r["year"]): r["metrics"] for r in results},
               "paired_HAC": {str(r["year"]): r["paired"] for r in results},
               "vs_old_ensemble": {str(r["year"]): r["paired"].get("corrected_minus_old_ensemble4") for r in results},
               "corrected_2024_daily": "experiments/revalidation_20260926/validation/corrected_2024_daily.csv"}
    for name in ("xgboost", "ensemble4"):
        deltas = [r["metrics"][name]["final_score"] - r["metrics"]["baseline"]["final_score"] for r in results]
        summary["aggregate"][name] = {"deltas": dict(zip(map(str, YEARS), deltas)),
                                      "mean_delta": float(np.mean(deltas)), "min_delta": min(deltas),
                                      "positive_years": int(sum(d > 1e-12 for d in deltas))}
    final_model = lgb.Booster(model_str=(ROOT / "models/final_lightgbm.txt").read_text(encoding="utf-8"))
    full_kept, full_dropped, _ = prune_names(final_model, feature_names())
    shipped_pruned = lgb.Booster(model_str=(ROOT / "releases/ensemble4/W2d_pruned.txt").read_text(encoding="utf-8"))
    summary["final_inference_feature_selection"] = {
        "full_training_selector_features": full_kept, "dropped": full_dropped,
        "equals_shipped_pruned_feature_order": full_kept == shipped_pruned.feature_name(),
        "note": "Full-history selection is appropriate for final test inference; this correction concerns historical evaluation only. No release model/prediction was changed."}
    summary["final_feature_selection_matches_shipped_model"] = full_kept == shipped_pruned.feature_name()
    summary["limitations"] = ["Retrospective previously viewed years; no new blind holdout or hidden test score",
        "Frozen model design and hyperparameters already reflect past experiments; fold-local selection fixes this specific leakage only",
        "Paired HAC intervals do not correct cumulative candidate selection",
        "Official return and turnover eligibility differ; metrics are not executable net portfolio returns",
        "2020/2021 include newly fitted pooled auxiliary, so only within-year same-stack comparisons are commensurate",
        "Historical reused caches have original provenance and verified hashes; new models use 8 threads"]
    write_new(OUT / "summary.json", summary)
    lines = ["# 训练折内特征筛选：五年回顾性复核", "", "本轮固定三个方案，所有年份均已被历史研究查看。五年统一使用 pooled 辅助头和25% Top内融合；没有重新选参、切换正式发布或修改旧记录。", "",
             "| 年份 | pooled基线 | XGBoost | 修正后四模型 | 原剪枝四模型（同口径） | 修正集成−基线 |", "|---|---:|---:|---:|---:|---:|"]
    for r in results:
        m=r["metrics"]
        lines.append(f"| {r['year']} | {m['baseline']['final_score']:.9f} | {m['xgboost']['final_score']:.9f} | {m['ensemble4']['final_score']:.9f} | {m['old_ensemble4']['final_score']:.9f} | {m['ensemble4']['final_score']-m['baseline']['final_score']:+.9f} |")
    lines += ["", "修正只改变历史折剪枝成员的列选择：每折从该折训练期模型的gain去除最低20列，再重训该折剪枝成员。原先全期重要性不参与历史列选择。", ""]
    for name, a in summary["aggregate"].items():
        lines.append(f"- {name}：五年平均增量 {a['mean_delta']:+.9f}，最差年 {a['min_delta']:+.9f}，{a['positive_years']}/5 年为正。")
    lines += ["", "完整分项、按年配对HAC区间、修正相对旧集成的影响、每折gain/入选列/时间边界/源指纹见 summary.json 和 result_<year>.json。区间未校正累计选模，不能称为新盲测显著性。", "", "最终全训练期剪枝与历史验证必须区分。正式最终模型使用其全训练期信息合法；本轮仅纠正回顾性检验，保持正式发布不动。", "", "所有真实数据标签投毒不变性、模型重载、标签可得日、前缀及基线原版评分检查均通过。"]
    (OUT / "结论.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    log("All five folds complete; summary and Chinese conclusion written")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("freeze", "run"))
    args = parser.parse_args()
    if args.stage == "freeze":
        freeze()
        return
    verify_protocol()
    if (OUT / "summary.json").exists():
        raise FileExistsError("Completed summary already exists")
    features, dates = feature_names(), calendar()
    results = []
    for year in YEARS:
        results.append(run_year(year, features, dates))
        gc.collect()
    verify_protocol()
    summarize(results)


if __name__ == "__main__":
    main()
