"""Wave-9 exploratory round: two information axes that no earlier round touched.

The user asked for further optimization after wave-8 closed the combination-rule and
post-processing axes. A read-only survey of every feature-building and auxiliary-head
module in this repository established that exactly two axes are still open:

  A. Extended features from the same OHLCV panel. The base 63 columns use rolling
     windows of 5/10/20/60 days only, and the single prior expansion round added
     price-volume and market-relative columns at 20/60 days. Nothing anywhere exceeds
     a 60-day window; return skewness, kurtosis and autocorrelation do not exist; the
     overnight gap appears only as a failed prediction TARGET and never as an input
     (base OPEN0 is the same-day open/close); and no column encodes path shape.
     `experiments/wave9_features.py` builds twenty such columns with an independent
     numpy reference, prefix invariance and label-poisoning tests.

  B. The identity of the auxiliary signal. The blend WEIGHT (0.0-1.0) and MODE axes are
     closed, and six alternative auxiliary formulations were scored, but every one of
     them is a REGRESSION on a return target. A binary "will this stock be in tomorrow's
     top decile" classifier has never been fitted anywhere in this project, and it is the
     only formulation that targets the 30% Top-excess term directly instead of through a
     return regression.

Everything else — post-processing, targets, feature transforms, model families,
ensembling rules, weights and nested hyperparameter selection — carries a frozen
negative record and is not re-proposed here.

DISCIPLINE. All five years have been examined repeatedly, so this round is
**exploratory by construction** and cannot produce a significance claim. It borrows the
r5 protocol's shape so the numbers stay comparable: 2020-2022 select one candidate,
2023-2024 confirm it once, pre-frozen thresholds, no fallback, no re-tuning. It writes
only inside `experiments/wave9_exploratory_20260927/` and never touches `releases/`,
`outputs/`, `active_release.json`, `maintenance/` or any frozen evidence directory.
"""
from __future__ import annotations

import argparse
import gc
import hashlib
import json
import time
from pathlib import Path

import lightgbm as lgb
import numpy as np
import polars as pl

from run import ROOT, FEATURE_FILE, feature_names, to_matrix
from src.scoring import Panel
from experiments.audit_r5_candidate import paired_block_bootstrap
from experiments.cached_recheck import make_prediction
from experiments.optimize_r5_models import load_year
from experiments.revalidate_fold_local import (PARAMS, ROUNDS, THREADS, boundaries, calendar,
                                               filter_training, paired, score_official)
from experiments.wave9_features import GROUPS, NEW_FEATURES, OUT, PANEL_FILE, file_hash, log

R4 = ROOT / "experiments" / "revalidation_20260926" / "validation"
R5 = ROOT / "experiments" / "optimization_r5_20260926"
KEYS = ["ts_code", "trade_date"]
YEARS = (2020, 2021, 2022, 2023, 2024)
DEVELOPMENT = (2020, 2021, 2022)
CONFIRMATION = (2023, 2024)
BASE_FEATURES = feature_names()
EXTENDED_FEATURES = [*BASE_FEATURES, *NEW_FEATURES]
JOINED_PANEL = OUT / "panel_extended.parquet"
TOP_DECILE_THRESHOLD = 0.4
BINARY_PARAMS = {**PARAMS, "objective": "binary", "metric": "auc"}
XGB_CONFIG = {"rounds": 180, "max_depth": 7, "learning_rate": 0.05, "subsample": 0.85,
              "colsample_bytree": 0.85, "reg_lambda": 5.0, "tree_method": "hist", "seed": 2026,
              "n_jobs": 16}
# References are frozen artifacts, re-anchored to their recorded metrics before any scoring.
REFERENCES = {
    "baseline": {"daily": R4, "metrics": ("r4_result", "baseline"), "predictions": R4},
    "ensemble4": {"daily": R4, "metrics": ("r4_result", "ensemble4"), "predictions": R4},
    "xgboost": {"daily": R4, "metrics": ("r4_result", "xgboost"), "predictions": R4},
    "xgb_two_mean": {"daily": R5, "metrics": ("r5_fold", "xgb_two_mean"), "predictions": R5},
}
DEVELOPMENT_REFERENCES = ("baseline", "xgboost", "ensemble4")
CONFIRMATION_REFERENCES = ("baseline", "xgboost", "ensemble4", "xgb_two_mean")
BOOTSTRAP_REFERENCES = ("baseline", "xgb_two_mean")
CANDIDATES = {
    "W9a_lgb_ext": {"axis": "features", "backbone": "lightgbm_rank", "features": "extended",
                    "models": 1, "auxiliary": "frozen_pooled",
                    "note": "the released LightGBM rank recipe on the 83-column panel"},
    "W9b_topdecile_aux": {"axis": "auxiliary", "backbone": "frozen_baseline", "features": "base",
                          "models": 1, "auxiliary": "binary_top_decile",
                          "note": "released backbone, auxiliary replaced by a binary next-day "
                                  "top-decile classifier blended top_only at the released 0.25"},
    "W9c_xgb_ext": {"axis": "features", "backbone": "xgboost", "features": "extended",
                    "models": 1, "auxiliary": "frozen_pooled",
                    "note": "the frozen T2f XGBoost recipe on the 83-column panel"},
    "W9d_ext_two_mean": {"axis": "features+combination", "backbone": "rank_average",
                         "features": "extended", "models": 2, "auxiliary": "frozen_pooled",
                         "note": "equal-weight cross-sectional rank average of W9a and W9c, the "
                                 "same rule as the r5 winner and the adopted ensemble"},
}
GATES = {
    "development": {"mean_score_delta_min": .001, "worst_year_score_delta_min": -.005,
                    "mean_ic_delta_min": -.002, "references": list(DEVELOPMENT_REFERENCES)},
    "confirmation": {"mean_score_delta_min": .0005, "worst_year_score_delta_min": -.003,
                     "mean_ic_delta_min": -.002, "references": list(CONFIRMATION_REFERENCES)},
    "bootstrap": {"block_days": 20, "draws": 20000, "seed": 2026, "positive_share_min": .80,
                  "references": list(BOOTSTRAP_REFERENCES)},
}
def protocol_references() -> dict:
    """JSON-safe view of the frozen reference artifact locations."""
    return {name: {"daily": str(spec["daily"].relative_to(ROOT).as_posix()),
                   "metrics": list(spec["metrics"]),
                   "predictions": str(spec["predictions"].relative_to(ROOT).as_posix())}
            for name, spec in REFERENCES.items()}


PROTOCOL = {
    "experiment": "wave9_exploratory_extended_features_and_binary_auxiliary",
    "status": "exploratory_all_years_previously_viewed",
    "candidates": CANDIDATES, "new_features": NEW_FEATURES, "feature_groups": GROUPS,
    "base_feature_count": len(BASE_FEATURES), "extended_feature_count": len(EXTENDED_FEATURES),
    "development_years": list(DEVELOPMENT), "confirmation_years": list(CONFIRMATION),
    "gates": GATES, "references": None,
    "candidate_selection": "Among candidates passing EVERY development threshold against EVERY "
                           "development reference, take the highest equally weighted mean annual "
                           "official score. Exact ties: fewer models, then lexical key. Select "
                           "exactly one or none. xgb_two_mean is reported but NOT gated on "
                           "development years because it was itself selected there.",
    "confirmation_rule": "Score only the frozen development winner on 2023 and 2024, once. Every "
                         "confirmation threshold against all four references AND the block "
                         "bootstrap against both bootstrap references must pass. No fallback to "
                         "another candidate, no re-tuning, no second winner.",
    "postprocess": "the released stack exactly: alpha 0.9 EMA on daily percentile ranks, "
                   "persistence bonus 0.3, protected-block restoration at top_current_weight 1.0, "
                   "then the 25% top-only pooled blend, via cached_recheck.make_prediction",
    "auxiliary": "frozen pooled RMS head from the r4 fold frame for every candidate except W9b, "
                 "which substitutes a binary top-decile classifier fitted on the same purged fold "
                 "with the same hyper-parameters apart from the objective",
    "training": "LightGBM rank/binary: PARAMS and 180 rounds from revalidate_fold_local, trained on "
                "the unsorted stock-major order, predicted from the RELOADED model file. XGBoost: "
                "the frozen T2f recipe on the date/code-sorted order. One-day purge boundary from "
                "the r4 fold record; no future importance pruning; no test-period rows.",
    "scorer": "the unmodified evaluate.py via revalidate_fold_local.score_official, which also "
              "rebuilds the daily evidence from the same CSVs and asserts agreement to 1e-12",
    "harness_proofs_required_before_any_candidate_scoring": [
        "the extended panel's keys equal the base panel's training-row keys in file order",
        "retraining the released LightGBM rank recipe on the 63 BASE features through the joined "
        "panel reproduces the frozen r4 baseline raw prediction for 2022 bit-for-bit, which also "
        "proves the join did not misalign a single row. On the audit-year folds the frozen rank "
        "model came from an earlier round's code path and agrees only to float-histogram noise, "
        "measured before any candidate existed (2020: max |diff| 1.16e-02 on the raw scale, mean "
        "|diff| 3.7e-07, correlation 0.999999831, minimum daily Spearman 0.999989138, mean Top-10% "
        "Jaccard 0.999977695, worst-day Top-10% Jaccard 0.994579946, composite 0.431472523 against "
        "the recorded 0.431472733, i.e. −2.1e-07). There the hard requirements are instead: minimum "
        "daily Spearman >= 0.999, mean Top-10% Jaccard >= 0.999, worst-day Top-10% Jaccard >= 0.99, "
        "and the composite of the retrained raw through the released stack within 1e-5 of the "
        "recorded baseline composite. The composite bound is the decision-relevant one: 50x tighter "
        "than the measured discrepancy and 50x smaller than the loosest gate threshold",
        "make_prediction on that raw with the frozen auxiliary reproduces the frozen r4 baseline "
        "final prediction exactly, and scores to the recorded composite within 1e-12",
        "every reference composite rebuilt from its frozen daily CSV equals its recorded metric "
        "within 1e-9",
    ],
    "invariants_per_candidate": ["label perturbation leaves predictions exact",
                                 "a 50-day prefix is exact", "all predictions finite",
                                 "price-invalid rows score below -1",
                                 "training rows end strictly before the validation year and every "
                                 "training label is available before validation begins"],
    "prohibited": ["Adding candidates, features or thresholds after any score exists",
                   "Selecting a second winner after confirmation",
                   "Retuning any hyper-parameter of any learner",
                   "Writing outside experiments/wave9_exploratory_20260927/",
                   "Touching releases/, outputs/, active_release.json or maintenance/",
                   "Quoting any number here as out-of-sample evidence"],
    "limitations": [
        "All five years have been examined by eight earlier suites, the r4 revalidation and the r5 "
        "round; a pass here is evidence against a fluke, not proof of edge.",
        "The 120-day features are null on 21.5-23.8% of rows because a single missing price inside "
        "the window voids it under the base min_samples convention, so they also act as a "
        "trading-gap indicator; that is recorded, not removed.",
        "No bootstrap or HAC interval corrects for cumulative candidate selection.",
        "The extended panel covers training rows only, so this round cannot produce a submission. "
        "Adopting any candidate would require rebuilding the panel over the test file first.",
        "On the 2020/2021 folds the frozen baseline rank model was produced by an earlier round's "
        "code path, so this round's candidates are trained through the corrected revalidation "
        "filter while that one reference raw was not. The measured effect of that difference on the "
        "identical recipe is −2.1e-07 on the 2020 composite, four orders below the smallest gate.",
    ],
}


def sha(path: Path) -> str:
    return file_hash(Path(path))


def read(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def write_new(path: Path, payload) -> None:
    with Path(path).open("x", encoding="utf-8") as stream:
        json.dump(payload, stream, ensure_ascii=False, indent=2, allow_nan=False)


def joined_panel() -> None:
    """Materialize base+extended once, in the base panel's own stock-major file order."""
    OUT.mkdir(parents=True, exist_ok=True)
    if JOINED_PANEL.exists():
        log(f"Reusing {JOINED_PANEL.name}")
        return
    started = time.monotonic()
    base = pl.read_parquet(FEATURE_FILE).filter(pl.col("is_train"))
    extended = pl.read_parquet(PANEL_FILE)
    joined = base.join(extended, on=KEYS, how="left", validate="1:1").sort("ts_code", "trade_date")
    if joined.height != base.height:
        raise AssertionError("Join changed the row count")
    expected = base.select(KEYS)
    if not joined.select(KEYS).equals(expected):
        raise AssertionError("Join did not preserve the base panel's stock-major row order")
    missing = joined.select([pl.col(name).is_null().sum().alias(name)
                             for name in NEW_FEATURES]).to_dicts()[0]
    if any(value == joined.height for value in missing.values()):
        raise AssertionError(f"A new feature is entirely null: {missing}")
    keep = KEYS + ["row_id", "is_train", "y_ret_1d", "y_rank", "price_valid"] + EXTENDED_FEATURES
    joined.select(keep).write_parquet(JOINED_PANEL, compression="zstd", compression_level=3)
    payload = {"built_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "seconds": round(time.monotonic() - started, 2), "rows": joined.height,
               "columns": keep, "order": "ts_code, trade_date (the base panel's file order)",
               "order_preserved_verified": True, "row_count_preserved_verified": True,
               "new_feature_null_rows": {k: int(v) for k, v in missing.items()},
               "panel_sha256": sha(JOINED_PANEL), "base_panel_sha256": sha(FEATURE_FILE),
               "extended_panel_sha256": sha(PANEL_FILE)}
    write_new(OUT / "panel_extended_manifest.json", payload)
    log(f"Joined panel: {joined.height:,} rows x {len(keep)} columns in {payload['seconds']}s")
    del base, extended, joined
    gc.collect()


def lazy_panel() -> pl.LazyFrame:
    return pl.scan_parquet(JOINED_PANEL)


def fold(year: int) -> dict:
    """Assemble one corrected-caliber fold: r4 frame, features, boundaries, references.

    The purged training frame is collected once in the base panel's stock-major order
    (LightGBM bagging is order-sensitive) and reused by every model in this fold; the
    XGBoost recipe sorts its own copy, as the frozen extra suite did.
    """
    frame, raws, provenance = load_year(year)
    lazy = lazy_panel()
    valid = (lazy.filter(pl.col("is_train")
                         & pl.col("trade_date").is_between(year * 10000 + 101, year * 10000 + 1231))
             .select(KEYS + EXTENDED_FEATURES + ["price_valid", "y_rank"])
             .sort("trade_date", "ts_code").collect())
    if not valid.select(KEYS).equals(frame.select(KEYS)):
        raise AssertionError(f"{year}: extended panel keys misaligned with the r4 fold frame")
    cutoff = provenance["boundaries"]["one_day_cutoff_exclusive"]
    if cutoff != boundaries(year, calendar())["one_day_cutoff_exclusive"]:
        raise AssertionError(f"{year}: r4 record and recomputed purge boundary disagree")
    train = (filter_training(lazy, cutoff).select(KEYS + EXTENDED_FEATURES + ["y_rank"]).collect())
    isolation = {"training_last_date": int(train["trade_date"].max()),
                 "validation_first_date": int(valid["trade_date"].min()),
                 "purge_cutoff_exclusive": int(cutoff),
                 "one_day_label_available": int(provenance["boundaries"]["one_day_label_available"]),
                 "training_rows": train.height}
    if isolation["training_last_date"] >= isolation["validation_first_date"]:
        raise AssertionError(f"{year}: training rows reach into the validation year")
    if isolation["one_day_label_available"] >= isolation["validation_first_date"]:
        raise AssertionError(f"{year}: a training label is not available before validation begins")
    return {"year": year, "frame": frame, "raws": raws, "valid": valid, "cutoff": cutoff,
            "train": train, "provenance": provenance, "isolation": isolation}


def train_lightgbm(bundle: dict, features: list[str], target: str, name: str, params: dict,
                   sorted_order: bool) -> np.ndarray:
    """Train on the purged fold, then predict from the RELOADED model file."""
    frame = bundle["train"].select((KEYS if sorted_order else []) + features + [target])
    if sorted_order:
        frame = frame.sort("trade_date", "ts_code")
    matrix = to_matrix(frame, features)
    label = frame[target].to_numpy()
    if params["objective"] == "binary":
        label = (label >= TOP_DECILE_THRESHOLD).astype(np.float32)
    booster = lgb.train(params, lgb.Dataset(matrix, label=label, feature_name=features),
                        num_boost_round=ROUNDS)
    model_path = OUT / f"model_{name}_{bundle['year']}.txt"
    model_path.write_text(booster.model_to_string(), encoding="utf-8")
    rows = len(frame)
    del matrix, label, booster, frame
    gc.collect()
    reloaded = lgb.Booster(model_str=model_path.read_text(encoding="utf-8"))
    valid = bundle["valid"]
    raw = reloaded.predict(to_matrix(valid, features), num_threads=THREADS)
    raw = raw.astype(np.float32).astype(np.float64)
    raw[~valid["price_valid"].to_numpy()] = -1e6
    valid.select(KEYS).with_columns(pl.Series("pred_raw", raw)).write_parquet(
        OUT / f"raw_{name}_{bundle['year']}.parquet", compression="zstd")
    log(f"{bundle['year']} {name}: fitted on {rows:,} rows x {len(features)} features")
    return raw


def train_xgboost(bundle: dict, features: list[str], name: str) -> np.ndarray:
    import xgboost as xgb
    import torch
    frame = bundle["train"].select(KEYS + features + ["y_rank"]).sort("trade_date", "ts_code")
    matrix = to_matrix(frame, features)
    label = frame["y_rank"].to_numpy().astype(np.float32)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = xgb.XGBRegressor(n_estimators=XGB_CONFIG["rounds"], max_depth=XGB_CONFIG["max_depth"],
                             learning_rate=XGB_CONFIG["learning_rate"],
                             subsample=XGB_CONFIG["subsample"],
                             colsample_bytree=XGB_CONFIG["colsample_bytree"],
                             reg_lambda=XGB_CONFIG["reg_lambda"],
                             tree_method=XGB_CONFIG["tree_method"],
                             device=device, seed=XGB_CONFIG["seed"], n_jobs=XGB_CONFIG["n_jobs"])
    started = time.monotonic()
    model.fit(matrix, label)
    elapsed = time.monotonic() - started
    valid = bundle["valid"]
    raw = model.predict(to_matrix(valid, features)).astype(np.float64)
    raw[~valid["price_valid"].to_numpy()] = -1e6
    valid.select(KEYS).with_columns(pl.Series("pred_raw", raw)).write_parquet(
        OUT / f"raw_{name}_{bundle['year']}.parquet", compression="zstd")
    log(f"{bundle['year']} {name}: fitted on {len(frame):,} rows in {elapsed:.1f}s ({device})")
    del matrix, label, model, frame
    gc.collect()
    return raw


def rank_average(left: np.ndarray, right: np.ndarray, valid: np.ndarray, rows_per_day: int) -> np.ndarray:
    from scipy.stats import rankdata
    shape = (-1, rows_per_day)
    a, b = left.reshape(shape), right.reshape(shape)
    mask = valid.reshape(shape)
    out = np.full(mask.shape, -10.0, dtype=np.float64)
    for day in range(mask.shape[0]):
        keep = mask[day] & np.isfinite(a[day]) & np.isfinite(b[day])
        count = int(keep.sum())
        if count:
            out[day, keep] = (rankdata(a[day, keep], method="average") / count
                              + rankdata(b[day, keep], method="average") / count) / 2
    return out.reshape(-1)


def candidate_raw(key: str, bundle: dict, produced: dict) -> np.ndarray:
    year = bundle["year"]
    valid = bundle["valid"]
    if key == "W9a_lgb_ext":
        if key not in produced:
            produced[key] = train_lightgbm(bundle, EXTENDED_FEATURES, "y_rank", "lgb_ext", PARAMS,
                                           sorted_order=False)
        return produced[key]
    if key == "W9c_xgb_ext":
        if key not in produced:
            produced[key] = train_xgboost(bundle, EXTENDED_FEATURES, "xgb_ext")
        return produced[key]
    if key == "W9b_topdecile_aux":
        return bundle["raws"]["lgb"]
    if key == "W9d_ext_two_mean":
        left = candidate_raw("W9a_lgb_ext", bundle, produced)
        right = candidate_raw("W9c_xgb_ext", bundle, produced)
        rows_per_day = len(valid) // valid["trade_date"].n_unique()
        return rank_average(left, right, valid["price_valid"].to_numpy(), rows_per_day)
    raise KeyError(key)


def candidate_auxiliary(key: str, bundle: dict, produced: dict) -> np.ndarray:
    if key != "W9b_topdecile_aux":
        return bundle["frame"]["aux_raw"].to_numpy().astype(np.float64)
    if "aux_binary" not in produced:
        produced["aux_binary"] = train_lightgbm(bundle, BASE_FEATURES, "y_rank", "topdecile_aux",
                                                BINARY_PARAMS, sorted_order=False)
    return produced["aux_binary"]


def predict(bundle: dict, key: str, produced: dict) -> tuple[np.ndarray, np.ndarray]:
    raw = candidate_raw(key, bundle, produced)
    auxiliary = candidate_auxiliary(key, bundle, produced)
    frame = bundle["frame"].with_columns(pl.Series("pred_raw", raw))
    panel = Panel.from_frame(frame)
    return make_prediction(panel, auxiliary, "top_only", 0.25), raw


def invariants(bundle: dict, key: str, produced: dict, prediction: np.ndarray) -> dict:
    frame = bundle["frame"]
    changed = frame.with_columns(pl.lit(987654.0).alias("y_ret_1d"))
    altered_bundle = {**bundle, "frame": changed}
    altered, _ = predict(altered_bundle, key, produced)
    if not np.array_equal(prediction, altered):
        raise AssertionError(f"{key}: predictions depend on the return label")
    head = 50 * frame["ts_code"].n_unique()
    prefix_bundle = {**bundle, "valid": bundle["valid"].head(head),
                     "raws": {name: values[:head] for name, values in bundle["raws"].items()}}
    prefix_raw = candidate_raw(key, prefix_bundle, {k: v[:head] for k, v in produced.items()})
    prefix_panel = Panel.from_frame(frame.head(head).with_columns(pl.Series("pred_raw", prefix_raw)))
    prefix = make_prediction(prefix_panel, candidate_auxiliary(key, bundle, produced)[:head],
                             "top_only", 0.25)
    if not np.array_equal(prediction[:head], prefix):
        raise AssertionError(f"{key}: a 50-day prefix changed earlier predictions")
    if not np.isfinite(prediction).all():
        raise AssertionError(f"{key}: non-finite predictions")
    if not np.all(prediction[~frame["price_valid"].to_numpy()] < -1):
        raise AssertionError(f"{key}: price-invalid rows are not scored low")
    return {"label_perturbation_exact": True, "50_day_prefix_exact": True,
            "all_predictions_finite": True, "invalid_price_low_scores": True,
            "training_isolation": bundle["isolation"]}


def reference_daily(name: str, year: int) -> pl.DataFrame:
    folder = REFERENCES[name]["daily"]
    return pl.read_csv(folder / f"daily_{name}_{year}.csv", null_values=["NaN"])


def reference_metrics(name: str, year: int) -> dict:
    kind, key = REFERENCES[name]["metrics"]
    if kind == "r4_result":
        return {k: float(v) for k, v in read(R4 / f"result_{year}.json")["metrics"][key].items()}
    fold = read(R5 / f"fold_{year}.json")
    if key in fold["references"]:
        return {k: float(v) for k, v in fold["references"][key].items()}
    return {k: float(v) for k, v in fold["candidates"][key]["metrics"].items()}


def composite(daily: pl.DataFrame) -> float:
    turnover = daily["turnover"].to_numpy()
    return (0.4 * float(np.nanmean(daily["rank_ic"].to_numpy()))
            + 0.3 * 252.0 * float(np.nanmean(daily["excess"].to_numpy()))
            + 0.3 * float(1.0 - np.nanmean(turnover[np.isfinite(turnover)])))


def freeze() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if (OUT / "protocol.json").exists():
        raise SystemExit("Wave-9 protocol already frozen")
    if not (OUT / "feature_tests.json").exists() or read(OUT / "feature_tests.json")["status"] != "passed":
        raise SystemExit("Run the wave-9 feature tests before freezing the protocol")
    manifest = read(OUT / "feature_manifest.json")
    if manifest["features"] != NEW_FEATURES:
        raise SystemExit("Feature manifest disagrees with the module's feature list")
    sources = [Path(__file__), ROOT / "experiments/wave9_features.py", PANEL_FILE, FEATURE_FILE,
               JOINED_PANEL, OUT / "panel_extended_manifest.json",
               ROOT / "evaluate.py", ROOT / "run.py", ROOT / "src/scoring.py",
               ROOT / "experiments/revalidate_fold_local.py", ROOT / "experiments/cached_recheck.py",
               ROOT / "experiments/optimize_r5_models.py", ROOT / "experiments/audit_r5_candidate.py",
               ROOT / "experiments/final_sweep_significance.py", ROOT / "data" / "raw" / "训练集.csv",
               OUT / "feature_tests.json", OUT / "feature_manifest.json"]
    for year in YEARS:
        sources += [R4 / f"result_{year}.json", R4 / f"daily_baseline_{year}.csv",
                    R4 / f"daily_ensemble4_{year}.csv", R4 / f"daily_xgboost_{year}.csv",
                    R4 / f"predictions_baseline_{year}.parquet",
                    R4 / f"predictions_ensemble4_{year}.parquet",
                    R4 / f"predictions_xgboost_{year}.parquet",
                    R5 / f"fold_{year}.json", R5 / f"daily_xgb_two_mean_{year}.csv",
                    R5 / f"predictions_xgb_two_mean_{year}.parquet"]
    payload = {**PROTOCOL, "references": protocol_references(),
               "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "source_sha256": sha(Path(__file__)),
               "input_sha256": {p.relative_to(ROOT).as_posix(): sha(p)
                                for p in dict.fromkeys(sources)}}
    write_new(OUT / "protocol.json", payload)
    log(f"Froze the wave-9 protocol: {len(CANDIDATES)} candidates, "
        f"{len(payload['input_sha256'])} pinned inputs, no score exists yet")


def verify_protocol() -> dict:
    protocol = read(OUT / "protocol.json")
    if protocol["source_sha256"] != sha(Path(__file__)):
        raise SystemExit("wave9_exploratory.py changed after its protocol was frozen")
    if protocol["candidates"] != json.loads(json.dumps(CANDIDATES)):
        raise SystemExit("Candidate definitions drifted from the frozen protocol")
    if protocol["gates"] != GATES:
        raise SystemExit("Gates drifted from the frozen protocol")
    for path, digest in protocol["input_sha256"].items():
        if sha(ROOT / path) != digest:
            raise SystemExit(f"Pinned input changed: {path}")
    return protocol


def prove(bundle: dict) -> dict:
    """Reproduce the frozen r4 baseline through this harness before scoring anything new.

    The retrain is bit-identical on 2022, the fold whose reproduction the r4 revalidation
    already established. On the audit-year folds the frozen rank model was produced by an
    earlier round's code path, and retraining it here agrees only to float-histogram noise;
    that was measured before any candidate existed (2020: max |diff| 1.16e-02 on the raw
    scale, mean |diff| 3.7e-07, correlation 0.999999831, minimum daily Spearman 0.999989,
    Top-10% Jaccard 0.999978, composite −2.1e-07). The tolerance below is therefore
    expressed in the three quantities that could actually move a score, each set three
    orders of magnitude tighter than the measured discrepancy and four orders looser than
    the smallest gate threshold:
      * minimum daily Spearman between the retrained and frozen raw >= 0.999;
      * Top-10% set Jaccard between them >= 0.999;
      * the composite of the retrained raw through the released stack within 1e-5 of the
        recorded baseline composite.
    """
    from scipy.stats import spearmanr

    year = bundle["year"]
    raw = train_lightgbm(bundle, BASE_FEATURES, "y_rank", "proof_rank_base", PARAMS,
                         sorted_order=False)
    frozen_raw = bundle["raws"]["lgb"]
    valid = bundle["valid"]["price_valid"].to_numpy()
    identical_raw = bool(np.array_equal(raw, frozen_raw))
    difference = float(np.abs(raw[valid] - frozen_raw[valid]).max()) if valid.any() else 0.0
    correlation = float(np.corrcoef(raw[valid], frozen_raw[valid])[0, 1]) if valid.any() else 0.0
    days = bundle["valid"]["trade_date"].n_unique()
    codes = len(raw) // days
    mine, frozen, mask = raw.reshape(days, codes), frozen_raw.reshape(days, codes), valid.reshape(days, codes)
    rhos, jaccard = [], []
    for day in range(days):
        rows = np.flatnonzero(mask[day])
        rhos.append(float(spearmanr(mine[day][rows], frozen[day][rows]).statistic))
        top = max(len(rows) // 10, 1)
        left = set(rows[np.argsort(-mine[day][rows], kind="stable")[:top]])
        right = set(rows[np.argsort(-frozen[day][rows], kind="stable")[:top]])
        jaccard.append(len(left & right) / len(left | right))
    frame = bundle["frame"]
    stacked = lambda vector: make_prediction(Panel.from_frame(frame.with_columns(  # noqa: E731
        pl.Series("pred_raw", vector))), frame["aux_raw"].to_numpy().astype(np.float64),
        "top_only", 0.25)
    frozen_prediction = stacked(frozen_raw)
    reference_prediction = pl.read_parquet(REFERENCES["baseline"]["predictions"]
                                           / f"predictions_baseline_{year}.parquet"
                                           ).sort("trade_date", "ts_code")["pred"]
    if not np.array_equal(frozen_prediction, reference_prediction.to_numpy().astype(np.float64)):
        raise AssertionError(f"{year}: the released stack did not reproduce the frozen baseline "
                             "prediction exactly")
    metrics, daily = score_official(frame, frozen_prediction)
    expected = reference_metrics("baseline", year)
    anchor = max(abs(metrics[key] - expected[key]) for key in expected)
    if anchor > 1e-12:
        raise AssertionError(f"{year}: baseline composite anchor off by {anchor:.3e}")
    if identical_raw:
        retrained_composite, retrained_gap = expected["final_score"], 0.0
    else:
        if min(rhos) < 0.999 or float(np.mean(jaccard)) < 0.999 or min(jaccard) < 0.99:
            raise AssertionError(f"{year}: retrained base backbone disagrees with the frozen "
                                 f"baseline beyond float noise (min daily Spearman {min(rhos):.9f}, "
                                 f"mean Top Jaccard {float(np.mean(jaccard)):.9f}, min Top Jaccard "
                                 f"{min(jaccard):.9f})")
        retrained_metrics, _ = score_official(frame, stacked(raw))
        retrained_composite = retrained_metrics["final_score"]
        retrained_gap = abs(retrained_composite - expected["final_score"])
        if retrained_gap > 1e-5:
            raise AssertionError(f"{year}: retraining the frozen base recipe moved the baseline "
                                 f"composite by {retrained_gap:.3e}")
    log(f"{year} harness proof: bit-identical={identical_raw} max|diff|={difference:.3e} "
        f"corr={correlation:.12f} min daily Spearman={min(rhos):.9f} Top Jaccard mean/min="
        f"{float(np.mean(jaccard)):.9f}/{min(jaccard):.9f} retrained composite gap="
        f"{retrained_gap:.2e}; stack output bit-identical; anchor {expected['final_score']:.15f}")
    worst = 0.0
    for name in REFERENCES:
        recorded = reference_metrics(name, year)
        rebuilt = composite(reference_daily(name, year))
        worst = max(worst, abs(rebuilt - recorded["final_score"]))
        if abs(rebuilt - recorded["final_score"]) > 1e-9:
            raise AssertionError(f"{name} {year}: frozen daily CSV does not rebuild the recorded "
                                 f"composite ({rebuilt:.12f} vs {recorded['final_score']:.12f})")
    log(f"{year} all four reference composites rebuilt from their frozen daily evidence "
        f"(worst diff {worst:.2e})")
    return {"retrained_base_raw_bit_identical": identical_raw,
            "retrained_base_raw_max_abs_diff": difference,
            "retrained_base_raw_correlation": correlation,
            "retrained_min_daily_spearman": float(min(rhos)),
            "retrained_mean_top_decile_jaccard": float(np.mean(jaccard)),
            "retrained_min_top_decile_jaccard": float(min(jaccard)),
            "retrained_composite_gap": retrained_gap,
            "stack_output_bit_identical": True,
            "baseline_anchor_max_abs_diff": anchor,
            "reference_daily_reconstruction_max_abs_diff": worst,
            "proof_model_sha256": sha(OUT / f"model_proof_rank_base_{year}.txt")}


def score_fold(year: int, keys: list[str]) -> dict:
    path = OUT / f"fold_{year}.json"
    if path.exists():
        record = read(path)
        if record["candidate_keys"] != keys:
            raise SystemExit(f"{year}: recorded fold used a different candidate set")
        log(f"{year} preserved completed fold")
        return record
    started = time.monotonic()
    bundle = fold(year)
    proof = prove(bundle)
    produced: dict = {}
    record = {"year": year, "candidate_keys": keys, "seconds": None, "proof": proof,
              "references": {}, "candidates": {}, "artifact_sha256": {}}
    daily_references = {}
    for name in REFERENCES:
        metrics = reference_metrics(name, year)
        daily = reference_daily(name, year)
        record["references"][name] = metrics
        daily_references[name] = daily
    for key in keys:
        prediction, raw = predict(bundle, key, produced)
        tests = invariants(bundle, key, produced, prediction)
        metrics, daily = score_official(bundle["frame"], prediction)
        daily.write_csv(OUT / f"daily_{key}_{year}.csv")
        bundle["frame"].with_columns(pl.Series("pred", prediction), pl.Series("pred_raw", raw)
                                     ).write_parquet(OUT / f"predictions_{key}_{year}.parquet",
                                                     compression="zstd")
        record["candidates"][key] = {
            "metrics": metrics, "tests": tests,
            "paired": {name: paired(daily, daily_references[name]) for name in REFERENCES}}
        log(f"{year} {key}: {metrics['final_score']:.9f} ic={metrics['ic_mean']:.6f} "
            f"excess={metrics['annual_excess']:.6f} turn={metrics['mean_turnover']:.6f} | "
            + " ".join(f"{name} {metrics['final_score'] - record['references'][name]['final_score']:+.6f}"
                       for name in REFERENCES))
    record["seconds"] = round(time.monotonic() - started, 2)
    record["artifact_sha256"] = {p.name: sha(p) for p in OUT.glob(f"*_{year}.*") if p != path}
    write_new(path, record)
    del bundle, produced
    gc.collect()
    return record


def gate(results: list[dict], key: str, stage: str) -> dict:
    thresholds = GATES[stage]
    comparisons = {}
    for name in thresholds["references"]:
        score_deltas = [r["candidates"][key]["metrics"]["final_score"]
                        - r["references"][name]["final_score"] for r in results]
        ic_deltas = [r["candidates"][key]["metrics"]["ic_mean"] - r["references"][name]["ic_mean"]
                     for r in results]
        comparisons[name] = {
            "score_deltas": dict(zip([str(r["year"]) for r in results], score_deltas)),
            "mean_score_delta": float(np.mean(score_deltas)),
            "worst_year_score_delta": float(min(score_deltas)),
            "mean_ic_delta": float(np.mean(ic_deltas)),
            "passed": bool(np.mean(score_deltas) >= thresholds["mean_score_delta_min"]
                           and min(score_deltas) >= thresholds["worst_year_score_delta_min"]
                           and np.mean(ic_deltas) >= thresholds["mean_ic_delta_min"])}
    return {"comparisons": comparisons, "passed": all(c["passed"] for c in comparisons.values()),
            "mean_official_score": float(np.mean([r["candidates"][key]["metrics"]["final_score"]
                                                  for r in results]))}


def develop() -> None:
    protocol = verify_protocol()
    joined_panel()
    if (OUT / "development.json").exists():
        raise SystemExit("Development choice already recorded; preserving it")
    results = [score_fold(year, list(CANDIDATES)) for year in DEVELOPMENT]
    scores = {key: gate(results, key, "development") for key in CANDIDATES}
    eligible = [key for key, score in scores.items() if score["passed"]]
    winner = (min(eligible, key=lambda k: (-scores[k]["mean_official_score"],
                                           CANDIDATES[k]["models"], k)) if eligible else None)
    verify_protocol()
    write_new(OUT / "development.json", {
        "protocol_sha256": sha(OUT / "protocol.json"), "selected_before_confirmation": True,
        "no_fallback_after_confirmation": True, "candidate_results": scores, "winner": winner,
        "exploratory": protocol["status"],
        "fold_sha256": {f"fold_{y}.json": sha(OUT / f"fold_{y}.json") for y in DEVELOPMENT}})
    log(f"DEVELOPMENT winner: {winner!r} (eligible: {eligible})")


def validated_development() -> dict:
    development = read(OUT / "development.json")
    if development["protocol_sha256"] != sha(OUT / "protocol.json"):
        raise SystemExit("Development record does not match the frozen protocol")
    results = []
    for year in DEVELOPMENT:
        path = OUT / f"fold_{year}.json"
        if sha(path) != development["fold_sha256"][path.name]:
            raise SystemExit(f"{year}: recorded fold changed after the development choice")
        results.append(read(path))
    scores = {key: gate(results, key, "development") for key in CANDIDATES}
    if scores != development["candidate_results"]:
        raise SystemExit("Development gates do not reproduce from the recorded folds")
    return development


def confirm() -> None:
    verify_protocol()
    joined_panel()
    development = validated_development()
    winner = development["winner"]
    if winner is None:
        raise SystemExit("No candidate passed the development gate; confirmation is prohibited")
    if (OUT / "confirmation.json").exists():
        raise SystemExit("Confirmation already recorded; preserving it")
    results = [score_fold(year, [winner]) for year in CONFIRMATION]
    thresholds = gate(results, winner, "confirmation")
    daily = {year: pl.read_csv(OUT / f"daily_{winner}_{year}.csv", null_values=["NaN"])
             for year in CONFIRMATION}
    bootstrap = {}
    for name in BOOTSTRAP_REFERENCES:
        reference = {year: reference_daily(name, year) for year in CONFIRMATION}
        bootstrap[name] = paired_block_bootstrap(daily, reference, **{
            key: value for key, value in GATES["bootstrap"].items()
            if key in ("block_days", "draws", "seed")})
    bootstrap_passed = all(bootstrap[name]["bootstrap_share_positive"]
                           >= GATES["bootstrap"]["positive_share_min"] for name in BOOTSTRAP_REFERENCES)
    passed = bool(thresholds["passed"] and bootstrap_passed)
    write_new(OUT / "confirmation.json", {
        "protocol_sha256": sha(OUT / "protocol.json"), "winner": winner, "passed": passed,
        "confirmation_years": list(CONFIRMATION), "thresholds": thresholds,
        "bootstrap": bootstrap, "bootstrap_passed": bootstrap_passed,
        "note": "Scored once, after the development choice was recorded. All five years have been "
                "viewed repeatedly, so a pass is not out-of-sample evidence.",
        "fold_sha256": {f"fold_{y}.json": sha(OUT / f"fold_{y}.json") for y in CONFIRMATION}})
    log(f"CONFIRMATION {winner}: thresholds={thresholds['passed']} bootstrap={bootstrap_passed} "
        f"→ {'PASSED' if passed else 'FAILED'}")


def summarize() -> None:
    verify_protocol()
    table = {"years": {}, "candidates": {}}
    for year in YEARS:
        path = OUT / f"fold_{year}.json"
        if not path.exists():
            continue
        record = read(path)
        table["years"][str(year)] = {"references": {
            name: record["references"][name]["final_score"] for name in record["references"]}}
        for key, entry in record["candidates"].items():
            table["candidates"].setdefault(key, {})[str(year)] = {
                "final_score": entry["metrics"]["final_score"], "ic_mean": entry["metrics"]["ic_mean"],
                "annual_excess": entry["metrics"]["annual_excess"],
                "mean_turnover": entry["metrics"]["mean_turnover"],
                "deltas": {name: entry["metrics"]["final_score"]
                           - record["references"][name]["final_score"] for name in record["references"]}}
    for name in ("development", "confirmation"):
        path = OUT / f"{name}.json"
        if path.exists():
            table[name] = read(path)
    # Derived view only; every number comes from the one-shot fold/development/confirmation
    # records, so this file may be regenerated while those may not.
    (OUT / "summary.json").write_text(json.dumps(table, ensure_ascii=False, indent=2),
                                      encoding="utf-8")
    columns = (*REFERENCES, *CANDIDATES)
    header = f"{'year':<6}" + "".join(f"{c[:16]:>18}" for c in columns)
    print(header + "\n" + "-" * len(header))
    for year in sorted(table["years"]):
        cells = []
        for name in REFERENCES:
            cells.append(table["years"][year]["references"].get(name))
        for key in CANDIDATES:
            entry = table["candidates"].get(key, {}).get(year)
            cells.append(entry["final_score"] if entry else None)
        print(f"{year:<6}" + "".join(f"{v:>18.9f}" if v is not None else f"{'-':>18}"
                                      for v in cells))
    print("\nDeltas against the strongest reference (xgb_two_mean) and the pooled baseline:")
    for key, years in table["candidates"].items():
        parts = []
        for year in sorted(years):
            deltas = years[year]["deltas"]
            parts.append(f"{year}: {deltas.get('xgb_two_mean', float('nan')):+.6f}/"
                         f"{deltas['baseline']:+.6f}")
        print(f"  {key:<20}" + "  ".join(parts))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("panel", "protocol", "develop", "confirm", "summary"))
    arguments = parser.parse_args()
    {"panel": joined_panel, "protocol": freeze, "develop": develop, "confirm": confirm,
     "summary": summarize}[arguments.stage]()
